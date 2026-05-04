import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Egypt Plastic Recycling Comparison",
    page_icon="♻️",
    layout="wide"
)

# -----------------------------
# Dataset
# Notes:
# - Egypt context is based on EEAA / UNIDO waste-management context.
# - GWP, CED, and cost are screening-level assumptions for comparison.
# - Replace with exact values later if you get a detailed EEAA datasheet.
# -----------------------------

df = pd.DataFrame([
    {
        "Method": "Mechanical Recycling",
        "Favorite Plastic Type": "PET, HDPE, PP - clean and sorted",
        "Efficiency (%)": 88,
        "CO2e/kg waste GWP": 0.35,
        "Power MJ/kg waste CED": 2.5,
        "Cost EGP/kg input": 8,
        "Clean Score": 9,
        "Egypt Suitability": "Very High",
        "Reason": "Best for clean sorted plastics; low energy and lowest emissions."
    },
    {
        "Method": "Chemical Recycling",
        "Favorite Plastic Type": "PET, selected engineering plastics",
        "Efficiency (%)": 75,
        "CO2e/kg waste GWP": 1.8,
        "Power MJ/kg waste CED": 15,
        "Cost EGP/kg input": 22,
        "Clean Score": 6,
        "Egypt Suitability": "Medium",
        "Reason": "Good product quality but expensive and technically complex."
    },
    {
        "Method": "Thermal Recycling",
        "Favorite Plastic Type": "Mixed PE, PP, PS contaminated waste",
        "Efficiency (%)": 78,
        "CO2e/kg waste GWP": 3.2,
        "Power MJ/kg waste CED": 25,
        "Cost EGP/kg input": 18,
        "Clean Score": 4,
        "Egypt Suitability": "Medium-High",
        "Reason": "Useful for mixed waste but has higher energy and emissions risk."
    }
])

# -----------------------------
# Dashboard Title
# -----------------------------

st.title("♻️ Environmental and Economic Comparison of Plastic Recycling Methods in Egypt")
st.caption("Mechanical vs Chemical vs Thermal Recycling | Egypt-focused technical dashboard")

st.markdown("""
This dashboard compares the three main plastic recycling methods using indicators relevant to Egypt:

- Favorite plastic type to use
- Efficiency
- CO₂e/kg waste as GWP
- Power MJ/kg waste as CED
- Cost in Egyptian Pound/kg input
- Cleanliness / environmental preference score
""")

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Scenario Control")

selected_methods = st.sidebar.multiselect(
    "Choose methods to compare",
    options=df["Method"].tolist(),
    default=df["Method"].tolist()
)

waste_input = st.sidebar.number_input(
    "Plastic waste input (kg)",
    min_value=100,
    max_value=10_000_000,
    value=10000,
    step=100
)

filtered = df[df["Method"].isin(selected_methods)].copy()

if filtered.empty:
    st.error("Please select at least one recycling method.")
    st.stop()

filtered["Recovered Output (kg)"] = waste_input * filtered["Efficiency (%)"] / 100
filtered["Total CO2e (kg)"] = waste_input * filtered["CO2e/kg waste GWP"]
filtered["Total Power CED (MJ)"] = waste_input * filtered["Power MJ/kg waste CED"]
filtered["Total Cost (EGP)"] = waste_input * filtered["Cost EGP/kg input"]

# -----------------------------
# KPIs
# -----------------------------

st.header("1. Scenario Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Waste Input", f"{waste_input:,.0f} kg")
col2.metric("Best Efficiency", f"{filtered['Efficiency (%)'].max():.0f}%")
col3.metric("Lowest CO₂e", f"{filtered['CO2e/kg waste GWP'].min():.2f} kg/kg")
col4.metric("Lowest Cost", f"{filtered['Cost EGP/kg input'].min():.0f} EGP/kg")

# -----------------------------
# Main Comparison Table
# -----------------------------

st.header("2. Main Technical Comparison")

comparison_table = filtered[
    [
        "Method",
        "Favorite Plastic Type",
        "Efficiency (%)",
        "CO2e/kg waste GWP",
        "Power MJ/kg waste CED",
        "Cost EGP/kg input",
        "Clean Score",
        "Egypt Suitability",
        "Reason"
    ]
]

st.dataframe(comparison_table, use_container_width=True)

# -----------------------------
# Charts
# -----------------------------

st.header("3. Efficiency Comparison")

