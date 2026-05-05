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

# =========================
# MARKET ENGINE
# =========================

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

    market_map = {row["Market"]: row for _, row in market.iterrows()}
    a = market_map[m1]
    b = market_map[m2]
    sel = pd.DataFrame([a, b])

    st.markdown("---")

    # =========================
    # RECYCLING RATE
    # =========================

    st.subheader("📊 Recycling Rate Comparison")

    fig = px.bar(sel, x="Market", y="Recycling", text="Recycling")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 Explanation: Recycling Rate"):
        st.markdown("""
The recycling rate represents the **final system output efficiency**.

It measures how much plastic waste successfully returns into usable material instead of ending in landfill or leakage.

### It depends on:
- Collection efficiency
- Sorting quality
- Infrastructure maturity
- Industrial processing capacity

👉 Higher values = stronger circular economy performance
""")

    st.markdown("---")

    # =========================
    # RADAR CHART
    # =========================

    st.subheader("📡 System Radar (Circular Economy Structure Model)")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill="toself",
            name=r["Market"]
        ))

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 Explanation: Radar System"):
        st.markdown("""
This radar shows the **structural maturity of each market’s circular economy system**.

### Axes meaning:
- Mechanical → physical recycling infrastructure
- Chemical → advanced recycling technologies
- Thermal → energy recovery systems
- Sorting → waste separation efficiency
- Policy → regulatory strength

👉 A larger and more balanced shape = a more advanced circular system
""")

    st.markdown("---")

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
        st.markdown("""
System gaps identify **why two markets perform differently**.

### Types of gaps:
- Recycling gap → difference in system output efficiency
- Sorting gap → difference in infrastructure quality
- Policy gap → difference in governance strength

👉 This helps identify whether issues are technological, infrastructural, or regulatory
""")

    st.markdown("---")

    # =========================
    # MCDA SCORE
    # =========================

    st.subheader("🏆 Overall Market Score Index")
    st.caption("MCDA = Multi-Criteria Decision Analysis")

    st.latex(r"""
    Score = 0.30R + 0.25S + 0.25P + 0.10M + 0.10C
    """)

    with st.expander("📖 Explanation: MCDA Model"):
        st.markdown("""
The MCDA score is a **weighted decision model** used to compare markets.

### Components:
- R (Recycling) → system output performance
- S (Sorting) → collection efficiency
- P (Policy) → regulatory strength
- M (Mechanical) → industrial capacity
- C (Chemical) → advanced recycling capability

### Why weights?
Weights reflect importance in circular economy development:
- Recycling & Sorting → highest impact
- Policy → system stability
- Technology → enabling layer

👉 Final score = overall circular economy maturity index
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

    st.markdown("---")

    # =========================
    # CATEGORY WINNERS
    # =========================

    st.subheader("🥇 Category Winners")

    def winner(x, y, key):
        if x[key] > y[key]:
            return m1
        elif x[key] < y[key]:
            return m2
        return "Tie"

    for name, key in {
        "Recycling": "Recycling",
        "Sorting": "Sort",
        "Policy": "Policy",
        "Mechanical": "Mech",
        "Chemical": "Chem",
        "Thermal": "Therm"
    }.items():
        st.write(f"{name}: **{winner(a, b, key)}**")

    with st.expander("📖 Explanation: Category Winners"):
        st.markdown("""
This section identifies **which market leads in each subsystem**.

### Interpretation:
- Infrastructure strength → Sorting, Policy
- Technology strength → Mechanical, Chemical, Thermal
- Output strength → Recycling

👉 This helps break down system performance into components
""")

    st.markdown("---")

    # =========================
    # SYSTEM CLASSIFICATION
    # =========================

    st.subheader("🏗 System Classification")

    def classify(x):
        if x > 30:
            return "Advanced Circular System"
        elif x > 15:
            return "Transition System"
        return "Emerging System"

    def explain(level):
        if level == "Advanced Circular System":
            return "Highly developed circular economy with strong infrastructure and policy enforcement."
        elif level == "Transition System":
            return "System in transition with growing recycling infrastructure."
        return "Early-stage system with limited recycling capacity."

    m1_level = classify(a["Recycling"])
    m2_level = classify(b["Recycling"])

    st.write(f"{m1}: **{m1_level}** → {explain(m1_level)}")
    st.write(f"{m2}: **{m2_level}** → {explain(m2_level)}")

    with st.expander("📖 Explanation: System Classification"):
        st.markdown("""
This classification groups markets into **development stages**.

### Stages:
- Emerging → weak infrastructure, low recycling
- Transition → improving systems and investments
- Advanced → mature circular economy

👉 Based mainly on recycling + system readiness
""")

    st.markdown("---")

    # =========================
    # INVESTMENT PRIORITY
    # =========================

    st.subheader("💰 Investment Priority Map")

    def priority(r):
        if r["Sort"] < 5:
            return "Priority 1: Improve sorting infrastructure"
        elif r["Chem"] < 5:
            return "Priority 2: Expand chemical recycling"
        elif r["Therm"] < 5:
            return "Priority 3: Improve thermal recovery"
        elif r["Policy"] < 5:
            return "Priority 4: Strengthen policy framework"
        return "System is optimized"

    st.write(f"{m1}: {priority(a)}")
    st.write(f"{m2}: {priority(b)}")

    with st.expander("📖 Explanation: Investment Priority"):
        st.markdown("""
Investment priorities are based on **system bottlenecks**.

### Logic:
- Sorting bottleneck → blocks entire recycling chain
- Chemical gap → limits complex plastic processing
- Thermal gap → reduces energy recovery efficiency
- Policy gap → affects long-term system stability

👉 Investment always targets weakest system layer first
""")

    st.markdown("---")

    # =========================
    # FUTURE OUTLOOK
    # =========================

    st.subheader("🌍 Future Outlook")

    def future(r):
        s = r["Recycling"] + r["Sort"] + r["Policy"]

        if s > 35:
            return "Advanced circular transition (closed-loop system forming)"
        elif s > 25:
            return "Strong growth phase (rapid infrastructure expansion)"
        elif s > 15:
            return "Transition phase (industrialization ongoing)"
        return "Early development phase (landfill-dependent system)"

    st.write(f"{m1}: {future(a)}")
    st.write(f"{m2}: {future(b)}")

    with st.expander("📖 Explanation: Future Outlook"):
        st.markdown("""
Future outlook estimates **how fast a market can become circular**.

### Based on:
- Recycling efficiency
- Sorting maturity
- Policy strength

### Interpretation:
- High score → fast circular transition
- Medium score → industrial growth phase
- Low score → early waste management stage

👉 This predicts long-term sustainability trajectory
""")

    st.markdown("---")

    # =========================
    # REFERENCES
    # =========================

    st.subheader("📚 References")

    with st.expander("Show Full References"):
        st.markdown("""
### Global Policy & Reports
- OECD (2022) — Global Plastics Outlook  
- World Bank — What a Waste 2.0  
- UNEP — Circular Economy Reports  
- European Commission — Circular Economy Action Plan  
- IEA — Energy & Waste Systems Reports  

### Academic Sources
- Volk et al. (2021) — Plastic Recycling LCA Study  

### Regional Sources
- Egyptian Environmental Affairs Agency (EEAA)
""")
