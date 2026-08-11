from collections import Counter


class SceneAnalyzer:

    def __init__(self):
        """
        Initialize Scene Analyzer
        """
        pass

    def analyze(self, result):

        detected_objects = []

        # ---------------------------------
        # Collect object names
        # ---------------------------------

        for box in result.boxes:

            class_id = int(box.cls[0])

            class_name = result.names[class_id]

            detected_objects.append(class_name)

        # ---------------------------------
        # Count objects
        # ---------------------------------

        object_counts = Counter(detected_objects)

        # ---------------------------------
        # Scene Summary
        # ---------------------------------

        summary = self.create_summary(object_counts)

        traffic_level = self.get_traffic_level(object_counts)

        pedestrian_risk = self.get_pedestrian_risk(object_counts)

        cyclist_present = self.check_cyclist(object_counts)

        return {

            "summary": summary,

            "traffic_level": traffic_level,

            "pedestrian_risk": pedestrian_risk,

            "cyclist_present": cyclist_present,

            "object_counts": object_counts

        }

    # ---------------------------------
    # Create Summary
    # ---------------------------------

    def create_summary(self, object_counts):

        if len(object_counts) == 0:
            return "No objects detected."

        sentence = "Detected "

        items = []

        for obj, count in object_counts.items():

            if count == 1:
                items.append(f"{count} {obj}")

            else:
                items.append(f"{count} {obj}s")

        sentence += ", ".join(items)

        sentence += "."

        return sentence

    # ---------------------------------
    # Traffic Density
    # ---------------------------------

    def get_traffic_level(self, object_counts):

        cars = object_counts.get("car", 0)

        if cars >= 8:
            return "Heavy"

        elif cars >= 4:
            return "Moderate"

        else:
            return "Light"

    # ---------------------------------
    # Pedestrian Risk
    # ---------------------------------

    def get_pedestrian_risk(self, object_counts):

        people = object_counts.get("person", 0)

        if people >= 5:
            return "High"

        elif people >= 2:
            return "Medium"

        else:
            return "Low"

    # ---------------------------------
    # Bicycle Presence
    # ---------------------------------

    def check_cyclist(self, object_counts):

        return object_counts.get("bicycle", 0) > 0