import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =======================================================
# PAGE CONFIG
# =======================================================
st.set_page_config(
    page_title="Plastic Recycling Market Engine",
    layout="wide"
)

# =======================================================
# MARKET DATA (UPDATED - Global removed + Saudi added)
# =======================================================
market = pd.DataFrame([
    {"Market": "Egypt", "Recycling": 12, "Mech": 7, "Chem": 3, "Therm": 4, "Sort": 4, "Policy": 5, "Conf": "High"},
    {"Market": "EU", "Recycling": 35, "Mech": 8, "Chem": 7, "Therm": 6, "Sort": 9, "Policy": 9, "Conf": "High"},
    {"Market": "Germany", "Recycling": 38, "Mech": 9, "Chem": 7, "Therm": 7, "Sort": 9, "Policy": 9, "Conf": "High"},
    {"Market": "Japan", "Recycling": 25, "Mech": 7, "Chem": 7, "Therm": 8, "Sort": 8, "Policy": 8, "Conf": "High"},
    {"Market": "USA", "Recycling": 9, "Mech": 6, "Chem": 6, "Therm": 5, "Sort": 6, "Policy": 5, "Conf": "Medium"},
    {"Market": "China", "Recycling": 20, "Mech": 7, "Chem": 6, "Therm": 6, "Sort": 6, "Policy": 7, "Conf": "Medium"},
    {"Market": "UAE", "Recycling": 15, "Mech": 6, "Chem": 5, "Therm": 6, "Sort": 6, "Policy": 7, "Conf": "Medium"},
    {"Market": "Saudi Arabia", "Recycling": 18, "Mech": 6, "Chem": 5, "Therm": 6, "Sort": 6, "Policy": 7, "Conf": "Medium"}
])

# =======================================================
# SIDEBAR
# =======================================================
page = st.sidebar.radio("Navigation", ["Market Engine"])

# =======================================================
# MARKET ENGINE
# =======================================================
if page == "Market Engine":

    st.title("🌍 Plastic Waste Market Comparison Engine")

    st.markdown("""
    This engine compares two markets across recycling performance,
    system maturity, and waste management structure.
    """)

    st.divider()

    # ===================================================
    # MARKET SELECTION
    # ===================================================
    st.subheader("📍 Select Markets")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Market 2", market["Market"])

    if m1 == m2:
        st.error("Please select two different markets.")
        st.stop()

    sel = market[market["Market"].isin([m1, m2])].copy()

    # FIX: safe indexing (NO iloc bug)
    a = sel[sel["Market"] == m1].iloc[0]
    b = sel[sel["Market"] == m2].iloc[0]

    st.divider()

    # ===================================================
    # 1. RECYCLING SCALE (FIXED BUG HERE)
    # ===================================================
    st.subheader("🌍 Recycling Scale Comparison")

    scale_df = pd.DataFrame([
        {"Market": m1, "Recycling Rate": a["Recycling"]},
        {"Market": m2, "Recycling Rate": b["Recycling"]}
    ])

    fig = px.bar(
        scale_df,
        x="Market",
        y="Recycling Rate",
        text="Recycling Rate",
        title="Plastic Recycling Rate Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    💡 Interpretation:
    Recycling rate shows how much plastic waste is successfully recovered.

    Higher value = stronger circular economy performance.
    """)

    st.divider()

    # ===================================================
    # 2. SYSTEM RADAR
    # ===================================================
    st.subheader("🧭 System Maturity Radar")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill='toself',
            name=r["Market"]
        ))

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    💡 Radar Meaning:

    - Mechanical → clean recycling strength  
    - Chemical → advanced material recovery  
    - Thermal → mixed waste dependence  
    - Sorting → collection efficiency  
    - Policy → governance strength  

    Bigger balanced shape = more mature circular system.
    """)

    st.divider()

    # ===================================================
    # 3. GAP ANALYSIS
    # ===================================================
    st.subheader("📉 System Gap Analysis")

    st.write(f"Recycling Gap: {b['Recycling'] - a['Recycling']}%")
    st.write(f"Sorting Gap: {b['Sort'] - a['Sort']}")
    st.write(f"Policy Gap: {b['Policy'] - a['Policy']}")

    st.markdown("""
    💡 Interpretation:

    - Recycling gap → overall system efficiency difference  
    - Sorting gap → infrastructure difference  
    - Policy gap → regulation strength difference  
    """)

    st.divider()

    # ===================================================
    # 4. ENGINEERING INTERPRETATION (FIXED - NO BIAS)
    # ===================================================
    st.subheader("🧠 Engineering Interpretation")

    def compare(metric_name, key):

        a_val = a[key]
        b_val = b[key]

        if a_val == b_val:
            st.write(f"⚖️ Both markets are equal in {metric_name}")
            return

        better = m1 if a_val > b_val else m2
        gap = abs(a_val - b_val)

        st.write(f"✔ {better} performs better in {metric_name} (gap: {gap})")

    compare("Recycling Efficiency", "Recycling")
    compare("Sorting System", "Sort")
    compare("Policy Strength", "Policy")
    compare("Mechanical Recycling", "Mech")
    compare("Chemical Recycling", "Chem")
    compare("Thermal Dependency", "Therm")

    st.info("""
    💡 Key Insight:
    Waste systems are multi-layered.
    No single country is “best” overall — performance depends on system component.
    """)

    st.divider()

    # ===================================================
    # 5. DATA CONFIDENCE
    # ===================================================
    st.subheader("🔍 Data Confidence Level")

    conf_map = {"High": 3, "Medium": 2, "Low": 1}

    st.plotly_chart(px.bar(
        sel,
        x="Market",
        y=sel["Conf"].map(conf_map),
        text="Conf"
    ))

    st.info("""
    💡 Meaning:
    Higher confidence = more reliable data sources and lower uncertainty.
    """)

    st.divider()

    # ===================================================
    # 6. FINAL CONCLUSION
    # ===================================================
    st.subheader("🏁 Final Conclusion")

    winner = sel.loc[sel["Recycling"].idxmax(), "Market"]

    st.success(f"""
    Overall Winner (based on recycling rate):

    🏆 {winner}

    This reflects stronger circular economy performance and better system efficiency.
    """)
