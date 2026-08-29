from __future__ import annotations

import json
from typing import Any

from ._client import compact_dict, csv_values


def build_search_request(tool_parameters: dict[str, Any]) -> dict[str, Any]:
    return compact_dict(
        {
            "query": tool_parameters["query"],
            "numResults": tool_parameters.get("num_results", 10),
            "includeDomains": csv_values(tool_parameters.get("include_domains")),
            "excludeDomains": csv_values(tool_parameters.get("exclude_domains")),
            "freshness": tool_parameters.get("freshness"),
            "country": tool_parameters.get("country"),
            "queryFanout": tool_parameters.get("query_fanout", False),
            "markdownOptions": {
                "enabled": bool(tool_parameters.get("include_markdown", True)),
                "useMainContentOnly": True,
                "includeLinks": True,
                "includeImages": False,
            },
            "timeoutMS": 60000,
        }
    )


def build_scrape_params(tool_parameters: dict[str, Any]) -> dict[str, Any]:
    return compact_dict(
        {
            "url": tool_parameters["url"],
            "useMainContentOnly": tool_parameters.get("use_main_content_only", True),
            "includeLinks": tool_parameters.get("include_links", True),
            "includeImages": tool_parameters.get("include_images", False),
            "includeHTML": tool_parameters.get("include_html", False),
            "includeSelectors": tool_parameters.get("include_selectors"),
            "excludeSelectors": tool_parameters.get("exclude_selectors"),
            "waitForMs": tool_parameters.get("wait_for_ms"),
            "timeoutMS": 60000,
        }
    )


def build_crawl_request(tool_parameters: dict[str, Any]) -> dict[str, Any]:
    return compact_dict(
        {
            "url": tool_parameters["url"],
            "maxPages": tool_parameters.get("max_pages", 10),
            "maxDepth": tool_parameters.get("max_depth", 2),
            "urlRegex": tool_parameters.get("url_regex"),
            "followSubdomains": tool_parameters.get("follow_subdomains", False),
            "useMainContentOnly": tool_parameters.get("use_main_content_only", True),
            "includeLinks": True,
            "includeImages": False,
            "stopAfterMs": 120000,
            "timeoutMS": 120000,
        }
    )


def build_sitemap_params(tool_parameters: dict[str, Any]) -> dict[str, Any]:
    return compact_dict(
        {
            "domain": tool_parameters["domain"],
            "search": tool_parameters.get("search"),
            "maxLinks": tool_parameters.get("max_links", 100),
            "sitemapUrl": tool_parameters.get("sitemap_url"),
            "urlRegex": tool_parameters.get("url_regex"),
            "timeoutMS": 60000,
        }
    )


def build_extract_request(tool_parameters: dict[str, Any]) -> dict[str, Any]:
    return compact_dict(
        {
            "url": tool_parameters["url"],
            "schema": parse_json_object(tool_parameters["schema"], "Schema"),
            "instructions": tool_parameters.get("instructions"),
            "maxPages": tool_parameters.get("max_pages", 1),
            "maxDepth": tool_parameters.get("max_depth", 0),
            "followSubdomains": tool_parameters.get("follow_subdomains", False),
            "factCheck": tool_parameters.get("fact_check", False),
            "timeoutMS": 120000,
        }
    )


def build_brand_request(tool_parameters: dict[str, Any]) -> dict[str, Any]:
    return compact_dict(
        {
            "type": "by_domain",
            "domain": tool_parameters["domain"],
            "maxSpeed": tool_parameters.get("maximum_speed", False),
            "maxAgeMs": tool_parameters.get("max_age_ms"),
            "timeoutMS": 60000,
        }
    )


def parse_json_object(value: Any, field_name: str) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(str(value))
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must be valid JSON.") from error
    if not isinstance(parsed, dict):
        raise TypeError(f"{field_name} must be a JSON object.")
    return parsed
