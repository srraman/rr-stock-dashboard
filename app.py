import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Frontier Discovery CAD/USD", layout="wide")

st.title("🛡️ North American Frontier Engine")
st.info("Unbiased Protocol: Strictly filtering for TSX and Major US Exchanges (NYSE/Nasdaq).")

# Industry keys for North American market discovery
industries = {
    "🌀 Quantum & Advanced Tech": "computer-hardware",
    "🔌 AI Infrastructure & Chips": "semiconductors",
    "🤖 Software & AI Platforms": "software-infrastructure",
    "🔥 Energy & Uranium (AI Fuel)": "uranium",
    "🏦 Core Wealth Compounders": "banks-diversified",
    "🏗️ Infrastructure & Rail": "railroads"
}

tab_cad, tab_usd = st.tabs(["🇨🇦 Canadian Listings (TSX/V)", "🇺🇸 US Listings (NYSE/Nasdaq)"])

def build_dashboard(is_cad_mode):
    for label, ind_key in industries.items():
        st.header(label)
        try:
            ind_data = yf.Industry(ind_key)
            # Search pool of 500 ensures we find CAD players hidden behind US giants
            pool_players = ind_data.top_companies.index.tolist()[:500] 
            
            if is_cad_mode:
                # STRICTOR: Only TSX (.TO) or Venture (.V)
                display_players = [t for t in pool_players if t.endswith((".TO", ".V"))][:4]
            else:
                # STRICTOR: Only Major US (No dots, excluding OTC or International tickers)
                display_players = [t for t in pool_players if "." not in t][:4]

            if not display_players:
                st.warning(f"No major {label} leaders currently qualifying for this exchange.")
                continue

            cols = st.columns(4)
            for i, ticker in enumerate(display_players):
                t_obj = yf.Ticker(ticker)
                # 2-Year window: The most relevant era for AI/Quantum commercialization
                hist = t_obj.history(period="2y") 
                if not hist.empty:
                    with cols[i]:
                        curr_p = hist['Close'].iloc[-1]
                        growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        
                        # Displaying currency based on the exchange detected
                        cur_label = "CAD" if is_cad_mode else "USD"
                        st.metric(label=f"{ticker} ({cur_label})", 
                                  value=f"${curr_p:.2f}", 
                                  delta=f"{growth:.1f}% (2Y)")
                        st.line_chart(hist['Close'], height=150)
                time.sleep(0.4) 
        except:
            st.error(f"Live data for {label} is currently updating...")
        st.divider()

with tab_cad:
    build_dashboard(is_cad_mode=True)

with tab_usd:
    build_dashboard(is_cad_mode=False)
