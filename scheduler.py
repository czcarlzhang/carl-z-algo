from datetime import timedelta

import schedule
import time

from helpers import utc_to_local
from get_history import is_market_open_today, trading
from buysell import closeAllPositions

# 09:00 - 00:00 UTC Time Market Data Updates
# 14:30 - 21:00 UTC Trading Hours

# 14:00 Fetch Today's Pre-Market Data
# If Pre-Market Data Exists, Market is Open Today Continue, Else Wait Next Day
# 15:00 - 20:00 Every Hour Buy/Sell Depending On Next Hour's Open Price LSTM Prediction
# 21:00 Sell Stock

def _next_run():
    pass # return schedule.next_run()

def fetch_pre_market_data():
    print("Fetching Pre-Market Data")

    hi = is_market_open_today()
    f = open("marketopen.txt", "a")
    f.write(str(hi))

    if hi:
        schedule.every(1).hours.until(timedelta(hours=3)).do(alpaca_trader)

    print(_next_run())

def alpaca_trader():
    print("Undergoing Transaction")
    trading()

    print(_next_run())

print(_next_run())
fetch_pre_market_data_time = utc_to_local('18', '02', '0')
schedule.every().day.at(fetch_pre_market_data_time).do(fetch_pre_market_data)

print(_next_run())
close_all_positions_time = utc_to_local('20', '55', '0')
schedule.every().day.at(close_all_positions_time).do(closeAllPositions)

while True:
    schedule.run_pending()
    time.sleep(1)
    print(schedule.next_run())