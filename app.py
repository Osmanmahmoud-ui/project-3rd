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
# DASHBOARD DATA (UNCHANGED)
# =========================

EUR_TO_EGP = 62.669

df = pd.DataFrame([
    {"Method": "Mechanical", "Efficiency (%)": 88, "Net GWP": 0.18, "Cost EUR": 0.10},
    {"Method": "Pyrolysis", "Efficiency (%)": 75, "Net GWP": 0.25, "Cost EUR": 0.33},
    {"Method": "Hybrid", "Efficiency (%)": 82, "Net GWP": -0.22, "Cost EUR": 0.14}
])

df["Cost EGP"] = df["Cost EUR"] * EUR_TO_EGP

# =========================
# MARKET DATA (FIXED + SAUDI INCLUDED)
# =========================

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
# DASHBOARD (UNCHANGED LOGIC)
# =========================

if page == "Dashboard":

    st.title("♻️ Plastic Recycling Dashboard")

    waste = st.number_input("Waste input (kg)", 100, 1000000, 10000)

    df["CO2 Impact"] = waste * df["Net GWP"]

    st.subheader("Efficiency Comparison")
    st.plotly_chart(px.bar(df, x="Method", y="Efficiency (%)"))

    st.subheader("Climate Impact")
    st.plotly_chart(px.bar(df, x="Method", y="CO2 Impact"))

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

    st.info("""
Recycling rate represents the **final system output efficiency**.
It reflects how much plastic waste is successfully diverted from landfill into recovery systems.
    """)

    st.markdown("---")

    # =========================
    # RADAR
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

    st.info("""
The radar chart represents the **structural readiness of the circular economy system**.

- Mechanical → physical processing capacity  
- Chemical → advanced material recovery  
- Thermal → energy recovery systems  
- Sorting → collection efficiency  
- Policy → regulatory strength  

A larger and more balanced shape indicates a more mature circular ecosystem.
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

    st.info("""
### Interpretation of Gaps:

- **Recycling Gap** → measures final system efficiency difference  
  → directly impacts waste diversion performance  

- **Sorting Gap** → reflects upstream infrastructure maturity  
  → higher sorting leads to higher recycling yield  

- **Policy Gap** → reflects governance strength  
  → determines investment stability and system enforcement  

👉 Together, these gaps show whether differences come from **technology, infrastructure, or governance**
    """)

    st.markdown("---")

    # =========================
    # SCORE INDEX
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

    st.plotly_chart(px.bar(scores, x="Market", y="Score", text="Score"))

    st.info("""
### MCDA Model Explanation:

This index is a **Multi-Criteria Decision Analysis (MCDA)** framework inspired by:

- OECD (2022) Global Plastics Outlook  
- UNEP Circular Economy Framework  
- European Commission sustainability indicators  

### What it combines:

- Recycling → system output performance  
- Sorting → collection efficiency  
- Policy → governance strength  
- Mechanical + Chemical → technology readiness  

👉 The goal is to convert a complex circular economy system into a **single comparable performance score**
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

    st.info("""
This section identifies **dominant system leadership by category**.

It helps isolate whether a market leads in:
- infrastructure (sorting, policy)
- technology (mechanical, chemical)
- or performance output (recycling)
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
            return "System shifting from informal recycling to industrial circular economy."
        else:
            return "Early-stage system with limited infrastructure and weak recovery systems."

    m1_level = classify(a["Recycling"])
    m2_level = classify(b["Recycling"])

    st.write(f"{m1}: **{m1_level}** → {explain(m1_level)}")
    st.write(f"{m2}: **{m2_level}** → {explain(m2_level)}")

    st.markdown("---")

    # =========================
    # INVESTMENT PRIORITY MAP
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
            return "Strategic priority: strengthen governance and regulatory enforcement."
        return "Optimization phase: focus on efficiency improvements."

    st.write(f"{m1}: {priority(a)}")
    st.write(f"{m2}: {priority(b)}")

    st.markdown("---")

    # =========================
    # FUTURE OUTLOOK
    # =========================

    st.subheader("🌍 Future Market Outlook")

    def future(r):
        s = r["Recycling"] + r["Sort"] + r["Policy"]

        if s > 35:
            return "Advanced circular transition → movement toward closed-loop recycling economy."
        elif s > 25:
            return "Strong growth phase → rapid expansion of infrastructure and regulatory frameworks."
        elif s > 15:
            return "Transition phase → shift from informal to industrial waste management systems."
        else:
            return "Early development phase → high dependency on landfill and informal recovery systems."

    st.write(f"{m1}: {future(a)}")
    st.write(f"{m2}: {future(b)}")

    st.info("""
### Interpretation:

Future outlook is based on **system readiness (recycling + sorting + policy)**.

- High scores → mature circular economies  
- Medium scores → scaling industrial systems  
- Low scores → emerging waste management systems  

👉 This shows **where each market is heading, not just where it is now**
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
- World Bank Waste Management Reports  
- Ellen MacArthur Foundation Circular Economy Model  
        """)
