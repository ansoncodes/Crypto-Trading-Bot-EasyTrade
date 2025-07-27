# trading_bot.py

import os
import logging
import argparse
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
load_dotenv()

def setup_logging():
    """Sets up the logging configuration."""
    # This part is correct, no changes needed here.
    # It's good practice to create the logs directory if it doesn't exist.
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/trading_bot.log"), # This will place logs in the 'logs' folder
            logging.StreamHandler()
        ]
    )

class BasicBot:
    """A simplified trading bot for Binance Futures."""
    
    def __init__(self, api_key, api_secret, testnet=True):
        """
        Initializes the bot.
        
        Args:
            api_key (str): Your Binance API key.
            api_secret (str): Your Binance API secret.
            testnet (bool): Whether to use the testnet or live environment.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            # Set the futures testnet URL
            if testnet:
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            
            # Test connectivity
            self.client.futures_ping()
            self.logger.info("Successfully connected to Binance Futures Testnet.")
        except (BinanceAPIException, BinanceRequestException) as e:
            self.logger.error(f"Failed to connect to Binance API: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """
        Places an order on the futures market.
        
        Returns:
            dict: The order response from the API on success.
            str: An error message string on failure.
        """
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity
        }

        # --- MODIFIED: Return error string instead of None ---
        if order_type.upper() == 'LIMIT':
            if not price:
                return "Error: Price is required for a LIMIT order."
            params['price'] = price
            params['timeInForce'] = 'GTC'
        
        elif order_type.upper() == 'STOP_LIMIT':
            if not price or not stop_price:
                return "Error: Price and Stop Price are required for a STOP_LIMIT order."
            params['price'] = price
            params['stopPrice'] = stop_price
            params['timeInForce'] = 'GTC'
            params['type'] = 'STOP'

        self.logger.info(f"Placing {side} {order_type} order with params: {params}")
        
        try:
            order = self.client.futures_create_order(**params)
            self.logger.info(f"Successfully placed order: {order}")
            return order # Returns a dictionary on success
        except BinanceAPIException as e:
            self.logger.error(f"API Error placing order: {e.message}")
            return f"API Error: {e.message}" # Return the specific API error message
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}" # Return other errors
  

    def get_current_price(self, symbol):
        """Fetches the last traded price for a given symbol."""
        try:
            ticker = self.client.futures_ticker(symbol=symbol)
            return float(ticker['lastPrice'])
        except Exception as e:
            self.logger.error(f"Could not fetch price for {symbol}: {e}")
            return None

def main():
    """Main function to run the bot from the command line."""
    setup_logging()
    
    parser = argparse.ArgumentParser(description="A simplified Binance Futures trading bot.")
    
    parser.add_argument('symbol', type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help="Order side: BUY or SELL")
    parser.add_argument('order_type', type=str, choices=['MARKET', 'LIMIT', 'STOP_LIMIT'], help="Order type: MARKET, LIMIT, or STOP_LIMIT")
    parser.add_argument('quantity', type=float, help="Order quantity")
    parser.add_argument('--price', type=float, help="Order price (required for LIMIT and STOP_LIMIT)")
    parser.add_argument('--stop_price', type=float, help="Stop price (required for STOP_LIMIT)")

    args = parser.parse_args()
    
    # --- Security Best Practice: Use Environment Variables ---
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        logging.error("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        return

    try:
        bot = BasicBot(api_key=api_key, api_secret=api_secret, testnet=True)
        
        order_response = bot.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
        
        if order_response:
            print("\n--- ✅ Order Placed Successfully! ---")
            print(f"   Symbol: {order_response.get('symbol')}")
            print(f"   Order ID: {order_response.get('orderId')}")
            print(f"   Side: {order_response.get('side')}")
            print(f"   Type: {order_response.get('type')}")
            print(f"   Status: {order_response.get('status')}")
            print("------------------------------------")
        else:
            print("\n--- ❌ Order Placement Failed ---")
            print("   Check 'trading_bot.log' for details.")
            print("---------------------------------")
            
    except Exception as e:
        logging.error(f"Bot initialization failed: {e}")
        print("\n--- ❌ Bot Initialization Failed ---")
        print("   Could not connect to Binance. Check your API keys and network connection.")
        print("---------------------------------")


if __name__ == "__main__":
    main()