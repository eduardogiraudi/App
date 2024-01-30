from imports.imports import *

load_dotenv('../')  # Carica le variabili d'ambiente da .env
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
hashing = Hashing(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 
otp_secret_key = 'otp key'
otp_salt = 'otp salt'

@app.route('/otp/generate/<string:userID>')
@jwt_required()
def generateOTP(userID):
    current_timestamp = datetime.now()

    #il valore va sendato ad esempio con twilio
    return Response(json.dumps({
        'timestamp': current_timestamp, 
        # bisogna ancora prendere le ultime 4 cifre numeriche dell'hashing
        'otp':hashing.hash_value(current_timestamp + userID + otp_secret_key, salt=otp_salt)
        }), 200)

@app.route('/otp/check/<string:userID>')
@jwt_required()
def checkOTP(userID):
    try:
        given_otp = request.form.get('otp')
        #converte la data ottenuta in oggetto time
        given_timestamp = datetime.strptime(request.form.get('timestamp', '%Y-%m-%d %H:%M:%S'))
        current_timestamp = datetime.now()
        time_difference = current_timestamp - given_timestamp
        if time_difference<=timedelta(minutes=15):
            #prendere le ultime 4 cifre dell'hashing 
            correct_otp = hashing.hash_value(given_timestamp + userID + otp_secret_key, salt=otp_salt)
            if correct_otp == given_otp:
                #deve poi inserire nel db che si è verificati con questo dispositivo
                return Response(json.dumps({'message': 'Correct OTP'}), status=200) 
            else: 
                return Response(json.dumps({'message': 'Incorrect OTP'}), status=401)
        else:
            return Response(json.dumps({'message': 'OTP expired'}), status=401)
    except:
        return Response(json.dumps({'message': 'General error, please try again'}), status=500)