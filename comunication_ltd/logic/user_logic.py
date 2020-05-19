from flask import Response, jsonify
from flask_mail import Message
from comunication_ltd import config
from comunication_ltd import db, mail
import os
import hashlib
from comunication_ltd.database.models import User
from comunication_ltd.logic.user_boundary import UserPayload
import re


def create_user(user):
    user_db = get_user_by_mail(user.email)
    if not user_db:
        user.salt, user.password = hash_password(user)
        # TODO: Verify Password , invalid password use this func - response_invalid_password()
        if not verify_password(user.password):
            response_invalid_password()
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
    if db_user.password != data.get("old_password"):
        return False
    if not verify_password(data.get("new_password")):
        return False
    if db_user.old_password_1 == data.get("new_password") or db_user.old_password_2 == data.get("new_password") or \
            db_user.password == data.get("new_password"):
        return False
    db_user.old_password_2 = db_user.old_password_1
    db_user.old_password_1 = db_user.password
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


def verify_password(password):
    # return false if password not valid
    if len(password) != config.get_value("PASSWORD_LENGTH", 10):
        return False
    if not any(x.islower() for x in password) and config.get_value("IS_BIG_LETTERS", False):  # capital letter
        return False
    if not any(x.isupper() for x in password) and config.get_value("IS_SMALL_LETTER", False):  # small letter
        return False
    if not any(x.digit() for x in password) and config.get_value("IS_NUMBERS", False):  # number
        return False
    string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if string_check.search(password) is None and config.get_value("SPECIAL_CHAR", False):  # special character
        return False
    return True


def forgot_change_password(payload):
    db_user = get_user_by_mail(payload.get("email"))
    key = db_user.forgot_password
    is_correct_key = key == str(payload.get('key'))
    if is_correct_key:
        # TODO: verify new password and move old passwords
        if not verify_password(payload.get('password')):
            return response_forbidden()
        if db_user.old_password_1 == payload.get("password") or db_user.old_password_2 == payload.get("password") or \
                db_user.password == payload.get("password"):
            return False
        db_user.old_password_2 = db_user.old_password_1
        db_user.old_password_1 = db_user.password
        db_user.password = hashlib.pbkdf2_hmac('sha256', payload.get("password"), db_user.salt, 100000)
        db_user.forgot_password = ""
        db.session.commit()

        return response_ok()
    return response_server_error()  # response 400 wrong key


def response_mail_already_exist():
    return Response(status=409)


def response_server_error():
    return Response(status=400)


def response_ok():
    return Response(status=200)


def response_forbidden():
    return Response(status=403)


def response_invalid_password():
    return Response(status=404)  # TODO: change status

