import pytest
import requests
from api_helpers.const_and_func import BASE_URL, check_response


def test_signup_with_minimal_correct_data(clear_users_from_mongo):
    url = f'http://{BASE_URL}:3003/signup'
    headers = {
        "Content-Type": "application/json"
    }
    payload = {"email":"user1@user1.com", "password":"testpasswd"
    }
    resp = requests.post(url, headers = headers, json=payload)
    check_response(resp.status_code, 201)
    mail = resp.json().get("email")
    assert mail == "user1@user1.com", "Signup doesn't work"


