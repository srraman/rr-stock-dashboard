import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Growth Potential Analyzer", layout="wide")

API_KEY = "EM716SRFFX4E4SKM" 

st.title("🛡️ 5-Year Growth & Potential Analyzer")
st.info("Goal: Identify stocks where the business growth matches the price growth.")

def get_growth_data(symbol):
    symbol = symbol.upper().replace(".TO", "")
    # 1. Get Price Data
    url_price = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSX:{symbol}&outputsize=full&apikey={API_KEY}'
    # 2. Get Fundamental Data (Revenue)
    url_rev = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=TSX:{symbol}&apikey={API_KEY}'
    
    try:
        r_p = requests.get(url_price).json()
        r_r = requests.get(url_rev).json()
        
        prices = pd.DataFrame.from_dict(r_p["Time Series (Daily)"], orient='index')
        prices.index = pd.to_datetime(prices.index)
        prices = prices['4. close'].astype(float).sort_index()
        
        # We only want the last 5 years
        five_y = prices[prices.index >= (pd.Timestamp.now() - pd.DateOffset(years=5))]
        
        return {
            "prices": five_y,
            "revenue_growth": r_r.get("QuarterlyRevenueGrowthYOY", "N/A"),
            "profit_margin": r_r.get("ProfitMargin", "N/A"),
            "description": r_r.get("Description", "No description available.")
        }
    except:
        return None

# --- RESEARCH LIST ---
# These 4 represent different 'types' of growth in 2026
research_list = ["CSU.TO", "SHOP.TO", "BN.TO", "CNR.TO"]

for stock in research_list:
    data = get_growth_data(stock)
    if data:
        st.subheader(f"Analysis: {stock}")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.metric("Current Price", f"${data['prices'].iloc[-1]:.2f}")
            st.write(f"**Revenue Growth (YoY):** {data['revenue_growth']}")
        
        with col2:
            growth_pct = ((data['prices'].iloc[-1] - data['prices'].iloc[0]) / data['prices'].iloc[0]) * 100
            st.metric("5-Year Price Growth", f"{growth_pct:.1f}%")
            st.write(f"**Profit Margin:** {data['profit_margin']}")

        with col3:
            st.line_chart(data['prices'])
            
        with st.expander(f"Why consider {stock} for 100x potential?"):
            st.write(data['description'])
        st.divider()
        time.sleep(2) # Stay under 25-search limit

st.subheader("🧠 Peer-to-Peer Decision Tool")
st.markdown("""
### How to spot "Real" Growth vs. "Hype"
1. **The 'Mirror' Test:** If the Price Growth is 500% but Revenue Growth is 0%, the stock is likely **hyped**. If both are growing together, it's a **strong engine**.
2. **The Profit Margin:** Does the company keep a lot of the money it makes? (e.g., CSU.TO has very high margins because software is cheap to replicate).
3. **The 5-Year Floor:** Look at the chart. Even during bad years, does the "floor" of the price keep getting higher? That is the sign of a 10-year winner.
""")
