#!/usr/bin/env python3
"""
Contains class TestUtils for testing the utils.py module.
"""
from parameterized import parameterized
from typing import Mapping, Sequence, Any
import unittest
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for testing the access_nested_map function.

    Attributes:
        None
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Mapping,
                               path: Sequence, expected: Any) -> None:
        """Testing the access_nested_map function."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence) -> None:
        """
        Testing the access_nested_map function for KeyError.

        Args:
            nested_map: The nested map to access.
            path: The path to access.

        Raises:
            KeyError: If the path is not found in the nested map.

        Returns:
            None
        """
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(error.exception.args[0], path[-1])


class TestGetJson(unittest.TestCase):
    """
    Test class for testing the get_json function.

    Attributes:
        None
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, url: str,
                      expected: Mapping, mock_get: Any) -> None:
        """
        Testing the get_json function.

        Args:
            url: The url to be used for testing.
            expected: The expected result.
            mock_get: The mock object for the requests.get function.

        Returns:
            None
        """
        mock_get.return_value.json.return_value = expected
        self.assertEqual(get_json(url), expected)
        mock_get.assert_called_once()


class TestMemoize(unittest.TestCase):
    """
    Test class for testing the memoize function.

    Attributes:
        None
    """

    def test_memoize(self) -> None:
        """
        Testing the memoize function.
        Returns:
            None
        """

        class TestClass:
            @staticmethod
            def a_method():
                """A method that returns a value."""
                return 42

            @memoize
            def a_property(self):
                """A property that returns a value."""
                return self.a_method()

        test_class = TestClass()
        with patch.object(test_class, "a_method") as mock_method:
            test_class.a_property()
            test_class.a_property()
            mock_method.assert_called_once()
