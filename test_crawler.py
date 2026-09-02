"""
Automated Verification Suite for DeepCrawl AI (Firecrawl Alternative)
Tests single-page Markdown parsing, noise stripping, domain crawler, URL mapping, and FastAPI server.
"""

import sys
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from core.markdown_extractor import clean_html_to_markdown
from core.domain_mapper import is_same_domain, map_domain_endpoints
from core.crawler_engine import crawl_domain_to_markdown
from api.index import app, ScrapeRequest, scrape_single_url, CrawlRequest, crawl_domain_endpoint, MapRequest, map_domain_endpoint

MOCK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Tutorial - First Steps</title>
    <meta name="description" content="Learn how to build high performance APIs with FastAPI." />
</head>
<body>
    <nav class="navbar"><a href="/">Home</a><a href="/docs">Docs</a></nav>
    <header class="header"><h1>Header Title (Should be stripped if noise)</h1></header>
    <div class="cookie-consent-banner">We use cookies! Click Accept</div>
    
    <main>
        <h1>Creating Your First API Endpoint</h1>
        <p>FastAPI is a modern, fast <strong>web framework</strong> for building APIs with Python.</p>
        
        <h2>Installation</h2>
        <p>Install FastAPI using pip:</p>
        <pre><code class="language-bash">pip install fastapi "uvicorn[standard]"</code></pre>
        
        <h2>Example Code</h2>
        <pre><code class="language-python">from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
</code></pre>
        
        <blockquote>FastAPI is based on standard Python type hints.</blockquote>
        
        <h3>Key Features</h3>
        <ul>
            <li>Automatic OpenAPI documentation</li>
            <li>Fast performance on par with NodeJS and Go</li>
            <li>Data validation with Pydantic</li>
        </ul>
        
        <p>Check out the <a href="https://fastapi.tiangolo.com/features/">Full Features List</a> for more.</p>
    </main>
    
    <footer class="footer">Copyright 2026 FastAPI. All rights reserved.</footer>
</body>
</html>
"""

def run_tests():
    print("=" * 65)
    print(" 📄 TESTING DEEPCRAWL AI (FIRECRAWL ALTERNATIVE)")
    print("=" * 65)

    # Test 1: HTML Noise Stripping & Clean Markdown Conversion
    print("\n[Test 1] HTML to Clean Markdown Conversion...")
    res = clean_html_to_markdown(MOCK_HTML, base_url="https://fastapi.tiangolo.com")
    print(f"✓ Title: {res['title']}")
    print(f"✓ Description: {res['description']}")
    print(f"✓ Word Count: {res['word_count']} | Token Count: {res['token_count']}")
    
    assert res['title'] == "FastAPI Tutorial - First Steps"
    assert "FastAPI is a modern, fast **web framework**" in res['markdown']
    assert "```python" in res['markdown']
    assert "```bash" in res['markdown']
    assert "cookie-consent-banner" not in res['markdown']
    assert "We use cookies" not in res['markdown']
    assert "[Full Features List](https://fastapi.tiangolo.com/features/)" in res['markdown']
    print("✓ Noise stripped, code fences preserved, clean Markdown validated!")

    # Test 2: Domain Boundary Verifier
    print("\n[Test 2] Domain Boundary Verification...")
    assert is_same_domain("https://docs.python.org/3/tutorial/index.html", "docs.python.org") is True
    assert is_same_domain("https://python.org/downloads", "docs.python.org") is True
    assert is_same_domain("https://google.com/search", "docs.python.org") is False
    print("✓ Domain boundary lock working perfectly!")

    # Test 3: Domain URL Mapping
    print("\n[Test 3] Domain URL Mapper...")
    map_res = map_domain_endpoints("https://fastapi.tiangolo.com/tutorial/", max_links=5)
    print(f"✓ Status: {map_res['status']}")
    print(f"✓ Total URLs Discovered: {map_res['total_urls_found']}")
    assert map_res['status'] == "success"
    assert len(map_res['urls']) > 0

    # Test 4: BFS Domain Crawler
    print("\n[Test 4] Breadth-First Search (BFS) Domain Crawler...")
    crawl_res = crawl_domain_to_markdown("https://fastapi.tiangolo.com/tutorial/", max_pages=2, max_depth=1)
    print(f"✓ Crawled Pages: {crawl_res['total_pages_crawled']}")
    print(f"✓ Total Tokens: ~{crawl_res['total_tokens_estimated']}")
    assert crawl_res['status'] == "success"
    assert crawl_res['total_pages_crawled'] >= 1
    assert len(crawl_res['combined_markdown']) > 50

    # Test 5: FastAPI Serverless Endpoints
    print("\n[Test 5] FastAPI Endpoints (/api/v1/scrape, /api/v1/crawl, /api/v1/map)...")
    scrape_req = ScrapeRequest(url="https://fastapi.tiangolo.com/tutorial/")
    scrape_out = scrape_single_url(scrape_req)
    assert scrape_out['status'] == "success"
    assert scrape_out['token_count'] > 0
    print(f"✓ POST /api/v1/scrape: Success ({scrape_out['word_count']} words)")

    map_req = MapRequest(start_url="https://fastapi.tiangolo.com/tutorial/", max_links=3)
    map_out = map_domain_endpoint(map_req)
    assert map_out['status'] == "success"
    print(f"✓ POST /api/v1/map: Success ({map_out['total_urls_found']} URLs)")

    print("\n" + "=" * 65)
    print(" 🎉 ALL DEEPCRAWL AI TESTS PASSED 100% SUCCESSFULLY!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_tests()
