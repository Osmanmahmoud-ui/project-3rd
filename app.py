import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Plastic Recycling Pathways Comparison",
    page_icon="♻️",
    layout="wide"
)

# -------------------------------------------------------
# Currency Conversion
# -------------------------------------------------------
# You can update this value if the exchange rate changes.

EUR_TO_EGP = 62.669

# -------------------------------------------------------
# Case Study Dataset
# Source: Volk et al. (2021) German LWP plastic recycling case study
# Functional unit: 1 kg of mixed lightweight packaging waste input
#
# IMPORTANT:
# Net CED values are negative because they represent energy savings.
# Net cost values are negative because they represent revenues / avoided costs.
# -------------------------------------------------------

df = pd.DataFrame([
    {
        "Scenario": "1.1.1",
        "Method": "Mechanical Recycling",
        "Description": "42% sorting yield + 100% MSWI incineration",
        "Sorting Yield (%)": 42,
        "Carbon Efficiency (%)": 40,
        "Net GWP kg CO2e/kg": 0.25,
        "Net CED MJ/kg": -16.81,
        "Net Cost EUR/kg": -0.16,
    },
    {
        "Scenario": "1.1.2",
        "Method": "Mechanical Recycling - Baseline",
        "Description": "42% sorting yield + 25% MSWI + 75% RDF combustion",
        "Sorting Yield (%)": 42,
        "Carbon Efficiency (%)": 40,
        "Net GWP kg CO2e/kg": 0.18,
        "Net CED MJ/kg": -18.14,
        "Net Cost EUR/kg": -0.16,
    },
    {
        "Scenario": "1.1.3",
        "Method": "Mechanical Recycling",
        "Description": "42% sorting yield + industrial co-combustion mix",
        "Sorting Yield (%)": 42,
        "Carbon Efficiency (%)": 40,
        "Net GWP kg CO2e/kg": 0.01,
        "Net CED MJ/kg": -23.49,
        "Net Cost EUR/kg": -0.16,
    },
    {
        "Scenario": "1.2.1",
        "Method": "Mechanical Recycling - Low Yield",
        "Description": "22% sorting yield + 100% MSWI incineration",
        "Sorting Yield (%)": 22,
        "Carbon Efficiency (%)": 20,
        "Net GWP kg CO2e/kg": 0.66,
        "Net CED MJ/kg": -5.06,
        "Net Cost EUR/kg": -0.08,
    },
    {
        "Scenario": "1.2.2",
        "Method": "Mechanical Recycling - Low Yield",
        "Description": "22% sorting yield + 25% MSWI + 75% RDF combustion",
        "Sorting Yield (%)": 22,
        "Carbon Efficiency (%)": 20,
        "Net GWP kg CO2e/kg": 0.56,
        "Net CED MJ/kg": -6.86,
        "Net Cost EUR/kg": -0.08,
    },
    {
        "Scenario": "1.2.3",
        "Method": "Mechanical Recycling - Low Yield",
        "Description": "22% sorting yield + industrial co-combustion mix",
        "Sorting Yield (%)": 22,
        "Carbon Efficiency (%)": 20,
        "Net GWP kg CO2e/kg": 0.32,
        "Net CED MJ/kg": -14.13,
        "Net Cost EUR/kg": -0.08,
    },
    {
        "Scenario": "2",
        "Method": "Chemical Recycling - Pyrolysis",
        "Description": "Chemical recycling through pyrolysis and steam cracking",
        "Sorting Yield (%)": 0,
        "Carbon Efficiency (%)": 59,
        "Net GWP kg CO2e/kg": 0.25,
        "Net CED MJ/kg": -15.92,
        "Net Cost EUR/kg": -0.24,
    },
    {
        "Scenario": "3.1",
        "Method": "Combined Mechanical + Chemical Recycling",
        "Description": "42% mechanical sorting yield + chemical recycling of residues",
        "Sorting Yield (%)": 42,
        "Carbon Efficiency (%)": 74,
        "Net GWP kg CO2e/kg": -0.22,
        "Net CED MJ/kg": -30.14,
        "Net Cost EUR/kg": -0.29,
    },
    {
        "Scenario": "3.2",
        "Method": "Combined Mechanical + Chemical Recycling - Low Yield",
        "Description": "22% mechanical sorting yield + chemical recycling of residues",
        "Sorting Yield (%)": 22,
        "Carbon Efficiency (%)": 66,
        "Net GWP kg CO2e/kg": 0.01,
        "Net CED MJ/kg": -23.14,
        "Net Cost EUR/kg": -0.25,
    },
])

