"""
app.py
------
This is the MAIN Flask application (the "controller" of the project,
similar to a @RestController class in Spring Boot).

WHAT IS FLASK?
Flask is a small Python web framework. It listens for web requests
(like a browser submitting a form) and decides what Python code
should run in response, then sends back an HTML page.

WHAT IS A "ROUTE"?
A route connects a URL (web address) to a Python function.
  In Spring Boot you might write:   @GetMapping("/history")
  In Flask you write:               @app.route("/history")

GET vs POST:
  GET  -> used to REQUEST/view a page (e.g. opening the home page).
          Data is not submitted, nothing changes on the server.
  POST -> used to SEND data to the server (e.g. submitting the email
          form). We use POST for /check because the user is sending
          sender/subject/body data that will be analyzed and stored.

HOW DATA FLOWS:
  1. Browser (HTML form) sends sender/subject/body via POST to /check
  2. Flask's check() function receives that data with request.form
  3. Python analyzes the email (rules + ML model)
  4. Flask saves the result in SQLite
  5. Flask renders result.html and sends it back to the browser
"""

import pickle
import re
import sqlite3
from datetime import datetime
from html import escape  # used to safely display user text (security)

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_NAME = "database.db"
MAX_INPUT_LENGTH = 5000  # protects against extremely long input


