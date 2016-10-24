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
            "/notme": self.unlink_me,
            "/help": self.help
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
                highlight.extend(self._get_account_ids(username))
        return

    @mentioned
    def help(self, flow_message):
        """Show all the command options."""
        self.render_response(flow_message, 'help.txt', {})

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

    def render_response(self, orig_message, template_name, context={}, highlight=None):  # NOQA
        """Render the context to the message template and respond."""
        response = ENV.get_template(template_name)
        self.reply(orig_message, response.render(**context), highlight)

    def _get_account_ids(self, github_username):
        """Get the record of all account ids linked w/ this username."""
        db_key = 'links_%s' % (github_username, )
        account_ids = self.channel_db.get_last(db_key)
        return account_ids if account_ids else []

    def _link_account_to_username(self, account_id, github_username):
        """Link the semaphor account_id with the github username."""
        db_key = 'links_%s' % (github_username, )
        account_ids = self._get_account_ids(github_username)
        if account_id not in account_ids:
            account_ids.append(account_id)
            self.channel_db.new(db_key, account_ids)

    def _unlink_account(self, account_id, github_username):
        """Unlink the account_id and github_username."""
        db_key = 'links_%s' % (github_username, )
        account_ids = self._get_account_ids(github_username)
        if account_id in account_ids:
            account_ids.remove(account_id)
            self.channel_db.new(db_key, account_ids)
