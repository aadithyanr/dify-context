from __future__ import annotations

from typing import Any

import pytest
import requests

from tools._client import (
    API_BASE_URL,
    ContextApiClient,
    ContextApiError,
    csv_values,
    normalize_query_params,
)


class FakeResponse:
    def __init__(self, status_code: int, payload: Any):
        self.status_code = status_code
        self.ok = 200 <= status_code < 300
        self._payload = payload

    def json(self) -> Any:
        return self._payload


def test_client_sends_bearer_auth_to_fixed_production_api(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_request(method: str, url: str, **kwargs: Any) -> FakeResponse:
        captured.update(method=method, url=url, **kwargs)
        return FakeResponse(200, {"success": True})

    monkeypatch.setattr(requests, "request", fake_request)

    result = ContextApiClient("ctxt_secret_test").post(
        "/web/search",
        body={"query": "Context.dev", "empty": ""},
        timeout_seconds=17,
    )

    assert result == {"success": True}
    assert captured["method"] == "POST"
    assert captured["url"] == f"{API_BASE_URL}/web/search"
    assert captured["headers"]["Authorization"] == "Bearer ctxt_secret_test"
    assert captured["json"] == {"query": "Context.dev"}
    assert captured["timeout"] == 17


def test_client_redacts_api_key_from_api_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api_key = "ctxt_secret_should_never_escape"
    monkeypatch.setattr(
        requests,
        "request",
        lambda *args, **kwargs: FakeResponse(401, {"message": f"invalid {api_key}"}),
    )

    with pytest.raises(ContextApiError) as error:
        ContextApiClient(api_key).get("/monitors/limits")

    assert api_key not in str(error.value)
    assert "[redacted]" in str(error.value)


def test_client_normalizes_network_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*args: Any, **kwargs: Any) -> None:
        raise requests.Timeout("request details")

    monkeypatch.setattr(requests, "request", fail)

    with pytest.raises(ContextApiError, match="could not be reached"):
        ContextApiClient("ctxt_secret_test").get("/monitors/limits")


def test_csv_values_cleans_empty_values() -> None:
    assert csv_values("context.dev, docs.context.dev, ") == [
        "context.dev",
        "docs.context.dev",
    ]
    assert csv_values("") is None


def test_query_params_serialize_booleans_for_api_validation() -> None:
    assert normalize_query_params(
        {"enabled": True, "disabled": False, "empty": None}
    ) == {
        "enabled": "true",
        "disabled": "false",
    }
