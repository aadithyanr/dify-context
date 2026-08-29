# Context.dev for Dify

Use [Context.dev](https://www.context.dev) in Dify workflows and agents for live web search, webpage scraping, website crawling, structured extraction, page discovery, and brand intelligence.

## Setup

1. Install the Context.dev plugin in Dify.
2. Create an API key in the [Context.dev dashboard](https://app.context.dev/api-keys).
3. Open the plugin credentials in Dify and enter the API key.

The plugin connects only to the production Context.dev API at `https://api.context.dev/v1`. It does not support custom API hosts.

## Tools

- **Search Web** searches the live web and can return cleaned page Markdown with each result.
- **Scrape URL** converts a known public webpage into Markdown and metadata.
- **Crawl Website** follows links from a starting URL and returns multiple pages as Markdown.
- **Find Website Pages** discovers sitemap URLs and can rank them against a topic.
- **Extract Structured Data** fills a JSON Schema from one or more public webpages.
- **Get Brand Profile** retrieves logos, colors, fonts, descriptions, and social profiles for a domain.

## Usage examples

- Search for a company's latest official product launches, then summarize the returned sources.
- Scrape a pricing page and extract the current plans into a JSON Schema.
- Find the documentation pages most relevant to authentication without crawling an entire site.
- Retrieve the brand profile for `linear.app`.

## Network access and credits

Search, scraping, crawling, extraction, and page discovery send user-provided queries, domains, URLs, schemas, and options to Context.dev. Crawl and extraction operations may access multiple public URLs. These operations consume Context.dev credits; limits in the plugin keep a single request bounded, but users should review the selected page count before running a workflow.

Every HTTP request has a fixed timeout. The plugin never executes user-provided code, shell commands, or SQL, and it does not expose a configurable proxy or API base URL.

## Documentation

- [Context.dev API documentation](https://docs.context.dev)
- [Source repository](https://github.com/aadithyanr/dify-context)
- [Terms of service](https://www.context.dev/term)
- [Privacy policy](https://www.context.dev/privacy)
