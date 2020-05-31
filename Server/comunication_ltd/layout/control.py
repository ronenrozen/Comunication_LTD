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
    response = ul.create_user(parse_user(request))
    if type(response) == Response:
        response.headers['Access-Control-Allow-Origin'] = '*'
    else:
        response = jsonify(response)
    return response


@app.route('/user/getall', methods=['GET'])
def get_all_users():
    return jsonify(ul.get_all())


@app.route('/user/change_password/<user_id>', methods=['PUT'])
@jwt_required
def change_password(user_id):
    response = ul.change_password(user_id, request.get_json())
    if type(response) == Response:
        response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/user/login', methods=['POST'])
def login():
    response = ul.login(request.get_json())
    if type(response) == Response:
        return response
    else:
        return jsonify(UserPayload(id=response.id, email=response.email).serialize())


@app.route('/user/forgot_password', methods=['POST'])
def forgot_password():
    return ul.forgot_password(request.get_json())


@app.route('/user/forgot_change_password', methods=['POST'])
def forgot_change_password():
    response = ul.forgot_change_password(request.get_json())
    if type(response) == Response:
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


#####################################################
#################### CUSTOMER #######################
#####################################################

@app.route('/customer/addcustomer', methods=['POST'])
@jwt_required
def add_customer():
    customer = cl.create_customer(parse_customer(request))
    if customer:
        return jsonify(CustomerPayload(id=customer.id, customer_name=customer.customer_name).serialize())
    else:
        return Response(status=409, response="Customer already exist")


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
