# 🛡️📧 E-Mail Scam Detector

<p align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=00AEEF&center=true&vCenter=true&width=800&lines=AI-Powered+Email+Security;Detect+Phishing+%7C+Detect+Scams+%7C+Stay+Safe;Machine+Learning+%2B+Flask+%2B+Python" alt="Typing Animation"/>

</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge&logo=sqlite&logoColor=black"/>
</p>

## 🚨 

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

The email contains fewer suspicious indicators.

### 🟡 31–70

**Medium Risk**

The email contains some suspicious characteristics.

### 🔴 71–100

**High Risk**

The email contains multiple phishing or scam indicators.

> ⚠️ The score is an automated prediction, not a guarantee that an email is safe or malicious.

---

# 🤖 Machine Learning

The project uses two main Machine Learning components.

### 1️⃣ TF-IDF

**TF-IDF = Term Frequency-Inverse Document Frequency**

It converts email text into numerical features.

Example:

```text
"Verify your password immediately"
```

TF-IDF identifies the importance of words such as:

```text
verify
password
immediately
```

and represents the text numerically.

---

### 2️⃣ Logistic Regression

The numerical TF-IDF features are given to the **Logistic Regression** classifier.

The model learns patterns from labeled email examples and predicts the category of a new email.

```text
Training Data
      ↓
TF-IDF
      ↓
Logistic Regression
      ↓
Trained Model
      ↓
New Email
      ↓
Prediction
```

---

# 🧪 Example Detection

### 🚨 Suspicious Email

```text
Subject:
URGENT! Your account will be blocked

Message:
Your account has been temporarily blocked.
Verify your password and OTP immediately.
Click the link below to restore your account.
```

### 🔍 Detector

```text
⚠️ Urgent language detected
⚠️ Password request detected
⚠️ OTP request detected
⚠️ Account threat detected
⚠️ URL detected
```

### 🛡️ Result

```text
🔴 LIKELY PHISHING

Risk Score: 85/100
Risk Level: HIGH
```

---


# 🏗️ Project Architecture

```text
                     👤 USER
                       │
                       ▼
              🌐 Flask Web Interface
                       │
                       ▼
                📩 Email Input
                       │
              ┌────────┴────────┐
              ▼                 ▼
        🤖 ML Prediction    🔍 Rule Checks
              │                 │
              └────────┬────────┘
                       ▼
                 📊 Risk Score
                       │
                       ▼
              🚦 Final Classification
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
             🟢       🟡       🔴
           Legit   Suspicious  Phishing
                       │
                       ▼
                 💾 SQLite
                 Scan History
```

---

# 📂 Project Structure

```text
📦 E-Mail--Scam-Detector
│
├── 🐍 app.py
├── 🧠 train_model.py
├── 📊 dataset.csv
├── 🤖 model.pkl
├── 🔢 vectorizer.pkl
├── 📋 requirements.txt
├── 📖 GUIDE.md
├── 🚫 .gitignore
│
├── 📁 templates
│   ├── 🏠 index.html
│   ├── 📊 result.html
│   └── 📜 history.html
│
└── 📁 static
    └── 🎨 style.css
```
---

# 🛠️ Technology Stack

<p align="center">

🐍 **Python**
🌐 **Flask**
🤖 **Scikit-learn**
📊 **Pandas**
🔢 **TF-IDF**
🧠 **Logistic Regression**
🗄️ **SQLite**
🎨 **HTML + CSS**

</p>

---

# ⚡ Getting Started

## 1️⃣ Clone the repository

```bash
git clone https://github.com/Akalya70/E-Mail--Scam-Detector.git
```

```bash
cd E-Mail--Scam-Detector
```

---

## 2️⃣ Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 4️⃣ Train the AI model

```bash
python train_model.py
```

This creates/updates:

```text
🤖 model.pkl
🔢 vectorizer.pkl
```

---

## 5️⃣ Start the application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

---

# 🔐 Security

The application treats email content as **untrusted input**.

The system does **not**:

```text
❌ Automatically open links
❌ Execute email attachments
❌ Execute email content
❌ Store passwords
❌ Store OTPs
❌ Guarantee that an email is safe
```

Always verify suspicious messages through official channels.

---

# 📈 Future Improvements

The project can be extended with:

```text
📎 Attachment Analysis
        ↓
🌐 URL Reputation Checking
        ↓
📧 Real Email Inbox Integration
        ↓
🧠 Advanced ML Models
        ↓
📊 Analytics Dashboard
        ↓
🔔 Real-Time Alerts
        ↓
☁️ Cloud Deployment
```

---

# 🎓 What I Learned

Through this project, I learned:

* 🐍 Python fundamentals
* 🌐 Flask web development
* 🤖 Machine Learning basics
* 🔢 TF-IDF vectorization
* 🧠 Logistic Regression
* 📊 Dataset preprocessing
* 🗄️ SQLite database operations
* 🔗 Connecting ML models with a web application
* 🔐 Basic application security
* 🧪 Testing and debugging

---

# 💡 Project Objective

The main objective is to create a simple system that helps users **identify potentially dangerous emails before interacting with them**.

The project combines:

```text
Python
  +
Machine Learning
  +
Web Development
  +
Database
  =
🛡️ Email Security Application
```

---





### 🚀 Built with Python & Machine Learning

**E-Mail Scam Detector — Turning suspicious emails into actionable warnings.**

</p>
