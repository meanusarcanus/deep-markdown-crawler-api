# 📄 DeepCrawl AI — Universal Website to Markdown Crawler API — Documentation

Welcome to the **DeepCrawl AI API** (Open-Source Firecrawl Alternative). Engineered for LLMs, RAG pipelines, fine-tuning datasets, and autonomous AI agents to crawl entire documentation portals, sitemaps, and domains into clean, structured Markdown.

---

## ⚡ 1. Authentication & Headers

All requests to the RapidAPI endpoint require the standard RapidAPI authentication headers:

```http
x-rapidapi-key: YOUR_RAPIDAPI_KEY
x-rapidapi-host: deep-markdown-crawler.p.rapidapi.com
Content-Type: application/json
```

---

## 📄 2. Endpoint 1: Single URL to Markdown (`POST /api/v1/scrape`)

Scrapes any single webpage, strips all ads, navigation menus, cookie popups, and boilerplate, and returns clean GitHub Flavored Markdown with token metrics.

### Request Body:
```json
{
  "url": "https://fastapi.tiangolo.com/tutorial/"
}
```

### Response Output:
```json
{
  "status": "success",
  "url": "https://fastapi.tiangolo.com/tutorial/",
  "title": "Tutorial - User Guide - FastAPI",
  "description": "FastAPI tutorial and user guide.",
  "markdown": "# Tutorial - User Guide\n\nThis tutorial shows you how to use **FastAPI** with most of its features...",
  "word_count": 857,
  "token_count": 1140
}
```

---

## 🌲 3. Endpoint 2: Deep BFS Domain Crawler (`POST /api/v1/crawl`)

Recursively crawls a documentation hub or domain up to a configurable page and depth limit. Returns individual page markdown objects and a concatenated bundle.

### Request Body:
```json
{
  "start_url": "https://fastapi.tiangolo.com/tutorial/",
  "max_pages": 5,
  "max_depth": 2
}
```

---

## 🗺️ 4. Endpoint 3: Fast Domain URL Mapper (`POST /api/v1/map`)

Discovers all internal URLs and sitemap routes across an entire domain in seconds.

### Request Body:
```json
{
  "start_url": "https://fastapi.tiangolo.com/",
  "max_links": 50
}
```

---

## 💻 5. Python Integration Example

```python
import requests

url = "https://deep-markdown-crawler.p.rapidapi.com/api/v1/crawl"

payload = {
    "start_url": "https://fastapi.tiangolo.com/tutorial/",
    "max_pages": 5,
    "max_depth": 2
}

headers = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
    "x-rapidapi-host": "deep-markdown-crawler.p.rapidapi.com",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

print(f"Crawled {data['total_pages_crawled']} pages ({data['total_tokens_estimated']} tokens).")
print(data['combined_markdown'][:500])
```
