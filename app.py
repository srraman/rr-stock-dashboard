import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Growth Research Dashboard", layout="wide")

API_KEY = "EM716SRFFX4E4SKM" 

st.title("🛡️ 5-Year Growth Research Dashboard")
st.markdown("""
**How to use this tool:** Don't just look at the price. Look at the 5-year trend. 
A stock that grows steadily over 5 years often has a stronger 'engine' than one that just spiked this week.
""")

def get_5y_data(symbol):
    symbol = symbol.upper().replace(".TO", "")
    api_symbol = f"TSX:{symbol}"
    # Using 'full' outputsize to get 5+ years of daily data
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={api_symbol}&outputsize=full&apikey={API_KEY}'
    try:
        r = requests.get(url)
        data = r.json()
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df['4. close'].astype(float)
            # Filter for the last 5 years only
            five_years_ago = pd.Timestamp.now() - pd.DateOffset(years=5)
            return df[df.index >= five_years_ago].sort_index()
    except:
        return None
    return None

# --- RESEARCH PORTFOLIO ---
# Based on 2026 analyst consensus for long-term compounders
research_list = ["CSU.TO", "SHOP.TO", "BN.TO", "CNR.TO"]

st.subheader("📈 Long-Term (5-Year) Trend Analysis")
for stock in research_list:
    prices = get_5y_data(stock)
    if prices is not None:
        col1, col2 = st.columns([1, 3])
        with col1:
            current = prices.iloc[-1]
            start = prices.iloc[0]
            total_growth = ((current - start) / start) * 100
            st.metric(label=f"{stock} (Today)", value=f"${current:.2f}", delta=f"{total_growth:.1f}% since 2021")
        with col2:
            st.line_chart(prices)
        time.sleep(2) # Protect your 25-search limit

# --- THE DECISION TOOLKIT ---
st.divider()
st.subheader("🧠 How to Evaluate 'Growth Potential'")
st.write("Use this checklist to decide if a stock is a 'Buy' for you. (Trends are NOT enough!)")

with st.expander("Step 1: Check the 'Moat' (Competitive Advantage)"):
    st.write("- Does this company do something others can't easily copy?")
    st.write("- **Example:** CN Railway (CNR) owns tracks no one else can build.")

with st.expander("Step 2: Revenue Growth vs. Stock Price"):
    st.write("- Is the company actually making more money, or is the stock just 'hyped'?")
    st.write("- Look for companies that consistently increase their sales every year.")

with st.expander("Step 3: Management & Debt"):
    st.write("- Do they have too much debt? High debt can kill growth if interest rates stay high.")
    st.write("- Check if the CEO has a long track record of success.")

st.warning("⚠️ Peer-to-peer advice: Historical growth does not guarantee future results. Diversify so you aren't reliant on just one 'bet'.")
