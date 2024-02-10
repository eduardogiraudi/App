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
logging.basicConfig(filename='./logs/errors.log', level=logging.ERROR)
#collezione di utenti mongodb
db = client['users']
collection = db['users']
#rotta di login







@app.route('/auth/login', methods=[ 'POST'])
def login ():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        real_user = collection.find_one({'name':name})
        if real_user:
            if hashing.check_value(real_user["password"],password, real_user["salt"]):
                response = {
                    'email' : real_user['email'], #deve essere univoco
                    'name': real_user['name'],
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
        





#creo un admin
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        salt = secrets.token_hex(16)
        admin = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': hashing.hash_value(request.form.get('password'), salt=salt),
            'salt': salt,
            'role': 'user'
        }
        collection.insert_one(admin)
        return Response(json.dumps({'message': 'Account created'}),status=200)
    except ValueError as ValErr:
        app.logger.error(str(ValErr))
        return Response(json.dumps({'message': 'Error, please try again'}), status=500)





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
        response = make_response(redirect('http://localhost:3000'))
        response.set_cookie('token', create_access_token(profile['sub'],expires_delta=expires)) 
        response.set_cookie('refresh_token', create_refresh_token(profile['sub'],expires_delta=expires)) 

        # create_access_token(profile['name'])
        return response

        # Impostare le informazioni utente nei cookie
    except ValueError as ValErr:
        app.logger.error(str(ValErr))
        #altrimenti redirect a pagina "di login"
        return redirect('/')
    