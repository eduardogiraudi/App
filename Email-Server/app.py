import mailtrap as mt
import json
import redis
from dotenv import load_dotenv
import os
import requests








load_dotenv('./Email.env')


redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, password=os.getenv('REDIS_PASSWORD'))


def send_email(sender,to, subject, text, html):
    requests.post(
		"https://api.mailgun.net/v3/sandbox9774dbdb078a4d7a8e11757be4e5dda9.mailgun.org/messages",
		auth=("api", os.getenv('MAILGUN_API_KEY')),
		data={"from": f"<{sender}>",
			"to": f"<{to}>",
			"subject": f"{subject}",
            "html":html,
			"text": text
            })
    print(sender, to, subject, text)


def listen_queue():
    while True:
        email = redis_client.brpop('email')[1]
        if email:
            email = json.loads(email)
            send_email(email['sender'],email['to'],email['subject'],email['text'], email['html'])


if __name__ == '__main__':
    listen_queue()
