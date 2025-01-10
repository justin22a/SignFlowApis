# importing all functions from each api
import time

from PayliumProject.app.apis.auth import * # login and protected

from PayliumProject.app.apis.conversion import *
from PayliumProject.app.apis.payment_request import * # create_payment_request and process_payment_request
from PayliumProject.app.apis.payment_verification import *
from PayliumProject.app.apis.settlement import *

# importing all functions from the mock_database CURRENTLY two tables see mock db for more
from PayliumProject.app.mock_database import * # create_connection, create_table, insert read delete variations
from PayliumProject.app.mock_database.mock_database import create_connection, create_tables, \
    print_all_tables, read_auth_by_username, read_auth_by_id
from flask import request

# we need to construct our database
conn = create_connection()
# initialize auth and payment request tables
create_tables(conn)

# NOTE: For now we are not testing actual HTTP requests, a failed attempt is as seen below

# with app.app_context():
#     with app.test_client() as client:
#         client.post('/register', json={'username': "ian", 'password': "vic"})
#         response = client.post('/login', json={'username': "ian", 'password': "vic"})
#         print(response.get_data(as_text=True))

print(register(conn, "ian", "vic"))
print(login(conn, "ian" , "vic")) # should succeed
print(login(conn, "justin" , "wii")) # should fail





