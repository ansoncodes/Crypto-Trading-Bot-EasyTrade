
# EasyTrade - Binance Futures Trading Bot

This project is a simplified crypto trading bot built in Python, created as a technical assessment for the Junior Python Developer role. The application provides two distinct interfaces: a robust command-line tool and an interactive, user-friendly web application built with Streamlit.

---
## Key Features

* **Dual Interface**: Operates via an interactive Streamlit web app or a CLI.
* **Multiple Order Types**: Full support for `MARKET`, `LIMIT`, and `STOP-LIMIT` orders.
* **Live Data & Validation**: The web UI fetches and displays live market prices from the Binance API and provides real-time validation to prevent common user errors.
* **Secure**: API keys are loaded securely from a `.env` file and are never exposed in the source code.
* **Comprehensive Logging**: All actions, successful orders, and API errors are logged to `logs/trading_bot.log` for easy debugging and monitoring.

## Setup and Installation

Follow these steps to set up the project environment.


### 1. Clone the Repository
Open your terminal and clone the project repository:
```bash
git clone https://github.com/ansoncodes/trading_bot
cd trading_bot
````

### 2. Set Up Virtual Environment & Install Dependencies

**On macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**Install Requirements:**

```bash
pip install -r requirements.txt
```

### 3. Add Your API Credentials

Add your API credentials in the `.env` file

```ini
# .env file
BINANCE_API_KEY="YOUR_TESTNET_API_KEY_HERE"
BINANCE_API_SECRET="YOUR_TESTNET_API_SECRET_HERE"
```

-----

## How to Run the Application

### 1. Web UI (Recommended)

Launch the Streamlit interface. This is the easiest way to test the bot's full functionality.

```bash
streamlit run app.py
```

This opens the EasyTrade app in your browser for real-time trading and monitoring.

### 2. Command-Line Interface (CLI)

You can also use the terminal to place and manage orders directly.

**View CLI Help:**

```bash
python trading_bot.py --help
```

**Example Commands:**

```bash
# Place a MARKET order to BUY 0.001 BTC
python trading_bot.py BTCUSDT BUY MARKET 0.001

# Place a LIMIT order to SELL 0.01 ETH at $4000
python trading_bot.py ETHUSDT SELL LIMIT 0.01 --price 4000
```

-----

### Logs

All activities are saved to `logs/trading_bot.log`, which is helpful for debugging and reviewing trade history.

-----

### Disclaimer

This bot is built for educational and testing purposes on Binance’s Futures Testnet. Do not use it on the live environment with real funds unless it has been thoroughly tested and audited.


