from unittest import TestCase
from ..webhooks import GithubWebhookConsumer
from mock import patch


class TestWebhookConsumer(TestCase):
    """Test the webhook consumers using a fake bot and canned webhooks."""

    def test_default_paths(self):
        """Assert that the defaults are injected."""
        paths = GithubWebhookConsumer.get_paths('issues')
        self.assertEqual(paths['repo'], ['repository'])
        self.assertEqual(paths['action'], ['action'])

    def test_default_dont_override(self):
        """If the paths object already contains a setting, don't override."""
        with patch.object(GithubWebhookConsumer, 'issues') as issues_paths:
            issues_paths.return_value = {'action': ['hello', 'foo']}
            paths = GithubWebhookConsumer.get_paths('issues')
        self.assertEqual(paths['action'], ['hello', 'foo'])
