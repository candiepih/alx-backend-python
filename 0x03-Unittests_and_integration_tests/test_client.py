#!/usr/bin/env python3
""""""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized


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
            'members_url': 'https://api.github.com/orgs/google/members'
                           '{/member}',
            'public_members_url': 'https://api.github.com/orgs/google/'
                                  'public_members{/member}',
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
            'public_members_url': 'https://api.github.com/orgs/abc/'
                                  'public_members{/member}',
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

    def test_public_repos_url(self):
        """Test `public_repos_url`."""
        client = GithubOrgClient('google')
        url = 'https://api.github.com/orgs/google/repos'
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock,
                          return_value={
                              'repos_url': url
                          }) as mock_get:
            self.assertEqual(client._public_repos_url,
                             mock_get.return_value['repos_url'])
            mock_get.assert_called_once()

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
    def test_has_license(self, repo, current_license, expected):
        """Test `has_license`."""
        client = GithubOrgClient('google')
        client_return = client.has_license(repo, current_license)
        self.assertEqual(client_return, expected)
