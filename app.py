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
# Dataset
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
    },
    {
        "Method": "Pyrolysis",
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
        "Method": "Hybrid System",
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

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Dashboard"])

# -------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------

if page == "Dashboard":
    st.title("♻️ Plastic Recycling Comparison Dashboard")

    selected_methods = st.multiselect(
        "Select pathways:",
        df["Method"].tolist(),
        default=df["Method"].tolist()
    )

    waste_input = st.number_input(
        "Waste input (kg)",
        min_value=100,
        value=10000,
        step=100
    )

    mode = st.radio(
        "Impact mode:",
        ["Gross impact", "Net impact"],
        horizontal=True
    )

    filtered = df[df["Method"].isin(selected_methods)].copy()

    if mode == "Gross impact":
        gwp = "Gross GWP kg CO2e/kg"
        ced = "Gross CED MJ/kg"
        cost = "Gross Cost EGP/kg"
    else:
        gwp = "Net GWP kg CO2e/kg"
        ced = "Net CED MJ/kg"
        cost = "Net Cost EGP/kg"

    filtered["GWP"] = filtered[gwp]
    filtered["CED"] = filtered[ced]
    filtered["Cost"] = filtered[cost]

    filtered["Recovered"] = waste_input * filtered["Efficiency (%)"] / 100
    filtered["CO2"] = waste_input * filtered["GWP"]
    filtered["Energy"] = waste_input * filtered["CED"]
    filtered["Total Cost"] = waste_input * filtered["Cost"]

    # ---------------------------------------------------
    # KPI
    # ---------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("Max Efficiency", f"{filtered['Efficiency (%)'].max():.0f}%")
    col2.metric("Lowest CO2", f"{filtered['GWP'].min():.2f}")
    col3.metric("Lowest Cost", f"{filtered['Cost'].min():.2f} EGP/kg")

    # ---------------------------------------------------
    # Charts (STATIC / NOT CLICKABLE)
    # ---------------------------------------------------

    st.subheader("Efficiency Comparison")

    fig = px.bar(filtered, x="Method", y="Efficiency (%)", text="Efficiency (%)")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "staticPlot": True}
    )

    st.subheader("CO2 Emissions")

    fig = px.bar(filtered, x="Method", y="GWP", text="GWP")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "staticPlot": True}
    )

    st.subheader("Energy Demand")

    fig = px.bar(filtered, x="Method", y="CED", text="CED")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "staticPlot": True}
    )

    st.subheader("Cost Comparison")

    fig = px.bar(filtered, x="Method", y="Cost", text="Cost")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "staticPlot": True}
    )

    # ---------------------------------------------------
    # Results Table
    # ---------------------------------------------------

    st.subheader("Results Table")

    st.dataframe(
        filtered[[
            "Method",
            "Efficiency (%)",
            "Recovered",
            "CO2",
            "Energy",
            "Cost"
        ]],
        use_container_width=True
    )

    # ---------------------------------------------------
    # Recommendation (simple)
    # ---------------------------------------------------

    best = filtered.sort_values(by=["GWP", "Cost"]).iloc[0]

    st.success(f"Recommended pathway: **{best['Method']}**")
