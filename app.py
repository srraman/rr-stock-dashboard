import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Discovery: Scanning TSX & US Exchanges for 'Staircase' leaders under $150.")

# Discovery Map: Using keywords that trigger both Large-Cap and Junior TSX leaders
discovery_map = {
    "🌀 Quantum & Tech": ["Quantum", "Technology", "Robotics"],
    "🔌 AI Infrastructure": ["Semiconductor", "Data Center", "Engineering"], 
    "🤖 Software & AI": ["Software", "Artificial Intelligence"],
    "🔥 Energy & Uranium": ["Uranium", "Energy Transition", "Nuclear"],
    "🏦 Core Wealth": ["Bank", "Insurance", "Financial"],
    "🏗️ Infrastructure": ["Railroad", "Construction", "Infrastructure"]
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, keywords in discovery_map.items():
        st.header(label)
        try:
            # Step 1: Broad Search for the Sector
            query = f"{keywords[0]} {'Canada' if is_cad_mode else 'USA'}"
            search = yf.Search(query, max_results=25)
            
            valid_stocks = []
            for item in search.quotes:
                ticker = item.get('symbol')
                if not ticker: continue
                
                # STRICT Exchange filter (Force TSX/V for Canada)
                if is_cad_mode:
                    if not ticker.endswith((".TO", ".V")): continue
                else:
                    if "." in ticker: continue 
                
                if len(valid_stocks) >= 4: break
                
                # Step 2: Fetch 2-Year Data
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    curr_p = hist['Close'].iloc[-1]
                    # Filter for affordability (<$150) and basic trading activity
                    if curr_p < 150 and hist['Volume'].iloc[-1] > 500:
                        valid_stocks.append((ticker, hist))
                
                time.sleep(0.1) # Protect against API throttling

            if not valid_stocks:
                st.write(f"No active {label} leaders found under $150 on this exchange.")
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
