import os
from dotenv import load_dotenv
from pathlib import Path

environment = os.environ.get('PROD_ENV', 'prod')
env_path = Path('.') / f'.env.{environment}'

load_dotenv(dotenv_path=env_path)

CHANGE_FORM_URL = os.getenv('CHANGE_FORM_URL')
GET_INFO_URL = os.getenv('GET_INFO_URL')
TOKEN_ENTREPRENEUR1 = os.getenv('TOKEN_ENTREPRENEUR1')
TOKEN_ENTREPRENEUR2 = os.getenv('TOKEN_ENTREPRENEUR2')
TOKEN_ENTREPRENEUR3 = os.getenv('TOKEN_ENTREPRENEUR3')
TOKEN_ENTREPRENEUR4 = os.getenv('TOKEN_ENTREPRENEUR4')
TOKEN_PHYSICAL1 = os.getenv('TOKEN_PHYSICAL1')
TOKEN_PHYSICAL2 = os.getenv('TOKEN_PHYSICAL2')
TOKEN_JUDICAL1 = os.getenv('TOKEN_JUDICAL1')
TOKEN_JUDICAL2 = os.getenv('TOKEN_JUDICAL2')
TOKEN_JUDICAL3 = os.getenv('TOKEN_JUDICAL3')
