# Medium Archive Site: Design

## Goal
A static site on GitHub Pages that hosts all of Matt's Medium articles, so they are
easy to search and readable without the Medium paywall. Substack is out of scope
(there is almost nothing there).

## Constraints
- The articles are the author's own.
- The repo is public, so it must contain only the converted articles, their images,
  and the site code. The Medium export zip also holds private data (`ips.html`,
  `sessions/`, `reading-history/`, `claps/`, etc.) and must never be committed.
- Static site only; search runs client-side.
- Served from `https://mckornfield.github.io/blog/` (repo is named `blog`), so the
  build uses a path prefix of `/blog/`.

## Source data
Medium export zip, extracted locally to an untracked `import/` directory.
- `posts/` has 317 published files plus 2 `draft_*` files.
- 259 published files are real articles (they contain a `graf--title` element).
- 58 are comment replies on other people's posts (no title element). Excluded.
- Drafts are excluded.
- Each file's footer carries the publish date (`dt-published`) and the canonical
  Medium URL (`p-canonical`).
- Images are hotlinked from `cdn-images-1.medium.com`.

## Repo layout
```
src/
  posts/YYYY-MM-DD-slug.md   front matter: title, subtitle, date, medium_url
  img/<post-slug>/*          images downloaded from Medium
  _includes/                 base layout, post layout
  index.njk                  posts grouped by year, newest first
  404.njk
eleventy.config.js
package.json
.github/workflows/deploy.yml
.gitignore                   *.zip, import/
docs/superpowers/specs/      this document
```

## One-time import (`tools/import_medium.py`)
1. Read the extracted export from `import/`; keep only files with `graf--title`.
2. Strip Medium inline CSS and wrapper `div`s; drop the duplicated title and
   subtitle at the top of the body.
3. Convert to Markdown, keeping headings, code blocks, quotes, lists and links.
   Image captions and Medium embeds (gists, YouTube, link cards) that cannot be
   converted cleanly are listed in a report, not silently dropped.
4. Download each image to `src/img/<slug>/` and rewrite links. Failed downloads
   are listed in the report; no hotlinks to `medium.com` remain.
5. Take date and canonical URL from the footer.

The script is deleted after the import, since the repo should hold only articles,
images and site code.

## Site
- Eleventy generates the pages from `src/posts`.
- Plain, readable, mobile-friendly theme with light and dark modes. No JavaScript
  except search.
- Home page lists posts by year, with a search box at the top.
- Pagefind builds a full-text index at deploy time and powers search with snippets
  and highlighting.
- Each post page shows title, subtitle, date and full text. A small
  "Originally published on Medium" link to `medium_url` sits at the bottom.

## Deployment
GitHub Actions workflow on every push to `main`: install, build Eleventy, run
Pagefind on the output, deploy to Pages. One manual step: set Pages -> Source to
"GitHub Actions" in the repo settings.

## Verification
- Build succeeds.
- Post count is 259.
- No `medium.com` image URLs remain in the output.
- Search returns results for known terms (for example "Kubernetes" and "Qualia").
- Spot-check several posts visually, including ones with code blocks, images,
  and embeds.

## Out of scope
Substack posts, comments/replies, drafts, analytics, a custom domain, RSS (can be
added later).
