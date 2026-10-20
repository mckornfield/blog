---
title: "A Short Guide to Mocking in Python Unit Testing"
subtitle: "Patching and mocking and asserting, oh my"
date: 2025-01-16
medium_url: "https://medium.com/@mckornfield/a-short-guide-to-mocking-in-python-unit-testing-a07875c2a773"
---

Patching and mocking and asserting, oh my

![Photo by Timothy Dykes on Unsplash](/img/a-short-guide-to-mocking-in-python-unit-testing/0_NxZd1hm1EYBJhoga.jpg)

*Photo by [Timothy Dykes](https://unsplash.com/@timothycdykes?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

There are a handful of ways to mock things in Python for unit testing, and I thought I’d give a set of ways to mock things, as well as explanations.

### Some Given Code

Let’s say I want to test the following contrived code, in a file called

`matts_module/request_samples.py`

The code relies on the `requests` library, but we don’t actually want to call out to that, so we’ll learn how we can mock all these request calls.

```python
import requests
from requests import Session
from typing import Tuple


def make_http_request(url: str) -> requests.Response:
  resp = requests.get(url)
  resp.raise_for_status()
  return resp


def make_session_based_request(url: str) -> requests.Response:
  with Session() as s:
    return s.get(url)


def make_http_request_prepend_https(url: str) -> requests.Response:
  return make_http_request("https://" + url)


def make_multiple_http_requests(
    url: str) -> Tuple[requests.Response, requests.Response]:
  resp = requests.get(url)
  resp.raise_for_status()
  resp2 = requests.post(url, json={"key": "val"})
  resp2.raise_for_status()
  return (resp, resp2)
```

### How Patching (basically) Works

When you `patch` a function/module/class in Python, you are replacing it with a [(Magic)Mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock) (MagicMocks let you mock special dunder functions like `__enter__` ). Since Python isn’t compiled, it’s easy for us to be sneaky and swap out the definitions of any function/class call with a patch.

You can define specific behavior for mocks, as we’ll see, and also assert on how they’re called by the test.

### 1. Patching Within a Test

This is the most basic, but you can essentially do `with("module.path") as mocked_fn` around a block of code to mock a module, a function or Class. Here’s an example:

```python
# These imports are going to apply for everything below.
# I'll remove them for brevity and only include the function name
import unittest
from unittest.mock import MagicMock, Mock, patch
from matts_module.request_samples import (make_http_request,
                                          make_http_request_prepend_https,
                                          make_session_based_request,
                                          make_multiple_http_requests)


class TestRequestMethods(unittest.TestCase):

  def test_make_request_mock(self):
    with patch(
        "matts_module.request_samples.make_http_request") as inner_fn_mock:
      resp = make_http_request_prepend_https(url="httpbin.org/status/500")

      inner_fn_mock.assert_called_once_with("https://httpbin.org/status/500")
      assert isinstance(resp, Mock)
      assert resp.ok

# I'll also leave this out for the remaining functions
if __name__ == "__main__":
  unittest.main()
```

This `with patch` construct is a bit messy inside the class method, but we’ll see how we can clean it up. The important thing to note is we can mock the function directly

Mock functions come with a nice set of utilities, including being able to assert they are called with certain values. Mocks also return mocks (which in many cases are all we need, like for booleans always returning `True`).

If this function actually ran, we’d get an error (that `httpbin.org` URL returns a 500, and the `raise_for_status` above throws an exception, if we don’t mock anything.) In your real tests, you might not get an error, but you might want to avoid a network call or relying on an external system for a unit test.

### 2. Patching With a Decorator

The next example we’ll go over is the more common patching outside of a test. You can do this with [a decorator](https://www.geeksforgeeks.org/decorators-in-python/).

```python
  @patch("matts_module.request_samples.make_http_request")
  def test_make_request_patch_annotation(self, mock_http_req: Mock):
    resp = make_http_request_prepend_https(url="httpbin.org/status/500")

    mock_http_req.assert_called_once_with("https://httpbin.org/status/500")
    assert isinstance(resp, Mock)
    assert resp.ok
```

You’ll notice it’s a bit cleaner in one sense (don’t have to indent the function), and instead of our mock being part of the `with` clause, the decorator injects the mock for us. Otherwise, it’s identical to the above.

So far we’ve been patching our own functions, but know we’ll move onto

### 3. Patching a Library Function

Very similar to mocking our own functions, we can mock a library function. It looks like

```less
  @patch("requests.get")
  def test_mock_library(self, requests_get_mock: Mock):
    resp = make_http_request("https://httpbin.org/status/500")

    requests_get_mock.assert_called_once_with("https://httpbin.org/status/500")
    assert resp.ok
```

Notice we can mock `requests.get` , and don’t have to worry about mocking the top level and dealing with nested mocks (which can be annoying). It functions very similarly to what we did before, but shows we can mock anything we define *or* import.

### 4. Multiple Patches

The only thing that’s really confusing about using multiple `@patch` statements is that the order is not intuitive. One engineer I worked with called it “reverse pancake order”, which is funny to me, but it is basically in stack order (i.e., the first patch defined is the last parameter in the function).

Here’s the example:

```less
  @patch("requests.get")
  @patch("requests.post")
  def test_mock_multiple(self, requests_post_mock: Mock,
                         requests_get_mock: Mock):
    # Note the order is closest is first for being injected
    get_resp, post_resp = make_multiple_http_requests(
        "https://httpbin.org/status/500")

    requests_get_mock.assert_called_once_with("https://httpbin.org/status/500")
    assert get_resp.ok
    requests_post_mock.assert_called_once_with(
        "https://httpbin.org/status/500", json={"key": "val"})
    assert post_resp.ok
```

Notice we defined the `requests.get` patch first, but it’s the *last* parameter.

It’s more the way that Python decorators work from what I understand, which is they are a set of function calls evaluated inside out, hence the stack looking behavior.

### 5. Patching a Class, and Patching a from … import … Construct

The next set of patching is a bit strange, so bear with me. We’re going to patch `Session` , which is a class, and is imported using `from requests import Session` , meaning our patching has to be a bit different.

```python
  @patch("matts_module.request_samples.Session")
  def test_session_mock_patch(self, mock_session_class: Mock):
    mock_session_instance = MagicMock()
    mock_session_http_instance = Mock()
    mock_session_instance.__enter__.return_value = mock_session_http_instance
    mock_session_class.return_value = mock_session_instance
    resp = make_session_based_request(url="https://httpbin.org/status/500")

    mock_session_class.assert_called_once()
    mock_session_http_instance.get.assert_called_once_with(
        "https://httpbin.org/status/500")
    assert isinstance(resp, Mock)
    assert resp.ok
```

First thing to note, because we imported Session using that `from` construct, we are actually patching an attribute inside *our module*.

I have been tripped up by this many, many times, so remember: from the patch’s perspective, when you do `from a import b` , in a file named `c.py` , the function looks like `c.b` not `a.b` .

There’s more than one way to patch a class (like using the `spec` keyword), but this is the one I’m most comfortable with, namely, creating a set of mocks that represent the instance call.

In our case, we need a `MagicMock` to mock the fact that our `Session` call is in a `with` , i.e., calls a `__enter__` function.

If we set the `.return_value` of that `mock_session_class` with a `MagicMock`, we can also set the `.return_value` of the `__enter__` call on *that* mock to be the `session` instance that we can perform assertions on, i.e., what gets set in the `with` statement.

### Recap

We showed how you can patch test functions, either within the function or as an annotation.

We showed how you can patch both internal code and library code, as well as how you can use multiple patches.

Lastly, we went over how you can patch classes, imported using the `from` syntax.

The code is available here as well:

<https://replit.com/@mckornfield/UnitTestExamples#main.py>

Thanks for reading!
