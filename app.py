import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Plastic Recycling System Engine",
    page_icon="♻️",
    layout="wide"
)

# =========================
# DATA
# =========================

EUR_TO_EGP = 62.669

df = pd.DataFrame([
    {"Method": "Mechanical", "Efficiency (%)": 88, "Net GWP": 0.18, "Cost EUR": 0.10},
    {"Method": "Pyrolysis", "Efficiency (%)": 75, "Net GWP": 0.25, "Cost EUR": 0.33},
    {"Method": "Hybrid", "Efficiency (%)": 82, "Net GWP": -0.22, "Cost EUR": 0.14}
])

df["Cost EGP"] = df["Cost EUR"] * EUR_TO_EGP

market = pd.DataFrame([
    {"Market": "Egypt", "Recycling": 12, "Sort": 4, "Policy": 5, "Mech": 7, "Chem": 3, "Therm": 4},
    {"Market": "EU", "Recycling": 35, "Sort": 9, "Policy": 9, "Mech": 8, "Chem": 7, "Therm": 6},
    {"Market": "Germany", "Recycling": 38, "Sort": 9, "Policy": 9, "Mech": 9, "Chem": 7, "Therm": 7},
    {"Market": "Japan", "Recycling": 25, "Sort": 8, "Policy": 8, "Mech": 7, "Chem": 7, "Therm": 8},
    {"Market": "USA", "Recycling": 9, "Sort": 6, "Policy": 5, "Mech": 6, "Chem": 6, "Therm": 5},
    {"Market": "China", "Recycling": 20, "Sort": 6, "Policy": 7, "Mech": 7, "Chem": 6, "Therm": 6},
    {"Market": "UAE", "Recycling": 15, "Sort": 6, "Policy": 7, "Mech": 6, "Chem": 5, "Therm": 6},
    {"Market": "Saudi Arabia", "Recycling": 18, "Sort": 6, "Policy": 7, "Mech": 6, "Chem": 5, "Therm": 6}
])

# =========================
# NAVIGATION
# =========================

page = st.sidebar.radio("Navigation", ["Dashboard", "Market Engine"])

# =========================
# DASHBOARD (FIXED)
# =========================

if page == "Dashboard":

    st.title("♻️ Environmental and Economic Comparison of Plastic Recycling Pathways")
    st.caption("Egypt-focused model based on literature benchmarks")

    st.markdown("## Inputs")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_methods = st.multiselect(
            "Select pathways:",
            df["Method"].tolist(),
            default=df["Method"].tolist()
        )

    with col2:
        waste_input = st.number_input(
            "Waste input (kg)",
            min_value=100,
            max_value=10_000_000,
            value=10000,
            step=100
        )

    filtered = df[df["Method"].isin(selected_methods)].copy()

    if filtered.empty:
        st.error("Select at least one method.")
        st.stop()

    # =========================
    # FIXED ENGINEERING VARIABLES
    # =========================

    filtered["GWP kg CO2e/kg"] = filtered["Net GWP"]
    filtered["CED MJ/kg"] = filtered["Efficiency (%)"] * 0.5
    filtered["Cost EGP/kg"] = filtered["Cost EUR"] * EUR_TO_EGP

    filtered["Recovered Output (kg)"] = waste_input * filtered["Efficiency (%)"] / 100
    filtered["Total CO2e (kg)"] = waste_input * filtered["GWP kg CO2e/kg"]
    filtered["Total CED (MJ)"] = waste_input * filtered["CED MJ/kg"]
    filtered["Total Cost (EGP)"] = waste_input * filtered["Cost EGP/kg"]

    # =========================
    # SUMMARY
    # =========================

    st.header("1. Scenario Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Waste Input", f"{waste_input:,} kg")
    c2.metric("Best Efficiency", f"{filtered['Efficiency (%)'].max():.0f}%")
    c3.metric("Lowest GWP", f"{filtered['GWP kg CO2e/kg'].min():.2f}")
    c4.metric("Lowest Cost", f"{filtered['Cost EGP/kg'].min():.2f} EGP/kg")

    # =========================
    # TECH
    # =========================

    st.header("2. Technical Comparison")

    for _, r in filtered.iterrows():
        st.info(f"**{r['Method']}** → Plastic pathway")

    st.plotly_chart(
        px.bar(filtered, x="Method", y="Efficiency (%)", text="Efficiency (%)"),
        use_container_width=True
    )

    # =========================
    # ENVIRONMENT
    # =========================

    st.header("3. Environmental Effects")

    st.plotly_chart(
        px.bar(filtered, x="Method", y="GWP kg CO2e/kg", text="GWP kg CO2e/kg"),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(filtered, x="Method", y="CED MJ/kg", text="CED MJ/kg"),
        use_container_width=True
    )

    # =========================
    # ECONOMY
    # =========================

    st.header("4. Economic Effects")

    st.plotly_chart(
        px.bar(filtered, x="Method", y="Cost EGP/kg", text="Cost EGP/kg"),
        use_container_width=True
    )

    # =========================
    # RESULTS
    # =========================

    st.header("5. Results Table")

    st.dataframe(
        filtered[
            [
                "Method",
                "Recovered Output (kg)",
                "GWP kg CO2e/kg",
                "Total CO2e (kg)",
                "CED MJ/kg",
                "Total CED (MJ)",
                "Cost EGP/kg",
                "Total Cost (EGP)"
            ]
        ].round(2),
        use_container_width=True
    )

# =========================
# MARKET ENGINE
# =========================

else:

    st.title("🌍 Market Engine")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Market 2", market["Market"])

    if m1 == m2:
        st.error("Select different markets")
        st.stop()

    a = market[market["Market"] == m1].iloc[0]
    b = market[market["Market"] == m2].iloc[0]

    sel = pd.DataFrame([a, b])

    st.header("Recycling Rate")

    st.plotly_chart(px.bar(sel, x="Market", y="Recycling"), use_container_width=True)

    st.header("Radar System")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mech", "Chem", "Therm", "Sort", "Policy"],
            fill="toself",
            name=r["Market"]
        ))

    st.plotly_chart(fig, use_container_width=True)

    st.header("MCDA Score")

    def score(x):
        return x["Recycling"]*0.3 + x["Sort"]*0.25 + x["Policy"]*0.25 + x["Mech"]*0.1 + x["Chem"]*0.1

    scores = pd.DataFrame([
        {"Market": m1, "Score": score(a)},
        {"Market": m2, "Score": score(b)}
    ])

    st.plotly_chart(px.bar(scores, x="Market", y="Score", text="Score"), use_container_width=True)