fig_eff = px.bar(
    filtered,
    x="Method",
    y="Efficiency (%)",
    text="Efficiency (%)",
    title="Recycling Efficiency (%)"
)
fig_eff.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
st.plotly_chart(fig_eff, use_container_width=True)

st.header("4. Environmental Effects")

fig_gwp = px.bar(
    filtered,
    x="Method",
    y="CO2e/kg waste GWP",
    text="CO2e/kg waste GWP",
    title="Global Warming Potential - CO₂e/kg Waste"
)
fig_gwp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
st.plotly_chart(fig_gwp, use_container_width=True)

fig_ced = px.bar(
    filtered,
    x="Method",
    y="Power MJ/kg waste CED",
    text="Power MJ/kg waste CED",
    title="Cumulative Energy Demand - MJ/kg Waste"
)
fig_ced.update_traces(texttemplate="%{text:.1f}", textposition="outside")
st.plotly_chart(fig_ced, use_container_width=True)

st.header("5. Economic Effects")

fig_cost = px.bar(
    filtered,
    x="Method",
    y="Cost EGP/kg input",
    text="Cost EGP/kg input",
    title="Estimated Treatment Cost - EGP/kg Input"
)
fig_cost.update_traces(texttemplate="%{text:.0f}", textposition="outside")
st.plotly_chart(fig_cost, use_container_width=True)

# -----------------------------
# Cleanest Method
# -----------------------------

st.header("6. Cleanest Method Ranking")

ranking = filtered.sort_values(
    by=["Clean Score", "CO2e/kg waste GWP", "Power MJ/kg waste CED", "Cost EGP/kg input"],
    ascending=[False, True, True, True]
)

fig_clean = px.bar(
    ranking,
    x="Method",
    y="Clean Score",
    text="Clean Score",
    title="Clean Score Ranking - 10 = Cleanest"
)
fig_clean.update_traces(texttemplate="%{text:.0f}/10", textposition="outside")
st.plotly_chart(fig_clean, use_container_width=True)

best_method = ranking.iloc[0]

st.success(
    f"Recommended cleanest option: {best_method['Method']} "
    f"for {best_method['Favorite Plastic Type']}."
)

# -----------------------------
# Scenario Calculations
# -----------------------------

st.header("7. Scenario Calculation Results")

scenario_table = filtered[
    [
        "Method",
        "Recovered Output (kg)",
        "Total CO2e (kg)",
        "Total Power CED (MJ)",
        "Total Cost (EGP)"
    ]
].copy()

scenario_table["Recovered Output (kg)"] = scenario_table["Recovered Output (kg)"].round(0)
scenario_table["Total CO2e (kg)"] = scenario_table["Total CO2e (kg)"].round(2)
scenario_table["Total Power CED (MJ)"] = scenario_table["Total Power CED (MJ)"].round(2)
scenario_table["Total Cost (EGP)"] = scenario_table["Total Cost (EGP)"].round(2)

st.dataframe(scenario_table, use_container_width=True)

# -----------------------------
# Recommendation Text
# -----------------------------

st.header("8. Engineering Recommendation for Egypt")

st.markdown("""
### Recommended pathway

**Mechanical recycling** is the cleanest and most suitable method when the plastic waste is clean and sorted, especially PET, HDPE, and PP.  
It has the highest efficiency, lowest CO₂e impact, lowest energy demand, and lowest estimated cost.

**Chemical recycling** is useful when the target is high-quality monomer or chemical feedstock recovery, especially for PET.  
However, it is more expensive and needs advanced technical operation.

**Thermal recycling** is suitable for mixed or contaminated plastic waste that cannot be mechanically recycled.  
However, it has the highest environmental risk because it requires high energy and may produce emissions if emission-control systems are weak.
""")

# -----------------------------
# Sources Section
# -----------------------------

st.header("9. Data Sources and Assumptions")

st.markdown("""
The dashboard uses a screening-level dataset prepared for educational and technical comparison.

**Egypt context sources:**
- EEAA State of Environment Report.
- EEAA solid-waste and environmental reporting.
- UNIDO Plastic Value Chain in Egypt.
- Egypt circular economy and plastic waste literature.

**Important note:**  
EEAA sources are useful for Egypt waste context, plastic-waste management, and national environmental conditions.  
However, detailed LCA indicators such as exact **CO₂e/kg waste GWP**, **MJ/kg waste CED**, and **EGP/kg treatment cost** are not usually provided directly as one ready datasheet.  
Therefore, the numerical values in this dashboard are comparative engineering assumptions and should be updated if a detailed Egyptian LCA dataset becomes available.
""")
