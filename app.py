import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Egypt Plastic Recycling Comparison",
    page_icon="♻️",
    layout="wide"
)

# -------------------------------------------------------
# Currency Conversion
# -------------------------------------------------------
EUR_TO_EGP = 62.669

# -------------------------------------------------------
# DASHBOARD DATA (UNCHANGED - DO NOT EDIT)
# -------------------------------------------------------
df = pd.DataFrame([
    {
        "Method": "Mechanical Recycling",
        "Favorite Plastic Type": "PET, HDPE, PP - clean and sorted",
        "Efficiency (%)": 88,
        "Gross GWP kg CO2e/kg": 0.67,
        "Gross CED MJ/kg": 3.83,
        "Gross Cost EUR/kg": 0.10,
        "Net GWP kg CO2e/kg": 0.18,
        "Net CED MJ/kg": -18.14,
        "Net Cost EUR/kg": -0.16,
        "Clean Score": 9,
    },
    {
        "Method": "Chemical Recycling - Pyrolysis",
        "Favorite Plastic Type": "Mixed PE, PP, PS",
        "Efficiency (%)": 75,
        "Gross GWP kg CO2e/kg": 0.96,
        "Gross CED MJ/kg": 15.66,
        "Gross Cost EUR/kg": 0.33,
        "Net GWP kg CO2e/kg": 0.25,
        "Net CED MJ/kg": -15.92,
        "Net Cost EUR/kg": -0.24,
        "Clean Score": 6,
    },
    {
        "Method": "Hybrid Mechanical + Chemical",
        "Favorite Plastic Type": "Mixed + sorted streams",
        "Efficiency (%)": 82,
        "Gross GWP kg CO2e/kg": 0.48,
        "Gross CED MJ/kg": 13.32,
        "Gross Cost EUR/kg": 0.14,
        "Net GWP kg CO2e/kg": -0.22,
        "Net CED MJ/kg": -30.14,
        "Net Cost EUR/kg": -0.29,
        "Clean Score": 10,
    }
])

df["Gross Cost EGP/kg"] = df["Gross Cost EUR/kg"] * EUR_TO_EGP
df["Net Cost EGP/kg"] = df["Net Cost EUR/kg"] * EUR_TO_EGP

# -------------------------------------------------------
# MARKET DATA
# -------------------------------------------------------
market = pd.DataFrame([
    {"Market": "Egypt", "Recycling": 12, "Mech": 7, "Chem": 3, "Therm": 4, "Sort": 4, "Policy": 5, "Conf": "High"},
    {"Market": "EU", "Recycling": 35, "Mech": 8, "Chem": 7, "Therm": 6, "Sort": 9, "Policy": 9, "Conf": "High"},
    {"Market": "Germany", "Recycling": 38, "Mech": 9, "Chem": 7, "Therm": 7, "Sort": 9, "Policy": 9, "Conf": "High"},
    {"Market": "Japan", "Recycling": 25, "Mech": 7, "Chem": 7, "Therm": 8, "Sort": 8, "Policy": 8, "Conf": "High"},
    {"Market": "USA", "Recycling": 9, "Mech": 6, "Chem": 6, "Therm": 5, "Sort": 6, "Policy": 5, "Conf": "Medium"},
    {"Market": "China", "Recycling": 20, "Mech": 7, "Chem": 6, "Therm": 6, "Sort": 6, "Policy": 7, "Conf": "Medium"},
    {"Market": "UAE", "Recycling": 15, "Mech": 6, "Chem": 5, "Therm": 6, "Sort": 6, "Policy": 7, "Conf": "Medium"},
    {"Market": "Global", "Recycling": 9, "Mech": 5, "Chem": 4, "Therm": 5, "Sort": 4, "Policy": 4, "Conf": "Low"},
])

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------
page = st.sidebar.radio("Navigation", ["Dashboard", "Market Engine"])

# -------------------------------------------------------
# DASHBOARD (UNCHANGED)
# -------------------------------------------------------
if page == "Dashboard":

    st.title("♻️ Recycling Technology Comparison")

    waste = st.number_input("Waste input (kg)", 100, 1000000, 10000)

    df["Output"] = waste * df["Efficiency (%)"] / 100
    df["CO2"] = waste * df["Net GWP kg CO2e/kg"]
    df["Cost"] = waste * df["Net Cost EGP/kg"]

    st.plotly_chart(px.bar(df, x="Method", y="Efficiency (%)"))
    st.plotly_chart(px.bar(df, x="Method", y="CO2"))
    st.plotly_chart(px.bar(df, x="Method", y="Cost"))

