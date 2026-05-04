import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Plastic Recycling Technologies in Egypt",
    page_icon="♻️",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/recycling_methods_egypt.csv")

df = load_data()

st.title("♻️ Technical Comparison of Plastic Recycling Technologies in Egypt")
st.caption("Mechanical vs Chemical vs Thermal recycling: technical, environmental, and economic comparison")

st.sidebar.header("Scenario Inputs")
waste_tons = st.sidebar.number_input("Plastic waste input (tons/year)", min_value=100, max_value=10_000_000, value=10000, step=100)
selected_methods = st.sidebar.multiselect(
    "Select recycling methods",
    options=df["method"].tolist(),
    default=df["method"].tolist()
)

filtered = df[df["method"].isin(selected_methods)].copy()
filtered["avg_efficiency_percent"] = (filtered["efficiency_min_percent"] + filtered["efficiency_max_percent"]) / 2
filtered["estimated_output_tons_per_year"] = waste_tons * filtered["avg_efficiency_percent"] / 100

st.header("1. Egypt Waste Context")
st.markdown("""
This dashboard is designed for the Egyptian plastic-waste context. Egypt has a large municipal solid-waste stream,
and several sources report plastics as a significant share of MSW. The dashboard uses method-specific assumptions
from the technical report and allows users to test different waste-input scenarios.
""")

col1, col2, col3 = st.columns(3)
col1.metric("Scenario waste input", f"{waste_tons:,.0f} tons/year")
col2.metric("Methods compared", len(filtered))
col3.metric("Highest efficiency", f"{filtered['avg_efficiency_percent'].max():.0f}%")

st.header("2. Technical Performance")
fig_eff = px.bar(
    filtered,
    x="method",
    y="avg_efficiency_percent",
    text="avg_efficiency_percent",
    title="Average Process Efficiency (%)",
)
fig_eff.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
st.plotly_chart(fig_eff, use_container_width=True)

fig_radar = px.line_polar(
    filtered.melt(
        id_vars=["method"],
        value_vars=[
            "energy_intensity_score_1_low_5_high",
            "feedstock_tolerance_score_1_low_5_high",
            "product_quality_score_1_low_5_high",
            "product_value_score_1_low_5_high",
        ],
        var_name="indicator",
        value_name="score",
    ),
    r="score",
    theta="indicator",
    color="method",
    line_close=True,
    title="Technical and Product Performance Scores (1 = low, 5 = high)"
)
st.plotly_chart(fig_radar, use_container_width=True)

st.header("3. Environmental Comparison")
env = filtered.melt(
    id_vars=["method"],
    value_vars=["energy_intensity_score_1_low_5_high", "ghg_risk_score_1_low_5_high", "pollution_risk_score_1_low_5_high"],
    var_name="environmental_indicator",
    value_name="risk_score"
)
fig_env = px.bar(
    env,
    x="method",
    y="risk_score",
    color="environmental_indicator",
    barmode="group",
    title="Environmental Risk Scores (1 = low risk, 5 = high risk)"
)
st.plotly_chart(fig_env, use_container_width=True)

st.header("4. Economic Comparison")
econ = filtered.melt(
    id_vars=["method"],
    value_vars=["capex_score_1_low_5_high", "opex_score_1_low_5_high", "product_value_score_1_low_5_high"],
    var_name="economic_indicator",
    value_name="score"
)
fig_econ = px.bar(
    econ,
    x="method",
    y="score",
    color="economic_indicator",
    barmode="group",
    title="Economic Scores (1 = low, 5 = high)"
)
st.plotly_chart(fig_econ, use_container_width=True)

st.header("5. Scenario Output")
scenario = filtered[[
    "method",
    "suitable_feedstock",
    "avg_efficiency_percent",
    "estimated_output_tons_per_year",
    "main_output",
    "limitations",
    "egypt_relevance"
]].copy()
scenario["estimated_output_tons_per_year"] = scenario["estimated_output_tons_per_year"].round(0)
st.dataframe(scenario, use_container_width=True)

st.header("6. Engineering Recommendation")
best_clean = "Mechanical recycling is recommended when the waste stream is clean, sorted, and dominated by PET/HDPE/PP."
best_mixed = "Thermal recycling is recommended for mixed or contaminated streams, but only with strong emission-control systems."
best_value = "Chemical recycling is recommended when high-value monomer recovery is the objective and sufficient capital/technical capacity is available."

st.success(best_clean)
st.warning(best_mixed)
st.info(best_value)

st.header("7. Data Table")
st.dataframe(filtered, use_container_width=True)
