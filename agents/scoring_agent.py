# agents/scoring_agent.py

class ScoringAgent:
    def __init__(self, answers: dict):
        self.answers = answers

    def evaluate(self):
        # Simulated scores
        return {
            "Communication": 8,
            "Technical Knowledge": 7,
            "Confidence": 9
        }
