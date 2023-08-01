import os
from dotenv import load_dotenv

import datetime as dt
import pytz
import csv

from alpaca.data.timeframe import TimeFrame

load_dotenv()

import alpaca_trade_api as tradeapi

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
base_url = 'https://paper-api.alpaca.markets'

api =tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Get daily price data for AAPL over the last 5 trading days.

_timeNow = dt.datetime.now(pytz.timezone('US/Eastern'))
_2DaysAgo = _timeNow - dt.timedelta(days=30)

print(_2DaysAgo)

barset = api.get_bars('AAPL', TimeFrame.Hour, start=_2DaysAgo.isoformat(), end=None)
aapl_bars = barset

# print(barset)

# print("time                      open")
# hi = [(bar.t, bar.o) for bar in barset]

# print(hi)

raw_barset = barset._raw
keys = raw_barset[0].keys()

print(keys)

with open('data-new.csv', 'w', newline='', index=False) as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(raw_barset)

# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('AAPL moved {}% over the last 5 days'.format(percent_change))