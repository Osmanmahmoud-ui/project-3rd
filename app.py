import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Egypt Plastic Recycling Comparison",
    page_icon="♻️",
    layout="wide"
)

# =======================================================
# DASHBOARD DATA (UNCHANGED)
# =======================================================

EUR_TO_EGP = 62.669

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
    }
])

df["Gross Cost EGP/kg"] = df["Gross Cost EUR/kg"] * EUR_TO_EGP
df["Net Cost EGP/kg"] = df["Net Cost EUR/kg"] * EUR_TO_EGP

# =======================================================
# MARKET DATA (UPDATED)
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

page = st.sidebar.radio("Navigation", ["Dashboard", "Market Engine"])

# =======================================================
# DASHBOARD (NO CHANGES)
# =======================================================

if page == "Dashboard":

    st.title("♻️ Plastic Recycling Pathway Analysis")

    waste = st.number_input("Waste input (kg)", 100, 1000000, 10000)

    df["Output"] = waste * df["Efficiency (%)"] / 100
    df["CO2"] = waste * df["Net GWP kg CO2e/kg"]
    df["Cost"] = waste * df["Net Cost EGP/kg"]

    st.subheader("Efficiency Comparison")
    st.plotly_chart(px.bar(df, x="Method", y="Efficiency (%)"))

    st.subheader("Carbon Impact")
    st.plotly_chart(px.bar(df, x="Method", y="CO2"))

    st.subheader("Cost Analysis")
    st.plotly_chart(px.bar(df, x="Method", y="Cost"))

# =======================================================
# 🌍 MARKET ENGINE (FIXED + UPGRADED)
# =======================================================

else:

    st.title("🌍 Market vs Market Plastic Waste Engine")

    st.markdown("""
    Compare two countries based on plastic waste systems, recycling performance, and infrastructure maturity.
    """)

    st.divider()

    # ---------------- SELECT MARKETS ----------------

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Market 2", market["Market"])

    if m1 == m2:
        st.error("Please select two different markets.")
        st.stop()

    sel = market[market["Market"].isin([m1, m2])].copy()

    # ✅ FIX BUG (NO iloc mismatch)
    a = sel[sel["Market"] == m1].iloc[0]
    b = sel[sel["Market"] == m2].iloc[0]

    st.divider()

    # ===================================================
    # 1. RECYCLING SCALE (FIXED)
    # ===================================================

    st.subheader("🌍 Recycling Scale Comparison")

    scale_df = pd.DataFrame([
        {"Market": m1, "Recycling Rate": a["Recycling"]},
        {"Market": m2, "Recycling Rate": b["Recycling"]}
    ])

    st.plotly_chart(px.bar(scale_df, x="Market", y="Recycling Rate", text="Recycling Rate"))

    st.info("""
    Recycling rate shows how much plastic waste is recovered and reprocessed.
    Higher values = stronger circular economy system.
    """)

    st.divider()

    # ===================================================
    # 2. RADAR SYSTEM
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

    st.plotly_chart(fig)

    st.info("""
    Radar interpretation:
    - Mechanical → clean recycling strength
    - Chemical → advanced processing capability
    - Thermal → mixed waste dependency
    - Sorting → collection efficiency
    - Policy → governance strength

    Larger balanced shape = more advanced circular system.
    """)

    st.divider()

    # ===================================================
    # 3. GAP ANALYSIS
    # ===================================================

    st.subheader("📉 System Gap Analysis")

    st.write(f"Recycling Gap: {b['Recycling'] - a['Recycling']}%")
    st.write(f"Sorting Gap: {b['Sort'] - a['Sort']}")
    st.write(f"Policy Gap: {b['Policy'] - a['Policy']}")

    st.divider()

    # ===================================================
    # 4. ENGINEERING INTERPRETATION (FIXED)
    # ===================================================

    st.subheader("🧠 Engineering Interpretation")

    def compare(name, key):
        av = a[key]
        bv = b[key]

        if av == bv:
            st.write(f"⚖️ Equal performance in {name}")
            return

        better = m1 if av > bv else m2
        st.write(f"✔ {better} is stronger in {name}")

    compare("Recycling Efficiency", "Recycling")
    compare("Sorting System", "Sort")
    compare("Policy Strength", "Policy")
    compare("Mechanical Recycling", "Mech")
    compare("Chemical Recycling", "Chem")
    compare("Thermal Treatment", "Therm")

    st.info("""
    System performance depends on integration of:
    policy + infrastructure + technology, not one factor alone.
    """)

    st.divider()

    # ===================================================
    # 5. CONFIDENCE LEVEL
    # ===================================================

    st.subheader("🔍 Data Confidence")

    conf_map = {"High": 3, "Medium": 2, "Low": 1}

    st.plotly_chart(px.bar(
        sel,
        x="Market",
        y=sel["Conf"].map(conf_map),
        text="Conf"
    ))

    st.divider()

    # ===================================================
    # 6. FINAL RESULT
    # ===================================================

    winner = sel.loc[sel["Recycling"].idxmax(), "Market"]

    st.success(f"🏆 Overall stronger circular system: {winner}")
