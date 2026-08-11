from collections import Counter

from detector import ObjectDetector
from visualizer import Visualizer
from scene_analyzer import SceneAnalyzer
from risk_engine import RiskEngine
from motion_analyzer import MotionAnalyzer
from llm_assistant import LLMAssistant
from decision_engine import DecisionEngine
from memory import DrivingMemory
from voice_agent import VoiceAgent
from alert_engine import AlertEngine


class AgentDrivePipeline:

    def __init__(self):

        self.detector = ObjectDetector()

        self.visualizer = Visualizer()

        self.scene_analyzer = SceneAnalyzer()

        self.risk_engine = RiskEngine()

        self.motion_analyzer = MotionAnalyzer()

        self.assistant = LLMAssistant()

        self.decision_engine = DecisionEngine()

        self.memory = DrivingMemory()

        self.voice = VoiceAgent()

        self.alert_engine = AlertEngine()

        self.previous_alert = ""

    def process_frame(self, frame):

        # -----------------------------
        # Object Detection
        # -----------------------------

        result = self.detector.track(frame)

        frame = self.visualizer.draw(frame, result)

        # -----------------------------
        # Scene Analysis
        # -----------------------------

        scene = self.scene_analyzer.analyze(result)

        # -----------------------------
        # Risk Analysis
        # -----------------------------

        risk = self.risk_engine.assess_risk(scene)

        # -----------------------------
        # Motion Analysis
        # -----------------------------

        motion = self.motion_analyzer.analyze(result)

        approaching = Counter()

        moving_away = Counter()

        for obj in motion.values():

            if obj["movement"] == "Approaching":

                approaching[obj["class"]] += 1

            elif obj["movement"] == "Moving Away":

                moving_away[obj["class"]] += 1

        lines = []

        for cls, count in approaching.items():

            if count == 1:

                lines.append(f"One {cls} is approaching.")

            else:

                lines.append(f"{count} {cls}s are approaching.")

        for cls, count in moving_away.items():

            if count == 1:

                lines.append(f"One {cls} is moving away.")

            else:

                lines.append(f"{count} {cls}s are moving away.")

        if lines:

            motion_summary = "\n".join(lines)

        else:

            motion_summary = "No significant object movement detected."

        # -----------------------------
        # Generate LLM Advice
        # -----------------------------

        if self.decision_engine.should_call_llm(risk):

            advice = self.assistant.generate_advice(
                scene,
                risk,
                motion_summary
            )

            self.memory.save_advice(advice)

        else:

            advice = self.memory.get_last_advice()

        # -----------------------------
        # Generate Voice Alert
        # -----------------------------

        alert = self.alert_engine.generate_alert(
            scene,
            risk
        )

        # -----------------------------
        # Speak Only When Alert Changes
        # -----------------------------

        if alert is not None:

            if alert != self.previous_alert:

                try:

                    self.voice.speak(alert)

                    self.previous_alert = alert

                except Exception as e:

                    print(f"Voice Error : {e}")

        # -----------------------------
        # Return Everything
        # -----------------------------

        return {

            "frame": frame,

            "scene": scene,

            "risk": risk,

            "motion_summary": motion_summary,

            "advice": advice,

            "last_alert": self.voice.get_last_message()

        }