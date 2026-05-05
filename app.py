import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# SAFE PDF IMPORT (FIX)
# =========================
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

st.set_page_config(
    page_title="Plastic Recycling Engine",
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
# MARKET DATA (FIXED + SAUDI)
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
# PDF GENERATOR
# =========================

def generate_pdf(m1, m2, a, b):
    file_path = "market_report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Plastic Waste Market Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Market 1: {m1}", styles["Normal"]))
    content.append(Paragraph(f"Market 2: {m2}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Key Indicators", styles["Heading2"]))
    content.append(Paragraph(f"{m1}: {a['Recycling']}%", styles["Normal"]))
    content.append(Paragraph(f"{m2}: {b['Recycling']}%", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("System Gap", styles["Heading2"]))
    content.append(Paragraph(f"Recycling Gap: {b['Recycling'] - a['Recycling']}%", styles["Normal"]))
    content.append(Paragraph(f"Sorting Gap: {b['Sort'] - a['Sort']}", styles["Normal"]))
    content.append(Paragraph(f"Policy Gap: {b['Policy'] - a['Policy']}", styles["Normal"]))
    content.append(Spacer(1, 12))

    winner = m1 if a["Recycling"] > b["Recycling"] else m2

    content.append(Paragraph("Conclusion", styles["Heading2"]))
    content.append(Paragraph(
        f"{winner} has stronger circular economy performance.",
        styles["Normal"]
    ))

    doc.build(content)
    return file_path

# =========================
# NAVIGATION
# =========================

page = st.sidebar.radio("Navigation", ["Dashboard", "Market Engine"])

# =========================
# DASHBOARD
# =========================

if page == "Dashboard":

    st.title("♻️ Recycling Dashboard")

    waste = st.number_input("Waste (kg)", 100, 1000000, 10000)

    df["CO2"] = waste * df["Net GWP"]

    st.plotly_chart(px.bar(df, x="Method", y="Efficiency (%)"))
    st.plotly_chart(px.bar(df, x="Method", y="CO2"))

# =========================
# MARKET ENGINE
# =========================

else:

    st.title("🌍 Market Comparison Engine")

    col1, col2 = st.columns(2)

    with col1:
        m1 = st.selectbox("Market 1", market["Market"])

    with col2:
        m2 = st.selectbox("Market 2", market["Market"])

    if m1 == m2:
        st.error("Select different markets")
        st.stop()

    sel = market[market["Market"].isin([m1, m2])]

    a = sel[sel["Market"] == m1].iloc[0]
    b = sel[sel["Market"] == m2].iloc[0]

    # =========================
    # CHARTS
    # =========================

    st.subheader("Recycling Comparison")
    st.plotly_chart(px.bar(sel, x="Market", y="Recycling"))

    st.subheader("System Radar")

    fig = go.Figure()

    for _, r in sel.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[r["Mech"], r["Chem"], r["Therm"], r["Sort"], r["Policy"]],
            theta=["Mechanical", "Chemical", "Thermal", "Sorting", "Policy"],
            fill="toself",
            name=r["Market"]
        ))

    st.plotly_chart(fig)

    # =========================
    # ANALYSIS
    # =========================

    st.subheader("System Gap")

    st.write(f"Recycling Gap: {b['Recycling'] - a['Recycling']}%")
    st.write(f"Sorting Gap: {b['Sort'] - a['Sort']}")
    st.write(f"Policy Gap: {b['Policy'] - a['Policy']}")

    winner = m1 if a["Recycling"] > b["Recycling"] else m2
    st.success(f"Better system: {winner}")

    # =========================
    # PDF SECTION
    # =========================

    st.divider()
    st.subheader("📄 Report Generator")

    if not PDF_AVAILABLE:
        st.warning("PDF feature disabled: install reportlab in requirements.txt")
    else:
        if st.button("Generate PDF Report"):

            pdf_file = generate_pdf(m1, m2, a, b)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "Download PDF",
                    f,
                    file_name="market_report.pdf",
                    mime="application/pdf"
                )

    st.info("Auto-generated engineering report from selected markets.")
