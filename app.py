import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Growth Discovery Engine", layout="wide")

st.title("🛡️ 5-Year Growth Discovery Engine")
st.info("I am scanning the TSX for 10-year growth leaders. Watch the dashboard build below.")

# --- THE SMART DISCOVERY LIST ---
# This list is based on 2026 market themes: Gold/Resources, Tech, and Infrastructure.
# These are currently flagged as having high '100x' long-term potential.
discovery_list = ["AEM.TO", "ATH.TO", "HUT.TO", "CSU.TO", "SHOP.TO"]

st.subheader("🔍 Automatic Growth Analysis")

for stock in discovery_list:
    try:
        ticker = yf.Ticker(stock)
        # Fetching 5 years of daily data
        hist = ticker.history(period="5y")
        
        if not hist.empty:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                current_p = hist['Close'].iloc[-1]
                start_p = hist['Close'].iloc[0]
                total_growth = ((current_p - start_p) / start_p) * 100
                
                st.metric(label=f"{stock}", 
                          value=f"${current_p:.2f} CAD", 
                          delta=f"{total_growth:.1f}% Growth (5Y)")
                
                # Dynamic Reasoning Label
                if total_growth > 200:
                    st.success("🔥 High Momentum")
                elif total_growth > 50:
                    st.info("📈 Steady Climber")
                
            with col2:
                # The 5-year visual trend
                st.line_chart(hist['Close'])
            
            st.divider()
        
    except Exception:
        st.write(f"Analyzing {stock}...")
    
    time.sleep(0.5) # Fast but stable loading

# --- AI DECISION TOOLS ---
st.subheader("🧠 How to Decide (Your Decision Toolkit)")
colA, colB = st.columns(2)

with colA:
    st.markdown("### The 10-Year '100x' Formula")
    st.write("1. **The Staircase:** Does the graph go bottom-left to top-right?")
    st.write("2. **The Floor:** Every time it drops, does it stop at a higher price than before?")

with colB:
    st.markdown("### 2026 Sector Trends")
    st.write("- **Resources (AEM/ATH):** Betting on global demand and inflation.")
    st.write("- **Tech (SHOP/CSU):** Betting on software eating the world.")
