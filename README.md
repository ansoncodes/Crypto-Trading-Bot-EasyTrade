# 🚀 EasyTrade - Binance Futures Trading Bot

**EasyTrade** is a simplified crypto trading bot built in Python as part of a technical assessment for a Junior Python Developer role.  
It provides both a powerful **command-line interface (CLI)** and an intuitive **web UI** built with **Streamlit** for easy order placement and market interaction.

---

## 🔑 Key Features

- **⚙️ Dual Interface**  
  Trade using a flexible CLI or a sleek Streamlit-based web interface.

- **📊 Multiple Order Types**  
  Supports `MARKET`, `LIMIT`, and `STOP-LIMIT` orders.

- **📈 Live Market Data & Validation**  
  Real-time price fetching and smart form validation to prevent common order errors.

- **🔐 Secure API Handling**  
  API keys are loaded securely from a `.env` file—never hardcoded.

- **📝 Detailed Logging**  
  All activities, errors, and successful trades are logged in `logs/trading_bot.log`.

---

## 🧱 Technology Stack

| Component         | Tech/Tool           |
|------------------|---------------------|
| Language          | Python 3            |
| Web UI            | Streamlit           |
| Binance API       | `python-binance`    |
| CLI Interface     | `argparse`          |
| Config Management | `python-dotenv`     |

---

## ⚙️ Setup and Installation

### Clone the Repository

```bash
git clone <your-repository-url>
cd <project-folder-name>

 Set Up Virtual Environment & Install Dependencies
🐧 On macOS/Linux:

Bash

python3 -m venv .venv
source .venv/bin/activate
🪟 On Windows:

Bash

python -m venv .venv
.\.venv\Scripts\activate
📦 Install Requirements:

Bash

pip install -r requirements.txt
4️⃣ Add Your API Credentials
Create a file named .env in the project root:

Ini, TOML

# .env file
BINANCE_API_KEY="YOUR_TESTNET_API_KEY_HERE"
BINANCE_API_SECRET="YOUR_TESTNET_API_SECRET_HERE"
⚠️ Keep your .env file private. Never commit it to version control.

▶️ Running the Application
🌐 Web UI (Recommended)
Launch the Streamlit interface:

Bash

streamlit run app.py
This opens the EasyTrade app in your browser for real-time trading and monitoring.

💻 Command-Line Interface (CLI)
Use the terminal to place and manage orders directly.

View CLI Help:

Bash

python trading_bot.py --help
Example Commands:

Bash

# Place a MARKET order to BUY 0.001 BTC
python trading_bot.py BTCUSDT BUY MARKET 0.001

# Place a LIMIT order to SELL 0.01 ETH at $4000
python trading_bot.py ETHUSDT SELL LIMIT 0.01 --price 4000
📂 Logs
All activities are saved to:

Bash

logs/trading_bot.log
This is helpful for debugging and reviewing trade history.

📌 Disclaimer
This bot is built for educational and testing purposes on Binance’s Futures Testnet. Do not use it on the live environment with real funds unless thoroughly tested and audited.
