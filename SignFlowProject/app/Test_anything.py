from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from SignFlowProject.app.mock_database.mock_database import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Set this to your actual secret key
app.config["JWT_VERIFY_SUB"]=False
jwt = JWTManager(app)

# Import and register the auth blueprint
from SignFlowProject.app.apis.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from SignFlowProject.app.apis.user_data import user_data as user_data_blueprint
app.register_blueprint(user_data_blueprint, url_prefix='/user_data')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        return jsonify(data), 200
    else:
        return jsonify(message="Welcome to the home page!"), 200



if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
