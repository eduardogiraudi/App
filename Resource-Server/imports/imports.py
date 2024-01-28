from flask import Flask, Response
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from dotenv import load_dotenv
import os