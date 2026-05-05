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

    st.title("🌍 Market vs Market Engine (Plastic Recycling System Analysis)")
    st.markdown("---")

    # =========================
    # MARKET SELECTION
    # =========================

    st.subheader("🔎 Market Selection")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"], key="m1_select")

    with col2:
        m2 = st.selectbox("Market 2", market["Market"], key="m2_select")

    if m1 == m2:
        st.error("Please select two different markets.")
        st.stop()

    a = market.set_index("Market").loc[m1]
    b = market.set_index("Market").loc[m2]

    sel = pd.DataFrame([a, b])

    st.markdown("---")

    # =========================
    # RECYCLING RATE
    # =========================

    st.subheader("📊 Recycling Rate Comparison")

    fig = px.bar(sel, x=sel.index, y="Recycling", text="Recycling")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 Explanation: Recycling Rate (Improved)"):
        st.write("""
Recycling rate shows how much plastic waste is successfully recovered.

It depends on:
- Collection system efficiency
- Sorting infrastructure quality
- Industrial recycling capacity

👉 Higher value = stronger circular economy + less landfill dependency
""")

    # =========================
    # RADAR CHART
    # =========================

    st.subheader("📡 System Radar (Circular Economy Structure)")

    fig = go.Figure()

    for name, r in zip([m1, m2], [a, b]):
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill="toself",
            name=name
        ))

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 Explanation: System Radar"):
        st.write("""
This radar shows **system maturity**, not just performance.

- Mechanical → physical recycling strength  
- Chemical → advanced recycling capability  
- Thermal → energy recovery systems  
- Sorting → waste separation quality  
- Policy → government enforcement  

👉 Bigger balanced shape = stronger circular economy system
""")

    # =========================
    # GAP ANALYSIS
    # =========================

    st.subheader("📉 System Gap Analysis")

    recycling_gap = b["Recycling"] - a["Recycling"]
    sort_gap = b["Sort"] - a["Sort"]
    policy_gap = b["Policy"] - a["Policy"]

    st.write(f"Recycling Gap: {recycling_gap}%")
    st.write(f"Sorting Gap: {sort_gap}")
    st.write(f"Policy Gap: {policy_gap}")

    with st.expander("📖 Explanation: System Gaps"):
        st.write("""
Gaps explain WHY markets differ:

- Recycling Gap → output efficiency difference  
- Sorting Gap → infrastructure gap  
- Policy Gap → governance strength gap  

👉 This shows where the system is failing or leading
""")

    # =========================
    # MCDA SCORE
    # =========================

    st.subheader("🏆 Overall Market Score Index")

    st.latex(r"Score = 0.30R + 0.25S + 0.25P + 0.10M + 0.10C")

    with st.expander("📖 What do R, S, P, M, C mean?"):
        st.markdown("""
- **R (Recycling Rate)** → final recovered waste  
- **S (Sorting Efficiency)** → separation quality  
- **P (Policy Strength)** → regulation power  
- **M (Mechanical Capacity)** → physical recycling systems  
- **C (Chemical Capacity)** → advanced recycling tech  
""")

    def score(r):
        return (
            r["Recycling"] * 0.30 +
            r["Sort"] * 0.25 +
            r["Policy"] * 0.25 +
            r["Mech"] * 0.10 +
            r["Chem"] * 0.10
        )

    scores = pd.DataFrame([
        {"Market": m1, "Score": score(a)},
        {"Market": m2, "Score": score(b)}
    ])

    st.plotly_chart(px.bar(scores, x="Market", y="Score", text="Score"),
                    use_container_width=True)

    # =========================
    # 🧠 ENGINEERING INTERPRETATION (BUTTON - NO SPACE)
    # =========================

    if "show_eng" not in st.session_state:
        st.session_state.show_eng = False

    if st.button("🧠 Engineering Interpretation"):
        st.session_state.show_eng = not st.session_state.show_eng

    if st.session_state.show_eng:

        st.markdown("### 🔍 Engineering Interpretation (Auto Analysis)")

        winner_market = scores.loc[scores["Score"].idxmax(), "Market"]

        st.success(f"""
**Winner: {winner_market}**

This market performs better due to:
- Stronger recycling infrastructure
- Better sorting efficiency
- More mature policy framework

👉 System bottleneck usually exists in the lower-score market
""")

    # =========================
    # CATEGORY WINNERS + AUTO SUMMARY
    # =========================

    st.subheader("🥇 Category Winners")

    def winner(x, y, key):
        return m1 if x[key] > y[key] else m2 if x[key] < y[key] else "Tie"

    results = {
        "Recycling": winner(a, b, "Recycling"),
        "Sorting": winner(a, b, "Sort"),
        "Policy": winner(a, b, "Policy"),
        "Mechanical": winner(a, b, "Mech"),
        "Chemical": winner(a, b, "Chem"),
        "Thermal": winner(a, b, "Therm")
    }

    for k, v in results.items():
        st.write(f"{k}: **{v}**")

    # AUTO SUMMARY
    st.markdown("### 🧾 Winner Summary")

    best = max(scores["Score"])
    best_market = scores.loc[scores["Score"].idxmax(), "Market"]

    st.info(f"""
Overall, **{best_market}** performs better in this comparison.

This is mainly due to stronger performance in:
- High-impact system layers (Recycling, Sorting, Policy)
- More balanced industrial structure

👉 This suggests better readiness for circular economy transition.
""")

    # =========================
    # 📈 IMPROVEMENT SECTION
    # =========================

    st.subheader("🚀 How to Improve Each Market")

    def improve(m, r):
        tips = []

        if r["Sort"] < 6:
            tips.append("Improve sorting infrastructure (critical bottleneck)")
        if r["Chem"] < 6:
            tips.append("Invest in chemical recycling technologies")
        if r["Therm"] < 6:
            tips.append("Enhance thermal recovery systems")
        if r["Policy"] < 6:
            tips.append("Strengthen environmental regulations")

        if not tips:
            return f"{m}: System already optimized"

        return f"{m}: " + " | ".join(tips)

    st.write(improve(m1, a))
    st.write(improve(m2, b))

    # =========================
    # 📊 BEFORE VS AFTER SIMULATION
    # =========================

    st.subheader("📊 Before vs After Improvement Simulation")

    improved_a = a.copy()
    improved_b = b.copy()

    # simulate improvement
    improved_a["Sort"] += 2
    improved_a["Policy"] += 2
    improved_b["Sort"] += 2
    improved_b["Policy"] += 2

    sim = pd.DataFrame([
        {"Market": m1 + " (Before)", "Score": score(a)},
        {"Market": m1 + " (After)", "Score": score(improved_a)},
        {"Market": m2 + " (Before)", "Score": score(b)},
        {"Market": m2 + " (After)", "Score": score(improved_b)}
    ])

    st.plotly_chart(px.bar(sim, x="Market", y="Score", text="Score"),
                    use_container_width=True)

    # =========================
    # 📚 REFERENCES (CLICKABLE)
    # =========================

    st.subheader("📚 References (Clickable)")

    with st.expander("Show Full References"):

        st.markdown("""
### 🌍 Global Policy & Reports
- [OECD – Global Plastics Outlook (2022)](https://www.oecd.org/environment/plastics/)
- [World Bank – What a Waste 2.0](https://www.worldbank.org/en/topic/urbandevelopment/publication/what-a-waste-2-international-benchmarking)
- [UNEP Circular Economy Reports](https://www.unep.org/circular-economy)
- [European Commission – Circular Economy Action Plan](https://environment.ec.europa.eu/strategy/circular-economy-action-plan_en)
- [IEA Energy & Waste Reports](https://www.iea.org/topics/waste)

### 📘 Academic Sources
- Volk et al. (2021) – Plastic Recycling LCA Study  
  https://doi.org/10.1111/jiec.13012

### 🇪🇬 Regional Sources
- [Egyptian Environmental Affairs Agency (EEAA)](https://www.eeaa.gov.eg/)
""")
