# AI-First CRM: HCP Interaction Module

A modern, intelligent CRM module designed for pharmaceutical sales representatives to log and manage interactions with Healthcare Professionals (HCPs). This application leverages **LangGraph**, **Groq (Llama 3)**, and **MySQL** to provide a seamless, AI-driven experience.

![Dashboard Preview](dashboard.png)

## 🚀 Key Features

-   **AI Assistant (LangGraph Powered)**: A sidebar assistant that processes natural language to auto-fill complex CRM forms.
-   **Smart Merge Logic**: Intelligently appends new discussion topics and outcomes to existing records without overwriting, maintaining full session history.
-   **Medical Entity Extraction**: Automatically identifies and categorizes drug names, symptoms, and specialties from conversation text.
-   **MySQL Integration**: Persistent storage using SQLAlchemy for robust data management.
-   **Professional UI**: Built with React, Redux Toolkit, and the Inter font for a premium, high-performance user experience.

---

## 🛠️ Tech Stack

-   **Frontend**: React (Vite), Redux Toolkit, Vanilla CSS, Lucide Icons.
-   **Backend**: FastAPI (Python), SQLAlchemy, Pydantic.
-   **AI/LLM**: LangChain, LangGraph, Groq (Llama-3.3-70b).
-   **Database**: MySQL.

---

## 📦 Setup & Installation

### Prerequisites
-   Python 3.10+
-   Node.js 18+
-   MySQL Server 8.0+
-   Groq API Key (Get it from [console.groq.com](https://console.groq.com))

### 1. Backend Setup
1.  Navigate to the `backend` folder:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure your `.env` file:
    ```env
    DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/assesment
    GROQ_API_KEY=YOUR_GROQ_API_KEY
    ```
5.  Run the server:
    ```bash
    python -m uvicorn main:app --reload
    ```

### 2. Frontend Setup
1.  Navigate to the `frontend_app` folder:
    ```bash
    cd frontend_app
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```

---

## 🤖 Sample Prompt Sequences
Try these in the AI Assistant to see the "Smart Merge" in action:
1.  *"Met Dr. Smith today for a meeting. He's positive about OncoBoost."*
2.  *"We also discussed patient fatigue and I shared the dosage guide."*
3.  *"Schedule a follow-up for next Tuesday and summarize our talk."*

---

## 📄 License
This project is for assessment purposes. All rights reserved.
