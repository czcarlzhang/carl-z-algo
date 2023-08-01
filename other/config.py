import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()

# authentication and connection details
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# get history of aappl

aapl = api.get_barset('AAPL', 'day')

print(aapl._raw)