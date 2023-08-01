import os
from dotenv import load_dotenv

load_dotenv()

import alpaca_trade_api as tradeapi

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
base_url = 'https://paper-api.alpaca.markets'

api =tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Get a list of all active assets.
active_assets = api.list_assets(status='active')

# Filter the assets down to just those on NASDAQ.
nasdaq_assets = [a.symbol for a in active_assets if a.exchange == 'NASDAQ']
print(nasdaq_assets)