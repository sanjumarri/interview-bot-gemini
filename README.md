
# AI Interview Assistant 🤖

This is an **AI-powered Interview Assistant** built on the **Gemini API (Google Generative AI)**, designed to simulate technical interview scenarios, generate follow-up questions, and evaluate user responses in a realistic, interactive format. The project aims to help candidates prepare for interviews by providing instant feedback and adaptive questioning, mirroring the dynamic of a real-world technical interview panel.


## 🚀 Features

- Simulates **real-time technical interviews**
- **Generates adaptive follow-up questions** based on user performance
- **Evaluates answers** using an LLM (Gemini API)
- Supports **voice** and **text input**
- Offers a **feedback scoring system** for self-assessment


## 🛠️ Tech Stack

- **Python**
- **Flask** (for the backend REST API)
- **Streamlit** (for interactive UI)
- **Gemini API** (Google Generative AI for NLP processing)
- **HTML, CSS, JS** & **Bootstrap** (for frontend enhancements)

## ⚙️ Working

The **AI Interview Assistant** operates as a modular, multi-agent system built on the ACP (Access, Control, Processing) protocol. Here’s how it works:

- **User Interaction:**  
  The user interacts with the system through the web UI (powered by Streamlit), choosing an interview mode, job role, or question type. Both text and voice inputs are supported.

- **Message Routing (ACP Protocol):**  
  All user messages are passed through the `acp` module.  
  - `message_format.py` ensures each message follows the consistent structure required for processing.
  - `router.py` directs incoming requests to the appropriate agent or module based on context, such as the type of interview or question.

- **Agent Collaboration:**  
  Specialized agents (in the `agents` folder)—including coding, HR, job-role, and scoring agents—handle different aspects of the interview:
  - **Coding Agent:** Assesses programming and technical questions.
  - **HR Agent:** Handles behavioral and soft-skill queries.
  - **Job Role Agent:** Customizes questions to specific job roles.
  - **Scoring Agent:** Analyzes user responses and provides feedback.

- **LLM Integration:**  
  The `llm/gemini_client.py` module connects with the Gemini API (Google Generative AI) to generate questions, evaluate answers, and simulate a realistic interviewer.

- **Feedback & Adaptation:**  
  After each response, the system evaluates the user's answer and offers feedback and a score. It may then generate follow-up questions or adjust the interview flow dynamically based on performance.

- **Backend Coordination:**  
  The backend, managed by Flask (if enabled), handles session state, API key management, and request authentication for the entire workflow.

- **Security & Separation:**  
  Environment variables (e.g., API keys) are stored in a `.env` file, which is never pushed to version control for security. The project structure—with clear separation of access, control, agent logic, and UI—makes it easy to extend or adapt to new interview domains.


**In summary:**  
Each user query flows through the ACP protocol for validation and routing, is processed by specialized AI agents, evaluated by the Gemini LLM, and returns structured, adaptive feedback — all orchestrated through modular Python components.


## 🔐 Setup

1. **Clone the repo:**
   ```
   git clone https://github.com/your-username/interview-bot-gemini.git
   cd interview-bot-gemini
   ```

2. **Create and activate the virtual environment:**
   ```
   python -m venv venv
   # For Linux/macOS
   source venv/bin/activate
   # For Windows
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Add your API key to a `.env` file:**
   ```
   GEMINI_API_KEY=your_google_generative_ai_key
   ```

5. **Run the app:**
   - For Flask backend:
     ```
     python app.py
     ```
   - For Streamlit UI frontend:
     ```
     streamlit run ui/streamlit_app.py
     ```

---

## 📁 Folder Structure

```
interview-bot-gemini/
│
├── acp/                 # ACP protocol: access/control/processing logic
│   ├── message_format.py
│   └── router.py
│
├── agents/              # Modular interview AI agents
│   ├── coding_agent.py
│   ├── hr_agents.py
│   ├── job_role_agent.py
│   └── scoring_agent.py
│
├── llm/                 # Language Model integration
│   └── gemini_client.py
│
├── ui/                  # Streamlit-based user interface
│   └── streamlit_app.py
│
├── static/              # CSS/JS/images (optional)
├── templates/           # HTML templates (optional, Flask-based UI)
├── app.py               # Main Flask backend (if used)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not tracked in Git)
├── .gitignore
└── README.md
```

---

## 📄 License

This project is for educational use only.
**Feel free to customize and extend it as needed to fit your technical interview simulation requirements!**
```
