import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Protocol: Scanning the top 500 companies per sector. No hand-picked stocks.")

# --- DYNAMIC SECTOR & ETF CONFIG ---
sectors = {
    "🌀 Quantum & Advanced Tech": {"ind": "computer-hardware", "cad_etf": "HURA.TO", "usd_etf": "QTUM"},
    "🔌 AI Infrastructure & Chips": {"ind": "semiconductors", "cad_etf": "ARTI.TO", "usd_etf": "SOXX"},
    "🤖 Software & AI Platforms": {"ind": "software-infrastructure", "cad_etf": "TEC.TO", "usd_etf": "IGV"},
    "🔥 Energy & Uranium (AI Fuel)": {"ind": "uranium", "cad_etf": "XETM.TO", "usd_etf": "URA"},
    "🏦 Core Wealth Compounders": {"ind": "banks-diversified", "cad_etf": "XFN.TO", "usd_etf": "KBE"},
    "🏗️ Infrastructure & Rail": {"ind": "railroads", "cad_etf": "XMA.TO", "usd_etf": "IYT"}
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    sector_momentum = {}
    
    for label, config in sectors.items():
        st.header(label)
        
        # --- PART 1: THEMATIC ETF ---
        etf_ticker = config["cad_etf"] if is_cad_mode else config["usd_etf"]
        try:
            etf_obj = yf.Ticker(etf_ticker)
            etf_hist = etf_obj.history(period="2y")
            if not etf_hist.empty:
                e_col1, e_col2 = st.columns([1, 3])
                with e_col1:
                    e_curr = etf_hist['Close'].iloc[-1]
                    e_growth = ((e_curr - etf_hist['Close'].iloc[0]) / etf_hist['Close'].iloc[0]) * 100
                    st.metric(label=f"Sector ETF: {etf_ticker}", value=f"${e_curr:.2f}", delta=f"{e_growth:.1f}% (2Y)")
                    sector_momentum[label] = e_growth
                with e_col2:
                    st.line_chart(etf_hist['Close'], height=100)
        except:
            continue

        # --- PART 2: DYNAMIC COMPANY DISCOVERY ---
        try:
            ind_data = yf.Industry(config["ind"])
            # Depth 500 ensures we find CAD leaders like CCO or SHOP hidden in the global list
            pool_players = ind_data.top_companies.index.tolist()[:500] 
            
            if is_cad_mode:
                display_players = [t for t in pool_players if t.endswith((".TO", ".V"))][:4]
            else:
                display_players = [t for t in pool_players if "." not in t][:4]

            if display_players:
                cols = st.columns(4)
                for i, ticker in enumerate(display_players):
                    t_obj = yf.Ticker(ticker)
                    hist = t_obj.history(period="2y") 
                    if not hist.empty:
                        with cols[i]:
                            curr_p = hist['Close'].iloc[-1]
                            growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                            st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                            st.line_chart(hist['Close'], height=120)
                    time.sleep(0.3)
            else:
                st.warning(f"No major {label} leaders found in the Top 500 for this exchange.")
        except:
            continue
        st.divider()
    
    # --- DYNAMIC SUGGESTION ENGINE ---
    if sector_momentum:
        st.subheader("💡 Data-Driven Momentum Signal")
        top_sector = max(sector_momentum, key=sector_momentum.get)
        st.success(f"Based on 2-year data, **{top_sector}** is currently showing the strongest sector-wide momentum (+{sector_momentum[top_sector]:.1f}%).")

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
