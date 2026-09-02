"""
Apify Actor Entrypoint: DeepCrawl AI Universal Website to Markdown Crawler Pro
Processes target URLs/domains and pushes clean Markdown datasets to Apify storage.
"""

import asyncio
from core.crawler_engine import crawl_domain_to_markdown
from core.markdown_extractor import clean_html_to_markdown, HEADERS
import requests

try:
    from apify import Actor
except ImportError:
    class Actor:
        @staticmethod
        async def init(): pass
        @staticmethod
        async def exit(): pass
        @staticmethod
        async def get_input():
            return {
                "start_urls": ["https://fastapi.tiangolo.com/tutorial/"],
                "max_pages_per_domain": 5,
                "max_depth": 2
            }
        @staticmethod
        async def push_data(data):
            print(f"[Apify Push] Pushed {len(data) if isinstance(data, list) else 1} items.")

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get("start_urls", [])
        max_pages = min(int(actor_input.get("max_pages_per_domain", 5)), 50)
        max_depth = min(int(actor_input.get("max_depth", 2)), 3)

        if isinstance(start_urls, str):
            start_urls = [u.strip() for u in start_urls.splitlines() if u.strip()]

        print(f"🚀 DeepCrawl started for {len(start_urls)} target roots (max {max_pages} pages each)...")

        total_pages = 0
        for start_url in start_urls:
            if not start_url:
                continue
            crawl_res = crawl_domain_to_markdown(start_url, max_pages=max_pages, max_depth=max_depth)
            for page in crawl_res.get("pages", []):
                total_pages += 1
                await Actor.push_data({
                    "url": page["url"],
                    "page_title": page["title"],
                    "word_count": page["word_count"],
                    "token_count": page["token_count"],
                    "markdown": page["markdown"]
                })

        print(f"✅ DeepCrawl completed! Pushed {total_pages} clean Markdown pages to dataset.")

if __name__ == "__main__":
    asyncio.run(main())
