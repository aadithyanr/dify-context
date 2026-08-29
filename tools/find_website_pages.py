from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from . import _base
from ._requests import build_sitemap_params


class FindWebsitePagesTool(_base.ContextTool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        params = build_sitemap_params(tool_parameters)
        yield from self.json_result(
            self.client.get("/web/scrape/sitemap", params=params, timeout_seconds=70)
        )
