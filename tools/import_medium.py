#!/usr/bin/env python3
"""One-time import of a Medium export into Eleventy Markdown posts.

Usage: python tools/import_medium.py <extracted-export-dir> <repo-dir>
"""
import json
import re
import unicodedata
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class Post:
    title: str
    subtitle: str
    date: str
    canonical: str
    body_html: str


def is_article(html: str) -> bool:
    """Real articles carry a title element in the body; comment replies do not."""
    return "graf--title" in html


def parse_post(html: str) -> Post:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one("h1.p-name").get_text(strip=True)
    sub = soup.select_one('section[data-field="subtitle"]')
    subtitle = sub.get_text(" ", strip=True) if sub else ""
    date = soup.select_one("time.dt-published")["datetime"][:10]
    canonical = soup.select_one("a.p-canonical")["href"]
    body = soup.select_one('section[data-field="body"]')
    return Post(title, subtitle, date, canonical, body.decode_contents())


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60].strip("-")


def post_id(filename: str) -> str:
    m = re.search(r"-([0-9a-f]{10,12})\.html$", filename)
    return m.group(1) if m else ""


def make_slug(title: str, filename: str, taken: set) -> str:
    slug = slugify(title) or post_id(filename) or "post"
    if slug in taken:
        slug = f"{slug}-{post_id(filename) or len(taken)}"
    taken.add(slug)
    return slug


def front_matter(post: Post) -> str:
    # JSON strings are valid YAML double-quoted scalars.
    lines = ["---", f"title: {json.dumps(post.title, ensure_ascii=False)}"]
    if post.subtitle:
        lines.append(f"subtitle: {json.dumps(post.subtitle, ensure_ascii=False)}")
    lines += [
        f"date: {post.date}",
        f"medium_url: {json.dumps(post.canonical)}",
        "---",
        "",
    ]
    return "\n".join(lines)
