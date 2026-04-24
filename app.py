import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Live Frontier Discovery", layout="wide")

st.title("🛡️ Live Frontier Discovery Engine")
st.info("Unbiased Protocol: Tracking live industry leaders with CAD/USD detection.")

# --- THE DYNAMIC INDUSTRY MAP ---
industries = {
    "🌀 Quantum & Advanced Tech": "computer-hardware",
    "🔌 AI Infrastructure & Chips": "semiconductors",
    "🤖 Software & AI Platforms": "software-infrastructure",
    "🔥 Energy & Uranium (AI Fuel)": "uranium",
    "🏦 Core Wealth Compounders": "banks-diversified",
    "🏗️ Infrastructure & Rail": "railroads"
}

for label, ind_key in industries.items():
    st.header(label)
    try:
        # Step 1: Query the actual industry for its current leaders
        ind_data = yf.Industry(ind_key)
        top_players = ind_data.top_companies.index.tolist()[:4] 
        
        cols = st.columns(4)
        for i, ticker in enumerate(top_players):
            t_obj = yf.Ticker(ticker)
            hist = t_obj.history(period="5y")
            
            if not hist.empty:
                with cols[i]:
                    # --- NEW CAD UPDATE START ---
                    # Check the ticker or the info to see if it's Canadian
                    # .TO means Toronto, .V means Venture. Both are CAD.
                    is_cad = ".TO" in ticker or ".V" in ticker or t_obj.info.get('currency') == 'CAD'
                    currency_label = "CAD" if is_cad else "USD"
                    # --- NEW CAD UPDATE END ---

                    curr_p = hist['Close'].iloc[-1]
                    growth = ((curr_p - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                    
                    # Displaying the currency clearly so you don't pay surprises
                    st.metric(
                        label=f"{ticker} ({currency_label})", 
                        value=f"${curr_p:.2f}", 
                        delta=f"{growth:.1f}% (5Y)"
                    )
                    st.line_chart(hist['Close'], height=150)
            
            time.sleep(0.5) 
    except Exception:
        st.write(f"Scanning the {label} sector...")
    st.divider()

st.subheader("🧠 Peer-to-Peer Decision Tool")
st.write("Look for the (CAD) tag to avoid conversion fees. If a (USD) stock has a much stronger 'Staircase' than the CAD options, that's when you decide if the fee is worth the growth.")
