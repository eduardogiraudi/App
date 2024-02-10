
from flask import Flask, json, Response, request, url_for, redirect, make_response
from flask_pymongo import MongoClient
from flask_hashing import Hashing
import secrets
from bson.json_util import dumps 
from bson import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from dotenv import load_dotenv
import os
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
import logging
from flask_cors import CORS