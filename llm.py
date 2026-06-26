from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Returns the current date and time in India."
        }
    }
]

prompt="""
        You are a tool selector.

        Available tools:
        - get_time

        Rules:
        1. If the user's question requires one of the available tools, reply with ONLY the tool name.
        2. If no tool is needed, reply with ONLY:
        NO_TOOL
        3. Do not explain your answer.
        4. Do not include punctuation.
        5. Do not include markdown.
        6. Do not include any extra words.
        """

def decide_tool(question):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role":"user",
            "content":question
        },
        {
            "role":"system",
            "content":prompt
        }
        ]
    )

    return response.choices[0].message.content


def generate_answer(messages):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content