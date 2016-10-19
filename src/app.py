"""app.py - Forwards webhook events as messages to bot.py."""

from flask import Flask
from bot import WebBot
from github_webhook import Webhook


app = Flask(__name__)
webhook = Webhook(app)
bot = WebBot()


@app.route('/', methods=['GET'])
def home():
    """The home page."""
    bot.alert('/', 'Someone just visited the homepage.')
    return 'Hello!'


@webhook.hook()
def on_push(data):
    """Handle GitHub Webhooks."""
    print(data)
    bot.message_all_channels('New event on github!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
