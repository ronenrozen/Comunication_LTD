from flask import Response, jsonify
from flask_mail import Message

from comunication_ltd import db, mail
import os
import hashlib
from comunication_ltd.database.models import User
from comunication_ltd.logic.user_boundary import UserPayload


def create_user(user):
    user_db = get_user_by_mail(user.email)
    if not user_db:
        user.salt, user.password = hash_password(user)
        # TODO: Verify Password , invalid password use this func - response_invalid_password()
        db.session.add(user)
        db.session.commit()
        return UserPayload(id=user.id, email=user.email).serialize()
    return response_mail_already_exist()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_mail(user_email):
    return User.query.filter_by(email=user_email).first()


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
    return


def forgot_password(payload):
    db_user = get_user_by_mail(payload.get("email"))
    if db_user:
        key = hashlib.sha1(os.urandom(10)).hexdigest()
        msg = Message("Forgot Password",
                      sender="comunication_LTD@protonmail.com",
                      recipients=[payload.get('email')])
        msg.body = f"Key for changing password-\n'{key}'"
        mail.send(msg)
        db_user.forgot_password = str(key)
        db.session.commit()
        return response_ok()
    return response_server_error()


def forgot_change_password(payload):
    db_user = get_user_by_mail(payload.get("email"))
    key = db_user.forgot_password
    is_verify = key == str(payload.get('key'))
    if is_verify:
        # TODO: verify new password and move old passwords
        db_user.password = hashlib.pbkdf2_hmac('sha256', payload.get("password"), db_user.salt, 100000)
        db.session.commit()
        return response_ok()
    return response_server_error() # response 400 wrong key


def response_mail_already_exist():
    return Response(status=409)


def response_server_error():
    return Response(status=400)


def response_ok():
    return Response(status=200)
