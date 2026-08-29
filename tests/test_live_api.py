from __future__ import annotations

import os

import pytest

from tools._client import ContextApiClient
from tools._requests import (
    build_brand_request,
    build_crawl_request,
    build_extract_request,
    build_scrape_params,
    build_search_request,
    build_sitemap_params,
)

API_KEY = os.getenv("CONTEXT_API_KEY")


@pytest.fixture(scope="module")
def client() -> ContextApiClient:
    if not API_KEY:
        pytest.skip("CONTEXT_API_KEY is not set")
    return ContextApiClient(API_KEY)


@pytest.mark.live
def test_production_credentials(client: ContextApiClient) -> None:
    assert client.get("/monitors/limits", timeout_seconds=15)


@pytest.mark.live
def test_production_read_tools(client: ContextApiClient) -> None:
    search = client.post(
        "/web/search",
        body=build_search_request(
            {
                "query": "site:context.dev Context.dev",
                "num_results": 10,
                "include_markdown": False,
            }
        ),
        timeout_seconds=70,
    )
    scrape = client.get(
        "/web/scrape/markdown",
        params=build_scrape_params({"url": "https://www.context.dev"}),
        timeout_seconds=70,
    )
    sitemap = client.get(
        "/web/scrape/sitemap",
        params=build_sitemap_params({"domain": "context.dev", "max_links": 3}),
        timeout_seconds=70,
    )
    brand = client.post(
        "/brand/retrieve",
        body=build_brand_request({"domain": "context.dev", "maximum_speed": True}),
        timeout_seconds=70,
    )

    assert search.get("results")
    assert scrape.get("markdown")
    assert sitemap.get("urls")
    assert brand


@pytest.mark.live
def test_production_multi_page_tools(client: ContextApiClient) -> None:
    crawl = client.post(
        "/web/crawl",
        body=build_crawl_request(
            {
                "url": "https://www.context.dev",
                "max_pages": 1,
                "max_depth": 0,
            }
        ),
        timeout_seconds=130,
    )
    extracted = client.post(
        "/web/extract",
        body=build_extract_request(
            {
                "url": "https://www.context.dev",
                "schema": '{"type":"object","properties":{"name":{"type":"string"}}}',
                "max_pages": 1,
                "max_depth": 0,
            }
        ),
        timeout_seconds=130,
    )

    assert crawl.get("results")
    assert extracted.get("data")
