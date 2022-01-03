#!/usr/bin/env python3
"""
Module contains tests for the client module.
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD


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

    @patch("client.get_json", return_value=[
        {'name': 'autoparse'},
        {'name': 'ChannelPlate'},
        {'name': 'truth'}
    ])
    def test_public_repos(self, mock_get_json):
        """Test `public_repos`."""
        url = 'https://api.github.com/orgs/google/repos'
        client = GithubOrgClient('google')
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock,
                          return_value=url) as mock_public_repos:
            repos = list(map(lambda x: x['name'],
                             mock_get_json.return_value))
            self.assertEqual(client.public_repos(), repos)
            mock_public_repos.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, current_license, expected):
        """Test `has_license`."""
        client = GithubOrgClient('google')
        client_return = client.has_license(repo, current_license)
        self.assertEqual(client_return, expected)


@parameterized_class(
    [
        {'org_payload': TEST_PAYLOAD[0][0]},
        {'repo_payload': TEST_PAYLOAD[0][1]},
        {'expected_repos': TEST_PAYLOAD[0][2]},
        {'apache2_repos': TEST_PAYLOAD[0][3]}
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test: fixtures"""
    @patch("requests.get")
    def setUpClass(self, mock_get_request) -> None:
        """Set up the class."""
        mock_get_request.return_value = [
            self.org_payload, self.repo_payload,
            self.expected_repos, self.apache2_repos
        ]
        self.get_patcher = mock_get_request
        self.get_patcher.side_effect = self.get_side_effect
        self.mock_get = self.get_patcher.start()

    def side_effect(self):
        """Return the side effect."""
        return self.mock_get()

    def tearDown(self) -> None:
        """Tear down the test."""
        self.get_patcher.stop()
