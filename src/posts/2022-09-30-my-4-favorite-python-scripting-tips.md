---
title: "My 4 Favorite Python Scripting Tips"
subtitle: "These are some Python tips I use to work with my personal scripts that help me be more productive/ automate things."
date: 2022-09-30
medium_url: "https://medium.com/@mckornfield/4-python-productivity-tips-bac195170487"
---

![Photo by Timothy Dykes on Unsplash](/img/my-4-favorite-python-scripting-tips/0_t0qI_bXYh_hMOJwz.jpg)

*Photo by [Timothy Dykes](https://unsplash.com/@timothycdykes?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

These are some Python tips I use to work with my personal scripts that help me be more productive/ automate things.

tl;dr

- Run snippets using `python` and use the REPL or `python -c "print('hello world')"`
- Store usernames/passwords in `~/.netrc` and use them automatically with `requests`
- Use `Pool` or `ThreadPool` to speed up CPU bound or IO bound loops
- Use `subprocess` and `shlex` to run terminal commands in Python, e.g. `subprocess.check_output(shlex.split("env"))`

## 1. Run Python snippets

If I want to test things out, instead of using a python program and running a script over and over, I usually run `python` in the shell and work with the Python REPL. The Python REPL is powerful but some things, like loops, can be a bit hard to work with (which is why I tend to use [list comprehensions](https://www.w3schools.com/python/python_lists_comprehension.asp) instead).

You can also [import a Python file](https://stackoverflow.com/a/36496608/10061484) to test things out using `exec(open('file.py').read())` , in case you want to manipulate classes or something not available in the standard library.

Another simple way to run a snippet is like so:

```
python -c "print('hello world')" # beware the quotes!
```

## 2. Use a ~/.netrc file

(Special thanks to [dalbertom](https://medium.com/@dalbertom) for showing me this originally)

The `~/.netrc` file is a great way to store usernames/api keys for systems that you can interact with using Basic Authentication. It’s also a good way to separate authentication from your application code. It can be used with curl if you simply run `curl -n` , but Python’s `requests` will check your `~/.netrc` file by default.

An example on how you would use this using Python’s `requests` library would look like so.

```
echo "machine httpbin.org login myusername password mypassword">> ~/.netrc
```

Once you have that entry added to your `~/.netrc` then requests will look up usernames and passwords, for example

```
python -c "import requests; print(requests.get('http://httpbin.org/basic-auth/myusername/mypassword'))"
```

## 3. Speed things up with a Pool

Pools are a nice way to speed up operations that might not work well in a single-threaded fashion (i.e. something in pure Python that is a bit computationally intense).

They’re super easy to use and part of the standard library, so consider dropping `from multiprocessing import Pool` into your code and starting to do some things in parallel!

Here’s an example where you make a request to different URLs in parallel (not the best use of multiprocessing, but we can talk about `async` another time).

```
from multiprocessing import Pool
```

```
import requests
```

```
urls = [f"https://httpbin.org/status/{code}" for code in range(200, 501, 100)]
```

```
def extract_code(url: str) -> int:
    return requests.get(url).status_code
```

```
def get_parallel():
    with Pool() as p:
        status_codes = p.map(extract_code, urls)
```

Even in this example with 4 URLs, you save about 2-3 seconds just parallelizing the get calls. Calling `Pool()`will infer the number of processes to spin up, but you can explicitly call it with a number.

If the act of creating the subprocesses is significant, then consider using `ThreadPool` instead, i.e.

```
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
```

```
import requests
```

```
urls = [f"https://httpbin.org/status/{code}" for code in range(200, 501, 100)]
```

```
def extract_code(url: str) -> int:
    return requests.get(url).status_code
```

```
def get_parallel_threadpool():
    with ThreadPool() as p:
        status_codes = p.map(extract_code, urls)
```

For the above example, ThreadPool took around 2 seconds, Pool 5 seconds, and running it serially was 8 seconds.

## 4. Run shell commands

Why would you do this in Python and not just BASH? Well consider the fact that you can’t do basic things in BASH like [add two decimals](https://stackoverflow.com/a/38751228/10061484) without using `bc` … and you might reconsider using Python to run some shell commands.

There’s many ways to do it but the main modules to use are `shlex` and `subprocess` . I use this snippet all the time in my code

```
def run_command(cmd_str: str, cwd: str) -> str:
    cmd = shlex.split(cmd_str)
    result = subprocess.check_output(
        cmd, cwd=cwd).decode('utf-8').strip()
    return result
```

This runs a command, throws an error if the exit code is non-zero, and returns the output as a String.

It’s great if you want to use some binary/BASH functions and then pass around the input in Python.

That’s all I’ve got… Let me know if you have any cool Python tips!
