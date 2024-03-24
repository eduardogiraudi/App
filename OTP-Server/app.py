from flask import Flask, Response, request, redirect
import json
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt, decode_token
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from flask_hashing import Hashing
import redis
from flask_pymongo import MongoClient, ObjectId
import secrets


load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
jwt = JWTManager(app)
hashing = Hashing(app)
mongoclient = MongoClient(f'mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/')
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, password=os.getenv('REDIS_PASSWORD'))
db = mongoclient['users']
collection = db['users']

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



# @jwt.expired_token_loader
# def get_expired_token_device (header, payload): 
#     token = payload
#     if 'device_id' in token:
#         device_id = token['device_id']
#         userId = token['sub']
#         user = collection.find_one({'_id': ObjectId(userId)})
#         if any(device_id == dev['device_id'] for dev in user['devices']):
#             return json.dumps({'message': token['device_id']})
#         else:
#             pass #token da blacklistare
#         #o il token è scaduto ma il dispositivo è ancora associato oppure il dispositivo è stato scollegato, allora lì il token va messo in blacklist
#     else: return json.dumps({'message': 'Token has expired'})  


# @app.route('/otp/test')
# @jwt_required()
# def handler ():
#     return 'hola'



@app.route('/otp/generate/', methods=['POST'])
@jwt_required()
def generateOTP():
    try:
        otp_salt = secrets.token_hex(32)
        current_timestamp = str(datetime.now())
        otp_secret_key = dynamic_secret_key(current_timestamp)
        userID = get_jwt_identity()
        user = collection.find_one({'_id': ObjectId(userID)})
        if not user: return Response(json.dumps({'message': 'user not found, probably deleted'}), status=404)

        preferred_broker = request.form.get('broker')
        # if not preferred_broker: return Response(json.dumps({'message': 'no broker provided'}), status=400)

        body= hash_to_last_4_int(hashing.hash_value(str(current_timestamp) + userID + otp_secret_key, salt=otp_salt))

        if preferred_broker == 'sms' or preferred_broker != 'email': #così ovviamo a errori tipo nessun broker selezionato
            if 'phone' in user:
                preferred_broker = 'sms' #se il preferred broker non era settato correttamente lo risettiamo 
                data={
                    'send_message_to': user['phone'],
                    'body': body
                }
            else: preferred_broker='email'

        if preferred_broker=='email': #altrimenti email

            data = {
                'sender': f'OTP <accounts@{os.getenv('APP_NAME')}.it',
                'to': f'{user['username']} <{user['email']}>',
                'subject': 'Il tuo codice OTP',
                'template': 'otp',
                'text': f'Il tuo codice di verifica OTP è {body}',
                'data': {
                    'otp': body, 
                    'name': user['username']
                }
            }
        
        # db = mongoclient['users']
        # collection = db['users']
        collection.update_one({'_id':ObjectId(userID)}, {"$set": {"OTP_Salt": otp_salt, 'OTP_number_of_tries': 0}})
        

        redis_client.rpush(preferred_broker,json.dumps(data))

        return Response(json.dumps({'message':{
            'broker': preferred_broker,
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
'''





jwt valid after da implementare






'''

@app.route('/otp/check', methods=['POST'])
@jwt_required()
def checkOTP():
    try:
        userID = get_jwt_identity()
        real_user = collection.find_one({'_id':ObjectId(userID)})
        given_otp = request.form.get('otp')
        user_agent = request.form.get('user_agent')
        if not real_user: return Response(json.dumps({'message': 'user not found, probably deleted'}), status=404)
        if not given_otp: return Response(json.dumps({'message': 'no otp provided'}), status=400)
        if not user_agent: return Response(json.dumps({'message': 'no user agent provided'}), status=400)
        #converte la data ottenuta in oggetto time
        given_timestamp = request.form.get('timestamp')
        if not given_timestamp: return Response(json.dumps({'message': 'no timestamp provided'}), status=400)
        given_timestamp = datetime.strptime(given_timestamp,  '%Y-%m-%d %H:%M:%S.%f') 
        current_timestamp = datetime.now()
        otp_secret_key = dynamic_secret_key(str(given_timestamp))
        time_difference = current_timestamp - given_timestamp
        if time_difference<=timedelta(minutes=5):
            #prendere le ultime 4 cifre dell'hashing 
            correct_otp = hash_to_last_4_int(hashing.hash_value(str(given_timestamp) + userID + otp_secret_key, salt=real_user['OTP_Salt']))
            if correct_otp == given_otp:
                #deve poi inserire nel db che si è verificati con questo dispositivo
                new_device = secrets.token_hex(32)

                #elimino il salt nel db e aggiungo il nuovo dispositivo
                collection.update_one({'_id':ObjectId(userID)}, {"$set": {"OTP_Salt": '','OTP_number_of_tries': 0}, '$push':{'devices': {'device_id':new_device, 'device_name': user_agent}}})

                #id del dispositivo da storare nei cookie
                return Response(json.dumps({'message': new_device}), status=200) 
            elif real_user['OTP_Salt'] == '':
                return Response(json.dumps({'message': 'You probably already used this OTP'}), status=410)
            else: 
                # in sto caso si adda un campo tries col numero tentativi, si gestisce anche la sua exception allora
                # si resetta all'otp corretto

                collection.update_one({'_id': ObjectId(userID)},{'$inc': {'OTP_number_of_tries':1}})
                updated_user=collection.find_one({'_id': ObjectId(userID)})
                if updated_user['OTP_number_of_tries']>=3:
                    collection.update_one({'_id': ObjectId(userID)}, {'$set':{'OTP_number_of_tries': 0, 'OTP_Salt': ''}})
                    return Response(json.dumps({'message':'Wrong OTP for 3 times in a row, request a new OTP code'}), status=410)

                return Response(json.dumps({'message': 'Incorrect OTP'}), status=401)
        else:
            return Response(json.dumps({'message': 'OTP expired'}), status=401)
    except ValueError as ValErr:
        # app.logger.error(str(ValErr))
        return Response(json.dumps({'message': 'General error, please try again' }), status=500)
    

@app.route('/otp/select_broker', methods=['POST'])
@jwt_required()
def select_broker():
    userId = get_jwt_identity()
    user = collection.find_one({'_id': ObjectId(userId)})
    if not user: return Response(json.dumps({'message':'user not found, probably deleted'}), status=404)
    user['_id'] = str(user['_id']) 
    brokers = {}
    brokers["email"]=user['email']
    mask = "*" * 11
    brokers['email']=mask+brokers['email'][11:]

    #dato che il numero di telefono non è obbligatorio registrarlo
    if 'phone' in user:
        brokers["phone"] = mask+user['phone'][11:] #con sta impostazione bisogna assicurarsi di storare anche il prefisso altrimenti si vedono solo gli asterischi
    

    return Response(json.dumps({"message":brokers}),status=200)

@app.route('/otp/check_device', methods=['POST'])
@jwt_required()
def check_device():
    try:
        user_id = get_jwt_identity()
        device=request.form.get('device')

        user = collection.find_one({'_id': ObjectId(user_id)})
        if not user: return Response(json.dumps({'message': 'user not found, probably deleted'}), status=404)
        if not device: return Response(json.dumps({'message': 'no device provided'}), status=400)

        #se il device è presente dentro la chiave device_id dentro l'array di oggetti devices
        if any(device == dev['device_id'] for dev in user['devices']):
            return Response(json.dumps({'message': 'ok'}), status=200)
        else: return Response(json.dumps({'message': 'device not found'}), status=404)
    except:
        return Response(json.dump({'message': 'internal server error'}), status=500)