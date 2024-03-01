from imports.imports import *



expires = timedelta(minutes=15)
load_dotenv('../.env')  # Carica le variabili d'ambiente da .env
load_dotenv('./Auth.env')
app = Flask(__name__)
oauth = OAuth(app)

CORS(app)

## runnarla con flask --debug run --port 8080 (non va la porta 5000 per mac per il localhost e serve il dominio localhost per oauth di facebook in fase di sviluppo)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_ID'),
    client_secret=os.getenv('GOOGLE_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://127.0.0.1:8080/auth/google/authorize',
    client_kwargs={'scope': 'email profile'},
)
client = MongoClient(os.getenv('MONGO_HOST'), int(os.getenv('MONGO_PORT')))
hashing = Hashing(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
# logging.basicConfig(filename='./logs/errors.log', level=logging.ERROR)
#collezione di utenti mongodb
db = client['users']
collection = db['users']
#rotta di login




password_policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1
)




@app.route('/auth/forgot_password', methods=['POST'])
def require_reset_token (): 
    try:
        serializer = URLSafeTimedSerializer(os.getenv('JWT_SECRET_KEY'))
        email = request.form.get('email')
        user = collection.find_one({'email':email})
        if user:
            token = str(user['_id'])
            token = serializer.dumps(token)
            #manda la mail e restituisce ok per dire al frontend per far visualizzare i diversi tipi di messaggio
            msg = Message('Il tuo link di recupero', body='il link scadrà tra 15 minuti '+os.getenv('FRONTEND_DOMAIN')+'/change_password?token='+token, sender=os.getenv('MAIL_SENDER'), recipients=[email])
            mail.send(msg)
            return Response(json.dumps({'message':'ok'}),status=200)
        else:
            return Response(json.dumps({'message':'User not found'}),status=404)
    except ValueError as er: 
        return Response(json.dumps({'message':'bad request, missing arguments'}),status=400)
        
@app.route('/auth/reset_password',methods=['POST'])
def reset_password ():
    #da mettere i controlli sulle nuove password anche qua poi
    try:
        token = request.form.get('token')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if confirm_password!=password:
            return Response(json.dumps({'message':'password and confirm password do not match'}),status=400)
        # policy.test returna un array vuoto se la pass rispetta i requirements, Passwordstats restituisce quanti match ci sono, quindi se non ci sono lettere minuscole i requirements non vengono rispettati
        if password_policy.test(password) or (not PasswordStats(password).letters_lowercase):
            return Response(json.dumps({'message':'password does not meet complexity requirements'}), status=400)


        serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
        token_data = serializer.loads(token, max_age=900)
        salt = secrets.token_hex(16)
        password = hashing.hash_value(request.form.get('password'), salt=salt)
        collection.update_one({'_id': ObjectId(token_data)},{'$set': {'password': password,'salt': salt}})
        return Response(json.dumps({'message':token_data}),status=200)
    except SignatureExpired:
        return Response(json.dumps({'message':'expired link'}),status=410)    
    except BadSignature:
        return Response(json.dumps({'message':'invalid token'}), status=401)

    # try:
    #     pass
    # except SignatureExpired:
    #     return jsonify({'message': 'Token has expired'})

    # except BadSignature:
    #     return jsonify({'message': 'Invalid token'})


@app.route('/auth/get_new_verification_link', methods=['POST'])
def new_verification_link():
    try:
        email = request.form.get('email')
        if email:
            user = collection.find_one({'email':email})
            if user:
                serializer = URLSafeTimedSerializer(os.getenv('JWT_SECRET_KEY'))
                token = str(user['_id'])
                token = serializer.dumps(token)

                msg = Message('Il tuo link di attivazione account', body='il link di attivazione sarà valido per 24 ore '+os.getenv('FRONTEND_DOMAIN')+'/activate_account?token='+token, sender=os.getenv('MAIL_SENDER'), recipients=[email])
                mail.send(msg)
                return Response(json.dumps({'message':'email sent'}), status=200)
            else:
                return Response(json.dumps({'message':'user not found'}),status=404)
        else:
            return Response(json.dumps({'message':'no email provided'}), status=400)
    except:
        return Response(json.dumps({'message':'internal server error'}), status=500)


@app.route('/auth/login', methods=[ 'POST'])
def login ():

    #se l'user non è loggato deve dire se vuole richiedere un nuovo link di attivazione
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        real_user = collection.find_one({'email':email})
        if real_user:
            if not real_user['active']:
                return Response(json.dumps({'message':'user not verified'}), status=422)
            if hashing.check_value(real_user["password"],password, real_user["salt"]):
                response = {
                    'email' : real_user['email'], #deve essere univoco
                    'username': real_user['username'],
                    'role' : real_user['role'],
                    '_id' : str(real_user['_id']),
                    'token': create_access_token(identity=str(real_user['_id']), expires_delta=expires), #mettere poi id
                    'refresh_token': create_refresh_token(identity=str(real_user['_id']))
                } #restituire poi un token e un refresh token
                response = dumps({'message':response})
                return Response(response, status=200)
            else: 
                return Response(json.dumps({'message': 'Invalid password'}), status=401)
        else:
            return Response(json.dumps({'message': 'User not found'}), status=404)
        



