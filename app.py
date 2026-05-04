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
# Exchange rate used:
# 1 EUR = 62.669 EGP
#
# The original cost values from Volk et al. (2021) are in EUR/kg.
# They are converted to EGP/kg using:
#
# Cost EGP/kg = Cost EUR/kg × 62.669
# -------------------------------------------------------

EUR_TO_EGP = 62.669

# -------------------------------------------------------
# Dashboard Dataset
# -------------------------------------------------------
# GWP, CED, and EUR cost factors are based on:
# Volk et al. (2021), Techno-economic assessment and comparison
# of different plastic recycling pathways: A German case study.
#
# Important:
# - GWP and CED are benchmark values from a German case study.
# - Cost is converted from EUR/kg to EGP/kg.
# - EEAA is used for Egypt environmental and waste-management context.
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

# Convert all EUR cost factors to EGP
df["Gross Cost EGP/kg"] = df["Gross Cost EUR/kg"] * EUR_TO_EGP
df["Net Cost EGP/kg"] = df["Net Cost EUR/kg"] * EUR_TO_EGP

# -------------------------------------------------------
# Market Research Data
# -------------------------------------------------------

global_waste_fate = pd.DataFrame([
    {"Waste Fate": "Landfills", "Share (%)": 50},
    {"Waste Fate": "Mismanaged / Open Dumping", "Share (%)": 22},
    {"Waste Fate": "Incineration", "Share (%)": 19},
    {"Waste Fate": "Recycled", "Share (%)": 9}
])

market_evolution = pd.DataFrame([
    {"Feature": "Model", "Pre-2023": "Linear", "2026": "Circular"},
    {"Feature": "Technology", "Pre-2023": "Manual + grinding", "2026": "Integrated systems"},
    {"Feature": "Growth", "Pre-2023": "Low", "2026": "High"},
    {"Feature": "Environmental Impact", "Pre-2023": "High leakage", "2026": "Controlled recovery"}
])

technology_comparison = pd.DataFrame([
    {
        "Technology": "Mechanical Recycling",
        "Efficiency": "85–90%",
        "Energy": "Low",
        "Output": "Recycled plastic",
        "Feedstock": "Clean PET, HDPE, PP",
        "Market Priority": "Priority 1"
    },
    {
        "Technology": "Pyrolysis",
        "Efficiency": "70–80%",
        "Energy": "High",
        "Output": "Oil, gas, char",
        "Feedstock": "Mixed plastic waste",
        "Market Priority": "Priority 2"
    },
    {
        "Technology": "Gasification",
        "Efficiency": "75–85%",
        "Energy": "Very High",
        "Output": "Syngas",
        "Feedstock": "Highly mixed waste",
        "Market Priority": "Priority 2"
    },
    {
        "Technology": "Chemical Depolymerization",
        "Efficiency": "Case-dependent",
        "Energy": "Medium to High",
        "Output": "Monomers / chemical feedstock",
        "Feedstock": "PET and selected polymers",
        "Market Priority": "Priority 3"
    }
])

egypt_vs_global = pd.DataFrame([
    {"Factor": "Technology", "Egypt": "Mechanical dominant", "Global Leaders": "Chemical recycling scaling"},
    {"Factor": "Sorting", "Egypt": "Semi-manual", "Global Leaders": "Automated NIR sorting"},
    {"Factor": "Waste Quality", "Egypt": "Mixed and variable", "Global Leaders": "More controlled streams"},
    {"Factor": "Regulation", "Egypt": "Developing", "Global Leaders": "EPR, plastic taxes, recycled content targets"},
    {"Factor": "Market Model", "Egypt": "Informal + emerging industrial", "Global Leaders": "Industrial circular systems"}
])

egypt_contribution = pd.DataFrame([
    {"Contribution Area": "PET recycling", "Market Role": "Bottle-to-flake and bottle-to-pellet recycling"},
    {"Contribution Area": "HDPE recycling", "Market Role": "Industrial and packaging applications"},
    {"Contribution Area": "Recycled pellets", "Market Role": "Potential local use and export"},
    {"Contribution Area": "Informal recovery sector", "Market Role": "Important collection and sorting contribution"},
    {"Contribution Area": "MENA hub potential", "Market Role": "Regional plastic conversion and recycling growth"}
])

