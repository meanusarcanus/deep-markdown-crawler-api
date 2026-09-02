"""
Domain URL Mapper and Sitemap Discovery Engine
Discovers all crawlable internal endpoints across a domain in seconds.
"""

import re
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from typing import List, Set, Dict, Any
from bs4 import BeautifulSoup
from core.markdown_extractor import HEADERS

def is_same_domain(url: str, base_domain: str) -> bool:
    """Verifies that the target URL belongs to the same parent root domain."""
    try:
        netloc = urllib.parse.urlparse(url).netloc.lower().replace("www.", "")
        base = base_domain.lower().replace("www.", "")
        # Get apex domain (last two parts, e.g. python.org)
        base_apex = ".".join(base.split(".")[-2:])
        netloc_apex = ".".join(netloc.split(".")[-2:])
        return base_apex == netloc_apex
    except Exception:
        return False


def discover_sitemap_urls(base_url: str) -> List[str]:
    """Attempts to fetch and parse /sitemap.xml or /sitemap_index.xml."""
    parsed = urllib.parse.urlparse(base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    sitemap_paths = ["/sitemap.xml", "/sitemap_index.xml", "/sitemaps/sitemap.xml"]
    
    found_urls = []
    for path in sitemap_paths:
        target = f"{origin}{path}"
        try:
            res = requests.get(target, headers=HEADERS, timeout=5)
            if res.status_code == 200 and ("xml" in res.headers.get("content-type", "") or "<urlset" in res.text):
                root = ET.fromstring(res.text)
                for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                    if loc.text and is_same_domain(loc.text, parsed.netloc):
                        found_urls.append(loc.text.strip())
                if found_urls:
                    break
        except Exception:
            continue
    return found_urls

def map_domain_endpoints(start_url: str, max_links: int = 50) -> Dict[str, Any]:
    """
    Scans the start URL and sitemaps to return a list of internal crawlable endpoints.
    """
    parsed = urllib.parse.urlparse(start_url)
    base_domain = parsed.netloc
    origin = f"{parsed.scheme}://{base_domain}"

    discovered_urls: Set[str] = set()
    discovered_urls.add(start_url)

    # 1. Check sitemaps
    sitemap_urls = discover_sitemap_urls(start_url)
    for u in sitemap_urls:
        if len(discovered_urls) >= max_links:
            break
        discovered_urls.add(u)

    # 2. Extract links from homepage / start URL
    try:
        res = requests.get(start_url, headers=HEADERS, timeout=6)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if not href or href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:"):
                    continue
                full_url = urllib.parse.urljoin(start_url, href)
                # Strip query params and fragment for clean sitemap
                clean_url = urllib.parse.urljoin(full_url, urllib.parse.urlparse(full_url).path)
                if is_same_domain(clean_url, base_domain):
                    discovered_urls.add(clean_url)
                if len(discovered_urls) >= max_links:
                    break
    except Exception:
        pass

    url_list = sorted(list(discovered_urls))
    return {
        "status": "success",
        "domain": base_domain,
        "total_urls_found": len(url_list),
        "urls": url_list
    }
