import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

st.set_page_config(
    page_title="Plastic Recycling Comparison Engine",
    page_icon="♻️",
    layout="wide"
)

# =======================================================
# DASHBOARD DATA (UNCHANGED)
# =======================================================

EUR_TO_EGP = 62.669

df = pd.DataFrame([
    {
        "Method": "Mechanical Recycling",
        "Efficiency (%)": 88,
        "Gross GWP kg CO2e/kg": 0.67,
        "Net GWP kg CO2e/kg": 0.18,
        "Gross Cost EUR/kg": 0.10,
        "Net Cost EUR/kg": -0.16
    },
    {
        "Method": "Pyrolysis",
        "Efficiency (%)": 75,
        "Gross GWP kg CO2e/kg": 0.96,
        "Net GWP kg CO2e/kg": 0.25,
        "Gross Cost EUR/kg": 0.33,
        "Net Cost EUR/kg": -0.24
    },
    {
        "Method": "Hybrid Recycling",
        "Efficiency (%)": 82,
        "Gross GWP kg CO2e/kg": 0.48,
        "Net GWP kg CO2e/kg": -0.22,
        "Gross Cost EUR/kg": 0.14,
        "Net Cost EUR/kg": -0.29
    }
])

df["Gross Cost EGP/kg"] = df["Gross Cost EUR/kg"] * EUR_TO_EGP
df["Net Cost EGP/kg"] = df["Net Cost EUR/kg"] * EUR_TO_EGP

# =======================================================
# MARKET DATA (FIXED + UPDATED + SAUDI ADDED)
# =======================================================

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

# =======================================================
# PDF GENERATOR
# =======================================================

def generate_pdf(m1, m2, a, b):
    file_path = "/mnt/data/market_report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Plastic Waste Market Comparison Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"<b>Market 1:</b> {m1}", styles["Normal"]))
    content.append(Paragraph(f"<b>Market 2:</b> {m2}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Key Indicators</b>", styles["Heading2"]))
    content.append(Paragraph(f"{m1} Recycling Rate: {a['Recycling']}%", styles["Normal"]))
    content.append(Paragraph(f"{m2} Recycling Rate: {b['Recycling']}%", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>System Gaps</b>", styles["Heading2"]))
    content.append(Paragraph(f"Recycling Gap: {b['Recycling'] - a['Recycling']}%", styles["Normal"]))
    content.append(Paragraph(f"Sorting Gap: {b['Sort'] - a['Sort']}", styles["Normal"]))
    content.append(Paragraph(f"Policy Gap: {b['Policy'] - a['Policy']}", styles["Normal"]))
    content.append(Spacer(1, 12))

    winner = m1 if a["Recycling"] > b["Recycling"] else m2

    content.append(Paragraph("<b>Conclusion</b>", styles["Heading2"]))
    content.append(Paragraph(
        f"{winner} shows stronger circular economy performance based on system indicators.",
        styles["Normal"]
    ))

    doc.build(content)
    return file_path

# =======================================================
# SIDEBAR
# =======================================================

page = st.sidebar.radio("Navigation", ["Dashboard", "Market Engine"])

# =======================================================
# DASHBOARD (UNCHANGED)
# =======================================================

if page == "Dashboard":

    st.title("♻️ Plastic Recycling Dashboard")

    waste = st.number_input("Waste input (kg)", 100, 1000000, 10000)

    df["CO2"] = waste * df["Net GWP kg CO2e/kg"]

    st.plotly_chart(px.bar(df, x="Method", y="Efficiency (%)"))
    st.plotly_chart(px.bar(df, x="Method", y="CO2"))

# =======================================================
# MARKET ENGINE
# =======================================================

else:

    st.title("🌍 Market vs Market Engine")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Market 2", market["Market"])

    if m1 == m2:
        st.error("Select two different markets")
        st.stop()

    sel = market[market["Market"].isin([m1, m2])]

    a = sel[sel["Market"] == m1].iloc[0]
    b = sel[sel["Market"] == m2].iloc[0]

    st.subheader("📊 Recycling Comparison")

    st.plotly_chart(px.bar(sel, x="Market", y="Recycling"))

    st.subheader("🧭 Radar System")

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

    st.write(f"Recycling Gap: {b['Recycling'] - a['Recycling']}%")
    st.write(f"Sorting Gap: {b['Sort'] - a['Sort']}")
    st.write(f"Policy Gap: {b['Policy'] - a['Policy']}")

    st.subheader("🧠 Insight")

    winner = m1 if a["Recycling"] > b["Recycling"] else m2
    st.success(f"{winner} has stronger recycling system overall.")

    # ===================================================
    # PDF EXPORT
    # ===================================================

    st.divider()
    st.subheader("📄 Generate Report")

    if st.button("Generate PDF Report"):

        pdf_file = generate_pdf(m1, m2, a, b)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="market_comparison_report.pdf",
                mime="application/pdf"
            )

    st.info("This report summarizes the full market comparison in a structured engineering format.")
