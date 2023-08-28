import pytest
from api_helpers.helper_functions import check_response


class TestSignup:
    @pytest.mark.parametrize("mail, expected_user_mail", [
        ("user@user.com", "user@user.com"),
        ("user.one.two@e-mail.com", "user.one.two@e-mail.com"),
        ("i-am-a_user33@mail33.cf", "i-am-a_user33@mail33.cf")
    ])
    def test_signup_with_valid_emails(
        self, clear_users_from_mongo, cl, mail, expected_user_mail
    ):
        cl.set_path('/signup')
        cl.data = {"email": mail, "password": "testpassword"}
        err_mssg = "Signup doesn't work"
        resp = cl.POST()
        check_response(resp.status_code, 201, err_mssg)
        mail = resp.json().get("email")
        assert mail == expected_user_mail, err_mssg

    @pytest.mark.parametrize("password", ["Iam33PassWo!!ord*", "abracadabra"])
    def test_signup_with_valid_passwords(
        self, clear_users_from_mongo, cl, password
    ):
        cl.set_path('/signup')
        cl.data = {"email": "user@user.com", "password": password}
        resp = cl.POST()
        check_response(resp.status_code, 201, "Signup doesn't work")
