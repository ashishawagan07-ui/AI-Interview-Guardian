import streamlit as st
import pandas as pd
from pathlib import Path
import time
import ollama
import hashlib
import re
import json
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Interview Guardian",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =========================
   COLORFUL LIGHT THEME
   ========================= */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.13), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(236,72,153,0.12), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(6,182,212,0.12), transparent 32%),
        linear-gradient(135deg, #f8faff 0%, #fff7fb 48%, #f2fbff 100%);
    color: #1e293b;
}

/* Main headings */
.main-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #4f46e5, #db2777, #0891b2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #475569;
    font-size: 17px;
    margin-bottom: 25px;
}

/* Login / Register cards */
.login-card {
    max-width: 500px;
    margin: 50px auto;
    padding: 35px;
    background: rgba(255,255,255,0.94);
    border-radius: 25px;
    box-shadow: 0 14px 40px rgba(79,70,229,0.18);
    border: 1px solid #ddd6fe;
}

.auth-title {
    text-align: center;
    color: #4f46e5;
    font-size: 32px;
    font-weight: 800;
}

.auth-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}

/* Dashboard cards */
.dashboard-card {
    padding: 22px;
    border-radius: 20px;
    color: #ffffff !important;
    min-height: 130px;
    box-shadow: 0 10px 28px rgba(79,70,229,0.16);
    border: 1px solid rgba(255,255,255,0.35);
}

