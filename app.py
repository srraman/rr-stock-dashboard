import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Discovery: Dynamic searching for TSX & US Leaders under $150.")

# Dynamic sector mapping
industries = {
    "🌀 Quantum & Tech": "Technology",
    "🔌 AI Infrastructure": "Semiconductors", 
    "🤖 Software & AI": "Software—Infrastructure",
    "🔥 Energy & Uranium": "Uranium",
    "🏦 Core Wealth": "Banks—Diversified",
    "🏗️ Infrastructure": "Railroads"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, sector_key in industries.items():
        st.header(label)
        try:
            # Step 1: Broad search for active stocks in the sector
            # Using yf.Search to find current trending tickers without hardcoding
            query = f"{sector_key} {'Canada' if is_cad_mode else 'USA'}"
            search_results = yf.Search(query, max_results=20).quotes
            
            valid_stocks = []
            for item in search_results:
                ticker = item['symbol']
                
                # Filter strictly by exchange
                if is_cad_mode and not ticker.endswith((".TO", ".V")): continue
                if not is_cad_mode and "." in ticker: continue
                
                if len(valid_stocks) >= 4: break
                
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    curr_p = hist['Close'].iloc[-1]
                    # PRICE & LIQUIDITY FILTER: Under $150 and has trading volume
                    if curr_p < 150 and hist['Volume'].iloc[-1] > 1000:
                        valid_stocks.append((ticker, hist))
                time.sleep(0.1)

            if not valid_stocks:
                st.write(f"Scanning market for {label} leaders...")
                continue

            cols = st.columns(4)
            for i, (ticker, hist) in enumerate(valid_stocks):
                with cols[i]:
                    curr_p = hist['Close'].iloc[-1]
                    growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                    st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                    st.line_chart(hist['Close'], height=150)
        except:
            continue
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
