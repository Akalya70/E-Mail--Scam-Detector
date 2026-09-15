# AI-Based Email Scam & Phishing Detection System — Full Guide

This guide explains everything: what each file does, how the app works,
how to run it, and how to talk about it in an interview. Written for
someone who knows **Java / Spring Boot** and is new to Python.

---

## 1. Project Structure & File Purposes

```
email-scam-detector/
│
├── app.py              ← Flask web server ("Controller" — like a @RestController)
├── train_model.py      ← One-time script that TEACHES the ML model (run before app.py)
├── model.pkl           ← The trained ML "brain", saved to disk (like a serialized object)
├── vectorizer.pkl      ← Remembers how to turn words into numbers, saved to disk
├── dataset.csv         ← 75 example emails used to train the model
├── database.db         ← SQLite file, created automatically when app.py first runs
├── requirements.txt    ← List of Python packages needed (like pom.xml dependencies)
│
├── templates/           ← HTML pages (Flask calls these "templates")
│   ├── index.html        (the input form / home page)
│   ├── result.html        (shows the prediction)
│   └── history.html       (shows past scans from the database)
│
└── static/
    └── style.css        ← Shared CSS styling for all pages
```

| File | Purpose |
|---|---|
| `app.py` | Starts the website, defines routes, loads the ML model, runs analysis, talks to the database |
| `train_model.py` | Reads `dataset.csv`, trains the ML model, prints real accuracy numbers, saves `model.pkl` and `vectorizer.pkl` |
| `model.pkl` | The trained Logistic Regression model, saved so it doesn't need retraining every time the site runs |
| `vectorizer.pkl` | The TF-IDF "translator" that turns new email text into the same number format the model understands |
| `dataset.csv` | Training data: two columns, `email_text` and `label` (legitimate / suspicious / phishing) |
| `database.db` | Stores every scan you've ever run, so `/history` can show it later |
| `templates/*.html` | What the user actually sees in the browser |
| `static/style.css` | Makes the pages look clean without Bootstrap/Tailwind |

**Java comparison:** `model.pkl`/`vectorizer.pkl` are like a serialized `.ser` object — you build it once with a training program, then "deserialize" (load) it in your main app instead of rebuilding it every time.

---

## 2. How a Request Flows Through the App

```
Browser form (index.html)
   │  POST /check  (sender, subject, body)
   ▼
Flask route: check() in app.py
   │  request.form.get(...)     ← like request.getParameter() in a Servlet
   ▼
Combine subject + body → TF-IDF vectorizer → numbers
   ▼
model.predict() + model.predict_proba()
   ▼
calculate_risk_score() → 0–100 score + risk level
   ▼
get_security_indicators() → keyword/URL warning flags (extra info only)
   ▼
save_scan() → INSERT INTO email_scans (SQLite)
   ▼
render_template("result.html", ...) → HTML sent back to browser
```

**GET vs POST, explained simply:**
- `GET /` and `GET /history` just *display* a page — nothing is being submitted, so GET is correct (like fetching a page, no side effects).
- `POST /check` *sends data* that causes something to happen (analysis + a database write), so POST is correct — the same rule you'd apply choosing `@PostMapping` over `@GetMapping` in Spring Boot.

---

## 3. The Machine Learning Part, Explained Simply

**Why TF-IDF?**
Computers only understand numbers, not words. TF-IDF converts each email into a row of numbers where words that are common in one email but rare overall (like "OTP" or "prize") get a high score, and filler words ("the", "is") get a low score. It's a simple, fast, well-understood technique — perfect for a beginner project, no deep learning needed.

**Why Logistic Regression?**
It's one of the simplest ML algorithms for classification (sorting things into categories), trains in a fraction of a second on small data, and — importantly — it gives you `predict_proba()`, a probability for each class, which is exactly what we need to build the 0–100 risk score. It's the "Hello World" of classification algorithms.

**Why Flask (not FastAPI/Django)?**
Flask has the smallest amount of "magic" — a handful of decorators (`@app.route`) and functions. That maps closely to concepts you already know (routes ≈ `@RequestMapping`), without an ORM, dependency injection container, or project-generator to learn first.

**Why SQLite (not a real database server)?**
SQLite is just a single file (`database.db`) — no server to install or configure. Python's built-in `sqlite3` module talks to it directly with plain SQL strings, no ORM layer (no SQLAlchemy) — you can see exactly what SQL is running, which is the clearest way to learn.

