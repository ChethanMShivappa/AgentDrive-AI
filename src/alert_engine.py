class AlertEngine:

    def generate_alert(self, scene, risk):

        risk_level = risk["risk_level"]

        counts = scene["object_counts"]

        # High Risk
        if risk_level == "High":

            if counts.get("person", 0) > 0:
                return "Warning. Pedestrian ahead."

            if counts.get("truck", 0) > 0:
                return "Warning. Heavy vehicle ahead."

            return "Warning. High collision risk."

        # Medium Risk
        if risk_level == "Medium":

            if counts.get("person", 0) > 0:
                return "Pedestrian nearby."

            if counts.get("truck", 0) > 0:
                return "Maintain distance from truck."

            if scene["traffic_level"] == "Heavy":
                return "Heavy traffic ahead."

            return "Proceed with caution."

        # Low Risk

        if scene["traffic_level"] == "Heavy":
            return "Traffic is heavy."

        return None