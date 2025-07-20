from llm.gemini_client import get_gemini_response

class HRAgent:
    def __init__(self, role: str):
        self.role = role

    def generate_questions(self, resume_text=None):
        if resume_text:
            prompt = (
                f"You're an HR interviewer. Based on this resume:\n\n{resume_text}\n\n"
                f"Generate 5 behavioral or HR interview questions tailored to the role: {self.role}."
                f"⚠️ Do not include explanations, context, or intro text."
                f"Format:"
                f"<question>"
                f"<question>"
                f"... and so on."
                f"Only Questions."
            )
        else:
            prompt = (
                f"Generate 5 behavioral or HR interview questions tailored to the role: {self.role}."
                f"⚠️ Do not include explanations, context, or intro text."
                f"Format:"
                f"<question>"
                f"<question>"
                f"... and so on."
                f"Only Questions."
            )
        return get_gemini_response(prompt)
