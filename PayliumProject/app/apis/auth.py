from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

from PayliumProject.app.mock_database.mock_database import check_auth, insert_auth

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login(conn, username, password):

    # below is for actual http requests
    # username = request.json.get('username', None)
    # password = request.json.get('password', None)

    if not check_auth(conn, username, password):  # Assume this function exists and checks the database
        #return jsonify({"msg": "Invalid credentials"}), 401
        return False

    # for actual http
    # access_token = create_access_token(identity=username)
    # return jsonify(access_token=access_token)
    # return jsonify({"msg": "Successful login"}), 200

    return True


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/register', methods=['POST'])
def register(conn, username, password):
    fake_user = username
    fake_password = password
    # username = request.json.get('username', None)
    # password = request.json.get('password', None)
    # Check if username or password is missing
    # if not username or not password:
    #     return jsonify({"msg": "Missing username or password"}), 400
    # if check_auth(conn, username, password):
    #     return jsonify({"msg": "User already exists"}), 409

    # Insert new user into the database
    insert_auth(conn, {'username': fake_user, 'password': fake_password})

    return True # jsonify({"msg": "User registered successfully"}) , 201

