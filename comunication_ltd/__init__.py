##################################################
from pathlib import Path
from flask import Flask
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import secrets

##################################################
from config.config_handler import Config

__DB = 'sqlite:///database/server.db'
config = Config()
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get_value('APP', 'SECRET_KEY', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = config.get_value('APP', 'SQLALCHEMY_DATABASE_URI', __DB)
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
mail = Mail(app)

from comunication_ltd.layout import control

base_path = Path(__file__).parent
file_path = (base_path / "./database/server.db").resolve()

if not file_path.is_file():
    db.drop_all()
    db.create_all()
