import requests
import pytest
from pymongo import MongoClient

from api_helpers.const_and_func import SERVER_ADDRESS, check_response
from api_helpers.wrapper import MainWrapper


@pytest.fixture
def get_users_from_mongo():
    client = MongoClient(f'mongodb://{SERVER_ADDRESS}', 27017)
    db = client.mestodb
    collection = db["users"]
    users= collection.find()
    print("\n")
    for user in users:
        print(user)


@pytest.fixture
def clear_users_from_mongo():
    client = MongoClient(f'mongodb://{SERVER_ADDRESS}', 27017)
    db = client.mestodb
    collection = db["users"]
    collection.delete_many({})
    print("\n")
    user = collection.find_one()
    if user is None:
        print("Setup: all users are deleted")
    else:
        print("Setup is not sucessful: not all users are deleted")


@pytest.fixture
def client(clear_users_from_mongo):
    cl = MainWrapper()
    url = cl.url +'/signup'
    cl.headers = {"Content-Type": "application/json"}
    cl.data = {"email":"user@user.com", "password":"password"
    }
    resp = requests.post(url, headers = cl.headers, json=cl.data)
    check_response(resp.status_code, 201, resp_text=resp.text)
    url = cl.url +'/signin'
    resp = requests.post(url, headers = cl.headers, json=cl.data)
    token = resp.json().get("token")
    cl.headers["Cookie"] = f"jwt={token}; path=/; HttpOnly"
    cl.token = token
    return cl

@pytest.fixture
def generate_custom_users(client):
    print("stub")