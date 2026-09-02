import requests
from typing import Dict, Any, Optional

def scrape_markdown(url: str, rapidapi_key: Optional[str] = None, base_url: Optional[str] = None) -> Dict[str, Any]:
    endpoint = f"{base_url or 'https://deep-markdown-crawler.p.rapidapi.com'}/api/v1/scrape"
    headers = {"Content-Type": "application/json"}
    if rapidapi_key:
        headers["x-rapidapi-key"] = rapidapi_key
        headers["x-rapidapi-host"] = "deep-markdown-crawler.p.rapidapi.com"
    try:
        res = requests.post(endpoint, json={"url": url}, headers=headers, timeout=25)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def crawl_site(url: str, max_depth: int = 1, max_pages: int = 5, rapidapi_key: Optional[str] = None, base_url: Optional[str] = None) -> Dict[str, Any]:
    endpoint = f"{base_url or 'https://deep-markdown-crawler.p.rapidapi.com'}/api/v1/crawl"
    headers = {"Content-Type": "application/json"}
    if rapidapi_key:
        headers["x-rapidapi-key"] = rapidapi_key
        headers["x-rapidapi-host"] = "deep-markdown-crawler.p.rapidapi.com"
    try:
        res = requests.post(endpoint, json={"url": url, "max_depth": max_depth, "max_pages": max_pages}, headers=headers, timeout=40)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

class DeepMarkdownCrawler:
    def __init__(self, rapidapi_key: Optional[str] = None, base_url: Optional[str] = None):
        self.rapidapi_key = rapidapi_key
        self.base_url = base_url or "https://deep-markdown-crawler.p.rapidapi.com"

    def scrape(self, url: str) -> Dict[str, Any]:
        return scrape_markdown(url, rapidapi_key=self.rapidapi_key, base_url=self.base_url)

    def crawl(self, url: str, max_depth: int = 1, max_pages: int = 5) -> Dict[str, Any]:
        return crawl_site(url, max_depth=max_depth, max_pages=max_pages, rapidapi_key=self.rapidapi_key, base_url=self.base_url)
