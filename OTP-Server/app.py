from flask import Flask, Response, request, redirect
import json
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from flask_hashing import Hashing
import redis
from flask_pymongo import MongoClient
import secrets


load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 
jwt = JWTManager(app)
hashing = Hashing(app)
mongoclient = MongoClient(f'mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/')
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, password=os.getenv('REDIS_PASSWORD'))


def dynamic_secret_key(timestamp):
    return hashing.hash_value(timestamp, salt=os.getenv('SALT_SECRET_KEY'))

def hash_to_last_4_int(hash):
    otp = ''
    for i in range(len(hash)-1,-1,-1,):
        if hash[i].isdigit():
            otp+=hash[i]
        if len(otp) == 4:
            break
    return otp

@app.route('/otp/generate/', methods=['POST'])
@jwt_required()
def generateOTP():
    try:
        otp_salt = secrets.token_hex(32)
        current_timestamp = str(datetime.now())
        otp_secret_key = dynamic_secret_key(current_timestamp)
        userID = get_jwt_identity()


        

        send_message_to = request.form.get('phone')



        db = mongoclient['users']
        collection = db['users']
        collection.update_one({'name':userID}, {"$set": {"OTP_Salt": otp_salt}})
        
        data={
            'send_message_to': send_message_to,
            'body': hash_to_last_4_int(hashing.hash_value(str(current_timestamp) + userID + otp_secret_key, salt=otp_salt))
        }

        redis_client.rpush(json.dumps(data))

        return Response(json.dumps({'message':{

            'timestamp': current_timestamp,
            # 'otp':hashing.hash_value(current_timestamp + userID + otp_secret_key, salt=otp_salt)
        }
            # bisogna ancora prendere le ultime 4 cifre numeriche dell'hashing
            }), 200)
    except ValueError as ValErr:
        # app.logger.error(str(ValErr))
        return Response(json.dumps({'message':'General error'}),status=500)



@app.route('/')
def redirect_to_frontend_server (): 
    return redirect('http://localhost:3002')


@app.route('/otp/check/', methods=['POST'])
@jwt_required()
def checkOTP():
    try:
        userID = get_jwt_identity()
        db = mongoclient['users']
        collection = db['users']
        real_user = collection.find_one({'name':userID})
        given_otp = request.form.get('otp')
        #converte la data ottenuta in oggetto time
        given_timestamp = request.form.get('timestamp')
        given_timestamp = datetime.strptime(given_timestamp,  '%Y-%m-%d %H:%M:%S.%f') 
        current_timestamp = datetime.now()
        otp_secret_key = dynamic_secret_key(str(given_timestamp))
        time_difference = current_timestamp - given_timestamp
        if time_difference<=timedelta(minutes=15):
            #prendere le ultime 4 cifre dell'hashing 
            correct_otp = hash_to_last_4_int(hashing.hash_value(str(given_timestamp) + userID + otp_secret_key, salt=real_user['OTP_Salt']))
            if correct_otp == given_otp:
                #deve poi inserire nel db che si è verificati con questo dispositivo
                #elimino il salt nel db
                collection.update_one({'name':userID}, {"$set": {"OTP_Salt": ''}})
                return Response(json.dumps({'message': 'Correct OTP'}), status=200) 
            elif real_user['OTP_Salt'] == '':
                return Response(json.dumps({'message': 'You probably already used this OTP'}), status=410)
            else: 
                return Response(json.dumps({'message': 'Incorrect OTP'}), status=401)
        else:
            return Response(json.dumps({'message': 'OTP expired'}), status=401)
    except ValueError as ValErr:
        # app.logger.error(str(ValErr))
        return Response(json.dumps({'message': 'General error, please try again' }), status=500)