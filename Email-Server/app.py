import mailtrap as mt
import json
import redis
from dotenv import load_dotenv
import os
import requests
from settings import test, test_email_settings
from jinja2 import Environment, FileSystemLoader



## per pushare un email deve avere un sender, un to, un subject, un text e un context (contiene i dati del text suddivisi, quindi un text un title e un link per ora)


load_dotenv('.env')




redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, password=os.getenv('REDIS_PASSWORD'))






def send_email(sender,to, subject, text,template, data):

    template_loader = FileSystemLoader(searchpath='html/')
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template+'.html')
    data = data
    data['app'] = os.getenv('APP_NAME')
    template = template.render(data)



    request=requests.post(
		"https://api.mailgun.net/v3/sandbox9774dbdb078a4d7a8e11757be4e5dda9.mailgun.org/messages",
		auth=("api", os.getenv('MAILGUN_API_KEY')),
		data={"from": f"{sender}",
			"to": f"{to}",
			"subject": f"{subject}",
            "html":template,
			"text": text
            })
    print(sender, to, subject, text, template, data, request.status_code)






def listen_queue():
    while True:
        email = redis_client.blpop('email')[1]
        if email:
            if test:
                send_email(test_email_settings['sender'],test_email_settings['to'],test_email_settings['subject'],test_email_settings['text'],test_email_settings['template'],test_email_settings['data'],)
            else:
                email = json.loads(email)
                send_email(email['sender'],email['to'],email['subject'],email['text'],email['template'],email['data'])

if __name__ == '__main__':
    listen_queue()
