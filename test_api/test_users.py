import pytest
import requests
import logging
from api_helpers.const_and_func import BASE_URL, check_response, wait_while



@pytest.fixture
def generate_several_users():
    url = BASE_URL + '/signup'
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
def get_users_from_mongo():
    client = MongoClient(f'mongodb://{SERVER_ADDRESS}', 27017)
    db = client.mestodb
    collection = db["users"]
    users= collection.find()
    print("\n")
    for user in users:
        print(user)


def test_get_users_valid_values(client, generate_several_users):
    client.url = BASE_URL +'/users'
    resp = client.GET()
    check_response(resp.status_code, 200, resp.text)
    users = resp.json()
    assert len(users) == 3
    assert all([
        users[0]["email"] == "user@user.com",
        users[1]["email"] == "user_one@user.com",
        users[2]["email"] == "user_two@user.com"
    ])

def test_get_user_by_id(client, generate_more_users):
    pass

def test_get_current_user(client, generate_more_users):
    pass


def test_patch_current_user(client):
    client.url = BASE_URL +'/users/me'
    updates = {"name":"Васко де Гама","about":"Мореплаватель"}
    client.data = updates
    resp = client.PATCH()
    for k, v in updates.items():
        assert resp.json().get(k) == v
    print(client.headers)





   
   # 
    # assert result, "It's impossible to patch a user"
    # client.GET()
    # assert user_dict = returned_user_dict, "The user is patched incorrectly"
   
    
"""
def test_patch_current_user(client):
    client.path = "+= /users/me"
    def patch_users():
        resp = client.PATCH()
        if resp.status_code = 200:
            return True
    result = wait_while(patch_users)
    assert result, "It's impossible to patch a user"
    client.GET()
    assert user_dict = returned_user_dict, "The user is patched incorrectly"
"""