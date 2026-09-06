# src/main.py
from modules.agent import create_agent_instance

async def  main(question_text: str, user_id: str) -> str:

    print("=== 1C AI Ассистент ===")
    print("Введите вопрос по разработке 1С: \n")

    config = {'configurable': {'thread_id': user_id}}

    agent = create_agent_instance()
    response = await agent.ainvoke({"messages": [{"role": "user", "content": question_text}]}, config)
    return response['messages'][-1].content