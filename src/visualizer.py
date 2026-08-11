import cv2


class Visualizer:

    def __init__(self):
        """
        Initialize the visualizer.
        """
        pass

    def get_color(self, class_name):
        """
        Return color based on object type.
        """

        if class_name == "person":
            return (0, 0, 255)      # Red

        elif class_name == "car":
            return (0, 255, 0)      # Green

        elif class_name == "bicycle":
            return (0, 255, 255)    # Yellow

        else:
            return (255, 255, 255)  # White

    def draw(self, frame, result):
        """
        Draw detections on the frame.
        """

        for box in result.boxes:

            class_id = int(box.cls[0])

            class_name = result.names[class_id]

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0]

            color = self.get_color(class_name)

            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                color,
                2
            )

            label = f"{class_name} {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        return frame