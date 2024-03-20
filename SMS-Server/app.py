import json
import redis
from dotenv import load_dotenv
import os
from settings import test, test_sms_settings
from twilio.rest import Client

load_dotenv('.env')
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, password=os.getenv('REDIS_PASSWORD'))

def send_sms(data):

    data['app'] = os.getenv('APP_NAME')
    account_sid = os.getenv('TWILIO_ID')
    auth_token = os.getenv('TWILIO_SECRET')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=data['send_message_to'],
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        body= f'il tuo codice di verifica {data['app']}: {data['body']}',
        )
    print(message.status + ' data: ' + json.dumps(data))


def listen_queue():
    while True:
        sms = redis_client.blpop('sms')[1]
        if sms:
            if test:
                send_sms(test_sms_settings)
            else:
                sms = json.loads(sms)
                send_sms(sms)

if __name__ == '__main__':
    listen_queue()
