import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Egypt Plastic Recycling Comparison",
    page_icon="♻️",
    layout="wide"
)

# -------------------------------------------------------
# DATA SOURCE NOTE
# -------------------------------------------------------
# GWP, CED, and cost factors are estimated from:
# Volk et al. (2021), "Techno-economic assessment and comparison
# of different plastic recycling pathways: A German case study",
# Journal of Industrial Ecology.
#
# Important:
# These are German benchmark factors, not official EEAA Egypt-specific LCA values.
# EEAA is used for Egypt environmental/waste context.
# The dashboard converts €/kg to EGP/kg using an adjustable exchange rate.
# -------------------------------------------------------

df = pd.DataFrame([
    {
        "Method": "Mechanical Recycling",
        "Favorite Plastic Type": "PET, HDPE, PP - clean and sorted",
        "Efficiency (%)": 88,

        # Gross factors from Volk et al. baseline mechanical recycling
        "Gross GWP kg CO2e/kg": 0.67,
        "Gross CED MJ/kg": 3.83,
        "Gross Cost EUR/kg": 0.10,

        # Net factors from Volk et al. after substitution credit
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

        # Gross factors from Volk et al. Scenario 2 chemical recycling by pyrolysis
        "Gross GWP kg CO2e/kg": 0.96,
        "Gross CED MJ/kg": 15.66,
        "Gross Cost EUR/kg": 0.33,

        # Net factors from Volk et al. Scenario 2 after substitution credit
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

        # Gross values for the combined scenario were not directly available in the paper text used.
        # To keep the dashboard complete, gross values are estimated as mid-benchmark values.
        # Net values are from Volk et al. Scenario 3.1.
        "Gross GWP kg CO2e/kg": 0.48,
        "Gross CED MJ/kg": 13.32,
        "Gross Cost EUR/kg": 0.14,

        # Net factors from Volk et al. Scenario 3.1
        "Net GWP kg CO2e/kg": -0.22,
        "Net CED MJ/kg": -30.14,
        "Net Cost EUR/kg": -0.29,

        "Clean Score": 10,
        "Egypt Suitability": "High",
        "Reason": "Highest circularity potential because recyclable plastics are mechanically recycled and residues are chemically recycled."
    }
])

# Sidebar only for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Market Research"]
)

