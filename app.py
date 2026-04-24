import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Protocol: Scanning TSX & US Exchanges. Displaying leaders priced under $150.")

# Dynamic Industry IDs
industries = {
    "🌀 Quantum & Advanced Tech": "computer-hardware",
    "🔌 AI Infrastructure & Chips": "semiconductors", 
    "🤖 Software & AI Platforms": "software-infrastructure",
    "🔥 Energy & Uranium (AI Fuel)": "uranium",
    "🏦 Core Wealth Compounders": "banks-diversified",
    "🏗️ Infrastructure & Rail": "railroads"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, ind_key in industries.items():
        st.header(label)
        try:
            ind_data = yf.Industry(ind_key)
            # Search a very deep pool to find CAD names and mid-priced US names
            pool_players = ind_data.top_companies.index.tolist()[:750] 
            
            # Filter by Exchange
            if is_cad_mode:
                exchange_players = [t for t in pool_players if t.endswith((".TO", ".V"))]
            else:
                exchange_players = [t for t in pool_players if "." not in t]

            valid_stocks = []
            
            # Filter by Price and Data Quality
            for ticker in exchange_players:
                if len(valid_stocks) >= 4: break # We only need the top 4 per sector
                
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    # PRICE CEILING: Only show stocks under $150 (CAD or USD)
                    if current_price < 150:
                        valid_stocks.append((ticker, hist))
                time.sleep(0.1) # Rapid scan delay

            if not valid_stocks:
                st.warning(f"No leaders under $150 found for {label} on this exchange.")
                continue

            cols = st.columns(4)
            for i, (ticker, hist) in enumerate(valid_stocks):
                with cols[i]:
                    curr_p = hist['Close'].iloc[-1]
                    growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                    currency = "CAD" if is_cad_mode else "USD"
                    
                    st.metric(label=f"{ticker} ({currency})", 
                              value=f"${curr_p:.2f}", 
                              delta=f"{growth:.1f}% (2Y)")
                    st.line_chart(hist['Close'], height=150)
        except:
            continue
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
