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

config = Config()
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get_value('SECRET_KEY', secrets.token_hex(16))
app.config['SQLALCHEMY_DATABASE_URI'] = config.get_value('SQLALCHEMY_DATABASE_URI', 'sqlite:///database/server.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='comunication.LTD@gmail.com',
    MAIL_PASSWORD='erontzufronen',
))

mail = Mail(app)

from comunication_ltd.layout import control

base_path = Path(__file__).parent
file_path = (base_path / "./database/server.db").resolve()

if not file_path.is_file():
    from comunication_ltd.logic import user_logic
    from comunication_ltd.database.models import User

    db.drop_all()
    db.create_all()
    user_logic.create_user(User(email='admin@admin.com', password='admin'))
    user_logic.create_user(User(email='ronen.rozen@gmail.com', password='admin'))
