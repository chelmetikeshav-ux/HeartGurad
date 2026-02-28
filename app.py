import streamlit as st
import numpy as np
import pickle
import sqlite3
import hashlib
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="HeartGuard AI", layout="wide")

# -------------------------
# LOAD MODEL
# -------------------------
@st.cache_resource
def load_model():
    with open("heart_model.pkl", "rb") as file:
        return pickle.load(file)

model_data = load_model()
model = model_data["model"]
train_accuracy = model_data["train_accuracy"]
test_accuracy = model_data["test_accuracy"]

# -------------------------
# DATABASE SETUP
# -------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    username TEXT,
    result TEXT
)
""")

conn.commit()

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

def register_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

# -------------------------
# SESSION STATE INIT
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# -------------------------
# TITLE
# -------------------------
st.title("❤️ HeartGuard AI")
st.caption("Secure ML-Based Heart Disease Prediction Platform")

st.markdown("---")

# -------------------------
# SIDEBAR AUTH
# -------------------------
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if menu == "Register":
    st.sidebar.subheader("Create Account")
    new_user = st.sidebar.text_input("Username")
    new_password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Register"):
        if register_user(new_user, new_password):
            st.sidebar.success("Account Created Successfully ✅")
        else:
            st.sidebar.error("Username Already Exists ❌")

elif menu == "Login":
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.admin = True if username == "admin" else False
            st.sidebar.success("Login Successful ✅")
        else:
            st.sidebar.error("Invalid Credentials ❌")

# -------------------------
# MAIN APP (PROTECTED)
# -------------------------
if st.session_state.logged_in:

    st.success(f"Welcome, {st.session_state.username} 👋")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.admin = False
        st.experimental_rerun()

    # -------------------------
    # MODEL PERFORMANCE
    # -------------------------
    st.markdown("## 📊 Model Performance")

    col1, col2 = st.columns(2)
    col1.metric("Training Accuracy", f"{round(train_accuracy*100,2)}%")
    col2.metric("Testing Accuracy", f"{round(test_accuracy*100,2)}%")

    st.markdown("---")

    # -------------------------
    # INPUT FORM
    # -------------------------
    st.markdown("## 🩺 Enter Patient Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 1, 120)
        sex = st.selectbox("Sex (0 = Female, 1 = Male)", [0, 1])
        cp = st.number_input("Chest Pain Type (0-3)", 0, 3)
        trestbps = st.number_input("Resting Blood Pressure")
        chol = st.number_input("Cholesterol")
        fbs = st.selectbox("Fasting Blood Sugar >120", [0, 1])

    with col2:
        restecg = st.number_input("Resting ECG (0-2)", 0, 2)
        thalach = st.number_input("Max Heart Rate Achieved")
        exang = st.selectbox("Exercise Induced Angina", [0, 1])
        oldpeak = st.number_input("ST Depression")
        slope = st.number_input("Slope (0-2)", 0, 2)
        ca = st.number_input("Major Vessels (0-3)", 0, 3)
        thal = st.number_input("Thal (1-3)", 1, 3)

    st.markdown("---")

    # -------------------------
    # PREDICTION
    # -------------------------
    if st.button("Predict Heart Disease"):

        input_data = np.array([[age, sex, cp, trestbps, chol, fbs,
                                restecg, thalach, exang, oldpeak,
                                slope, ca, thal]])

        prediction = model.predict(input_data)

        if prediction[0] == 1:
            result = "High Risk"
            st.error("⚠️ High Risk of Heart Disease")
        else:
            result = "Low Risk"
            st.success("✅ Low Risk of Heart Disease")

        c.execute("INSERT INTO predictions VALUES (?, ?)",
                  (st.session_state.username, result))
        conn.commit()

    # -------------------------
    # USER HISTORY
    # -------------------------
    st.markdown("## 📁 Your Prediction History")

    c.execute("SELECT result FROM predictions WHERE username=?",
              (st.session_state.username,))
    records = c.fetchall()

    if records:
        df = pd.DataFrame(records, columns=["Result"])
        st.dataframe(df)

        counts = df["Result"].value_counts()

        st.markdown("### 📈 Prediction Distribution")
        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax)
        st.pyplot(fig)
    else:
        st.info("No predictions yet.")

    # -------------------------
    # ADMIN PANEL
    # -------------------------
    if st.session_state.admin:

        st.markdown("## 🛠 Admin Dashboard")

        st.subheader("👥 Registered Users")
        c.execute("SELECT username FROM users")
        users = c.fetchall()
        st.write([user[0] for user in users])

        st.subheader("📊 All Predictions")
        c.execute("SELECT username, result FROM predictions")
        all_predictions = c.fetchall()

        if all_predictions:
            admin_df = pd.DataFrame(all_predictions, columns=["Username", "Result"])
            st.dataframe(admin_df)

            counts = admin_df["Result"].value_counts()
            fig, ax = plt.subplots()
            counts.plot(kind="bar", ax=ax)
            st.pyplot(fig)
