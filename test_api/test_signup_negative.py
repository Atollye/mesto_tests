import pytest
import requests

from api_helpers.wrapper import MainWrapper
from api_helpers.helper_functions import check_response

USER_FIELDS = {
    "name":"Жак-Ив Кусто",
    "about":"Исследователь",
    "avatar":"https://pictures.s3.yandex.net/resources/jacques-cousteau_1604399756.png"
}

INVALID_JSON = """{"email":"user2@user2.com","password":"testpasswd}}"""

@pytest.fixture
def signup_client(base_url):
    cl = MainWrapper()
    cl.url = base_url +'/signup'
    return cl


class TestSignupNegativeVals():


    @pytest.mark.xfail(reason="Here is a registration bug")
    @pytest.mark.signup_negative
    def test_cannot_signup_with_existing_username(self, basic_signup, signup_client):
        signup_client.data = {"email": "user@user.com", "password":"password"}
        resp  = signup_client.POST()
        assert resp.status_code == 400, (
            "User with an existing email can be reqistrated"
        )

    @pytest.mark.signup_negative
    def test_signup_without_required_field_email(self, signup_client):
        signup_client.data = {"name":"James Cook", "password":"password"}
        resp  = signup_client.POST()
        assert resp.status_code == 400
        returned_err = resp.json()["validation"]["body"]["message"]
        assert  returned_err == '"email" is required'

    @pytest.mark.signup_negative
    def test_signup_with_too_short_password(self, signup_client):
        signup_client.data = {"email": "user@user.com", "password":"pass"}
        resp  = signup_client.POST()
        assert resp.status_code == 400
        returned_err = resp.json()["validation"]["body"]["message"]
        assert  returned_err == '"password" length must be at least 8 characters long'

    @pytest.mark.signup_negative
    def test_signup_with_invalid_json(self, base_url):
        url = base_url + '/signup'
        headers = {
            "Content-Type": "application/json"
        }
        payload = INVALID_JSON
        resp = requests.post(url, headers=headers, data=payload)
        assert resp.status_code == 400
        assert resp.json() == {'message': 'Unexpected end of JSON input'}, (
            "Wrong message text for invalid input"
        )
