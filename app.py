import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Egypt Plastic Recycling Comparison",
    page_icon="♻️",
    layout="wide"
)

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

# Sidebar only for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Market Research"]
)

if page == "Dashboard":
    st.title("♻️ Environmental and Economic Comparison of Plastic Recycling Methods in Egypt")
    st.caption("Mechanical vs Chemical vs Thermal Recycling | Egypt-focused technical dashboard")

    st.markdown("## Dashboard Inputs")

    input_col1, input_col2 = st.columns([2, 1])

    with input_col1:
        selected_methods = st.multiselect(
            "Choose recycling methods to compare:",
            options=df["Method"].tolist(),
            default=df["Method"].tolist()
        )

    with input_col2:
        waste_input = st.number_input(
            "Plastic waste input (kg):",
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

    st.header("1. Scenario Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Waste Input", f"{waste_input:,.0f} kg")
    col2.metric("Best Efficiency", f"{filtered['Efficiency (%)'].max():.0f}%")
    col3.metric("Lowest CO₂e", f"{filtered['CO2e/kg waste GWP'].min():.2f} kg/kg")
    col4.metric("Lowest Cost", f"{filtered['Cost EGP/kg input'].min():.0f} EGP/kg")

    st.header("2. Visual Technical Comparison")

    st.subheader("Favorite Plastic Type for Each Method")

    for _, row in filtered.iterrows():
        st.info(f"**{row['Method']}** → {row['Favorite Plastic Type']}")

    fig_eff = px.bar(
        filtered,
        x="Method",
        y="Efficiency (%)",
        text="Efficiency (%)",
        title="Recycling Efficiency (%)"
    )
    fig_eff.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    st.plotly_chart(fig_eff, use_container_width=True)

    fig_clean = px.bar(
        filtered,
        x="Method",
        y="Clean Score",
        text="Clean Score",
        title="Clean Score: 10 = Cleanest"
    )
    fig_clean.update_traces(texttemplate="%{text:.0f}/10", textposition="outside")
    st.plotly_chart(fig_clean, use_container_width=True)

    st.header("3. Environmental Effects")

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

    st.header("4. Economic Effects")

    fig_cost = px.bar(
        filtered,
        x="Method",
        y="Cost EGP/kg input",
        text="Cost EGP/kg input",
        title="Estimated Treatment Cost - EGP/kg Input"
    )
    fig_cost.update_traces(texttemplate="%{text:.0f} EGP", textposition="outside")
    st.plotly_chart(fig_cost, use_container_width=True)

    st.header("5. Scenario Calculation Results")

    scenario_data = filtered[
        [
            "Method",
            "Recovered Output (kg)",
            "Total CO2e (kg)",
            "Total Power CED (MJ)",
            "Total Cost (EGP)"
        ]
    ].copy()

    scenario_data["Recovered Output (kg)"] = scenario_data["Recovered Output (kg)"].round(0)
    scenario_data["Total CO2e (kg)"] = scenario_data["Total CO2e (kg)"].round(2)
    scenario_data["Total Power CED (MJ)"] = scenario_data["Total Power CED (MJ)"].round(2)
    scenario_data["Total Cost (EGP)"] = scenario_data["Total Cost (EGP)"].round(2)

    st.dataframe(scenario_data, use_container_width=True)

    st.header("6. Engineering Recommendation for Egypt")

    ranking = filtered.sort_values(
        by=["Clean Score", "CO2e/kg waste GWP", "Power MJ/kg waste CED", "Cost EGP/kg input"],
        ascending=[False, True, True, True]
    )

    best_method = ranking.iloc[0]

    st.success(
        f"Recommended cleanest option: **{best_method['Method']}** "
        f"for **{best_method['Favorite Plastic Type']}**."
    )

elif page == "Market Research":
    st.title("📊 Market Research")
    st.info("This page is currently empty and will be developed later.")
