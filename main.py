from fastapi import FastAPI
from pydantic import BaseModel
from llm import decide_tool, generate_answer
from tools import get_time
from pprint import pprint

chat_history=[]

app=FastAPI()

class Question(BaseModel):
    question:str

@app.post("/question")
def ask(data:Question):

    chat_history.append({
        "role":"user",
        "content":data.question
    })

    tool_name=decide_tool(data.question)

    messages=[{
        "role":"system",
        "content":"You are an Ai Agent, use tool content if it is provided."
    }]

    messages.extend(chat_history)

    if "get_time" in tool_name:
        current_time=get_time()
        messages.append({
            "role":"assistant",
            "content":f"The current time is {current_time}. Use this exact value to answer the user's question."
        })

    answer=generate_answer(messages)

    print(answer)

    chat_history.append({
        "role":"assistant",
        "content":answer
    })

    return{
        "question":data.question,
        "answer":answer
    }
