#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["beautifulsoup4", "markdownify"]
# ///
"""Pull new posts from the Medium RSS feed into the Eleventy site.

Usage (from the repo root): uv run tools/medium_pull.py [--dry-run] [--feed-file FILE]

Writes src/posts/*.md and src/img/<slug>/*; review and commit the result yourself.
Medium's feed holds only the latest ~10 posts, and member-only posts come through as
teasers. Teasers are reported, not written.
"""
import argparse
import json
import re
import sys
import unicodedata
import urllib.request
from dataclasses import dataclass, field
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify

FEED_URL = "https://medium.com/feed/@mckornfield"
AUTHOR = "mckornfield"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}encoded"


@dataclass
class Post:
    title: str
    date: str
    canonical: str
    post_id: str
    body_html: str


def parse_feed(xml: str) -> list:
    posts = []
    for item in ElementTree.fromstring(xml).iter("item"):
        post_id = item.findtext("guid", "").rsplit("/", 1)[-1]
        slug = item.findtext("link", "").split("?")[0].rstrip("/").rsplit("/", 1)[-1]
        when = parsedate_to_datetime(item.findtext("pubDate")).astimezone(timezone.utc)
        posts.append(Post(
            title=item.findtext("title", "").strip(),
            date=when.date().isoformat(),
            canonical=f"https://medium.com/@{AUTHOR}/{slug}",
            post_id=post_id,
            body_html=item.findtext(CONTENT, "") or "",
        ))
    return posts


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60].strip("-")


def make_slug(title: str, post_id: str, taken: set) -> str:
    slug = slugify(title) or post_id or "post"
    if slug in taken:
        slug = f"{slug}-{post_id or len(taken)}"
    taken.add(slug)
    return slug


def front_matter(post: Post, subtitle: str) -> str:
    # JSON strings are valid YAML double-quoted scalars.
    lines = ["---", f"title: {json.dumps(post.title, ensure_ascii=False)}"]
    if subtitle:
        lines.append(f"subtitle: {json.dumps(subtitle, ensure_ascii=False)}")
    lines += [f"date: {post.date}", f"medium_url: {json.dumps(post.canonical)}", "---", ""]
    return "\n".join(lines)


# Alphanumeric so Markdown escaping cannot alter it; END stops CODEBLOCK1 matching CODEBLOCK10.
CODE_TOKEN = "CODEBLOCK{}END"
UNCONVERTED = ["iframe", "video", "audio", "embed", "object", "table"]


@dataclass
class Converted:
    markdown: str
    subtitle: str = ""
    warnings: list = field(default_factory=list)


def to_markdown(body_html: str, subtitle: bool = False) -> Converted:
    """Convert a Medium post body. With subtitle=True a leading <h4> is taken as the subtitle."""
    soup = BeautifulSoup(body_html, "html.parser")
    out = Converted("")

    for el in soup.select("script"):
        el.decompose()
    # The feed ends with a 1x1 view-tracking pixel.
    for img in soup.find_all("img", src=re.compile(r"medium\.com/_/stat")):
        img.decompose()

    first = next((c for c in soup.contents if getattr(c, "name", None)), None)
    if subtitle and first is not None and first.name == "h4":
        out.subtitle = first.get_text(" ", strip=True)
        first.decompose()

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
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", candidate.rstrip("/").rsplit("/", 1)[-1])
        if not re.search(r"\.(jpe?g|png|gif|webp|svg)$", name, re.I):
            name += ext
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / name).write_bytes(data)
        return name
    return None


def local_posts(repo: Path) -> dict:
    """Map Medium post id -> slug for every post already in the site."""
    known = {}
    for path in (repo / "src" / "posts").glob("*.md"):
        m = re.search(r'^medium_url: ".*-([0-9a-f]{10,12})"$', path.read_text(encoding="utf-8"), re.M)
        if m:
            known[m.group(1)] = re.sub(r"^\d{4}-\d{2}-\d{2}-|\.md$", "", path.name)
    return known


# Own-Medium URL: <author>.medium.com/... or medium.com/@<author>/..., with a trailing post id.
OWN_LINK = re.compile(
    rf"https?://(?:{AUTHOR}\.medium\.com|medium\.com/@{AUTHOR})/[^)\s\"]*?-([0-9a-f]{{10,12}})(?:[?#][^)\s\"]*)?(?=[)\s\"]|$)"
)


def rewrite_own_links(markdown: str, known: dict) -> str:
    def repl(m):
        slug = known.get(m.group(1))
        return f"/posts/{slug}/" if slug else m.group(0)
    return OWN_LINK.sub(repl, markdown)


@dataclass
class Report:
    written: list = field(default_factory=list)
    skipped: int = 0
    teasers: list = field(default_factory=list)
    image_failures: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def pull(feed_xml: str, repo: Path, fetch=_fetch, dry_run: bool = False) -> Report:
    report = Report()
    known = local_posts(repo)
    taken = set(known.values())
    for post in parse_feed(feed_xml):
        if post.post_id in known:
            report.skipped += 1
            continue
        if not post.body_html:
            report.teasers.append(post.title)
            continue
        slug = make_slug(post.title, post.post_id, taken)
        conv = to_markdown(post.body_html, subtitle=True)
        md = conv.markdown
        for url in image_urls(md):
            if dry_run:
                continue
            name = save_image(url, repo / "src" / "img" / slug, fetch)
            if name:
                md = md.replace(url, f"/img/{slug}/{name}")
            else:
                report.image_failures.append((slug, url))
        md = rewrite_own_links(md, known)
        report.warnings += [(slug, w) for w in conv.warnings]
        stem = f"{post.date}-{slug}"
        if not dry_run:
            (repo / "src" / "posts" / f"{stem}.md").write_text(
                front_matter(post, conv.subtitle) + "\n" + md, encoding="utf-8")
        report.written.append(stem)
    return report


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="list what would be written; write nothing")
    ap.add_argument("--feed-file", help="read the feed from a local file instead of Medium")
    args = ap.parse_args(argv)
    if args.feed_file:
        xml = Path(args.feed_file).read_text(encoding="utf-8")
    else:
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
        xml = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    r = pull(xml, Path.cwd(), dry_run=args.dry_run)
    verb = "would write" if args.dry_run else "wrote"
    print(f"{verb} {len(r.written)} new post(s); {r.skipped} already in the site")
    for stem in r.written:
        print(f"  NEW      src/posts/{stem}.md")
    for title in r.teasers:
        print(f"  TEASER   {title!r}: feed has only a preview (member-only); not written")
    for slug, url in r.image_failures:
        print(f"  IMAGE FAILED  {slug}  {url}")
    for slug, w in r.warnings:
        print(f"  WARNING  {slug}  {w}")


if __name__ == "__main__":
    main(sys.argv[1:])
