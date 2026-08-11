from ultralytics import YOLO


class ObjectDetector:

    def __init__(self, model_path="yolo11n.pt"):
        """
        Load YOLO model.
        """

        self.model = YOLO(model_path)

    def detect(self, frame):
        """
        Standard object detection.
        """

        results = self.model(frame)

        return results[0]

    def track(self, frame):
        """
        Multi-object tracking using ByteTrack.
        """

        results = self.model.track(

            frame,

            persist=True,

            tracker="bytetrack.yaml",

            verbose=False

        )

        return results[0]