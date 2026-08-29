from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

API_BASE_URL = "https://api.context.dev/v1"
DEFAULT_TIMEOUT_SECONDS = 120


class ContextApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class ContextApiClient:
    api_key: str

    @classmethod
    def from_credentials(cls, credentials: dict[str, Any]) -> ContextApiClient:
        api_key = str(credentials.get("api_key") or "").strip()
        if not api_key:
            raise ValueError("A Context.dev API key is required.")
        return cls(api_key=api_key)

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> dict[str, Any]:
        return self._request(
            "GET", path, params=params, timeout_seconds=timeout_seconds
        )

    def post(
        self,
        path: str,
        *,
        body: dict[str, Any],
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> dict[str, Any]:
        return self._request("POST", path, body=body, timeout_seconds=timeout_seconds)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        timeout_seconds: int,
    ) -> dict[str, Any]:
        try:
            response = requests.request(
                method,
                f"{API_BASE_URL}{path}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "dify-context-dev/0.0.1",
                },
                params=normalize_query_params(params or {}),
                json=compact_dict(body or {}) if body is not None else None,
                timeout=timeout_seconds,
            )
        except requests.RequestException as error:
            raise ContextApiError(
                "Context.dev could not be reached. Try the request again."
            ) from error

        if not response.ok:
            raise ContextApiError(_error_message(response, self.api_key))

        try:
            payload = response.json()
        except ValueError as error:
            raise ContextApiError(
                "Context.dev returned an invalid JSON response."
            ) from error

        if not isinstance(payload, dict):
            raise ContextApiError("Context.dev returned an unexpected response shape.")
        return payload


def compact_dict(values: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in values.items() if value is not None and value != ""
    }


def normalize_query_params(values: dict[str, Any]) -> dict[str, Any]:
    return {
        key: "true" if value is True else "false" if value is False else value
        for key, value in compact_dict(values).items()
    }


def csv_values(value: Any) -> list[str] | None:
    if value in (None, ""):
        return None
    source = value if isinstance(value, list) else str(value).split(",")
    values = [str(item).strip() for item in source if str(item).strip()]
    return values or None


def _error_message(response: requests.Response, api_key: str) -> str:
    detail = ""
    try:
        payload = response.json()
        if isinstance(payload, dict):
            detail = str(payload.get("message") or payload.get("error") or "").strip()
    except ValueError:
        detail = ""

    if detail:
        safe_detail = detail.replace(api_key, "[redacted]")
        return (
            f"Context.dev request failed ({response.status_code}): {safe_detail[:300]}"
        )
    return f"Context.dev request failed with HTTP {response.status_code}."
