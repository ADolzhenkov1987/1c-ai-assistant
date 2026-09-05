# src/tools.py
from langchain.tools import tool
from rag_pipeline import get_query_engine, build_index

_index = build_index()
_query_engine = get_query_engine(_index)

@tool
def search_1c_docs(query: str) -> str:
    """Ищет по документации, примерам кода и стандартам 1С."""
    response = _query_engine.query(query)
    sources = [n.metadata.get("source", "?") for n in response.source_nodes]
    return f"{response.response}\n\nИсточники: {', '.join(sources[:3])}"

@tool
def generate_bsl(task: str) -> str:
    """Генерирует код на встроенном языке 1С (BSL) по описанию задачи."""
    context = _query_engine.query(f"Примеры кода для задачи: {task}")
    prompt = f"""Ты — опытный разработчик 1С. Напиши код на BSL для задачи:

    {task}

    Контекст из базы знаний:
    {context.response}

    Требования:
    - Стандарты разработки 1С
    - Комментарии к процедурам/функциям
    - Обработка ошибок
    - Если нужен запрос — используй язык запросов 1С
    """
    # В LangChain 1.x агент сам отправит этот промпт в LLM,
    # поэтому здесь мы просто возвращаем промпт как «результат инструмента».
    return prompt

tools = [search_1c_docs, generate_bsl]