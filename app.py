import streamlit as st
import pandas as pd
import plotly.express as px

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
        "Efficiency (%)": 75,
        "Gross GWP kg CO2e/kg": 0.96,
        "Gross CED MJ/kg": 15.66,
        "Gross Cost EUR/kg": 0.33,
        "Net GWP kg CO2e/kg": 0.25,
        "Net CED MJ/kg": -15.92,
        "Net Cost EUR/kg": -0.24,
    },
    {
        "Method": "Combined Mechanical + Chemical Recycling",
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

    st.title("♻️ Plastic Recycling Pathways - Egypt Comparison")

    st.markdown("## Inputs")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_methods = st.multiselect(
            "Choose recycling pathways:",
            df["Method"].tolist(),
            df["Method"].tolist()
        )

    with col2:
        waste_input = st.number_input(
            "Plastic waste input (kg):",
            100, 10_000_000, 10000, 100
        )

    mode = st.radio(
        "Impact mode:",
        ["Gross impact", "Net impact"],
        horizontal=True
    )

    filtered = df[df["Method"].isin(selected_methods)].copy()

    if filtered.empty:
        st.error("Select at least one method.")
        st.stop()

    if mode == "Gross impact":
        gwp_col = "Gross GWP kg CO2e/kg"
        ced_col = "Gross CED MJ/kg"
        cost_col = "Gross Cost EGP/kg"
    else:
        gwp_col = "Net GWP kg CO2e/kg"
        ced_col = "Net CED MJ/kg"
        cost_col = "Net Cost EGP/kg"

    filtered["GWP"] = filtered[gwp_col]
    filtered["CED"] = filtered[ced_col]
    filtered["Cost"] = filtered[cost_col]

    filtered["Recovered Output"] = waste_input * filtered["Efficiency (%)"] / 100
    filtered["Total CO2e"] = waste_input * filtered["GWP"]
    filtered["Total CED"] = waste_input * filtered["CED"]
    filtered["Total Cost"] = waste_input * filtered["Cost"]

    # ---------------------------------------------------
    # Static chart configuration
    # ---------------------------------------------------

    chart_config = {
        "displayModeBar": False,
        "staticPlot": True
    }

    # ---------------- Economic ----------------
    st.header("1. Economic Impact")

    fig4 = px.bar(filtered, x="Method", y="Cost", text="Cost")
    fig4.update_traces(texttemplate="%{text:.2f}", textposition="outside")

    st.plotly_chart(fig4, use_container_width=True, config=chart_config)

    # ---------------- Scenario Table ----------------
    st.header("2. Scenario Results")

    st.dataframe(filtered[[
        "Method",
        "Recovered Output",
        "GWP",
        "Total CO2e",
        "CED",
        "Total CED",
        "Cost",
        "Total Cost"
    ]].round(2), use_container_width=True)

    # -------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------

    st.header("3. References")

    st.markdown("""
    - Volk et al. (2021) — Techno-economic assessment of plastic recycling pathways  
    - OECD Global Plastics Outlook (2022)  
    - UNEP Global Plastic Waste Reports  
    - World Bank — What a Waste 2.0  
    - European Commission — Circular Economy Action Plan  
    - IEA Plastics Recycling and Energy Reports  

    **Note:**  
    Environmental and cost factors are based on literature benchmarks and are used for comparative analysis only.
    """)