# Convert cost to EGP
df["Net Cost EGP/kg"] = df["Net Cost EUR/kg"] * EUR_TO_EGP

# Correct interpretation columns
# Negative CED = saving, so multiply by -1 to show saving as positive.
# Negative cost = revenue / economic benefit, so multiply by -1 to show benefit as positive.

df["CED Saving MJ/kg"] = -df["Net CED MJ/kg"]
df["Economic Benefit EUR/kg"] = -df["Net Cost EUR/kg"]
df["Economic Benefit EGP/kg"] = -df["Net Cost EGP/kg"]

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Dashboard", "Data Table", "Method Notes"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Currency")
st.sidebar.write(f"1 EUR = {EUR_TO_EGP:.3f} EGP")

# -------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------

if page == "Dashboard":

    st.title("♻️ Plastic Recycling Pathways Comparison")
    st.caption("Based on the German LWP plastic recycling case study by Volk et al. (2021).")

    st.markdown("## Inputs")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_scenarios = st.multiselect(
            "Choose recycling scenarios:",
            df["Scenario"] + " - " + df["Method"],
            default=[
                "1.1.2 - Mechanical Recycling - Baseline",
                "2 - Chemical Recycling - Pyrolysis",
                "3.1 - Combined Mechanical + Chemical Recycling"
            ]
        )

    with col2:
        waste_input = st.number_input(
            "Plastic waste input (kg):",
            min_value=1,
            max_value=10_000_000,
            value=10_000,
            step=100
        )

    if not selected_scenarios:
        st.error("Please select at least one scenario.")
        st.stop()

    selected_scenario_numbers = [item.split(" - ")[0] for item in selected_scenarios]
    filtered = df[df["Scenario"].isin(selected_scenario_numbers)].copy()

    # -------------------------------------------------------
    # Total Calculations
    # -------------------------------------------------------

    filtered["Total Net GWP kg CO2e"] = waste_input * filtered["Net GWP kg CO2e/kg"]
    filtered["Total Net CED MJ"] = waste_input * filtered["Net CED MJ/kg"]
    filtered["Total CED Saving MJ"] = waste_input * filtered["CED Saving MJ/kg"]
    filtered["Total Net Cost EUR"] = waste_input * filtered["Net Cost EUR/kg"]
    filtered["Total Net Cost EGP"] = waste_input * filtered["Net Cost EGP/kg"]
    filtered["Total Economic Benefit EUR"] = waste_input * filtered["Economic Benefit EUR/kg"]
    filtered["Total Economic Benefit EGP"] = waste_input * filtered["Economic Benefit EGP/kg"]

    # -------------------------------------------------------
    # Key Metrics
    # -------------------------------------------------------

    best_gwp = filtered.loc[filtered["Net GWP kg CO2e/kg"].idxmin()]
    best_ced = filtered.loc[filtered["CED Saving MJ/kg"].idxmax()]
    best_cost = filtered.loc[filtered["Economic Benefit EUR/kg"].idxmax()]

    st.markdown("## Best Options Based on Selected Scenarios")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Lowest Net GWP",
            f"{best_gwp['Net GWP kg CO2e/kg']:.2f} kg CO₂e/kg",
            best_gwp["Scenario"]
        )

    with m2:
        st.metric(
            "Highest CED Saving",
            f"{best_ced['CED Saving MJ/kg']:.2f} MJ/kg saved",
            best_ced["Scenario"]
        )

    with m3:
        st.metric(
            "Highest Economic Benefit",
            f"{best_cost['Economic Benefit EUR/kg']:.2f} €/kg",
            best_cost["Scenario"]
        )

    st.markdown("---")

    chart_config = {
        "displayModeBar": False,
        "staticPlot": True
    }

    # -------------------------------------------------------
    # Carbon Efficiency
    # -------------------------------------------------------

    st.header("1. Carbon Efficiency Comparison")

    fig_eff = px.bar(
        filtered,
        x="Scenario",
        y="Carbon Efficiency (%)",
        color="Method",
        text="Carbon Efficiency (%)",
        hover_data=["Description"]
    )
    fig_eff.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    fig_eff.update_layout(
        yaxis_title="Carbon Efficiency (%)",
        xaxis_title="Scenario",
        showlegend=True
    )
    st.plotly_chart(fig_eff, use_container_width=True, config=chart_config)

    # -------------------------------------------------------
    # GWP
    # -------------------------------------------------------

    st.header("2. Net Global Warming Potential")
    st.caption("Lower is better. Negative values mean avoided emissions / climate benefit.")

    fig_gwp = px.bar(
        filtered,
        x="Scenario",
        y="Net GWP kg CO2e/kg",
        color="Method",
        text="Net GWP kg CO2e/kg",
        hover_data=["Description"]
    )
    fig_gwp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_gwp.update_layout(
        yaxis_title="Net GWP (kg CO₂e/kg input)",
        xaxis_title="Scenario",
        showlegend=True
    )
    st.plotly_chart(fig_gwp, use_container_width=True, config=chart_config)

    # -------------------------------------------------------
    # CED
    # -------------------------------------------------------

    st.header("3. Corrected CED Comparison")
    st.caption(
        "The paper reports net CED as negative values. "
        "For comparison, this chart converts them into positive energy savings."
    )

    fig_ced = px.bar(
        filtered,
        x="Scenario",
        y="CED Saving MJ/kg",
        color="Method",
        text="CED Saving MJ/kg",
        hover_data=["Net CED MJ/kg", "Description"]
    )
    fig_ced.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_ced.update_layout(
        yaxis_title="CED Saving (MJ/kg input)",
        xaxis_title="Scenario",
        showlegend=True
    )
    st.plotly_chart(fig_ced, use_container_width=True, config=chart_config)

    # -------------------------------------------------------
    # Cost
    # -------------------------------------------------------

    st.header("4. Corrected Cost Comparison")
    st.caption(
        "The paper reports net cost as negative values. "
        "Negative cost means revenue / economic benefit, so this chart shows benefit as positive."
    )

    currency = st.radio(
        "Choose currency:",
        ["EUR", "EGP"],
        horizontal=True
    )

    if currency == "EUR":
        cost_y = "Economic Benefit EUR/kg"
        cost_total = "Total Economic Benefit EUR"
        y_label = "Economic Benefit (€/kg input)"
    else:
        cost_y = "Economic Benefit EGP/kg"
        cost_total = "Total Economic Benefit EGP"
        y_label = "Economic Benefit (EGP/kg input)"

    fig_cost = px.bar(
        filtered,
        x="Scenario",
        y=cost_y,
        color="Method",
        text=cost_y,
        hover_data=["Net Cost EUR/kg", "Net Cost EGP/kg", "Description"]
    )
    fig_cost.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_cost.update_layout(
        yaxis_title=y_label,
        xaxis_title="Scenario",
        showlegend=True
    )
    st.plotly_chart(fig_cost, use_container_width=True, config=chart_config)

    # -------------------------------------------------------
    # Scenario Results Table
    # -------------------------------------------------------

    st.header("5. Scenario Results for Selected Waste Input")

    results_table = filtered[[
        "Scenario",
        "Method",
        "Description",
        "Carbon Efficiency (%)",
        "Net GWP kg CO2e/kg",
        "Total Net GWP kg CO2e",
        "Net CED MJ/kg",
        "CED Saving MJ/kg",
        "Total CED Saving MJ",
        "Net Cost EUR/kg",
        "Economic Benefit EUR/kg",
        "Total Economic Benefit EUR",
        "Net Cost EGP/kg",
        "Economic Benefit EGP/kg",
        "Total Economic Benefit EGP"
    ]].copy()

    st.dataframe(results_table.round(2), use_container_width=True)

    # -------------------------------------------------------
    # Interpretation
    # -------------------------------------------------------

    st.header("6. Interpretation")

    st.markdown(f"""
    For **{waste_input:,.0f} kg** of plastic waste input:

    - The lowest climate impact among the selected scenarios is **Scenario {best_gwp['Scenario']}**, with  
      **{best_gwp['Net GWP kg CO2e/kg']:.2f} kg CO₂e/kg input**.

    - The highest cumulative energy saving is **Scenario {best_ced['Scenario']}**, with  
      **{best_ced['CED Saving MJ/kg']:.2f} MJ/kg input saved**.

    - The highest economic benefit is **Scenario {best_cost['Scenario']}**, with  
      **{best_cost['Economic Benefit EUR/kg']:.2f} €/kg input**, equal to approximately  
      **{best_cost['Economic Benefit EGP/kg']:.2f} EGP/kg input**.

    **Important correction:**  
    Net CED and net cost are not interpreted like normal positive impacts.  
    - Net CED = negative value → energy saving.  
    - Net cost = negative value → revenue / economic benefit.  
    Therefore, the comparison charts convert them into positive savings/benefits.
    """)

