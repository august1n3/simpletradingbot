from binance_client import BinanceBotClient

import logging
import utils
import time

# Setup logging
utils.setup_logging()
logger = logging.getLogger(__name__)

#configs
SYMBOL = "BTCUSDT"
QUANTITY = 0.001
LIMITPRICE = 30000

def run_bot():
    logger.info("Starting Simplified Trading Bot on Binance Testnet...")

    binance_client = BinanceBotClient()

    # 1. Get Exchange Info
    exchange_info = binance_client.get_exchange_info()
    if exchange_info:
        logger.info(f"Exchange Info loaded. Number of symbols: {len(exchange_info.get('symbols', []))}")
    else:
        logger.error("Could not fetch exchange information. Exiting.")
        return

    # 2. Get Account Balance
    account_balance = binance_client.get_account_balance()
    if account_balance:
        for asset in account_balance.get('assets', []):
            if asset.get('asset') == 'USDT':
                logger.info(f"USDT Balance: {asset.get('walletBalance')}")
                break
    else:
        logger.error("Could not fetch account balance.")

    #Get Current Price
    current_price = binance_client.get_current_price(SYMBOL)
    if current_price:
        logger.info(f"Current price of {SYMBOL}: {current_price}")
    else:
        logger.error(f"Could not fetch current price for {SYMBOL}.")
        return # Cannot proceed without price

    #Place a Market Buy Order (Example)
    logger.info(f"Attempting to place a MARKET BUY order for {SYMBOL} with quantity {QUANTITY}")
    market_buy_order = binance_client.place_market_order(
        symbol=SYMBOL,
        side='BUY',
        quantity=QUANTITY
    )
    if market_buy_order:
        logger.info(f"Market Buy Order ID: {market_buy_order.get('orderId')}")
        time.sleep(2) # Give some time for the order to process

    #Place a Limit Sell Order (Example)
    sell_price = round(current_price * 1.005, 1) # 0.5% higher
    logger.info(f"Attempting to place a LIMIT SELL order for {SYMBOL} with quantity {QUANTITY} at price {sell_price}")
    symbols = exchange_info.get('symbols', [])
    for i in symbols:
        if i.get('symbol') == SYMBOL:
            print(float(i.get('filters')[0].get('tickSize')))
    limit_sell_order = binance_client.place_limit_order(
        symbol=SYMBOL,
        side='SELL',
        quantity=QUANTITY,
        price=sell_price
    )
    if limit_sell_order:
        logger.info(f"Limit Sell Order ID: {limit_sell_order.get('orderId')}")
        time.sleep(2)

    #Get Open Orders
    logger.info(f"Checking for open orders for {SYMBOL}...")
    open_orders = binance_client.get_open_orders(symbol=SYMBOL)
    if open_orders:
        if open_orders:
            logger.info("Currently open orders:")
            for order in open_orders:
                logger.info(f"  Order ID: {order.get('orderId')}, Symbol: {order.get('symbol')}, Type: {order.get('type')}, Side: {order.get('side')}, Price: {order.get('price')}, Status: {order.get('status')}")
        else:
            logger.info("No open orders found.")

    #Cancel the Limit Order (Example)
    if limit_sell_order and limit_sell_order.get('orderId'):
        logger.info(f"Attempting to cancel Limit Sell Order ID: {limit_sell_order.get('orderId')}")
        cancel_result = binance_client.cancel_order(
            symbol="BTCUSDT",
            order_id=limit_sell_order.get('orderId')
        )
        if cancel_result:
            logger.info("Limit order cancelled successfully.")
        else:
            logger.error("Failed to cancel limit order.")
    else:
        logger.info("No limit order to cancel or order ID not found.")

    logger.info("Simplified Trading Bot finished.")

if __name__ == "__main__":
    run_bot()