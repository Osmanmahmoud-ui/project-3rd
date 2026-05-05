import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Plastic Recycling System",
    page_icon="♻️",
    layout="wide"
)

EUR_TO_EGP = 62.669

# =========================
# DATA: DASHBOARD
# =========================

df = pd.DataFrame([
    {
        "Method": "Mechanical Recycling",
        "Efficiency (%)": 88,
        "Gross GWP": 0.67,
        "Net GWP": 0.18,
        "Gross Cost EUR": 0.10,
        "Net Cost EUR": -0.16
    },
    {
        "Method": "Pyrolysis",
        "Efficiency (%)": 75,
        "Gross GWP": 0.96,
        "Net GWP": 0.25,
        "Gross Cost EUR": 0.33,
        "Net Cost EUR": -0.24
    },
    {
        "Method": "Hybrid System",
        "Efficiency (%)": 82,
        "Gross GWP": 0.48,
        "Net GWP": -0.22,
        "Gross Cost EUR": 0.14,
        "Net Cost EUR": -0.29
    }
])

df["Gross Cost EGP"] = df["Gross Cost EUR"] * EUR_TO_EGP
df["Net Cost EGP"] = df["Net Cost EUR"] * EUR_TO_EGP

# =========================
# DATA: MARKET ENGINE
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
# DASHBOARD
# =========================

if page == "Dashboard":

    st.title("♻️ Plastic Recycling Dashboard")

    waste = st.number_input("Waste input (kg)", 100, 1_000_000, 10000)

    mode = st.radio("Impact mode", ["Gross", "Net"], horizontal=True)

    if mode == "Gross":
        df["GWP"] = df["Gross GWP"]
        df["Cost"] = df["Gross Cost EGP"]
    else:
        df["GWP"] = df["Net GWP"]
        df["Cost"] = df["Net Cost EGP"]

    df["CO2 Impact"] = df["GWP"] * waste

    st.subheader("Efficiency Comparison")
    st.plotly_chart(px.bar(df, x="Method", y="Efficiency (%)", text="Efficiency (%)"))

    st.subheader("Climate Impact")
    st.plotly_chart(px.bar(df, x="Method", y="CO2 Impact", text="CO2 Impact"))

    st.subheader("Cost Impact")
    st.plotly_chart(px.bar(df, x="Method", y="Cost", text="Cost"))

# =========================
# MARKET ENGINE
# =========================

else:

    st.title("🌍 Market vs Market Engine")

    st.markdown("---")

    # -------------------------
    # MARKET SELECTION
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Market 2", market["Market"])

    if m1 == m2:
        st.error("Please select two different markets.")
        st.stop()

    a = market[market["Market"] == m1].iloc[0]
    b = market[market["Market"] == m2].iloc[0]

    sel = pd.DataFrame([a, b])

    st.subheader("📊 Recycling Rate Comparison")
    st.plotly_chart(px.bar(sel, x="Market", y="Recycling", text="Recycling"))

    st.subheader("📡 System Radar")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill="toself",
            name=r["Market"]
        ))

    st.plotly_chart(fig)

    st.subheader("📉 System Gaps")

    st.write("Recycling Gap:", b["Recycling"] - a["Recycling"])
    st.write("Sorting Gap:", b["Sort"] - a["Sort"])
    st.write("Policy Gap:", b["Policy"] - a["Policy"])

    st.subheader("🏆 MCDA Score Index")

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

    st.subheader("🥇 Category Winners")

    def winner(x, y, key):
        return m1 if x[key] > y[key] else m2 if x[key] < y[key] else "Tie"

    st.write("Recycling:", winner(a, b, "Recycling"))
    st.write("Sorting:", winner(a, b, "Sort"))
    st.write("Policy:", winner(a, b, "Policy"))
    st.write("Mechanical:", winner(a, b, "Mech"))
    st.write("Chemical:", winner(a, b, "Chem"))
    st.write("Thermal:", winner(a, b, "Therm"))
