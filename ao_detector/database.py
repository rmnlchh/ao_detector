import sqlite3


def init_db():
    conn = sqlite3.connect('missiles.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        phone_number TEXT NOT NULL);''')

    conn.commit()
    conn.close()


def is_user_authorized(user_id):
    conn = sqlite3.connect('missiles.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    user = cursor.fetchone()

    conn.close()

    return user is not None


def add_user(user_id, phone_number):
    conn = sqlite3.connect('missiles.db')
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO users (user_id, phone_number) VALUES ({user_id}, {phone_number})")

    conn.commit()
    conn.close()
