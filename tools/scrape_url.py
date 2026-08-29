from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from . import _base
from ._requests import build_scrape_params


class ScrapeUrlTool(_base.ContextTool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        params = build_scrape_params(tool_parameters)
        result = self.client.get(
            "/web/scrape/markdown", params=params, timeout_seconds=70
        )
        markdown = result.get("markdown")
        if isinstance(markdown, str) and markdown:
            yield self.create_text_message(markdown)
        yield from self.json_result(result)
