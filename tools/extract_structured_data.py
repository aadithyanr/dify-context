from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from . import _base
from ._requests import build_extract_request


class ExtractStructuredDataTool(_base.ContextTool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        body = build_extract_request(tool_parameters)
        yield from self.json_result(
            self.client.post("/web/extract", body=body, timeout_seconds=130)
        )
