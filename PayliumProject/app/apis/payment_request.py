# Purpose: Handles the creation and submission of payment requests. When a user or a system wants to initiate a payment using stablecoins, this API processes that request by validating input data, creating a record of the payment request, and possibly initiating the transaction process.
#
# Key Functions:
#
# Validate payment request data
# Record payment requests in the database
# Initiate payment processing (may interact with external payment gateways or blockchain networks)

from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from PayliumProject.app.mock_database.mock_database import insert_payment_request

payment = Blueprint('payment', __name__)

@payment.route('/make_request', methods=['POST'])
@jwt_required()  # Ensure that only authenticated users can make a payment request
def create_payment_request():
    try:
        data = request.get_json()
        amount = data['amount']
        currency = data['currency']
        user_id = get_jwt_identity()  # assuming that the JWT token includes user identity
        print(f"user_id from JWT: {user_id}")
        status = 'PENDING'

        # make sure that there exists valid parameters
        if not amount or not currency:
            return jsonify({"error": "Invalid data provided"}), 400
        # add payment request to DB
        insert_payment_request(user_id, amount, currency, status)
        # Logic to handle the creation of the payment request
        # This could involve saving the request to a database and/or initiating a transaction process
        # payment_id = process_payment_request(user_id, amount, currency)

        return jsonify({"message": "Payment request created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_payment_request(user_id, amount, currency):
    # HERE we might want to consider saving the request in a database and initiating the payment
        # do we use a message queue to preserve an ordering of requests
    # For example, save to a database
    # Return a unique payment ID or transaction ID
    return "unique_payment_id_12345"




# Example of a send below to the endpoint
# fetch('http://yourserver.com/payment/make_request', {
#     method: 'POST',
#     headers: {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer your_jwt_token_here' // If authentication is required
#     },
#     body: JSON.stringify({
#         amount: 100,
#         currency: 'USDC'
#     })
# })
# .then(response => response.json())
# .then(data => console.log(data))
# .catch(error => console.error('Error:', error));
