import sqlite3

def create_connection():
    """ Create a database connection to a SQLite database """
    conn = sqlite3.connect(':memory:')  # use ':memory:' to use it in RAM, or 'example.db' to save in file
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    # Create auth table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Create payment_requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_requests (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES auth (id)
        )
    ''')
    conn.commit()

# Auth helpers
def insert_auth(conn, data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO auth (username, password) VALUES (?, ?)', (data['username'], data['password']))
    conn.commit()

def read_auth(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM auth WHERE id=?', (user_id,))
    return cursor.fetchone()

def delete_auth(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM auth WHERE id=?', (user_id,))
    conn.commit()

def check_auth(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    return result is not None

# Payment request helpers
def insert_payment_request(conn, data):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO payment_requests (user_id, amount, currency) VALUES (?, ?, ?)', (data['user_id'], data['amount'], data['currency']))
    conn.commit()

def read_payment_request(conn, request_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payment_requests WHERE id=?', (request_id,))
    return cursor.fetchone()

def delete_payment_request(conn, request_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM payment_requests WHERE id=?', (request_id,))
    conn.commit()
