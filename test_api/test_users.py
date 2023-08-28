import logging

import requests
import pytest

from api_helpers.helper_functions import check_response, wait_while


@pytest.fixture
def generate_several_users(clear_users_from_mongo, cl):
    cl.set_path('/signup')
    users = [
        {"email": "user_one@user.com", "password": "password"},
        {"email": "user_two@user.com", "password": "password"}
    ]
    headers = {"Content-Type": "application/json"}
    user_ids = []
    for user in users:
        resp = requests.post(cl.url, headers=headers, json=user)
        check_response(
            resp.status_code, 201, resp_text="Невозможно создать пользователя"
        )
        logging.info(f"User with {user} is created")
        user_ids.append(resp.json()["_id"])
    return user_ids


@pytest.fixture
def login_as_user_one(cl):
    cl.set_path('/signin')
    cl.data = {"email":"user_one@user.com", "password":"password"}
    resp = cl.POST()
    check_response(resp.status_code, 200, resp_text=resp.text)
    token = resp.json().get("token")
    cl.headers["Cookie"] = f"jwt={token}; path=/; HttpOnly"
    return cl


class TestGetUsers():
    def test_get_users_valid_values(self, client, generate_several_users):
        client.set_path("/users/")
        resp = client.GET()
        check_response(resp.status_code, 200, resp.text)
        users = resp.json()
        assert len(users) == 3
        assert all([
            users[0]["email"] == "user@user.com",
            users[1]["email"] == "user_one@user.com",
            users[2]["email"] == "user_two@user.com"
        ])

    def test_user_by_id(self, generate_several_users, login_as_user_one):
        cl = login_as_user_one
        user_id = generate_several_users[0]
        cl.set_path("/users/")
        cl.id(user_id)
        resp = cl.GET()
        check_response(resp.status_code, 200)
        assert resp.json()["_id"] == user_id, (
            "It's impossible to get users by id"
        )
        

@pytest.mark.patch_me
class TestPatchUsers():
    def test_patch_current_user(self, client):
        client.set_path("/users/me")
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

    def test_patch_user_empty_params(self):
        updates = {"name":"","about":""}
        assert True