---

## 4. How the Risk Score Is Calculated (exact formula)

1. The model outputs a probability for each class, e.g. `legitimate: 0.05, suspicious: 0.10, phishing: 0.85`.
2. We compute `danger = P(phishing) + 0.5 × P(suspicious)` — phishing counts fully, suspicious counts as "half risky."
3. `risk_score = round(danger × 100)`, clamped to 0–100.
4. Bands:
   - **0–30 → LOW RISK → "Likely Legitimate"**
   - **31–70 → MEDIUM RISK → "Suspicious"**
   - **71–100 → HIGH RISK → "Likely Phishing"**

The security indicators (urgent language, password/OTP request, links, prize bait) are **only shown as extra context** — they never override the ML model's decision.

---

## 5. Installation (Windows CMD, step by step)

```cmd
:: 1. Move into the project folder
cd email-scam-detector

:: 2. Create a virtual environment (an isolated copy of Python for just this project,
::    similar to how a Maven/Gradle project keeps its own dependency versions)
python -m venv venv

:: 3. Activate it (your terminal prompt will show "(venv)" once active)
venv\Scripts\activate

:: 4. Install the three required packages
pip install flask pandas scikit-learn

:: (requirements.txt is already provided — alternative one-liner:)
pip install -r requirements.txt
```

## 6. Running the Project

```cmd
:: Step 1 — Train the model (only needed once, or whenever dataset.csv changes)
python train_model.py

:: Step 2 — Start the website
python app.py
```

You'll see `Open your browser at: http://127.0.0.1:5000` in the terminal.
Open that address in any browser (Chrome/Edge/Firefox). To stop the server, press `Ctrl+C` in the terminal.

---

## 7. Demonstration Test Emails

These are for **demonstration only** — a real system's accuracy depends entirely on the size and quality of its training dataset (75 rows here is small and made for learning, not production use).

| Expect | Email |
|---|---|
| Likely Legitimate | "Hello, your interview is scheduled for Monday at 10 AM. Please join the meeting using the company meeting link." |
| Likely Phishing | "URGENT! Your bank account will be blocked today. Click this link immediately and enter your password and OTP." |
| Suspicious | "Your account requires verification. Please review your account information." |

When tested against the actual trained model, these produced: **Likely Phishing (82%)**, **Likely Legitimate (25%)**, and **Suspicious (52%)** respectively.

---

## 8. Interview Preparation

### 1. Project Introduction
A beginner-friendly web app that takes an email's sender, subject, and body, and predicts whether it is legitimate, suspicious, or phishing — using a trained machine learning model rather than only hard-coded keyword rules.

### 2. Problem Statement
Phishing emails cause data theft and financial fraud. Manually checking every email for scam signs is slow and error-prone, and simple keyword filters are easy for attackers to bypass by rewording their messages.

### 3. Existing System
Most spam filters historically relied on fixed rule lists (blocked words, blacklisted senders) or basic pattern matching.

### 4. Problems with Existing System
Rule lists must be updated manually for every new scam wording, cannot generalize to phrasing they haven't seen, and produce many false positives/negatives — this is essentially the same "hard-coded if/else" limitation you'd hit writing this in plain Java without any learning component.

### 5. Proposed System
Use a Logistic Regression model trained on labeled email examples (via TF-IDF features) so the system generalizes to *new, unseen* wording, combined with simple rule-based indicators for transparency.

### 6. How Machine Learning Works in This Project
`train_model.py` shows the model many labeled emails; it statistically learns which words correlate with which label. `app.py` then feeds new emails through the same transformation and asks the trained model to predict a label and probability.

### 7. Why TF-IDF Is Used
It converts text into meaningful numeric features, weighting distinctive words (like "OTP") higher than common filler words, without needing complex embeddings or deep learning.

### 8. Why Logistic Regression Is Used
It's simple, fast to train on small datasets, easy to explain, and natively outputs class probabilities — needed for the risk score.

### 9. Why Flask Is Used
Minimal, unopinionated, and maps cleanly onto concepts from Spring Boot (routes, request objects, template rendering) without an ORM or heavy configuration.

