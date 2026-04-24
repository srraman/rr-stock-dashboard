import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Protocol: Scanning live exchange data for leaders under $150. No hard-coded lists.")

# These keywords drive the discovery engine without pre-defining winners
discovery_logic = {
    "🌀 Quantum & Tech": "Technology",
    "🔌 AI Infrastructure": "Semiconductor", 
    "🤖 Software & AI": "Software",
    "🔥 Energy & Uranium": "Uranium",
    "🏦 Core Wealth": "Bank",
    "🏗️ Infrastructure": "Railroad"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    # This prevents the 'Waiting for data' block by using a more efficient search
    for label, keyword in discovery_logic.items():
        st.header(label)
        try:
            # Step 1: Dynamic Discovery
            # We search for the sector + the specific region to force exchange isolation
            region = "Canada" if is_cad_mode else "USA"
            search_query = f"{keyword} {region}"
            discovery = yf.Search(search_query, max_results=15).quotes
            
            valid_stocks = []
            for item in discovery:
                ticker = item.get('symbol')
                if not ticker: continue
                
                # Step 2: Strict Exchange & Price Filtering
                if is_cad_mode:
                    if not (ticker.endswith(".TO") or ticker.endswith(".V")): continue
                else:
                    if "." in ticker: continue # Skips international/CAD on US tab
                
                if len(valid_stocks) >= 3: break
                
                # Step 3: Performance Validation
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    curr_p = hist['Close'].iloc[-1]
                    # Only show if accessible (<$150)
                    if curr_p < 150:
                        valid_stocks.append((ticker, hist))
                time.sleep(0.1)

            if not valid_stocks:
                st.write(f"Scanning {label} for local leaders under $150...")
                continue

            # Step 4: UI Generation
            cols = st.columns(3)
            for i, (ticker, hist) in enumerate(valid_stocks):
                with cols[i]:
                    curr_p = hist['Close'].iloc[-1]
                    growth = ((curr_p - hist.iloc[0]['Close']) / hist.iloc[0]['Close']) * 100
                    st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                    st.line_chart(hist['Close'], height=150)
        except:
            continue
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
