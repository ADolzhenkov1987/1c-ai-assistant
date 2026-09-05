# src/main.py
from src.agent import create_agent

def main():
    print("=== 1C AI Ассистент ===")
    print("Введите вопрос по разработке 1С (или 'выход' для завершения)\n")

    agent = create_agent()

    while True:
        user_input = input("Вы: ").strip()
        if user_input.lower() in ("выход", "exit", "quit"):
            break

        try:
            response = agent.invoke({"input": user_input})
            print(f"\nАссистент: {response['output']}\n")
        except Exception as e:
            print(f"\nОшибка: {e}\n")

if __name__ == "__main__":
    main()