# src/agent.py
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.tools import tools
from src.config import OLLAMA_BASE_URL, LLM_MODEL

def create_agent():
    llm = ChatOpenAI(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        api_key="not-needed",
        temperature=0.3,
    )

    system_prompt = """Ты — AI-ассистент разработчика 1С. Твоя задача — помогать 
    с написанием кода на встроенном языке 1С (BSL), языке запросов 1С, 
    работе с метаданными, формами, регистрами и справочниками.

    Правила:
    1. ВСЕГДА ищи точную информацию в базе знаний перед генерацией кода
    2. Используй актуальный синтаксис платформы 1С:Предприятие 8.3
    3. Соблюдай стандарты разработки 1С
    4. Объясняй свои решения кратко и по делу
    5. Если не уверен — скажи об этом и предложи варианты

    У тебя есть инструменты:
    - search_1c_docs: поиск по документации и примерам 1С
    - generate_bsl: генерация BSL-кода с учётом контекста

    Сначала ищи информацию, потом генерируй код.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )