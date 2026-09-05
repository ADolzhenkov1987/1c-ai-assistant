# src/main.py
from agent import create_agent_instance

def main():
    print("=== 1C AI Ассистент ===")
    print("Введите вопрос по разработке 1С (или 'выход' для завершения)\n")

    agent = create_agent_instance()

    while True:
        user_input = input("Вы: ").strip()
        if user_input.lower() in ("выход", "exit", "quit"):
            break

        try:
            response = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            # Последнее сообщение в списке — финальный ответ агента
            final_message = response["messages"][-1]
            print(f"\nАссистент: {final_message.text}\n")
        except Exception as e:
            print(f"\nОшибка: {e}\n")

if __name__ == "__main__":
    main()