"""bot.py A simple bot that sends messages to Semaphor."""

from flowbot import FlowBot


class WebhookBot(FlowBot):
    """WebhookBot responds to GitHub webhooks in Semaphor."""

    def handle_webhook_message(self, message):
        """Message Semaphor channels with a summary of the webhook."""
        msg = message.render()
        if msg:
            self.message_all_channels(msg)
