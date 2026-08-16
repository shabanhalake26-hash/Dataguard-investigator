# 🛡️ DataGuard Investigator

## AI-Powered Fraud Detection and Investigation

DataGuard Investigator is an AI-powered fraud investigation prototype designed to help identify suspicious financial transactions, explain risk signals, and support faster investigation decisions.

## 🚨 What It Does

DataGuard analyzes transaction information and calculates a risk score from 0–100.

It considers signals such as:

- 💰 Transaction amount
- 👤 Account age
- 🔐 Failed login attempts
- 📱 New device activity
- 📍 Transaction location

The system then classifies the transaction as:

- 🟢 **Low Risk**
- 🟠 **Medium Risk**
- 🔴 **High Risk**

## 🤖 AI Investigation

DataGuard uses Google's Gemini AI to generate an investigation explanation.

The AI explains:

1. Why the transaction received its risk score.
2. Which risk signals are most concerning.
3. What an investigator should check next.

The AI is designed to support investigators rather than automatically declare that fraud has occurred.

## 📊 Risk Scoring

The prototype combines multiple transaction signals to produce a risk score from **0 to 100**.

Higher scores indicate that a transaction requires more investigation.

## 🔐 Security

The Gemini API key is stored using Streamlit Secrets rather than being exposed directly in the application code.

## 🚀 How to Use

1. Enter the transaction details.
2. Click **Investigate Transaction**.
3. Review the risk score and risk level.
4. Review the detected risk signals.
5. Read the AI-generated investigation explanation.
6. Use the recommendations to guide further investigation.

## 🎯 Project Goal

The goal of DataGuard Investigator is to demonstrate how AI can assist fraud investigators by combining rule-based risk detection with AI-generated explanations.

## ⚠️ Disclaimer

DataGuard Investigator is a prototype for demonstration and research purposes. Its results should support human investigation and should not be treated as definitive proof of fraud.

---

**DataGuard Investigator — Turning suspicious transactions into actionable investigation insights.**
