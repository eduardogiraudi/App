
import redis
import os
from dotenv import load_dotenv
load_dotenv('.env')
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, password=os.getenv('REDIS_PASSWORD'))
redis_client.rpush('email','prova push')