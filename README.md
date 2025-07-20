
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
- **HTML + CSS + JS** (frontend)
- **Bootstrap** (UI components)

## 🔐 Setup

1. **Clone the repo:**
   ```
   git clone https://github.com/your-username/interview-bot-gemini.git
   cd interview-bot-gemini
   ```

2. **Create and activate virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Add your API keys to a `.env` file:**
   ```
   GEMINI_API_KEY=your_google_generative_ai_key
   ```

5. **Run the app:**
   ```
   python app.py
   ```

## 📁 Folder Structure

```
interview-bot-gemini/
│
├── templates/         # HTML templates
├── static/            # CSS/JS/images
├── app.py             # Main Flask backend
├── .env               # Environment variables (not pushed to GitHub)
├── .gitignore
└── README.md
```

## 📄 License

This project is for educational use only. **Customize and extend it as needed!**
```