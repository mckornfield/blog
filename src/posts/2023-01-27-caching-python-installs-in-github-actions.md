---
title: "Caching Python Installs in GitHub Actions"
subtitle: "The journey of 1000 packages begins with a single pip install"
date: 2023-01-27
medium_url: "https://medium.com/@mckornfield/caching-python-installs-in-github-actions-8309e12a15e6"
---

The journey of 1000 packages begins with a single `pip install`

![Saving ~3 minutes with some caching!](/img/caching-python-installs-in-github-actions/1_43p3UFNlP8goPkmLPBYB8w.png.png)

*Saving ~3 minutes with some caching!*

### The Beginning: No Caching

In the beginning, our basic GitHub Actions Python install steps were:

```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.9'
- run: make python-install
```

I was surprised by how long it took to download packages for our larger Python project. In that install step there were some pretty slow packages to install (ahem, [pytorch](https://github.com/pytorch/pytorch/issues/1022)).

I said to myself, we spend 3–4 minutes re-downloading the same packages all day. Why can’t we just cache the dang things?

### The Middle: Using the Built-in Python Caching Action

Well of course it turns out you can! And GitHub offers a pretty neat way.

I looked around for what readily available GitHub Actions there were that used the Actions caching feature, and stumbled upon this [option for the setup action](https://github.com/actions/setup-python#caching-packages-dependencies). So yeah caching was as easy as:

```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.9'
    cache: 'pip'
- run: make python-install
```

Now when our jobs ran, if they had the same `requirements.txt` file, python version, and OS, then they would reuse the cache entries.

Before declaring victory let’s talk through…

**Some Details**

Getting into some of the specifics, GitHub Actions has a [default cache size limit at 10GB](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows). It also expires items from the cache on a weekly basis. So if you’re running many jobs a day, installing the same Python (or any other kind for that matter) dependencies, the cache is probably a good thing to reach for.

The thing about this cache offered by the `setup-python` action is that it caches the `pip`,`pipenv` , or `poetry` installation directories. That means instead of making network calls to *the* [Python Package Index](https://pypi.org/) (`pypi`), these cache hits grab an entry from the GitHub Actions repository cache.

If no cache entry is found, it can fall back to a related entry, but one that might not match exactly the contents of `requirements.txt` , that way you have SOME gains on download time.

Downloading and un-tarring the cache entry is faster than downloading things from any `pypi` , considering it’s all within GitHub’s infrastructure, and one single entry instead of many other entries.

So things must have been a lot faster, right?

**Not Fast Enough**

The problem with the midpoint in my journey was that the GitHub Actions pip install still took on the order of minutes. I wasn’t seeing much of a speedup, because what was happening was:

- GitHub Actions would pull down and unzip the cached pip entries (instead of getting them from `pypi` )
- The `make install-python` action would have to go over and reinstall hundreds of packages, even though they were just a few directories away

I might have saved a bit of network time but only marginally some. The times went from ~3ish minutes to ~2ish. I needed to find a way to go faster…

### The End: Caching the Virtualenv

Part of what made the speedup not so significant was the work that pip itself still had to do. When using cached entries for `pip install` , that still meant pip would do some work to move files around, or (heaven forbid) build some projects from source that didn’t have `wheels` . Blegh!

When it seemed like I’d just spent a lot of time moving some network calls from here over to there, I did a bit more searching and found a source of inspiration: what if I installed everything into a virtualenv and cached that? And then skipped the pip install completely?

Sure, the cache size was bigger (now it was on the order of 1GB instead of 100s of MB). But that’s because it had the final installed binaries in it.

But remember: [storage costs way less than runtime for cloud services](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#per-minute-rates).

Consider what 8 cents gets you as of this writing on GitHub Actions:

- 10GB of storage per day ~ $0.08
- 10 Minutes of Runtime on a 2CPU Linux Runner ~ $0.08

So if you just store 1–2GB of cache data and it saves you ~2–3 minutes, you’ll essentially break even. Considering back to back pushes for branch CI runs can add up to hours of CI time, storage is the way to go.

So how do you cache the virtualenv? It looks something like:

```yaml
- name: Set up Python
  id: setup_python
  uses: actions/setup-python@v1
  with:
    python-version: 3.9
- name: cache virtualenv
  uses: actions/cache@v3
  id: cache-venv
  with:
    path: ./.venv/
    key: ${{ runner.os }}-${{ steps.setup_python.outputs.python-version }}-venv-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-${{ steps.setup_python.outputs.python-version }}-venv-
- name: Install dependencies
  shell: bash
  run: |
    python -m venv ./.venv
    source ./.venv/bin/activate
    python -m pip install -r requirements.txt
  if: steps.cache-venv.outputs.cache-hit != 'true'
- name: Install repo project # We do this since the install deps step can be skipped
  shell: bash
  run: |
    source ./.venv/bin/activate
    python -m pip install -U -e ./python
```

The above:

- Tries to read a value from the cache into `.venv` , falling back if there’s no exact match on the `requirements.txt` file to another cache entry
- Installs dependencies ONLY if there’s no cache hit
- Installs the repo based Python project (in case there are code changes but no `requirements.txt` changes)

Later steps then just used the virtualenv to execute various Python tasks instead of the globally available python in the GitHub Actions runner.

At the end of our journey, we brought down the install time to under 1 minute, from 3–4 minutes at the beginning. And we gave `pypi` a break :)

Thanks for reading!
