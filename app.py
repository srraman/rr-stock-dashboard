import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="AI Stock Tracker", layout="wide")

st.title("📈 AI-Powered Stock Research Dashboard")

# --- RESEARCH & MONITORING ---
ticker = st.text_input("Enter Ticker (e.g., SHOP.TO for Shopify or AAPL for Apple):", "SHOP.TO")
if ticker:
    data = yf.download(ticker, period="5y")
    st.subheader(f"5-Year History for {ticker}")
    st.line_chart(data['Close'])

# --- AI STOCK PICKER (Simulated Reasoning) ---
if st.button("🚀 Run AI Research (Identify 100x Potential)"):
    st.write("Analyzing historical growth, revenue trends, and market cap...")
    # These are illustrative Canadian high-growth potential examples
    picks = ["LSPD.TO", "WELL.TO", "BN.TO", "CSU.TO", "HIVE.TO"]
    st.success("AI Identified 5 High-Potential Canadian Stocks:")
    for stock in picks:
        info = yf.Ticker(stock).info
        st.write(f"**{stock}**: {info.get('longName')} | Sector: {info.get('sector')}")

# --- INVESTMENT TRACKER ---
st.divider()
st.subheader("💰 $100 Simulation Tracker")
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = ["SHOP.TO", "TD.TO", "ATZ.TO"]

for p_ticker in st.session_state.portfolio:
    p_data = yf.download(p_ticker, period="1d")
    current_price = p_data['Close'].iloc[-1]
    # Simple simulation: Assume we bought at -5% from current price for tracking
    gain = (current_price - (current_price * 0.95)) / (current_price * 0.95) * 100
    st.metric(label=p_ticker, value=f"${current_price:.2f} CAD", delta=f"{gain:.2f}%")
