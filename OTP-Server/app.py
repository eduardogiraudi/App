from imports.imports import *

load_dotenv('../.env')  # Carica le variabili d'ambiente da .env
load_dotenv('./OTP.env')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 
jwt = JWTManager(app)
hashing = Hashing(app)
mongoclient = MongoClient(os.getenv('MONGO_HOST'), int(os.getenv('MONGO_PORT')))
logging.basicConfig(filename='./logs/errors.log', level=logging.ERROR)


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
        account_sid = os.getenv('TWILIO_ID')
        auth_token = os.getenv('TWILIO_SECRET')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=send_message_to,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            body=hash_to_last_4_int(hashing.hash_value(str(current_timestamp) + userID + otp_secret_key, salt=otp_salt)),
        )

        db = mongoclient['users']
        collection = db['users']
        collection.update_one({'name':userID}, {"$set": {"OTP_Salt": otp_salt}})
        
        # print(message.sid)
        #il valore va sendato ad esempio con twilio
        return Response(json.dumps({'message':{

            'timestamp': current_timestamp,
            # 'otp':hashing.hash_value(current_timestamp + userID + otp_secret_key, salt=otp_salt)
        }
            # bisogna ancora prendere le ultime 4 cifre numeriche dell'hashing
            }), 200)
    except ValueError as ValErr:
        app.logger.error(str(ValErr))
        return Response(json.dumps({'message':'General error'}),status=500)





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
        app.logger.error(str(ValErr))
        return Response(json.dumps({'message': 'General error, please try again' }), status=500)