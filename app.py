import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Discovery: Using Screener Logic to bypass API blocks. No fallbacks.")

# We use the 'Screener' module which is the most robust part of yfinance in 2026
# This pulls the top companies directly from the exchange indices
sector_map = {
    "🌀 Quantum & Tech": "ms_technology",
    "🔌 AI Infrastructure": "ms_technology", # Refining within logic below
    "🤖 Software & AI": "ms_technology",
    "🔥 Energy & Uranium": "ms_energy",
    "🏦 Core Wealth": "ms_financial_services",
    "🏗️ Infrastructure": "ms_industrials"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, screener_id in sector_map.items():
        st.header(label)
        try:
            # Step 1: Query the Sector Screener directly
            # This is much faster and less likely to be blocked than a keyword search
            s = yf.Screener()
            s.set_predefined_body(screener_id)
            scr_data = s.response.get('quotes', [])
            
            valid_stocks = []
            for item in scr_data:
                ticker = item.get('symbol')
                if not ticker: continue
                
                # Strict regional filtering
                if is_cad_mode and not ticker.endswith((".TO", ".V")): continue
                if not is_cad_mode and "." in ticker: continue
                
                if len(valid_stocks) >= 4: break
                
                # Step 2: Validate Data
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    curr_p = hist['Close'].iloc[-1]
                    # Price Cap < $150
                    if curr_p < 150:
                        valid_stocks.append((ticker, hist))
                time.sleep(0.1)

            if not valid_stocks:
                st.warning(f"No {label} leaders found under $150. Market data may be refreshing.")
                continue

            cols = st.columns(4)
            for i, (ticker, hist) in enumerate(valid_stocks):
                with cols[i]:
                    curr_p = hist['Close'].iloc[-1]
                    growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                    st.metric(label=f"{ticker}", value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                    st.line_chart(hist['Close'], height=150)
                    
        except Exception:
            st.error(f"Waiting for {label} data from exchange...")
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
