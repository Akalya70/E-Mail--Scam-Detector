# 🛡️📧 E-Mail Scam Detector

<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=00AEEF&center=true&vCenter=true&width=800&lines=AI-Powered+Email+Security;Detect+Phishing+%7C+Detect+Scams+%7C+Stay+Safe;Machine+Learning+%2B+Flask+%2B+Python" alt="Typing Animation"/>

</p>

<p align="center">
  <strong>🔍 Analyze • 🤖 Predict • 🛡️ Protect</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-Web%20App-black?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge&logo=sqlite&logoColor=black"/>
</p>

---

## 🚨 What is this?

**E-Mail Scam Detector** is a beginner-friendly AI-powered web application that analyzes email content and identifies potentially dangerous emails.

Instead of simply saying **"Real" or "Fake"**, the system provides three levels of prediction:

```text
🟢 LIKELY LEGITIMATE
        ↓
🟡 SUSPICIOUS
        ↓
🔴 LIKELY PHISHING
```

The application uses **TF-IDF + Logistic Regression** to learn patterns from email text and predict the possibility of phishing or scam content.

---

## ✨ Why this project?

Imagine receiving an email:

> ⚠️ "URGENT! Your bank account will be blocked. Verify your password and OTP immediately!"

Would you click the link?

**Don't click first. Analyze first. 🔍**

This project is designed to provide users with an additional layer of awareness before they interact with suspicious emails.

---

# 🧠 How the AI Works

<p align="center">

```text
        📧 EMAIL
           │
           ▼
   ┌─────────────────┐
   │ Text Processing │
   └────────┬────────┘
            │
            ▼
      🔢 TF-IDF
   Text → Numbers
            │
            ▼
   🤖 Logistic Regression
            │
            ▼
     📊 Prediction
            │
       ┌────┼────┐
       ▼    ▼    ▼
      🟢   🟡   🔴
    Legit  Suspicious  Phishing
            │
            ▼
      ⚠️ Risk Score
        0 ──── 100
```

</p>

---

# 🔥 Main Features

| Feature            | Description                            |
| ------------------ | -------------------------------------- |
| 📧 Email Analysis  | Analyze sender, subject and email body |
| 🤖 AI Prediction   | Machine Learning-based classification  |
| 🔍 Scam Indicators | Detect suspicious words and patterns   |
| 🔗 URL Detection   | Identify URLs in email content         |
| 📊 Risk Score      | Generate a score from 0–100            |
| 🚦 Risk Level      | Low, Medium and High risk              |
| 💾 Scan History    | Store previous scans using SQLite      |
| 🎨 Simple UI       | Clean beginner-friendly interface      |

---

# 🎯 Risk Meter

```text
0                    30                    70                   100
│---------------------│---------------------│---------------------│
🟢 LOW RISK           🟡 MEDIUM RISK       🔴 HIGH RISK
```

### 🟢 0–30

**Low Risk**

The email c