#PYMONGO  THROWA STATUS 404 SE UNO DEI DUE ARGOMENTI POSSIBILI è NULL, api da dividere in chech username e email
@app.route('/auth/user_exists', methods=['GET'])
def user_exists():
    if(request.args.get('username')):
        username = request.args.get('username')
        if(collection.find_one({'username':username})):
            return Response(json.dumps({'message':'Resource already exists'}),status=409)
        else:
            return Response(json.dumps({'message':'available'}), status=200)
    elif (request.args.get('email')):
        email = request.args.get('email')
        if(collection.find_one({'email':email})):
            return Response(json.dumps({'message':'Resource already exists'}),status=409)
        else:
            return Response(json.dumps({'message':'available'}), status=200)
    else:
        return Response(json.dumps({'message':'missing arguments'}), status=400)


#crea account
@app.route('/auth/register', methods=['POST'])
def register():
    try:

        salt = secrets.token_hex(16)
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        if collection.find_one({'username':username}):
            return Response(json.dumps({'message':'username already exist'}), status=409)

        if confirm_password!=password:
            return Response(json.dumps({'message':'password and confirm password do not match'}),status=400)
        # policy.test returna un array vuoto se la pass rispetta i requirements, Passwordstats restituisce quanti match ci sono, quindi se non ci sono lettere minuscole i requirements non vengono rispettati
        if password_policy.test(password) or (not PasswordStats(password).letters_lowercase):
            return Response(json.dumps({'message':'password does not meet complexity requirements'}), status=400)
        #validazione email (se non è valida la butta in exception e se esiste già returna 409)

        validate_email(email)
        if collection.find_one({'email':email}):
            return Response(json.dumps({'message':'email already exist'}),status=409)


        #aggiungere validazione poi
        user = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': hashing.hash_value(request.form.get('password'), salt=salt),
            'salt': salt,
            'role': 'user',
            'active':False #in tutte le rotte da loggati dobbiamo verificare se l'utente è attivo, magari creiamo un decoratore??
        }
        insert=collection.insert_one(user)
        serializer = URLSafeTimedSerializer(os.getenv('JWT_SECRET_KEY'))
        token = str(insert.inserted_id)
        token = serializer.dumps(token)

        msg = Message('Il tuo link di attivazione account', body='il link di attivazione sarà valido per 24 ore '+os.getenv('FRONTEND_DOMAIN')+'/activate_account?token='+token, sender=os.getenv('MAIL_SENDER'), recipients=[email])
        mail.send(msg)
        return Response(json.dumps({'message': user['username']}),status=200)
    except EmailNotValidError as e:
        return Response(json.dumps({'message':'invalid email'}),status=400)
    except ValueError as ValErr:
        app.logger.error(str(ValErr))
        return Response(json.dumps({'message': 'Error, please try again'}), status=500)

#attiva account
@app.route('/auth/activate_account', methods=['POST'])
def activate_account ():
    try:
        serializer = URLSafeTimedSerializer(os.getenv('JWT_SECRET_KEY'))
        token = request.form.get('token')
        if not token:
            return Response(json.dumps({'message':'The URL is missing parameters, or it may be incomplete'}), status=400)
        token_data = serializer.loads(token,max_age=60*60*24)
        user = collection.find_one({'_id':ObjectId(token_data)})
        if not user['active']:
            collection.update_one({'_id':ObjectId(token_data)},{'$set':{'active':True}})
            return Response(json.dumps({'message':'account activated'}), status=200)
        return Response(json.dumps({'message':'account already activated'}), status=409)
    except SignatureExpired:
        return Response(json.dumps({'message':'link expired, please request a new activation link'}), status=410)
    except BadSignature:
        return Response(json.dumps({'message':'invalid link'}), status=401)













#rotta per ottenere un nuovo access token
@app.route('/auth/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, expires_delta=expires)
        return Response(json.dumps({'message':new_access_token}), status=200)
    except ValueError as ValErr:
        app.logger.error(str(ValErr))
        return Response(json.dumps({'message': 'Invalid token or internal server error'}), status=401)
    







#oAuth google
    
#mostra bottone di login esempio di view html 
@app.route('/')
def index():
    return '<a href="/auth/google/login">Login con Google</a>'


#ottengo il token
@app.route('/auth/google/login')
def google_login():
    return google.authorize_redirect(url_for('authorize', _external=True))







#ottengo le informazioni andando a chiamare l'api userinfo
@app.route('/auth/google/authorize')
def authorize():
    #se va a buon fine display dei dati ottenuti
    try:
        token = google.authorize_access_token()
        resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
        profile = resp.json()
        #todo: salvare le info utili nel db utenti e restituire un access token per mantenere l'utente loggato
        # return f'{profile} <a href="/profile">Profilo</a> <img src="{profile["picture"]}"/>'
                # Salvare le informazioni utili nei cookie
        if(not collection.find_one({'google_id':profile['sub']})):
            collection.insert_one({
                'google_id': profile['sub'],
                'email': profile['email'],
                'username': profile['given_name'],
                'propic': profile['picture']
            })
        else:
            pass #se l'utente è già entrato in precedenza con google
        response = make_response(redirect(os.getenv('FRONTEND_DOMAIN')))
        response.set_cookie('token', create_access_token(profile['sub'],expires_delta=expires)) 
        response.set_cookie('refresh_token', create_refresh_token(profile['sub'],expires_delta=expires)) 

        # create_access_token(profile['name'])
        return response

        # Impostare le informazioni utente nei cookie
    except ValueError as ValErr:
        app.logger.error(str(ValErr))
        #altrimenti redirect a pagina "di login"
        return redirect('/')
    