"""message.py - Format messages using Jinja2."""

import os
from jinja2 import Environment, FileSystemLoader
import util


ENV = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__))
)
ENV.filters['emoji'] = util.action_emoji


class WebhookMessage(object):
    """A WebhookMessage is a summary of a GitHub webhook event."""

    def __init__(self, message_type, payload, **kwargs):
        """Initialize a message."""
        _template_name = "{0}.txt".format(message_type)
        self.message_type = message_type
        self.template = ENV.get_template(_template_name)
        self.title = util.traverse_dict(payload, kwargs['title'])
        self.url = util.traverse_dict(payload, kwargs['url'])
        self.action = util.traverse_dict(payload, kwargs['action'])
        self.repo_name = util.get_repo_name(payload, kwargs['repo'])
        self.usernames = util.get_usernames(payload, kwargs['users'])

        if message_type == 'pull_request':
            self.action = self.get_pr_status(self.action, payload)

    def render(self):
        """Render the context of this message to the template."""
        if self.ignore(self.message_type, self.action):
            return None

        context = self.context()
        return self.template.render(**context)

    @staticmethod
    def ignore(message_type, action):
        """Ignore some webhook messages."""
        ignored_actions = {
            'pull_request': ("unassigned", "labeled", "unlabeled"),
            'issues': ("unassigned", "labeled", "unlabeled")
        }

        if message_type in ignored_actions:
            if action in ignored_actions[message_type]:
                return True
        return False

    def context(self):
        """Return a context dict to be used in rendering templates."""
        return {
            "repo_name": self.repo_name,
            "title": self.title,
            "url": self.url,
            "action": self.action
        }

    def get_pr_status(self, action, payload):
        """Determine of the PR is merged or not; update action accordingly."""
        merged = payload.get('merged', False)
        if action == 'closed' and merged:
            return 'merged'
        return action
