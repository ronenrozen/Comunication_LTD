from comunication_ltd import app
import requests
from flask import request, jsonify, Response
from comunication_ltd.logic.user_boundary import parse_user, UserPayload
import comunication_ltd.logic.user_logic as ul
from comunication_ltd.logic.customer_bounary import parse_customer, CustomerPayload
import comunication_ltd.logic.customer_logic as cl


@app.route('/user/adduser', methods=['POST'])
def add_user():
    user = ul.create_user(parse_user(request))
    if user:
        return jsonify(UserPayload(id=user.id, username=user.username).serialize())
    else:
        return Response(status=409, response="User already exist")


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


@app.route('/user/update/<user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    is_updated = ul.update_user_by_id(user_id, request.get_json())
    if is_updated:
        return Response(status=200)
    else:
        return Response(status=500)


@app.route('/user/login', methods=['POST'])
def login():
    is_auth, user = ul.login(request.get_json())
    if is_auth:
        user_payload = jsonify(
            UserPayload(id=user.id, mail=user.mail, username=user.username).serialize())
        # user_payload["access_token"] = create_access_token(identity=user.username)
        # user_payload["refresh_token"] = create_refresh_token(identity=user.username)
        return user_payload
    else:
        return Response(status=500)


@app.route('/customer/addcustomer', methods=['POST'])
def add_customer():
    customer = cl.create_customer(parse_customer(request))
    if customer:
        return jsonify(CustomerPayload(id=customer.id, customer_name=customer.customer_name).serialize())
    else:
        return Response(status=409, response="User already exist")


@app.route('/user/forgot_password', methods=['POST'])
def forgot_password():
    return ul.forgot_password(request.get_json())


@app.route('/customer/getall', methods=['GET'])
def get_all_customers():
    customers = cl.get_all()

# @app.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     ''' refresh token endpoint '''
#     current_user = get_jwt_identity()
#     ret = {
#             'token': create_access_token(identity=current_user)
#     }
#     return jsonify({'ok': True, 'data': ret}), 200
