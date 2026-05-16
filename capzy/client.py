"""Sync HTTP client for the Capzy API.

Most callers want the module-level shortcuts (`capzy.solve(...)`),
not this class. Use ``CapzyClient`` directly only when you need to
inject a custom ``requests.Session`` (proxy, retries, custom TLS).
"""

from __future__ import annotations

import time
from typing import Any, Mapping
from urllib.parse import urljoin

import requests

from capzy._version import __version__
from capzy.exceptions import (
    ApiError,
    CapzyError,
    TaskFailedError,
    TaskTimeoutError,
)

DEFAULT_BASE_URL = "https://api.capzy.ai"
DEFAULT_TIMEOUT = 30.0       # per-request HTTP timeout
DEFAULT_POLL_INTERVAL = 2.0  # seconds between getTaskResult polls
DEFAULT_MAX_WAIT = 180.0     # cap on total polling time per .solve()


# snake_case → camelCase wire-name remap. Anything not listed passes
# through untouched, so you can also just write camelCase directly.
_KEY_RENAME = {
    "website_url": "websiteURL",
    "website_key": "websiteKey",
    "website_public_key": "websitePublicKey",
    "is_invisible": "isInvisible",
    "is_enterprise": "isEnterprise",
    "page_action": "pageAction",
    "min_score": "minScore",
    "api_domain": "apiDomain",
    "enterprise_payload": "enterprisePayload",
    "data_s": "data-s",
    "user_agent": "userAgent",
    "proxy_address": "proxyAddress",
    "proxy_port": "proxyPort",
    "proxy_login": "proxyLogin",
    "proxy_password": "proxyPassword",
    "proxy_type": "proxyType",
    "captcha_id": "captchaId",
    "captcha_url": "captchaUrl",
    "geetest_api_server_subdomain": "geetestApiServerSubdomain",
    "geetest_get_lib": "geetestGetLib",
    "funcaptcha_api_js_subdomain": "funcaptchaApiJSSubdomain",
    "case_sensitive": "case",
    "min_length": "minLength",
    "max_length": "maxLength",
    "app_id": "appId",
    "validate_id": "validateId",
    "aws_key": "awsKey",
    "aws_iv": "awsIv",
    "aws_context": "awsContext",
    "aws_challenge_js": "awsChallengeJS",
    "package_name": "packageName",
    "device_id": "deviceId",
    "device_name": "deviceName",
}


def _camelize_params(params: Mapping[str, Any]) -> dict[str, Any]:
    """Pass-through with snake_case keys auto-converted, None values dropped."""
    out: dict[str, Any] = {}
    for k, v in params.items():
        if v is None:
            continue
        out[_KEY_RENAME.get(k, k)] = v
    return out


class CapzyClient:
    """Lower-level handle. Most callers use the module-level functions.

    Args:
        api_key:   API key from https://capzy.ai/dashboard
        base_url:  override the API root (defaults to api.capzy.ai)
        timeout:   per-request HTTP timeout in seconds
        session:   inject a custom ``requests.Session``
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        session: requests.Session | None = None,
    ) -> None:
        if not api_key:
            raise ValueError(
                "api_key is required (get one at https://capzy.ai/dashboard)"
            )
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self._session = session or requests.Session()
        self._session.headers.setdefault("User-Agent", f"capzy-python/{__version__}")
        self._session.headers.setdefault("Accept", "application/json")

    # ── Public methods ──────────────────────────────────────────────────

    def get_balance(self) -> float:
        body = self._post("getBalance", {"clientKey": self.api_key})
        return float(body.get("balance", 0.0))

    def create_task(self, *, type: str, **params: Any) -> dict[str, Any]:
        """Submit a task — returns the raw createTask response."""
        task_body = {"type": type, **_camelize_params(params)}
        return self._post(
            "createTask",
            {"clientKey": self.api_key, "task": task_body},
        )

    def get_task_result(self, task_id: str) -> dict[str, Any]:
        return self._post(
            "getTaskResult",
            {"clientKey": self.api_key, "taskId": task_id},
        )

    def report_score(
        self,
        task_id: str,
        score: float,
        action: str | None = None,
        hostname: str | None = None,
    ) -> None:
        """Report a reCAPTCHA v3 score for dashboard analytics."""
        self._post(
            "reportScore",
            {
                "clientKey": self.api_key,
                "taskId": task_id,
                "score": score,
                "action": action,
                "hostname": hostname,
            },
        )

    def solve(
        self,
        *,
        type: str,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        max_wait: float = DEFAULT_MAX_WAIT,
        **params: Any,
    ) -> dict[str, Any]:
        """Submit + poll until ready. Returns the ``solution`` dict.

        Raises:
            ApiError: createTask was rejected (e.g. bad key, wrong type).
            TaskFailedError: the task ran but failed (refunded).
            TaskTimeoutError: ``max_wait`` elapsed (refunded).
        """
        created = self.create_task(type=type, **params)

        # ImageToText / MathCaptcha return the solution synchronously.
        if created.get("solution"):
            return created["solution"]

        task_id = created.get("taskId")
        if not task_id:
            raise CapzyError("createTask did not return a taskId")

        server_timeout = created.get("timeout")
        if isinstance(server_timeout, (int, float)) and server_timeout > 0:
            max_wait = min(max_wait, float(server_timeout) + 5.0)

        deadline = time.monotonic() + max_wait
        while True:
            time.sleep(poll_interval)
            result = self.get_task_result(task_id)
            status = result.get("status")
            if status == "ready":
                return result.get("solution") or {}
            if status == "failed":
                raise TaskFailedError(
                    task_id,
                    result.get("errorCode"),
                    result.get("errorDescription"),
                )
            if time.monotonic() >= deadline:
                raise TaskTimeoutError(task_id, max_wait)

    # ── Internals ───────────────────────────────────────────────────────

    def _post(self, path: str, body: Mapping[str, Any]) -> dict[str, Any]:
        url = urljoin(self.base_url, path)
        clean = {k: v for k, v in body.items() if v is not None}
        try:
            resp = self._session.post(url, json=clean, timeout=self.timeout)
        except requests.RequestException as exc:
            raise CapzyError(f"network error talking to {url}: {exc}") from exc

        try:
            data = resp.json()
        except ValueError as exc:
            raise CapzyError(
                f"expected JSON from {url} (HTTP {resp.status_code}): "
                f"{resp.text[:200]}"
            ) from exc

        if not isinstance(data, dict):
            raise CapzyError(f"unexpected response shape from {url}: {data!r}")

        error_id = data.get("errorId", 0) or 0
        if error_id != 0:
            raise ApiError(
                error_id=int(error_id),
                error_code=data.get("errorCode"),
                error_description=data.get("errorDescription"),
                recommended_task_type=data.get("recommendedTaskType"),
                raw=data,
            )

        if resp.status_code >= 400:
            raise CapzyError(f"HTTP {resp.status_code} from {url}: {resp.text[:200]}")
        return data
