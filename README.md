# 🤖 DeepCrawl AI — Universal Website to Markdown Crawler Pro (Model Context Protocol Server)

[![MCP Protocol](https://img.shields.io/badge/MCP-Model_Context_Protocol-blue.svg)](https://modelcontextprotocol.io/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Glama](https://img.shields.io/badge/Glama-MCP_Server-purple.svg)](https://glama.ai/mcp/servers)

A high-performance **Model Context Protocol (MCP) Server** and deep domain crawler that turns any website, documentation hub, or sitemap into clean, LLM-ready Markdown for **Claude Desktop, Cursor IDE, LangChain, RAG pipelines, and Autonomous AI Agents**.

<p align="center">
  <img src="https://raw.githubusercontent.com/meanusarcanus/deep-markdown-crawler-api/master/assets/logo.jpg" alt="DeepCrawl AI Logo" width="180" style="border-radius: 20px;" />
</p>

---

## ⚡ Overview

**DeepCrawl AI** is a lightweight, high-speed alternative to Firecrawl and Crawl4AI. It recursively crawls documentation portals (e.g. Stripe, FastAPI, Supabase) and blogs, strips all web noise (ads, cookie banners, tracking scripts, navigation menus), and formats the core content into token-budgeted GitHub-Flavored Markdown.

* 🛡️ **Zero Noise HTML Cleaner**: Strips header/footer boilerplates, cookie banners, popups, and sidebar ads.
* 🌲 **BFS Deep Domain Crawler**: Recursively discovers internal links with strict domain boundary locking.
* 🗺️ **Fast Sitemap & URL Mapper**: Maps all available URLs across an entire domain in seconds.
* 🔌 **Zero-Config MCP Integration**: Plug-and-play with Claude Desktop, Cursor, and Antigravity agents.

---

## 🛠️ MCP Tools & Capabilities

The server exposes the following Model Context Protocol (MCP) tools:

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| **`scrape_url_markdown`** | `url` *(string, required)* | Scrapes a single webpage, removes ads/cookie popups, and returns clean GitHub Flavored Markdown with token metrics. |
| **`crawl_domain_markdown`** | `start_url` *(string, required)*, `max_pages` *(int)*, `max_depth` *(int)* | Recursively crawls an entire documentation site or blog up to a depth limit, returning a unified Markdown bundle for RAG. |
| **`map_domain_urls`** | `start_url` *(string, required)*, `max_links` *(int)* | Fast discovery of all internal URLs and sitemap routes across a domain without downloading full page bodies. |

---

## 🔌 Quickstart: Connect to Claude Desktop & Cursor

### 1. Claude Desktop Configuration
Add this server to your `claude_desktop_config.json`:

* **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
* **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "deep-markdown-crawler": {
      "command": "python3",
      "args": [
        "/path/to/deep-markdown-crawler-api/mcp_server.py"
      ]
    }
  }
}
```

### 2. Cursor IDE Configuration (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "deep-markdown-crawler": {
      "command": "python3",
      "args": ["/path/to/deep-markdown-crawler-api/mcp_server.py"]
    }
  }
}
```

---

## 📦 Python SDK & CLI Usage

```bash
pip install deep-markdown-crawler
```

```python
from deep_markdown_crawler import scrape_url_to_markdown, crawl_domain_to_markdown

# 1. Scrape Single URL
doc = scrape_url_to_markdown("https://fastapi.tiangolo.com/tutorial/")
print(f"Title: {doc['title']} | Tokens: ~{doc['token_count']}")
print(doc['markdown'][:500])

# 2. Deep Crawl Entire Domain
crawl = crawl_domain_to_markdown(
    start_url="https://fastapi.tiangolo.com/tutorial/",
    max_pages=5,
    max_depth=2
)
print(f"Crawled {crawl['total_pages_crawled']} pages ({crawl['total_tokens_estimated']} tokens).")
```

---

## 🌐 Serverless REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/scrape` | Single URL to clean GitHub-Flavored Markdown. |
| `POST` | `/api/v1/crawl` | Recursive domain crawler for multi-page documentation hubs. |
| `POST` | `/api/v1/map` | Fast domain URL & sitemap mapper. |
| `GET` | `/api/v1/health` | Service health status and supported features. |

---

## 📄 License
MIT License. Created by Meanus Arcanus.
