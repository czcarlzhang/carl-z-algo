import os
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
base_url = 'https://paper-api.alpaca.markets'

client = TradingClient(api_key, api_secret, paper=True)
account = dict(client.get_account())

for k, v in account.items():
    print(f"{k:30}{v}")

order_details = MarketOrderRequest(
    symbol="EA",
    qty=5,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY,
)

order = client.submit_order(order_data=order_details)

print(OrderSide.BUY)

trades = TradingStream(api_key, api_secret, paper=True)

async def trade_status(data):
    print(data)

trades.subscribe_trade_updates(trade_status)
trades.run()

# assets = [asset for asset in client.get_all_positions()]
# positions = [(asset.symbol, asset.qty, asset.current_price) for asset in assets]
# print("Positions")
# print(f"{'Symbol':9}{'Qty':>4}{'Value':>15}")
# print("-" * 28)

# for position in positions:
#     print(f"{position[0]:9}{position[1]:>4}{float(position[1]) * float(position[2]):>15.2f}")

# client.close_all_positions(cancel_orders=True)