# ==================================================================
# DATABASE SETUP
# ==================================================================
def init_db():
    """
    Creates the email_scans table if it does not already exist.
    We use Python's built-in sqlite3 module (no SQLAlchemy needed).
    SQLite stores the whole database in a single file: database.db
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            result TEXT,
            risk_score INTEGER,
            scanned_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_scan(sender, subject, result, risk_score):
    """Inserts one scan record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO email_scans (sender, subject, result, risk_score, scanned_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (sender, subject, result, risk_score, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()


def get_all_scans():
    """Fetches every past scan, most recent first, for the History page."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT sender, subject, result, risk_score, scanned_at "
                    "FROM email_scans ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ==================================================================
# LOAD THE TRAINED ML MODEL (done once, when the app starts)
# ==================================================================
def load_ml_files():
    """
    Loads model.pkl and vectorizer.pkl that train_model.py created.
    If they are missing, we tell the user clearly instead of crashing
    with a confusing error.
    """
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        return None, None


ml_model, ml_vectorizer = load_ml_files()


# ==================================================================
# SIMPLE RULE-BASED INDICATORS (extra hints, NOT the main decision)
# ==================================================================
# These are just warning flags shown to the user for transparency.
# The ACTUAL classification decision comes from the ML model above.
SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "password", "otp", "account blocked",
    "click here", "congratulations", "prize", "winner", "bank"
]

URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)


def get_security_indicators(text):
    """
    Scans the email text for simple warning words and links.
    Returns a list of short, human-readable indicator strings.
    This does NOT decide the final result - it only adds context.
    """
    text_lower = text.lower()
    indicators = []

    if "urgent" in text_lower or "immediately" in text_lower:
        indicators.append("Urgent language detected")

    if "password" in text_lower or "otp" in text_lower:
        indicators.append("Password/OTP request detected")

    if URL_PATTERN.search(text):
        indicators.append("Suspicious link detected")

    if "prize" in text_lower or "winner" in text_lower or "congratulations" in text_lower:
        indicators.append("Prize/reward bait language detected")

    if "account blocked" in text_lower or "account will be blocked" in text_lower or "suspended" in text_lower:
        indicators.append("Account threat language detected")

    matched_keywords = [word for word in SUSPICIOUS_KEYWORDS if word in text_lower]

    return indicators, matched_keywords


# ==================================================================
# RISK SCORE CALCULATION
# ==================================================================
# HOW THE SCORE IS CALCULATED (explained simply):
# 1. The ML model outputs a PROBABILITY for each class
#    (e.g. legitimate: 0.05, suspicious: 0.10, phishing: 0.85).
# 2. We take the probability of the predicted class and convert it
#    to a 0-100 scale. That becomes the main part of the risk score.
# 3. If the predicted class itself is "legitimate", we INVERT the
#    scale so a confident "legitimate" prediction gives a LOW risk
#    score (safe), while a confident "phishing" prediction gives a
#    HIGH risk score (dangerous).
# 4. The score is then mapped into three bands:
#      0-30   -> LOW RISK    -> Likely Legitimate
#      31-70  -> MEDIUM RISK -> Suspicious
#      71-100 -> HIGH RISK   -> Likely Phishing
def calculate_risk_score(predicted_label, class_probabilities, class_names):
    """
    predicted_label: the label the model chose (e.g. 'phishing')
    class_probabilities: array of probabilities, one per class
    class_names: the model's list of class names, in the same order
                 as class_probabilities (model.classes_)
    """
    prob_map = dict(zip(class_names, class_probabilities))

    # Combine "suspicious" and "phishing" probability as the danger side,
    # since both mean the email is NOT purely legitimate.
    danger_probability = prob_map.get("phishing", 0) + (prob_map.get("suspicious", 0) * 0.5)

    risk_score = round(danger_probability * 100)
    risk_score = max(0, min(100, risk_score))  # keep it between 0 and 100

    if risk_score <= 30:
        risk_level = "LOW RISK"
        final_result = "Likely Legitimate"
    elif risk_score <= 70:
        risk_level = "MEDIUM RISK"
        final_result = "Suspicious"
    else:
        risk_level = "HIGH RISK"
        final_result = "Likely Phishing"

    return risk_score, risk_level, final_result


# ==================================================================
# BASIC EMAIL FORMAT CHECK (very simple, beginner-friendly)
# ==================================================================
def is_valid_email_format(email_text):
    """A light check - not a full RFC validator, just catches obvious mistakes."""
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email_text.strip()) is not None


# ==================================================================
# ROUTES
# ==================================================================
@app.route("/")
def home():
    """GET / -> shows the input form (index.html)."""
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    """
    POST /check -> receives form data, runs analysis, shows result.html

    request.form is how Flask reads data submitted by an HTML <form>.
    It works like reading parameters from an HttpServletRequest in Java.
    """
    sender = request.form.get("sender", "").strip()
    subject = request.form.get("subject", "").strip()
    body = request.form.get("body", "").strip()

    # ---------------- ERROR HANDLING ----------------
    errors = []
    if not sender:
        errors.append("Sender email cannot be empty.")
    elif not is_valid_email_format(sender):
        errors.append("Sender email format looks invalid (expected something like name@example.com).")

    if not body:
        errors.append("Email body cannot be empty.")

    if len(body) > MAX_INPUT_LENGTH or len(subject) > MAX_INPUT_LENGTH:
        errors.append(f"Input is too long. Please keep it under {MAX_INPUT_LENGTH} characters.")

    if ml_model is None or ml_vectorizer is None:
        errors.append("The ML model files were not found. Please run 'python train_model.py' first.")

    if errors:
        return render_template("index.html", errors=errors,
                                sender=sender, subject=subject, body=body)

    # ---------------- COMBINE TEXT FOR THE MODEL ----------------
    # We never execute email content - it is only ever treated as plain
    # text data for analysis, never as code or an active link.
    combined_text = subject + " " + body

    try:
        # Convert the email into the same TF-IDF number format the
        # model was trained on, then ask the model to predict.
        text_vector = ml_vectorizer.transform([combined_text])
        predicted_label = ml_model.predict(text_vector)[0]
        probabilities = ml_model.predict_proba(text_vector)[0]
        class_names = ml_model.classes_

        risk_score, risk_level, final_result = calculate_risk_score(
            predicted_label, probabilities, class_names
        )

        indicators, matched_keywords = get_security_indicators(combined_text)

    except Exception as e:
        return render_template("index.html",
                                errors=[f"Something went wrong analyzing this email: {e}"],
                                sender=sender, subject=subject, body=body)

    # ---------------- SAVE TO DATABASE ----------------
    try:
        save_scan(sender, subject, final_result, risk_score)
    except sqlite3.Error as e:
        errors.append(f"Warning: result could not be saved to history ({e}).")

    # ---------------- DISPLAY RESULT ----------------
    # escape() prevents any HTML/JS inside the email from being rendered
    # by the browser - the email content is always treated as plain text.
    return render_template(
        "result.html",
        sender=escape(sender),
        subject=escape(subject) if subject else "(no subject)",
        final_result=final_result,
        risk_score=risk_score,
        risk_level=risk_level,
        indicators=indicators,
        matched_keywords=matched_keywords,
        ml_predicted_label=predicted_label,
    )


@app.route("/history")
def history():
    """GET /history -> shows every past scan from the database."""
    try:
        scans = get_all_scans()
        db_error = None
    except sqlite3.Error as e:
        scans = []
        db_error = str(e)
    return render_template("history.html", scans=scans, db_error=db_error)


if __name__ == "__main__":
    init_db()
    print("Database ready. Starting Flask server ...")
    print("Open your browser at: http://127.0.0.1:5000")
    app.run(debug=True)
