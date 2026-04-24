import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Growth Research", layout="wide")

API_KEY = "EM716SRFFX4E4SKM" 

st.title("🛡️ 5-Year Growth & Potential Analyzer")

def get_clean_data(symbol):
    # Standardize for the data provider
    clean_ticker = symbol.upper().replace(".TO", "")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSX:{clean_ticker}&outputsize=full&apikey={API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Note" in data:
            st.warning(f"⏸️ Waiting for {symbol} data... (Free limit reached. I will retry in 60 seconds.)")
            return "LIMIT"
            
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
            df.index = pd.to_datetime(df.index)
            # Use '4. close' as the price
            prices = df['4. close'].astype(float).sort_index()
            # Only show last 5 years
            return prices.last('1825D') # 1825 days = 5 years
    except:
        return None
    return None

# --- RESEARCH LIST ---
stocks = ["CSU.TO", "SHOP.TO", "BN.TO", "CNR.TO"]

st.subheader("📈 5-Year Performance Charts")

for s in stocks:
    result = get_clean_data(s)
    
    if result == "LIMIT":
        time.sleep(60) # If we hit the limit, wait a full minute
    elif result is not None:
        # Create a clean box for each stock
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                current_p = result.iloc[-1]
                st.metric(label=s, value=f"${current_p:.2f}")
                st.write("Target: 10-Year Growth")
            with col2:
                # This creates the actual chart you are looking for
                st.line_chart(result)
            st.divider()
    
    # Essential pause between stocks to stay under the free limit
    time.sleep(15) 

st.subheader("🧠 Peer-to-Peer Decision Tool")
st.write("Use the 'Mirror Test' below to evaluate these charts once they load.")