### 10. How SQLite Is Used
`sqlite3` (Python's built-in module) creates/reads a single-file database (`database.db`) with one table, `email_scans`, storing every analysis for the History page — no separate database server or ORM required.

### 11. Project Workflow
User fills the form → Flask receives POST data → text is vectorized with TF-IDF → Logistic Regression predicts a label and probabilities → risk score is calculated → rule-based indicators are added → result is saved to SQLite → result page is rendered.

### 12. Challenges Faced
Keeping the dataset balanced across three classes; deciding how to combine ML probabilities into a single, understandable risk score; making sure the app fails gracefully (missing model file, empty input) instead of crashing.

### 13. Future Improvements
Train on a much larger, real-world labeled dataset; add more ML models to compare (e.g., Naive Bayes, Random Forest) and pick the best; add user accounts; add a browser extension; retrain automatically as new labeled data comes in.

### 14. 20 Technical Interview Questions with Simple Answers

1. **What is Flask?** A lightweight Python web framework for building websites by mapping URLs to Python functions.
2. **What is a route?** A rule connecting a URL path to a function that runs when that URL is requested — similar to `@RequestMapping` in Spring Boot.
3. **Difference between GET and POST?** GET requests/views data with no side effects; POST sends data to the server to create or change something.
4. **What is TF-IDF?** A way to turn text into numbers by scoring words higher when they're frequent in one document but rare across all documents.
5. **What is Logistic Regression?** A classification algorithm that predicts a category (not a continuous number, despite the name) using a probability function.
6. **Why split data into train/test sets?** To fairly evaluate whether the model generalizes to new data, instead of just memorizing what it already saw.
7. **What does `model.fit()` do?** It's where the model actually learns — adjusting its internal parameters based on the training data and labels.
8. **What is `predict_proba()`?** Returns the probability the model assigns to each possible class, instead of just the single most likely label.
9. **What is pickling?** Saving a Python object (like a trained model) to a file so it can be reloaded later without recomputation — similar to Java object serialization.
10. **What is a vectorizer, and why save it separately from the model?** It converts raw text into numeric features; it must be saved because new emails need to be converted using the exact same vocabulary the model was trained on.
11. **What is SQLite, and why use it here?** A lightweight, file-based database requiring no separate server — ideal for small/beginner projects.
12. **Why not use SQLAlchemy?** To keep the project simple and let a beginner see the raw SQL being executed via Python's built-in `sqlite3` module.
13. **What is overfitting?** When a model performs very well on training data but poorly on new data because it memorized specifics instead of learning general patterns.
14. **How is the risk score calculated here?** From the model's predicted probability for phishing/suspicious classes, scaled to 0–100 and mapped into LOW/MEDIUM/HIGH bands.
15. **Why combine ML with simple rule-based indicators?** ML provides the core prediction; rules add transparent, human-readable context (e.g., "urgent language detected") without controlling the final decision.
16. **How is user input kept safe when displayed?** By escaping it (`html.escape`) before rendering, so any HTML/script in an email can't run in the browser.
17. **What does `render_template()` do?** Combines an HTML file with Python variables (via Jinja2 templating) to produce the final page sent to the browser.
18. **What happens if `model.pkl` is missing?** `app.py` catches the `FileNotFoundError` and shows a clear error message instead of crashing.
19. **What are precision, recall, and F1-score?** Precision = accuracy of positive predictions; recall = how many actual positives were found; F1 = their harmonic mean, balancing both.
20. **Could this be used in production as-is?** No — it's trained on a small demonstration dataset; a production system needs thousands of real, diverse labeled emails and stronger validation, but the architecture (Flask + TF-IDF + Logistic Regression + SQLite) is a valid, extensible foundation.

---

## 9. Key Python-vs-Java Concepts Quick Reference

| Concept | Java | Python (this project) |
|---|---|---|
| Route/endpoint | `@GetMapping("/x")` | `@app.route("/x")` |
| Reading request data | `request.getParameter("x")` | `request.form.get("x")` |
| Object serialization | `.ser` file, `ObjectOutputStream` | `pickle.dump(obj, file)` |
| Dependency list | `pom.xml` | `requirements.txt` |
| Virtual environment | separate Maven/Gradle project | `venv` (isolated package copies) |
| Template rendering | Thymeleaf/JSP | Jinja2 (`render_template`) |
| DB access | JDBC | `sqlite3` module |
