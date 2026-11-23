import os
import uuid

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

ERROR_MESSAGES = {
    400: "Недостаточно данных для входа",
    404: "Учетная запись не найдена",
}


class TestCourierLogin:

    @pytest.mark.parametrize(
        "login_type, password_type, expected_status",
        [
            ("valid", "valid", 200),
            ("missing", "valid", 400),
            ("valid", "missing", 400),
            ("invalid", "invalid", 404),
        ],
    )
    def test_courier_login(
        self,
        courier,
        login_type,
        password_type,
        expected_status,
    ):
        logins = {
            "valid": courier["login"],
            "missing": "",
            "invalid": f"no_user_{uuid.uuid4().hex[:8]}",
        }
        passwords = {
            "valid": courier["password"],
            "missing": "",
            "invalid": "wrong_password",
        }

        login = logins[login_type]
        password = passwords[password_type]

        payload = {
            "login": login,
            "password": password,
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            json=payload,
        )

        assert response.status_code == expected_status

        if expected_status == 200:
            assert "id" in response.json()
        else:
            assert response.json()["message"] == ERROR_MESSAGES[expected_status]