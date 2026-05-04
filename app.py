import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Plastic Recycling Technologies in Egypt",
    page_icon="♻️",
    layout="wide"
)

df = pd.DataFrame([
    {
        "method": "Mechanical recycling",
        "efficiency_min_percent": 85,
        "efficiency_max_percent": 90,
        "energy_intensity_score_1_low_5_high": 1,
        "capex_score_1_low_5_high": 2,
        "opex_score_1_low_5_high": 2,
        "product_value_score_1_low_5_high": 3,
        "feedstock_tolerance_score_1_low_5_high": 2,
        "product_quality_score_1_low_5_high": 3,
        "ghg_risk_score_1_low_5_high": 1,
        "pollution_risk_score_1_low_5_high": 2,
        "suitable_feedstock": "Clean, sorted PET/HDPE/LDPE/PP/PS",
        "main_output": "Plastic flakes or pellets",
        "limitations": "Needs clean sorting; quality decreases after repeated recycling.",
        "egypt_relevance": "High relevance for Egypt because manual sorting and local recycling already exist."
    },
    {
        "method": "Chemical recycling",
        "efficiency_min_percent": 65,
        "efficiency_max_percent": 85,
        "energy_intensity_score_1_low_5_high": 4,
        "capex_score_1_low_5_high": 5,
        "opex_score_1_low_5_high": 5,
        "product_value_score_1_low_5_high": 5,
        "feedstock_tolerance_score_1_low_5_high": 3,
        "product_quality_score_1_low_5_high": 5,
        "ghg_risk_score_1_low_5_high": 3,
        "pollution_risk_score_1_low_5_high": 3,
        "suitable_feedstock": "PET, engineering plastics, selected contaminated streams",
        "main_output": "Monomers and chemical feedstock",
        "limitations": "High cost, catalysts, solvents, complex operation.",
        "egypt_relevance": "Potential future option for high-value PET and industrial plastic waste."
    },
    {
        "method": "Thermal recycling",
        "efficiency_min_percent": 70,
        "efficiency_max_percent": 85,
        "energy_intensity_score_1_low_5_high": 5,
        "capex_score_1_low_5_high": 4,
        "opex_score_1_low_5_high": 4,
        "product_value_score_1_low_5_high": 4,
        "feedstock_tolerance_score_1_low_5_high": 5,
        "product_quality_score_1_low_5_high": 4,
        "ghg_risk_score_1_low_5_high": 5,
        "pollution_risk_score_1_low_5_high": 5,
        "suitable_feedstock": "Mixed or contaminated plastic waste, PE/PP/PS-rich streams",
        "main_output": "Pyrolysis oil, syngas, heat/energy, char",
        "limitations": "High temperature, high energy demand, emissions risk.",
        "egypt_relevance": "Useful for mixed waste that cannot be mechanically recycled."
    }
])

df["avg_efficiency_percent"] = (
    df["efficiency_min_percent"] + df["efficiency_max_percent"]
) / 2

st.title("♻️ Technical Comparison of Plastic Recycling Technologies in Egypt")
st.caption("Mechanical vs Chemical vs Thermal recycling")

st.sidebar.header("Scenario Inputs")

waste_tons = st.sidebar.number_input(
    "Plastic waste input (tons/year)",
    min_value=100,
    max_value=10_000_000,
    value=10000,
    step=100
)

selected_methods = st.sidebar.multiselect(
    "Select recycling methods",
    options=df["method"].tolist(),
    default=df["method"].tolist()
)

filtered = df[df["method"].isin(selected_methods)].copy()
filtered["estimated_output_tons_per_year"] = (
    waste_tons * filtered["avg_efficiency_percent"] / 100
)

st.header("1. Egypt Waste Context")
st.write(
    """
    This dashboard compares the three main plastic recycling methods under the Egyptian
    waste-management context. It helps users compare technical performance,
    environmental effects, economic indicators, and expected recycled output.
    """
)

col1, col2, col3 = st.columns(3)

col1.metric("Plastic waste input", f"{waste_tons:,.0f} tons/year")
col2.metric("Methods compared", len(filtered))

if len(filtered) > 0:
    col3.metric("Highest average efficiency", f"{filtered['avg_efficiency_percent'].max():.0f}%")
else:
    col3.metric("Highest average efficiency", "N/A")

st.header("2. Technical Performance")

if len(filtered) > 0:
    fig_eff = px.bar(
        filtered,
        x="method",
        y="avg_efficiency_percent",
        text="avg_efficiency_percent",
        title="Average Process Efficiency (%)"
    )
    fig_eff.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    st.plotly_chart(fig_eff, use_container_width=True)

    technical_data = filtered.melt(
        id_vars=["method"],
        value_vars=[
            "energy_intensity_score_1_low_5_high",
            "feedstock_tolerance_score_1_low_5_high",
            "product_quality_score_1_low_5_high",
            "product_value_score_1_low_5_high"
        ],
        var_name="indicator",
        value_name="score"
    )

    fig_tech = px.bar(
        technical_data,
        x="method",
        y="score",
        color="indicator",
        barmode="group",
        title="Technical Scores: 1 = Low, 5 = High"
    )
    st.plotly_chart(fig_tech, use_container_width=True)

    st.header("3. Environmental Effects")

    environmental_data = filtered.melt(
        id_vars=["method"],
        value_vars=[
            "energy_intensity_score_1_low_5_high",
            "ghg_risk_score_1_low_5_high",
            "pollution_risk_score_1_low_5_high"
        ],
        var_name="environmental_indicator",
        value_name="risk_score"
    )

    fig_env = px.bar(
        environmental_data,
        x="method",
        y="risk_score",
        color="environmental_indicator",
        barmode="group",
        title="Environmental Risk Scores: 1 = Low Risk, 5 = High Risk"
    )
    st.plotly_chart(fig_env, use_container_width=True)

    st.header("4. Economic Effects")

    economic_data = filtered.melt(
        id_vars=["method"],
        value_vars=[
            "capex_score_1_low_5_high",
            "opex_score_1_low_5_high",
            "product_value_score_1_low_5_high"
        ],
        var_name="economic_indicator",
        value_name="score"
    )

    fig_econ = px.bar(
        economic_data,
        x="method",
        y="score",
        color="economic_indicator",
        barmode="group",
        title="Economic Scores: 1 = Low, 5 = High"
    )
    st.plotly_chart(fig_econ, use_container_width=True)

    st.header("5. Scenario Output")

    scenario = filtered[
        [
            "method",
            "suitable_feedstock",
            "avg_efficiency_percent",
            "estimated_output_tons_per_year",
            "main_output",
            "limitations",
            "egypt_relevance"
        ]
    ].copy()

    scenario["estimated_output_tons_per_year"] = scenario[
        "estimated_output_tons_per_year"
    ].round(0)

    st.dataframe(scenario, use_container_width=True)

    st.header("6. Engineering Recommendation")

    st.success(
        "Mechanical recycling is recommended for clean and well-sorted PET, HDPE, LDPE, PP, and PS streams because it has high efficiency and low energy demand."
    )

    st.info(
        "Chemical recycling is recommended when the goal is to recover high-value monomers or chemical feedstock, but it requires higher investment and more complex operation."
    )

    st.warning(
        "Thermal recycling is useful for mixed or contaminated plastic waste, but it requires strict emission-control systems because of higher greenhouse-gas and pollution risks."
    )

    st.header("7. Full Data Table")
    st.dataframe(filtered, use_container_width=True)

else:
    st.error("Please select at least one recycling method from the sidebar.")
