from __future__ import annotations

from pathlib import Path

import yaml

from tools._requests import (
    build_brand_request,
    build_crawl_request,
    build_extract_request,
    build_scrape_params,
    build_search_request,
    build_sitemap_params,
)

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_references_six_production_tools() -> None:
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text())
    provider_path = ROOT / manifest["plugins"]["tools"][0]
    provider = yaml.safe_load(provider_path.read_text())

    assert manifest["author"] == "aadithyanr"
    assert manifest["privacy"] == "PRIVACY.md"
    assert provider["identity"]["author"] == "aadithyanr"
    assert provider["identity"]["icon"] == "icon.png"
    assert provider["tools"] == [
        "tools/search_web.yaml",
        "tools/scrape_url.yaml",
        "tools/crawl_website.yaml",
        "tools/find_website_pages.yaml",
        "tools/extract_structured_data.yaml",
        "tools/get_brand_profile.yaml",
    ]

    for tool_path in provider["tools"]:
        tool = yaml.safe_load((ROOT / tool_path).read_text())
        source = ROOT / tool["extra"]["python"]["source"]
        assert tool["identity"]["author"] == "aadithyanr"
        assert source.is_file()


def test_plugin_does_not_expose_unreleased_answers_api() -> None:
    production_files = [
        ROOT / "manifest.yaml",
        ROOT / "README.md",
        ROOT / "PRIVACY.md",
        ROOT / "main.py",
        *(ROOT / "provider").glob("*"),
        *(ROOT / "tools").glob("*"),
    ]
    production_files = [
        path for path in production_files if path.is_file() and path.suffix != ".pyc"
    ]
    contents = "\n".join(
        path.read_text(errors="ignore").lower() for path in production_files
    )
    assert "/answers" not in contents
    assert "/web/answers" not in contents


def test_search_request_maps_public_api_fields() -> None:
    assert build_search_request(
        {
            "query": "latest Context.dev launch",
            "num_results": 10,
            "include_domains": "context.dev, docs.context.dev",
            "include_markdown": False,
        }
    ) == {
        "query": "latest Context.dev launch",
        "numResults": 10,
        "includeDomains": ["context.dev", "docs.context.dev"],
        "queryFanout": False,
        "markdownOptions": {
            "enabled": False,
            "useMainContentOnly": True,
            "includeLinks": True,
            "includeImages": False,
        },
        "timeoutMS": 60000,
    }


def test_scrape_and_crawl_requests_are_bounded() -> None:
    scrape = build_scrape_params({"url": "https://context.dev"})
    crawl = build_crawl_request({"url": "https://context.dev"})

    assert scrape["timeoutMS"] == 60000
    assert crawl["maxPages"] == 10
    assert crawl["maxDepth"] == 2
    assert crawl["stopAfterMs"] == 120000
    assert crawl["timeoutMS"] == 120000


def test_sitemap_extract_and_brand_request_contracts() -> None:
    assert build_sitemap_params({"domain": "context.dev", "search": "pricing"}) == {
        "domain": "context.dev",
        "search": "pricing",
        "maxLinks": 100,
        "timeoutMS": 60000,
    }
    assert build_extract_request(
        {
            "url": "https://context.dev/pricing",
            "schema": '{"type":"object"}',
        }
    ) == {
        "url": "https://context.dev/pricing",
        "schema": {"type": "object"},
        "maxPages": 1,
        "maxDepth": 0,
        "followSubdomains": False,
        "factCheck": False,
        "timeoutMS": 120000,
    }
    assert build_brand_request({"domain": "context.dev"}) == {
        "type": "by_domain",
        "domain": "context.dev",
        "maxSpeed": False,
        "timeoutMS": 60000,
    }
