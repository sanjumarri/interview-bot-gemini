```markdown
# AI Interview Assistant 🤖

This is an **AI-powered Interview Assistant** built with the **Gemini API (Google Generative AI)** that simulates technical interview scenarios and evaluates your responses.

## 🚀 Features

- Simulates real-time technical interviews  
- Generates follow-up questions  
- Evaluates your answers using LLM  
- Supports voice and text input  
- Feedback scoring system

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **Gemini API** (Google Generative AI)
- **Streamlit** (for UI)
- **HTML + CSS + JS** (frontend assets)
- **Bootstrap** (UI components)

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
   - For Flask backend (if used):  
     ```
     python app.py
     ```
   - For Streamlit UI frontend:  
     ```
     streamlit run ui/streamlit_app.py
     ```

## 📁 Folder Structure

```
interview-bot-gemini/
│
├── acp/                 # Access control & processing
│   ├── message_format.py
│   └── router.py
│
├── agents/              # Interview AI agents
│   ├── coding_agent.py
│   ├── hr_agents.py
│   ├── job_role_agent.py
│   └── scoring_agent.py
│
├── llm/                 # Language Model integration
│   └── gemini_client.py
│
├── ui/                  # User Interface (Streamlit frontend)
│   └── streamlit_app.py
│
├── static/              # CSS/JS/images (if used)
├── templates/           # HTML templates (if Flask is used)
├── app.py               # Main Flask backend (if used)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not pushed to GitHub)
├── .gitignore
└── README.md
```

## 📄 License

This project is for educational use only. **Customize and extend it as needed!**
```
