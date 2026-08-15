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

    new_device = st.checkbox(
        "Transaction from a new device"
    )

    suspicious_location = st.checkbox(
        "Transaction from a suspicious location"
    )

st.divider()

if st.button(
    "🚨 Investigate Transaction",
    use_container_width=True
):

    risk_score = 0
    risk_reasons = []

    # Large transaction risk
    if amount >= 100000:
        risk_score += 30
        risk_reasons.append(
            "Very large transaction amount"
        )
    elif amount >= 50000:
        risk_score += 20
        risk_reasons.append(
            "High transaction amount"
        )

    # Account age risk
    if account_age < 30:
        risk_score += 20
        risk_reasons.append(
            "Very new account"
        )

    # Failed login risk
    if failed_attempts >= 5:
        risk_score += 25
        risk_reasons.append(
            "Multiple failed login attempts"
        )
    elif failed_attempts >= 3:
        risk_score += 15
        risk_reasons.append(
            "Several failed login attempts"
        )

    # New device risk
    if new_device:
        risk_score += 20
        risk_reasons.append(
            "Transaction made from a new device"
        )

    # Suspicious location risk
    if suspicious_location:
        risk_score += 15
        risk_reasons.append(
            "Transaction originated from a suspicious location"
        )

    # Maximum score
    risk_score = min(risk_score, 100)

    # Risk level
    if risk_score >= 70:
        risk_level = "🔴 HIGH RISK"
        recommendation = (
            "Block or hold the transaction and conduct "
            "a manual investigation."
        )
    elif risk_score >= 40:
        risk_level = "🟠 MEDIUM RISK"
        recommendation = (
            "Investigate this transaction further "
            "before approving it."
        )
    else:
        risk_level = "🟢 LOW RISK"
        recommendation = (
            "Transaction currently appears relatively "
            "low risk, but continue monitoring."
        )

    st.header("📊 Investigation Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

    with col2:
        st.metric(
            "Risk Level",
            risk_level
        )

    st.subheader("🚩 Risk Signals")

    if risk_reasons:
        for reason in risk_reasons:
            st.warning(reason)
    else:
        st.success(
            "No major risk signals detected."
        )

    st.subheader("📋 Investigation Summary")

    investigation_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    st.write(
        f"""
**Transaction ID:** {transaction_id or "Not provided"}

**Amount:** KES {amount:,.2f}

**Location:** {location or "Not provided"}

**Account age:** {account_age} days

**Failed login attempts:** {failed_attempts}

**New device:** {"Yes" if new_device else "No"}

**Suspicious location:** {"Yes" if suspicious_location else "No"}

**Investigation time:** {investigation_time}

**Recommendation:** {recommendation}
"""
    )

    # Downloadable investigation report
    report = f"""
DATAGUARD INVESTIGATOR
Fraud Investigation Report
================================

Transaction ID: {transaction_id or "Not provided"}
Amount: KES {amount:,.2f}
Location: {location or "Not provided"}

Account Age: {account_age} days
Failed Login Attempts: {failed_attempts}
New Device: {"Yes" if new_device else "No"}
Suspicious Location: {"Yes" if suspicious_location else "No"}

Risk Score: {risk_score}/100
Risk Level: {risk_level}

Risk Signals:
"""

    if risk_reasons:
        for reason in risk_reasons:
            report += f"- {reason}\n"
    else:
        report += "- No major risk signals detected.\n"

    report += f"""
Recommendation:
{recommendation}

Investigation Time:
{investigation_time}

================================
DataGuard Investigator
"""

    st.download_button(
        label="📥 Download Investigation Report",
        data=report,
        file_name=f"{transaction_id or 'transaction'}_report.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()

st.caption(
    "DataGuard Investigator — Prototype for AI-powered fraud investigation."
    )
