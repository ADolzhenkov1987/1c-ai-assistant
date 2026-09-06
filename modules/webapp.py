from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os.path import join, dirname
from fastapi.responses import HTMLResponse
from fastapi import Cookie, Response
from typing import Annotated
from uuid import uuid4

from main import main

frontend_path = join(dirname(dirname(__file__)), "frontend-http.html")

app = FastAPI()

class Question(BaseModel):
    question: str

app = FastAPI(
    title = "Виртуальный помощник 1С",
    description = "Помогает писать код на языке 1С",
    version = "0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                 
    allow_credentials=True,
    allow_methods=["*"],                 
    allow_headers=["*"],
)

@app.get ('/')
async def front():
    with open(frontend_path, encoding='utf-8') as f:
        html = f.read()
    return HTMLResponse(html)

@app.post("/answer/")
async def answer(question: Question, response: Response, user_id: Annotated[str | None, Cookie()] = None):
    if not user_id :
        user_id = uuid4()
        response. set_cookie('user_id' , user_id)
    answer = await main(question.question, user_id)
    return {"answer": answer}