# llm/gemini_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-70b-8192"  # You can try: llama3-70b-8192, gemma-7b-it, etc.

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt: str) -> str:
    try:
        response = requests.post(
            ENDPOINT,
            headers=HEADERS,
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an expert career advisor and technical interviewer."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1024
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[Groq Error] {e}"

# ---------------------- Replace Gemini Functions ----------------------

def get_gemini_response(prompt: str) -> list:
    text = call_groq(prompt)
    return [line.strip() for line in text.split("\n") if line.strip()]

def should_ask_questions(role: str) -> dict:
    prompt = (
        f"Analyze the job role '{role}' and decide whether coding and/or HR interview questions are needed.\n"
        f"Reply only in this format:\n"
        f"coding: yes/no\nhr: yes/no"
    )
    text = call_groq(prompt).lower()

    try:
        return {
            "coding": "yes" in text.split("coding:")[1].split("\n")[0],
            "hr": "yes" in text.split("hr:")[1]
        }
    except Exception as e:
        print("[Groq parsing error]", e)
        return {"coding": True, "hr": True}  # fallback

def get_feedback_on_answer(question: str, answer: str) -> dict:
    prompt = (
        f"You are an interview coach.\n"
        f"Evaluate the following answer to an interview question:\n\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n\n"
        f"1. Rate it out of 10 (as 'Score: <number>')\n"
        f"2. Give one short improvement suggestion (as 'Suggestion: <your tip>')"
    )

    try:
        response = call_groq(prompt)
        lines = response.splitlines()
        score_line = next((l for l in lines if "score" in l.lower()), "Score: 7")
        suggestion_line = next((l for l in lines if "suggestion" in l.lower()), "Suggestion: Looks good.")

        score = int(''.join(filter(str.isdigit, score_line)))
        suggestion = suggestion_line.split(":", 1)[-1].strip()
        return {"score": score, "suggestion": suggestion}
    except Exception as e:
        return {"score": 7, "suggestion": f"[Error] {e}"}
    
def get_followup_question(question: str, answer: str) -> str:
    prompt = (
        f"You are an interview coach.\n"
        f"Based on the question:\n'{question}'\n"
        f"and the candidate's answer:\n'{answer}'\n\n"
        f"Generate one smart follow-up question the interviewer might ask.\n"
        f"Keep it short and on topic. No explanation, just the question."
    )
    return call_groq(prompt)
