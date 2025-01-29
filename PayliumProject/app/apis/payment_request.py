# Purpose: Handles the creation and submission of payment requests. When a user or a system wants to initiate a payment using stablecoins, this API processes that request by validating input data, creating a record of the payment request, and possibly initiating the transaction process.
#
# Key Functions:
#
# Validate payment request data
# Record payment requests in the database
# Initiate payment processing (may interact with external payment gateways or blockchain networks)

from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from PayliumProject.app.mock_database.mock_database import insert_payment_request, read_auth_by_username, \
    get_user_id_by_username, delete_payment_request_by_id

payment = Blueprint('payment', __name__)

@payment.route('/make_request', methods=['POST'])
# @jwt_required()  # Ensure that only authenticated users can make a payment request
def create_payment_request():
    try:
        data = request.get_json()
        amount = data['amount']
        currency = data['currency']
        receiver_username = data['receiver']
        sender_username = data['sender']
        status = 'PENDING'
        if sender_username == receiver_username:
            return jsonify({"error" : "Cannot send to self"}) , 401
        # Validate sender and receiver existence in the database
        sender_id = get_user_id_by_username(sender_username)
        if sender_id is None:
            return jsonify({"error": f"User {sender_username} does not exist, this is not a valid sender"}), 401

        receiver_id = get_user_id_by_username(receiver_username)
        if receiver_id is None:
            return jsonify({"error": f"User {receiver_username} does not exist, cannot send to them"}), 401

        # Validate that the required parameters are provided
        if not amount or not currency:
            return jsonify({"error": "Invalid data provided"}), 400

        # Add the payment request to the database
        insert_payment_request(sender_id, receiver_id, amount, currency, status)

        return jsonify({"message": "Payment request created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@payment.route('/delete_request/', methods=['DELETE'])
# @jwt_required()  # Uncomment this to enable JWT authentication
def delete_payment_request():
    try:
        data = request.get_json()
        request_id = data['request_id']
        success = delete_payment_request_by_id(request_id)
        if not success:
            return jsonify({'error': 'Payment request not found or already deleted'}), 404
        return jsonify({'message': 'Payment request deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500





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
