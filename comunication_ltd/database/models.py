from comunication_ltd import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mail = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.LargeBinary, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"User(User ID:{self.id}'," \
               f"Username - {self.username}'," \
               f"Password - '{self.password}'," \
               f"salt - {self.salt}'," \
               f"Created : - {self.date_created})"
