from flask_mail import Message

from comunication_ltd import db, mail
import os
import hashlib
from comunication_ltd.database.models import User


def create_user(user):
    user.salt, user.password = hash_password(user)
    # TODO: Verify Password
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_mail(user_mail):
    return User.query.filter_by(mail=user_mail).first()


def hash_password(user):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000)
    return salt, key


def change_password(user_id, data):
    # TODO: verify current password
    db_user = get_user_by_id(user_id)
    # TODO: add check for 3 passwords in the past, and General rules of password, return True if success  else False
    db_user.password = hashlib.pbkdf2_hmac('sha256', data.get("new_password"), db_user.salt, 100000)
    db.session.commit()
    return True


def login(user):
    db_user = get_user_by_mail(user.get("email"))
    if db_user:
        key = hashlib.pbkdf2_hmac('sha256', user.get("password").encode('utf-8'), db_user.salt, 100000)
        is_same_key = key == db_user.password
        if is_same_key:
            return True, db_user
        else:
            return False
    return False


def forgot_password(payload):
    db_user = get_user_by_mail(payload.get("email"))
    key = hashlib.sha1()
    msg = Message("Forgot Password",
                  sender="comunication_LTD@protonmail.com",
                  recipients=[payload.get('email')])
    msg.body = f"Key for changing password-\n'{key}'"
    mail.send(msg)
    db_user.forgot_password = key
    db.session.commit()
