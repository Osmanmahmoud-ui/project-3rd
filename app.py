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

    st.title("🌍 Market vs Market Engine (Recycling System Analysis)")

    # =========================
    # MARKET SELECT
    # =========================

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

    # =========================
    # SECTION: COMPARISON
    # =========================

    st.subheader("📊 Recycling Rate Comparison")
    st.plotly_chart(px.bar(sel, x="Market", y="Recycling"))

    # =========================
    # RADAR CHART
    # =========================

    st.subheader("📡 System Radar (Market Structure)")

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
    Radar Explanation:
    Mechanical = clean recycling strength  
    Chemical = advanced recycling capability  
    Thermal = mixed waste handling  
    Sorting = collection system strength  
    Policy = government support level  
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

    # =========================
    # OVERALL SCORE
    # =========================

    st.subheader("🏆 Overall Market Score")

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

    st.info("Combined index of recycling, policy, and technology maturity.")

    # =========================
    # CATEGORY WINNERS
    # =========================

    st.subheader("🥇 Category Winners")

    def winner(x, y, key):
        if x[key] > y[key]:
            return m1
        elif x[key] < y[key]:
            return m2
        else:
            return "Tie"

    categories = {
        "Recycling Rate": "Recycling",
        "Sorting": "Sort",
        "Policy Strength": "Policy",
        "Mechanical Recycling": "Mech",
        "Chemical Recycling": "Chem",
        "Thermal Recycling": "Therm"
    }

    for name, key in categories.items():
        st.write(f"{name}: **{winner(a, b, key)}**")

    # =========================
    # SYSTEM CLASSIFICATION
    # =========================

    st.subheader("🏗 Circular Economy Classification")

    def classify(x):
        if x > 30:
            return "Advanced Circular System"
        elif x > 15:
            return "Transition System"
        else:
            return "Emerging System"

    st.write(f"{m1}: {classify(a['Recycling'])}")
    st.write(f"{m2}: {classify(b['Recycling'])}")

    # =========================
    # ENGINEERING INSIGHT
    # =========================

    st.subheader("🧠 Engineering Insight")

    better = m1 if a["Recycling"] > b["Recycling"] else m2

    st.success(f"""
    {better} shows a stronger circular economy structure due to higher recycling efficiency
    and better system integration between collection, sorting, and processing.
    """)

    # =========================
    # FINAL CONCLUSION
    # =========================

    st.subheader("🏁 Final Conclusion")

    winner_final = m1 if a["Recycling"] > b["Recycling"] else m2

    st.success(f"""
    Final result:
    {winner_final} has the more mature plastic recycling system based on overall circular economy indicators.
    """)

    # =========================
    # REFERENCES
    # =========================

    st.divider()
    st.subheader("📚 References")

    st.markdown("""
    - OECD (2022) — Global Plastics Outlook  
    - UNEP (2023) — Plastic Pollution Report  
    - World Bank (2018) — What a Waste 2.0  
    - European Commission — Circular Economy Action Plan  
    - IEA — Energy & Waste Reports  
    - Volk et al. (2021) — Recycling techno-economic analysis  
    - Ellen MacArthur Foundation — Circular Economy Reports  
    - Egypt EEAA — National Waste Strategy Reports  
    """)

    st.info("References used for benchmarking and system modeling.")
