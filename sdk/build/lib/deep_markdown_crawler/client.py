import requests
from typing import Dict, Any, Optional

def scrape_url_to_markdown(url: str, base_url: str = "https://deep-markdown-crawler-api.vercel.app") -> Dict[str, Any]:
    """Scrape a single URL into clean Markdown."""
    endpoint = f"{base_url.rstrip('/')}/api/v1/scrape"
    try:
        res = requests.post(endpoint, json={"url": url}, timeout=25)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def crawl_domain_to_markdown(start_url: str, max_pages: int = 5, max_depth: int = 2, base_url: str = "https://deep-markdown-crawler-api.vercel.app") -> Dict[str, Any]:
    """Crawl a full domain or doc portal into clean Markdown."""
    endpoint = f"{base_url.rstrip('/')}/api/v1/crawl"
    try:
        res = requests.post(endpoint, json={"start_url": start_url, "max_pages": max_pages, "max_depth": max_depth}, timeout=45)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

class DeepMarkdownCrawler:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://deep-markdown-crawler-api.vercel.app"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def scrape(self, url: str) -> Dict[str, Any]:
        return scrape_url_to_markdown(url, base_url=self.base_url)

    def crawl(self, start_url: str, max_pages: int = 5, max_depth: int = 2) -> Dict[str, Any]:
        return crawl_domain_to_markdown(start_url, max_pages=max_pages, max_depth=max_depth, base_url=self.base_url)
