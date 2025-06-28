from binance.um_futures import UMFutures as Client
from binance.exceptions import BinanceAPIException

import logging
import utils

logger = logging.getLogger(__name__)

class BinanceBotClient:
    def __init__(self):
        ##initializes the Binance Futures client.
        api_key, api_secret = utils.obtain_keys()
        logger.info("Keys obtained successfully.")
        self.client = Client()
        logger.info(self.client.time())
        self.client = Client(base_url="https://testnet.binancefuture.com", key=api_key, secret=api_secret)
        logger.info(self.client.klines(symbol="BTCUSDT", interval="1m"))

        logger.info(f"Initialized Binance Futures Client with base URL: https://testnet.binancefuture.com")

    def get_exchange_info(self):
        ## Fetches exchange information.
        try:
            info = self.client.exchange_info()
            logger.info("Successfully fetched exchange info.")
            return info
        except BinanceAPIException as e:
            logger.error(f"Error fetching exchange info: {e}")
            return None

    def get_account_balance(self):
        ##Fetches account balance information.
        try:
            balance = self.client.account()
            logger.info("Successfully fetched account balance.")
            return balance
        except BinanceAPIException as e:
            logger.error(f"Error fetching account balance: {e}")
            return None

    def get_current_price(self, symbol: str):
        """Fetches the current market price for a given symbol."""
        try:
            ticker = self.client.ticker_price(symbol)
            price = float(ticker['price'])
            logger.info(f"Current price for {symbol}: {price}")
            return price
        except BinanceAPIException as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None

    def place_market_order(self, symbol: str, side: str, quantity: float):
        ## places a market order
        try:
            order = self.client.new_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logger.info(f"Placed MARKET {side} order: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error placing MARKET order for {symbol}, side {side}, quantity {quantity}: {e}")
            return None

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        ## places a limit order
        try:
            order = self.client.new_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC', # Good Till Cancelled
                quantity=quantity,
                price=price
            )
            logger.info(f"Placed LIMIT {side} order at {price} for {symbol}: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error placing LIMIT order for {symbol}, side {side}, quantity {quantity}, price {price}: {e}")
            return None

    def cancel_order(self, symbol: str, order_id: str):
        ## Cancels an open order.
        try:
            cancel_result = self.client.cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            logger.info(f"Cancelled order {order_id} for {symbol}: {cancel_result}")
            return cancel_result
        except BinanceAPIException as e:
            logger.error(f"Error cancelling order {order_id} for {symbol}: {e}")
            return None

    def get_open_orders(self, symbol: str = None):
        ## Fetches open orders for a given symbol or all symbols.
        try:
            if symbol:
                open_orders = self.client.get_all_orders(symbol=symbol, openOnly='true')
            else:
                open_orders = self.client.get_all_orders(openOnly='true')
            logger.info(f"Fetched open orders: {open_orders}")
            return open_orders
        except BinanceAPIException as e:
            logger.error(f"Error fetching open orders: {e}")
            return None

    
        