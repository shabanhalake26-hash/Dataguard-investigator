import streamlit as st
from datetime import datetime
from google import genai
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)
st.set_page_config(
    page_title="DataGuard Investigator",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Session history
# -----------------------------
if "investigations" not in st.session_state:
    st.session_state.investigations = []

# -----------------------------
# Header
# -----------------------------
st.title("🛡️ DataGuard Investigator")
st.subheader("AI-powered fraud detection and investigation")

st.write(
    "Analyze suspicious transactions, identify risk signals, "
    "and generate an investigation summary."
)

st.divider()

# -----------------------------
# Dashboard
# -----------------------------
st.header("📊 Investigation Dashboard")

total = len(st.session_state.investigations)
high = sum(
    1 for x in st.session_state.investigations
    if x["risk_score"] >= 70
)
medium = sum(
    1 for x in st.session_state.investigations
    if 40 <= x["risk_score"] < 70
)
low = sum(
    1 for x in st.session_state.investigations
    if x["risk_score"] < 40
)

d1, d2, d3, d4 = st.columns(4)

with d1:
    st.metric("Total Investigations", total)

with d2:
    st.metric("🔴 High Risk", high)

with d3:
    st.metric("🟠 Medium Risk", medium)

with d4:
    st.metric("🟢 Low Risk", low)

if total > 0:
    st.bar_chart({
        "Risk Level": {
            "High Risk": high,
            "Medium Risk": medium,
            "Low Risk": low
        }
    })

st.divider()

# -----------------------------
# Transaction investigation
# -----------------------------
st.header("🔎 Transaction Investigation")

col1, col2 = st.columns(2)

with col1:
    transaction_id = st.text_input(
        "Transaction ID",
        placeholder="e.g. TXN-20001"
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
        "Suspicious transaction location"
    )

st.divider()

# -----------------------------
# Investigation engine
# -----------------------------
if st.button(
    "🚨 Investigate Transaction",
    use_container_width=True
):

    risk_score = 0
    risk_reasons = []

    # Transaction amount
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

    # Account age
    if account_age < 30:
        risk_score += 20
        risk_reasons.append(
            "Very new account"
        )

    # Failed logins
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

    # New device
    if new_device:
        risk_score += 20
        risk_reasons.append(
            "Transaction made from a new device"
        )

    # Suspicious location
    if suspicious_location:
        risk_score += 20
        risk_reasons.append(
            "Suspicious transaction location"
        )

    risk_score = min(risk_score, 100)

    # Risk level
    if risk_score >= 70:
        risk_level = "🔴 HIGH RISK"
        recommendation = (
            "Block or hold the transaction and "
            "conduct a manual investigation."
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

    investigation_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Save investigation
    investigation = {
        "transaction_id": transaction_id or "Not provided",
        "amount": amount,
        "location": location or "Not provided",
        "account_age": account_age,
        "failed_attempts": failed_attempts,
        "new_device": new_device,
        "suspicious_location": suspicious_location,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "time": investigation_time
    }

    st.session_state.investigations.append(
        investigation
    )

    # -----------------------------
    # Results
    # -----------------------------
    st.header("📊 Investigation Result")

    r1, r2 = st.columns(2)

    with r1:
        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

    with r2:
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

    # -----------------------------
    # Gemini investigation explanation
    # -----------------------------
    st.subheader("🤖 AI Investigation Explanation")

    prompt = f"""
You are a fraud investigation assistant.

Analyze this transaction:

Transaction ID: {transaction_id or "Not provided"}
Amount: KES {amount:,.2f}
Location: {location or "Not provided"}
Account age: {account_age} days
Failed login attempts: {failed_attempts}
New device: {"Yes" if new_device else "No"}
Suspicious location: {"Yes" if suspicious_location else "No"}
Risk score: {risk_score}/100
Risk level: {risk_level}

Risk signals:
{", ".join(risk_reasons) if risk_reasons else "None"}

Explain in simple language:
1. Why this transaction received this risk score.
2. Which signals are most concerning.
3. What an investigator should check next.

Do not claim that fraud has definitely occurred.
Keep the explanation concise and professional.
"""

            try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.info(response.text)

        except Exception as e:
            st.warning(
                f"AI explanation could not be generated: {e}"
            )
    

    st.subheader("📋 Investigation Summary")

    st.write(
        f"""
**Transaction ID:** {transaction_id or "Not provided"}

**Amount:** KES {amount:,.2f}

**Location:** {location or "Not provided"}

**Account age:** {account_age} days

**Failed login attempts:** {failed_attempts}

**New device:** {"Yes" if new_device else "No"}

**Suspicious location:** {"Yes" if suspicious_location else "No"}

**Risk Score:** {risk_score}/100

**Risk Level:** {risk_level}

**Recommendation:** {recommendation}

**Investigation time:** {investigation_time}
"""
    )

    # -----------------------------
    # Download report
    # -----------------------------
    report = f"""
DATAGUARD INVESTIGATOR
======================

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

======================
DataGuard Investigator
"""

    st.download_button(
        label="📥 Download Investigation Report",
        data=report,
        file_name=f"{transaction_id or 'transaction'}_report.txt",
        mime="text/plain",
        use_container_width=True
    )

# -----------------------------
# Investigation history
# -----------------------------
st.divider()

st.header("🗂️ Investigation History")

if st.session_state.investigations:

    for item in reversed(
        st.session_state.investigations
    ):
        st.write(
            f"**{item['transaction_id']}** — "
            f"KES {item['amount']:,.2f} — "
            f"{item['risk_level']} — "
            f"{item['time']}"
        )

else:
    st.info(
        "No investigations yet. "
        "Run an investigation to create history."
    )

st.divider()

st.caption(
    "DataGuard Investigator — Prototype for "
    "AI-powered fraud investigation."
    )
