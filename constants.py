import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'
SYMBOL_PATH = os.getenv('SYMBOL_PATH')


# db
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PWD = os.getenv('PWD')
PORT = os.getenv('PORT')

PARAMS = {
    "host"      : str(HOST),
    "database"  : str(DATABASE),
    "user"      : str(USER),
    "password"  : str(PWD),
    "port"      : str(PORT),
}