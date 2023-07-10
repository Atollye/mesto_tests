import logging

import requests
import pytest

from api_helpers.const_and_func import check_response, wait_while



@pytest.fixture
def generate_several_users(base_url):
    url = base_url + '/signup'
    users = [
        {"email":"user_one@user.com", "password":"password"},
        {"email":"user_two@user.com", "password":"password"}   
    ]
    headers = {"Content-Type": "application/json"}
    for user in users:
        resp = requests.post(url, headers=headers, json=user)
        check_response(
            resp.status_code, 201, resp_text="Невозможно создать пользователя"
        )
        logging.info(f"User with {user} is created")

@pytest.fixture
def get_users_from_mongo(ip):
    client = MongoClient(f'mongodb://{ip}', 27017)
    db = client.mestodb
    collection = db["users"]
    users= collection.find()
    for user in users:
        print(user)



def test_get_users_valid_values(client, generate_several_users):
    client.url = client.base_url +'/users'
    resp = client.GET()
    check_response(resp.status_code, 200, resp.text)
    users = resp.json()
    assert len(users) == 3
    assert all([
        users[0]["email"] == "user@user.com",
        users[1]["email"] == "user_one@user.com",
        users[2]["email"] == "user_two@user.com"
    ])

def test_get_user_by_id(client, generate_several_users):
    assert True

def test_get_current_user(client, generate_several_users):
    assert True


def test_patch_current_user(client):
    client.url = client.base_url +'/users/me'
    updates = {"name":"Васко де Гама","about":"Мореплаватель"}
    client.data = updates
    def patch_users():
        resp = client.PATCH()
        if resp.status_code == 200:
            return True
    is_patched = wait_while(patch_users)
    assert is_patched, "It's impossible to patch a user"
    resp = client.GET().json()
    for k, v in updates.items():
        assert resp.get(k) == v, "The user is patched incorrectly"

