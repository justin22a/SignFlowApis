import sqlite3

def get_db_connection(db_path='test.db'):
    """ Create a new database connection """
    return sqlite3.connect(db_path, check_same_thread=False)

def create_tables():
    conn = get_db_connection()
    print("Creating tables...")
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_requests (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES auth (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                wallet_address TEXT NOT NULL,
                wallet_private_key TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES auth (id)
            )
        ''')
        conn.commit()
    finally:
        conn.close()

def print_all_tables():
    conn = get_db_connection()
    print("Printing all tables...")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            print(f"Contents of the table {table_name[0]}:")
            cursor.execute(f"SELECT * FROM {table_name[0]}")
            columns = [description[0] for description in cursor.description]
            print("\t" + ", ".join(columns))  # show the headers
            rows = cursor.fetchall()
            for row in rows:
                print("\t" + ", ".join(map(str, row)))
            print()
    finally:
        conn.close()

def insert_auth(username, password):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO auth (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the newly created user
    finally:
        conn.close()

def read_auth_by_id(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auth WHERE id=?', (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def read_auth_by_username(username):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auth WHERE username=?', (username,))
        return cursor.fetchone()
    finally:
        conn.close()

def delete_auth(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM auth WHERE id=?', (user_id,))
        conn.commit()
    finally:
        conn.close()

def check_auth(username, password):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auth WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        return result is not None
    finally:
        conn.close()

def insert_payment_request(user_id, amount, currency):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO payment_requests (user_id, amount, currency) VALUES (?, ?, ?)', (user_id, amount, currency))
        conn.commit()
    finally:
        conn.close()

def read_payment_request(request_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payment_requests WHERE id=?', (request_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def delete_payment_request(request_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM payment_requests WHERE id=?', (request_id,))
        conn.commit()
    finally:
        conn.close()

def insert_wallet(user_id, wallet_address, wallet_private_key):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO wallets (user_id, wallet_address, wallet_private_key) 
            VALUES (?, ?, ?)
        ''', (user_id, wallet_address, wallet_private_key))
        conn.commit()
    finally:
        conn.close()
