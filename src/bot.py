"""bot.py A simple bot that sends messages to Semaphor."""

from flowbot import FlowBot
from template_env import template


class WebhookBot(FlowBot):
    """WebhookBot responds to GitHub webhooks in Semaphor."""

    def handle_webhook_summary(self, summary):
        """Message Semaphor channels with a summary of the webhook."""
        msg = template.get_template('webhook_summary.txt').render(summary=summary)  # NOQA
        self.message_all_channels(msg)
