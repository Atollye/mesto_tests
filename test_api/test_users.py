import logging

import requests
import pytest

from api_helpers.helper_functions import check_response, wait_while
from api_helpers.wrapper import MainWrapper


@pytest.fixture
def generate_several_users(clear_users_from_mongo, base_url):
    url = base_url + '/signup'
    users = [
        {"email":"user_one@user.com", "password":"password"},
        {"email":"user_two@user.com", "password":"password"}   
    ]
    headers = {"Content-Type": "application/json"}
    user_ids = []
    for user in users:
        resp = requests.post(url, headers=headers, json=user)
        check_response(
            resp.status_code, 201, resp_text="Невозможно создать пользователя"
        )
        logging.info(f"User with {user} is created")
        user_ids.append(resp.json()["_id"])
    return user_ids

@pytest.fixture
def client_as_user_one(base_url):
    cl = MainWrapper()
    cl.base_url = base_url
    cl.url =  cl.base_url +'/signin'
    cl.data = {"email":"user_one@user.com", "password":"password"}
    resp = cl.POST()
    check_response(resp.status_code, 200, resp_text=resp.text)
    token = resp.json().get("token")
    cl.headers["Cookie"] = f"jwt={token}; path=/; HttpOnly"
    return cl

class TestGetUsers():
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

    def test_user_by_id(client, generate_several_users, client_as_user_one):
        cl = client_as_user_one
        user_id = generate_several_users[0]
        cl.url = f'{cl.base_url}/users/'
        cl.id(user_id)
        resp = cl.GET()
        check_response(resp.status_code, 200)
        print(resp.json()["_id"])
        assert resp.json()["_id"] == user_id, "It's impossible to get users by id"
        

@pytest.mark.patch_me
class TestPatchUsers():
    def test_patch_current_user(self, client):
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
        for k, v in updates.items(  ):
            assert resp.get(k) == v, "The user is patched incorrectly"


# client.users_me метод, который прибавляет к  client.base_url '/users/me' 
# в отдельной ветке


    def test_patch_current_user_empty_param(self):
        updates = {"name":"","about":""}
        assert True

