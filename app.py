import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Discovery: Searching TSX & US Exchanges for leaders under $150. No preloaded names.")

# Thematic keywords to drive the dynamic search
discovery_map = {
    "🌀 Quantum & Tech": "Quantum Computing",
    "🔌 AI Infrastructure": "Semiconductor", 
    "🤖 Software & AI": "AI Software",
    "🔥 Energy & Uranium": "Uranium",
    "🏦 Core Wealth": "Bank",
    "🏗️ Infrastructure": "Railroad"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, query_keyword in discovery_map.items():
        st.header(label)
        try:
            # Step 1: Search the live market using the keyword
            # This avoids "global ranking" bias by finding any active ticker with the keyword
            search_query = f"{query_keyword}"
            search = yf.Search(search_query, max_results=25)
            
            valid_stocks = []
            for item in search.quotes:
                ticker = item.get('symbol')
                if not ticker: continue
                
                # STRICT Exchange filter
                if is_cad_mode:
                    if not ticker.endswith((".TO", ".V")): continue
                else:
                    if "." in ticker: continue # Skips .TO, .L, .DE etc.
                
                if len(valid_stocks) >= 4: break
                
                # Step 2: Validate Price and Data
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="2y")
                
                if not hist.empty:
                    curr_p = hist['Close'].iloc[-1]
                    # Filter for affordability and liquidity
                    if curr_p < 150 and hist['Volume'].iloc[-1] > 1000:
                        valid_stocks.append((ticker, hist))
                
                time.sleep(0.1) # Small delay to prevent API lockout

            if not valid_stocks:
                st.warning(f"No {label} leaders under $150 found on this exchange.")
                continue

            # Step 3: Display results
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
