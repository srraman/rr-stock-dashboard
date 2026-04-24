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
            ind_data = yf.Industry(keys["cad" if is_cad_mode else "usd"])
            pool_players = ind_data.top_companies.index.tolist()[:200] 
            
            if is_cad_mode:
                display_players = [t for t in pool_players if ".TO" in t or ".V" in t][:4]
                # ENHANCED FALLBACK: Reliable CAD leaders in Emerging Tech & Industry
                if not display_players:
                    fallback = {
                        "🌀 Quantum & Advanced Tech": ["QNC.V", "D-WAVE.TO"], 
                        "🔌 AI Infrastructure & Chips": ["CLS.TO", "VNP.TO", "POW.V"],
                        "🏦 Core Wealth Compounders": ["RY.TO", "TD.TO", "BN.TO"], 
                        "🔥 Energy & Uranium (AI Fuel)": ["CCO.TO", "DML.TO", "CNQ.TO"],
                        "🏗️ Infrastructure & Rail": ["CNR.TO", "CP.TO"]
                    }
                    display_players = fallback.get(label, [])
            else:
                display_players = [t for t in pool_players if ".TO" not in t][:4]

            if not display_players:
                st.write(f"Searching for {label}...")
                continue

            cols = st.columns(4)
            for i, ticker in enumerate(display_players):
                t_obj = yf.Ticker(ticker)
                # UPDATED: Period set to 2y to focus on recent tech adoption
                hist = t_obj.history(period="2y") 
                if not hist.empty:
                    with cols[i]:
                        curr_p = hist['Close'].iloc[-1]
                        # UPDATED: Growth calculation based on 2-year window
                        growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                        st.line_chart(hist['Close'], height=150)
                time.sleep(0.4) 
        except:
            continue
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)

st.subheader("🧠 Peer-to-Peer Decision Tool")
st.write("2-Year Focus: This removes the 2021 hype spikes and shows who is winning in the actual 2024-2026 commercial era.")