# -------------------------------------------------------
# 🌍 MARKET ENGINE (ONLY PART EDITED)
# -------------------------------------------------------
else:

    st.title("🌍 Market vs Market Plastic Waste System Engine")

    st.markdown("""
    This engine compares two countries based on plastic waste generation,
    recycling system maturity, and circular economy performance.
    """)

    st.divider()

    # =====================================================
    # MARKET SELECTION
    # =====================================================
    st.subheader("📍 Market Selection")
    st.caption("Choose two markets to compare their waste management systems.")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Select Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Select Market 2", market["Market"])

    if m1 == m2:
        st.error("Please select two different markets.")
        st.stop()

    sel = market[market["Market"].isin([m1, m2])].copy()

    a = sel.iloc[0]
    b = sel.iloc[1]

    st.divider()

    # =====================================================
    # 1. RECYCLING SCALE
    # =====================================================
    st.subheader("🌍 Recycling Scale Comparison")
    st.caption("Compares total recycling performance between the two markets.")

    scale_df = pd.DataFrame([
        {"Market": m1, "Recycling Rate": a["Recycling"]},
        {"Market": m2, "Recycling Rate": b["Recycling"]}
    ])

    st.plotly_chart(px.bar(scale_df, x="Market", y="Recycling Rate", text="Recycling Rate"))

    st.info("""
    💡 Interpretation:
    This metric shows how much plastic waste is successfully recycled.
    Higher values indicate stronger circular economy performance.
    """)

    st.divider()

    # =====================================================
    # 2. SYSTEM RADAR
    # =====================================================
    st.subheader("🧭 Recycling System Maturity Radar")
    st.caption("Compares technological and institutional maturity of each market.")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill='toself',
            name=r["Market"]
        ))

    st.plotly_chart(fig)

    st.info("""
    💡 How to read this radar:

    - Mechanical → clean recycling capability  
    - Chemical → advanced material recovery  
    - Thermal → mixed waste treatment dependency  
    - Sorting → collection efficiency  
    - Policy → governance strength  

    A larger balanced shape = more advanced circular system.
    """)

    st.divider()

    # =====================================================
    # 3. GAP ANALYSIS
    # =====================================================
    st.subheader("📉 System Gap Analysis")
    st.caption("Shows structural differences between the two markets.")

    st.info(f"""
    Recycling Gap: {b['Recycling'] - a['Recycling']}%

    Sorting Gap: {b['Sort'] - a['Sort']}

    Policy Gap: {b['Policy'] - a['Policy']}
    """)

    st.markdown("""
    💡 Interpretation:
    - Recycling gap → overall circularity difference  
    - Sorting gap → infrastructure efficiency difference  
    - Policy gap → regulatory strength difference  
    """)

    st.divider()

    # =====================================================
    # 4. ENGINEERING INSIGHT
    # =====================================================
    st.subheader("🧠 Engineering Interpretation")
    st.caption("Explains system-level meaning of the data.")

    if a["Sort"] < b["Sort"]:
        st.write("✔ Market 2 has stronger sorting infrastructure")

    if a["Policy"] < b["Policy"]:
        st.write("✔ Market 2 has stronger policy enforcement")

    if a["Recycling"] < b["Recycling"]:
        st.write("✔ Market 2 has higher recycling efficiency")

    st.info("""
    💡 Key insight:
    Waste performance is not driven only by technology,
    but by system integration: policy + sorting + infrastructure.
    """)

    st.divider()

    # =====================================================
    # 5. DATA CONFIDENCE
    # =====================================================
    st.subheader("🔍 Data Confidence Level")
    st.caption("Indicates reliability of each market dataset.")

    conf_map = {"High": 3, "Medium": 2, "Low": 1}

    st.plotly_chart(px.bar(
        sel,
        x="Market",
        y=sel["Conf"].map(conf_map),
        text="Conf"
    ))

    st.info("""
    💡 Meaning:
    Higher confidence = more reliable national statistics and lower uncertainty.
    """)

    st.divider()

    # =====================================================
    # 6. FINAL CONCLUSION
    # =====================================================
    st.subheader("🏁 Final System Conclusion")

    winner = sel.loc[sel["Recycling"].idxmax(), "Market"]

    st.success(f"""
    🏆 Final Result:
    {winner} shows stronger circular economy performance due to better system maturity and recycling efficiency.
    """)

    st.divider()

    # =====================================================
    # 📚 REFERENCES SECTION (NEW)
    # =====================================================
    st.subheader("📚 References")

    st.markdown("""
    This analysis is based on international waste and circular economy datasets:

    - OECD (2022) – Global Plastics Outlook  
    - UNEP – Global Waste Management Reports  
    - World Bank – What a Waste 2.0  
    - European Commission – Circular Economy Action Plan  
    - Volk et al. (2021) – Recycling pathway LCA study  
    - International Energy Agency (IEA) – Plastics & Energy Reports  
    - Egypt Environmental Affairs Agency (EEAA) – National Waste Context  

    """)

    st.info("""
    💡 Note:
    All metrics are standardized indicators for comparative system analysis
    and are intended for academic and engineering decision-making purposes.
    """)
