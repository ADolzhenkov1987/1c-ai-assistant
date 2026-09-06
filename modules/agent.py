# src/agent.py
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from modules.tools import tools
from modules.config import LLM_MODEL, OLLAMA_BASE_URL
from modules.system_prompt import system_prompt
from langgraph.checkpoint.memory import InMemorySaver

def create_agent_instance():
    llm = ChatOllama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.3,
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver()
    )

    return agent