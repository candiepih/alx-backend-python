# Unittests and Integration Tests

This topics aim was to understand the following concepts:

* The difference between `unit` and `integration tests`. 
* Common testing patterns such as `mocking`, `parametrizations` and `fixtures`
* `Unittest` — Unit testing framework 
* `unittest.mock` — mock object library 
* How to mock a `readonly property with mock`? 
* `Parameterized` testing with any Python test framework
* `Memoization`

# Files

The following files were used to test understanding on the various concepts.

[test_utils.py](./test_utils.py)

### Task 0 ([test_client.py](./test_client.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

First unit test for `utils.access_nested_map`.

Requirements:

* Create a `TestAccessNestedMap` class that inherits from `unittest.TestCase`.
* Implement the `TestAccessNestedMap.test_access_nested_map` method to test that the method returns what it is supposed to. 
* Decorate the method with `@parameterized.expand` to test the function for following inputs:

```python
nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")
```

* For each of these inputs, test with assertEqual that the function returns the expected result.

### Task 1 ([test_client.py](./test_client.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

Implement `TestAccessNestedMap.test_access_nested_map_exception`. Use the `assertRaises` context manager to test that a `KeyError` is raised for the following inputs (use `@parameterized.expand`):

```python
nested_map={}, path=("a",)
nested_map={"a": 1}, path=("a", "b")
```
Also make sure that the exception message is as expected.

### Task 2 ([test_client.py](./test_client.py))

Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

Define the `TestGetJson(unittest.TestCase)` class and implement the `TestGetJson.test_get_json` method to test that `utils.get_json` returns the expected result.

We don’t want to make any actual external HTTP calls. Use `unittest.mock.patch` to patch `requests.get`. Make sure it returns a `Mock object` with a `json method` that returns `test_payload` which you parametrize alongside the `test_url` that you will pass to `get_json` with the following inputs:

```python
test_url="http://example.com", test_payload={"payload": True}
test_url="http://holberton.io", test_payload={"payload": False}
```
* Test that the mocked `get` method was called exactly once (per input) with test_url as argument. 
* Test that the output of `get_json` is equal to `test_payload`.

### Task 3 ([test_client.py](./test_client.py))

Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

Implement the `TestMemoize(unittest.TestCase)` class with a `test_memoize` method.

Inside `test_memoize`, define following class

```python
class TestClass:

    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()
```

### Task 4 ([test_utils.py](./test_utils.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

In a new `test_client.py` file, declare the `TestGithubOrgClient(unittest.TestCase)` class and implement the `test_org` method.

This method should test that `GithubOrgClient.org` returns the correct value.

Use `@patch` as a decorator to make sure `get_json` is called once with the expected argument but make sure it is not executed.

Use `@parameterized.expand` as a decorator to parametrize the test with a couple of `org` examples to pass to `GithubOrgClient`, in this order:

* google 
* abc

**Of course, no external HTTP calls should be made.**

### Task 5 ([test_utils.py](./test_utils.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

Implements the `test_public_repos_url` method to `unit-test GithubOrgClient._public_repos_url`.

Test that the result of `_public_repos_url` is the expected one based on the mocked payload.

### Task 5 ([test_utils.py](./test_utils.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

### Task 6 ([test_utils.py](./test_utils.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

Implement `TestGithubOrgClient.test_public_repos` to unit-test `GithubOrgClient.public_repos`.

Use `@patch` as a decorator to mock `get_json` and make it `return` a payload of your choice.

Use `patch as a context manager` to mock `GithubOrgClient._public_repos_url` and return a value of your choice.

* Test that the list of repos is what you expect from the chosen payload. 
* Test that the mocked property and the mocked `get_json` was called once.

### Task 7 ([test_utils.py](./test_utils.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

Implement `TestGithubOrgClient.test_has_license` to unit-test `GithubOrgClient.has_license`.

Parametrize the test with the following inputs:

```python
repo={"license": {"key": "my_license"}}, license_key="my_license"
repo={"license": {"key": "other_license"}}, license_key="my_license"
```

### Task 7 ([test_utils.py](./test_utils.py))
Using files [client.py](./client.py), [utils.py](./utils.py) and [fixtures.py](./fixtures.py)

Test the `GithubOrgClient.public_repos` method in an integration test. That means that we will only mock code that sends external requests.

Create the `TestIntegrationGithubOrgClient(unittest.TestCase)` class and implement the `setUpClass` and `tearDownClass` which are part of the `unittest.TestCase` API.

Use `@parameterized_class` to decorate the class and parameterize it with fixtures found in `fixtures.py`. The file contains the following fixtures:

```python
org_payload, repos_payload, expected_repos, apache2_repos
```

The `setupClass` should mock `requests.get` to return example payloads found in the fixtures.

Use `patch` to start a patcher named `get_patcher`, and use `side_effect` to make sure the mock of `requests.get(url).json()` returns the correct fixtures for the various values of url that you anticipate to receive.