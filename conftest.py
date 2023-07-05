import requests
import pytest
from pymongo import MongoClient

from api_helpers.const_and_func import BASE_URL, SERVER_ADDRESS, check_response
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
    user = collection.find_one()
    if user is None:
        print("\nSetup: all users are deleted")
    else:
        print("\nSetup is not sucessful: not all users are deleted")


@pytest.fixture
def signup(clear_users_from_mongo):
    url = BASE_URL +'/signup'
    headers = {"Content-Type": "application/json"}
    payload = {"email":"user@user.com", "password":"password"}
    resp = requests.post(url, headers = headers, json=payload)
    check_response(resp.status_code, 201, resp.text)
    mail = resp.json().get("email")
    assert mail == "user@user.com", "Setup: signup doesn't work"


@pytest.fixture
def client(signup):
    cl = MainWrapper()
    cl.url =  cl.base_url +'/signin'
    cl.data = {"email":"user@user.com", "password":"password"
    }
    resp = cl.POST()
    check_response(resp.status_code, 200, resp_text=resp.text)
    token = resp.json().get("token")
    cl.headers["Cookie"] = f"jwt={token}; path=/; HttpOnly"
    cl.token = token
    return cl





