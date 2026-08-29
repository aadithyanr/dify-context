from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from . import _base
from ._requests import build_brand_request


class GetBrandProfileTool(_base.ContextTool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        body = build_brand_request(tool_parameters)
        yield from self.json_result(
            self.client.post("/brand/retrieve", body=body, timeout_seconds=70)
        )
