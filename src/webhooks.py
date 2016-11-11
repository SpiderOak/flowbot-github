"""webhook.py - Parse various webhooks from GitHub."""
from collections import namedtuple
from message import WebhookMessage


# WebhookSummary provides a simplified version of any webhook that is ready
# to be consumed by the FlowBot.
WebhookSummary = namedtuple('WebhookSummary', ['msg', 'users', 'repo', 'url'])


class GithubWebhookConsumer(object):
    """Consume github webhooks and return parsed data."""

    def __init__(self, flowbot):
        """Initlize the consumer and attach a running flowbot."""
        self.flowbot = flowbot

    def process(self, payload, webhook_name):
        """Send a message to the flowbot based on the webhook payload."""
        paths = self.get_paths(webhook_name)
        message = WebhookMessage(webhook_name, payload, **paths)
        self.flowbot.handle_webhook_message(message)
        return '', 200

    @classmethod
    def get_paths(cls, webhook_name):
        """Return the paths to message information within the payload.

        There are also some default settings that are injected if the specified
        path processor doesn't already provide them.
        """
        path_processor = getattr(cls, webhook_name)
        paths = path_processor() if path_processor else {}
        defaults = {
            'repo': ['repository'],
            'action': ['action'],
            'title': [],
            'users': [],
            'url': []
        }
        for key, default_value in defaults.items():
            if key not in paths:
                paths[key] = default_value
        return paths

    @staticmethod
    def issues():
        """Return the payload paths for issues."""
        return {
            "title": ['issue', 'title'],
            "url": ['issue', 'html_url'],
            "users": [
                ['issue', 'user'],
                ['repository', 'owner'],
                ['assignee'],
                ['sender']
            ]
        }

    @staticmethod
    def pull_request():
        """Return the payload paths for pull_requests."""
        return {
            "title": ['pull_request', 'title'],
            "url": ['pull_request', 'html_url'],
            "users": [
                ['pull_request', 'user'],
                ['pull_request', 'head', 'user'],
                ['pull_request', 'head', 'repo', 'user'],
                ['pull_request', 'base', 'user'],
                ['pull_request', 'base', 'repo', 'user'],
                ['repository', 'owner'],
                ['sender']
            ]
        }
