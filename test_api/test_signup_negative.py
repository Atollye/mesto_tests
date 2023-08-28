import pytest
import requests


INVALID_JSON = """{"email":"user2@user2.com","password":"testpasswd}}"""


class TestSignupNegativeVals():

    @pytest.mark.xfail(reason="Here is a registration bug")
    @pytest.mark.negative
    def test_existing_user_cannot_signup_twice(
        self, clear_users_from_mongo, signup_a_user, cl
    ):
        cl.set_path('/signup')
        cl.data = {"email": "user@user.com", "password":"password"}
        resp  = cl.POST()
        assert resp.status_code == 400, (
            "User with an existing email can be reqistrated"
        )

    @pytest.mark.negative
    def test_signup_without_required_field_email(self, cl):
        cl.set_path('/signup')
        cl.data = {"name":"James Cook", "password":"password"}
        resp  = cl.POST()
        assert resp.status_code == 400
        returned_err = resp.json()["validation"]["body"]["message"]
        assert  returned_err == '"email" is required'

    @pytest.mark.negative
    def test_signup_with_too_short_password(self, cl):
        cl.set_path('/signup')
        cl.data = {"email": "user@user.com", "password": "pass"}
        resp = cl.POST()
        assert resp.status_code == 400
        returned_err = resp.json()["validation"]["body"]["message"]
        assert (
            returned_err == '"password" length must be at least 8 characters long'
        )

    @pytest.mark.negative
    def test_signup_with_invalid_json(self, cl):
        cl.set_path('/signup')
        cl.headers = {
            "Content-Type": "application/json"
        }
        payload = INVALID_JSON
        resp = requests.post(cl.url, headers=cl.headers, data=payload)
        assert resp.status_code == 400
        assert resp.json() == {'message': 'Unexpected end of JSON input'}, (
            "Wrong message text for invalid json input"
        )
