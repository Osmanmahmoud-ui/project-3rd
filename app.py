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
# Sidebar Navigation
# -------------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Dashboard"])

# -------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------

if page == "Dashboard":

    st.title("♻️ Environmental and Economic Comparison of Plastic Recycling Pathways")
    st.caption("Egypt-focused dashboard based on Volk et al. (2021) and engineering benchmarks")

    st.markdown("## Dashboard Inputs")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_methods = st.multiselect(
            "Choose recycling pathways:",
            df["Method"].tolist(),
            default=df["Method"].tolist()
        )

    with col2:
        waste_input = st.number_input(
            "Plastic waste input (kg)",
            min_value=100,
            max_value=10_000_000,
            value=10000,
            step=100
        )

    accounting_mode = st.radio(
        "Impact mode:",
        ["Gross impact", "Net impact with substitution credit"],
        horizontal=True
    )

    filtered = df[df["Method"].isin(selected_methods)].copy()

    if filtered.empty:
        st.error("Please select at least one method.")
        st.stop()

    if accounting_mode == "Gross impact":
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

    filtered["Recovered Output (kg)"] = waste_input * filtered["Efficiency (%)"] / 100
    filtered["Total CO2e (kg)"] = waste_input * filtered["GWP"]
    filtered["Total CED (MJ)"] = waste_input * filtered["CED"]
    filtered["Total Cost (EGP)"] = waste_input * filtered["Cost"]

    st.header("1. Scenario Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Waste Input", f"{waste_input:,} kg")
    col2.metric("Best Efficiency", f"{filtered['Efficiency (%)'].max():.0f}%")
    col3.metric("Lowest GWP", f"{filtered['GWP'].min():.2f}")
    col4.metric("Lowest Cost", f"{filtered['Cost'].min():.2f} EGP/kg")

    st.header("2. Technical Comparison")

    for _, r in filtered.iterrows():
        st.info(f"{r['Method']} → {r['Favorite Plastic Type']}")

    st.plotly_chart(
        px.bar(filtered, x="Method", y="Efficiency (%)", text="Efficiency (%)"),
        use_container_width=True
    )

    st.header("3. Environmental Effects")

    st.plotly_chart(
        px.bar(filtered, x="Method", y="GWP", text="GWP"),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(filtered, x="Method", y="CED", text="CED"),
        use_container_width=True
    )

    st.header("4. Economic Effects")

    st.plotly_chart(
        px.bar(filtered, x="Method", y="Cost", text="Cost"),
        use_container_width=True
    )

    st.header("5. Results Table")

    st.dataframe(filtered[[
        "Method",
        "Recovered Output (kg)",
        "GWP",
        "Total CO2e (kg)",
        "CED",
        "Total CED (MJ)",
        "Cost",
        "Total Cost (EGP)"
    ]].round(2), use_container_width=True)

    st.header("6. Data Sources and Methodology")

    st.markdown("""
**Main reference:**

Volk et al. (2021) — Techno-economic assessment of plastic recycling pathways

**Supporting frameworks:**
- UNEP circular economy reports
- IEA waste & energy system reports
- European Commission circular economy strategy

**Equations used:**

Recovered Output = Waste Input × Efficiency / 100  
Total GWP = Waste Input × GWP factor  
Total CED = Waste Input × CED factor  
Cost EGP/kg = Cost EUR/kg × Exchange Rate  
Total Cost = Waste Input × Cost EGP/kg  
""")

    st.header("7. Engineering Recommendation")

    best = filtered.sort_values(by=["GWP", "CED", "Cost"]).iloc[0]

    st.success(f"Recommended pathway: {best['Method']}")
