import streamlit as st
import pandas as pd
import requests
import io
import time

# YOUR RETRIEVED API KEY
API_KEY = "EM716SRFFX4E4SKM"

st.set_page_config(page_title="Stable Frontier Engine", layout="wide")
st.title("🛡️ Stable CA/US Frontier Discovery")
st.info("Protocol: Error-Resistant Discovery | TSX & US Only | Under $150 | Alpha Vantage")

@st.cache_data(ttl=3600)
def get_all_active_listings():
    """Downloads listings with error handling for API limits."""
    url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}'
    try:
        r = requests.get(url)
        # If Alpha Vantage sends an error, it's usually JSON. CSV starts with 'symbol'
        if r.text.startswith("{"):
            st.error("⚠️ Alpha Vantage API Limit Reached. Please wait a few minutes or check your daily quota (25/day).")
            return pd.DataFrame()
        
        df = pd.read_csv(io.StringIO(r.text))
        # Ensure the column exists before filtering
        if 'assetType' in df.columns:
            return df[df['assetType'] == 'Stock']
        return df
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return pd.DataFrame()

def get_stock_price(symbol):
    """Fetches price with rate-limit protection."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    try:
        r = requests.get(url)
        data = r.json()
        if "Note" in data:
            st.warning("Rate limit hit. Slowing down...")
            time.sleep(10) # Wait if we are going too fast
            return None
        if "Time Series (Daily)" in data:
            df = pd.DataFrame(data["Time Series (Daily)"]).T
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            return df['4. close'].sort_index().tail(500)
    except:
        return None
    return None

# Execution logic
all_listings = get_all_active_listings()

if not all_listings.empty:
    tab_cad, tab_usd = st.tabs(["🇨🇦 Canada (TSX)", "🇺🇸 USA (NYSE/NASDAQ)"])

    def run_market(is_cad):
        # Filter strictly by region
        if is_cad:
            market_df = all_listings[all_listings['exchange'] == 'TSX']
        else:
            market_df = all_listings[all_listings['exchange'].isin(['NYSE', 'NASDAQ'])]
        
        # Pull a random sample so it's different every time
        sample_tickers = market_df.sample(min(15, len(market_df)))['symbol'].tolist()
        
        cols = st.columns(3)
        display_count = 0
        
        for ticker in sample_tickers:
            if display_count >= 3: break # Keep it small to stay under free tier limits
            
            # Use .TRT for Toronto stocks in price queries
            lookup = f"{ticker}.TRT" if is_cad else ticker
            hist = get_stock_price(lookup)
            
            if hist is not None:
                curr_p = hist.iloc[-1]
                if curr_p < 150:
                    growth = ((curr_p - hist.iloc[0]) / hist.iloc[0]) * 100
                    with cols[display_count % 3]:
                        st.metric(label=f"{ticker}", value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                        st.line_chart(hist)
                        display_count += 1
            time.sleep(2) # Mandatory 2-second pause between stocks for free tier

    with tab_cad:
        run_market(is_cad=True)
    with tab_usd:
        run_market(is_cad=False)
else:
    st.write("Could not retrieve market data. Please refresh in a moment.")
