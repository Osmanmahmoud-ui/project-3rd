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

    st.caption("Choose two markets to compare their circular economy performance.")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Market 2", market["Market"])

    if m1 == m2:
        st.error("Please select two different markets")
        st.stop()

    sel = market[market["Market"].isin([m1, m2])]
    a = sel[sel["Market"] == m1].iloc[0]
    b = sel[sel["Market"] == m2].iloc[0]

    st.markdown("---")

    # =========================
    # RECYCLING RATE
    # =========================

    st.subheader("📊 Recycling Rate Comparison")

    st.caption("Shows how much plastic waste is actually recycled in each market.")

    st.plotly_chart(px.bar(sel, x="Market", y="Recycling"))

    st.markdown("---")

    # =========================
    # RADAR CHART
    # =========================

    st.subheader("📡 Circular System Radar")

    st.caption("Visual comparison of recycling system strength across 5 dimensions.")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill="toself",
            name=r["Market"]
        ))

    st.plotly_chart(fig)

    st.info("""
    Radar Meaning:
    - Mechanical → clean recycling ability  
    - Chemical → advanced material recovery  
    - Thermal → ability to handle mixed waste  
    - Sorting → collection system strength  
    - Policy → government regulation strength  
    """)

    st.markdown("---")

    # =========================
    # GAP ANALYSIS
    # =========================

    st.subheader("📉 System Gap Analysis")

    st.caption("Shows direct performance differences between both markets.")

    recycling_gap = b["Recycling"] - a["Recycling"]
    sort_gap = b["Sort"] - a["Sort"]
    policy_gap = b["Policy"] - a["Policy"]

    st.write(f"Recycling Gap: **{recycling_gap}%**")
    st.write(f"Sorting Gap: **{sort_gap} points**")
    st.write(f"Policy Gap: **{policy_gap} points**")

    st.markdown("---")

    # =========================
    # OVERALL SCORE
    # =========================

    st.subheader("🏆 Overall Market Score Index")

    st.caption("A weighted index combining recycling, policy, and technology maturity.")

    def score(r):
        return (
            r["Recycling"] * 0.3 +
            r["Sort"] * 0.25 +
            r["Policy"] * 0.25 +
            r["Mech"] * 0.1 +
            r["Chem"] * 0.1
        )

    scores = pd.DataFrame([
        {"Market": m1, "Score": score(a)},
        {"Market": m2, "Score": score(b)}
    ])

    st.plotly_chart(px.bar(scores, x="Market", y="Score", text="Score"))

    st.markdown("---")

    # =========================
    # CATEGORY WINNERS
    # =========================

    st.subheader("🥇 Category Winner Breakdown")

    st.caption("Shows which market performs better in each system category.")

    def winner(x, y, key):
        if x[key] > y[key]:
            return m1
        elif x[key] < y[key]:
            return m2
        else:
            return "Tie"

    categories = {
        "Recycling Rate": "Recycling",
        "Sorting System": "Sort",
        "Policy Strength": "Policy",
        "Mechanical Recycling": "Mech",
        "Chemical Recycling": "Chem",
        "Thermal Recycling": "Therm"
    }

    for name, key in categories.items():
        st.write(f"**{name} →** {winner(a, b, key)}")

    st.markdown("---")

    # =========================
    # SYSTEM CLASSIFICATION
    # =========================

    st.subheader("🏗 Circular Economy Level")

    st.caption("Classifies each market into a development stage of recycling maturity.")

    def classify(x):
        if x > 30:
            return "Advanced Circular System"
        elif x > 15:
            return "Transition System"
        else:
            return "Emerging System"

    st.write(f"{m1}: **{classify(a['Recycling'])}**")
    st.write(f"{m2}: **{classify(b['Recycling'])}**")

    st.markdown("---")

    # =========================
    # ENGINEERING INSIGHT
    # =========================

    st.subheader("🧠 Engineering Insight Generator")

    st.caption("Automatically generates a system-level interpretation of the comparison.")

    better = m1 if a["Recycling"] > b["Recycling"] else m2

    st.success(f"""
    {better} demonstrates stronger circular economy performance due to higher recycling efficiency
    and better integration of collection, sorting, and processing systems.
    """)

    st.markdown("---")

    # =========================
    # FINAL CONCLUSION
    # =========================

    st.subheader("🏁 Final System Conclusion")

    st.caption("Final decision output similar to consulting report conclusion.")

    winner_final = m1 if a["Recycling"] > b["Recycling"] else m2

    st.success(f"""
    Final conclusion:
    {winner_final} has the more mature plastic recycling system based on overall system indicators.
    """)

    st.markdown("---")

    # =========================
    # REFERENCES (EXPLAINED)
    # =========================

    st.subheader("📚 References (Explained by Usage)")

    st.markdown("""
    - OECD (2022) → Used for global recycling rate benchmarks and circular economy indicators.  
    - UNEP (2023) → Provides global plastic pollution and waste management trends.  
    - World Bank (What a Waste 2.0) → Used for country-level waste generation and system comparison.  
    - European Commission → Used for policy strength and circular economy regulation benchmarks (EU/Germany).  
    - IEA Reports → Used for energy demand and waste-to-energy technology comparison.  
    - Volk et al. (2021) → Used for technical recycling efficiency and cost assumptions.  
    - Ellen MacArthur Foundation → Used for circular economy system design logic.  
    - Egypt EEAA Reports → Used for Egypt-specific waste structure and informal sector role.
    """)

    st.info("""
    These references are used to build a hybrid benchmarking model combining technical, environmental,
    and policy-based indicators across all markets.
    """)
