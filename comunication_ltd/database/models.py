from sqlalchemy import ForeignKey

from comunication_ltd import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    old_password_1 = db.Column(db.String(120), nullable=True)
    old_password_2 = db.Column(db.String(120), nullable=True)
    salt = db.Column(db.LargeBinary, nullable=False)
    forgot_password = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"User(User ID:{self.id}'," \
               f"Email - {self.email}'," \
               f"Password - '{self.password}'," \
               f"salt - {self.salt}'," \
               f"Created : - {self.date_created})"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    sector = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    package_id = db.Column(db.Integer, ForeignKey('package.id'))
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Customer(Customer ID:{self.id}'," \
               f"Company Name - {self.company_name}'," \
               f"email - '{self.email}'," \
               f"Created : - {self.date_created})"


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
