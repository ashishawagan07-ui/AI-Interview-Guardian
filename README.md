# 🤖 AI Interview Guardian

**AI Interview Guardian** is an AI-powered mock interview platform designed to help candidates practice technical interviews and improve their interview performance.

The application uses **Streamlit** for the web interface and **Ollama (Llama 3.2:3B)** for local AI-based answer evaluation. It provides interview questions based on role, difficulty, topic, and skills, then evaluates the candidate's answers and provides personalized feedback.

---

## 🚀 Features

- 🎯 Role-based mock interviews
- 📚 100,000+ interview question dataset
- 🧠 AI-powered answer evaluation
- 🤖 Local LLM using Ollama
- ⏱️ 120-second interview timer
- 📊 Interview score and performance analysis
- 💡 Personalized strengths and improvement suggestions
- 👤 User registration and login
- 📜 Interview history
- 🔐 User-specific data management
- 📈 Performance statistics
- 🎨 Professional Streamlit dashboard
- 🛠️ Creator/Admin dashboard

---

## 🧑‍💻 Supported Interview Areas

The platform can be configured for different interview domains, including:

- Data Analyst
- Python
- SQL
- Machine Learning
- Data Science
- Excel
- Power BI
- Technical & HR Interview Questions

---

## 🏗️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Web application |
| Ollama | Local AI/LLM |
| Llama 3.2:3B | Answer evaluation |
| Pandas | Data processing |
| NumPy | Numerical operations |
| JSON | User & interview history storage |

---

## ⚙️ How It Works

```text
User Login
     ↓
Select Interview Role
     ↓
Select Topic / Difficulty
     ↓
AI Generates Interview Question
     ↓
User Submits Answer
     ↓
Ollama AI Evaluates Answer
     ↓
Score + Feedback
     ↓
Interview History & Performance
```

---

## 📂 Project Structure

```text
AI-Interview-Guardian/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── data.csv
│
├── assets/
│   └── screenshots/
│
└── models/
    └── README.md
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ashishawagan07-ui/AI-Interview-Guardian.git
```

### 2. Open the Project

```bash
cd AI-Interview-Guardian
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Setup Ollama

Install Ollama and download the required model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before starting the application.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📊 AI Evaluation

The AI evaluates interview answers based on factors such as:

- Technical correctness
- Relevance
- Completeness
- Communication quality
- Understanding of the concept

It then provides:

- Overall Score
- Strengths
- Areas for Improvement
- AI Feedback

---

## 🔒 Security & Privacy

User-specific files such as login credentials and interview history should not be committed to GitHub.

Add the following files to `.gitignore`:

```text
users.json
interview_history.json
.env
__pycache__/
venv/
```

---

## 🎯 Project Objective

The main objective of this project is to create an interactive AI-powered interview practice platform that helps candidates:

- Practice technical interviews
- Improve answer quality
- Identify knowledge gaps
- Receive instant AI feedback
- Track interview performance

---

## 🔮 Future Improvements

- Voice-based interviews
- Speech-to-text answers
- Resume-based interview questions
- Advanced performance analytics
- Multiple AI model support
- Real-time interview difficulty adjustment
- Cloud database integration
- Deployment on Streamlit Cloud

---

## 👨‍💻 Author

**Ashish Awagan**

**B.Sc. Computer Science | Data Analyst | Data Science**

GitHub: `ashishawagan07-ui`

---

## ⭐ If You Like This Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
