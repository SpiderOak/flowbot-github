"""bot.py A simple bot that sends messages to Semaphor."""
import re
from flowbot import FlowBot
from flowbot.decorators import mentioned
from message import ENV


class WebhookBot(FlowBot):
    """WebhookBot responds to GitHub webhooks in Semaphor."""

    def commands(self):
        return {
            "/me": self.link_me,
            "/notme": self.unlink_me
        }

    def handle_webhook_message(self, webhook_message):
        """Message Semaphor channels with a summary of the webhook."""
        msg = webhook_message.render()
        highlight = self._get_highlights(webhook_message)

        if msg:
            self.message_all_channels(msg, highlight=highlight)

    def _get_highlights(self, webhook_message):
        """Get all the account_ids that should be highlighted."""
        highlight = []
        if webhook_message.usernames:
            for username in webhook_message.usernames:
                highlight.extend(self._get_links(username))
        return

    @mentioned
    def link_me(self, flow_message):
        """Link the current Semaphor user to the github username given."""
        match = re.search('/me (\w+)', flow_message.get('text', ''))
        if match:
            github_username = match.group(1)
            sender_id = flow_message['senderAccountId']
            self._link_account_to_username(sender_id, github_username)
            self.render_response(
                orig_message=flow_message,
                template_name='link_me.txt',
                context={"github_username": github_username},
                highlight=[sender_id]
            )

    @mentioned
    def unlink_me(self, flow_message):
        """Link the current Semaphor user to the github username given."""
        match = re.search('/notme (\w+)', flow_message.get('text', ''))
        if match:
            github_username = match.group(1)
            sender_id = flow_message['senderAccountId']
            self._unlink_account(sender_id, github_username)
            self.render_response(
                orig_message=flow_message,
                template_name='unlink_me.txt',
                context={"github_username": github_username},
                highlight=[sender_id]
            )

    def render_response(self, orig_message, template_name, context, highlight):
        """Render the context to the message template and respond."""
        response = ENV.get_template(template_name)
        self.reply(orig_message, response.render(**context), highlight)

    def _get_links(self, github_username):
        """Get the record of all accounts linked w/ this username."""
        db_key = 'links_%s' % (github_username, )
        links = self.channel_db.get_last(db_key)
        return links if links else []

    def _link_account_to_username(self, account_id, github_username):
        """Link the semaphor account_id with the github username."""
        db_key = 'links_%s' % (github_username, )
        existing_links = self._get_links(github_username)
        if account_id not in existing_links:
            existing_links.append(account_id)
            self.channel_db.new(db_key, existing_links)

    def _unlink_account(self, account_id, github_username):
        """Unlink the account_id and github_username."""
        db_key = 'links_%s' % (github_username, )
        existing_links = self._get_links(github_username)
        if account_id in existing_links:
            existing_links.remove(account_id)
            self.channel_db.new(db_key, existing_links)
