from pathlib import Path

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
        if not verify_password(user.password):
            return response_invalid_password()
        if not check_sqli(user.email):
            return response_server_error()  # might be sql injection
        user.salt, user.password = hash_password(user)
        db.session.add(user)
        db.session.commit()
        return UserPayload(id=user.id, email=user.email).serialize()
    return response_mail_already_exist()


def create_admin_user(user):
    user_db = get_user_by_mail(user.email)
    if not user_db:
        user.salt, user.password = hash_password(user)
        db.session.add(user)
        db.session.commit()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_mail(user_email):
    return User.query.filter_by(email=user_email).first()


def hash_password(user):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000)
    return salt, key


def change_password(user_id, data):
    db_user = get_user_by_id(user_id)
    hashed_new_password = hashlib.pbkdf2_hmac('sha256', data.get("new_password").encode("utf8"), db_user.salt, 100000)
    hashed_old_password = hashlib.pbkdf2_hmac('sha256', data.get("old_password").encode("utf8"), db_user.salt, 100000)
    if db_user.password != hashed_old_password:
        return Response(status=400)
    if not verify_password(data.get("new_password")):
        return Response(status=401)
    if db_user.old_password_1 == hashed_new_password or db_user.old_password_2 == hashed_new_password or \
            db_user.password == hashed_new_password:
        return Response(status=403)
    db_user.old_password_2 = db_user.old_password_1
    db_user.old_password_1 = db_user.password
    db_user.password = hashed_new_password
    db.session.commit()
    return Response(status=200)


def login(user):
    db_user = get_user_by_mail(user.get("email"))
    if db_user:
        if db_user.blocked:
            return Response(status=400)
        key = hashlib.pbkdf2_hmac('sha256', user.get("password").encode('utf-8'), db_user.salt, 100000)
        is_same_key = key == db_user.password
        if is_same_key:
            db_user.password_attempts = 0
            db.session.commit()
            return db_user
        else:
            response = password_attempt_logic(db_user)
            return Response(status=401) if response else Response(status=404)
    return Response(status=403)


def password_attempt_logic(user):
    flag = False
    number_of_attempts = int(config.get_value('PASSWORD_ATTEMPTS', 3)) - 1
    password_attempt = user.password_attempts
    if password_attempt < number_of_attempts:
        user.password_attempts = password_attempt + 1
    elif password_attempt == number_of_attempts:
        user.password_attempts = number_of_attempts + 1
        user.blocked = True
        flag = True
    db.session.commit()
    return flag


def forgot_password(payload):
    db_user = get_user_by_mail(payload.get("email"))
    if db_user:
        key = hashlib.sha1(os.urandom(10)).hexdigest()
        msg = Message("Forgot Password",
                      sender="comunication_LTD@protonmail.com",
                      recipients=[payload.get('email')])
        msg.body = f"Go to our site http://localhost:3000/forgetchangepassword and use below" \
                   f" Key for changing password-\n{key}"
        mail.send(msg)
        db_user.forgot_password = str(key)
        db.session.commit()
        return response_ok()
    return response_server_error()


def verify_password(password):
    # return false if password not valid
    if len(password) < int(config.get_value("PASSWORD_LENGTH", 10)):
        return False
    if not any(x.islower() for x in password) and config.get_value("IS_SMALL_LETTERS", True):  # small letter
        return False
    if not any(x.isupper() for x in password) and config.get_value("IS_BIG_LETTERS", True):  # capital letter
        return False
    digit_check = re.compile('[1-9]')
    if digit_check.search(password) is None and config.get_value("IS_NUMBERS", True):
        return False
    string_check = re.compile('[@_!#$%^&*()?/\|}{~:]')
    if string_check.search(password) is None and config.get_value("SPECIAL_CHAR", True):  # special character
        return False
    if password_dict_check(password):
        return False
    return check_sqli(password)  # returns true if ' " < > = not exist else false


def check_sqli(data):
    string_check = re.compile('''[><'"=]''')
    if string_check.search(str(data)) is not None or not data:  # for sqli
        return False
    return True


def password_dict_check(password):
    base_path = Path(__file__).parent
    file_path = (base_path / "./realhuman_phill.txt").resolve()

    with open(file_path, 'r') as f:
        for line in f.readline().strip():
            if line == password:
                return True
    return False


def forgot_change_password(payload):
    db_user = get_user_by_mail(payload.get("email"))
    if not db_user:
        return response_mail_already_exist()
    key = db_user.forgot_password
    is_correct_key = key == str(payload.get('key'))
    if is_correct_key:
        if not verify_password(payload.get('password')):
            return response_forbidden()
        hashed_password = hashlib.pbkdf2_hmac('sha256', payload.get("password").encode('utf-8'), db_user.salt, 100000)
        if db_user.old_password_1 == hashed_password or db_user.old_password_2 == hashed_password or \
                db_user.password == hashed_password:
            return Response(status=401)
        db_user.old_password_2 = db_user.old_password_1
        db_user.old_password_1 = db_user.password
        db_user.password = hashed_password
        db_user.forgot_password = ""
        db.session.commit()

        return response_ok()
    db_user.forgot_password = ""
    db.session.commit()
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
    return Response(status=400)
