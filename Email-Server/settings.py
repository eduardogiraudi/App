
import redis
import os
from dotenv import load_dotenv
load_dotenv('.env')

test = False
test_email_settings = {
    'sender': 'Eduardo <eduardo.giraudi@edu.unito.it>',
    'to': 'Eduardo <eduardo.giraudi13@gmail.com>',
    'subject': 'Email testing',
    'text': 'email server running in test mode',
    'context': {
        'title': 'titolo prova',
        'text': 'testo di prova', 
        'name': 'Eduardo',
        'link': 'https://www.linkdiprova.it',
        'link_title': 'Link'
    }
}
