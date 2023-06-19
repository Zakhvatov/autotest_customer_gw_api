import pytest

from config import TOKEN_JUDICAL2, TOKEN_JUDICAL1, TOKEN_JUDICAL3
from helpers import JSON_SCHEMA_PATH, base_helpers
from helpers.error_text import customer_juridical_gos_true, customer_juridical_gos_false, customer_already_have_type


class Test200:
    class Test200:
        tokens = [
            TOKEN_JUDICAL1,
            TOKEN_JUDICAL2
        ]

        @pytest.mark.parametrize(
            'type_, sign_type, power_of_attorney, token',
            [
                (3, 1, True, tokens[0]),
                (3, 1, False, tokens[1])

            ],
            ids=[
                'JUDICAL_PAPER_TRUE',
                'JUDICAL_PAPER_FALSE'
            ],)
        def test_correct_juridical_type(self, type_, sign_type, power_of_attorney, token):
            payload = {"type": type_, "sign_type": sign_type, "power_of_attorney": power_of_attorney}
            response = base_helpers.change_legal_form(token, payload)
            assert response.status_code == 200
            response_get_info = base_helpers.getinfo(token)
            assert response_get_info['type'] == type_
            assert response_get_info['sign_type'] == sign_type
            assert response_get_info['power_of_attorney'] == power_of_attorney
            base_helpers.assert_valid_schema(response_get_info, JSON_SCHEMA_PATH)

class Test400:
    token = TOKEN_JUDICAL3

    @pytest.mark.parametrize(
        'type_, sign_type, power_of_attorney',
        [
            (3, 2, True),
            (3, 2, False)

        ],
        ids=[
            'JUDICAL_GOS_TRUE',
            'JUDICAL_GOS_FALSE'
        ], )
    def test_incorrect_juridical_type(self, type_, sign_type, power_of_attorney, token):
        payload = {"type": type_, "sign_type": sign_type, "power_of_attorney": power_of_attorney}
        response = base_helpers.change_legal_form(token, payload)
        assert response.status_code == 400
        if type == 3 and sign_type == 2 and power_of_attorney == True:
            assert response.json()[
                       "error"] == customer_juridical_gos_true
        elif type == 3 and sign_type == 2 and power_of_attorney == False:
            assert response.json()[
                       "error"] == customer_juridical_gos_false

    def test_second_change_entrepreneur_type(self):
        token = TOKEN_JUDICAL1
        payload = {"type": 2, "sign_type": 1, "power_of_attorney": True}
        response = base_helpers.change_legal_form(token, payload)
        assert response.status_code == 400
        assert response.json()[
                   "error"] == customer_already_have_type
