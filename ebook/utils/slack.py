from slacker import Slacker
from config import settings

def slack_notify(text=None, channel='#general', username='jiho', attachments=None):
	token = settings.SLACK_TOKEN
	slack = Slacker(token)
	slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments)