import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

class CarlZAlgo():

    def __init__(self, API_KEY, API_SECRET, ticker):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.base_url = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.REST(self.api_key, self.api_secret, self.base_url, api_version='v2')
        self.symbol = ticker

        # obtain account information
        account = self.api.get_account()
        print(account.status)

        try:
            self.position = int(self.api.get_position(self.symbol().qty))
        except:
            self.position = 0

        print(f'Current holding {self.position} {self.symbol} stocks')

    def submit_order(self, target):
        delta = target - self.position
        if delta == 0:
            return

        if delta > 0:
            buy_quality = delta

            print(f'Buying {buy_quality} {self.symbol} shares')

            self.order = self.api.submit_order(
                symbol=self.symbol,
                qty=buy_quality,
                type='market',
                side='buy',
                time_in_force='day'
            )

        if delta < 0:
            sell_quantity = abs(delta)
            print(f'Selling {sell_quantity} {self.symbol} shares')

            self.order = self.api.submit_order(
                symbol=self.symbol,
                qty=sell_quantity,
                type='market',
                side='sell',
                time_in_force='day'
            )

    def cancel_all_orders(self):
        self.api.cancel_all_orders()

    def get_historic_data(self, symbol):
        aapl = self.api.get_barset('AAPL', 'day')\

    def get_list_assets(self):
        return self.api.list_assets(status='active')

load_dotenv()

# authentication and connection details
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
base_url = 'https://paper-api.alpaca.markets'

aapl = CarlZAlgo(api_key, api_secret, 'AAPL')
# aapl.cancel_all_orders()
# aapl.submit_order(10)
list = aapl.get_list_assets()
print(list)

print()

# get list of assets.. find time when market clsoes
