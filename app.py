# app.py

import streamlit as st
import os
from dotenv import load_dotenv
from trading_bot import BasicBot, setup_logging

# Load API keys from .env file
load_dotenv()
API_KEY = os.environ.get('BINANCE_API_KEY')
API_SECRET = os.environ.get('BINANCE_API_SECRET')

# --- FIX: Use @st.cache_resource instead of the outdated @st.singleton ---
@st.cache_resource
def get_bot():
    """Creates and returns a single, cached instance of the BasicBot."""
    if API_KEY and API_SECRET:
        setup_logging()
        return BasicBot(api_key=API_KEY, api_secret=API_SECRET, testnet=True)
    return None

# --- Get the single bot instance for the entire app session ---
bot = get_bot()

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Trading Bot", layout="centered")
st.title("EasyTrade")

# --- STEP 1: Select Asset & Order Type ---
st.subheader("1. Select Asset & Order Type")
col1, col2 = st.columns(2)
with col1:
    symbol = st.text_input("Symbol", "BTCUSDT").upper()
with col2:
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_LIMIT"])

# --- Display Current Price ---
current_price = 0.0
if bot:
    try:
        fetched_price = bot.get_current_price(symbol)
        if fetched_price:
            current_price = fetched_price
            st.metric(label=f"Current {symbol} Price", value=f"${current_price:,.2f}")
    except Exception as e:
        st.warning(f"Could not fetch current price: {e}")

st.button("Refresh Current Price")

# --- STEP 2: Enter Order Details ---
st.subheader("2. Enter Order Details")
with st.form("trading_form"):
    price = 0.0
    stop_price = 0.0

    form_col1, form_col2 = st.columns(2)
    with form_col1:
        side = st.selectbox("Side", ["BUY", "SELL"])
        quantity = st.number_input("Quantity", min_value=0.0, step=0.001, format="%.8f")
    
    with form_col2:
        if order_type == "LIMIT":
            price = st.number_input("Price", min_value=0.0, format="%.8f")
        elif order_type == "STOP_LIMIT":
            price = st.number_input("Price", min_value=0.0, format="%.8f")
            stop_price = st.number_input("Stop Price", min_value=0.0, format="%.8f")

    submitted = st.form_submit_button("Place Order")

# --- Handle Form Submission ---
if submitted:
    if not bot:
        st.error("API keys are not configured. Please check your .env file.")
    else:
        st.info(f"Placing {side} {order_type} order for {quantity} {symbol}...")
        
        order_response = bot.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price if order_type in ["LIMIT", "STOP_LIMIT"] else None,
            stop_price=stop_price if order_type == "STOP_LIMIT" else None
        )
        
        if isinstance(order_response, dict):
            st.success("✅ Order placed successfully!")
            st.json(order_response)
        elif isinstance(order_response, str):
            st.error(f"❌ {order_response}")
        else:
            st.error("❌ Order placement failed. Check the logs for details.")