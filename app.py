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
# Market Comparison Data
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
        "Main Strength": "Strong regulation, EPR, automated sorting, recycled-content targets",
        "Main Weakness": "High operating cost",
        "Recommended Strategy": "Integrated circular system"
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
        "Main Strength": "Advanced separation and waste-to-energy",
        "Main Weakness": "High dependence on thermal recovery",
        "Recommended Strategy": "Increase circularity"
    }
])

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Market Research"]
)

# -------------------------------------------------------
# Dashboard (UNCHANGED - shortened here for clarity)
# -------------------------------------------------------

if page == "Dashboard":
    st.title("♻️ Recycling Dashboard")
    st.write("Your original dashboard code remains here...")

# -------------------------------------------------------
# Market Research (ONLY MARKET VS MARKET)
# -------------------------------------------------------

elif page == "Market Research":

    st.title("🌍 Market vs Market Comparison")

    col1, col2 = st.columns(2)

    with col1:
        market_1 = st.selectbox("Market 1", market_comparison_data["Market"])

    with col2:
        market_2 = st.selectbox("Market 2", market_comparison_data["Market"], index=1)

    df_selected = market_comparison_data[
        market_comparison_data["Market"].isin([market_1, market_2])
    ]

    m1 = df_selected[df_selected["Market"] == market_1].iloc[0]
    m2 = df_selected[df_selected["Market"] == market_2].iloc[0]

    st.subheader("KPIs")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(f"{market_1} Recycling", f"{m1['Recycling Rate (%)']}%")
    c2.metric(f"{market_2} Recycling", f"{m2['Recycling Rate (%)']}%")
    c3.metric(f"{market_1} Policy", f"{m1['Policy Strength']}/10")
    c4.metric(f"{market_2} Policy", f"{m2['Policy Strength']}/10")

    st.subheader("Recycling Rate")

    fig = px.bar(df_selected, x="Market", y="Recycling Rate (%)", text="Recycling Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Technology Maturity")

    tech = df_selected.melt(
        id_vars="Market",
        value_vars=[
            "Mechanical Recycling Maturity",
            "Chemical Recycling Maturity",
            "Thermal Recycling Maturity"
        ]
    )

    fig2 = px.bar(tech, x="variable", y="value", color="Market", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Radar")

    fig_radar = go.Figure()

    for _, row in df_selected.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
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

    st.plotly_chart(fig_radar)

    st.subheader("Insights")

    gap = m2["Recycling Rate (%)"] - m1["Recycling Rate (%)"]

    st.info(f"Recycling gap: {gap:+}%")

    if "Egypt" in [market_1, market_2]:
        st.success("Egypt needs sorting + policy + hybrid recycling to close the gap.")
