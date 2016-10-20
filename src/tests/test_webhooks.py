from unittest import TestCase
from ..webhooks import GithubWebhookConsumer
import json
import os


class FakeFlowbot(object):
    def handle_webhook_message(self, msg):
        pass


class TestWebhookConsumer(TestCase):
    """Test the webhook consumers using a fake bot and canned webhooks."""

    def load_sample_webhook(self, webhook_name):
        """Loak a webhook response from a sample file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = "{0}.json".format(webhook_name)
        json_file_path = os.path.join(
            current_dir, 'sample_webhooks', json_file)

        with open(json_file_path, 'rb') as file:
            payload = json.load(file)
        return payload

    def test_issues_webhook(self):
        """Process the fake issues webhook."""
        payload = self.load_sample_webhook('issues')
        msg = GithubWebhookConsumer(FakeFlowbot()).issues(payload)
        self.assertEqual(msg.repo, 'baxterthehacker/public-repo')
        self.assertEqual(msg.msg, 'Issue opened')
        self.assertEqual(msg.url, 'https://api.github.com/repos/baxterthehacker/public-repo/issues/2')  # NOQA

    def test_pull_request_webhook(self):
        """Process the fake pull request webhook."""
        payload = self.load_sample_webhook('pull_request')
        msg = GithubWebhookConsumer(FakeFlowbot()).pull_request(payload)
        self.assertEqual(msg.repo, 'baxterthehacker/public-repo')
        self.assertEqual(msg.msg, 'Pull Request opened')
        self.assertEqual(msg.url, 'https://api.github.com/repos/baxterthehacker/public-repo/pulls/1')  # NOQA
