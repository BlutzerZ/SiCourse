from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

print(os.getenv('MYSQL_HOST'))

app = Flask(__name__)
app.config.from_object(Config)
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = '/image'

from routes.users import *
from routes.admin import *