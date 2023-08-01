import alpaca_trade_api as tradeapi
import requests

from alpaca.trading.client import TradingClient

from constants import API_KEY, API_SECRET, BASE_URL

api_key = API_KEY
api_secret = API_SECRET
base_url = BASE_URL

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
client = TradingClient(api_key, api_secret, paper=True)

def get_open_position_symbols():
    open_positions = api.list_positions()
    f = open("file.txt", "a")
    f.write(str(open_positions))
    symbols = set([position.symbol for position in open_positions])

    return symbols


def buyOrder(symbol, qty):
    if symbol in get_open_position_symbols():
        api.close_position(symbol)

    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='day',
    )

    print('Buy: ', order)

def sellOrder(symbol, qty):
    if symbol in get_open_position_symbols():
        api.close_position(symbol)

    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='day',
    )

    print('Sell: ', order)

def closeAllPositions():
    for symbol in get_open_position_symbols():
        api.close_position(symbol)

# closeAllPositions()
# get_open_position_symbols()