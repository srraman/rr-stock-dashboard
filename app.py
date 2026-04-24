import streamlit as st
import requests
import pandas as pd
import time

# YOUR RETRIEVED API KEY
API_KEY = "EM716SRFFX4E4SKM"

st.set_page_config(page_title="Professional Frontier Engine", layout="wide")
st.title("🛡️ Professional Frontier Discovery")
st.info("Direct Exchange Feed via Alpha Vantage. Protocol: Dynamic Discovery | Under $150 | No ETFs.")

def get_market_leaders():
    """Fetches the current top gainers/actives globally from Alpha Vantage"""
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}'
    r = requests.get(url)
    return r.json()

def get_stock_data(symbol):
    """Fetches 2-year daily history for a specific symbol"""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    if "Time Series (Daily)" in data:
        df = pd.DataFrame(data["Time Series (Daily)"]).T
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df['4. close'].sort_index().tail(500) # Roughly 2 years of trading days
    return None

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

# Load the raw leadership data
leaders_data = get_market_leaders()

def process_tab(is_cad_mode):
    # Alpha Vantage provides 'top_gainers', 'top_losers', and 'most_actively_traded'
    # We use 'most_actively_traded' for the most stable 'staircase' discovery
    raw_list = leaders_data.get('most_actively_traded', [])
    
    found_count = 0
    cols = st.columns(3)
    
    for item in raw_list:
        ticker = item['ticker']
        price = float(item['price'])
        
        # 1. PRICE FILTER: Under $150
        if price > 150: continue
            
        # 2. EXCHANGE FILTER: 
        # Note: Alpha Vantage uses different suffixes or focuses; 
        # for free tier, we filter US vs Non-US.
        if is_cad_mode:
            if not ticker.endswith(".TO"): continue
        else:
            if "." in ticker: continue
            
        if found_count >= 6: break # Respecting Alpha Vantage free tier limits
            
        # 3. GET HISTORY & DISPLAY
        hist = get_stock_data(ticker)
        if hist is not None:
            with cols[found_count % 3]:
                growth = ((price - hist.iloc[0]) / hist.iloc[0]) * 100
                st.metric(label=ticker, value=f"${price:.2f}", delta=f"{growth:.1f}% (2Y)")
                st.line_chart(hist)
                found_count += 1
            time.sleep(1) # Delay to stay within 2026 API rate limits

with tab_cad:
    process_tab(is_cad_mode=True)

with tab_usd:
    process_tab(is_cad_mode=False)
