"""Capzy — official Python SDK.

Quick start:

    from capzy import CapzyClient

    capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

    solution = capzy.solve(
        type="AntiTurnstileTaskProxyLess",
        website_url="https://example.com",
        website_key="0x4AAA...",
    )
    print(solution["token"])

Find your API key at https://capzy.ai/dashboard.
Every new account gets $0.10 in free credits — no card required.
"""

from capzy._version import __version__
from capzy.client import CapzyClient
from capzy.exceptions import (
    ApiError,
    CapzyError,
    TaskFailedError,
    TaskTimeoutError,
)

__all__ = [
    "__version__",
    "CapzyClient",
    "CapzyError",
    "ApiError",
    "TaskFailedError",
    "TaskTimeoutError",
]
