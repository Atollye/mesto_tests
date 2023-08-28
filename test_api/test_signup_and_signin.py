import pytest
import requests
from api_helpers.helper_functions import check_response
from api_helpers.wrapper import MainWrapper

@pytest.fixture
def non_auth_client(clear_users_from_mongo, base_url):
    cl = MainWrapper()
    cl.base_url = base_url
    return cl

@pytest.mark.parametrize("mail, expected_user_mail", [
        ("user@user.com", "user@user.com"), 
      ("user.one.two@e-mail.com", "user.one.two@e-mail.com"),
      ("i-am-a_user33@mail33.cf", "i-am-a_user33@mail33.cf")
])
def test_signup_with_valid_emails(non_auth_client, mail, expected_user_mail):
    non_auth_client.url = non_auth_client.base_url +'/signup'
    non_auth_client.data = {"email": mail, "password":"testpassword"}
    err_mssg = "Signup doesn't work"
    resp  = non_auth_client.POST()
    check_response(resp.status_code, 201, err_mssg)
    mail = resp.json().get("email")
    assert mail == expected_user_mail, err_mssg


@pytest.mark.parametrize("password", ["Iam33PassWo!!ord*", "abracadabra"])
def test_signup_with_valid_passwords(
    clear_users_from_mongo, non_auth_client, password
):
    non_auth_client.url = non_auth_client.base_url +'/signup'
    non_auth_client.data = {"email": "user@user.com", "password": password}
    resp  = non_auth_client.POST()
    check_response(resp.status_code, 201, "Signup doesn't work")



