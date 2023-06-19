import pytest
import requests

from helpers import JSON_SCHEMA_PATH
from helpers import base_helpers
from config import TOKEN_ENTREPRENEUR1, TOKEN_ENTREPRENEUR2, TOKEN_ENTREPRENEUR3, TOKEN_ENTREPRENEUR4
from helpers.error_text import incorrect_entrepreneur_type, customer_already_have_type


class Test200:
    tokens = [
        TOKEN_ENTREPRENEUR1,
        TOKEN_ENTREPRENEUR2,
        TOKEN_ENTREPRENEUR3,
    ]

    @pytest.mark.parametrize(
        'type_, sign_type, power_of_attorney, token',
        [
            (2, 1, True, tokens[0]),
            (2, 1, False, tokens[1]),
            (2, 2, False, tokens[2]),
        ],
        ids=[
            'ENTREPRENEUR_PAPER_TRUE',
            'ENTREPRENEUR_PAPER_FALSE',
            'ENTREPRENEUR_GOS_FALSE',
        ],
    )
    def test_correct_entrepreneur_type(self, type_, sign_type, power_of_attorney, token):
        payload = {"type": type_, "sign_type": sign_type, "power_of_attorney": power_of_attorney}
        response = base_helpers.change_legal_form(token, payload)
        assert response.status_code == 200
        response_get_info = base_helpers.getinfo(token)
        assert response_get_info['type'] == type_
        assert response_get_info['sign_type'] == sign_type
        assert response_get_info['power_of_attorney'] == power_of_attorney
        base_helpers.assert_valid_schema(response_get_info, JSON_SCHEMA_PATH)


class Test400:

    def test_incorrect_entrepreneur_type(self):
        token = TOKEN_ENTREPRENEUR4
        payload = {"type": 2, "sign_type": 1, "power_of_attorney": True}
        response = base_helpers.change_legal_form(token, payload)
        assert response.status_code == 400
        assert response.json()[
                   "error"] == incorrect_entrepreneur_type

    def test_second_change_entrepreneur_type(self):
        token = TOKEN_ENTREPRENEUR1
        payload = {"type": 2, "sign_type": 1, "power_of_attorney": True}
        response = base_helpers.change_legal_form(token, payload)
        assert response.status_code == 400
        assert response.json()[
                   "error"] == customer_already_have_type
