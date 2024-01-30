from flask import Flask, Response, request
import json
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from flask_hashing import Hashing