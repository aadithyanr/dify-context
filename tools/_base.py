from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import ContextApiClient


class ContextTool(Tool):
    @property
    def client(self) -> ContextApiClient:
        return ContextApiClient.from_credentials(self.runtime.credentials)

    def json_result(
        self, value: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        yield self.create_json_message(value)
