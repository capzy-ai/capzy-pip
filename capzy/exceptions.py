"""Exceptions raised by the Capzy SDK."""

from __future__ import annotations

from typing import Any


class CapzyError(Exception):
    """Base class for every error raised by this SDK."""


class ApiError(CapzyError):
    """The API returned a non-zero errorId.

    Attributes:
        error_id: numeric errorId from the response.
        error_code: short string code (e.g. "ERROR_KEY_DOES_NOT_EXIST").
        error_description: human-readable explanation.
        recommended_task_type: set when the API hints the caller picked
            the wrong task type for the sitekey.
        raw: full decoded JSON body, for debugging.
    """

    def __init__(
        self,
        error_id: int,
        error_code: str | None,
        error_description: str | None,
        recommended_task_type: str | None = None,
        raw: dict[str, Any] | None = None,
    ) -> None:
        self.error_id = error_id
        self.error_code = error_code
        self.error_description = error_description
        self.recommended_task_type = recommended_task_type
        self.raw = raw or {}
        msg = f"[{error_code or error_id}] {error_description or 'API error'}"
        if recommended_task_type:
            msg += f" (hint: try {recommended_task_type})"
        super().__init__(msg)


class TaskFailedError(CapzyError):
    """getTaskResult returned status='failed'."""

    def __init__(self, task_id: str, error_code: str | None, error_description: str | None) -> None:
        self.task_id = task_id
        self.error_code = error_code
        self.error_description = error_description
        super().__init__(
            f"Task {task_id} failed: [{error_code or '?'}] {error_description or 'no description'}"
        )


class TaskTimeoutError(CapzyError):
    """The task did not return a solution before the polling deadline."""

    def __init__(self, task_id: str, waited: float) -> None:
        self.task_id = task_id
        self.waited = waited
        super().__init__(f"Task {task_id} did not finish within {waited:.0f}s")
