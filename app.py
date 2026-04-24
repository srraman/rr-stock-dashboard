import streamlit as st
import pandas as pd
import requests
import io
import time

# YOUR API KEY
API_KEY = "EM716SRFFX4E4SKM"

st.set_page_config(page_title="Dynamic CA/US Discovery", layout="wide")
st.title("🛡️ Dynamic CA/US Frontier Discovery")
st.info("Protocol: Live Market Scan | TSX & US Only | Under $150 | No ETFs | Alpha Vantage")

@st.cache_data(ttl=3600)
def get_all_active_listings():
    """Downloads the entire global listing status from Alpha Vantage once per hour."""
    url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}'
    r = requests.get(url)
    df = pd.read_csv(io.StringIO(r.text))
    # Filter for common stocks only (No ETFs)
    return df[df['assetType'] == 'Stock']

def get_stock_price(symbol):
    """Fetches the latest price and history for a discovered symbol."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    try:
        r = requests.get(url)
        data = r.json()
        if "Time Series (Daily)" in data:
            df = pd.DataFrame(data["Time Series (Daily)"]).T
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            return df['4. close'].sort_index().tail(500)
    except:
        return None
    return None

# 1. Load all active stocks globally
with st.spinner("Scanning Global Exchanges..."):
    all_listings = get_all_active_listings()

tab_cad, tab_usd = st.tabs(["🇨🇦 Canada (TSX)", "🇺🇸 USA (NYSE/NASDAQ)"])

def process_market(is_cad):
    # 2. Filter strictly by Exchange
    if is_cad:
        # TSX stocks usually have no suffix in the listing file but are marked as 'TSX'
        market_df = all_listings[all_listings['exchange'] == 'TSX']
    else:
        market_df = all_listings[all_listings['exchange'].isin(['NYSE', 'NASDAQ'])]

    # 3. Dynamic Discovery: Pick 6 active companies to analyze
    # We sample from the 'Active' status list to ensure variety
    discovered_list = market_df.sample(20)['symbol'].tolist()
    
    cols = st.columns(3)
    display_count = 0
    
    for ticker in discovered_list:
        if display_count >= 6: break # Alpha Vantage free tier limit
        
        # In Alpha Vantage, TSX stocks need the .TRT suffix for price data
        price_ticker = f"{ticker}.TRT" if is_cad else ticker
        
        hist = get_stock_price(price_ticker)
        if hist is not None:
            curr_p = hist.iloc[-1]
            
            # 4. PRICE FILTER: Strictly under $150
            if curr_p < 150:
                growth = ((curr_p - hist.iloc[0]) / hist.iloc[0]) * 100
                with cols[display_count % 3]:
                    st.metric(label=f"{ticker} ({'TSX' if is_cad else 'US'})", 
                              value=f"${curr_p:.2f}", 
                              delta=f"{growth:.1f}% (2Y)")
                    st.line_chart(hist)
                    display_count += 1
                time.sleep(1) # API Rate Limit protection

with tab_cad:
    process_market(is_cad=True)

with tab_usd:
    process_market(is_cad=False)
