import psycopg2
import redis

from constant import *


rcache = redis.Redis(host='localhost', port=6379, db=0)


def get_connection():
    conn = psycopg2.connect(
        dbname=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    cursor = conn.cursor()
    return conn, cursor


def create_database():
    conn, cursor = get_connection()
    query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            birth_date DATE,
            photo_of_profile UUID,
            about VARCHAR(200),
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS group_messages (
            group_message_id SERIAL PRIMARY KEY,
            sender_id INTEGER REFERENCES users(user_id),
            date_sending TIMESTAMP,
            text_message TEXT
        );

        CREATE TABLE IF NOT EXISTS private_messages (
            private_message_id SERIAL PRIMARY KEY,
            sender_id INTEGER REFERENCES users(user_id),
            recipient_id INTEGER REFERENCES users(user_id),
            text_message TEXT,
            date_sending TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS friends (
            user_id INTEGER REFERENCES users(user_id),
            friend_id INTEGER REFERENCES users(user_id),
            PRIMARY KEY (user_id, friend_id)
        );

        CREATE TABLE IF NOT EXISTS notification (
            friend_id INTEGER REFERENCES users(user_id),
            user_id INTEGER REFERENCES users(user_id),
            accept BOOLEAN
        );    
    """
    cursor.execute(query)
    conn.commit()
create_database()
    