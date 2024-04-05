from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename



current_directory = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(current_directory, 'bookUploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myvdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
