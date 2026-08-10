import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="DataGuard Investigator",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ DataGuard Investigator")
st.subheader("AI-powered fraud detection and investigation")

st.write(
    "Analyze suspicious transactions, identify risk signals, "
    "and generate an investigation summary."
)

st.divider()

# Transaction details
st.header("🔎 Transaction Investigation")

col1, col2 = st.columns(2)

with col1:
    transaction_id = st.text_input(
        "Transaction ID",
        placeholder="e.g. TXN-10025"
    )

    amount = st.number_input(
        "Transaction Amount (KES)",
        min_value=0.0,
        value=1000.0
    )

    location = st.text_input(
        "Transaction Location",
        placeholder="e.g. Nairobi"
    )

with col2:
    account_age = st.number_input(
        "Account Age (days)",
        min_value=0,
        value=365
    )

    failed_attempts = st.number_input(
        "Failed Login Attempts",
        min_value=0,
        value=0
    )

    new_device = st.checkbox("Transaction from a new device")

st.divider()

if st.button("🚨 Investigate Transaction", use_container_width=True):

    risk_score = 0
    risk_reasons = []

    # Amount risk
    if amount >= 100000:
        risk_score += 30
        risk_reasons.append("Very large transaction amount")
    elif amount >= 50000:
        risk_score += 20
        risk_reasons.append("High transaction amount")

    # Account age risk
    if account_age < 30:
        risk_score += 20
        risk_reasons.append("Very new account")

    # Failed login risk
    if failed_attempts >= 5:
        risk_score += 25
        risk_reasons.append("Multiple failed login attempts")
    elif failed_attempts >= 3:
        risk_score += 15
        risk_reasons.append("Several failed login attempts")

    # Device risk
    if new_device:
        risk_score += 20
        risk_reasons.append("Transaction made from a new device")

    risk_score = min(risk_score, 100)

    # Risk level
    if risk_score >= 70:
        risk_level = "🔴 HIGH RISK"
    elif risk_score >= 40:
        risk_level = "🟠 MEDIUM RISK"
    else:
        risk_level = "🟢 LOW RISK"

    st.header("Investigation Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Risk Score", f"{risk_score}/100")

    with col2:
        st.metric("Risk Level", risk_level)

    st.subheader("🚩 Risk Signals")

    if risk_reasons:
        for reason in risk_reasons:
            st.warning(reason)
    else:
        st.success("No major risk signals detected.")

    st.subheader("📋 Investigation Summary")

    st.write(
        f"""
        **Transaction:** {transaction_id or "Not provided"}

        **Amount:** KES {amount:,.2f}

        **Location:** {location or "Not provided"}

        **Investigation time:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        **Recommendation:** 
        {"Investigate this transaction further before approving it."
        if risk_score >= 40
        else
        "Transaction currently appears relatively low risk, but continue monitoring."}
        """
    )

st.divider()

st.caption(
    "DataGuard Investigator — Prototype for AI-powered fraud investigation."
)
