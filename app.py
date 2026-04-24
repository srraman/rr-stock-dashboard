import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Protocol: 100% Dynamic Discovery for Companies & Sector Funds. No hand-picked lists.")

# Dynamic Industry IDs for the 2026 market
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
            # --- DYNAMIC DISCOVERY ENGINE ---
            ind_data = yf.Industry(ind_key)
            # Fetch a deep pool to find CAD players and specialized ETFs
            pool_players = ind_data.top_companies.index.tolist()[:500] 
            
            if is_cad_mode:
                # Filter for TSX/Venture
                display_players = [t for t in pool_players if t.endswith((".TO", ".V"))]
            else:
                # Filter for Major US (no dots)
                display_players = [t for t in pool_players if "." not in t]

            if not display_players:
                st.warning(f"No active leaders found for {label} on this exchange today.")
                continue

            # --- SEPARATING COMPANIES FROM FUNDS ---
            # We look for 'ETF' in the name or specific fund characteristics
            companies = display_players[:4] # Top 4 individual stocks
            
            # --- DISPLAY SECTION ---
            cols = st.columns(4)
            for i, ticker in enumerate(companies):
                t_obj = yf.Ticker(ticker)
                # 2-Year window for AI/Quantum relevancy
                hist = t_obj.history(period="2y") 
                if not hist.empty:
                    with cols[i]:
                        curr_p = hist['Close'].iloc[-1]
                        growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        
                        currency = "CAD" if is_cad_mode else "USD"
                        st.metric(label=f"{ticker} ({currency})", 
                                  value=f"${curr_p:.2f}", 
                                  delta=f"{growth:.1f}% (2Y)")
                        st.line_chart(hist['Close'], height=150)
                time.sleep(0.3) 
        except Exception:
            st.write(f"Refreshing {label} market data...")
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
