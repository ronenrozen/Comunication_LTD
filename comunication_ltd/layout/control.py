from flask_jwt_extended import jwt_required, create_access_token

from comunication_ltd import app
import requests
from flask import request, jsonify, Response
from comunication_ltd.logic.user_boundary import parse_user, UserPayload
import comunication_ltd.logic.user_logic as ul
from comunication_ltd.logic.customer_bounary import parse_customer, CustomerPayload
import comunication_ltd.logic.customer_logic as cl
import comunication_ltd.logic.pacakge_logic as pl


#####################################################
#################### USER ###########################
#####################################################

@app.route('/user/register', methods=['POST'])
def add_user():
    return ul.create_user(parse_user(request))


@app.route('/user/getall', methods=['GET'])
def get_all_users():
    return jsonify(ul.get_all())


@app.route('/user/change_password/<user_id>')
def change_password(user_id):
    is_changed = ul.change_password(user_id, request.get_json())
    if is_changed:
        return Response(status=200)
    else:
        return Response(status=500)


@app.route('/user/login', methods=['POST'])
def login():
    is_auth, user = ul.login(request.get_json())
    if is_auth:
        user_payload = jsonify(UserPayload(id=user.id, email=user.email).serialize())
        # user_payload["access_token"] = create_access_token(identity=user.email)
        # user_payload["refresh_token"] = create_refresh_token(identity=user.username)
        return user_payload
    else:
        return Response(status=500)


@app.route('/user/forgot_password', methods=['POST'])
def forgot_password():
    return ul.forgot_password(request.get_json())


@app.route('/user/forgot_change_password', methods=['POST'])
def forgot_change_password():
    return ul.forgot_change_password(request.get_json())


#####################################################
#################### CUSTOMER #######################
#####################################################

@app.route('/customer/addcustomer', methods=['POST'])
def add_customer():
    customer = cl.create_customer(parse_customer(request))
    if customer:
        return jsonify(CustomerPayload(id=customer.id, customer_name=customer.customer_name).serialize())
    else:
        return Response(status=409, response="User already exist")


@app.route('/customer/getall', methods=['GET'])
@jwt_required
def get_all_customers():
    return jsonify(cl.get_all())


@app.route('/customer/delete/<customer_id>', methods=['DELETE'])
@jwt_required
def delete_customer_by_id(customer_id):
    is_deleted = cl.delete_customer_by_id(customer_id)
    if is_deleted:
        return Response(status=200)
    else:
        return Response(status=500)


@app.route('/customer/update/<customer_id>', methods=['PUT'])
@jwt_required
def update_customer_by_id(customer_id):
    is_updated = cl.update_customer_by_id(customer_id, request.get_json())
    if is_updated:
        return Response(status=200)
    else:
        return Response(status=500)


#####################################################
#################### PACKAGE ########################
#####################################################
@app.route('/package/getall', methods=['GET'])
@jwt_required
def get_all_packages():
    return jsonify(pl.get_all())

# @app.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     ''' refresh token endpoint '''
#     current_user = get_jwt_identity()
#     ret = {
#             'token': create_access_token(identity=current_user)
#     }
#     return jsonify({'ok': True, 'data': ret}), 200
