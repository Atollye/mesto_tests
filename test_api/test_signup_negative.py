import pytest
import requests

from api_helpers.wrapper import MainWrapper
from api_helpers.const_and_func import check_response

USER_FIELDS = {
    "name":"Жак-Ив Кусто",
    "about":"Исследователь",
    "avatar":"https://pictures.s3.yandex.net/resources/jacques-cousteau_1604399756.png"
}


@pytest.fixture
def signup_client(base_url):
    cl = MainWrapper()
    cl.url = base_url +'/signup'
    return cl


class TestSignupNegativeVals():
    @pytest.mark.xfail(reason="Here is a registration bug")
    def test_cannot_signup_with_existing_username(self, basic_signup, signup_client):
        signup_client.data = {"email": "user@user.com", "password":"somepassword"}
        resp  = signup_client.POST()
        assert resp.status_code == 400, (
            "User with an existing email can be reqistrated"
        )

    def test_signup_without_required_field_email(self, signup_client):
        signup_client.data = {"name":"James Cook", "password":"testpassword"}
        resp  = signup_client.POST()
        assert resp.status_code = 400
        returned_err = resp.json()["validation"]["body"]["message"]
        assert  returned_err == '"email" is required'



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
