# src/tools.py
from langchain.tools import Tool
from src.rag_pipeline import get_query_engine, build_index

_index = build_index()
_query_engine = get_query_engine(_index)

def search_1c_knowledge(query: str) -> str:
    """Ищет по базе знаний 1С: документация, примеры кода, стандарты."""
    response = _query_engine.query(query)
    sources = [n.metadata.get("source", "?") for n in response.source_nodes]
    return f"{response.response}\n\nИсточники: {', '.join(sources[:3])}"

def generate_bsl_code(task: str) -> str:
    """Генерирует код на встроенном языке 1С по описанию задачи."""
    context = _query_engine.query(f"Примеры кода для задачи: {task}")
    prompt = f"""Ты — опытный разработчик 1С. Напиши код на встроенном языке 1С (BSL) 
    для следующей задачи:

    {task}

    Контекст из базы знаний:
    {context.response}

    Требования:
    - Используй стандарты разработки 1С
    - Добавь комментарии к процедурам и функциям
    - Обрабатывай возможные ошибки
    - Если нужен запрос — используй язык запросов 1С
    """
    return prompt

tools = [
    Tool(
        name="search_1c_docs",
        func=search_1c_knowledge,
        description="Ищет по документации, примерам кода и стандартам 1С. "
                    "Используй, когда нужны точные методы платформы, синтаксис или примеры.",
    ),
    Tool(
        name="generate_bsl",
        func=generate_bsl_code,
        description="Генерирует код на встроенном языке 1С по описанию задачи на русском.",
    ),
]