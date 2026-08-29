from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from . import _base
from ._requests import build_search_request


class SearchWebTool(_base.ContextTool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        body = build_search_request(tool_parameters)
        yield from self.json_result(
            self.client.post("/web/search", body=body, timeout_seconds=70)
        )
