"""webhook.py - Parse various webhooks from GitHub."""
from collections import namedtuple
from . import util


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
        processor = getattr(self, webhook_name)
        summary = processor(payload)
        self.flowbot.handle_webhook_summary(summary)
        return '', 200

    def issues(self, payload):
        """Return an issue message."""
        userpaths = (
            ['issue', 'user'],
            ['repository', 'owner'],
            ['assignee'],
            ['sender']
        )

        return WebhookSummary(
            msg='Issue {0}'.format(payload.get('action')),
            url=payload['issue']['url'],
            users=util.get_usernames(payload, userpaths),
            repo=payload['repository']['full_name']
        )

    def pull_request(self, payload):
        """Return a pull request message."""
        userpaths = (
            ['pull_request', 'user'],
            ['pull_request', 'head', 'user'],
            ['pull_request', 'head', 'repo', 'user'],
            ['pull_request', 'base', 'user'],
            ['pull_request', 'base', 'repo', 'user'],
            ['repository', 'owner'],
            ['sender']
        )

        return WebhookSummary(
            msg='Pull Request {0}'.format(payload.get('action')),
            url=payload['pull_request']['url'],
            users=util.get_usernames(payload, userpaths),
            repo=payload['repository']['full_name']
        )
