import cv2
from collections import Counter

from detector import ObjectDetector
from visualizer import Visualizer
from scene_analyzer import SceneAnalyzer
from risk_engine import RiskEngine
from motion_analyzer import MotionAnalyzer
from llm_assistant import LLMAssistant
from decision_engine import DecisionEngine
from memory import DrivingMemory

# ==========================================
# Create Objects
# ==========================================

detector = ObjectDetector()
visualizer = Visualizer()
analyzer = SceneAnalyzer()
risk_engine = RiskEngine()
motion_analyzer = MotionAnalyzer()
assistant = LLMAssistant()
decision_engine = DecisionEngine()
memory = DrivingMemory()

# ==========================================
# Open Video
# ==========================================

video = cv2.VideoCapture("videos/road.mp4")

# ==========================================
# Process Video
# ==========================================

while True:

    success, frame = video.read()

    if not success:
        break

    # --------------------------------------
    # Object Detection + Tracking
    # --------------------------------------

    result = detector.track(frame)

    # --------------------------------------
    # Scene Analysis
    # --------------------------------------

    scene = analyzer.analyze(result)

    # --------------------------------------
    # Risk Analysis
    # --------------------------------------

    risk = risk_engine.assess_risk(scene)

    # --------------------------------------
    # Motion Analysis
    # --------------------------------------

    motion = motion_analyzer.analyze(result)

    # --------------------------------------
    # Summarize Motion
    # --------------------------------------

    approaching = Counter()
    moving_away = Counter()

    for info in motion.values():

        if info["movement"] == "Approaching":
            approaching[info["class"]] += 1

        elif info["movement"] == "Moving Away":
            moving_away[info["class"]] += 1

    motion_lines = []

    for obj, count in approaching.items():

        if count == 1:
            motion_lines.append(f"One {obj} is approaching.")
        else:
            motion_lines.append(f"{count} {obj}s are approaching.")

    for obj, count in moving_away.items():

        if count == 1:
            motion_lines.append(f"One {obj} is moving away.")
        else:
            motion_lines.append(f"{count} {obj}s are moving away.")

    if motion_lines:
        motion_summary = "\n".join(motion_lines)
    else:
        motion_summary = "No significant object movement detected."

    # --------------------------------------
    # Draw Bounding Boxes
    # --------------------------------------

    frame = visualizer.draw(frame, result)

    # --------------------------------------
    # Decision Engine
    # --------------------------------------

    if decision_engine.should_call_llm(risk):

        advice = assistant.generate_advice(
            scene,
            risk,
            motion_summary
        )

        memory.save_advice(advice)

    else:

        advice = memory.get_last_advice()

    # --------------------------------------
    # Terminal Output
    # --------------------------------------

    print("\n" + "=" * 70)
    print("AGENTDRIVE AI")
    print("=" * 70)

    print(scene["summary"])
    print()

    print(f"Traffic Level      : {scene['traffic_level']}")
    print(f"Pedestrian Risk    : {scene['pedestrian_risk']}")
    print(f"Cyclist Present    : {scene['cyclist_present']}")
    print()

    print(f"Overall Risk Level : {risk['risk_level']}")
    print(f"Risk Score         : {risk['risk_score']}")
    print()

    print("-" * 70)
    print("Motion Summary")
    print()

    print(motion_summary)

    print("-" * 70)
    print("AI Driving Advice")
    print()

    print(advice)

    print("=" * 70)

    # --------------------------------------
    # Display Video
    # --------------------------------------

    cv2.imshow("AgentDrive AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()