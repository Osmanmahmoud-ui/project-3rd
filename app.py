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

    st.caption("Direct comparison of actual recycling performance between selected markets.")

    fig = px.bar(sel, x="Market", y="Recycling", text="Recycling")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =========================
    # RADAR
    # =========================

    st.subheader("📡 System Radar (Circular Economy Structure Model)")

    st.caption("Radar represents system structure: technology, infrastructure, and policy readiness.")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill="toself",
            name=r["Market"]
        ))

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =========================
    # GAP ANALYSIS (RADAR-BASED)
    # =========================

    st.subheader("📉 System Gap Analysis")

    st.caption("Gaps are derived from radar system indicators and recycling performance differences.")

    recycling_gap = b["Recycling"] - a["Recycling"]
    sort_gap = b["Sort"] - a["Sort"]
    policy_gap = b["Policy"] - a["Policy"]

    st.write(f"Recycling Gap: {recycling_gap}% → difference in actual recycling efficiency")
    st.write(f"Sorting Gap: {sort_gap} → difference in collection system maturity (radar indicator)")
    st.write(f"Policy Gap: {policy_gap} → difference in governance and regulation strength (radar indicator)")

    st.info("""
    Recycling Gap = output performance difference  
    Sorting/Policy Gap = structural system differences derived from radar indicators
    """)

    st.markdown("---")

    # =========================
    # SCORE INDEX (MCDA EXPLAINED PROPERLY)
    # =========================

    st.subheader("🏆 Overall Market Score Index")

    st.caption("Composite Circular Economy Performance Index (MCDA-based).")

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
    The Overall Market Score is a Multi-Criteria Decision Analysis (MCDA) index.

    It is constructed using circular economy assessment principles inspired by:
    - OECD (2022) Global Plastics Outlook
    - UNEP Circular Economy Frameworks
    - European Commission sustainability indicators

    It combines:
    - Recycling performance (system output)
    - Sorting infrastructure (collection efficiency)
    - Policy strength (governance)
    - Mechanical + chemical recycling (technology readiness)
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

    st.markdown("---")

    # =========================
    # SYSTEM CLASSIFICATION (EXPLAINED)
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
            return "Highly developed circular economy with strong recycling infrastructure, automation, and strict policy enforcement."
        elif level == "Transition System":
            return "Intermediate system shifting from informal recycling to industrial circular economy structures."
        else:
            return "Early-stage system with limited infrastructure and high dependence on landfill and informal recovery."

    m1_level = classify(a["Recycling"])
    m2_level = classify(b["Recycling"])

    st.write(f"{m1}: **{m1_level}** → {explain(m1_level)}")
    st.write(f"{m2}: **{m2_level}** → {explain(m2_level)}")

    st.markdown("---")

    # =========================
    # CAUSE → EFFECT ENGINE
    # =========================

    st.subheader("🧠 Cause → Effect Engine")

    if a["Sort"] < b["Sort"]:
        st.write(f"{m2} has stronger sorting infrastructure → increases recycling efficiency and reduces contamination.")

    if a["Policy"] < b["Policy"]:
        st.write(f"{m2} has stronger policy framework → improves investment and system stability.")

    if a["Mech"] < b["Mech"]:
        st.write(f"{m2} has higher mechanical recycling capacity → better handling of clean plastic streams.")

    if a["Chem"] < b["Chem"]:
        st.write(f"{m2} has higher chemical recycling capability → better treatment of mixed plastic waste.")

    st.markdown("---")

    # =========================
    # DIAGNOSTIC REPORT
    # =========================

    st.subheader("🏥 Country Diagnostic Report")

    def diagnose(r):
        issues = []
        if r["Sort"] < 5:
            issues.append("weak sorting infrastructure")
        if r["Policy"] < 5:
            issues.append("weak policy enforcement")
        if r["Chem"] < 5:
            issues.append("low chemical recycling capacity")
        if r["Therm"] < 5:
            issues.append("limited thermal processing")
        if r["Recycling"] < 20:
            issues.append("low recycling efficiency")
        return issues

    st.write(f"{m1}: {', '.join(diagnose(a)) or 'No major issues'}")
    st.write(f"{m2}: {', '.join(diagnose(b)) or 'No major issues'}")

    st.markdown("---")

    # =========================
    # INVESTMENT PRIORITY MAP
    # =========================

    st.subheader("💰 Investment Priority Map")

    def priority(r):
        if r["Sort"] < 5:
            return "Invest in sorting infrastructure (highest impact)"
        elif r["Chem"] < 5:
            return "Invest in chemical recycling facilities"
        elif r["Therm"] < 5:
            return "Invest in thermal treatment capacity"
        elif r["Policy"] < 5:
            return "Strengthen regulatory framework"
        return "Optimize existing system"

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
            return "Advanced circular transition → closed-loop recycling system development"
        elif s > 25:
            return "Strong growth phase → rapid expansion of recycling infrastructure"
        elif s > 15:
            return "Transition phase → shift from informal to industrial recycling systems"
        else:
            return "Early development phase → reliance on landfill and informal recovery"

    st.write(f"{m1}: {future(a)}")
    st.write(f"{m2}: {future(b)}")

    st.markdown("---")

    # =========================
    # REFERENCES
    # =========================

    st.subheader("📚 References")

    show = st.checkbox("Show References")

    if show:
        st.markdown("""
        - OECD (2022) – Global Plastics Outlook (circular economy indicators)
        - UNEP (2023) – Global Plastic Pollution Assessment
        - World Bank – What a Waste 2.0 (waste system benchmarks)
        - European Commission – Circular Economy Action Plan
        - IEA – Waste and energy system reports
        - Volk et al. (2021) – Techno-economic recycling pathways
        - Ellen MacArthur Foundation – Circular economy system design
        - Egypt EEAA – National waste management reports
        """)
