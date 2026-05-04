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
# Dashboard Dataset
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
        "Egypt Suitability": "Very High",
        "Reason": "Best for clean sorted plastics; low energy and low GWP compared with other pathways."
    },
    {
        "Method": "Chemical Recycling - Pyrolysis",
        "Favorite Plastic Type": "Mixed PE, PP, PS and RDF-like plastic fractions",
        "Efficiency (%)": 75,

        "Gross GWP kg CO2e/kg": 0.96,
        "Gross CED MJ/kg": 15.66,
        "Gross Cost EUR/kg": 0.33,

        "Net GWP kg CO2e/kg": 0.25,
        "Net CED MJ/kg": -15.92,
        "Net Cost EUR/kg": -0.24,

        "Clean Score": 6,
        "Egypt Suitability": "Medium",
        "Reason": "Useful for mixed plastic and chemical feedstock recovery, but requires higher energy and more advanced operation."
    },
    {
        "Method": "Combined Mechanical + Chemical Recycling",
        "Favorite Plastic Type": "Sorted recyclable plastics plus residues for pyrolysis",
        "Efficiency (%)": 82,

        "Gross GWP kg CO2e/kg": 0.48,
        "Gross CED MJ/kg": 13.32,
        "Gross Cost EUR/kg": 0.14,

        "Net GWP kg CO2e/kg": -0.22,
        "Net CED MJ/kg": -30.14,
        "Net Cost EUR/kg": -0.29,

        "Clean Score": 10,
        "Egypt Suitability": "High",
        "Reason": "Highest circularity potential because recyclable plastics are mechanically recycled and residues are chemically recycled."
    }
])

df["Gross Cost EGP/kg"] = df["Gross Cost EUR/kg"] * EUR_TO_EGP
df["Net Cost EGP/kg"] = df["Net Cost EUR/kg"] * EUR_TO_EGP

# -------------------------------------------------------
# Market Dataset (EXPANDED)
# -------------------------------------------------------
market_comparison_data = pd.DataFrame([
    {
        "Market": "Egypt",
        "Plastic Waste (M tons/year)": 5.4,
        "Recycling Rate (%)": 12,
        "Mechanical Recycling Maturity": 7,
        "Chemical Recycling Maturity": 3,
        "Thermal Recycling Maturity": 4,
        "Sorting Automation": 4,
        "Policy Strength": 5,
        "Informal Sector Role (%)": 60,
        "Main Strength": "Strong informal collection and mechanical recycling base",
        "Main Weakness": "Mixed waste quality and limited advanced recycling",
        "Recommended Strategy": "Upgrade sorting + expand mechanical recycling + pilot pyrolysis"
    },
    {
        "Market": "European Union",
        "Plastic Waste (M tons/year)": 30,
        "Recycling Rate (%)": 35,
        "Mechanical Recycling Maturity": 8,
        "Chemical Recycling Maturity": 7,
        "Thermal Recycling Maturity": 6,
        "Sorting Automation": 9,
        "Policy Strength": 9,
        "Informal Sector Role (%)": 5,
        "Main Strength": "Strong regulation, EPR, automated sorting",
        "Main Weakness": "High cost systems",
        "Recommended Strategy": "Circular system optimization"
    },
    {
        "Market": "Germany",
        "Plastic Waste (M tons/year)": 6,
        "Recycling Rate (%)": 38,
        "Mechanical Recycling Maturity": 9,
        "Chemical Recycling Maturity": 7,
        "Thermal Recycling Maturity": 7,
        "Sorting Automation": 9,
        "Policy Strength": 9,
        "Informal Sector Role (%)": 2,
        "Main Strength": "Best-in-class circular system",
        "Main Weakness": "High regulation cost"
    },
    {
        "Market": "Japan",
        "Plastic Waste (M tons/year)": 8,
        "Recycling Rate (%)": 25,
        "Mechanical Recycling Maturity": 7,
        "Chemical Recycling Maturity": 7,
        "Thermal Recycling Maturity": 8,
        "Sorting Automation": 8,
        "Policy Strength": 8,
        "Informal Sector Role (%)": 3,
        "Main Strength": "Advanced separation system",
        "Main Weakness": "Thermal dependency"
    },
    {
        "Market": "United States",
        "Plastic Waste (M tons/year)": 40,
        "Recycling Rate (%)": 9,
        "Mechanical Recycling Maturity": 6,
        "Chemical Recycling Maturity": 6,
        "Thermal Recycling Maturity": 5,
        "Sorting Automation": 6,
        "Policy Strength": 5,
        "Informal Sector Role (%)": 2,
        "Main Strength": "Large investment potential",
        "Main Weakness": "Low recycling efficiency"
    },
    {
        "Market": "China",
        "Plastic Waste (M tons/year)": 60,
        "Recycling Rate (%)": 20,
        "Mechanical Recycling Maturity": 7,
        "Chemical Recycling Maturity": 6,
        "Thermal Recycling Maturity": 6,
        "Sorting Automation": 6,
        "Policy Strength": 7,
        "Informal Sector Role (%)": 20,
        "Main Strength": "Fast policy development",
        "Main Weakness": "Waste inconsistency"
    },
    {
        "Market": "UAE",
        "Plastic Waste (M tons/year)": 1.5,
        "Recycling Rate (%)": 15,
        "Mechanical Recycling Maturity": 6,
        "Chemical Recycling Maturity": 5,
        "Thermal Recycling Maturity": 6,
        "Sorting Automation": 6,
        "Policy Strength": 7,
        "Informal Sector Role (%)": 5,
        "Main Strength": "Modern infrastructure",
        "Main Weakness": "Low recycling culture"
    },
    {
        "Market": "Global Average",
        "Plastic Waste (M tons/year)": 400,
        "Recycling Rate (%)": 9,
        "Mechanical Recycling Maturity": 5,
        "Chemical Recycling Maturity": 4,
        "Thermal Recycling Maturity": 5,
        "Sorting Automation": 4,
        "Policy Strength": 4,
        "Informal Sector Role (%)": 25,
        "Main Strength": "Huge global opportunity",
        "Main Weakness": "Very low recycling rate"
    }
])

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Dashboard", "Market Research"])

