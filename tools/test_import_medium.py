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