# -------------------------------------------------------
# DATA TABLE PAGE
# -------------------------------------------------------

elif page == "Data Table":

    st.title("📊 Full Case Study Dataset")

    st.markdown("""
    The table below uses net values per 1 kg of mixed lightweight packaging waste input.
    Negative CED values represent energy savings, and negative cost values represent revenues.
    """)

    st.dataframe(df.round(3), use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Dataset as CSV",
        data=csv,
        file_name="plastic_recycling_case_study_dataset.csv",
        mime="text/csv"
    )

# -------------------------------------------------------
# METHOD NOTES PAGE
# -------------------------------------------------------

elif page == "Method Notes":

    st.title("📘 Method Notes")

    st.markdown("""
    ## Functional Unit

    The functional unit is:

    **1 kg of separately collected mixed lightweight packaging waste input.**

    ## Indicators Used

    ### 1. GWP — Global Warming Potential

    Unit:

    **kg CO₂e/kg input**

    Lower values are better.  
    Negative values mean avoided emissions.

    ### 2. CED — Cumulative Energy Demand

    Unit:

    **MJ/kg input**

    In the original case study, net CED can be negative because primary material substitution creates energy savings.

    Therefore:

    **CED Saving = - Net CED**

    Example:

    If Net CED = -30.14 MJ/kg, then:

    **CED Saving = 30.14 MJ/kg**

    ### 3. Net Cost

    Unit:

    **€/kg input**

    In the original case study, net cost can be negative because the recycling pathway generates revenues or avoids primary material costs.

    Therefore:

    **Economic Benefit = - Net Cost**

    Example:

    If Net Cost = -0.29 €/kg, then:

    **Economic Benefit = 0.29 €/kg**

    ## Why the Calculation Was Corrected

    The previous code used the negative CED and negative cost values directly in the comparison charts.  
    This made the better scenarios appear visually smaller, even though they actually represent higher savings.

    The corrected version keeps the original net values in the table, but uses positive converted values for:

    - CED saving comparison
    - Economic benefit comparison

    ## Main Result

    In the selected case study values, the combined mechanical + chemical recycling pathway, especially Scenario 3.1, performs best overall because it combines:

    - Low or negative net GWP
    - Highest CED saving
    - Highest economic benefit
    - Highest carbon efficiency
    """)

    st.markdown("## References")

    st.markdown("""
    - Volk, R., Stallkamp, C., Steins, J. J., Yogish, S. P., Müller, R. C., Stapf, D., & Schultmann, F. (2021).  
      *Techno-economic assessment and comparison of different plastic recycling pathways: A German case study.*  
      Journal of Industrial Ecology, 25, 1318–1337.
    """)
