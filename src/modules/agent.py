# src/agent.py
from langchain.agents import create_agent
from modules.tools import tools
from modules.system_prompt import system_prompt
from langgraph.checkpoint.memory import InMemorySaver
from .model import model

def create_agent_instance():
    #llm = ChatOllama(
    #    model=LLM_MODEL,
    #    base_url=OLLAMA_BASE_URL,
    #    temperature=0.3,
    #)

    #agent = create_agent(
    #    model=llm,
    #    tools=tools,
    #    system_prompt=system_prompt,
    #    checkpointer=InMemorySaver()
    #)
    agent = create_agent(
        model=model, 
        tools=tools, 
        system_prompt=system_prompt,
        checkpointer=InMemorySaver()
    )

    return agent