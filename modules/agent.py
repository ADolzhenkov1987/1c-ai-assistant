# src/agent.py
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools import tools
from config import LLM_MODEL
from system_prompt import system_prompt

def create_agent_instance():
    llm = ChatOllama(
        model=LLM_MODEL,
        base_url="http://localhost:11434",
        temperature=0.3,
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    return agent