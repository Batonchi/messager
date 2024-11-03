import psycopg2
from constant import *


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

    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        birth_date DATE,
        photo_of_profile UUID,
        about VARCHAR(200),
        password text
    );


    
    """
    cursor.execute(query)
    conn.commit()
    