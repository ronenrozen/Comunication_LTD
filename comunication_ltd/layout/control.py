from comunication_ltd import app
import requests
from flask import request, jsonify, Response
from comunication_ltd.logic.user_boundary import parse_user, UserPayload
from comunication_ltd.logic.user_logic import create_user


@app.route('/user/adduser', methods=['POST'])
def add_user():
    user = create_user(parse_user(request))
    if user:
        return jsonify(UserPayload(user.id, user.username, user.password, user.role).serialize())
    else:
        return Response(status=409, response="User already exist")
