from urllib import request

from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

from SignFlowProject.app.mock_database.mock_database import check_auth, read_auth_by_username, read_user_data, \
    upsert_user_data

user_data = Blueprint('user_data', __name__)


@user_data.route('/update_user_data', methods=['POST'])
def update():

    username = request.json.get('username', None)
    updated_data = request.json.get('data' , None)
    user = read_auth_by_username(username)
    if not user:
        return jsonify({"msg": "Invalid user"}), 401

    # for actual http
    # Retrieve the user's ID from the database based on the username
    user_id = user[0]  # Replace with the correct field name
    current_data = read_user_data(user_id)
    for key , value in updated_data.items():
        current_data[key] = value
    upsert_user_data(user_id, current_data)
    # Use user_id as the identity in the token
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 200

@user_data.route('/get_user_data', methods=['GET'])
def get_user_data():
    username = request.json.get('username', None)
    user = read_auth_by_username(username)
    if not user:
        return jsonify({"msg": "Invalid user"}), 401
    user_id = user[0]
    current_data = read_user_data(user_id)
    if not current_data:
        return jsonify({"msg": "No data found"}), 200