.card-purple {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.card-pink {
    background: linear-gradient(135deg, #ec4899, #f43f5e);
}

.card-blue {
    background: linear-gradient(135deg, #0284c7, #06b6d4);
}

.card-green {
    background: linear-gradient(135deg, #059669, #10b981);
}

.card-orange {
    background: linear-gradient(135deg, #ea580c, #f59e0b);
}

.card-red {
    background: linear-gradient(135deg, #e11d48, #f97316);
}

.card-number {
    font-size: 35px;
    font-weight: 800;
}

.card-label {
    font-size: 15px;
    opacity: 0.96;
}

/* Question / evaluation / history */
.question-box {
    background: rgba(255,255,255,0.96);
    padding: 28px;
    border-radius: 22px;
    border-left: 7px solid #6366f1;
    box-shadow: 0 10px 30px rgba(99,102,241,0.14);
    margin-bottom: 20px;
}

.question-text {
    font-size: 23px;
    font-weight: 700;
    color: #1e293b;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 13px;
    font-weight: 600;
}

.badge-purple {
    background: #ede9fe;
    color: #6d28d9;
}

.badge-blue {
    background: #e0f2fe;
    color: #0369a1;
}

.badge-green {
    background: #dcfce7;
    color: #15803d;
}

.badge-pink {
    background: #fce7f3;
    color: #be185d;
}

.evaluation-box {
    background: rgba(255,255,255,0.96);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(14,165,233,0.14);
    border: 1px solid #bae6fd;
}

.history-box {
    background: rgba(255,255,255,0.96);
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 10px;
    border-left: 5px solid #06b6d4;
    box-shadow: 0 6px 18px rgba(6,182,212,0.12);
}

/* Colorful sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #312e81 0%, #4f46e5 42%, #7c3aed 72%, #db2777 100%);
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Inputs - FIXES BLACK INPUTS */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label {
    color: #475569 !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #ffffff !important;
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    border: 2px solid #c7d2fe !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.10) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.14) !important;
}

/* BaseWeb input containers - FIXES BLACK BACKGROUND */
div[data-baseweb="input"],
div[data-baseweb="textarea"],
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border-radius: 14px !important;
    border-color: #c7d2fe !important;
    color: #1e293b !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    background: #ffffff !important;
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
}

/* Dropdown text */
div[data-baseweb="select"] * {
    color: #1e293b !important;
}

/* ALL BUTTONS - no black */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed, #db2777) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 750 !important;
    padding: 10px 20px !important;
    box-shadow: 0 7px 18px rgba(99,102,241,0.22) !important;
    transition: all 0.2s ease-in-out !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(219,39,119,0.25) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    color: #475569 !important;
    font-weight: 700 !important;
}

.stTabs [aria-selected="true"] {
    color: #4f46e5 !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.92);
    border: 1px solid #ddd6fe;
    border-radius: 16px;
    padding: 14px;
    box-shadow: 0 6px 18px rgba(99,102,241,0.10);
}

div[data-testid="stMetricValue"] {
    color: #4f46e5 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 40px;
    padding: 20px;
}

/* Divider */
hr {
    border-color: #ddd6fe !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / "data" / "data.csv"

USERS_FILE = BASE_DIR / "users.json"

HISTORY_FILE = BASE_DIR / "interview_history.csv"


# =========================================================
# USER FUNCTIONS
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def load_users():

    if USERS_FILE.exists():

        try:

            with open(USERS_FILE, "r", encoding="utf-8") as f:

                return json.load(f)

        except:

            return {}

    return {}


def save_users(users):

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            users,
            f,
            indent=4
        )


def register_user(username, password):

    users = load_users()

    if username in users:

        return False, "Username already exists."

    users[username] = {
        "password": hash_password(password),
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    save_users(users)

    return True, "Registration successful."


def login_user(username, password):

    users = load_users()

    if username not in users:

        return False

    return users[username]["password"] == hash_password(password)


# =========================================================
# HISTORY FUNCTIONS
# =========================================================

def load_history():

    if HISTORY_FILE.exists():

        try:

            return pd.read_csv(HISTORY_FILE)

        except:

            pass

    return pd.DataFrame(
        columns=[
            "username",
            "date",
            "question",
            "role",
            "topic",
            "overall",
            "technical",
            "relevance",
            "communication"
        ]
    )


def save_history(
    username,
    question,
    role,
    topic,
    overall,
    technical,
    relevance,
    communication
):

    history = load_history()

    new_row = pd.DataFrame([{

        "username": username,

        "date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "question": question,

        "role": role,

        "topic": topic,

        "overall": overall,

        "technical": technical,

        "relevance": relevance,

        "communication": communication

    }])

    history = pd.concat(
        [history, new_row],
        ignore_index=True
    )

    history.to_csv(
        HISTORY_FILE,
        index=False
    )


# =========================================================
# AI EVALUATION
# =========================================================

def evaluate_answer_with_ai(
    question,
    user_answer,
    sample_answer
):

    prompt = f"""

You are an expert technical interview evaluator.

Evaluate the candidate's answer.

QUESTION:
{question}

CANDIDATE ANSWER:
{user_answer}

REFERENCE ANSWER:
{sample_answer}

Give scores from 0 to 100.

Return EXACTLY in this format:

Overall Score: XX
Technical Score: XX
Relevance Score: XX
Communication Score: XX

Strengths:
- point 1
- point 2

Improvements:
- point 1
- point 2

Feedback:
short practical feedback for a fresher.

Be fair and concise.
"""

    response = ollama.chat(

        model="llama3.2:3b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        options={
            "temperature": 0.2
        }
    )

    return response["message"]["content"]


# =========================================================
# SCORE PARSER
# =========================================================

def extract_score(text, keyword):

    pattern = rf"{keyword}\s*:\s*(\d+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        return int(match.group(1))

    return 0


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_dataset():

    return pd.read_csv(DATA_FILE)


try:

    df = load_dataset()

except Exception as e:

    st.error(
        f"Dataset load error: {e}"
    )

    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "username" not in st.session_state:

    st.session_state.username = ""


if "page" not in st.session_state:

    st.session_state.page = "Dashboard"


if "current_question" not in st.session_state:

    st.session_state.current_question = (
        df.sample(1).iloc[0]
    )


if "last_score" not in st.session_state:

    st.session_state.last_score = None


if "timer_running" not in st.session_state:

    st.session_state.timer_running = False


if "time_left" not in st.session_state:

    st.session_state.time_left = 120


if "saved_questions" not in st.session_state:

    st.session_state.saved_questions = []


if "answer_version" not in st.session_state:

    st.session_state.answer_version = 0


# =========================================================
# LOGIN / REGISTER
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">🤖 AI Interview Guardian</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-Powered Interview Preparation Platform</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with tab1:

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="auth-title">Welcome Back 👋</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="auth-subtitle">Login to continue your interview journey</div>',
            unsafe_allow_html=True
        )

        username = st.text_input(
            "👤 Username",
            key="login_username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if login_user(
                username,
                password
            ):

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.page = "Dashboard"

                st.success(
                    "Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # REGISTER
    # -----------------------------------------------------

    with tab2:

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="auth-title">Create Account 🚀</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="auth-subtitle">Start your AI interview preparation</div>',
            unsafe_allow_html=True
        )

        new_username = st.text_input(
            "👤 Create Username",
            key="register_username"
        )

        new_password = st.text_input(
            "🔑 Create Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "🔐 Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "✨ Create Account",
            use_container_width=True
        ):

            if not new_username or not new_password:

                st.warning(
                    "Please fill all fields."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 4:

                st.warning(
                    "Password should contain at least 4 characters."
                )

            else:

                success, message = register_user(
                    new_username,
                    new_password
                )

                if success:

                    st.success(
                        message
                    )

                    st.info(
                        "Now go to Login and sign in."
                    )

                else:

                    st.error(
                        message
                    )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="footer">AI Interview Guardian • Local AI • Ollama</div>',
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "# 🤖 AI Guardian"
    )

    st.markdown(
        f"### 👋 Hello, {st.session_state.username}"
    )

    st.divider()

    navigation_pages = [
        "🏠 Dashboard",
        "🎯 Interview",
        "📊 Performance",
        "⭐ Saved Questions",
        "🕘 History"
    ]

    # Keep the sidebar selection synchronized with every dashboard button.
    if st.session_state.page not in navigation_pages:
        st.session_state.page = "🏠 Dashboard"

    page = st.radio(
        "Navigation",
        navigation_pages,
        index=navigation_pages.index(st.session_state.page)
    )

    st.session_state.page = page

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="sidebar_logout"
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "🏠 Dashboard"
        st.session_state.timer_running = False
        st.rerun()


# =========================================================
# USER HISTORY
# =========================================================

history = load_history()

user_history = history[
    history["username"]
    == st.session_state.username
]


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">AI Interview Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Track your interview preparation and improve your answers with AI</div>',
        unsafe_allow_html=True
    )

    total_attempts = len(user_history)

    if total_attempts > 0:

        avg_score = round(
            user_history["overall"].mean(),
            1
        )

        best_score = int(
            user_history["overall"].max()
        )

    else:

        avg_score = 0

        best_score = 0

    total_questions = len(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="dashboard-card card-purple">
            <div class="card-number">{total_questions:,}</div>
            <div class="card-label">Interview Questions</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="dashboard-card card-pink">
            <div class="card-number">{total_attempts}</div>
            <div class="card-label">Attempts</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="dashboard-card card-blue">
            <div class="card-number">{avg_score}</div>
            <div class="card-label">Average Score</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="dashboard-card card-green">
            <div class="card-number">{best_score}</div>
            <div class="card-label">Best Score</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🚀 Start Interview")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🎯 Start Interview",
            use_container_width=True
        ):

            st.session_state.page = "🎯 Interview"
            st.session_state.timer_running = False
            st.rerun()

    with col2:

        if st.button(
            "📊 View Performance",
            use_container_width=True
        ):

            st.session_state.page = "📊 Performance"
            st.rerun()

    with col3:

        if st.button(
            "⭐ Saved Questions",
            use_container_width=True
        ):

            st.session_state.page = "⭐ Saved Questions"
            st.rerun()

    st.markdown("## 📚 Dataset Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        f"{len(df):,}"
    )

    c2.metric(
        "Columns",
        len(df.columns)
    )

    c3.metric(
        "Missing Values",
        int(df.isna().sum().sum())
    )

    c4.metric(
        "Duplicates",
        int(df.duplicated().sum())
    )


# =========================================================
# INTERVIEW
# =========================================================

elif page == "🎯 Interview":

    st.markdown(
        '<div class="main-title">🎯 AI Mock Interview</div>',
        unsafe_allow_html=True
    )

    # FILTERS

    st.markdown("### 🎛️ Interview Filters")

    c1, c2, c3 = st.columns(3)

    with c1:

        role = st.selectbox(
            "Target Role",
            ["All"] +
            sorted(
                df["target_role"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with c2:

        difficulty = st.selectbox(
            "Difficulty",
            ["All"] +
            sorted(
                df["difficulty"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with c3:

        topic = st.selectbox(
            "Topic",
            ["All"] +
            sorted(
                df["topic"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    filtered = df.copy()

    if role != "All":

        filtered = filtered[
            filtered["target_role"] == role
        ]

    if difficulty != "All":

        filtered = filtered[
            filtered["difficulty"] == difficulty
        ]

    if topic != "All":

        filtered = filtered[
            filtered["topic"] == topic
        ]

    if len(filtered) == 0:

        st.warning(
            "No questions found for these filters."
        )

    else:

        if st.button(
            "🎲 Generate New Question",
            use_container_width=True
        ):

            st.session_state.current_question = (
                filtered.sample(1).iloc[0]
            )

            st.session_state.last_score = None
            st.session_state.timer_running = False
            st.session_state.time_left = 120
            st.session_state.answer_version += 1
            st.rerun()

    q = st.session_state.current_question

    # QUESTION

    st.markdown(
        f"""
        <div class="question-box">

        <div>
        <span class="badge badge-purple">
        🎯 {q['target_role']}
        </span>

        <span class="badge badge-blue">
        📚 {q['topic']}
        </span>

        <span class="badge badge-green">
        ⚡ {q['difficulty']}
        </span>

        <span class="badge badge-pink">
        💻 {q['primary_skill']}
        </span>
        </div>

        <br>

        <div class="question-text">
        {q['question']}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # SAVE

    if st.button(
        "⭐ Save Question",
        use_container_width=True,
        key="save_question_button"
    ):

        question_text = str(q["question"])

        if question_text not in st.session_state.saved_questions:
            st.session_state.saved_questions.append({
                "question": question_text,
                "role": str(q["target_role"]),
                "topic": str(q["topic"]),
                "difficulty": str(q["difficulty"])
            })
            st.success("⭐ Question saved successfully!")
        else:
            st.info("This question is already saved.")

    # TIMER

    st.markdown("### ⏱️ Interview Timer")

    timer_col1, timer_col2 = st.columns(2)

    with timer_col1:

        st.metric(
            "Time Remaining",
            f"{st.session_state.time_left} sec"
        )

    with timer_col2:

        if not st.session_state.timer_running:

            if st.button(
                "▶️ Start Timer"
            ):

                st.session_state.timer_running = True

                st.rerun()

        else:

            if st.button(
                "⏸️ Stop Timer"
            ):

                st.session_state.timer_running = False

                st.rerun()

    if st.session_state.timer_running:

        if st.session_state.time_left > 0:

            time.sleep(1)

            st.session_state.time_left -= 1

            st.rerun()

        else:

            st.session_state.timer_running = False

            st.warning(
                "⏰ Time is over!"
            )

    # ANSWER

    st.markdown("### ✍️ Your Answer")

    answer = st.text_area(
        "Write your interview answer here...",
        height=220,
        key=f"answer_box_{st.session_state.answer_version}"
    )

    if st.button(
        "🤖 AI Submit & Evaluate",
        use_container_width=True
    ):

        if not answer.strip():

            st.warning(
                "Please write an answer first."
            )

        else:

            with st.spinner(
                "🤖 Ollama AI is evaluating your answer..."
            ):

                try:

                    result = evaluate_answer_with_ai(

                        q["question"],

                        answer,

                        q["sample_answer"]

                    )

                    st.session_state.last_score = result

                    overall = extract_score(
                        result,
                        "Overall Score"
                    )

                    technical = extract_score(
                        result,
                        "Technical Score"
                    )

                    relevance = extract_score(
                        result,
                        "Relevance Score"
                    )

                    communication = extract_score(
                        result,
                        "Communication Score"
                    )

                    save_history(

                        st.session_state.username,

                        q["question"],

                        q["target_role"],

                        q["topic"],

                        overall,

                        technical,

                        relevance,

                        communication

                    )

                    st.success(
                        "🎉 AI Evaluation Completed!"
                    )

                except Exception as e:

                    st.error(
                        f"AI Error: {e}"
                    )

    # RESULTS

    if st.session_state.last_score:

        result = st.session_state.last_score

        overall = extract_score(
            result,
            "Overall Score"
        )

        technical = extract_score(
            result,
            "Technical Score"
        )

        relevance = extract_score(
            result,
            "Relevance Score"
        )

        communication = extract_score(
            result,
            "Communication Score"
        )

        st.markdown("---")

        st.markdown(
            "## 📊 AI Evaluation"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.markdown(
                f"""
                <div class="dashboard-card card-purple">
                <div class="card-number">{overall}/100</div>
                <div class="card-label">Overall Score</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="dashboard-card card-blue">
                <div class="card-number">{technical}/100</div>
                <div class="card-label">Technical</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="dashboard-card card-pink">
                <div class="card-number">{relevance}/100</div>
                <div class="card-label">Relevance</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:

            st.markdown(
                f"""
                <div class="dashboard-card card-green">
                <div class="card-number">{communication}/100</div>
                <div class="card-label">Communication</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 🤖 Detailed AI Feedback")

        st.markdown(
            f"""
            <div class="evaluation-box">

            {result.replace(chr(10), "<br>")}

            </div>
            """,
            unsafe_allow_html=True
        )

    # NEXT

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "➡️ Next Question",
            use_container_width=True
        ):

            st.session_state.current_question = (
                filtered.sample(1).iloc[0]
            )

            st.session_state.last_score = None
            st.session_state.timer_running = False
            st.session_state.time_left = 120
            st.session_state.answer_version += 1
            st.rerun()

    with col2:

        if st.button(
            "🎲 Random Question",
            use_container_width=True
        ):

            st.session_state.current_question = (
                df.sample(1).iloc[0]
            )

            st.session_state.last_score = None
            st.session_state.timer_running = False
            st.session_state.time_left = 120
            st.session_state.answer_version += 1
            st.rerun()


# =========================================================
# PERFORMANCE
# =========================================================

elif page == "📊 Performance":

    st.markdown(
        '<div class="main-title">📊 Performance Dashboard</div>',
        unsafe_allow_html=True
    )

    if user_history.empty:

        st.info(
            "Complete at least one interview to see performance."
        )

    else:

        avg = user_history[
            "overall"
        ].mean()

        technical_avg = user_history[
            "technical"
        ].mean()

        relevance_avg = user_history[
            "relevance"
        ].mean()

        communication_avg = user_history[
            "communication"
        ].mean()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Overall",
            f"{avg:.1f}"
        )

        c2.metric(
            "Technical",
            f"{technical_avg:.1f}"
        )

        c3.metric(
            "Relevance",
            f"{relevance_avg:.1f}"
        )

        c4.metric(
            "Communication",
            f"{communication_avg:.1f}"
        )

        st.markdown("### 📈 Score Comparison")

        chart_data = user_history[
            [
                "technical",
                "relevance",
                "communication",
                "overall"
            ]
        ]

        st.bar_chart(
            chart_data
        )

        st.markdown(
            "### 📋 Attempts"
        )

        st.dataframe(
            user_history,
            use_container_width=True
        )

        csv = user_history.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download Performance CSV",
            csv,
            file_name="interview_performance.csv",
            mime="text/csv"
        )


# =========================================================
# SAVED QUESTIONS
# =========================================================

elif page == "⭐ Saved Questions":

    st.markdown(
        '<div class="main-title">⭐ Saved Questions</div>',
        unsafe_allow_html=True
    )

    saved = st.session_state.saved_questions

    if not saved:

        st.info("No saved questions yet. Save a question from the Interview page.")

        if st.button("🎯 Go to Interview", use_container_width=True, key="saved_go_interview"):
            st.session_state.page = "🎯 Interview"
            st.rerun()

    else:

        st.markdown(f"### ⭐ {len(saved)} Saved Question(s)")

        for i, item in enumerate(saved, start=1):

            st.markdown(
                f"""
                <div class="history-box">
                    <b>#{i} {item['question']}</b><br><br>
                    🎯 {item['role']} &nbsp; | &nbsp; 📚 {item['topic']} &nbsp; | &nbsp; ⚡ {item['difficulty']}
                </div>
                """,
                unsafe_allow_html=True
            )

        c1, c2 = st.columns(2)

        with c1:
            if st.button("🎯 Practice Saved Question", use_container_width=True, key="practice_saved"):
                st.session_state.page = "🎯 Interview"
                st.rerun()

        with c2:
            if st.button("🗑️ Clear Saved Questions", use_container_width=True, key="clear_saved"):
                st.session_state.saved_questions = []
                st.success("All saved questions cleared.")
                st.rerun()


# HISTORY
# =========================================================

elif page == "🕘 History":

    st.markdown(
        '<div class="main-title">🕘 Interview History</div>',
        unsafe_allow_html=True
    )

    if user_history.empty:

        st.info(
            "No interview history available."
        )

    else:

        for _, row in user_history.iloc[::-1].iterrows():

            st.markdown(
                f"""
                <div class="history-box">

                <b>📅 {row['date']}</b>

                <br><br>

                <b>❓ Question:</b>
                {row['question']}

                <br><br>

                🎯 Overall:
                <b>{row['overall']}/100</b>

                &nbsp;&nbsp;

                💻 Technical:
                <b>{row['technical']}/100</b>

                &nbsp;&nbsp;

                📌 Relevance:
                <b>{row['relevance']}/100</b>

                &nbsp;&nbsp;

                🗣️ Communication:
                <b>{row['communication']}/100</b>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

    🤖 <b>AI Interview Guardian</b>

    <br>

    Built with Python • Streamlit • Pandas • Ollama

    <br>

    Local AI Interview Preparation Platform

    </div>
    """,
    unsafe_allow_html=True
)