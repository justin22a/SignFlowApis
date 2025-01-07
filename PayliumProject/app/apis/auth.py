from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Validate username and password against our database WE DONT HAVE ONE
    if username != 'admin' or password != 'password':
        return jsonify({"msg": "Bad username or password"}), 401

    # Create a new token with the user id inside
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
