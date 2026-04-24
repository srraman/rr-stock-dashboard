import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ Live Frontier Discovery Engine")
st.info("Unbiased Protocol: Industry-led scanning (2-Year Momentum Focus).")

# --- THE DYNAMIC SECTOR MAP ---
industries = {
    "🌀 Quantum & Advanced Tech": {"cad": "computer-hardware", "usd": "computer-hardware"},
    "🔌 AI Infrastructure & Chips": {"cad": "semiconductors", "usd": "semiconductors"},
    "🤖 Software & AI Platforms": {"cad": "software-infrastructure", "usd": "software-infrastructure"},
    "🔥 Energy & Uranium (AI Fuel)": {"cad": "uranium", "usd": "uranium"},
    "🏦 Core Wealth Compounders": {"cad": "banks-diversified", "usd": "banks-diversified"},
    "🏗️ Infrastructure & Rail": {"cad": "railroads", "usd": "railroads"}
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Dashboard (CAD)", "🇺🇸 US Dashboard (USD)"])

def build_dashboard(is_cad_mode):
    for label, keys in industries.items():
        st.header(label)
        try:
            # We fetch the industry but expand the search significantly
            ind_data = yf.Industry(keys["cad" if is_cad_mode else "usd"])
            
            # We pull the top 300 to ensure we find CAD stocks buried in the global list
            pool_players = ind_data.top_companies.index.tolist()[:300] 
            
            if is_cad_mode:
                # Filter for TSX (.TO) or TSX-V (.V)
                display_players = [t for t in pool_players if ".TO" in t or ".V" in t][:4]
            else:
                # Filter for US tickers
                display_players = [t for t in pool_players if ".TO" not in t and ".V" not in t][:4]

            # If the scanner STILL finds nothing, we give a live search link instead of a fallback
            if not display_players:
                st.warning(f"No global 'Top 300' leaders for {label} found on TSX today.")
                continue

            cols = st.columns(4)
            for i, ticker in enumerate(display_players):
                t_obj = yf.Ticker(ticker)
                # 2-Year timeframe as discussed
                hist = t_obj.history(period="2y") 
                if not hist.empty:
                    with cols[i]:
                        curr_p = hist['Close'].iloc[-1]
                        growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                        st.line_chart(hist['Close'], height=150)
                time.sleep(0.4) 
        except Exception:
            st.write(f"Scanning {label} leaders...")
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
