from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools._client import ContextApiClient, ContextApiError


class ContextDevProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            ContextApiClient.from_credentials(credentials).get(
                "/monitors/limits", timeout_seconds=15
            )
        except (ContextApiError, ValueError) as error:
            raise ToolProviderCredentialValidationError(str(error)) from error
