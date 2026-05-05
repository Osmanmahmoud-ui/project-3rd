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
        st.write("""
Recycling rate represents the **final output efficiency** of the waste system.

It measures:
- Collection efficiency
- Processing success rate
- Material recovery effectiveness

Higher values = lower landfill dependency and stronger circular economy performance.
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
        st.write("""
This radar represents **structural maturity of the circular economy system**, not output performance.

Each axis means:

- Mechanical → physical processing capability  
- Chemical → advanced recycling technology  
- Thermal → energy recovery systems  
- Sorting → waste collection efficiency  
- Policy → governance strength  

👉 Larger balanced shape = more mature system
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
        st.write("""
System gaps explain **why performance differs between markets**:

- Recycling Gap → final system efficiency difference  
- Sorting Gap → infrastructure maturity difference  
- Policy Gap → governance strength difference  

👉 These gaps show whether differences come from:
technology, infrastructure, or regulation.
""")

    st.markdown("---")

    # =========================
    # MCDA SCORE
    # =========================

    st.subheader("🏆 Overall Market Score Index")

    st.caption("Multi-Criteria Decision Analysis (MCDA) Circular Economy Index")

    st.latex(r"""
    Score = 0.30R + 0.25S + 0.25P + 0.10M + 0.10C
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

    st.plotly_chart(px.bar(scores, x="Market", y="Score", text="Score"), use_container_width=True)

    with st.expander("📖 Explanation: MCDA Score Model"):
        st.write("""
This is a **Multi-Criteria Decision Analysis (MCDA)** model inspired by:

- OECD (2022) Global Plastics Outlook  
- UNEP Circular Economy Framework  
- European Commission sustainability indicators  

It combines:

- Recycling → system output performance  
- Sorting → collection efficiency  
- Policy → governance strength  
- Mechanical + Chemical → technology readiness  

👉 Converts complex system data into one comparable score
""")

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
        st.write("""
This section identifies **which market leads in each subsystem**:

- Infrastructure (Sorting, Policy)  
- Technology (Mechanical, Chemical, Thermal)  
- Performance (Recycling)

👉 Helps isolate strengths and weaknesses per system layer
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
            return "Highly developed circular ecosystem with strong infrastructure and enforcement."
        elif level == "Transition System":
            return "System transitioning from informal to industrial circular economy."
        else:
            return "Early-stage system with limited infrastructure and weak recovery systems."

    m1_level = classify(a["Recycling"])
    m2_level = classify(b["Recycling"])

    st.write(f"{m1}: **{m1_level}** → {explain(m1_level)}")
    st.write(f"{m2}: **{m2_level}** → {explain(m2_level)}")

    st.markdown("---")

    # =========================
    # INVESTMENT PRIORITY
    # =========================

    st.subheader("💰 Investment Priority Map")

    def priority(r):
        if r["Sort"] < 5:
            return "High priority: invest in sorting infrastructure to unlock recycling efficiency."
        elif r["Chem"] < 5:
            return "High priority: expand chemical recycling for mixed plastic streams."
        elif r["Therm"] < 5:
            return "Medium priority: improve thermal recovery capacity."
        elif r["Policy"] < 5:
            return "Strategic priority: strengthen regulatory framework."
        return "Optimization phase: improve efficiency."

    st.write(f"{m1}: {priority(a)}")
    st.write(f"{m2}: {priority(b)}")

    with st.expander("📖 Explanation: Investment Logic"):
        st.write("""
Investment is based on **system bottlenecks**:

- Sorting → unlocks entire recycling chain  
- Chemical → handles complex waste streams  
- Thermal → improves energy recovery  
- Policy → stabilizes investment environment  

👉 Priority goes to the **largest system constraint first**
""")

    st.markdown("---")

    # =========================
    # FUTURE OUTLOOK
    # =========================

    st.subheader("🌍 Future Market Outlook")

    def future(r):
        s = r["Recycling"] + r["Sort"] + r["Policy"]

        if s > 35:
            return "Advanced circular transition → closed-loop system development"
        elif s > 25:
            return "Strong growth phase → rapid infrastructure expansion"
        elif s > 15:
            return "Transition phase → industrialization of waste systems"
        else:
            return "Early development phase → landfill-dependent system"

    st.write(f"{m1}: {future(a)}")
    st.write(f"{m2}: {future(b)}")

    with st.expander("📖 Explanation: Future Outlook"):
        st.write("""
Future outlook is based on **system readiness indicators**:

- Recycling → system efficiency  
- Sorting → infrastructure maturity  
- Policy → governance strength  

👉 Higher combined score = faster circular economy transition
""")

    st.markdown("---")

    # =========================
    # REFERENCES
    # =========================

    st.subheader("📚 References")

    show = st.checkbox("Show References")

    if show:
        st.markdown("""
- OECD (2022) – Global Plastics Outlook  
- UNEP Circular Economy Framework  
- European Commission Sustainability Indicators  
- World Bank Waste Reports  
- Ellen MacArthur Foundation Circular Economy Model  
""")
