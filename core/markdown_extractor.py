"""
Universal HTML to Clean Markdown Extractor
Strips ads, navbars, cookie popups, and scripts to produce dense, LLM-ready Markdown.
"""

import re
import urllib.parse
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup, Comment

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

def clean_html_to_markdown(html_content: str, base_url: str = "") -> Dict[str, Any]:
    """
    Parses raw HTML and converts the core content into structured GitHub-Flavored Markdown.
    """
    if not html_content or not isinstance(html_content, str):
        return {"title": "", "description": "", "markdown": "", "word_count": 0, "token_count": 0}

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Extract metadata
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    elif soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)

    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()

    # 2. Remove comments
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # 3. Strip boilerplate tags
    strip_tags = [
        "nav", "header", "footer", "script", "style", "noscript",
        "svg", "form", "iframe", "aside", "dialog", "canvas"
    ]
    for tag in soup.find_all(strip_tags):
        tag.decompose()

    # 4. Remove elements by class / ID heuristics (ads, cookie banners, tracking)
    noise_patterns = re.compile(
        r"(cookie|banner|consent|sidebar|popup|modal|advert|sponsor|promo|share-button|newsletter|tracking|toast)",
        re.IGNORECASE
    )
    for elem in soup.find_all(attrs={"class": noise_patterns}):
        elem.decompose()
    for elem in soup.find_all(attrs={"id": noise_patterns}):
        elem.decompose()

    # 5. Extract main container if present
    main_content = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile(r"(content|post|doc|article|body)", re.IGNORECASE)) or soup.body or soup

    # 6. Convert HTML tags to Markdown formatting
    # Headings
    for i in range(1, 7):
        for h in main_content.find_all(f"h{i}"):
            h_text = h.get_text(strip=True)
            if h_text:
                h.replace_with(f"\n\n{'#' * i} {h_text}\n\n")

    # Code blocks
    for pre in main_content.find_all("pre"):
        code_tag = pre.find("code")
        lang = ""
        if code_tag and code_tag.get("class"):
            for cls in code_tag.get("class"):
                if cls.startswith("language-") or cls.startswith("lang-"):
                    lang = cls.replace("language-", "").replace("lang-", "")
                    break
        code_text = code_tag.get_text() if code_tag else pre.get_text()
        pre.replace_with(f"\n\n```{lang}\n{code_text.strip()}\n```\n\n")

    # Inline code
    for code in main_content.find_all("code"):
        code.replace_with(f"`{code.get_text().strip()}`")

    # Bold and Italic
    for b in main_content.find_all(["strong", "b"]):
        b.replace_with(f"**{b.get_text().strip()}**")
    for em in main_content.find_all(["em", "i"]):
        em.replace_with(f"*{em.get_text().strip()}*")

    # Blockquotes
    for bq in main_content.find_all("blockquote"):
        bq_text = bq.get_text(strip=True)
        bq.replace_with(f"\n> {bq_text}\n")

    # Unordered Lists
    for ul in main_content.find_all("ul"):
        list_items = []
        for li in ul.find_all("li", recursive=False):
            t = li.get_text(strip=True)
            if t:
                list_items.append(f"* {t}")
        ul.replace_with("\n" + "\n".join(list_items) + "\n")

    # Ordered Lists
    for ol in main_content.find_all("ol"):
        list_items = []
        for idx, li in enumerate(ol.find_all("li", recursive=False), 1):
            t = li.get_text(strip=True)
            if t:
                list_items.append(f"{idx}. {t}")
        ol.replace_with("\n" + "\n".join(list_items) + "\n")

    # Links (Preserve clean markdown links)
    for a in main_content.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if text and href and not href.startswith("javascript:") and not href.startswith("#"):
            if base_url and not href.startswith("http"):
                href = urllib.parse.urljoin(base_url, href)
            a.replace_with(f"[{text}]({href})")

    # 7. Final text cleaning & whitespace collapse
    raw_md = main_content.get_text()
    clean_lines = []
    for line in raw_md.splitlines():
        l = line.strip()
        if l:
            clean_lines.append(l)
        elif clean_lines and clean_lines[-1] != "":
            clean_lines.append("")

    final_markdown = "\n".join(clean_lines).strip()
    words = len(final_markdown.split())
    tokens = int(round(words * 1.33)) # Standard token estimation

    return {
        "title": title,
        "description": description,
        "markdown": final_markdown,
        "word_count": words,
        "token_count": tokens
    }
