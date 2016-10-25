import os
import json


from unittest import TestCase
from ..message import WebhookMessage
from ..webhooks import GithubWebhookConsumer


class TestMessage(TestCase):
    """Test the Message model against some canned webhooks."""

    def load_sample_webhook(self, webhook_name):
        """Loak a webhook response from a sample file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = "{0}.json".format(webhook_name)
        json_file_path = os.path.join(
            current_dir, 'sample_webhooks', json_file)

        with open(json_file_path, 'rb') as file:
            payload = json.load(file)
        return payload

    def test_issue_message(self):
        """Make sure Message loads the canned issue response."""
        paths = GithubWebhookConsumer.get_paths('issues')
        payload = self.load_sample_webhook('issues')
        message = WebhookMessage('issues', payload, **paths)
        self.assertEqual(message.title, 'Spelling error in the README file')
        self.assertEqual(message.action, 'opened')
        self.assertEqual(message.repo_name, 'baxterthehacker/public-repo')
        self.assertEqual(message.url, 'https://github.com/baxterthehacker/public-repo/issues/2')  # NOQA

    def test_pull_request_message(self):
        """Make sure Message loads the canned pull-request response."""
        paths = GithubWebhookConsumer.get_paths('pull_request')
        payload = self.load_sample_webhook('pull_request')
        message = WebhookMessage('pull_request', payload, **paths)
        self.assertEqual(message.title, 'Update the README with new information')  # NOQA
        self.assertEqual(message.repo_name, 'baxterthehacker/public-repo')
        self.assertEqual(message.action, 'opened')
        self.assertEqual(message.url, 'https://github.com/baxterthehacker/public-repo/pull/1')  # NOQA

    def test_ignore_certain_actions(self):
        """Certain actions should be ignored."""
        ignored_actions = {
            'pull_request': ("unassigned", "labeled", "unlabeled"),
            'issues': ("unassigned", "labeled", "unlabeled")
        }
        for message_type, actions in ignored_actions.iteritems():
            for action in actions:
                self.assertTrue(WebhookMessage.ignore(message_type, action))

        # Other actions should not be ignored.
        self.assertFalse(WebhookMessage.ignore('pull_request', 'opened'))
