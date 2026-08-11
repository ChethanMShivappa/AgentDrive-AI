class RiskEngine:

    def __init__(self):
        """
        Initialize Risk Engine.
        """
        pass

    def assess_risk(self, scene):

        score = 0

        # -------------------------
        # Traffic Score
        # -------------------------

        traffic = scene["traffic_level"]

        if traffic == "Light":
            score += 1

        elif traffic == "Moderate":
            score += 2

        elif traffic == "Heavy":
            score += 3

        # -------------------------
        # Pedestrian Score
        # -------------------------

        pedestrian = scene["pedestrian_risk"]

        if pedestrian == "Low":
            score += 1

        elif pedestrian == "Medium":
            score += 2

        elif pedestrian == "High":
            score += 3

        # -------------------------
        # Cyclist Score
        # -------------------------

        if scene["cyclist_present"]:
            score += 2

        # -------------------------
        # Risk Level
        # -------------------------

        if score >= 7:

            risk = "High"

        elif score >= 4:

            risk = "Medium"

        else:

            risk = "Low"

        return {

            "risk_score": score,

            "risk_level": risk

        }