# -------------------------------------------------------
# DASHBOARD (UNCHANGED — RESTORED)
# -------------------------------------------------------
if page == "Dashboard":

    st.title("♻️ Environmental and Economic Comparison of Plastic Recycling Pathways")

    waste_input = st.number_input("Plastic waste input (kg):", 100, 1000000, 10000)

    selected_methods = df["Method"].tolist()
    filtered = df.copy()

    filtered["Recovered Output (kg)"] = waste_input * filtered["Efficiency (%)"] / 100
    filtered["Total CO2e (kg)"] = waste_input * filtered["Net GWP kg CO2e/kg"]
    filtered["Total CED (MJ)"] = waste_input * filtered["Net CED MJ/kg"]
    filtered["Total Cost (EGP)"] = waste_input * filtered["Net Cost EGP/kg"]

    st.plotly_chart(px.bar(filtered, x="Method", y="Efficiency (%)"))
    st.plotly_chart(px.bar(filtered, x="Method", y="Total CO2e (kg)"))
    st.plotly_chart(px.bar(filtered, x="Method", y="Total Cost (EGP)"))

# -------------------------------------------------------
# MARKET ENGINE (COMPETITION VERSION ONLY)
# -------------------------------------------------------
elif page == "Market Research":

    st.title("🌍 Market vs Market Strategic Engine")

    col1, col2 = st.columns(2)

    with col1:
        m1_name = st.selectbox("Market 1", market_comparison_data["Market"], index=0)

    with col2:
        m2_name = st.selectbox("Market 2", market_comparison_data["Market"], index=1)

    df_sel = market_comparison_data[
        market_comparison_data["Market"].isin([m1_name, m2_name])
    ].copy()

    m1 = df_sel[df_sel["Market"] == m1_name].iloc[0]
    m2 = df_sel[df_sel["Market"] == m2_name].iloc[0]

    st.subheader("📊 KPIs")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(m1_name, f"{m1['Recycling Rate (%)']}%")
    c2.metric(m2_name, f"{m2['Recycling Rate (%)']}%")
    c3.metric("Sorting Gap", f"{m2['Sorting Automation'] - m1['Sorting Automation']:+}")
    c4.metric("Policy Gap", f"{m2['Policy Strength'] - m1['Policy Strength']:+}")

    st.subheader("🏁 Performance Index")

    df_sel["Index"] = (
        df_sel["Recycling Rate (%)"] * 0.4 +
        df_sel["Sorting Automation"] * 6 +
        df_sel["Policy Strength"] * 6
    )

    st.plotly_chart(px.bar(df_sel, x="Market", y="Index", text="Index"))

    winner = df_sel.sort_values("Index", ascending=False).iloc[0]
    st.success(f"🏆 Winner: {winner['Market']}")

    st.subheader("🧭 System Radar")

    fig = go.Figure()

    for _, row in df_sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[
                row["Mechanical Recycling Maturity"],
                row["Chemical Recycling Maturity"],
                row["Thermal Recycling Maturity"],
                row["Sorting Automation"],
                row["Policy Strength"]
            ],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill='toself',
            name=row["Market"]
        ))

    st.plotly_chart(fig)

    st.subheader("📉 Gap Analysis")

    st.info(f"""
    Recycling Gap: {m2['Recycling Rate (%)'] - m1['Recycling Rate (%)']}%
    Sorting Gap: {m2['Sorting Automation'] - m1['Sorting Automation']}
    Policy Gap: {m2['Policy Strength'] - m1['Policy Strength']}
    """)

    st.subheader("🎯 Recommendations")

    if m1["Sorting Automation"] < m2["Sorting Automation"]:
        st.write("- Improve sorting systems")

    if m1["Policy Strength"] < m2["Policy Strength"]:
        st.write("- Strengthen policy framework")

    if m1["Recycling Rate (%)"] < m2["Recycling Rate (%)"]:
        st.write("- Increase recycling capacity")

    if "Egypt" in [m1_name, m2_name]:
        st.warning("🇪🇬 Egypt needs sorting + policy + hybrid recycling upgrade")

    st.header("🧠 Executive Summary")

    st.success(f"""
    Leader: {winner['Market']}

    Key insight: Circular economy performance depends on system integration:
    policy + sorting + technology working together.
    """)
