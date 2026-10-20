#!/usr/bin/env python3
"""One-time import of a Medium export into Eleventy Markdown posts.

Usage: python tools/import_medium.py <extracted-export-dir> <repo-dir>
"""
import json
import re
import sys
import unicodedata
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify


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


# Alphanumeric so Markdown escaping cannot alter it; END stops CODEBLOCK1 matching CODEBLOCK10.
CODE_TOKEN = "CODEBLOCK{}END"
UNCONVERTED = ["iframe", "video", "audio", "embed", "object", "table"]


@dataclass
class Converted:
    markdown: str
    warnings: list = field(default_factory=list)
    embeds: int = 0


def to_markdown(body_html: str) -> Converted:
    soup = BeautifulSoup(body_html, "html.parser")
    out = Converted("")

    for el in soup.select("script, .graf--title, .graf--subtitle"):
        el.decompose()

    # Every Medium section starts with a divider; the first one is just the top of the post.
    dividers = soup.select("div.section-divider")
    for d in dividers[1:]:
        d.replace_with(soup.new_tag("hr"))
    if dividers:
        dividers[0].decompose()

    for fig in soup.find_all("figure"):
        img, cap = fig.find("img"), fig.find("figcaption")
        cap_text = cap.get_text(" ", strip=True) if cap else ""
        wrapper = soup.new_tag("div")
        if img is not None and img.get("src"):
            p = soup.new_tag("p")
            p.append(soup.new_tag("img", src=img["src"], alt=cap_text))
            wrapper.append(p)
        if cap_text:
            p, em = soup.new_tag("p"), soup.new_tag("em")
            for child in list(cap.contents):
                em.append(child.extract())
            p.append(em)
            wrapper.append(p)
        fig.replace_with(wrapper)

    for mix in soup.select(".graf--mixtapeEmbed"):
        a = mix.find("a", href=True)
        if a is None:
            out.warnings.append("mixtape embed without link")
            mix.decompose()
            continue
        strong = mix.find("strong")
        label = strong.get_text(" ", strip=True) if strong else a["href"]
        p, link = soup.new_tag("p"), soup.new_tag("a", href=a["href"])
        link.string = label
        p.append(link)
        mix.replace_with(p)
        out.embeds += 1

    blocks = []
    for pre in soup.find_all("pre"):
        for br in pre.find_all("br"):
            br.replace_with("\n")
        text = pre.get_text().strip("\n")
        lang = pre.get("data-code-block-lang") or ""
        if lang == "auto":
            lang = ""
        fence = "```" if "```" not in text else "~~~~"
        blocks.append(f"{fence}{lang}\n{text}\n{fence}")
        p = soup.new_tag("p")
        p.string = CODE_TOKEN.format(len(blocks) - 1)
        pre.replace_with(p)

    for h in soup.find_all(["h2", "h3", "h4"]):
        h.name = {"h2": "h2", "h3": "h2", "h4": "h3"}[h.name]
    for q in soup.select(".graf--pullquote"):
        q.name = "blockquote"

    for tag in soup.find_all(UNCONVERTED):
        out.warnings.append(f"unconverted <{tag.name}>")

    # A bare "<" in prose would otherwise be read as the start of an HTML tag by the site's Markdown.
    for t in soup.find_all(string=True):
        if "<" in t:
            t.replace_with(NavigableString(t.replace("<", "&lt;")))

    md = markdownify(str(soup), heading_style="ATX", bullets="-")
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    for i, block in enumerate(blocks):
        md = md.replace(CODE_TOKEN.format(i), block)
    out.markdown = md
    return out


def image_urls(markdown: str) -> list:
    return list(dict.fromkeys(re.findall(r"!\[[^\]]*\]\(([^)\s]+)", markdown)))


EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
       "image/webp": ".webp", "image/svg+xml": ".svg"}


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get_content_type()


def hires(url: str) -> str:
    return re.sub(r"/max/\d+/", "/max/1600/", url)


def save_image(url, dest_dir, fetch=_fetch):
    """Download url (trying a larger rendition first); return the saved filename or None."""
    for candidate in dict.fromkeys([hires(url), url]):
        try:
            data, ctype = fetch(candidate)
        except Exception:
            continue
        ext = EXT.get(ctype)
        if not ext:
            continue
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", candidate.rstrip("/").rsplit("/", 1)[-1]) + ext
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / name).write_bytes(data)
        return name
    return None


@dataclass
class Report:
    imported: int = 0
    replies: int = 0
    drafts: int = 0
    image_failures: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    embeds: list = field(default_factory=list)


def import_export(export_dir: Path, repo_dir: Path, fetch=_fetch) -> Report:
    report, taken = Report(), set()
    posts_dir = repo_dir / "src" / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted((export_dir / "posts").glob("*.html")):
        if path.name.startswith("draft_"):
            report.drafts += 1
            continue
        html = path.read_text(encoding="utf-8")
        if not is_article(html):
            report.replies += 1
            continue
        post = parse_post(html)
        slug = make_slug(post.title, path.name, taken)
        conv = to_markdown(post.body_html)
        md = conv.markdown
        for url in image_urls(md):
            name = save_image(url, repo_dir / "src" / "img" / slug, fetch)
            if name:
                md = md.replace(url, f"/img/{slug}/{name}")
            else:
                report.image_failures.append((slug, url))
        report.warnings += [(slug, w) for w in conv.warnings]
        if conv.embeds:
            report.embeds.append(slug)
        (posts_dir / f"{post.date}-{slug}.md").write_text(front_matter(post) + "\n" + md, encoding="utf-8")
        report.imported += 1
    return report


def main(argv):
    export_dir, repo_dir = Path(argv[1]), Path(argv[2])
    r = import_export(export_dir, repo_dir)
    print(f"imported={r.imported} replies_skipped={r.replies} drafts_skipped={r.drafts}")
    print(f"posts with link-card embeds converted to links: {len(r.embeds)}")
    for slug, url in r.image_failures:
        print(f"IMAGE FAILED  {slug}  {url}")
    for slug, w in r.warnings:
        print(f"WARNING       {slug}  {w}")


if __name__ == "__main__":
    main(sys.argv)
