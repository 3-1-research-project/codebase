import os
import json
import base64
import psycopg2
import requests

from helpers.postgres_helper import DATABASE_URL, clean_database
from helpers.test_helper import BASE_URL

API_URL = f"{BASE_URL}/api"

USERNAME = "simulator"
PWD = "super_safe!"
CREDENTIALS = ":".join([USERNAME, PWD]).encode("ascii")
ENCODED_CREDENTIALS = base64.b64encode(CREDENTIALS).decode()
HEADERS = {
    "Connection": "close",
    "Content-Type": "application/json",
    f"Authorization": f"Basic {ENCODED_CREDENTIALS}",
}


def create_new_session():
    session = requests.Session()
    session.headers.update(
        {
            "Connection": "close",
            "Content-Type": "application/json",
            "Authorization": f"Basic {ENCODED_CREDENTIALS}",
        }
    )
    return session


def verify_database_is_clean():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            for table in ["users", "messages", "followers"]:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                assert cur.fetchone()[0] == 0, f"Table {table} is not empty!"


def test_register():
    clean_database()
    session = create_new_session()
    username = "aa"
    email = "a@a.a"
    pwd = "a"
    data = {"username": username, "email": email, "pwd": pwd}
    params = {"latest": 1}
    response = session.post(f"{API_URL}/register", data=json.dumps(data), params=params)
    assert response.ok
    # TODO: add another assertion that it is really there

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 1


def test_register_b():
    session = create_new_session()
    username = "bb"
    email = "b@b.b"
    pwd = "b"
    data = {"username": username, "email": email, "pwd": pwd}
    params = {"latest": 5}
    response = session.post(f"{API_URL}/register", data=json.dumps(data), params=params)
    assert response.ok
    # TODO: add another assertion that it is really there

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 5


def test_register_c():
    session = create_new_session()
    username = "cc"
    email = "c@c.c"
    pwd = "c"
    data = {"username": username, "email": email, "pwd": pwd}
    params = {"latest": 6}
    response = session.post(f"{API_URL}/register", data=json.dumps(data), params=params)
    assert response.ok

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 6


def test_latest():
    session = create_new_session()
    # post something to update LATEST
    url = f"{API_URL}/register"
    data = {"username": "test", "email": "test@test", "pwd": "foo"}
    params = {"latest": 1337}
    response = session.post(url, data=json.dumps(data), params=params)
    assert response.ok

    # verify that latest was updated
    url = f"{API_URL}/latest"
    response = session.get(url)
    assert response.ok
    assert response.json()["latest"] == 1337


def test_create_msg():
    session = create_new_session()
    username = "aa"
    data = {"content": "Blub!"}
    url = f"{API_URL}/msgs/{username}"
    params = {"latest": 2}
    response = session.post(url, data=json.dumps(data), params=params)
    assert response.ok

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 2


def test_get_latest_user_msgs():
    session = create_new_session()
    username = "aa"
    query = {"no": 20, "latest": 3}
    url = f"{API_URL}/msgs/{username}"
    response = session.get(url, params=query)
    assert response.status_code == 200

    got_it_earlier = False
    for msg in response.json():
        if msg["content"] == "Blub!" and msg["user"] == username:
            got_it_earlier = True

    assert got_it_earlier

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 3


def test_get_latest_msgs():
    session = create_new_session()
    username = "aa"
    query = {"no": 20, "latest": 4}
    url = f"{API_URL}/msgs"
    response = session.get(url, params=query)
    assert response.status_code == 200

    got_it_earlier = False
    for msg in response.json():
        if msg["content"] == "Blub!" and msg["user"] == username:
            got_it_earlier = True

    assert got_it_earlier

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 4


def test_follow_user():
    session = create_new_session()
    username = "aa"
    url = f"{API_URL}/fllws/{username}"
    data = {"follow": "bb"}
    params = {"latest": 7}
    response = session.post(url, data=json.dumps(data), params=params)
    assert response.ok

    data = {"follow": "cc"}
    params = {"latest": 8}
    response = session.post(url, data=json.dumps(data), params=params)
    assert response.ok

    query = {"no": 20, "latest": 9}
    response = session.get(url, params=query)
    assert response.ok

    json_data = response.json()
    assert "bb" in json_data["follows"]
    assert "cc" in json_data["follows"]

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 9


def test_a_unfollows_b():
    session = create_new_session()
    username = "aa"
    url = f"{API_URL}/fllws/{username}"

    #  first send unfollow command
    data = {"unfollow": "bb"}
    params = {"latest": 10}
    response = session.post(url, data=json.dumps(data), params=params)
    assert response.ok

    # then verify that b is no longer in follows list
    query = {"no": 20, "latest": 11}
    response = session.get(url, params=query)
    assert response.ok
    assert "bb" not in response.json()["follows"]

    # verify that latest was updated
    response = session.get(f"{API_URL}/latest")
    assert response.json()["latest"] == 11


def test_cleaning_the_db():
    session = create_new_session()
    username = "aa"
    query = {"no": 20, "latest": 3}
    url = f"{API_URL}/msgs/{username}"
    response = session.get(url, params=query)
    assert response.status_code == 200

    clean_database()
    verify_database_is_clean()

    response = session.get(url, params=query)
    assert response.status_code == 404
