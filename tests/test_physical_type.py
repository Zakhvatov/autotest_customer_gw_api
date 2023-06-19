import pytest
import requests

from config import TOKEN_PHYSICAL1, TOKEN_PHYSICAL2
from helpers import base_helpers
from helpers import JSON_SCHEMA_PATH
from helpers.error_text import customer_physical_paper_true, customer_physical_paper_false, customer_physical_gos_true, \
    customer_already_have_type


class Test200:
    def test_correct_physical_type(self):
        token = TOKEN_PHYSICAL1
        payload = {"type": 1, "sign_type": 2, "power_of_attorney": False}
        response = base_helpers.change_Legal_Form(token, payload)
        response.raise_for_status()
        assert response.status_code == 200
        response_get_info = base_helpers.getinfo(token)
        assert response_get_info['type'] == 1
        assert response_get_info['sign_type'] == 2
        assert response_get_info['power_of_attorney'] == False
        base_helpers.assert_valid_schema(response_get_info, JSON_SCHEMA_PATH)


class Test400:
    token = TOKEN_PHYSICAL2

    @pytest.mark.parametrize('type_, sign_type, power_of_attorney',
                             [('CUSTOMER_TYPE_PHYSICAL', 'CUSTOMER_SIGN_TYPE_PAPER', True),
                              ('CUSTOMER_TYPE_PHYSICAL', 'CUSTOMER_SIGN_TYPE_PAPER', False),
                              ('CUSTOMER_TYPE_PHYSICAL', 'CUSTOMER_SIGN_TYPE_GOS', True)],
                             ids=['PHYSICAL_PAPER_TRUE', 'PHYSICAL_PAPER_FALSE', 'PHYSICAL_GOS_TRUE'])
    def test_incorrect_physical_type(self, type_, sign_type, power_of_attorney, token):
        payload = {"type": type_, "sign_type": sign_type, "power_of_attorney": power_of_attorney}
        response = base_helpers.change_legal_form(token, payload)
        assert response.status_code == 400
        if type == 'CUSTOMER_TYPE_PHYSICAL' and sign_type == 'CUSTOMER_SIGN_TYPE_PAPER' and power_of_attorney == True:
            assert response.json()[
                       "error"] == customer_physical_paper_true
        elif type == 'CUSTOMER_TYPE_PHYSICAL' and sign_type == 'CUSTOMER_SIGN_TYPE_PAPER' and power_of_attorney == False:
            assert response.json()[
                       "error"] == customer_physical_paper_false
        elif type == 'CUSTOMER_TYPE_PHYSICAL' and sign_type == 'CUSTOMER_SIGN_TYPE_GOS' and power_of_attorney == True:
            assert response.json()[
                       "error"] == customer_physical_gos_true

    def test_second_change_physical_type(self):
        token = TOKEN_PHYSICAL1
        payload = {"type": 1, "sign_type": 2, "power_of_attorney": False}
        response = base_helpers.change_legal_form(token, payload)
        assert response.status_code == 400
        assert response.json()[
                   "error"] == customer_already_have_type

