---
title: "Why is Importing in Python So Slow?"
subtitle: "tl;dr all that file I/O"
date: 2026-09-21
medium_url: "https://medium.com/@mckornfield/why-is-importing-in-python-so-slow-0a327a429483"
---

![Photo by Zach Tilford on Unsplash (not a Python probably)](/img/why-is-importing-in-python-so-slow/0_SuTmdCRIDGmH-KHT.jpg)

*Photo by [Zach Tilford](https://unsplash.com/@zach_tilford?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral) (not a Python probably)*

### Ye old Cprofile

I started wondering why certain CLI commands at work were taking so long. I ran Cprofile on just an import and it just spammed the heck out of my terminal window. Running `head` and installing just `pandas` with `uv`, I find a good amount of time passes.

```xml
$ cat test.py
import pandas

$ uv run --with pandas python -m cProfile -s cumtime test.py | head -n 15
         316504 function calls (308669 primitive calls) in 0.451 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       67    0.001    0.000    1.293    0.019 __init__.py:1(<module>)
    432/1    0.002    0.000    0.451    0.451 {built-in method builtins.exec}
        1    0.000    0.000    0.451    0.451 test.py:1(<module>)
    521/1    0.001    0.000    0.451    0.451 <frozen importlib._bootstrap>:1165(_find_and_load)
    521/1    0.001    0.000    0.451    0.451 <frozen importlib._bootstrap>:1120(_find_and_load_unlocked)
    498/1    0.001    0.000    0.451    0.451 <frozen importlib._bootstrap>:666(_load_unlocked)
    410/1    0.000    0.000    0.451    0.451 <frozen importlib._bootstrap_external>:934(exec_module)
   1173/2    0.000    0.000    0.450    0.225 <frozen importlib._bootstrap>:233(_call_with_frames_removed)
   464/42    0.000    0.000    0.310    0.007 {built-in method builtins.__import__}
  672/377    0.000    0.000    0.217    0.001 <frozen importlib._bootstrap>:1207(_handle_fromlist)
```

Computers are pretty fast. Importing pandas takes around ~0.2–0.5 seconds no matter how many times I run this, and even if it’s “warm.”

This cProfile output isn’t very helpful other than telling me “I was importing your file for the whole time.”

### What Happens When You Import?

If you read through the [modules](https://docs.python.org/3/tutorial/modules.html) Python docs, you’ll find that importing is ~three steps, e.g., if I run `import foo`

1. Scan all the files in a PYTHONPATH until we find a corresponding module with that name (any foos here?)
2. If a `foo` is found, then run the code in its `__init__.py` and updates the python context to have `foo` as an available variable with attributes.
3. If not, throw a nice `ModuleNotFoundError`

The step (2) of “run arbitrary code” is really the most “just go wild here.”

### Python is Interpreted, and that matters for imports

When you run a Python program for the *very* first time, all of that text that makes up the Python program has to be fed to an interpreter. This turns into some unreadable nonsense. If you had a simple `test.py` file with just `print("hello")` in it, its corresponding `.pyc` file (on MacOS with Python 14) would be:

```lua
�j���]!R4R#)�helloN)�print���test.py<module>rs
                                                 ���g�r
```

Imports get mangled a bit more weirdly, but what happens when you run `import openai` the very first time on a virtual environment, is that every file that gets scanned over/run via Python’s module strategy needs to be compiled to a `.pyc` file. When we have big libraries with large `ext` packages, it can be 100s, 1000s or even more files that are scanned over.

### Understanding flamegraphs

If you don’t understand flamegraphs, it’s ok, you’re in good company. I had used them before but did [a bit of reading](https://www.brendangregg.com/flamegraphs.html) on what the colors come from. Turns out they are random, just to differentiate the different calls.

So what we should understand about flamegraphs is:

1. There is no “time” component, since processor speed will make things slower or faster, just how many “calls”
2. The stacking portion is just to show where of the call “duration” is other time going
3. The colors are random, but let you differentiate things

Here’s a flamegraph I made for the Pandas import. It’s definitely hard to read as things are getting squished, but you’ll see underneath `find_and_load`, most of that time is spent in the middle, running `exec_module`, which, yeah that’s running code in the `__init__.py` files.

![flamegraph by function](/img/why-is-importing-in-python-so-slow/1_KbvuMw4wUuPFlsT48kcO_w.png.jpg)

*flamegraph by function*

You can also build a flamegraph of imports of other packages underneath. Pandas itself imports quite a few modules, numpy being the biggest offender in time, outside of a bunch of internal pandas imports.

![](/img/why-is-importing-in-python-so-slow/1_DQi7iHeowi9ljLWsa0AVGw.png.png)

The flamegraphs just tell us “of this amount of processor time, this is where the lionshare of it was eaten up.”

I generated a table summary at the end of the flamegraph/cProfile analysis that grouped functions together as part of this, and we can see that ~37% goes to reading the files, while there are some interesting calls like “regex compilation” or “bytecode compilation”, which even on a warm run takes up 9% of the time.

```bash
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ category                       ┃ self ms ┃ % of profiled self time ┃ top contributors                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ file read I/O                  │  116.44 │                   36.8% │ <built-in method io.open_code> (~:0); <method 'read' of '_io.BufferedReader' objects>     │
│                                │         │                         │ (~:0)                                                                                     │
│ other python code              │   57.05 │                   18.0% │ cleandoc                                                                                  │
│                                │         │                         │ (/Users/mkornfield/.local/share/uv/python/cpython-3.11.13-macos-aarch64-none/lib/python3. │
│                                │         │                         │ 11/inspect.py:863); <built-in method builtins.exec> (~:0)                                 │
│ native extension load (dlopen) │   51.66 │                   16.3% │ <built-in method _imp.create_dynamic> (~:0); <built-in method _imp.exec_dynamic> (~:0)    │
│ bytecode compile/validate      │   28.38 │                    9.0% │ <built-in method marshal.loads> (~:0); _compile_bytecode (<frozen                         │
│                                │         │                         │ importlib._bootstrap_external>:727)                                                       │
│ import machinery (find/load)   │   25.15 │                    7.9% │ find_spec (<frozen importlib._bootstrap_external>:1607); _find_spec (<frozen              │
│                                │         │                         │ importlib._bootstrap>:1054)                                                               │
│ filesystem stat/path search    │   16.51 │                    5.2% │ <built-in method posix.listdir> (~:0); <built-in method posix.stat> (~:0)                 │
│ regex compilation              │    9.34 │                    3.0% │ _parse                                                                                    │
│                                │         │                         │ (/Users/mkornfield/.local/share/uv/python/cpython-3.11.13-macos-aarch64-none/lib/python3. │
│                                │         │                         │ 11/re/_parser.py:516); _compile                                                           │
│                                │         │                         │ (/Users/mkornfield/.local/share/uv/python/cpython-3.11.13-macos-aarch64-none/lib/python3. │
│                                │         │                         │ 11/re/_compiler.py:37)                                                                    │
│ package module-level code      │    6.07 │                    1.9% │ <module>                                                                                  │
│                                │         │                         │ (/Users/mkornfield/.cache/profile-import/venvs/pandas-652a06995c/lib/python3.11/site-pack │
│                                │         │                         │ ages/numpy/ma/core.py:1); <module>                                                        │
│                                │         │                         │ (/Users/mkornfield/.cache/profile-import/venvs/pandas-652a06995c/lib/python3.11/site-pack │
│                                │         │                         │ ages/numpy/__init__.py:1)                                                                 │
│ class/type creation            │    5.83 │                    1.8% │ <built-in method builtins.__build_class__> (~:0)                                          │
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
```

### Why are other languages faster at importing?

They do all this work upfront.

“Compilation” is an act of taking a bunch of human readable instructions and making them machine readable, including linking functions, generating bytecode/machine code, and doing all of this sort of import resolution dance that Python has to do right before you run the program, but at “compilation time”.

One of the biggest tradeoffs with interpreted vs. compiled languages: if you want interpreted, you pay the cost at runtime (or “just before running”) that other languages pay at compile-time.

Even with cached `.pyc` files, Python can’t get away from reading over the tree of files of that represents a module, processing all the `__init__.py` files and associated imports from them, and doing work that compiled languages do upfront (in addition to some sneaky arbitrary stuff because yay, code execution during imports).

### What we can do about it

1. Warm stuff up (i.e., execute imports/build `pyc`files ahead of time)
2. Accept that importing is slow, even when warm, because the tradeoff is you ship content that is human readable instead of binaries (unless you are a [Python library that wraps a binary](https://github.com/pytorch/pytorch), of which there are many)
3. Guard against libraries with slow imports until we absolutely need them (`if TYPE_CHECKING` , restructuring modules to be lazily imported)
4. Use a different language than Python (lol), which is kinda what the second part of (2) is. Pytorch as the example wraps C/CUDA libraries, which themselves do not pay the import penalties Python does

Lazy imports you’ll have seen a bit, and they’re the cheapest way to get some gains on import time, like instead of

```cpp
import pandas


def my_func():
  df = pandas.DataFrame()
```

You can do

```java
def my_func():
  import pandas
  df = pandas.DataFrame()
```

You’ll pay the cost ONLY if that function is called, and not if you simply import the file/module containing this code.

Thanks for reading!
