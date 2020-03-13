from comunication_ltd import db
import os
import hashlib


def create_user(user):
    user.salt, user.password = hash_password(user)
    db.session.add(user)
    db.session.commit()
    return user


def hash_password(user):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000)
    return salt, key
