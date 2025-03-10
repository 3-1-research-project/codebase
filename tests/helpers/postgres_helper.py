from collections import namedtuple
from datetime import datetime
import os
import string

import psycopg2

from helpers.test_helper import generate_random_email, generate_random_password, generate_random_username

DATABASE_URL = os.environ["DATABASE_URL"]

User = namedtuple('User', ['user_id', 'username', 'email', 'password'])

def fetch_postgres_query(query: string):
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

def execute_postgres_query(query: string):
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)

def create_user_using_psql() -> User:
    username = generate_random_username()
    email = generate_random_email()
    password = generate_random_password()

    execute_postgres_query(f"insert into users (username, email, pw_hash) values ('{username}', '{email}', '{password}')")
    user_id = fetch_postgres_query(f"select user_id from users where username = '{username}'")[0][0]
    
    return User(user_id=user_id, username=username, email=email, password=password)

def tweet_using_psql(user_id: int):
    execute_postgres_query(f"insert into messages (author_id, text, pub_date, flagged) values ({user_id}, '{generate_random_username()}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}', 0)")
    
def follow_user_using_psql(user_id: int, other_user_id: int):
    execute_postgres_query(f"insert into followers (who_id, whom_id) values ({user_id}, {other_user_id})")