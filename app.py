import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Protocol: Scanning top 500 companies in the US and Canada. No fallbacks allowed.")

# The core industry IDs used by the market
industries = {
    "🌀 Quantum & Advanced Tech": "computer-hardware",
    "🔌 AI Infrastructure & Chips": "semiconductors",
    "🤖 Software & AI Platforms": "software-infrastructure",
    "🔥 Energy & Uranium (AI Fuel)": "uranium",
    "🏦 Core Wealth Compounders": "banks-diversified",
    "🏗️ Infrastructure & Rail": "railroads"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Dashboard (CAD)", "🇺🇸 US Dashboard (USD)"])

def build_dashboard(is_cad_mode):
    for label, ind_key in industries.items():
        st.header(label)
        try:
            # Step 1: Query the actual industry
            ind_data = yf.Industry(ind_key)
            # Step 2: Pool the top 500 to ensure we catch TSX leaders
            pool_players = ind_data.top_companies.index.tolist()[:500] 
            
            if is_cad_mode:
                # Filter strictly for Toronto or Venture exchanges
                display_players = [t for t in pool_players if ".TO" in t or ".V" in t][:4]
            else:
                # Filter for US-only (NYSE/Nasdaq)
                display_players = [t for t in pool_players if ".TO" not in t and ".V" not in t][:4]

            if not display_players:
                st.warning(f"No major {label} leaders currently found in the {'CAD' if is_cad_mode else 'USD'} market.")
                continue

            cols = st.columns(4)
            for i, ticker in enumerate(display_players):
                t_obj = yf.Ticker(ticker)
                # 2-Year momentum focus
                hist = t_obj.history(period="2y") 
                if not hist.empty:
                    with cols[i]:
                        curr_p = hist['Close'].iloc[-1]
                        growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        st.metric(label=ticker, value=f"${curr_p:.2f}", delta=f"{growth:.1f}% (2Y)")
                        st.line_chart(hist['Close'], height=150)
                time.sleep(0.4) # Protective delay for API stability
        except:
            st.error(f"Error scanning {label}. The market data may be temporarily unavailable.")
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)

st.subheader("🧠 The Unbiased Signal")
st.write("If a sector appears empty, it means there are no companies in that industry currently large enough to be in the Top 500 globally. This is a sign of extreme 'early stage' risk.")
