##################################################
import datetime
##################################################
from pathlib import Path
from flask import Flask
from flask_jwt_extended import JWTManager
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
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = config.get_value('SECRET_KEY', secrets.token_hex(16))
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)
jwt._set_error_handler_callbacks(app)

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



def create_initial_db():
    from comunication_ltd.logic import user_logic, pacakge_logic, customer_logic
    from comunication_ltd.database.models import User, Package, Customer
    user_logic.create_admin_user(User(email='admin@admin.com', password='admin'))
    pacakge_logic.create_package(Package(package_name="20G, 100$", package_size=20, package_price=100))
    pacakge_logic.create_package(Package(package_name="30G, 120$", package_size=30, package_price=120))
    pacakge_logic.create_package(Package(package_name="40G, 130$", package_size=40, package_price=130))
    pacakge_logic.create_package(Package(package_name="50G, 140$", package_size=50, package_price=140))
    customer_logic.create_customer(
        Customer(customer_name="Tzuf_LTD", sector="Public Transport", email="tzufltd@gmail.com", package_id=1))
    customer_logic.create_customer(
        Customer(customer_name="Sports Eron", sector="Sport", email="brutality@gmail.com", package_id=3))


base_path = Path(__file__).parent
file_path = (base_path / "./database/server.db").resolve()

if not file_path.is_file():
    db.drop_all()
    db.create_all()
    create_initial_db()
