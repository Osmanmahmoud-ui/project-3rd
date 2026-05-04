import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Plastic Recycling Decision Dashboard",
    page_icon="♻️",
    layout="wide"
)

# -------------------------------------------------------
# Currency
# -------------------------------------------------------
EUR_TO_EGP = 62.669

# -------------------------------------------------------
# Recycling Dataset
# -------------------------------------------------------
df = pd.DataFrame([
    {"Method": "Mechanical Recycling", "Efficiency": 88, "GWP": 0.18, "Cost": -0.16},
    {"Method": "Pyrolysis", "Efficiency": 75, "GWP": 0.25, "Cost": -0.24},
    {"Method": "Hybrid System", "Efficiency": 82, "GWP": -0.22, "Cost": -0.29},
])

df["Cost EGP"] = df["Cost"] * EUR_TO_EGP

# -------------------------------------------------------
# Market Dataset (EXPANDED)
# -------------------------------------------------------
market = pd.DataFrame([
    {"Market": "Egypt", "Waste": 5.4, "Recycling": 12, "Mech": 7, "Chem": 3, "Therm": 4, "Sorting": 4, "Policy": 5, "Informal": 60},
    {"Market": "European Union", "Waste": 30, "Recycling": 35, "Mech": 8, "Chem": 7, "Therm": 6, "Sorting": 9, "Policy": 9, "Informal": 5},
    {"Market": "Germany", "Waste": 6, "Recycling": 38, "Mech": 9, "Chem": 7, "Therm": 7, "Sorting": 9, "Policy": 9, "Informal": 2},
    {"Market": "Japan", "Waste": 8, "Recycling": 25, "Mech": 7, "Chem": 7, "Therm": 8, "Sorting": 8, "Policy": 8, "Informal": 3},
    {"Market": "United States", "Waste": 40, "Recycling": 9, "Mech": 6, "Chem": 6, "Therm": 5, "Sorting": 6, "Policy": 5, "Informal": 2},
    {"Market": "China", "Waste": 60, "Recycling": 20, "Mech": 7, "Chem": 6, "Therm": 6, "Sorting": 6, "Policy": 7, "Informal": 20},
    {"Market": "UAE", "Waste": 1.5, "Recycling": 15, "Mech": 6, "Chem": 5, "Therm": 6, "Sorting": 6, "Policy": 7, "Informal": 5},
    {"Market": "Global Avg", "Waste": 400, "Recycling": 9, "Mech": 5, "Chem": 4, "Therm": 5, "Sorting": 4, "Policy": 4, "Informal": 25}
])

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
page = st.sidebar.radio("Navigation", ["Dashboard", "Market Engine"])

# -------------------------------------------------------
# Dashboard
# -------------------------------------------------------
if page == "Dashboard":

    st.title("♻️ Recycling Technology Comparison")

    waste = st.number_input("Waste input (kg)", 100, 1000000, 10000)

    df["Output"] = waste * df["Efficiency"] / 100
    df["CO2"] = waste * df["GWP"]
    df["Total Cost"] = waste * df["Cost EGP"]

    st.plotly_chart(px.bar(df, x="Method", y="Efficiency", title="Efficiency"))
    st.plotly_chart(px.bar(df, x="Method", y="CO2", title="CO₂ Impact"))
    st.plotly_chart(px.bar(df, x="Method", y="Total Cost", title="Cost"))

# -------------------------------------------------------
# 🚀 MARKET ENGINE
# -------------------------------------------------------
elif page == "Market Engine":

    st.title("🌍 Circular Economy Decision Engine")

    col1, col2 = st.columns(2)

    with col1:
        m1_name = st.selectbox("Market 1", market["Market"])

    with col2:
        m2_name = st.selectbox("Market 2", market["Market"], index=1)

    df_sel = market[market["Market"].isin([m1_name, m2_name])]

    m1 = df_sel[df_sel["Market"] == m1_name].iloc[0]
    m2 = df_sel[df_sel["Market"] == m2_name].iloc[0]

    # KPIs
    st.subheader("📊 KPIs")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(m1_name, f"{m1['Recycling']}%")
    c2.metric(m2_name, f"{m2['Recycling']}%")
    c3.metric("Sorting Gap", f"{m2['Sorting'] - m1['Sorting']:+}")
    c4.metric("Policy Gap", f"{m2['Policy'] - m1['Policy']:+}")

    # Performance Index
    st.subheader("🏁 Performance Index")

    df_sel["Index"] = (
        df_sel["Recycling"] * 0.4 +
        df_sel["Sorting"] * 6 +
        df_sel["Policy"] * 6
    )

    st.plotly_chart(px.bar(df_sel, x="Market", y="Index", text="Index"))

    winner = df_sel.sort_values("Index", ascending=False).iloc[0]
    st.success(f"🏆 Winner: {winner['Market']}")

    # Radar
    st.subheader("🧭 System Radar")

    fig = go.Figure()

    for _, row in df_sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["Mech"], row["Chem"], row["Therm"], row["Sorting"], row["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill='toself',
            name=row["Market"]
        ))

    st.plotly_chart(fig)

    # Gap
    st.subheader("📉 Gap Analysis")

    st.info(f"""
    Recycling Gap: {m2['Recycling'] - m1['Recycling']}%
    Sorting Gap: {m2['Sorting'] - m1['Sorting']}
    Policy Gap: {m2['Policy'] - m1['Policy']}
    """)

    # Recommendations
    st.subheader("🎯 Recommendations")

    actions = []

    if m1["Sorting"] < m2["Sorting"]:
        actions.append("Invest in automated sorting")

    if m1["Policy"] < m2["Policy"]:
        actions.append("Strengthen regulation")

    if m1["Recycling"] < m2["Recycling"]:
        actions.append("Increase recycling capacity")

    for a in actions:
        st.write(f"- {a}")

    # Egypt insight
    if "Egypt" in [m1_name, m2_name]:
        st.warning("🇪🇬 Egypt: biggest opportunity = sorting + policy + hybrid recycling")

    # Executive summary
    st.header("🧠 Executive Summary")

    st.success(f"""
    Leader: {winner['Market']}

    Key driver: Sorting + Policy

    Strategy:
    - Improve sorting
    - Strengthen policy
    - Expand recycling

    Insight:
    Circular economy success depends on system integration, not one technology.
    """)
