import alpaca_trade_api as tradeapi
import requests
import config

ORDERS_URL = '{}/v2/orders'.format(config.APCA_API_BASE_URL)

def createMakeOrder():
    ticker = 'AAPL'
    qty = '2'
    side = 'buy'
    ordertype = 'market'

    data = {
        'symbol': ticker,
        'qty': qty,
        'side': side,
        'type': ordertype,
        'time_in_force': 'day'
    }

    r = requests.post(ORDERS_URL, json=data, headers=config.HEADERS)

    return r.content

print(createMakeOrder())