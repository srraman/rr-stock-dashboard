import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ Live Frontier Discovery Engine")
st.info("Unbiased Protocol: Industry-led scanning. Navigate between CAD and USD tabs below.")

# --- THE DYNAMIC SECTOR MAP ---
# For CAD, we use 'Index' tickers to find the top Canadian players.
# For USD, we use 'Industry' keys for the global leaders.
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
            # We use a broader search (Top 200) to find CAD companies buried in global data
            ind_data = yf.Industry(keys["cad" if is_cad_mode else "usd"])
            pool_players = ind_data.top_companies.index.tolist()[:200] 
            
            if is_cad_mode:
                display_players = [t for t in pool_players if ".TO" in t or ".V" in t][:4]
                # FALLBACK: If the industry search fails for CAD, we use reliable Canadian anchors
                if not display_players:
                    fallback = {"🏦 Core Wealth Compounders": ["RY.TO", "TD.TO", "BN.TO"], 
                                "🔥 Energy & Uranium (AI Fuel)": ["CCO.TO", "DML.TO", "CNQ.TO"],
                                "🏗️ Infrastructure & Rail": ["CNR.TO", "CP.TO"]}
                    display_players = fallback.get(label, [])
            else:
                display_players = [t for t in pool_players if ".TO" not in t][:4]

            if not display_players:
                st.write(f"Scanning market for {label}...")
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
        except:
            continue
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
