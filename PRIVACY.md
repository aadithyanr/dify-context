# Privacy Policy

Last updated: August 29, 2026

## Data processed

This plugin requires a Context.dev API key. Dify manages the stored credential and provides it to the plugin at runtime. The plugin sends that key to the fixed Context.dev API endpoint in an `Authorization` header.

Depending on the tool used, the plugin sends search queries, public domains or URLs, extraction schemas and instructions, and request options to Context.dev. Webpages reached through user-provided URLs may contain personal or other sensitive information selected by the user.

## Data use and sharing

The data is used only to perform the requested Context.dev API operation and return its response to the Dify workflow. The plugin communicates with Context.dev at `https://api.context.dev` and does not send data to any other third-party service.

The plugin does not independently log, sell, or persist API keys, queries, URLs, webpage content, or results. Context.dev processes requests according to the [Context.dev privacy policy](https://www.context.dev/privacy) and [terms of service](https://www.context.dev/term). Dify's handling of credentials and workflow data is governed by the user's Dify deployment and policies.

## Retention and deletion

The plugin itself has no database and retains no data between invocations. For information about data handled by Context.dev, including retention or deletion requests, see the [Context.dev privacy policy](https://www.context.dev/privacy).

## Contact

Privacy questions may be sent to [hello@context.dev](mailto:hello@context.dev).
