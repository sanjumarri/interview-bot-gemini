# acp/router.py

import os
from datetime import datetime

from agents.coding_agent import CodingAgent
from agents.hr_agent import HRAgent

def send_message(message, resume_text=None):
    log_message(message)

    receiver = message.get("receiver")
    intent = message.get("intent", "")

    if receiver == "CodingAgent" and intent == "GenerateQuestions":
        agent = CodingAgent(message["content"]["role"], message["content"]["level"])
        return agent.generate_questions(resume_text)

    elif receiver == "HRAgent" and intent == "GenerateQuestions":
        agent = HRAgent(message["content"]["role"])
        return agent.generate_questions(resume_text)

    # fallback for messages like "No questions needed"
    return message.get("content", ["No response generated."])

def log_message(message):
    log_path = os.path.join("logs", "communication_log.txt")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as log_file:
        if all(k in message for k in ["sender", "receiver", "intent"]):
            log_line = (
                f"{datetime.now()} | {message['sender']} -> {message['receiver']} | "
                f"Intent: {message['intent']}\n"
            )
        else:
            log_line = (
                f"{datetime.now()} | System -> {message.get('receiver', 'Unknown')} | "
                f"Content: {str(message.get('content'))}\n"
            )
        log_file.write(log_line)
