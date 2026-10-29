import json
from pathlib import Path

from medium_pull import (
    Post, front_matter, hires, image_urls, local_posts, make_slug, parse_feed,
    pull, rewrite_own_links, save_image, slugify, to_markdown,
)

FEED = """<?xml version="1.0"?><rss xmlns:content="http://purl.org/rss/1.0/modules/content/"
 xmlns:dc="http://purl.org/dc/elements/1.1/"><channel><title>Stories</title>
<item><title><![CDATA[The Basement]]></title>
<link>https://mckornfield.medium.com/the-basement-687b78608cd3?source=rss-x</link>
<guid isPermaLink="false">https://medium.com/p/687b78608cd3</guid>
<pubDate>Wed, 28 Oct 2026 13:03:30 GMT</pubDate>
<content:encoded><![CDATA[<h4>And how I remember it</h4><figure><img alt="" src="https://cdn-images-1.medium.com/max/1024/1*abc@2x.jpeg" /><figcaption>Photo by X</figcaption></figure><p>Boo!</p><h4>Section</h4><p>Body.</p><img src="https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=687b78608cd3" width="1" height="1" alt="">]]></content:encoded></item>
<item><title><![CDATA[Paywalled One]]></title>
<link>https://mckornfield.medium.com/paywalled-one-1635cda8b337?source=rss-x</link>
<guid isPermaLink="false">https://medium.com/p/1635cda8b337</guid>
<pubDate>Fri, 09 Oct 2026 05:42:59 GMT</pubDate>
<description><![CDATA[<div>teaser</div>]]></description></item>
</channel></rss>"""

JPEG = b"\xff\xd8\xff fake"


def fetch_ok(url):
    return JPEG, "image/jpeg"


def test_parse_feed_extracts_posts():
    posts = parse_feed(FEED)
    assert [p.title for p in posts] == ["The Basement", "Paywalled One"]
    b = posts[0]
    assert b.post_id == "687b78608cd3"
    assert b.date == "2026-10-28"
    assert b.canonical == "https://medium.com/@mckornfield/the-basement-687b78608cd3"
    assert "Boo!" in b.body_html
    assert posts[1].body_html == ""


def test_leading_h4_is_subtitle_and_tracking_pixel_dropped():
    conv = to_markdown(parse_feed(FEED)[0].body_html, subtitle=True)
    assert conv.subtitle == "And how I remember it"
    assert "And how I remember it" not in conv.markdown
    assert "stat?event" not in conv.markdown
    assert "### Section" in conv.markdown
    assert "![Photo by X](https://cdn-images-1.medium.com/max/1024/1*abc@2x.jpeg)" in conv.markdown


def test_no_subtitle_when_body_starts_with_paragraph():
    conv = to_markdown("<p>Hi</p><h4>Sec</h4>", subtitle=True)
    assert conv.subtitle == ""
    assert "Hi" in conv.markdown


def test_slugify_and_make_slug():
    assert slugify("Mérida: Why I'm Thankful!") == "merida-why-i-m-thankful"
    taken = {"same"}
    assert make_slug("Same", "bbbbbbbbbbbb", taken) == "same-bbbbbbbbbbbb"


def test_front_matter_valid_and_omits_empty_subtitle():
    post = Post("T", "2026-10-28", "https://medium.com/@mckornfield/t-abc123def456", "abc123def456", "")
    fm = front_matter(post, "")
    assert "subtitle" not in fm and "date: 2026-10-28" in fm
    fm = front_matter(post, 'He said "hi"')
    line = next(l for l in fm.splitlines() if l.startswith("subtitle: "))
    assert json.loads(line[len("subtitle: "):]) == 'He said "hi"'


def test_hires_and_save_image(tmp_path):
    assert hires("https://cdn-images-1.medium.com/max/1024/1*a") == "https://cdn-images-1.medium.com/max/1600/1*a"
    name = save_image("https://cdn-images-1.medium.com/max/1024/1*abc@2x.jpeg", tmp_path / "d", fetch_ok)
    assert name == "1_abc_2x.jpeg" and (tmp_path / "d" / name).read_bytes() == JPEG
    assert save_image("https://cdn-images-1.medium.com/max/1024/0*GoQg", tmp_path / "f", fetch_ok) == "0_GoQg.jpg"
    assert save_image("https://x/y", tmp_path / "e", lambda u: (_ for _ in ()).throw(OSError())) is None


def test_rewrite_own_links_to_local_copies():
    known = {"06e7077f8515": "evolved-for-a-more-dangerous-place"}
    md = ("[a](https://mckornfield.medium.com/evolved-for-a-more-dangerous-place-06e7077f8515?source=x) "
          "[b](https://medium.com/@mckornfield/zzz-06e7077f8515) [c](https://other.com/x-06e7077f8515)")
    out = rewrite_own_links(md, known)
    assert "[a](/posts/evolved-for-a-more-dangerous-place/)" in out
    assert "[b](/posts/evolved-for-a-more-dangerous-place/)" in out
    assert "[c](https://other.com/x-06e7077f8515)" in out


def make_repo(tmp_path):
    posts = tmp_path / "src" / "posts"
    posts.mkdir(parents=True)
    (posts / "2026-10-18-old-one.md").write_text(
        '---\ntitle: "Old"\ndate: 2026-10-18\nmedium_url: "https://medium.com/@mckornfield/old-one-06e7077f8515"\n---\n\nx\n')
    return tmp_path


def test_local_posts_maps_ids_to_slugs(tmp_path):
    repo = make_repo(tmp_path)
    assert local_posts(repo) == {"06e7077f8515": "old-one"}


def test_pull_writes_new_post_skips_existing_and_teasers(tmp_path):
    repo = make_repo(tmp_path)
    report = pull(FEED, repo, fetch=fetch_ok)
    assert report.written == ["2026-10-28-the-basement"]
    assert [t for t in report.teasers] == ["Paywalled One"]
    text = (repo / "src/posts/2026-10-28-the-basement.md").read_text()
    assert 'title: "The Basement"' in text and 'subtitle: "And how I remember it"' in text
    assert 'medium_url: "https://medium.com/@mckornfield/the-basement-687b78608cd3"' in text
    assert "](/img/the-basement/" in text and "cdn-images" not in text
    assert list((repo / "src/img/the-basement").iterdir())
    # second run finds nothing new
    again = pull(FEED, repo, fetch=fetch_ok)
    assert again.written == [] and again.skipped == 1


def test_pull_dry_run_writes_nothing(tmp_path):
    repo = make_repo(tmp_path)
    report = pull(FEED, repo, fetch=fetch_ok, dry_run=True)
    assert report.written == ["2026-10-28-the-basement"]
    assert not (repo / "src/posts/2026-10-28-the-basement.md").exists()
