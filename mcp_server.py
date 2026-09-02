#!/usr/bin/env python3
"""
DeepCrawl AI — Model Context Protocol (MCP) Server
Exposes clean web scraping, domain crawling, and sitemap mapping directly to Claude Desktop, Cursor IDE, and AI Agents.
"""

import sys
import json
import requests
from typing import Dict, Any, List
from core.markdown_extractor import clean_html_to_markdown, HEADERS
from core.crawler_engine import crawl_domain_to_markdown
from core.domain_mapper import map_domain_endpoints

TOOLS_DEFINITION = [
    {
        "name": "scrape_url_markdown",
        "description": "Scrapes a single webpage, strips all ads/navbars/cookie popups, and converts the core content into dense, LLM-ready GitHub Flavored Markdown.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The target webpage URL to scrape and convert to Markdown."
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "crawl_domain_markdown",
        "description": "Recursively crawls an entire documentation portal, blog, or domain to extract clean Markdown for RAG context windows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_url": {
                    "type": "string",
                    "description": "The starting root URL or documentation page to crawl (e.g. https://docs.python.org/3/)."
                },
                "max_pages": {
                    "type": "integer",
                    "description": "Maximum number of pages to crawl (default: 5, max: 25).",
                    "default": 5
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum crawling depth from start URL (default: 2).",
                    "default": 2
                }
            },
            "required": ["start_url"]
        }
    },
    {
        "name": "map_domain_urls",
        "description": "Fast discovery of all internal URLs and sitemap routes across a domain without downloading full page bodies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_url": {
                    "type": "string",
                    "description": "Root URL to map."
                },
                "max_links": {
                    "type": "integer",
                    "description": "Maximum number of URLs to discover (default: 50).",
                    "default": 50
                }
            },
            "required": ["start_url"]
        }
    }
]

def handle_call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "scrape_url_markdown":
        url = arguments.get("url", "")
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                data = clean_html_to_markdown(res.text, base_url=url)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"# {data['title']}\n**URL**: {url}\n**Tokens**: ~{data['token_count']}\n\n{data['markdown']}"
                        }
                    ]
                }
            else:
                return {"content": [{"type": "text", "text": f"Error: HTTP {res.status_code} when fetching {url}"}]}
        except Exception as e:
            return {"content": [{"type": "text", "text": f"Error fetching {url}: {str(e)}"}]}

    elif tool_name == "crawl_domain_markdown":
        start_url = arguments.get("start_url", "")
        max_pages = min(int(arguments.get("max_pages", 5)), 25)
        max_depth = min(int(arguments.get("max_depth", 2)), 3)
        res = crawl_domain_to_markdown(start_url, max_pages=max_pages, max_depth=max_depth)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"✓ Crawled {res['total_pages_crawled']} pages from {res['domain']} (~{res['total_tokens_estimated']} tokens):\n\n{res['combined_markdown']}"
                }
            ]
        }

    elif tool_name == "map_domain_urls":
        start_url = arguments.get("start_url", "")
        max_links = min(int(arguments.get("max_links", 50)), 100)
        res = map_domain_endpoints(start_url, max_links=max_links)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(res, indent=2)
                }
            ]
        }

    return {"content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}]}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "deep-markdown-crawler",
                            "version": "1.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": TOOLS_DEFINITION
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                tool_res = handle_call_tool(name, args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": tool_res
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"MCP Server Error: {str(e)}\n")

if __name__ == "__main__":
    main()
