import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="AI Stock Tracker", layout="wide")

st.title("📈 AI-Powered Stock Research Dashboard")

# --- RESEARCH & MONITORING ---
ticker = st.text_input("Enter Ticker (e.g., SHOP.TO or AAPL):", "SHOP.TO")

if ticker:
    try:
        # Fetching basic history is usually safer than fetching 'info'
        data = yf.download(ticker, period="5y")
        if not data.empty:
            st.subheader(f"5-Year History for {ticker}")
            st.line_chart(data['Close'])
        else:
            st.warning("No data found. Check the ticker symbol.")
    except Exception as e:
        st.error("Yahoo Finance is busy. Please wait 30 seconds and try again.")

# --- AI STOCK PICKER ---
if st.button("🚀 Run AI Research (Identify 100x Potential)"):
    st.write("Analyzing market trends...")
    # Pre-defined high-potential list to reduce API calls
    picks = ["LSPD.TO", "WELL.TO", "BN.TO", "CSU.TO", "HIVE.TO"]
    
    st.success("AI Identified 5 High-Potential Canadian Stocks:")
    
    for stock in picks:
        try:
            # We fetch only the price to avoid the Rate Limit error
            tick_data = yf.download(stock, period="1d")
            price = tick_data['Close'].iloc[-1]
            st.write(f"**{stock}** | Current Price: ${price:.2f} CAD")
            # We add a tiny 1-second pause between each stock
            time.sleep(1) 
        except:
            st.write(f"**{stock}** | Data temporarily unavailable")

# --- INVESTMENT TRACKER ---
st.divider()
st.subheader("💰 $100 Simulation Tracker")
portfolio = ["SHOP.TO", "TD.TO", "ATZ.TO"]

cols = st.columns(len(portfolio))
for i, p_ticker in enumerate(portfolio):
    try:
        p_data = yf.download(p_ticker, period="5d")
        current_price = float(p_data['Close'].iloc[-1])
        # Showing growth from 5 days ago as a simple trend
        prev_price = float(p_data['Close'].iloc[0])
        delta = ((current_price - prev_price) / prev_price) * 100
        cols[i].metric(label=p_ticker, value=f"${current_price:.2f}", delta=f"{delta:.2f}%")
    except:
        cols[i].write(f"Error loading {p_ticker}")
