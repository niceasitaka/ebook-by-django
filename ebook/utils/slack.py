from slacker import Slacker

def slack_notify(text=None, channel='#test', username='알림봇', attachments=None):
	token = 'xoxb-429824523894-427908557777-Rqm6aejrF3ZkLJyFsNlwbhc1'
	slack = Slacker(token)
	slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments)