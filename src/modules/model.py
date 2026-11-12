from langchain_gigachat import GigaChat
import os
credentials = os.getenv("GIGACHAT_CREDENTIALS")
if not credentials:
    raise RuntimeError(
        "GIGACHAT_CREDENTIALS не задана. Проверьте файл .env рядом с docker-compose.yml"
    )
model = GigaChat(
    credentials = credentials,
    model="GigaChat-2",
    verify_ssl_certs=False,
)