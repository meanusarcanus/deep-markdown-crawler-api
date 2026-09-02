"""
Deep Domain to Markdown Crawler Engine (BFS)
Crawls documentation portals, blogs, and websites to produce concatenated or structured Markdown.
"""

import collections
import urllib.parse
import requests
from typing import List, Dict, Any, Set
from bs4 import BeautifulSoup
from core.markdown_extractor import clean_html_to_markdown, HEADERS
from core.domain_mapper import is_same_domain

def crawl_domain_to_markdown(
    start_url: str,
    max_pages: int = 10,
    max_depth: int = 2,
    extract_main_only: bool = True
) -> Dict[str, Any]:
    """
    Recursively crawls internal pages starting from `start_url` up to `max_pages` and `max_depth`.
    Returns list of page Markdown objects and a combined concatenated Markdown bundle.
    """
    parsed = urllib.parse.urlparse(start_url)
    base_domain = parsed.netloc

    queue = collections.deque([(start_url, 0)]) # (url, current_depth)
    visited: Set[str] = set()
    crawled_pages: List[Dict[str, Any]] = []
    total_tokens = 0

    while queue and len(crawled_pages) < max_pages:
        current_url, depth = queue.popleft()
        
        # Clean URL (strip fragment)
        clean_url = urllib.parse.urldefrag(current_url)[0].rstrip("/")
        if clean_url in visited:
            continue
        visited.add(clean_url)

        try:
            res = requests.get(clean_url, headers=HEADERS, timeout=7)
            if res.status_code != 200 or "text/html" not in res.headers.get("content-type", ""):
                continue

            # Extract clean markdown
            parsed_data = clean_html_to_markdown(res.text, base_url=clean_url)
            page_obj = {
                "url": clean_url,
                "depth": depth,
                "title": parsed_data["title"] or clean_url,
                "description": parsed_data["description"],
                "markdown": parsed_data["markdown"],
                "word_count": parsed_data["word_count"],
                "token_count": parsed_data["token_count"]
            }
            crawled_pages.append(page_obj)
            total_tokens += parsed_data["token_count"]

            # If depth allows, discover child links
            if depth < max_depth:
                soup = BeautifulSoup(res.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"].strip()
                    if not href or href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:"):
                        continue
                    full_child = urllib.parse.urljoin(clean_url, href)
                    clean_child = urllib.parse.urldefrag(full_child)[0].rstrip("/")
                    if clean_child not in visited and is_same_domain(clean_child, base_domain):
                        queue.append((clean_child, depth + 1))
        except Exception:
            continue

    # Generate combined bundle
    bundle_parts = []
    for page in crawled_pages:
        bundle_parts.append(f"# {page['title']}\n**Source**: {page['url']}\n\n{page['markdown']}\n\n---\n")
    combined_markdown = "\n".join(bundle_parts)

    return {
        "status": "success",
        "start_url": start_url,
        "domain": base_domain,
        "total_pages_crawled": len(crawled_pages),
        "total_tokens_estimated": total_tokens,
        "pages": crawled_pages,
        "combined_markdown": combined_markdown
    }
