"""
train_model.py
----------------
This script TEACHES the computer how to recognize phishing emails.

Think of it like this (Java comparison):
- In Java, you write "if/else" rules by hand.
- In Machine Learning, we instead show the computer MANY examples
  (dataset.csv) and let it learn the pattern itself.

This script does 9 simple steps. Read the comments above each step.
Run it with:  python train_model.py
"""

import pandas as pd                                   # pandas = tool for reading tables (like an Excel file in code)
from sklearn.model_selection import train_test_split   # splits data into "practice" and "test" sets
from sklearn.feature_extraction.text import TfidfVectorizer  # turns words into numbers
from sklearn.linear_model import LogisticRegression    # the ML algorithm that learns to classify
from sklearn.metrics import accuracy_score, classification_report
import pickle                                          # pickle = saves a Python object to a file (like Java serialization)


# ----------------------------------------------------------------
# STEP 1: Read the dataset
# ----------------------------------------------------------------
# dataset.csv has two columns: "email_text" and "label"
# This is similar to reading rows from a database table in Java,
# except pandas loads the whole CSV into a table called a "DataFrame".
print("Step 1: Reading dataset.csv ...")
data = pd.read_csv("dataset.csv")
print(f"  Loaded {len(data)} emails.")
print(f"  Label counts:\n{data['label'].value_counts()}\n")


# ----------------------------------------------------------------
# STEP 2: Separate email text (input) and labels (correct answer)
# ----------------------------------------------------------------
# X = the questions (email text)
# y = the answers (legitimate / suspicious / phishing)
print("Step 2: Separating text (X) and labels (y) ...")
X = data["email_text"]
y = data["label"]


# ----------------------------------------------------------------
# STEP 3: Split into training data and testing data
# ----------------------------------------------------------------
# We do NOT test the model on the same emails it studied from,
# otherwise it would just "memorize the answers" instead of learning.
# This is like keeping some exam questions hidden from a student
# during revision, so you can fairly test what they actually learned.
print("Step 3: Splitting into training (80%) and testing (20%) sets ...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% of emails are kept aside for testing
    random_state=42,    # makes the split repeatable every time we run this
    stratify=y          # keeps a fair mix of each label in both sets
)
print(f"  Training emails: {len(X_train)}, Testing emails: {len(X_test)}\n")


# ----------------------------------------------------------------
# STEP 4: Convert email text into numbers using TF-IDF
# ----------------------------------------------------------------
# Computers cannot understand words directly, only numbers.
# TF-IDF (Term Frequency - Inverse Document Frequency) turns each
# email into a row of numbers, where:
#   - words that appear often in ONE email but rarely in others
#     get a HIGH score (they are more meaningful, e.g. "OTP", "prize")
#   - very common words (like "the", "is") get a LOW score
# This is similar to converting a Java object into a numeric array
# before you can do math on it.
print("Step 4: Converting email text into TF-IDF number features ...")
vectorizer = TfidfVectorizer(
    lowercase=True,      # treat "Urgent" and "urgent" as the same word
    stop_words="english" # ignore common filler words like "the", "is", "a"
)
X_train_vectors = vectorizer.fit_transform(X_train)  # learn vocabulary AND convert training emails
X_test_vectors = vectorizer.transform(X_test)         # convert testing emails using the SAME vocabulary
print(f"  Vocabulary size learned: {len(vectorizer.vocabulary_)} unique words\n")


# ----------------------------------------------------------------
# STEP 5: Train the Logistic Regression model
# ----------------------------------------------------------------
# Logistic Regression is a simple, well-known ML algorithm used for
# classification (sorting things into categories). Despite the name
# "regression", it is used here to predict a CATEGORY (legitimate /
# suspicious / phishing), not a number.
# .fit() is where the actual "learning" happens: the model looks at
# X_train_vectors (the numbers) and y_train (the correct labels) and
# adjusts itself to find patterns that connect the two.
print("Step 5: Training the Logistic Regression model ...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vectors, y_train)
print("  Training complete.\n")


# ----------------------------------------------------------------
# STEP 6: Test the model on unseen emails
# ----------------------------------------------------------------
print("Step 6: Testing the model on emails it has NEVER seen ...")
predictions = model.predict(X_test_vectors)


# ----------------------------------------------------------------
# STEP 7: Print accuracy, precision, recall and F1-score
# ----------------------------------------------------------------
# These numbers are printed FROM THE ACTUAL TEST RESULTS, not made up:
#   - Accuracy  : % of emails the model classified correctly overall
#   - Precision : when the model says "phishing", how often is it right?
#   - Recall    : out of all real phishing emails, how many did it catch?
#   - F1-score  : a balance between precision and recall
print("Step 7: Evaluation results")
print("-" * 50)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.2f} ({accuracy * 100:.1f}%)\n")
print("Detailed report (precision, recall, F1-score per class):")
print(classification_report(y_test, predictions, zero_division=0))
print("-" * 50)
print("NOTE: This dataset is small and made for LEARNING purposes.")
print("A real production system needs thousands of real, labeled emails.\n")


# ----------------------------------------------------------------
# STEP 8: Save the trained model as model.pkl
# ----------------------------------------------------------------
# "Saving" the model means writing the learned patterns to a file so
# that app.py can load it later WITHOUT retraining every time.
# This is conceptually like saving a trained employee's knowledge to
# a file instead of re-training a new employee every single day.
print("Step 8: Saving trained model to model.pkl ...")
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)


# ----------------------------------------------------------------
# STEP 9: Save the TF-IDF vectorizer as vectorizer.pkl
# ----------------------------------------------------------------
# We must save the vectorizer too! It remembers the exact vocabulary
# learned in Step 4. Without it, app.py would not know how to turn a
# NEW email's words into the same number format the model expects.
print("Step 9: Saving TF-IDF vectorizer to vectorizer.pkl ...")
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nAll done! You can now run: python app.py")
