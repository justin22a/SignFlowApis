from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from SignFlowProject.app.mock_database.mock_database import check_auth, insert_auth, delete_auth_by_username, \
    read_auth_by_username

# Creating a blueprint for authentication
auth = Blueprint('auth', __name__)


@auth.route('/test_auth', methods=['GET', 'POST'])
def test_auth():
    print("test auth is working wooshooo")
    return jsonify(message="Test auth is working now"), 200

@auth.route('/delete_user_auth', methods=['DELETE'])
def delete_user_auth():
    user_to_delete = request.json.get('username')
    password = request.json.get('password')

    if not check_auth(user_to_delete , password):
        return jsonify(message="Invalid username or password"), 401

    delete_auth_by_username(user_to_delete)

    return jsonify(message="User deleted successfully"), 200

@auth.route('/login', methods=['POST'])
def login():

    # below is for actual http requests
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not check_auth(username, password):  # Assume this function exists and checks the database
        return jsonify({"msg": "Invalid credentials"}), 401

    # for actual http
    # Retrieve the user's ID from the database based on the username
    user = read_auth_by_username(username)  # A function to fetch user details from the DB
    user_id = user[0]  # Replace with the correct field name

    # Use user_id as the identity in the token
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 200



@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # check if either are null
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if check_auth(username, password):  # This checks if user exists
        return jsonify({"msg": "User already exists"}), 409

    # Insert new user into the database
    insert_auth(username, password)


    return jsonify({"msg": "User registered successfully"}), 201
