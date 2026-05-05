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
    # MARKET SELECTION (FIXED BUG)
    # =========================

    st.subheader("🔎 Market Selection")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"], key="m1_select")

    with col2:
        m2 = st.selectbox("Market 2", market["Market"], key="m2_select")

    if m1 == m2:
        st.error("Please select two different markets")
        st.stop()

    # FIX: ensure correct mapping always updates dynamically
    market_map = {row["Market"]: row for _, row in market.iterrows()}

    a = market_map[m1]
    b = market_map[m2]

    sel = pd.DataFrame([a, b])

    st.markdown("---")

    # =========================
    # RECYCLING RATE (FIXED DISPLAY BUG)
    # =========================

    st.subheader("📊 Recycling Rate Comparison")

    st.caption("Compares actual recycling performance between selected markets.")

    fig_rate = px.bar(sel, x="Market", y="Recycling", text="Recycling")
    fig_rate.update_traces(texttemplate="%{text}%", textposition="outside")

    st.plotly_chart(fig_rate, use_container_width=True)

    st.markdown("---")

    # =========================
    # RADAR
    # =========================

    st.subheader("📡 System Radar")

    st.caption("Shows technical maturity of each recycling system.")

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
    Radar meaning:
    Mechanical = clean recycling  
    Chemical = advanced recycling  
    Thermal = mixed waste handling  
    Sorting = collection system  
    Policy = government strength  
    """)

    st.markdown("---")

    # =========================
    # GAP ANALYSIS (EXPLAINED)
    # =========================

    st.subheader("📉 System Gap Analysis")

    recycling_gap = b["Recycling"] - a["Recycling"]
    sort_gap = b["Sort"] - a["Sort"]
    policy_gap = b["Policy"] - a["Policy"]

    st.write(f"Recycling Gap: **{recycling_gap}%** → difference in actual recycling efficiency")
    st.write(f"Sorting Gap: **{sort_gap}** → difference in collection system strength")
    st.write(f"Policy Gap: **{policy_gap}** → difference in government support level")

    st.markdown("---")

    # =========================
    # SCORE INDEX (EXPLAINED)
    # =========================

    st.subheader("🏆 Overall Market Score Index")

    st.caption("Weighted score combining environmental, technical, and policy factors.")

    def score(r):
        return (
            r["Recycling"] * 0.30 +   # main performance driver
            r["Sort"] * 0.25 +        # collection efficiency
            r["Policy"] * 0.25 +      # regulation strength
            r["Mech"] * 0.10 +        # mechanical capability
            r["Chem"] * 0.10          # advanced recycling
        )

    scores = pd.DataFrame([
        {"Market": m1, "Score": score(a)},
        {"Market": m2, "Score": score(b)}
    ])

    st.plotly_chart(px.bar(scores, x="Market", y="Score", text="Score"))

    st.info("""
    Score explanation:
    - Recycling has highest weight because it reflects real system output  
    - Sorting + Policy represent system infrastructure  
    - Mechanical + Chemical represent technology maturity  
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

    categories = {
        "Recycling": "Recycling",
        "Sorting": "Sort",
        "Policy": "Policy",
        "Mechanical": "Mech",
        "Chemical": "Chem",
        "Thermal": "Therm"
    }

    for name, key in categories.items():
        st.write(f"**{name}:** {winner(a, b, key)}")

    st.markdown("---")

    # =========================
    # CLASSIFICATION
    # =========================

    st.subheader("🏗 System Classification")

    def classify(x):
        if x > 30:
            return "Advanced System"
        elif x > 15:
            return "Transition System"
        return "Emerging System"

    st.write(f"{m1}: {classify(a['Recycling'])}")
    st.write(f"{m2}: {classify(b['Recycling'])}")

    st.markdown("---")

    # =========================
    # INSIGHT
    # =========================

    st.subheader("🧠 Engineering Insight")

    better = m1 if a["Recycling"] > b["Recycling"] else m2

    st.success(f"""
    {better} shows stronger circular economy performance due to higher recycling efficiency
    and better system integration across collection and processing stages.
    """)

    st.markdown("---")

    # =========================
    # FINAL CONCLUSION
    # =========================

    st.subheader("🏁 Final Conclusion")

    winner_final = m1 if a["Recycling"] > b["Recycling"] else m2

    st.success(f"""
    Final conclusion:
    {winner_final} has the more mature plastic recycling system based on system-level indicators.
    """)

    st.markdown("---")

    # =========================
    # REFERENCES (TOGGLE BUTTON)
    # =========================

    st.subheader("📚 References")

    show_refs = st.checkbox("Show / Hide References")

    if show_refs:

        st.markdown("""
        - OECD (2022) → Recycling benchmarks and circular economy KPIs  
        - UNEP (2023) → Global plastic pollution trends  
        - World Bank → Waste generation and country comparison  
        - European Commission → Policy strength (EU/Germany benchmark)  
        - IEA → Energy and waste processing systems  
        - Volk et al. (2021) → Recycling efficiency + cost modeling  
        - Ellen MacArthur Foundation → Circular system logic  
        - Egypt EEAA → Local waste structure and informal sector data  
        """)

        st.info("These references support environmental, technical, and policy indicators used in the model.")

    else:
        st.caption("References hidden (click checkbox to display)")
