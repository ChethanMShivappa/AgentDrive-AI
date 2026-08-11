class DecisionEngine:

    def __init__(self):

        self.previous_risk = None

    def should_call_llm(self, risk):

        current_risk = risk["risk_level"]

        if self.previous_risk is None:

            self.previous_risk = current_risk

            return True

        if current_risk != self.previous_risk:

            self.previous_risk = current_risk

            return True

        return False