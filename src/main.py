# src/main.py
from modules.agent import create_agent_instance


async def main(question_text: str, user_id: str) -> str:
    """Задаёт вопрос ассистенту 1С и возвращает ответ.

    user_id используется как thread_id в LangGraph —
    по нему хранится история диалога пользователя.
    """
    config = {"configurable": {"thread_id": user_id}}

    agent = create_agent_instance()
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": question_text}]},
        config,
    )
    return response["messages"][-1].content