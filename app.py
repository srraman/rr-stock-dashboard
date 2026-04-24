import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Discovery: Searching TSX/V and US Exchanges for leaders under $150.")

# Discovery Map: Using specific keywords that trigger Canadian junior tech
discovery_map = {
    "🌀 Quantum & Tech": "Quantum Computing Canada",
    "🔌 AI Infrastructure": "AI Infrastructure TSX", 
    "🤖 Software & AI": "AI Software Platforms Canada",
    "🔥 Energy & Uranium": "Uranium Mining Canada",
    "🏦 Core Wealth": "Bank Canada",
    "🏗️ Infrastructure": "Engineering Infrastructure Canada"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, query_keyword in discovery_map.items():
        st.header(label)
        try:
            # Step 1: Live Market Search
            search = yf.Search(query_keyword, max_results=20)
            
            valid_stocks = []
            for item in search.quotes:
                ticker = item.get('symbol')
                if not ticker: continue
                
                # STRICT Exchange filter
                if is_cad_mode:
                    if not ticker.endswith((".TO", ".V")): continue
                else:
                    if "." in ticker: continue 
                
                if len(valid_stocks) >= 4: break
                
                # Step 2: Fetch Data
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    curr_p = hist['Close'].iloc[-1]
                    # Filter for affordability (<$150)
                    if curr_p < 150:
                        valid_stocks.append((ticker, hist))
                
                time.sleep(0.1)

            if not valid_stocks:
                st.warning(f"No {label} leaders under $150 currently active.")
                continue

            # Step 3: UI Layout
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
        except Exception:
            continue
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
