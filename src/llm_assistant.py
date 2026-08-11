from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from config import MODEL_NAME, TEMPERATURE, GROQ_API_KEY


class LLMAssistant:

    def __init__(self):

        self.llm = ChatGroq(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            api_key=GROQ_API_KEY,
        )

        self.prompt = ChatPromptTemplate.from_messages(

            [

                (

                    "system",

                    """
You are AgentDrive AI.

You are an intelligent driving assistant.

Use ONLY the information provided.

Do NOT invent objects.

Do NOT invent traffic conditions.

Return plain text only.

Do NOT use markdown.

Do NOT use headings.

Do NOT use bullet points.

Do NOT use numbering.

Write a maximum of three short sentences.

Focus only on safe driving advice.
"""

                ),

                (

                    "human",

                    """
Road Summary

{summary}

Traffic Level : {traffic}

Pedestrian Risk : {pedestrian}

Cyclist Present : {cyclist}

Overall Risk : {risk}

Moving Objects

{motion_summary}

Provide driving advice.
"""

                ),

            ]

        )

    def generate_advice(self, scene, risk, motion_summary):

        chain = self.prompt | self.llm

        response = chain.invoke(

            {

                "summary": scene["summary"],

                "traffic": scene["traffic_level"],

                "pedestrian": scene["pedestrian_risk"],

                "cyclist": scene["cyclist_present"],

                "risk": risk["risk_level"],

                "motion_summary": motion_summary

            }

        )

        return response.content