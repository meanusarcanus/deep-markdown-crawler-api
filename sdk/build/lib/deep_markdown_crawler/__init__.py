"""
DeepCrawl AI — Universal Website to Markdown Crawler SDK
Official Python client for deep website and documentation crawling into clean Markdown.
"""

from .client import DeepMarkdownCrawler, scrape_url_to_markdown, crawl_domain_to_markdown

__version__ = "1.0.0"
__all__ = ["DeepMarkdownCrawler", "scrape_url_to_markdown", "crawl_domain_to_markdown"]
