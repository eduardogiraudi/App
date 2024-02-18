from imports.imports import *
load_dotenv('../')  # Carica le variabili d'ambiente da .env

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

@app.route('/resource/protected')
@jwt_required()
def protected(): 
    return Response(get_jwt_identity(), status=200)

@app.route('/resource/profile', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def profile():
    if request.method == 'GET': 
        pass
    if request.method == 'POST': 
        pass
    if request.method == 'PUT': 
        pass
    if request.method == 'DELETE': 
        pass
    
    return 'lol'