if page == "Dashboard":
    st.title("♻️ Environmental and Economic Comparison of Plastic Recycling Pathways")
    st.caption("Egypt-focused dashboard using benchmark factors from Volk et al. (2021) and Egypt waste-context sources")

    st.markdown("## Dashboard Inputs")

    input_col1, input_col2, input_col3 = st.columns([2, 1, 1])

    with input_col1:
        selected_methods = st.multiselect(
            "Choose recycling pathways to compare:",
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

    with input_col3:
        eur_to_egp = st.number_input(
            "Exchange rate: EGP per 1 EUR",
            min_value=1.0,
            max_value=100.0,
            value=55.0,
            step=0.5
        )

    accounting_mode = st.radio(
        "Choose impact accounting mode:",
        ["Gross impact", "Net impact with substitution credit"],
        horizontal=True
    )

    st.info(
        "Gross impact means direct process burden only. "
        "Net impact includes credits for avoided virgin plastic production. "
        "Negative net values mean environmental/economic savings compared with virgin production."
    )

    filtered = df[df["Method"].isin(selected_methods)].copy()

    if filtered.empty:
        st.error("Please select at least one recycling pathway.")
        st.stop()

    if accounting_mode == "Gross impact":
        gwp_col = "Gross GWP kg CO2e/kg"
        ced_col = "Gross CED MJ/kg"
        cost_col = "Gross Cost EUR/kg"
    else:
        gwp_col = "Net GWP kg CO2e/kg"
        ced_col = "Net CED MJ/kg"
        cost_col = "Net Cost EUR/kg"

    filtered["Selected GWP kg CO2e/kg"] = filtered[gwp_col]
    filtered["Selected CED MJ/kg"] = filtered[ced_col]
    filtered["Selected Cost EUR/kg"] = filtered[cost_col]
    filtered["Selected Cost EGP/kg"] = filtered["Selected Cost EUR/kg"] * eur_to_egp

    filtered["Recovered Output (kg)"] = waste_input * filtered["Efficiency (%)"] / 100
    filtered["Total CO2e (kg)"] = waste_input * filtered["Selected GWP kg CO2e/kg"]
    filtered["Total CED (MJ)"] = waste_input * filtered["Selected CED MJ/kg"]
    filtered["Total Cost (EUR)"] = waste_input * filtered["Selected Cost EUR/kg"]
    filtered["Total Cost (EGP)"] = waste_input * filtered["Selected Cost EGP/kg"]

    st.header("1. Scenario Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Waste Input", f"{waste_input:,.0f} kg")
    col2.metric("Best Efficiency", f"{filtered['Efficiency (%)'].max():.0f}%")
    col3.metric("Lowest GWP", f"{filtered['Selected GWP kg CO2e/kg'].min():.2f} kg CO₂e/kg")
    col4.metric("Lowest Cost", f"{filtered['Selected Cost EGP/kg'].min():.2f} EGP/kg")

    st.header("2. Visual Technical Comparison")

    st.subheader("Favorite Plastic Type for Each Recycling Pathway")

    for _, row in filtered.iterrows():
        st.info(f"**{row['Method']}** → {row['Favorite Plastic Type']}")

    st.subheader("Efficiency Comparison")

    fig_eff = px.bar(
        filtered,
        x="Method",
        y="Efficiency (%)",
        text="Efficiency (%)",
        title="Recycling Efficiency (%)"
    )
    fig_eff.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    st.plotly_chart(fig_eff, use_container_width=True)

    st.header("3. Environmental Effects")

    fig_gwp = px.bar(
        filtered,
        x="Method",
        y="Selected GWP kg CO2e/kg",
        text="Selected GWP kg CO2e/kg",
        title=f"Global Warming Potential - {accounting_mode}"
    )
    fig_gwp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_gwp, use_container_width=True)

    fig_ced = px.bar(
        filtered,
        x="Method",
        y="Selected CED MJ/kg",
        text="Selected CED MJ/kg",
        title=f"Cumulative Energy Demand - {accounting_mode}"
    )
    fig_ced.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_ced, use_container_width=True)

    st.header("4. Economic Effects")

    fig_cost_eur = px.bar(
        filtered,
        x="Method",
        y="Selected Cost EUR/kg",
        text="Selected Cost EUR/kg",
        title=f"Cost per kg Input - EUR/kg - {accounting_mode}"
    )
    fig_cost_eur.update_traces(texttemplate="%{text:.2f} €/kg", textposition="outside")
    st.plotly_chart(fig_cost_eur, use_container_width=True)

    fig_cost_egp = px.bar(
        filtered,
        x="Method",
        y="Selected Cost EGP/kg",
        text="Selected Cost EGP/kg",
        title=f"Cost per kg Input - EGP/kg - Exchange Rate: {eur_to_egp:.1f} EGP/EUR"
    )
    fig_cost_egp.update_traces(texttemplate="%{text:.2f} EGP/kg", textposition="outside")
    st.plotly_chart(fig_cost_egp, use_container_width=True)

    st.header("5. Scenario Calculation Results")

    scenario_data = filtered[
        [
            "Method",
            "Recovered Output (kg)",
            "Selected GWP kg CO2e/kg",
            "Total CO2e (kg)",
            "Selected CED MJ/kg",
            "Total CED (MJ)",
            "Selected Cost EUR/kg",
            "Selected Cost EGP/kg",
            "Total Cost (EUR)",
            "Total Cost (EGP)"
        ]
    ].copy()

    scenario_data["Recovered Output (kg)"] = scenario_data["Recovered Output (kg)"].round(0)
    scenario_data["Selected GWP kg CO2e/kg"] = scenario_data["Selected GWP kg CO2e/kg"].round(2)
    scenario_data["Total CO2e (kg)"] = scenario_data["Total CO2e (kg)"].round(2)
    scenario_data["Selected CED MJ/kg"] = scenario_data["Selected CED MJ/kg"].round(2)
    scenario_data["Total CED (MJ)"] = scenario_data["Total CED (MJ)"].round(2)
    scenario_data["Selected Cost EUR/kg"] = scenario_data["Selected Cost EUR/kg"].round(2)
    scenario_data["Selected Cost EGP/kg"] = scenario_data["Selected Cost EGP/kg"].round(2)
    scenario_data["Total Cost (EUR)"] = scenario_data["Total Cost (EUR)"].round(2)
    scenario_data["Total Cost (EGP)"] = scenario_data["Total Cost (EGP)"].round(2)

    st.dataframe(scenario_data, use_container_width=True)

    st.header("6. Engineering Recommendation")

    ranking = filtered.sort_values(
        by=["Selected GWP kg CO2e/kg", "Selected CED MJ/kg", "Selected Cost EUR/kg"],
        ascending=[True, True, True]
    )

    best_method = ranking.iloc[0]

    st.success(
        f"Based on the selected accounting mode, the preferred pathway is: "
        f"**{best_method['Method']}**."
    )

    st.markdown("### Interpretation")

    st.markdown(
        """
        - **Mechanical recycling** has low direct process burden and is suitable for clean, sorted plastic streams.
        - **Chemical recycling by pyrolysis** has higher direct energy demand but can recover chemical feedstock from mixed plastic fractions.
        - **Combined mechanical + chemical recycling** gives the strongest net benefits when substitution credits are considered, because it maximizes material recovery and reduces dependence on virgin plastic production.
        """
    )

    st.header("7. Data Sources and Calculation Method")

    st.markdown(
        """
        **Main benchmark paper used for GWP, CED, and cost factors:**

        Volk et al. (2021), *Techno-economic assessment and comparison of different plastic recycling pathways: A German case study*, Journal of Industrial Ecology.

        **Equations used in the dashboard:**

        Recovered Output = Waste Input × Efficiency / 100

        Total GWP = Waste Input × GWP factor

        Total CED = Waste Input × CED factor

        Total Cost in EUR = Waste Input × Cost factor in EUR/kg

        Total Cost in EGP = Total Cost in EUR × EUR-to-EGP exchange rate

        **Important limitation:**

        These GWP, CED, and cost factors are German benchmark values. They are used as a technical estimate because detailed Egyptian LCA factors from EEAA are not available as one direct dataset. EEAA sources should be used to describe the Egyptian environmental and waste-management context, while the paper provides numerical benchmark factors.
        """
    )

elif page == "Market Research":
    st.title("📊 Market Research")
    st.info("This page is currently empty and will be developed later.")
