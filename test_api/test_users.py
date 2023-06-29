import pytest
import requests
from api_helpers.const_and_func import BASE_URL, check_response

def test_get_users_valid_values(client, generate_more_users):
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



