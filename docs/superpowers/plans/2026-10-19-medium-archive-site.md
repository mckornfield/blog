# Medium Archive Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish all 259 of Matt's Medium articles as a searchable static site on GitHub Pages, readable without the paywall.

**Architecture:** A one-time Python script converts the Medium export into Markdown posts plus locally stored images under `src/`. Eleventy builds those into static HTML, Pagefind indexes the output for full-text search, and a GitHub Actions workflow deploys `_site` to Pages.

**Tech Stack:** Python 3 (`beautifulsoup4`, `markdownify`, `pytest`; import only), Node 20+ with Eleventy 3 and Pagefind, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-19-medium-archive-site-design.md`

## Global Constraints

- The repo is public: it may contain only converted articles, their images, site code, and docs. Never commit the export zip or anything from it (`ips.html`, `sessions/`, `reading-history/`, `claps/`, etc.). `.gitignore` must list `*.zip` and `import/` before the first commit.
- Keep only the 259 real articles. Skip the 58 comment replies (no `graf--title` element) and the 2 `draft_*` files.
- Site is served at `https://mckornfield.github.io/blog/`, so Eleventy `pathPrefix` is `/blog/`.
- The only JavaScript on the site is Pagefind search.
- A small "Originally published on Medium" link sits at the bottom of each post.
- No `medium.com` image URLs may remain in the output. A failed download is listed in the import report, not silently left.
- `tools/` (the importer, its tests and requirements) is deleted after the import.
- Every commit message ends with the trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` (pass it as a second `-m`).
- Out of scope: Substack, comments, drafts, RSS, analytics, a custom domain, cross-posting to Medium (planned as a follow-up project).

## Review Focus

- A title that slugifies to nothing (emoji or punctuation only): slug falls back to the Medium post id; two posts with the same title get distinct slugs.
- Titles with quotes, colons or non-ASCII characters (curly quotes, "Mérida"): front matter must stay valid YAML.
- Code blocks containing template syntax (`{{ .Values.x }}`, `{% %}`) from the Helm and Kubernetes posts: must reach the page verbatim, so Markdown must not run through a template engine.
- Images whose URL has no file extension, or whose download fails: saved with an extension taken from the response `Content-Type`; failures are reported.
- A literal `<` in prose (e.g. "a < b") must not be read as an HTML tag by the Markdown renderer.

---

### Task 1: Repo hygiene and import environment

**Files:**
- Create: `.gitignore`
- Create: `tools/requirements.txt`
- Create (untracked): `import/medium/` (extracted export), `.venv/`

**Interfaces:**
- Produces: extracted export at `import/medium/posts/*.html`; Python venv at `.venv` with `bs4`, `markdownify`, `pytest`.

- [ ] **Step 1: Write `.gitignore`**

```
node_modules/
_site/
.venv/
__pycache__/
.pytest_cache/
*.zip
import/
.DS_Store
```

- [ ] **Step 2: Extract the export into an ignored directory**

Run:
```bash
cd /Users/mckornfield/blog
mkdir -p import/medium
unzip -q medium-export-*.zip -d import/medium
ls import/medium/posts | wc -l
```
Expected: `319` (317 published files + 2 drafts).

- [ ] **Step 3: Create the Python environment**

`tools/requirements.txt`:
```
beautifulsoup4
markdownify
pytest
```
Run:
```bash
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
node --version
```
Expected: pip succeeds; Node prints `v20` or newer. If Node is missing or older, stop and ask the user to install Node 20+.

- [ ] **Step 4: Confirm nothing private is tracked, then commit**

Run:
```bash
git status --short
```
Expected: lists `.gitignore`, `docs/`, `tools/` only. No `.zip`, no `import/`, no `.venv/`.

```bash
git add .gitignore tools/requirements.txt docs
git commit -m "chore: ignore export data, add design spec and plan" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Importer: parsing, slugs, front matter

**Files:**
- Create: `tools/import_medium.py`
- Test: `tools/test_import_medium.py`

**Interfaces:**
- Produces (all in `tools/import_medium.py`):
  - `@dataclass Post(title: str, subtitle: str, date: str, canonical: str, body_html: str)`
  - `is_article(html: str) -> bool`
  - `parse_post(html: str) -> Post` (`date` is `YYYY-MM-DD`)
  - `slugify(text: str) -> str`
  - `post_id(filename: str) -> str`
  - `make_slug(title: str, filename: str, taken: set[str]) -> str` (adds the result to `taken`)
  - `front_matter(post: Post) -> str`

- [ ] **Step 1: Write the failing tests**

`tools/test_import_medium.py`:
```python
import pytest
from import_medium import (
    Post, front_matter, is_article, make_slug, parse_post, post_id, slugify,
)


def make_article(title="Hello", body="<p>Body text.</p>", date="2024-12-02",
                 subtitle="A sub", canonical="https://medium.com/@mckornfield/hello-abc123def456"):
    sub = (f'<section data-field="subtitle" class="p-summary">\n{subtitle}\n</section>\n'
           if subtitle else "")
    return (
        '<!DOCTYPE html><html><head><title>t</title></head><body><article class="h-entry">\n'
        f'<header>\n<h1 class="p-name">{title}</h1>\n</header>\n{sub}'
        '<section data-field="body" class="e-content">\n'
        '<section name="a" class="section"><div class="section-divider"><hr class="section-divider"></div>'
        '<div class="section-content"><div class="section-inner">'
        f'<h3 class="graf graf--h3 graf--title">{title}</h3>{body}'
        '</div></div></section>\n</section>\n'
        '<footer><p>By <a href="https://medium.com/@mckornfield" class="p-author h-card">Matt</a> on '
        f'<a href="https://medium.com/p/abc"><time class="dt-published" datetime="{date}T07:47:58.422Z">x</time></a>.</p>'
        f'<p><a href="{canonical}" class="p-canonical">Canonical link</a></p></footer></article></body></html>'
    )


REPLY = make_article().replace(" graf--title", "")


def test_is_article_true_for_article_false_for_reply():
    assert is_article(make_article())
    assert not is_article(REPLY)


def test_parse_post_extracts_fields():
    post = parse_post(make_article(title="Hello World", date="2024-12-02"))
    assert post.title == "Hello World"
    assert post.subtitle == "A sub"
    assert post.date == "2024-12-02"
    assert post.canonical == "https://medium.com/@mckornfield/hello-abc123def456"
    assert "Body text." in post.body_html


def test_parse_post_without_subtitle():
    assert parse_post(make_article(subtitle="")).subtitle == ""


def test_slugify_ascii_lowercase_and_hyphens():
    assert slugify("Mérida: Why I'm Thankful!") == "merida-why-i-m-thankful"
    assert len(slugify("a" * 100)) <= 60


def test_post_id_from_filename():
    assert post_id("2026-07-05_250-2409052ea089.html") == "2409052ea089"
    assert post_id("2022-10-15_Explain-Like-I-m-5--Python-Functions-e71bbefdfbb.html") == "e71bbefdfbb"
    assert post_id("weird.html") == ""


def test_make_slug_falls_back_to_post_id_when_title_has_no_ascii():
    assert make_slug("🙂", "2026-07-05_x-2409052ea089.html", set()) == "2409052ea089"


def test_make_slug_disambiguates_duplicate_titles():
    taken = set()
    first = make_slug("Same", "2024-01-01_Same-aaaaaaaaaaaa.html", taken)
    second = make_slug("Same", "2024-02-02_Same-bbbbbbbbbbbb.html", taken)
    assert first == "same"
    assert second == "same-bbbbbbbbbbbb"
    assert taken == {"same", "same-bbbbbbbbbbbb"}


def test_front_matter_is_valid_yaml_for_awkward_titles():
    post = Post('He said "hi": a \\ test, Mérida “quoted”', "Sub: title", "2024-12-02",
                "https://medium.com/@mckornfield/x-1", "")
    fm = front_matter(post)
    assert fm.startswith("---\n") and fm.endswith("---\n")
    import json
    title_line = next(l for l in fm.splitlines() if l.startswith("title: "))
    assert json.loads(title_line[len("title: "):]) == post.title
    assert "date: 2024-12-02" in fm


def test_front_matter_omits_empty_subtitle():
    fm = front_matter(Post("T", "", "2024-12-02", "https://medium.com/x", ""))
    assert "subtitle" not in fm
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tools -q`
Expected: collection error `ModuleNotFoundError: No module named 'import_medium'`.

- [ ] **Step 3: Write the implementation**

`tools/import_medium.py`:
```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tools -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add tools
git commit -m "feat(import): parse Medium export posts, slugs, front matter" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Importer: body HTML to Markdown

**Files:**
- Modify: `tools/import_medium.py` (append)
- Test: `tools/test_import_medium.py` (append)

**Interfaces:**
- Consumes: nothing new from Task 2 (works on `Post.body_html` strings).
- Produces:
  - `@dataclass Converted(markdown: str, warnings: list[str], embeds: int)`
  - `to_markdown(body_html: str) -> Converted`
  - `image_urls(markdown: str) -> list[str]` (unique, in order of appearance)

- [ ] **Step 1: Write the failing tests**

Append to `tools/test_import_medium.py`:
```python
from import_medium import image_urls, to_markdown


def md(body):
    return to_markdown(body).markdown


def test_drops_title_and_subtitle_elements():
    html = ('<h3 class="graf graf--h3 graf--title">T</h3>'
            '<h4 class="graf graf--h4 graf--subtitle">S</h4><p>Body</p>')
    assert md(html) == "Body\n"


def test_drops_first_divider_keeps_later_ones_as_rules():
    html = ('<div class="section-divider"><hr class="section-divider"></div><p>One</p>'
            '<div class="section-divider"><hr class="section-divider"></div><p>Two</p>')
    out = md(html)
    assert out.startswith("One")
    assert "One\n\n---\n\nTwo" in out


def test_removes_scripts():
    assert "alert" not in md("<p>Hi</p><script>alert(1)</script>")


def test_figure_becomes_image_and_italic_caption():
    html = ('<figure><div><img src="https://cdn-images-1.medium.com/max/800/0*abc" data-width="1"></div>'
            '<figcaption class="imageCaption">Photo by <a href="https://x.com">X</a></figcaption></figure>')
    out = md(html)
    assert "![Photo by X](https://cdn-images-1.medium.com/max/800/0*abc)" in out
    assert "*Photo by [X](https://x.com)*" in out
    assert image_urls(out) == ["https://cdn-images-1.medium.com/max/800/0*abc"]


def test_figure_without_caption():
    out = md('<figure><img src="https://cdn-images-1.medium.com/max/800/1*z"></figure>')
    assert "![](https://cdn-images-1.medium.com/max/800/1*z)" in out


def test_image_urls_unique_and_ordered():
    text = "![a](http://h/1) ![b](http://h/2) ![c](http://h/1)"
    assert image_urls(text) == ["http://h/1", "http://h/2"]


def test_code_block_is_fenced_and_untouched():
    html = ('<p>Run:</p><pre data-code-block-lang="yaml" class="graf graf--pre">'
            '<span class="pre--content">a: {{ .Values.x }}<br><br>b: <span class="hljs-string">1</span></span></pre>')
    out = md(html)
    assert "```yaml\na: {{ .Values.x }}\n\nb: 1\n```" in out


def test_code_block_containing_backticks_uses_tilde_fence():
    html = '<pre><span class="pre--content">echo ```hi```</span></pre>'
    assert "~~~~\necho ```hi```\n~~~~" in md(html)


def test_multiple_code_blocks_keep_their_own_content():
    pres = "".join(f'<pre data-code-block-lang="bash"><span>cmd{i}</span></pre><p>x</p>' for i in range(12))
    out = md(pres)
    for i in range(12):
        assert f"```bash\ncmd{i}\n```" in out


def test_headings_shift_under_page_title():
    out = md("<h2>A</h2><h3>B</h3><h4>C</h4>")
    assert "## A" in out and "## B" in out and "### C" in out
    assert "\n# " not in "\n" + out


def test_mixtape_embed_becomes_link():
    html = ('<div class="graf graf--mixtapeEmbed"><a class="markup--mixtapeEmbed-anchor" href="https://example.com/p">'
            '<strong class="markup--mixtapeEmbed-strong">Cool Post</strong><em class="markup--mixtapeEmbed-em">desc</em></a>'
            '<a href="https://example.com/p" class="js-mixtapeImage" style="background-image: url(x);"></a></div>')
    conv = to_markdown(html)
    assert "[Cool Post](https://example.com/p)" in conv.markdown
    assert conv.embeds == 1


def test_pullquote_becomes_blockquote():
    assert "> Wise words" in md('<blockquote class="graf graf--pullquote">Wise words</blockquote>')
    assert "> Said" in md('<p class="graf graf--pullquote">Said</p>')


def test_lists_and_inline_formatting():
    out = md("<ul><li>one <strong>b</strong></li><li>two</li></ul>")
    assert "- one **b**" in out and "- two" in out


def test_literal_less_than_in_prose_is_escaped():
    out = md("<p>if a &lt; b then</p>")
    assert "a &lt; b" in out
    assert "a < b" not in out


def test_unconverted_tags_produce_warnings():
    conv = to_markdown("<table><tr><td>x</td></tr></table><iframe src='y'></iframe>")
    assert "unconverted <table>" in conv.warnings
    assert "unconverted <iframe>" in conv.warnings
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tools -q`
Expected: ImportError for `image_urls` / `to_markdown`.

- [ ] **Step 3: Write the implementation**

Append to `tools/import_medium.py`, and add `from dataclasses import dataclass, field`, `from bs4 import BeautifulSoup, NavigableString` and `from markdownify import markdownify` to the imports at the top:
```python
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
```

- [ ] **Step 4: Run tests and fix library quirks**

Run: `.venv/bin/python -m pytest tools -q`
Expected: all pass. If `test_literal_less_than_in_prose_is_escaped` fails because markdownify escaped the ampersand (output contains `\&lt;`), pass `escape_misc=False` to `markdownify(...)`. If the pullquote test fails, check how markdownify renders `blockquote` and adjust only the assertion's expected string, not the behavior. Do not change any other behavior to make a test pass; investigate first.

- [ ] **Step 5: Commit**

```bash
git add tools
git commit -m "feat(import): convert Medium body HTML to Markdown" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Importer: images, pipeline, and the real import

**Files:**
- Modify: `tools/import_medium.py` (append)
- Test: `tools/test_import_medium.py` (append)
- Create (generated, committed): `src/posts/*.md`, `src/img/<slug>/*`

**Interfaces:**
- Consumes: `Post`, `is_article`, `parse_post`, `make_slug`, `front_matter`, `to_markdown`, `image_urls`.
- Produces:
  - `hires(url: str) -> str`
  - `save_image(url: str, dest_dir: Path, fetch=_fetch) -> str | None` (returns the saved filename; `fetch(url) -> (bytes, content_type)`)
  - `@dataclass Report(imported, replies, drafts, image_failures: list[(slug, url)], warnings: list[(slug, text)], embeds: list[slug])`
  - `import_export(export_dir: Path, repo_dir: Path, fetch=_fetch) -> Report`
  - Output convention: `src/posts/<date>-<slug>.md`; images at `/img/<slug>/<file>` (root-relative in Markdown).

- [ ] **Step 1: Write the failing tests**

Append to `tools/test_import_medium.py`:
```python
from pathlib import Path

from import_medium import hires, import_export, save_image

JPEG = b"\xff\xd8\xff fake"


def fake_fetch_factory(log=None, fail_hires=False, fail_all=False):
    def fetch(url):
        if log is not None:
            log.append(url)
        if fail_all or (fail_hires and "/max/1600/" in url):
            raise OSError("boom")
        return JPEG, "image/jpeg"
    return fetch


def test_hires_rewrites_width():
    assert hires("https://cdn-images-1.medium.com/max/800/0*abc") == "https://cdn-images-1.medium.com/max/1600/0*abc"
    assert hires("https://cdn-images-1.medium.com/other/x") == "https://cdn-images-1.medium.com/other/x"


def test_save_image_adds_extension_from_content_type(tmp_path):
    name = save_image("https://cdn-images-1.medium.com/max/800/0*GoQg8bKAYF5hwXgT", tmp_path / "d",
                      fake_fetch_factory())
    assert name == "0_GoQg8bKAYF5hwXgT.jpg"
    assert (tmp_path / "d" / name).read_bytes() == JPEG


def test_save_image_falls_back_to_original_url(tmp_path):
    log = []
    name = save_image("https://cdn-images-1.medium.com/max/800/0*abc", tmp_path,
                      fake_fetch_factory(log, fail_hires=True))
    assert name == "0_abc.jpg"
    assert log == ["https://cdn-images-1.medium.com/max/1600/0*abc",
                   "https://cdn-images-1.medium.com/max/800/0*abc"]


def test_save_image_returns_none_when_everything_fails(tmp_path):
    assert save_image("https://cdn-images-1.medium.com/max/800/0*abc", tmp_path,
                      fake_fetch_factory(fail_all=True)) is None


def build_export(tmp_path):
    posts = tmp_path / "export" / "posts"
    posts.mkdir(parents=True)
    img = '<figure><img src="https://cdn-images-1.medium.com/max/800/0*abc"></figure>'
    (posts / "2024-12-02_Hello-aaaaaaaaaaaa.html").write_text(make_article("Hello", f"<p>Hi</p>{img}"), encoding="utf-8")
    (posts / "2024-12-03_Reply-bbbbbbbbbbbb.html").write_text(REPLY, encoding="utf-8")
    (posts / "draft_Later-cccccccccccc.html").write_text(make_article("Later"), encoding="utf-8")
    return tmp_path / "export", tmp_path / "repo"


def test_import_export_writes_post_and_image_and_skips_replies_and_drafts(tmp_path):
    export, repo = build_export(tmp_path)
    report = import_export(export, repo, fake_fetch_factory())
    assert (report.imported, report.replies, report.drafts) == (1, 1, 1)
    post = repo / "src" / "posts" / "2024-12-02-hello.md"
    text = post.read_text(encoding="utf-8")
    assert text.startswith('---\ntitle: "Hello"\n')
    assert "![](/img/hello/0_abc.jpg)" in text
    assert "medium.com/max" not in text
    assert (repo / "src" / "img" / "hello" / "0_abc.jpg").exists()
    assert list((repo / "src" / "posts").glob("*.md")) == [post]


def test_import_export_reports_failed_images(tmp_path):
    export, repo = build_export(tmp_path)
    report = import_export(export, repo, fake_fetch_factory(fail_all=True))
    assert report.image_failures == [("hello", "https://cdn-images-1.medium.com/max/800/0*abc")]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tools -q`
Expected: ImportError for `hires` / `save_image` / `import_export`.

- [ ] **Step 3: Write the implementation**

Add `import sys`, `import urllib.request` and `from pathlib import Path` to the imports at the top of `tools/import_medium.py`, then append:
```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tools -q`
Expected: all pass.

- [ ] **Step 5: Run the real import**

Run: `.venv/bin/python tools/import_medium.py import/medium . | tee import/report.txt`
Expected first line: `imported=259 replies_skipped=58 drafts_skipped=2`. This downloads about 419 images and may take several minutes. Review `IMAGE FAILED` and `WARNING` lines. For each failed image, fetch it manually or decide with the user; for each warning, open the post and fix the Markdown by hand. Do not continue while any `IMAGE FAILED` line remains unresolved.

- [ ] **Step 6: Inspect the output**

Run:
```bash
ls src/posts | wc -l
ls src/img | wc -l
grep -rl 'cdn-images-1.medium.com' src | head
grep -rlE 'class="graf|section-inner|<div' src/posts | head
head -30 src/posts/2026-10-09-my-stupid-expense-capturing-thingy.md
grep -c '{{' src/posts/*helm* 2>/dev/null | head
```
Expected: 259 posts; image directory count about 258 (one article has no image); the two greps print nothing (any hit is a conversion bug to investigate); the head shows clean front matter and Markdown with `/img/...` links. Read one Kubernetes/Helm post and one long personal essay end to end and confirm they read correctly.

- [ ] **Step 7: Commit**

```bash
git add src tools
git commit -m "feat: import 259 Medium articles and images" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Eleventy site, theme, and Pagefind search

**Files:**
- Create: `package.json`, `eleventy.config.js`
- Create: `src/posts/posts.json`, `src/_includes/base.njk`, `src/_includes/post.njk`
- Create: `src/index.njk`, `src/404.njk`, `src/css/style.css`

**Interfaces:**
- Consumes: `src/posts/*.md` with front matter `title`, `subtitle?`, `date`, `medium_url`; images at `/img/...`.
- Produces: `npm run build` creates `_site/` including `_site/pagefind/`; posts at `/blog/posts/<slug>/`.

- [ ] **Step 1: Install dependencies**

Run:
```bash
npm init -y
npm install --save-dev @11ty/eleventy pagefind
```
Then replace the generated `package.json` fields so it contains:
```json
{
  "name": "blog",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "eleventy && pagefind --site _site",
    "start": "eleventy --serve"
  }
}
```
(keep the `devDependencies` block npm wrote).

- [ ] **Step 2: Write `eleventy.config.js`**

```js
import { HtmlBasePlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  // Prefixes root-relative links, images, css and scripts with pathPrefix.
  eleventyConfig.addPlugin(HtmlBasePlugin);
  eleventyConfig.addPassthroughCopy("src/img");
  eleventyConfig.addPassthroughCopy("src/css");

  eleventyConfig.addFilter("isoDate", (d) => d.toISOString().slice(0, 10));
  eleventyConfig.addFilter("longDate", (d) =>
    d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })
  );
  // Newest first, grouped as [[year, [posts...]], ...]
  eleventyConfig.addFilter("groupByYear", (posts) => {
    const sorted = [...posts].sort((a, b) => b.date - a.date);
    const groups = new Map();
    for (const p of sorted) {
      const y = p.date.getUTCFullYear();
      if (!groups.has(y)) groups.set(y, []);
      groups.get(y).push(p);
    }
    return [...groups];
  });

  return {
    dir: { input: "src", output: "_site" },
    pathPrefix: "/blog/",
    // Posts contain Helm/Go template syntax ({{ }}); never run Markdown through a template engine.
    markdownTemplateEngine: false,
  };
}
```

- [ ] **Step 3: Write the templates**

`src/posts/posts.json`:
```json
{
  "layout": "post.njk",
  "tags": "posts",
  "permalink": "/posts/{{ page.fileSlug }}/index.html"
}
```

`src/_includes/base.njk`:
```njk
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% if title %}{{ title }} · {% endif %}Matt Kornfield</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <header class="site"><a href="/">Matt Kornfield</a></header>
  <main>{{ content | safe }}</main>
</body>
</html>
```

`src/_includes/post.njk`:
```njk
---
layout: base.njk
---
<article data-pagefind-body>
  <h1>{{ title }}</h1>
  {% if subtitle %}<p class="subtitle">{{ subtitle }}</p>{% endif %}
  <p class="meta"><time datetime="{{ date | isoDate }}">{{ date | longDate }}</time></p>
  <div class="body">{{ content | safe }}</div>
  <p class="origin">Originally published on <a href="{{ medium_url }}">Medium</a>.</p>
</article>
```

`src/index.njk`:
```njk
---
layout: base.njk
title: All posts
---
<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<div id="search"></div>
<script src="/pagefind/pagefind-ui.js"></script>
<script>
  window.addEventListener("DOMContentLoaded", function () {
    new PagefindUI({ element: "#search", showImages: false, showSubResults: true, resetStyles: false });
  });
</script>
{% for group in collections.posts | groupByYear %}
<h2 class="year">{{ group[0] }}</h2>
<ul class="posts">
  {% for post in group[1] %}
  <li><a href="{{ post.url }}">{{ post.data.title }}</a> <time datetime="{{ post.date | isoDate }}">{{ post.date | longDate }}</time></li>
  {% endfor %}
</ul>
{% endfor %}
```

`src/404.njk`:
```njk
---
layout: base.njk
title: Not found
permalink: /404.html
---
<h1>Not found</h1>
<p><a href="/">Back to all posts</a></p>
```

- [ ] **Step 4: Write `src/css/style.css`**

```css
:root {
  color-scheme: light dark;
  --bg: #fdfdfc;
  --text: #1e1e1e;
  --muted: #6b6b6b;
  --link: #1a5fb4;
  --rule: #e2e2e0;
  --code-bg: #f1f1ef;
  --pagefind-ui-scale: 0.9;
  --pagefind-ui-primary: #1a5fb4;
  --pagefind-ui-text: #1e1e1e;
  --pagefind-ui-background: #fdfdfc;
  --pagefind-ui-border: #e2e2e0;
  --pagefind-ui-tag: #f1f1ef;
  --pagefind-ui-font: Georgia, "Times New Roman", serif;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #161616;
    --text: #e6e6e3;
    --muted: #9a9a96;
    --link: #7cb2ff;
    --rule: #2e2e2c;
    --code-bg: #232321;
    --pagefind-ui-primary: #7cb2ff;
    --pagefind-ui-text: #e6e6e3;
    --pagefind-ui-background: #161616;
    --pagefind-ui-border: #2e2e2c;
    --pagefind-ui-tag: #232321;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 1.125rem/1.7 Georgia, "Times New Roman", serif;
}
a { color: var(--link); }
header.site, main { max-width: 44rem; margin: 0 auto; padding: 0 1rem; }
header.site { padding-top: 1.25rem; padding-bottom: 1rem; border-bottom: 1px solid var(--rule); font-weight: bold; }
header.site a { color: var(--text); text-decoration: none; }
main { padding-top: 1.5rem; padding-bottom: 4rem; }
h1 { line-height: 1.25; margin-bottom: 0.25rem; }
.subtitle { color: var(--muted); font-size: 1.2rem; margin-top: 0; }
.meta, .origin, .posts time { color: var(--muted); font-size: 0.9rem; }
.origin { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--rule); }
.body img { max-width: 100%; height: auto; display: block; margin: 1.5rem auto 0.5rem; }
.body blockquote { margin-left: 0; padding-left: 1rem; border-left: 3px solid var(--rule); color: var(--muted); }
.body pre { background: var(--code-bg); padding: 1rem; overflow-x: auto; font-size: 0.85rem; line-height: 1.5; }
.body code { background: var(--code-bg); padding: 0.1em 0.3em; font-size: 0.9em; }
.body pre code { background: none; padding: 0; }
.body hr { border: 0; border-top: 1px solid var(--rule); margin: 2rem 0; }
.year { margin-top: 2rem; border-bottom: 1px solid var(--rule); }
.posts { list-style: none; padding: 0; }
.posts li { display: flex; justify-content: space-between; gap: 1rem; padding: 0.25rem 0; }
.posts time { white-space: nowrap; flex-shrink: 0; }
@media (max-width: 30rem) { .posts li { flex-direction: column; gap: 0; } }
```

- [ ] **Step 5: Build and check counts**

Run:
```bash
npm run build
ls _site/posts | wc -l
```
Expected: the build succeeds; Pagefind prints `Indexed 259 pages`; `ls` prints `259`.

- [ ] **Step 6: Check template syntax survived and no remote images remain**

Run:
```bash
grep -rl '{{' src/posts | head -3
f=$(grep -rl '{{ ' src/posts/*.md | head -1); echo "$f"
grep -c '{{' "_site/posts/$(basename "$f" .md | sed 's/^[0-9-]\{10\}-//')/index.html"
grep -rl 'cdn-images-1.medium.com' _site | head
```
Expected: the `{{` line count in the built page is at least 1 (code survived verbatim); the last grep prints nothing.

- [ ] **Step 7: View the site locally and search**

The build uses the `/blog/` prefix, so serve it under that path:
```bash
rm -rf import/serve && mkdir -p import/serve && cp -r _site import/serve/blog
python3 -m http.server 8000 -d import/serve
```
Run the server in the background. Open `http://localhost:8000/blog/` (use the `claude-in-chrome` or built-in browser skill if available; otherwise ask the user to look). Check: the home page lists posts by year; searching "Qualia" finds "On Qualia and Quantia"; searching "Kubernetes" returns many results; a post page shows images, a code block, and the Medium link at the bottom; dark mode looks right (toggle the OS setting or emulate). Stop the server.

- [ ] **Step 8: Commit**

```bash
git add package.json package-lock.json eleventy.config.js src
git commit -m "feat: Eleventy site with Pagefind search" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Deploy workflow, cleanup, and publish

**Files:**
- Create: `.github/workflows/deploy.yml`
- Delete: `tools/`

**Interfaces:**
- Consumes: `npm run build` from Task 5 (writes `_site/`).
- Produces: a live site at `https://mckornfield.github.io/blog/`.

- [ ] **Step 1: Write the workflow**

`.github/workflows/deploy.yml`:
```yaml
name: Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Remove the importer**

The spec says the repo keeps only articles, images and site code. Run:
```bash
git rm -r tools
rm -rf .venv tools
git status --short
```
Expected: only `tools/` deletions and the new workflow. `import/` stays on disk but ignored; tell the user it can be deleted along with the zip once they are happy.

- [ ] **Step 3: Final privacy and correctness check**

Run:
```bash
git add .github
git ls-files | grep -Ei 'zip|ips\.html|sessions|claps|reading-history|import/' ; echo "private-files-tracked-exit=$?"
git ls-files src/posts | grep -c '\.md$'
npm run build
```
Expected: the `grep` prints nothing and `exit=1`; post count is `259`; the build succeeds and indexes 259 pages.

- [ ] **Step 4: Commit**

```bash
git commit -m "ci: deploy to GitHub Pages; remove one-time importer" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 5: Confirm with the user before publishing**

Creating a public repo and pushing is outward-facing. Ask the user to confirm creating `mckornfield/blog` as a **public** repo and pushing all 259 articles. Do not run Step 6 until they say yes.

- [ ] **Step 6: Create the repo, enable Pages, push**

Run:
```bash
gh repo create mckornfield/blog --public --source=. --push
gh api -X POST repos/mckornfield/blog/pages -f build_type=workflow
gh run watch
```
Expected: the workflow run succeeds. If `gh api` reports Pages already exists, use `-X PUT` instead.

- [ ] **Step 7: Verify the live site**

Open `https://mckornfield.github.io/blog/`. Confirm the post list loads, search for "Qualia" finds the post, and one post with images and code renders correctly. Report the URL to the user.
