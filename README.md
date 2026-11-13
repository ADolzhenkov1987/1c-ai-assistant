# Настройка ИИ-агента для работы с 1C:EDT

Связка: **VS Code + Cline → gpt2giga → GigaChat**, плюс два MCP-сервера:
контекст конфигурации из EDT и собственный ассистент по стандартам 1С (Docker).

## Предусловия

Установлены: Docker, 1C:EDT, Docker-контейнер агента (порт 8000, работает).
Дополнительно требуются: **git**, **Python 3.10–3.14**, **uv** (`pip install uv`),
**VS Code**, **ключ GigaChat** (free-тариф физлица, scope `GIGACHAT_API_PERS`).

## Этап 1. Прокси gpt2giga

powershell:
pip install --upgrade uv          # если uv старый
uv tool install gpt2giga

В отдельной папке (например C:\Python\gpt2giga) создать .env

Содержимое файла .env:

GPT2GIGA_MODE=PROD
GPT2GIGA_ENABLE_API_KEY_AUTH=True
GPT2GIGA_API_KEY=<произвольный_секрет> (задать самостоятельно, запомнить)
GIGACHAT_CREDENTIALS=<тот же ключ, что в .env контейнера агента> (Ваш ключ от Гигачата)
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_VERIFY_SSL_CERTS=False   # для локальной разработки

cd C:\Python\gpt2giga
gpt2giga        # окно держать открытым

Если команда gpt2giga не находится: uv tool bin path показывает папку тулов — добавить её в PATH либо запускать через uvx gpt2giga.

Проверка: Invoke-RestMethod http://localhost:8090/health

## Этап 2. VS Code + Cline

Установить расширение Cline из marketplace.
Настройки провайдера:

| Поле | Значение |
|---|---|
|API Provider |	OpenAI Compatible|
|Base URL | http://localhost:8090/v1 (слэш /v1 обязателен)|
|API Key | значение GPT2GIGA_API_KEY из .env прокси|
|Model ID | GigaChat-3-Ultra — единственная модель free-тарифа|

Проверка: задать простой вопрос. Если модель указана неверно — прокси вернёт 502 «Upstream service error» с 404 «No such model» в логах.

## Этап 3. Плагин edt-companion-mcp в EDT

EDT → Help → Install New Software… → https://sekam68.github.io/edt-companion-mcp/
Установить edt-companion-mcp, перезапустить EDT.

Проверка: Invoke-RestMethod http://127.0.0.1:6868/health — статус ok и список проектов workspace.

## Этап 4. Проекты в git и подключение MCP-серверов

Проекты EDT должны лежать в git (плагин прописывает .mcp.json в корень репозитория через «Прописать сервер в .mcp.json проектов…»). В .gitignore: .metadata/, *.cfe, *.hbk, *.dt.

В Cline: MCP Servers → Configure → файл cline_mcp_settings.json:

{
  "mcpServers": {
    "edt-companion-mcp": {
      "type": "streamableHttp",
      "url": "http://127.0.0.1:6868/mcp",
      "disabled": false
    },
    "assistant-1c": {
      "type": "streamableHttp",
      "url": "http://localhost:8000/mcp",
      "disabled": false
    }
  }
}

Важно: транспорт строго streamableHttp — без этого Cline уходит в SSE и получает ошибку 405.
Имя сервера агента не должно начинаться с цифры (1c-assistant отклоняет GigaChat с 422) — используется assistant-1c.

Проверка: в панели MCP Servers оба сервера «connected», тулы видны.

## Этап 5. Правила и рабочий процесс

Файл .clinerules в корне репозитория в формате md (VS Code открыт на корне репозитория):

'''
# Правила работы с кодом 1С

## Получение контекста
- Перед ответами по конфигурации читать код через edt-companion-mcp,
  не опираться на память. Нет модуля — спросить путь, не выдумывать.

## Экспертиза по стандартам 1С
- Рекомендации по стандартам проверять через тул ask_1c_assistant
  сервера assistant-1c. Параметр user_id всегда "edt-work".

## Внесение изменений
- Перед правкой показать план. Править по одному модулю, дифф — на
  подтверждение. После правок запустить валидацию проекта.
- Git-коммиты не делать — коммитит пользователь.
'''

Рабочий цикл:

В EDT открыть нужный модуль, в VS Code — корень репозитория.
Задачу давать в режиме Plan (анализ без правок), план подтвердить → Act.
Изменения файлов Cline вносит на диске; EDT подхватит их в редакторе (перед запуском агента сохранить несохранённые правки в EDT).
Валидация проекта — тулами плагина. Контроль, что отвечал именно Docker-агент: docker compose logs --tail 20 — видны вызовы tools/call с ask_1c_assistant.
Коммит — вручную.

Типовые проблемы
|Симптом | Причина и решение |
|---|---|
|gpt2giga не распознано | Путь тулов не в PATH: uv tool bin path → в PATH, либо uvx gpt2giga|
|Прокси: 502 Upstream service error | Смотреть окно прокси: неверный Model ID (404 No such model), ключ/scope (401), TLS|
|404 «No such model» | Model ID должен быть GigaChat-3-Ultra (free-тариф)|
|Cline: SSE error 405 | В конфиге серверов нет "type": "streamableHttp"|
|422 Invalid function names | Имя MCP-сервера начинается с цифры — переименовать|
|Тулы не видны | JSON-конфиг серверов с ошибкой, нет перезапуска после правки|