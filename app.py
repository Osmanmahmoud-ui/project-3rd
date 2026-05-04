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
# Currency
# -------------------------------------------------------
EUR_TO_EGP = 62.669

# -------------------------------------------------------
# DASHBOARD DATA (UNCHANGED)
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
# MARKET DATA (EXPANDED)
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
# 🏆 MARKET ENGINE (SAFE + JURY VERSION)
# -------------------------------------------------------
else:

    st.title("🌍 Circular Economy Jury Engine")

    c1, c2 = st.columns(2)

    with c1:
        m1 = st.selectbox("Market 1", market["Market"])

    with c2:
        m2 = st.selectbox("Market 2", market["Market"])

    # ---------------------------------------------------
    # SAFETY CHECK (FIXES YOUR ERROR)
    # ---------------------------------------------------
    if m1 == m2:
        st.error("❌ Please select TWO DIFFERENT markets.")
        st.stop()

    sel = market[market["Market"].isin([m1, m2])].copy()

    if len(sel) < 2:
        st.error("❌ Comparison requires two markets.")
        st.stop()

    a = sel.iloc[0]
    b = sel.iloc[1]

    # ---------------------------------------------------
    # KPIs
    # ---------------------------------------------------
    st.subheader("📊 KPIs")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(m1, f"{a['Recycling']}%")
    c2.metric(m2, f"{b['Recycling']}%")
    c3.metric("Sorting Gap", f"{b['Sort'] - a['Sort']:+}")
    c4.metric("Policy Gap", f"{b['Policy'] - a['Policy']:+}")

    # ---------------------------------------------------
    # NORMALIZED SCORE
    # ---------------------------------------------------
    sel["Score"] = (
        sel["Recycling"] * 0.4 +
        sel["Sort"] * 6 +
        sel["Policy"] * 6
    )

    sel["Normalized"] = (
        sel["Recycling"] / 40 * 35 +
        sel["Sort"] / 10 * 30 +
        sel["Policy"] / 10 * 35
    )

    st.subheader("🏁 Jury Score")

    st.plotly_chart(px.bar(sel, x="Market", y="Normalized", text="Normalized"))

    winner = sel.sort_values("Normalized", ascending=False).iloc[0]

    st.success(f"🏆 Winner: {winner['Market']} ({winner['Normalized']:.1f}/100)")

    # ---------------------------------------------------
    # RADAR
    # ---------------------------------------------------
    st.subheader("🧭 System Radar")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill='toself',
            name=r["Market"]
        ))

    st.plotly_chart(fig)

    # ---------------------------------------------------
    # GAP ANALYSIS
    # ---------------------------------------------------
    st.subheader("📉 Gap Analysis")

    st.info(f"""
    Recycling Gap: {b['Recycling'] - a['Recycling']}%
    Sorting Gap: {b['Sort'] - a['Sort']}
    Policy Gap: {b['Policy'] - a['Policy']}
    """)

    # ---------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------
    st.subheader("🔍 Data Confidence")

    conf_map = {"High": 3, "Medium": 2, "Low": 1}

    st.plotly_chart(px.bar(
        sel,
        x="Market",
        y=sel["Conf"].map(conf_map),
        text="Conf",
        title="Data Reliability Level"
    ))

    # ---------------------------------------------------
    # INSIGHT
    # ---------------------------------------------------
    st.subheader("🧠 Jury Insight")

    st.warning("""
    Market leadership is driven by system integration:
    - Policy strength
    - Sorting efficiency
    - Recycling capacity
    """)

    # ---------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------
    st.subheader("🎯 Strategy")

    if a["Sort"] < b["Sort"]:
        st.write("✔ Improve sorting systems")

    if a["Policy"] < b["Policy"]:
        st.write("✔ Strengthen policy")

    if a["Recycling"] < b["Recycling"]:
        st.write("✔ Increase recycling capacity")

    # ---------------------------------------------------
    # EGYPT NOTE
    # ---------------------------------------------------
    if "Egypt" in [m1, m2]:
        st.error("Egypt opportunity: hybrid recycling + policy + sorting upgrade")

    # ---------------------------------------------------
    # REFERENCES
    # ---------------------------------------------------
    st.subheader("📚 References")

    st.markdown("""
    OECD (2022) – Global Plastics Outlook  
    UNEP – Waste Reports  
    World Bank – What a Waste 2.0  
    EU Circular Economy Action Plan  
    Volk et al. (2021) – Recycling LCA study  
    EPA / EEAA / JETRO datasets  
    """)

    # ---------------------------------------------------
    # FINAL MESSAGE
    # ---------------------------------------------------
    st.success(f"""
    🏆 Final Decision:
    {winner['Market']} leads due to balanced policy + sorting + recycling system integration.
    """)
