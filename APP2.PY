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
# Market Research Data
# -------------------------------------------------------

market_evolution = pd.DataFrame([
    {"Feature": "Model", "Pre-2023": "Linear", "2026": "Circular"},
    {"Feature": "Technology", "Pre-2023": "Manual + grinding", "2026": "Integrated systems"},
    {"Feature": "Growth", "Pre-2023": "Low", "2026": "High"},
    {"Feature": "Environmental Impact", "Pre-2023": "High leakage", "2026": "Controlled recovery"}
])

technology_comparison = pd.DataFrame([
    {
        "Technology": "Mechanical Recycling",
        "Efficiency Min (%)": 85,
        "Efficiency Max (%)": 90,
        "Energy": "Low",
        "Output": "Recycled plastic",
        "Feedstock": "Clean PET, HDPE, PP",
        "Market Priority": "Priority 1"
    },
    {
        "Technology": "Pyrolysis",
        "Efficiency Min (%)": 70,
        "Efficiency Max (%)": 80,
        "Energy": "High",
        "Output": "Oil, gas, char",
        "Feedstock": "Mixed plastic waste",
        "Market Priority": "Priority 2"
    },
    {
        "Technology": "Gasification",
        "Efficiency Min (%)": 75,
        "Efficiency Max (%)": 85,
        "Energy": "Very High",
        "Output": "Syngas",
        "Feedstock": "Highly mixed waste",
        "Market Priority": "Priority 2"
    },
    {
        "Technology": "Chemical Depolymerization",
        "Efficiency Min (%)": 60,
        "Efficiency Max (%)": 85,
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
    {
        "Contribution Area": "PET recycling",
        "Strategic Score": 9,
        "Market Role": "Bottle-to-flake and bottle-to-pellet recycling"
    },
    {
        "Contribution Area": "HDPE recycling",
        "Strategic Score": 8,
        "Market Role": "Industrial and packaging applications"
    },
    {
        "Contribution Area": "Recycled pellets",
        "Strategic Score": 8,
        "Market Role": "Potential local use and export"
    },
    {
        "Contribution Area": "Informal recovery sector",
        "Strategic Score": 7,
        "Market Role": "Important collection and sorting contribution"
    },
    {
        "Contribution Area": "MENA hub potential",
        "Strategic Score": 8,
        "Market Role": "Regional plastic conversion and recycling growth"
    }
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

market_comparison_data = pd.DataFrame([
    {
        "Market": "Egypt",
        "Plastic Waste (M tons/year)": 5.4,
        "Recycling Rate (%)": 12,
        "Mechanical Recycling Maturity": 7,
        "Chemical Recycling Maturity": 3,
        "Thermal Recycling Maturity": 4,
        "Sorting Automation": 4,
        "Policy Strength": 5,
        "Informal Sector Role (%)": 60,
        "Main Strength": "Strong informal collection and mechanical recycling base",
        "Main Weakness": "Mixed waste quality and limited advanced recycling",
        "Recommended Strategy": "Upgrade sorting + expand mechanical recycling + pilot pyrolysis"
    },
    {
        "Market": "European Union",
        "Plastic Waste (M tons/year)": 30,
        "Recycling Rate (%)": 35,
        "Mechanical Recycling Maturity": 8,
        "Chemical Recycling Maturity": 7,
        "Thermal Recycling Maturity": 6,
        "Sorting Automation": 9,
        "Policy Strength": 9,
        "Informal Sector Role (%)": 5,
        "Main Strength": "Strong regulation, EPR, automated sorting, recycled-content targets",
        "Main Weakness": "High operating cost and strict compliance requirements",
        "Recommended Strategy": "Integrated circular system with high-quality sorting and chemical recycling scale-up"
    },
    {
        "Market": "Japan",
        "Plastic Waste (M tons/year)": 8,
        "Recycling Rate (%)": 25,
        "Mechanical Recycling Maturity": 7,
        "Chemical Recycling Maturity": 7,
        "Thermal Recycling Maturity": 8,
        "Sorting Automation": 8,
        "Policy Strength": 8,
        "Informal Sector Role (%)": 3,
        "Main Strength": "Advanced waste separation and strong waste-to-energy infrastructure",
        "Main Weakness": "High dependence on thermal recovery compared with closed-loop recycling",
        "Recommended Strategy": "Improve material circularity and reduce dependence on energy recovery"
    },
    {
        "Market": "Germany",
        "Plastic Waste (M tons/year)": 6,
        "Recycling Rate (%)": 38,
        "Mechanical Recycling Maturity": 9,
        "Chemical Recycling Maturity": 7,
        "Thermal Recycling Maturity": 7,
        "Sorting Automation": 9,
        "Policy Strength": 9,
        "Informal Sector Role (%)": 2,
        "Main Strength": "Highly developed sorting, EPR system, and industrial recycling market",
        "Main Weakness": "High cost and complex regulatory environment",
        "Recommended Strategy": "Optimize combined mechanical and chemical recycling pathways"
    },
    {
        "Market": "United States",
        "Plastic Waste (M tons/year)": 40,
        "Recycling Rate (%)": 9,
        "Mechanical Recycling Maturity": 6,
        "Chemical Recycling Maturity": 6,
        "Thermal Recycling Maturity": 5,
        "Sorting Automation": 6,
        "Policy Strength": 5,
        "Informal Sector Role (%)": 2,
        "Main Strength": "Large market size and strong private-sector investment potential",
        "Main Weakness": "Low recycling rate and fragmented policy framework",
        "Recommended Strategy": "Increase collection, standardize policy, and scale chemical recycling"
    },
    {
        "Market": "Global Average",
        "Plastic Waste (M tons/year)": 400,
        "Recycling Rate (%)": 9,
        "Mechanical Recycling Maturity": 5,
        "Chemical Recycling Maturity": 4,
        "Thermal Recycling Maturity": 5,
        "Sorting Automation": 4,
        "Policy Strength": 4,
        "Informal Sector Role (%)": 25,
        "Main Strength": "Large global opportunity for circular economy transition",
        "Main Weakness": "More than 90% of plastic waste is not effectively recycled",
        "Recommended Strategy": "Develop hybrid recycling systems adapted to local waste quality"
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
        """
    )

# -------------------------------------------------------
# Page 2: Market Research
# -------------------------------------------------------

elif page == "Market Research":
    st.title("🌍 Comprehensive Plastic Recycling Market Research")
    st.caption("Interactive market research page with section-based navigation, charts, and visuals")

    st.markdown("## Choose Market Research Section")

    section = st.radio(
        "Select section to view:",
        [
            "Global Market Overview",
            "Egypt Market Analysis",
            "Technology Comparison",
            "Egypt vs Global Leaders",
            "Market vs Market Comparison",
            "Egypt Contribution",
            "Industrial Recommendations",
            "References"
        ],
        horizontal=True
    )

    st.markdown("---")

    # ---------------------------------------------------
    # Section 1: Global Market Overview
    # ---------------------------------------------------

    if section == "Global Market Overview":
        st.header("1. Global Market Overview")

        st.markdown("""
        The global plastic system is undergoing a transition toward a circular economy.
        This section presents the default global market values as fixed reference information,
        based on international plastic-waste reports.
        """)

        annual_waste = 400
        projected_waste = 1100

        landfill = 50
        mismanaged = 22
        incinerated = 19
        recycled = 9

        st.subheader("Key Global Plastic Waste Indicators")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Annual Plastic Waste Generation",
            f"{annual_waste}M tons/year"
        )

        col2.metric(
            "Projected Plastic Waste by 2050",
            f"{projected_waste}M tons/year"
        )

        col3.metric(
            "Effective Recycling Rate",
            f"{recycled}%"
        )

        st.info("""
        Global plastic waste generation is currently estimated at around **400 million tons per year**.
        If current production and disposal trends continue, this could increase to around
        **1.1 billion tons per year by 2050**.
        """)

        waste_fate_custom = pd.DataFrame([
            {
                "Waste Fate": "Landfills",
                "Share (%)": landfill,
                "Amount (million tons/year)": annual_waste * landfill / 100
            },
            {
                "Waste Fate": "Mismanaged / Open Dumping",
                "Share (%)": mismanaged,
                "Amount (million tons/year)": annual_waste * mismanaged / 100
            },
            {
                "Waste Fate": "Incineration",
                "Share (%)": incinerated,
                "Amount (million tons/year)": annual_waste * incinerated / 100
            },
            {
                "Waste Fate": "Recycled",
                "Share (%)": recycled,
                "Amount (million tons/year)": annual_waste * recycled / 100
            }
        ])

        st.subheader("Global Plastic Waste Fate Distribution")

        fig_pie = px.pie(
            waste_fate_custom,
            names="Waste Fate",
            values="Share (%)",
            title="Global Plastic Waste Fate Share (%)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        fig_amount = px.bar(
            waste_fate_custom,
            x="Waste Fate",
            y="Amount (million tons/year)",
            text="Amount (million tons/year)",
            title="Estimated Plastic Waste Amount by Fate"
        )
        fig_amount.update_traces(
            texttemplate="%{text:.1f}M tons",
            textposition="outside"
        )
        st.plotly_chart(fig_amount, use_container_width=True)

        st.subheader("Plastic Waste Growth Projection")

        projection_df = pd.DataFrame([
            {
                "Year": 2026,
                "Plastic Waste (million tons/year)": annual_waste
            },
            {
                "Year": 2050,
                "Plastic Waste (million tons/year)": projected_waste
            }
        ])

        fig_projection = px.line(
            projection_df,
            x="Year",
            y="Plastic Waste (million tons/year)",
            markers=True,
            title="Projected Growth of Global Plastic Waste"
        )
        st.plotly_chart(fig_projection, use_container_width=True)

        st.subheader("Circularity Gap")

        circularity_df = pd.DataFrame([
            {
                "Category": "Recycled",
                "Share (%)": recycled
            },
            {
                "Category": "Not Effectively Recycled",
                "Share (%)": 100 - recycled
            }
        ])

        fig_gap = px.bar(
            circularity_df,
            x="Category",
            y="Share (%)",
            text="Share (%)",
            title="Global Circularity Gap in Plastic Waste Management"
        )
        fig_gap.update_traces(
            texttemplate="%{text:.0f}%",
            textposition="outside"
        )
        st.plotly_chart(fig_gap, use_container_width=True)

        st.warning("""
        **Key Insight:**  
        Despite the availability of recycling technologies, around **91% of global plastic waste**
        is still not effectively recycled. This creates a major circularity gap and explains why
        mechanical, chemical, and thermal recycling technologies are increasingly important.
        """)

        st.caption("""
        Source basis: OECD Global Plastics Outlook (2022), UNEP plastic pollution reports,
        and circular-economy literature. Values are used as fixed market-reference indicators
        for dashboard visualization.
        """)

    # ---------------------------------------------------
    # Section 2: Egypt Market Analysis
    # ---------------------------------------------------

    elif section == "Egypt Market Analysis":
        st.header("2. Egypt Market Analysis")

        st.markdown("""
        Egypt is shifting from an informal recycling ecosystem to a semi-industrial circular model.
        Use the inputs below to explore how recycling rate and informal-sector contribution affect market volumes.
        """)

        col_input1, col_input2, col_input3 = st.columns(3)

        with col_input1:
            egypt_plastic_waste = st.number_input(
                "Egypt plastic waste generated (million tons/year)",
                min_value=1.0,
                max_value=20.0,
                value=5.4,
                step=0.1
            )

        with col_input2:
            egypt_recycling_rate = st.slider(
                "Estimated recycling rate (%)",
                min_value=0,
                max_value=60,
                value=12
            )

        with col_input3:
            informal_share = st.slider(
                "Informal sector contribution to collection/sorting (%)",
                min_value=0,
                max_value=100,
                value=60
            )

        recycled_amount = egypt_plastic_waste * egypt_recycling_rate / 100
        non_recycled_amount = egypt_plastic_waste - recycled_amount
        informal_amount = egypt_plastic_waste * informal_share / 100
        formal_amount = egypt_plastic_waste - informal_amount

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Egypt Plastic Waste", f"{egypt_plastic_waste:.1f}M tons/year")
        col2.metric("Recycled Amount", f"{recycled_amount:.2f}M tons/year")
        col3.metric("Non-Recycled Amount", f"{non_recycled_amount:.2f}M tons/year")
        col4.metric("Informal Sector Managed", f"{informal_amount:.2f}M tons/year")

        egypt_recycling_df = pd.DataFrame([
            {"Category": "Recycled", "Amount (million tons/year)": recycled_amount},
            {"Category": "Not Recycled", "Amount (million tons/year)": non_recycled_amount}
        ])

        sector_df = pd.DataFrame([
            {"Sector": "Informal sector", "Amount (million tons/year)": informal_amount},
            {"Sector": "Formal / industrial sector", "Amount (million tons/year)": formal_amount}
        ])

        show_recycling_chart = st.checkbox("Show recycled vs non-recycled chart", value=True)
        show_sector_chart = st.checkbox("Show informal vs formal sector chart", value=True)
        show_market_evolution = st.checkbox("Show market evolution table", value=True)

        if show_recycling_chart:
            fig_egypt_recycling = px.pie(
                egypt_recycling_df,
                names="Category",
                values="Amount (million tons/year)",
                title="Egypt Plastic Waste: Recycled vs Not Recycled"
            )
            st.plotly_chart(fig_egypt_recycling, use_container_width=True)

        if show_sector_chart:
            fig_sector = px.bar(
                sector_df,
                x="Sector",
                y="Amount (million tons/year)",
                text="Amount (million tons/year)",
                title="Estimated Informal vs Formal Sector Contribution"
            )
            fig_sector.update_traces(texttemplate="%{text:.2f}M", textposition="outside")
            st.plotly_chart(fig_sector, use_container_width=True)

        if show_market_evolution:
            st.subheader("Egypt Market Evolution")
            st.dataframe(market_evolution, use_container_width=True)

        st.success("Market Insight: Egypt has a large opportunity to upgrade from semi-manual sorting toward industrial recycling systems.")

    # ---------------------------------------------------
    # Section 3: Technology Comparison
    # ---------------------------------------------------

    elif section == "Technology Comparison":
        st.header("3. Technology Comparison")

        st.markdown("""
        This section compares recycling technologies based on efficiency, energy intensity,
        output type, and suitable feedstock.
        """)

        selected_tech = st.multiselect(
            "Choose technologies to compare:",
            options=technology_comparison["Technology"].tolist(),
            default=technology_comparison["Technology"].tolist()
        )

        tech_filtered = technology_comparison[
            technology_comparison["Technology"].isin(selected_tech)
        ].copy()

        if tech_filtered.empty:
            st.error("Please select at least one technology.")
            st.stop()

        tech_filtered["Efficiency Midpoint (%)"] = (
            tech_filtered["Efficiency Min (%)"] + tech_filtered["Efficiency Max (%)"]
        ) / 2

        show_eff_chart = st.checkbox("Show efficiency comparison chart", value=True)
        show_range_chart = st.checkbox("Show efficiency range chart", value=True)
        show_table = st.checkbox("Show technology comparison table", value=True)

        if show_eff_chart:
            fig_mid = px.bar(
                tech_filtered,
                x="Technology",
                y="Efficiency Midpoint (%)",
                text="Efficiency Midpoint (%)",
                title="Technology Efficiency Midpoint Comparison"
            )
            fig_mid.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            st.plotly_chart(fig_mid, use_container_width=True)

        if show_range_chart:
            fig_range = go.Figure()

            for _, row in tech_filtered.iterrows():
                fig_range.add_trace(go.Scatter(
                    x=[row["Efficiency Min (%)"], row["Efficiency Max (%)"]],
                    y=[row["Technology"], row["Technology"]],
                    mode="lines+markers",
                    name=row["Technology"]
                ))

            fig_range.update_layout(
                title="Efficiency Range by Technology",
                xaxis_title="Efficiency (%)",
                yaxis_title="Technology"
            )
            st.plotly_chart(fig_range, use_container_width=True)

        if show_table:
            display_cols = [
                "Technology",
                "Efficiency Min (%)",
                "Efficiency Max (%)",
                "Energy",
                "Output",
                "Feedstock",
                "Market Priority"
            ]
            st.dataframe(tech_filtered[display_cols], use_container_width=True)

        st.info(
            "Engineering Insight: Mechanical recycling is strongest for clean streams, "
            "while thermal and chemical routes are needed for mixed or contaminated waste."
        )

    # ---------------------------------------------------
    # Section 4: Egypt vs Global Leaders
    # ---------------------------------------------------

    elif section == "Egypt vs Global Leaders":
        st.header("4. Egypt vs Global Leaders")

        st.markdown("""
        This section compares Egypt's recycling-market maturity with global leaders such as the EU and Japan.
        """)

        show_table = st.checkbox("Show comparison table", value=True)
        show_gap_chart = st.checkbox("Show maturity gap chart", value=True)

        maturity_df = pd.DataFrame([
            {"Factor": "Technology", "Egypt Score": 5, "Global Leaders Score": 9},
            {"Factor": "Sorting", "Egypt Score": 4, "Global Leaders Score": 9},
            {"Factor": "Waste Quality Control", "Egypt Score": 4, "Global Leaders Score": 8},
            {"Factor": "Regulation", "Egypt Score": 5, "Global Leaders Score": 9},
            {"Factor": "Industrial Integration", "Egypt Score": 5, "Global Leaders Score": 9}
        ])

        if show_table:
            st.dataframe(egypt_vs_global, use_container_width=True)

        if show_gap_chart:
            gap_data = maturity_df.melt(
                id_vars=["Factor"],
                value_vars=["Egypt Score", "Global Leaders Score"],
                var_name="Region",
                value_name="Maturity Score"
            )

            fig_gap = px.bar(
                gap_data,
                x="Factor",
                y="Maturity Score",
                color="Region",
                barmode="group",
                title="Egypt vs Global Leaders: Recycling Market Maturity Score"
            )
            st.plotly_chart(fig_gap, use_container_width=True)

        st.warning(
            "Key Gap: Egypt needs stronger automated sorting, better feedstock quality control, "
            "and stronger circular-economy regulation."
        )

    # ---------------------------------------------------
    # Section 5: Market vs Market Comparison
    # ---------------------------------------------------

    elif section == "Market vs Market Comparison":
        st.header("🌍 Market vs Market Comparison")

        st.markdown("""
        This section allows you to compare **Egypt with another global market**.
        The comparison focuses on recycling rate, technology maturity, sorting automation,
        policy strength, informal sector role, and strategic recommendations.
        """)

        col_select1, col_select2 = st.columns(2)

        with col_select1:
            market_1 = st.selectbox(
                "Select first market:",
                options=market_comparison_data["Market"].tolist(),
                index=0
            )

        with col_select2:
            market_2_options = market_comparison_data["Market"].tolist()
            default_index = market_2_options.index("European Union")

            market_2 = st.selectbox(
                "Select second market:",
                options=market_2_options,
                index=default_index
            )

        selected_markets_df = market_comparison_data[
            market_comparison_data["Market"].isin([market_1, market_2])
        ].copy()

        if market_1 == market_2:
            st.warning(
                "You selected the same market twice. "
                "Choose two different markets for a stronger comparison."
            )

        st.subheader("1. Market Summary KPIs")

        market_1_data = market_comparison_data[
            market_comparison_data["Market"] == market_1
        ].iloc[0]

        market_2_data = market_comparison_data[
            market_comparison_data["Market"] == market_2
        ].iloc[0]

        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

        kpi_col1.metric(
            f"{market_1} Recycling Rate",
            f"{market_1_data['Recycling Rate (%)']}%"
        )

        kpi_col2.metric(
            f"{market_2} Recycling Rate",
            f"{market_2_data['Recycling Rate (%)']}%"
        )

        kpi_col3.metric(
            f"{market_1} Policy Strength",
            f"{market_1_data['Policy Strength']}/10"
        )

        kpi_col4.metric(
            f"{market_2} Policy Strength",
            f"{market_2_data['Policy Strength']}/10"
        )

        show_market_size = st.checkbox("Show plastic waste generation chart", value=True)
        show_recycling_rate = st.checkbox("Show recycling rate chart", value=True)
        show_technology_maturity = st.checkbox("Show technology maturity chart", value=True)
        show_radar = st.checkbox("Show market readiness radar chart", value=True)
        show_informal = st.checkbox("Show informal sector chart", value=True)
        show_table = st.checkbox("Show strategic comparison table", value=True)

        if show_market_size:
            market_size_chart = px.bar(
                selected_markets_df,
                x="Market",
                y="Plastic Waste (M tons/year)",
                text="Plastic Waste (M tons/year)",
                title="Plastic Waste Generation by Market"
            )
            market_size_chart.update_traces(
                texttemplate="%{text:.1f}M tons",
                textposition="outside"
            )
            st.plotly_chart(market_size_chart, use_container_width=True)

        if show_recycling_rate:
            recycling_chart = px.bar(
                selected_markets_df,
                x="Market",
                y="Recycling Rate (%)",
                text="Recycling Rate (%)",
                title="Recycling Rate Comparison"
            )
            recycling_chart.update_traces(
                texttemplate="%{text:.0f}%",
                textposition="outside"
            )
            st.plotly_chart(recycling_chart, use_container_width=True)

        if show_technology_maturity:
            st.subheader("Technology Maturity Comparison")

            technology_maturity = selected_markets_df.melt(
                id_vars=["Market"],
                value_vars=[
                    "Mechanical Recycling Maturity",
                    "Chemical Recycling Maturity",
                    "Thermal Recycling Maturity"
                ],
                var_name="Technology",
                value_name="Maturity Score"
            )

            technology_chart = px.bar(
                technology_maturity,
                x="Technology",
                y="Maturity Score",
                color="Market",
                barmode="group",
                title="Technology Maturity Score by Market"
            )
            technology_chart.update_yaxes(range=[0, 10])
            st.plotly_chart(technology_chart, use_container_width=True)

        if show_radar:
            st.subheader("Market Readiness Radar Chart")

            fig_radar = go.Figure()

            for _, row in selected_markets_df.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[
                        row["Mechanical Recycling Maturity"],
                        row["Chemical Recycling Maturity"],
                        row["Thermal Recycling Maturity"],
                        row["Sorting Automation"],
                        row["Policy Strength"]
                    ],
                    theta=[
                        "Mechanical Recycling",
                        "Chemical Recycling",
                        "Thermal Recycling",
                        "Sorting Automation",
                        "Policy Strength"
                    ],
                    fill="toself",
                    name=row["Market"]
                ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )
                ),
                title="Market Readiness Radar Comparison",
                showlegend=True
            )

            st.plotly_chart(fig_radar, use_container_width=True)

        if show_informal:
            st.subheader("Informal Sector Role")

            informal_chart = px.bar(
                selected_markets_df,
                x="Market",
                y="Informal Sector Role (%)",
                text="Informal Sector Role (%)",
                title="Informal Sector Role in Collection and Sorting"
            )
            informal_chart.update_traces(
                texttemplate="%{text:.0f}%",
                textposition="outside"
            )
            st.plotly_chart(informal_chart, use_container_width=True)

        if show_table:
            st.subheader("Strategic Comparison Table")

            comparison_table = selected_markets_df[
                [
                    "Market",
                    "Plastic Waste (M tons/year)",
                    "Recycling Rate (%)",
                    "Mechanical Recycling Maturity",
                    "Chemical Recycling Maturity",
                    "Thermal Recycling Maturity",
                    "Sorting Automation",
                    "Policy Strength",
                    "Informal Sector Role (%)",
                    "Main Strength",
                    "Main Weakness",
                    "Recommended Strategy"
                ]
            ]

            st.dataframe(comparison_table, use_container_width=True)

        st.subheader("Interpretation")

        recycling_gap = market_2_data["Recycling Rate (%)"] - market_1_data["Recycling Rate (%)"]
        sorting_gap = market_2_data["Sorting Automation"] - market_1_data["Sorting Automation"]
        policy_gap = market_2_data["Policy Strength"] - market_1_data["Policy Strength"]

        st.markdown(f"""
        ### Main comparison insight

        **{market_1}** has a recycling rate of **{market_1_data['Recycling Rate (%)']}%**, while  
        **{market_2}** has a recycling rate of **{market_2_data['Recycling Rate (%)']}%**.

        The recycling-rate difference is:

        **{recycling_gap:+.0f} percentage points**

        Sorting automation difference:

        **{sorting_gap:+.0f} points out of 10**

        Policy-strength difference:

        **{policy_gap:+.0f} points out of 10**
        """)

        if market_1 == "Egypt" or market_2 == "Egypt":
            st.success("""
            **Egypt-specific conclusion:**  
            Egypt has a strong opportunity to improve its position by upgrading sorting systems,
            strengthening formal recycling infrastructure, and applying a hybrid recycling model:
            mechanical recycling for clean streams, thermal recycling for contaminated waste,
            and chemical recycling for high-quality recovery.
            """)

        st.info("""
        Note: These values are market-screening indicators prepared for visualization and comparison.
        They are suitable for presentation and preliminary strategic analysis, but final investment
        decisions require detailed official datasets and feasibility studies.
        """)

    # ---------------------------------------------------
    # Section 6: Egypt Contribution
    # ---------------------------------------------------

    elif section == "Egypt Contribution":
        st.header("5. Egypt Contribution to the Global and MENA Market")

        st.markdown("""
        Egypt can play a regional hub role in MENA because of its large plastic market,
        informal recovery experience, and potential to expand recycled pellets and PET/HDPE recycling.
        """)

        selected_areas = st.multiselect(
            "Choose contribution areas:",
            options=egypt_contribution["Contribution Area"].tolist(),
            default=egypt_contribution["Contribution Area"].tolist()
        )

        contrib_filtered = egypt_contribution[
            egypt_contribution["Contribution Area"].isin(selected_areas)
        ].copy()

        if contrib_filtered.empty:
            st.error("Please select at least one contribution area.")
            st.stop()

        show_bar = st.checkbox("Show strategic importance chart", value=True)
        show_table = st.checkbox("Show contribution table", value=True)

        if show_bar:
            fig_contrib = px.bar(
                contrib_filtered,
                x="Contribution Area",
                y="Strategic Score",
                text="Strategic Score",
                title="Egypt Contribution Areas: Strategic Importance Score"
            )
            fig_contrib.update_traces(texttemplate="%{text:.0f}/10", textposition="outside")
            st.plotly_chart(fig_contrib, use_container_width=True)

        if show_table:
            st.dataframe(contrib_filtered, use_container_width=True)

        st.success(
            "Market Insight: Egypt’s strongest contribution areas are PET recycling, "
            "HDPE recycling, and recycled-pellet production."
        )

    # ---------------------------------------------------
    # Section 7: Industrial Recommendations
    # ---------------------------------------------------

    elif section == "Industrial Recommendations":
        st.header("6. Industrial Recommendations")

        st.markdown("""
        This section helps select an industrial strategy depending on the target waste stream.
        """)

        waste_type = st.selectbox(
            "Select target waste stream:",
            [
                "Clean PET / HDPE / PP",
                "Mixed contaminated plastic waste",
                "Multilayer plastics",
                "PET requiring high-quality recovery",
                "Highly heterogeneous municipal plastic waste"
            ]
        )

        if waste_type == "Clean PET / HDPE / PP":
            selected_strategy = "Mechanical Recycling"
            explanation = (
                "Use mechanical recycling because it has high efficiency, lower cost, "
                "and is best for clean sorted streams."
            )
        elif waste_type == "Mixed contaminated plastic waste":
            selected_strategy = "Pyrolysis"
            explanation = (
                "Use pyrolysis because it can treat mixed waste and recover oil, gas, and char."
            )
        elif waste_type == "Multilayer plastics":
            selected_strategy = "Thermal / Chemical Recycling"
            explanation = (
                "Use thermal or chemical recycling because multilayer plastics are difficult "
                "to separate mechanically."
            )
        elif waste_type == "PET requiring high-quality recovery":
            selected_strategy = "Chemical Depolymerization"
            explanation = (
                "Use hydrolysis or methanolysis to recover monomers and reduce downcycling."
            )
        else:
            selected_strategy = "Gasification / Integrated Hybrid System"
            explanation = (
                "Use gasification or an integrated system for highly mixed municipal plastic waste."
            )

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"Recommended Strategy: **{selected_strategy}**")

        with col2:
            st.info(explanation)

        show_recommendation_table = st.checkbox("Show full recommendation table", value=True)

        if show_recommendation_table:
            st.dataframe(recommendations, use_container_width=True)

        strategy_scores = pd.DataFrame([
            {
                "Technology": "Mechanical Recycling",
                "Priority Score": 9 if selected_strategy == "Mechanical Recycling" else 6
            },
            {
                "Technology": "Pyrolysis",
                "Priority Score": 9 if selected_strategy == "Pyrolysis" else 7
            },
            {
                "Technology": "Gasification",
                "Priority Score": 9 if "Gasification" in selected_strategy else 6
            },
            {
                "Technology": "Chemical Depolymerization",
                "Priority Score": 9 if selected_strategy == "Chemical Depolymerization" else 6
            },
            {
                "Technology": "Integrated Hybrid System",
                "Priority Score": 10 if "Integrated" in selected_strategy else 8
            }
        ])

        fig_strategy = px.bar(
            strategy_scores,
            x="Technology",
            y="Priority Score",
            text="Priority Score",
            title=f"Technology Priority Score for: {waste_type}"
        )
        fig_strategy.update_traces(texttemplate="%{text:.0f}/10", textposition="outside")
        st.plotly_chart(fig_strategy, use_container_width=True)

        st.header("Strong Closing Insight")

        st.success("""
        The future of plastic recycling is not one technology.

        It is an **Integrated Hybrid Recycling System**:

        - Mechanical recycling for clean streams
        - Thermal recycling for mixed and contaminated waste
        - Chemical recycling for high-quality material recovery
        """)

    # ---------------------------------------------------
    # Section 8: References
    # ---------------------------------------------------

    elif section == "References":
        st.header("7. References for Market Research")

        st.markdown("""
        1. Organisation for Economic Co-operation and Development — *Global Plastics Outlook* (2022)  
        2. World Bank — *What a Waste 2.0*  
        3. International Energy Agency — Plastics and recycling-related reports  
        4. United Nations Environment Programme — Global plastics and circularity reports  
        5. Cairo University technical assessment report on plastic recycling technologies  
        6. European Commission — Circular Economy Action Plan  
        7. Egyptian Environmental Affairs Agency — Egyptian environmental and waste-management context  
        8. Volk et al. (2021) — *Techno-economic assessment and comparison of different plastic recycling pathways: A German case study*  
        """)

        st.info("""
        Note: The market research page is designed for strategic visualization and presentation.
        Some figures are screening-level market assumptions and should be replaced with exact official data if required by the instructor.
        """)
