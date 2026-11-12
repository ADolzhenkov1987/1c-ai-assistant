# modules/webapp.py
import contextlib
from contextlib import asynccontextmanager
from os.path import join, dirname
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from modules.mcpapp import mcp
from main import main

frontend_path = join(dirname(dirname(__file__)), "frontend-http.html")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(
    title="Виртуальный помощник 1С",
    description="Помогает писать код на языке 1С",
    version="0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.get("/")
async def front():
    with open(frontend_path, encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)


@app.post("/answer/")
async def answer(question: Question, response: Response, user_id: Annotated[str | None, Cookie()] = None):
    if not user_id:
        user_id = str(uuid4())  # строка, а не UUID-объект
        response.set_cookie("user_id", user_id)
    answer_text = await main(question.question, user_id)
    return {"answer": answer_text}


app.mount("/", mcp.streamable_http_app(stateless_http=True, json_response=True))