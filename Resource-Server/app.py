from flask import Flask, Response,redirect, render_template
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from dotenv import load_dotenv
from jwt.exceptions import ExpiredSignatureError
from flask_cors import CORS
import os
import json
from flask_pymongo import MongoClient

load_dotenv('.env')  # Carica le variabili d'ambiente da .env

app = Flask(__name__,template_folder='./app/build/', static_folder='./app/build/static/')
CORS(app)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

@app.route('/resource/profile', methods=['POST'])
@jwt_required()
def protected(): 
    return Response(json.dumps({'message':get_jwt_identity()}), status=200)

@app.route('/')
def red():
    return redirect('http://localhost:3001')
    # return render_template('index.html')


# @app.route('/resource/profile', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @jwt_required()
# def profile():
#     if request.method == 'GET': 
#         pass
#     if request.method == 'POST': 
#         pass
#     if request.method == 'PUT': 
#         pass
#     if request.method == 'DELETE': 
#         pass
    
#     return 'lol'