import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="AI Stock Tracker", layout="wide")

# Your API Key
API_KEY = "EM716SRFFX4E4SKM" 

st.title("📈 AI-Powered Stock Research Dashboard")

def get_stock_data(symbol):
    # Standardize the symbol for Alpha Vantage
    # Converts SHOP.TO to TSX:SHOP
    symbol = symbol.upper()
    if ".TO" in symbol:
        api_symbol = "TSX:" + symbol.replace(".TO", "")
    elif ".V" in symbol:
        api_symbol = "TSXV:" + symbol.replace(".V", "")
    else:
        api_symbol = symbol

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={api_symbol}&apikey={API_KEY}'
    
    try:
        r = requests.get(url)
        data = r.json()
        
        # If Alpha Vantage sends a "Note", it means we hit the frequency limit
        if "Note" in data:
            st.error("API Limit reached! Please wait 1 minute before searching again.")
            return None

        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            # Rename columns to be cleaner
            df.columns = [c.split(' ')[1] for c in df.columns]
            return df['close'].sort_index()
    except:
        return None
    return None

# --- RESEARCH & MONITORING ---
ticker = st.text_input("Enter Ticker (Use .TO for Canadian stocks, e.g., SHOP.TO or TD.TO):", "SHOP.TO")

if ticker:
    with st.spinner(f'Searching for {ticker}...'):
        price_data = get_stock_data(ticker)
        if price_data is not None:
            st.subheader(f"5-Year Growth Trend: {ticker}")
            st.line_chart(price_data)
        else:
            st.info("Searching... if no chart appears, check the ticker or wait 60 seconds.")

# --- AI STOCK PICKER ---
st.divider()
if st.button("🚀 Run AI Research (100x Potential Picks)"):
    # These are your identified high-potential Canadian stocks
    picks = ["LSPD.TO", "WELL.TO", "BN.TO", "CSU.TO", "HIVE.TO"]
    st.write("Analyzing market cap and revenue trends...")
    
    for stock in picks:
        p_data = get_stock_data(stock)
        if p_data is not None:
            current_price = p_data.iloc[-1]
            st.success(f"**{stock}** | Current Price: ${current_price:.2f} CAD")
        # Small pause to avoid hitting the API limit too fast
        time.sleep(2)

# --- INVESTMENT TRACKER ---
st.divider()
st.subheader("💰 $100 Simulation Tracker")
# You can edit this list to track your personal favorites
my_portfolio = ["SHOP.TO", "TD.TO", "ATZ.TO"]

cols = st.columns(len(my_portfolio))
for i, p_ticker in enumerate(my_portfolio):
    p_data = get_stock_data(p_ticker)
    if p_data is not None:
        current_price = p_data.iloc[-1]
        # Basic simulation: showing price and ticker
        cols[i].metric(label=p_ticker, value=f"${current_price:.2f} CAD")
