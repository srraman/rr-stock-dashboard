import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Stock Tracker", layout="wide")

# --- EM716SRFFX4E4SKM ---
API_KEY = "EM716SRFFX4E4SKM" 

st.title("📈 Reliable Stock Research Dashboard")

def get_stock_data(symbol):
    # This automatically converts "SHOP.TO" or "SHOP" into "TSX:SHOP"
    symbol = symbol.upper().replace(".TO", "")
    if ":" not in symbol:
        # We assume you want Canadian stocks first; if not, you can type "AAPL"
        api_symbol = f"TSX:{symbol}"
    else:
        api_symbol = symbol

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={api_symbol}&apikey={API_KEY}'
    
    try:
        r = requests.get(url)
        data = r.json()
        
        # If TSX doesn't work, try it as a US stock
        if "Error Message" in data or "Note" in data:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
            r = requests.get(url)
            data = r.json()

        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            return df['4. close'].sort_index()
    except:
        return None
    return None

# --- RESEARCH & MONITORING ---
ticker = st.text_input("Enter Ticker (e.g., SHOP, TD, or AAPL):", "SHOP")

if ticker:
    with st.spinner('Fetching market data...'):
        price_data = get_stock_data(ticker)
        if price_data is not None:
            st.subheader(f"Recent History for {ticker}")
            st.line_chart(price_data)
        else:
            st.warning("Limit Reached: Alpha Vantage allows 25 searches per day on the free version. Please try again tomorrow!")

# --- INVESTMENT TRACKER ---
st.divider()
st.subheader("💰 $100 Simulation Tracker")
portfolio = ["SHOP", "TD", "ATZ"]
cols = st.columns(len(portfolio))

for i, p_ticker in enumerate(portfolio):
    p_data = get_stock_data(p_ticker)
    if p_data is not None:
        current_price = p_data.iloc[-1]
        cols[i].metric(label=p_ticker, value=f"${current_price:.2f} CAD")
