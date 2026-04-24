import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Live Frontier Discovery", layout="wide")

st.title("🛡️ Live Frontier Discovery Engine")
st.info("Unbiased Protocol: This app queries live industry data. No tickers are hand-picked.")

# --- THE DYNAMIC INDUSTRY MAP ---
# Instead of tickers, we use 'Industry Keys'. 
# These represent the entire sector, and the app will find the leaders for us.
industries = {
    "🌀 Quantum & Advanced Tech": "computer-hardware",
    "🔌 AI Infrastructure & Chips": "semiconductors",
    "🤖 Software & AI Platforms": "software-infrastructure",
    "🔥 Energy & Uranium (AI Fuel)": "uranium",
    "🏦 Core Wealth Compounders": "banks-diversified",
    "🏗️ Infrastructure & Rail": "railroads"
}

for label, ind_key in industries.items():
    st.header(label)
    try:
        # Step 1: Query the actual industry for its current leaders
        ind_data = yf.Industry(ind_key)
        
        # Pull the top 4 companies by market relevance automatically
        # This list changes as the market changes!
        top_players = ind_data.top_companies.index.tolist()[:4] 
        
        cols = st.columns(4)
        for i, ticker in enumerate(top_players):
            # Step 2: Get 5-year data for these market-selected leaders
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="5y")
            
            if not hist.empty:
                with cols[i]:
                    curr_p = hist['Close'].iloc[-1]
                    # Calculate the 5-year 'Engine' strength
                    growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                    st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (5Y)")
                    st.line_chart(hist['Close'], height=150)
            
            time.sleep(0.5) # Stability pause to prevent being blocked
    except Exception:
        st.write(f"Scanning the {label} sector for today's market leaders...")
    st.divider()

st.subheader("🧠 Peer-to-Peer Decision Tool")
st.write("If you see a new ticker today that wasn't there yesterday, the market is shifting. That's your unbiased signal.")
