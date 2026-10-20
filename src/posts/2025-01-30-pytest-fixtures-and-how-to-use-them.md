---
title: "Pytest Fixtures and How to Use Them"
date: 2025-01-30
medium_url: "https://medium.com/@mckornfield/pytest-fixtures-and-how-to-use-them-9b981eb0d687"
---

They can be tricky, but useful

![Photo by Ýlona María Rybka on Unsplash](/img/pytest-fixtures-and-how-to-use-them/0_waMD5RcIXDcpdUei.jpg)

*Photo by [Ýlona María Rybka](https://unsplash.com/@yloryb?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Fixtures? Like lightbulbs?

A `fixture` in `pytest` is [well explained in their docs](https://docs.pytest.org/en/6.2.x/fixture.html), but it’s basically a reusable “setup” portion of a test. I always thought of tests in the “GWT” style:

- Given (I have a bad payload to send)
- When (I send the payload to the service)
- Then (I get a 400 error)

I’ve also seen GWT as AAA (Arrange, Act, Assert), but it’s basically all the same. The “given” part of the test though can be extremely copy pasta heavy, especially if it involves mocking something or starting a test database.

That’s where the fixtures come in. They give you something reusable that you can simply call. There are really only a couple reasons to use a pytest fixture:

1. To reduce copy paste in tests
2. To save on expensive setup (usually relying on `scopes` )

Let’s jump into a couple examples

### 1. Reducing copy paste in tests

For reference, this code will refer to my [patching unit testing article](/posts/a-short-guide-to-mocking-in-python-unit-testing/)

Let’s say we have two copy pasta style tests like the following:

```python
def test_make_http_request_returns_response():
  with patch("requests.get") as mock_requests:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "val"}
    mock_requests.return_value = mock_response
    response = make_http_request("https://example.com")
    assert response.status_code == 200
    assert response.json() == {"key": "val"}


def test_prepend_http_request(patch_good_resp):
  with patch("requests.get") as mock_requests:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "val"}
    mock_requests.return_value = mock_response
    response = make_http_request_prepend_https("https://example.com")
    assert response.status_code == 200
    assert response.json() == {"key": "val"}
```

Granted, we could use the `@patch` annotation to reduce the nesting, but for this example, it’s easier if we’re mocking requests inline.

To lift the “given” portion out into a fixture, we can simply make a method annotated with `@pytest.fixture`

```csharp
@pytest.fixture
def patch_good_resp() -> Generator[MagicMock, Any, Any]:
  with patch("requests.get") as mock_requests:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "val"}
    mock_requests.return_value = mock_response
    yield mock_requests
```

Now if we run this test with `python -m pytest` , and we request this fixture by name in our tests, like so:

```python
# Notice we inject our fixture in as an argument
def test_make_http_request_returns_response(patch_good_resp):
  response = make_http_request("https://example.com")
  assert response.status_code == 200
  assert response.json() == {"key": "val"}


def test_prepend_http_request(patch_good_resp):
  response = make_http_request_prepend_https("https://example.com")
  assert response.status_code == 200
  assert response.json() == {"key": "val"}
```

We can use the mocked behavior (even assert on the mock) without the copy paste of the test setup.

### 2. Reducing Redundant Setup Time

One extra feature of `fixtures` is that they can be setup per *test*, which is useful for asserting mocks, or at different levels, i.e., scopes:

```javascript
The scope for which this fixture is shared; one of ``"function"``
(default), ``"class"``, ``"module"``, ``"package"`` or ``"session"``.
```

If we use one of the other options, we’ll notice that our fixture isn’t called nearly as many times. This can be useful in the case where a setup has to do something like stand up an in memory database, but we don’t need to remove it until all the test *cases* are done.

We can simulate something like this with a small tweak to our setup from before:

```csharp
@pytest.fixture
def patch_good_resp() -> Generator[MagicMock, Any, Any]:
  with patch("requests.get") as mock_requests:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "val"}
    mock_requests.return_value = mock_response
    time.sleep(2) # New!
    yield mock_requests
```

If we rerun our tests, we’ll get a very predictable ~4 seconds (2 seconds for each function level setup).

Conversely, if we set the scope to be “module”.

```csharp
@pytest.fixture(scope="module") # New!
def patch_good_resp() -> Generator[MagicMock, Any, Any]:
  with patch("requests.get") as mock_requests:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"key": "val"}
    mock_requests.return_value = mock_response
    time.sleep(2)
    yield mock_requests
```

Then our test run time will come out to be only 2 seconds, since we only eat the startup cost *once* per module initialization.

Short and sweet, hopefully that helps!

Thanks for reading.
