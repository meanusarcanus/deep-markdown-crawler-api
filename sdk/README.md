# 📄 DeepCrawl AI — Universal Website to Markdown Crawler SDK

Official Python SDK for **DeepCrawl AI** (Open-Source Firecrawl Alternative).

---

## ⚡ Quickstart

```bash
pip install deep-markdown-crawler
```

```python
from deep_markdown_crawler import scrape_url_to_markdown, crawl_domain_to_markdown

# 1. Scrape Single URL to Clean Markdown
doc = scrape_url_to_markdown("https://fastapi.tiangolo.com/tutorial/")
print(f"Title: {doc['title']} | Tokens: ~{doc['token_count']}")
print(doc['markdown'][:500])

# 2. Deep Crawl Entire Documentation Domain
crawl = crawl_domain_to_markdown(
    start_url="https://fastapi.tiangolo.com/tutorial/",
    max_pages=5,
    max_depth=2
)

print(f"Crawled {crawl['total_pages_crawled']} pages ({crawl['total_tokens_estimated']} tokens).")
```
