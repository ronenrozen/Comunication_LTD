##################################################
from pathlib import Path
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

##################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dce0f737d0ade95d9118d41dcd6f9fcd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/server.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
from comunication_ltd.layout import control


base_path = Path(__file__).parent
file_path = (base_path / "./database/server.db").resolve()

if not file_path.is_file():
    db.drop_all()
    db.create_all()
