import pytest
import requests
from data.const_and_func import SERVER_ADDRESS, check_response


def test_signup_with_minimal_correct_data(clear_users_from_mongo):
    url = f'http://{SERVER_ADDRESS}:3003/signup'
    headers = {
        "Origin": "http://{SERVER_ADDRESS}:3003",
        "Content-Type": "application/json"
    }
    payload = {"email":"user1@user1.com", "password":"testpasswd"
    }
    resp = requests.post(url, headers = headers, json=payload)
    check_response(resp.status_code, 201)
    mail = resp.json().get("email")
    assert mail == "user1@user1.com", "Signup doesn't work"


