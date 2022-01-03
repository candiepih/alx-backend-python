#!/usr/bin/env python3
""""""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized
# parameterized_class
# from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for `client.py`."""

    @parameterized.expand([
        ('google', {
            'login': 'google',
            'id': 1,
            'node_id': 'MDEyOk9yZ2FuaXphdGlvbjE=',
            'url': 'https://api.github.com/orgs/google',
            'repos_url': 'https://api.github.com/orgs/google/repos',
            'events_url': 'https://api.github.com/orgs/google/events',
            'hooks_url': 'https://api.github.com/orgs/google/hooks',
            'issues_url': 'https://api.github.com/orgs/google/issues',
            'members_url': 'https://api.github.com/orgs/google/members{/member}',
            'public_members_url': 'https://api.github.com/orgs/google/public_members{/member}',
            'avatar_url': 'https://avatars3.githubusercontent.com/u/1?v=4',
            'description': 'Google'
        }),
        ('abc', {
            'login': 'abc',
            'id': 2,
            'node_id': 'MDEyOk9yZ2FuaXphdGlvbjI=',
            'url': 'https://api.github.com/orgs/abc',
            'repos_url': 'https://api.github.com/orgs/abc/repos',
            'events_url': 'https://api.github.com/orgs/abc/events',
            'hooks_url': 'https://api.github.com/orgs/abc/hooks',
            'issues_url': 'https://api.github.com/orgs/abc/issues',
            'members_url': 'https://api.github.com/orgs/abc/members{/member}',
            'public_members_url': 'https://api.github.com/orgs/abc/public_members{/member}',
            'avatar_url': 'https://avatars3.githubusercontent.com/u/2?v=4',
            'description': 'ABC'
        })
    ])
    @patch("requests.get")
    def test_org(self, org, expected, mock_get_request):
        """Test `get_json`."""
        mock_get_request.return_value.json.return_value = expected
        client = GithubOrgClient(org)
        self.assertEqual(client.org, expected)
        mock_get_request.assert_called_once()

    @patch("client.GithubOrgClient.org")
    def test_public_repos_url(self, mock_org):
        """Test `public_repos_url`."""
        mock_org.return_value = {
            'public_repos_url': 'https://api.github.com/orgs/google/repos'
        }
        # client = GithubOrgClient('google')
        mock = PropertyMock(return_value='https://api.github.com'
                                         '/orgs/google/repos')
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=mock) as mock_public_repos_url:
            self.assertEqual(mock_public_repos_url,
                             mock_org.return_value['public_repos_url'])

    @patch("utils.get_json")
    def test_public_repos(self, mock_get_json):
        """Test `public_repos`."""
        mock_get_json.return_value.json.return_value = [
            'truth', 'ruby-openid-apps-discovery',
            'autoparse', 'anvil-build',
            'googletv-android-samples', 'ChannelPlate'
        ]

        with patch.object(GithubOrgClient, 'public_repos',
                          new_callable=PropertyMock) as mock_public_repos:
            mock_public_repos.return_value = \
                mock_get_json.return_value.json.return_value
            self.assertEqual(mock_public_repos.return_value,
                             mock_get_json.return_value.json.return_value)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, current_license: str, expected: bool):
        """Test `has_license`."""
        client = GithubOrgClient('google')
        self.assertEqual(client.has_license(repo, current_license), expected)

# @parameterized_class(
#     ("repo", "current_license", "expected"),
# )
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     @patch("requests.get")
#     def setUpClass(self, mock_get_request) -> None:
#         """Set up the class."""
#         pass
#
#     def tearDown(self) -> None:
#         """Tear down the test."""
#         pass