recommendations = pd.DataFrame([
    {
        "Priority": "Priority 1",
        "Technology": "Mechanical Recycling",
        "Target Waste": "PET, HDPE, PP",
        "Reason": "Lowest cost, highest maturity, high efficiency for clean sorted streams"
    },
    {
        "Priority": "Priority 2",
        "Technology": "Thermal Recycling: Pyrolysis / Gasification",
        "Target Waste": "Mixed, contaminated, multilayer plastics",
        "Reason": "Useful for waste that cannot be mechanically recycled"
    },
    {
        "Priority": "Priority 3",
        "Technology": "Chemical Recycling: Hydrolysis / Methanolysis",
        "Target Waste": "PET and selected polymers",
        "Reason": "Reduces downcycling and recovers higher-quality chemical feedstock"
    }
])

# -------------------------------------------------------
# Sidebar Navigation Only
# -------------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Market Research"]
)

# -------------------------------------------------------
# Page 1: Dashboard
# -------------------------------------------------------

if page == "Dashboard":
    st.title("♻️ Environmental and Economic Comparison of Plastic Recycling Pathways")
    st.caption("Egypt-focused dashboard using benchmark factors from Volk et al. (2021) and Egypt waste-context sources")

    st.markdown("## Dashboard Inputs")

    input_col1, input_col2 = st.columns([2, 1])

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

    accounting_mode = st.radio(
        "Choose impact accounting mode:",
        ["Gross impact", "Net impact with substitution credit"],
        horizontal=True
    )

    st.info(
        "Gross impact means direct recycling-process burden only. "
        "Net impact includes credits for avoiding virgin plastic production. "
        "Negative net values mean savings compared with virgin plastic production."
    )

    filtered = df[df["Method"].isin(selected_methods)].copy()

    if filtered.empty:
        st.error("Please select at least one recycling pathway.")
        st.stop()

    if accounting_mode == "Gross impact":
        gwp_col = "Gross GWP kg CO2e/kg"
        ced_col = "Gross CED MJ/kg"
        cost_col_egp = "Gross Cost EGP/kg"
    else:
        gwp_col = "Net GWP kg CO2e/kg"
        ced_col = "Net CED MJ/kg"
        cost_col_egp = "Net Cost EGP/kg"

    filtered["Selected GWP kg CO2e/kg"] = filtered[gwp_col]
    filtered["Selected CED MJ/kg"] = filtered[ced_col]
    filtered["Selected Cost EGP/kg"] = filtered[cost_col_egp]

    filtered["Recovered Output (kg)"] = waste_input * filtered["Efficiency (%)"] / 100
    filtered["Total CO2e (kg)"] = waste_input * filtered["Selected GWP kg CO2e/kg"]
    filtered["Total CED (MJ)"] = waste_input * filtered["Selected CED MJ/kg"]
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
    fig_gwp.update_traces(texttemplate="%{text:.2f} kg CO₂e/kg", textposition="outside")
    st.plotly_chart(fig_gwp, use_container_width=True)

    fig_ced = px.bar(
        filtered,
        x="Method",
        y="Selected CED MJ/kg",
        text="Selected CED MJ/kg",
        title=f"Cumulative Energy Demand - {accounting_mode}"
    )
    fig_ced.update_traces(texttemplate="%{text:.2f} MJ/kg", textposition="outside")
    st.plotly_chart(fig_ced, use_container_width=True)

    st.header("4. Economic Effects")

    fig_cost_egp = px.bar(
        filtered,
        x="Method",
        y="Selected Cost EGP/kg",
        text="Selected Cost EGP/kg",
        title=f"Cost per kg Input in EGP - {accounting_mode}"
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
            "Selected Cost EGP/kg",
            "Total Cost (EGP)"
        ]
    ].copy()

    scenario_data["Recovered Output (kg)"] = scenario_data["Recovered Output (kg)"].round(0)
    scenario_data["Selected GWP kg CO2e/kg"] = scenario_data["Selected GWP kg CO2e/kg"].round(2)
    scenario_data["Total CO2e (kg)"] = scenario_data["Total CO2e (kg)"].round(2)
    scenario_data["Selected CED MJ/kg"] = scenario_data["Selected CED MJ/kg"].round(2)
    scenario_data["Total CED (MJ)"] = scenario_data["Total CED (MJ)"].round(2)
    scenario_data["Selected Cost EGP/kg"] = scenario_data["Selected Cost EGP/kg"].round(2)
    scenario_data["Total Cost (EGP)"] = scenario_data["Total Cost (EGP)"].round(2)

    st.dataframe(scenario_data, use_container_width=True)

    st.header("6. Cost Conversion Explanation")

    st.markdown(f"""
    The original cost values in Volk et al. (2021) are reported in **€/kg input**.

    For this dashboard, they were converted to Egyptian Pound using:

    **Cost EGP/kg = Cost EUR/kg × {EUR_TO_EGP}**

    Example for mechanical recycling gross cost:

    **0.10 €/kg × {EUR_TO_EGP} = {0.10 * EUR_TO_EGP:.2f} EGP/kg**

    Therefore, when the waste input is **{waste_input:,.0f} kg**, the total cost is:

    **Total Cost = Waste Input × Cost EGP/kg**
    """)

    st.header("7. Engineering Recommendation")

    ranking = filtered.sort_values(
        by=["Selected GWP kg CO2e/kg", "Selected CED MJ/kg", "Selected Cost EGP/kg"],
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

    st.header("8. Data Sources and Calculation Method")

    st.markdown(
        """
        **Main benchmark paper used for GWP, CED, and cost factors:**

        Volk et al. (2021), *Techno-economic assessment and comparison of different plastic recycling pathways: A German case study*, Journal of Industrial Ecology.

        **Equations used in the dashboard:**

        Recovered Output = Waste Input × Efficiency / 100

        Total GWP = Waste Input × GWP factor

        Total CED = Waste Input × CED factor

        Cost EGP/kg = Cost EUR/kg × Exchange Rate

        Total Cost in EGP = Waste Input × Cost EGP/kg

        **Important limitation:**

        These GWP, CED, and cost factors are German benchmark values. They are used as a technical estimate because detailed Egyptian LCA factors from EEAA are not available as one direct dataset. EEAA sources should be used to describe the Egyptian environmental and waste-management context, while the paper provides numerical benchmark factors.
        """
    )

# -------------------------------------------------------
# Page 2: Market Research
# -------------------------------------------------------

elif page == "Market Research":
    st.title("🌍 Comprehensive Plastic Recycling Market Research")
    st.caption("Global and Egypt market analysis for plastic recycling technologies")

    st.markdown("""
    This page summarizes the market research supporting the technical dashboard.  
    It connects the engineering comparison with global circular-economy trends, Egypt’s market position, and future industrial opportunities.
    """)

    st.header("1. Global Market Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Annual Plastic Waste", "≈ 400M tons/year")
    col2.metric("Projected by 2050", "≈ 1.1B tons/year")
    col3.metric("Currently Recycled", "≈ 9%")

    st.markdown("""
    The global plastic system is moving toward a **circular economy model**, driven by climate targets,
    marine pollution control, ESG regulations, and corporate recycled-content commitments.
    """)

    fig_global_fate = px.pie(
        global_waste_fate,
        names="Waste Fate",
        values="Share (%)",
        title="Global Plastic Waste Fate Distribution"
    )
    st.plotly_chart(fig_global_fate, use_container_width=True)

    st.warning(
        "Key Insight: Despite technical feasibility, more than 90% of global plastic waste is still not effectively recycled."
    )

    st.header("2. Technological Shift")

    shift_col1, shift_col2 = st.columns(2)

    with shift_col1:
        st.subheader("Traditional Direction")
        st.info("""
        **Mechanical Recycling**
        - Mature and widely applied
        - Best for clean PET, HDPE, and PP
        - Lower cost and lower energy demand
        - Limited by contamination and downcycling
        """)

    with shift_col2:
        st.subheader("Emerging Direction")
        st.success("""
        **Chemical and Thermal Recycling**
        - Can treat mixed and contaminated waste
        - Can produce chemical feedstock or fuel-like outputs
        - Useful for multilayer plastics
        - Requires higher investment and stricter control
        """)

    st.header("3. Egypt Market Analysis")

    egypt_col1, egypt_col2, egypt_col3 = st.columns(3)

    egypt_col1.metric("Plastic Waste Generated", "≈ 5.4M tons/year")
    egypt_col2.metric("Estimated Recycling Rate", "≈ 10–15%")
    egypt_col3.metric("Informal Sector Role", "≈ 60% collection/sorting")

    st.markdown("""
    Egypt is moving from an informal recycling ecosystem toward a more semi-industrial circular model.
    Mechanical recycling remains dominant, but there is increasing interest in integrated sorting,
    pelletizing, pyrolysis, and industrial-scale recycling systems.
    """)

    st.subheader("Egypt Market Evolution")

    st.dataframe(market_evolution, use_container_width=True)

    st.header("4. Why Egypt's Recycling Market is Growing")

    growth_col1, growth_col2 = st.columns(2)

    with growth_col1:
        st.success("""
        **Efficiency Improvements**
        - Mechanical recycling can reach 85–90% efficiency for clean PET and HDPE.
        - Better sorting lines improve product quality.
        """)

        st.info("""
        **Infrastructure Development**
        - Sorting lines
        - Washing lines
        - Pelletizing plants
        - Industrial-scale recyclers
        """)

    with growth_col2:
        st.warning("""
        **New Revenue Streams**
        - Pyrolysis oil
        - Gas
        - Char
        - Recycled pellets
        """)

        st.error("""
        **Policy and Environmental Pressure**
        - Waste leakage reduction
        - Ministry of Environment initiatives
        - National sustainability and circular-economy direction
        """)

    st.header("5. Technology Comparison")

    st.dataframe(technology_comparison, use_container_width=True)

    efficiency_chart_data = pd.DataFrame([
        {"Technology": "Mechanical Recycling", "Efficiency Midpoint (%)": 87.5},
        {"Technology": "Pyrolysis", "Efficiency Midpoint (%)": 75},
        {"Technology": "Gasification", "Efficiency Midpoint (%)": 80}
    ])

    fig_tech_eff = px.bar(
        efficiency_chart_data,
        x="Technology",
        y="Efficiency Midpoint (%)",
        text="Efficiency Midpoint (%)",
        title="Technology Efficiency Comparison"
    )
    fig_tech_eff.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig_tech_eff, use_container_width=True)

    st.header("6. Egypt vs Global Leaders")

    st.dataframe(egypt_vs_global, use_container_width=True)

    st.markdown("""
    Global leaders such as the EU and Japan are ahead in automated sorting, chemical recycling capacity,
    extended producer responsibility, and recycled-content regulation. Egypt still depends strongly on
    mechanical recycling and informal sorting, but this creates a strong opportunity for upgrading.
    """)

    st.header("7. Key Technical Challenge")

    st.error("""
    Egypt has a high mixed-waste challenge. This makes mechanical recycling alone insufficient.
    Thermal technologies such as pyrolysis and gasification can target contaminated and multilayer plastic waste,
    but they require strong environmental control systems.
    """)

    st.info("""
    For pyrolysis and thermal degradation, activation energy values commonly range around **120–270 kJ/mol**,
    depending on plastic composition, heating rate, and catalyst use.
    """)

    st.header("8. Egypt Contribution to the Global Market")

    st.dataframe(egypt_contribution, use_container_width=True)

    contribution_chart = px.bar(
        egypt_contribution,
        x="Contribution Area",
        y=[1, 1, 1, 1, 1],
        text="Market Role",
        title="Egypt's Potential Contribution Areas",
        labels={"value": "Strategic Importance", "variable": ""}
    )
    contribution_chart.update_layout(showlegend=False)
    st.plotly_chart(contribution_chart, use_container_width=True)

    st.header("9. Industrial Recommendations")

    st.dataframe(recommendations, use_container_width=True)

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    with rec_col1:
        st.success("""
        **Priority 1: Mechanical Recycling**
        - PET
        - HDPE
        - PP
        - Lowest cost and highest maturity
        """)

    with rec_col2:
        st.warning("""
        **Priority 2: Thermal Recycling**
        - Pyrolysis
        - Gasification
        - For mixed and contaminated waste
        """)

    with rec_col3:
        st.info("""
        **Priority 3: Chemical Recycling**
        - Hydrolysis
        - Methanolysis
        - For higher-quality recovery
        """)

    st.header("10. Strong Closing Insight")

    st.success("""
    The future of plastic recycling is not one technology.

    It is an **Integrated Hybrid Recycling System**:

    - Mechanical recycling for clean streams
    - Thermal recycling for mixed and contaminated waste
    - Chemical recycling for high-quality material recovery
    """)

    st.header("11. References for Market Research")

    st.markdown("""
    1. Organisation for Economic Co-operation and Development — *Global Plastics Outlook* (2022)  
    2. World Bank — *What a Waste 2.0*  
    3. International Energy Agency — Plastics and recycling-related reports  
    4. United Nations Environment Programme — Global plastics and circularity reports  
    5. Cairo University technical assessment report on plastic recycling technologies  
    6. European Commission — Circular Economy Action Plan  
    7. Egyptian Environmental Affairs Agency — Egyptian environmental and waste-management context  
    """)
