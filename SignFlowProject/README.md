Engineers:
Ian Kelsey, Justin Adam, Victor Polisetty

Introduction:
This project will contain all the infrastructure for SMBs to accept and convert stablecoin payments. We intend to integrate with PoS systems like Square.

Structure Overview:
The structure is mostly divided into /app and /tests. /app will have a few directories in /apis, /models, /services, and /utils. /apis will contain the main apis for this infrastructure, and /services will contain the business logic for the files inside /apis. The intended relationship is as follows.
- auth.py uses authentication_service.py
- conversion.py uses conversion_service.py
- settlement.py, payment_request.py, and payment_verification.py all use payment_service.py

## Usage
- To install required packages (in SignFlowProject): `pip install -r requirements.txt`
- To start virtual env (in root): `source venv/bin/activate`
- To hit local endpoints: http://127.0.0.1:5000/
- To create mock DB run: `Test_anything.py`
