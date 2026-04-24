import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Discovery: Independent sector scanning for TSX and US markets. Price Cap: $150.")

# Dynamic sector mapping using high-confidence keywords
sectors = {
    "🌀 Quantum & Advanced Tech": ["Quantum", "Tech", "Robotics"],
    "🔌 AI Infrastructure & Chips": ["Semiconductor", "Infrastructure", "Power"], 
    "🤖 Software & AI Platforms": ["AI Software", "Enterprise Software"],
    "🔥 Energy & Uranium (AI Fuel)": ["Uranium", "Nuclear", "Energy Transition"],
    "🏦 Core Wealth Compounders": ["Bank", "Finance", "Insurance"],
    "🏗️ Infrastructure & Rail": ["Rail", "Construction", "Engineering"]
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, keywords in sectors.items():
        st.header(label)
        try:
            # Step 1: Independent Market Discovery
            # We add 'Canada' or 'USA' to force the search engine out of its global bias
            search_term = f"{keywords[0]} {'Canada' if is_cad_mode else 'USA'}"
            discovery = yf.Search(search_term, max_results=15)
            
            valid_results = []
            for item in discovery.quotes:
                ticker = item.get('symbol')
                if not ticker: continue
                
                # STRICT REGIONAL ENFORCEMENT
                if is_cad_mode:
                    if not ticker.endswith((".TO", ".V")): continue
                else:
                    if "." in ticker: continue # Eliminates .TO, .L, .DE, etc.
                
                if len(valid_results) >= 4: break
                
                # Step 2: Live Price & 2-Year Growth Validation
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    # Price Cap for accessibility
                    if current_price < 150:
                        valid_results.append((ticker, hist))
                
                time.sleep(0.2) # API Protection

            if not valid_results:
                st.warning(f"No {label} leaders under $150 found on this exchange.")
                continue

            # Step 3: UI Output
            cols = st.columns(4)
            for i, (ticker, hist) in enumerate(valid_results):
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
