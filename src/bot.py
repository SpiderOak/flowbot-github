"""bot.py A simple bot that sends messages to Semaphor."""

import json
from flowbot import FlowBot


class WebBot(FlowBot):
    """WebBot posts messages into Semaphor ostensibly from the web."""

    def __init__(self):
        """Initialize the bot with settings in settings.json."""
        with open('settings.json') as data_file:
            settings = json.load(data_file)
        super(WebBot, self).__init__(settings)

    def alert(self, endpoint, msg):
        """Alert all channels that a new endpoint has been accessed."""
        message = "New web event (%s): %s" % (endpoint, msg)
        self.message_all_channels(message)
