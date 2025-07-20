# agents/job_role_agent.py

import sys
import os

# Add root path so "from acp.message_format" works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# agents/job_role_agent.py

from acp.message_format import create_message
from llm.gemini_client import should_ask_questions

class JobRoleAgent:
    def __init__(self, role: str, level: str):
        self.role = role
        self.level = level

    def analyze_role(self):
        messages = []
        decisions = should_ask_questions(self.role)

        if decisions["coding"]:
            messages.append(create_message(
                sender="JobRoleAgent",
                receiver="CodingAgent",
                intent="GenerateQuestions",
                content={"role": self.role, "level": self.level}
            ))
        else:
            messages.append({
                "receiver": "CodingAgent",
                "content": ["No coding questions are needed for this role."]
            })

        if decisions["hr"]:
            messages.append(create_message(
                sender="JobRoleAgent",
                receiver="HRAgent",
                intent="GenerateQuestions",
                content={"role": self.role}
            ))
        else:
            messages.append({
                "receiver": "HRAgent",
                "content": ["No HR questions are needed for this role."]
            })

        return messages
