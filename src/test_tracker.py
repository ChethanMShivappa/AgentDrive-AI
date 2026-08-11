import cv2

from detector import ObjectDetector

detector = ObjectDetector()

video = cv2.VideoCapture("videos/road.mp4")

while True:

    success, frame = video.read()

    if not success:
        break

    result = detector.track(frame)

    print(result.boxes.id)

    cv2.imshow("Tracking Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()

cv2.destroyAllWindows()