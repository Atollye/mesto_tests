import logging
import requests
import pytest
from pymongo import MongoClient

from api_helpers.helper_functions import check_response
from api_helpers.wrapper import MainWrapper


def pytest_addoption(parser):
    parser.addoption("--ip", action="store", default="91.222.238.238")


@pytest.fixture
def ip(request):
    return request.config.getoption("--ip")


@pytest.fixture
def get_users_from_mongo(ip):
    client = MongoClient(f'mongodb://{ip}', 27017)
    db = client.mestodb
    collection = db["users"]
    users= collection.find()
    for user in users:
        print(user)


@pytest.fixture
def clear_users_from_mongo(ip):
    client = MongoClient(f'mongodb://{ip}', 27017)
    db = client.mestodb
    collection = db["users"]
    collection.delete_many({})
    user = collection.find_one()
    if user is None:
        logging.info("Setup: all users are deleted")
    else:
        logging.info("Setup: not all users are deleted")


@pytest.fixture
def get_base_url(ip):
    return f'http://{ip}:3003'


@pytest.fixture
def cl(get_base_url):
    cl = MainWrapper()
    cl.base_url = get_base_url
    return cl


@pytest.fixture
def signup_a_user(clear_users_from_mongo, get_base_url):
    url = f'{get_base_url}/signup'
    headers = {"Content-Type": "application/json"}
    payload = {"email":"user@user.com", "password":"password"}
    resp = requests.post(url, headers=headers, json=payload)
    check_response(resp.status_code, 201, resp.text)
    mail = resp.json().get("email")
    assert mail == "user@user.com", "Setup: signup doesn't work"


@pytest.fixture
def client(signup_a_user, cl):
    cl.set_path('/signin')
    cl.data = {
        "email":"user@user.com", "password":"password"
    }
    resp = cl.POST()
    check_response(resp.status_code, 200, resp_text=resp.text)
    logging.info(f"User with {cl.data} is created")
    token = resp.json().get("token")
    cl.headers["Cookie"] = f"jwt={token}; path=/; HttpOnly"
    return cl
