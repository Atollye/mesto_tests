import pytest
import requests
from api_helpers.const_and_func import SERVER_ADDRESS, check_response

def test_get_users_valid_values(client):
    client.url += '/users'
    # generate_custom_users()
    resp = client.GET()
    check_response(resp.status_code, 200, resp.text)
    print(resp.text)
    assert len(resp.json()) == 1 

    # and assert resp.json() == empty_result_template, resp.text

