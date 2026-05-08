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
        "Reason": "Best for clean sorted plastics."
    },
    {
        "Method": "Chemical Recycling - Pyrolysis",
        "Favorite Plastic Type": "Mixed PE, PP, PS",
        "Efficiency (%)": 75,

        "Gross GWP kg CO2e/kg": 0.96,
        "Gross CED MJ/kg": 15.66,
        "Gross Cost EUR/kg": 0.33,

        "Net GWP kg CO2e/kg": 0.25,
        "Net CED MJ/kg": -15.92,
        "Net Cost EUR/kg": -0.24,

        "Clean Score": 6,
        "Egypt Suitability": "Medium",
        "Reason": "Useful for mixed plastic waste."
    },
    {
        "Method": "Combined Mechanical + Chemical Recycling",
        "Favorite Plastic Type": "Mixed + residues",
        "Efficiency (%)": 82,

        "Gross GWP kg CO2e/kg": 0.48,
        "Gross CED MJ/kg": 13.32,
        "Gross Cost EUR/kg": 0.14,

        "Net GWP kg CO2e/kg": -0.22,
        "Net CED MJ/kg": -30.14,
        "Net Cost EUR/kg": -0.29,

        "Clean Score": 10,
        "Egypt Suitability": "High",
        "Reason": "Highest circularity potential."
    }
])

df["Gross Cost EGP/kg"] = df["Gross Cost EUR/kg"] * EUR_TO_EGP
df["Net Cost EGP/kg"] = df["Net Cost EUR/kg"] * EUR_TO_EGP

# -------------------------------------------------------
# Sidebar Navigation (ONLY Dashboard)
# -------------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Dashboard"])

# -------------------------------------------------------
# DASHBOARD ONLY
# -------------------------------------------------------

if page == "Dashboard":

    st.title("♻️ Plastic Recycling Pathways - Egypt Comparison")

    # ---------------- Inputs ----------------
    st.markdown("## Inputs")

    input_col1, input_col2 = st.columns([2, 1])

    with input_col1:
        selected_methods = st.multiselect(
            "Choose recycling pathways:",
            df["Method"].tolist(),
            df["Method"].tolist()
        )

    with input_col2:
        waste_input = st.number_input(
            "Plastic waste input (kg):",
            100, 10_000_000, 10000, 100
        )

    accounting_mode = st.radio(
        "Impact mode:",
        ["Gross impact", "Net impact with substitution credit"],
        horizontal=True
    )

    filtered = df[df["Method"].isin(selected_methods)].copy()

    if filtered.empty:
        st.error("Select at least one method.")
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
    filtered["Total CO2e"] = waste_input * filtered["GWP"]
    filtered["Total CED"] = waste_input * filtered["CED"]
    filtered["Total Cost"] = waste_input * filtered["Cost"]

    # ---------------- Efficiency ----------------
    st.header("1. Efficiency Comparison")

    fig_eff = px.bar(filtered, x="Method", y="Efficiency (%)", text="Efficiency (%)")
    fig_eff.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    st.plotly_chart(fig_eff, use_container_width=True)

    # ---------------- Environmental ----------------
    st.header("2. Environmental Impact")

    fig_gwp = px.bar(filtered, x="Method", y="GWP", text="GWP")
    fig_gwp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_gwp, use_container_width=True)

    fig_ced = px.bar(filtered, x="Method", y="CED", text="CED")
    fig_ced.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_ced, use_container_width=True)

    # ---------------- Economic ----------------
    st.header("3. Economic Impact")

    fig_cost = px.bar(filtered, x="Method", y="Cost", text="Cost")
    fig_cost.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_cost, use_container_width=True)

    # ---------------- Scenario Table ----------------
    st.header("4. Scenario Results")

    st.dataframe(filtered[[
        "Method",
        "Recovered Output (kg)",
        "GWP",
        "Total CO2e",
        "CED",
        "Total CED",
        "Cost",
        "Total Cost"
    ]].round(2), use_container_width=True)

    # ---------------- Favorite Plastic ----------------
    st.header("5. Suitable Plastic Types")

    for _, row in filtered.iterrows():
        st.info(f"{row['Method']} → {row['Favorite Plastic Type']}")

    # ---------------- Recommendation ----------------
    st.header("6. Best Option")

    best = filtered.sort_values(["GWP", "CED", "Cost"]).iloc[0]

    st.success(f"Recommended pathway: **{best['Method']}**")
