import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add root directory to sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.markdown_extractor import clean_html_to_markdown, HEADERS
from core.crawler_engine import crawl_domain_to_markdown
from core.domain_mapper import map_domain_endpoints

app = FastAPI(
    title="DeepCrawl AI — Universal Website to Markdown Crawler Pro API",
    description="Crawl entire documentation portals, sitemaps, and domains into clean, LLM-ready Markdown without ads or noise for RAG and AI Agents.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# Pydantic Schemas
# ==============================================================================
class ScrapeRequest(BaseModel):
    url: str = Field(..., example="https://fastapi.tiangolo.com/tutorial/", description="Target webpage URL to scrape and convert into Markdown.")

class CrawlRequest(BaseModel):
    start_url: str = Field(..., example="https://fastapi.tiangolo.com/tutorial/", description="Root URL or documentation hub to crawl recursively.")
    max_pages: Optional[int] = Field(default=5, description="Maximum number of pages to crawl (1 to 25).")
    max_depth: Optional[int] = Field(default=2, description="Maximum depth of links to follow (1 to 3).")

class MapRequest(BaseModel):
    start_url: str = Field(..., example="https://fastapi.tiangolo.com/", description="Root domain URL to map.")
    max_links: Optional[int] = Field(default=50, description="Maximum number of URLs to discover.")

# ==============================================================================
# API Endpoints
# ==============================================================================
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DeepCrawl AI — Universal Website to Markdown Crawler Pro API",
        "version": "1.0.0",
        "supported_features": ["Single Page to Markdown", "Deep BFS Domain Crawler", "Sitemap URL Mapper", "MCP Server"]
    }

@app.post("/api/v1/scrape")
def scrape_single_url(payload: ScrapeRequest):
    """
    Scrape single webpage and convert into clean GitHub-Flavored Markdown.
    """
    if not payload.url.strip():
        raise HTTPException(status_code=400, detail="url cannot be empty.")
    try:
        res = requests.get(payload.url.strip(), headers=HEADERS, timeout=12)
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=f"Failed to fetch URL: HTTP {res.status_code}")
        data = clean_html_to_markdown(res.text, base_url=payload.url.strip())
        return {
            "status": "success",
            "url": payload.url.strip(),
            "title": data["title"],
            "description": data["description"],
            "markdown": data["markdown"],
            "word_count": data["word_count"],
            "token_count": data["token_count"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/scrape")
def scrape_single_url_get(
    url: str = Query(..., examples=["https://fastapi.tiangolo.com/tutorial/"], description="Target URL")
):
    """
    Quick GET endpoint for single-page Markdown conversion.
    """
    return scrape_single_url(ScrapeRequest(url=url))

@app.post("/api/v1/crawl")
def crawl_domain_endpoint(payload: CrawlRequest):
    """
    Deep recursive domain crawler for entire documentation sites.
    """
    if not payload.start_url.strip():
        raise HTTPException(status_code=400, detail="start_url cannot be empty.")
    max_pages = min(max(1, payload.max_pages or 5), 25)
    max_depth = min(max(1, payload.max_depth or 2), 3)
    return crawl_domain_to_markdown(payload.start_url.strip(), max_pages=max_pages, max_depth=max_depth)

@app.post("/api/v1/map")
def map_domain_endpoint(payload: MapRequest):
    """
    Fast discovery of internal URLs across a domain without fetching full pages.
    """
    if not payload.start_url.strip():
        raise HTTPException(status_code=400, detail="start_url cannot be empty.")
    max_links = min(max(1, payload.max_links or 50), 100)
    return map_domain_endpoints(payload.start_url.strip(), max_links=max_links)
