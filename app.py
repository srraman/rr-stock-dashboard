import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ Live Frontier Discovery Engine")
st.info("Unbiased Protocol: Industry-led scanning. Navigate between CAD and USD tabs below.")

# --- THE DYNAMIC INDUSTRY MAP ---
industries = {
    "🌀 Quantum & Advanced Tech": "computer-hardware",
    "🔌 AI Infrastructure & Chips": "semiconductors",
    "🤖 Software & AI Platforms": "software-infrastructure",
    "🔥 Energy & Uranium (AI Fuel)": "uranium",
    "🏦 Core Wealth Compounders": "banks-diversified",
    "🏗️ Infrastructure & Rail": "railroads"
}

# Create two tabs
tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Dashboard (CAD)", "🇺🇸 US Dashboard (USD)"])

def build_dashboard(is_cad_mode):
    for label, ind_key in industries.items():
        st.header(label)
        try:
            ind_data = yf.Industry(ind_key)
            # CHANGE: Increased from 15 to 100 to find Canadian stocks buried in the global list
            pool_players = ind_data.top_companies.index.tolist()[:100] 
            
            if is_cad_mode:
                # Looks for .TO (Toronto) or .V (Venture)
                display_players = [t for t in pool_players if ".TO" in t or ".V" in t][:4]
            else:
                # Looks for US tickers (no dots)
                display_players = [t for t in pool_players if ".TO" not in t and ".V" not in t][:4]

            if not display_players:
                st.write(f"No major {'CAD' if is_cad_mode else 'USD'} leaders currently in the Top 100.")
                continue

            cols = st.columns(4)
            for i, ticker in enumerate(display_players):
                t_obj = yf.Ticker(ticker)
                hist = t_obj.history(period="5y")
                
                if not hist.empty:
                    with cols[i]:
                        curr_p = hist['Close'].iloc[-1]
                        growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (5Y)")
                        st.line_chart(hist['Close'], height=150)
                
                time.sleep(0.4) 
        except Exception:
            st.write(f"Scanning {label} leaders...")
        st.divider()

# Fill the Tabs
with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)

st.subheader("🧠 Peer-to-Peer Decision Tool")
st.write("Compare the CAD 'Staircases' against the USD leaders to minimize conversion risk.")
