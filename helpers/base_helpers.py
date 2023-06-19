import json
import requests
import jsonschema
import os

url = os.environ.get('CHANGE_FORM_URL')
url_get_info = os.environ.get('GET_INFO_URL')


def change_legal_form(token, payload):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def assert_valid_schema(data, schema_file):
    with open(schema_file) as schema_file:
        schema = json.load(schema_file)
    return jsonschema.validate(data, schema)


def getinfo(token):
    headers = {'Content-type': 'application/json; charset=UTF-8',
               'Authorization': f'Bearer {token}'}
    response = requests.post(url_get_info, headers=headers)
    return response.json()
