import sqlite3
import json

def get_db_connection(db_path='test.db'):
    """ Create a new database connection """
    return sqlite3.connect(db_path, check_same_thread=False)

def create_tables():
    conn = get_db_connection()
    print("Creating tables...")
    try:
        cursor = conn.cursor()
        # Create auth table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Create user_data table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                user_id INTEGER,
                data TEXT,
                FOREIGN KEY(user_id) REFERENCES auth(id)
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

def read_user_data(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM user_data WHERE user_id=?', (user_id,))
        data = cursor.fetchone()
        return json.loads(data[0]) if data else None  # Convert JSON string back to Python dictionary
    finally:
        conn.close()

def upsert_user_data(user_id, data):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        json_data = json.dumps(data)  # Convert Python dictionary to JSON string
        # Use INSERT OR REPLACE to handle both new insertions and updates
        cursor.execute('''
            INSERT OR REPLACE INTO user_data (user_id, data)
            VALUES (?, ?)
        ''', (user_id, json_data))
        conn.commit()
    finally:
        conn.close()

def delete_user_data(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_data WHERE user_id=?', (user_id,))
        conn.commit()
    finally:
        conn.close()

# Example functions to interact with the authentication system

def delete_auth_by_username(username):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM auth WHERE username=?', (username,))
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]
            # Delete the user data associated with this user ID
            delete_user_data(user_id)
            # Then delete the user from the auth table
            cursor.execute('DELETE FROM auth WHERE id=?', (user_id,))
            conn.commit()
        else:
            print("No user found with that username.")
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


def read_auth_by_username(username):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auth WHERE username=?', (username,))
        return cursor.fetchone()
    finally:
        conn.close()