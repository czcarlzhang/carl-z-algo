import os

import datetime as dt
from datetime import datetime, timedelta
import pytz

import pandas as pd
import csv

from alpaca.data.timeframe import TimeFrame

from alpaca.trading.client import TradingClient

import alpaca_trade_api as tradeapi

from constants import API_KEY, API_SECRET, BASE_URL, SYMBOL_PATH
from helpers import utc_to_local

from lstm import get_next_hour_prediction

from buysell import buyOrder, sellOrder

api_key = API_KEY
api_secret = API_SECRET
base_url = BASE_URL

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
client = TradingClient(api_key, api_secret, paper=True)


# print(api.get_account())
# print(api.list_positions())
# api.close_position('AAPL')
# client.close_all_positions(cancel_orders=True)
# print(api.list_positions())
# print(api.get_asset('AAPL'))

# print(api.list_orders())

# Get daily price data for AAPL over the last 5 trading days.

_timeNow = dt.datetime.now(pytz.timezone('US/Eastern'))

# symbols_to_trade = ['AAPL']
# symbols_to_trade = ['F']

# symbol : money to trade
symbols_investement_dict = {
    'AAPL': 45000,
    'SPY': 45000,
}

def trading():
    # too many values to unpack
    for symbol in symbols_investement_dict:
        # print(symbol, symbols_investement_dict[symbol])

        path = SYMBOL_PATH + symbol + '.csv'
        csv_exists = os.path.isfile(path)

        if csv_exists:
            df = pd.read_csv(SYMBOL_PATH + symbol + '.csv')
            start_date_to_fetch = list(pd.to_datetime(df['t']))[-1] + timedelta(hours=1)

            print(start_date_to_fetch)

            bars = api.get_bars(symbol, TimeFrame.Hour, start=start_date_to_fetch.isoformat(), end=None)
            raw_bars = bars._raw
            keys = raw_bars[0].keys()

            with open(SYMBOL_PATH + symbol + '.csv', 'a', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writerows(raw_bars)

        else:
            start_date_to_fetch = datetime.now(pytz.timezone('UTC')) - timedelta(days=30)

            bars = api.get_bars(symbol, TimeFrame.Hour, start=start_date_to_fetch.isoformat(), end=None)
            raw_bars = bars._raw
            keys = raw_bars[0].keys()

            with open(SYMBOL_PATH + symbol + '.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(raw_bars)

        # symbol price movement
        first_open = bars[0].o
        last_close = bars[-1].c
        percent_change = (last_close - first_open) / first_open * 100
        print('AAPL moved {}% over since last time'.format(percent_change))

        # predict the next hours price
        predicted_open_price, last_open_price = get_next_hour_prediction(symbol)
        print(predicted_open_price[0], last_open_price)
        # try using 7 day prediciton instead of 30

        qty = str(int(symbols_investement_dict[symbol] / last_open_price))
        print(qty)

        # buy or sell depending on price
        if predicted_open_price[0] > last_open_price:
            print('buying')
            # buyOrder(symbol)
            buyOrder(symbol, qty)
        else:
            print('selling')
            #sellOrder(symbol)
            sellOrder(symbol, qty)

        # BOOM DONE

def is_market_open_today():
    '''
    Check at 14:00 UTC / 08:00 EST if market is open
    '''
    clock = api.get_clock()
    # seconds_to_open = (clock.next_open - clock.timestamp).total_seconds()

    # print(clock)
    # print(seconds_to_open)

    return clock.is_open