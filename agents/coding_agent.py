from llm.gemini_client import get_gemini_response

class CodingAgent:
    def __init__(self, role: str, level: str):
        self.role = role
        self.level = level

    def generate_questions(self, resume_text=None):
        if resume_text:
            prompt = (
                f"You're a technical interviewer. Based on this resume:\n\n{resume_text}\n\n"
                f"Generate 5 {self.level.lower()} level coding questions tailored to the resume "
                f"for the role of {self.role}."
                f"⚠️ Do not include explanations, context, or intro text."
                f"Format:"
                f"<question>"
                f"<question>"
                f"... and so on."
            )
        else:
            prompt = (
                f"Generate 5 {self.level.lower()} level coding interview questions for a {self.role} role."
                f"⚠️ Do not include explanations, context, or intro text."
                f"Format:"
                f"<question>"
                f"<question>"
                f"... and so on."
            )
        return get_gemini_response(prompt)
