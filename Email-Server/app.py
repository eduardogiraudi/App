import mailtrap as mt
import json
import redis
from dotenv import load_dotenv
import os
load_dotenv('./Email.env')


redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)


def send_email(sender,to, subject, text):
    # mail = mt.Mail(
    #     sender=mt.Address(email=sender, name=sender),
    #     to=[mt.Address(email=to, name=to)],
    #     subject=subject,
    #     # text="Congrats for sending test email with Mailtrap!",
    #     html=f"""
    #     <!doctype html>
    #     <html>
    #     <head>
    #         <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    #     </head>
    #     <body style="font-family: sans-serif;">
    #         <div style="display: block; margin: auto; max-width: 600px;" class="main">
    #         <h1 style="font-size: 18px; font-weight: bold; margin-top: 20px">
    #             {subject}
    #         </h1>
    #         <p>{text}</p>
    #         </div>
    #     </body>
    #     </html>
    #     """,
    #     category="Test",
    #     headers={"X-MT-Header": "Custom header"},
    #     custom_variables={"year": 2023},
    # )

    # client = mt.MailtrapClient(token="38c193b4429fb516078866a08128e24d")
    # client.send(mail)
    print(sender, to, subject, text)





def listen_queue():
    while True:
        email = redis_client.brpop('email')[1]
        if email:
            email = json.loads(email)
            send_email(email['sender'],email['to'],email['subject'],email['text'])





    

if __name__ == '__main__':
    listen_queue()