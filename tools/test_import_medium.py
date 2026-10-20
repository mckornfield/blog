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
