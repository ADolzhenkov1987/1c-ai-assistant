# src/config.py
from pathlib import Path

'''Развернул локальную модель. До этого пробовал GigaChat, но для того, 
    чтобы можно было использовать RAG в GigaChat необходима платная подписка с картой сбера, чего у меня не было
'''
OLLAMA_BASE_URL = "http://localhost:11434/v1"

# Данная модель подходит под конфигурацию ноута:
# 32 gb RAM и 5080 mobile with 16 gb vRAM
LLM_MODEL = "qwen2.5:14b"
# модель для поддержки русского языка
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

DOCS_DIR = Path("data/docs")
CODE_EXAMPLES_DIR = Path("data/code_examples")
CHROMA_PERSIST_DIR = Path("chroma_db")
CHROMA_COLLECTION = "1c_knowledge_base"

# размер чанков для пакетной обработки RAG
CHUNK_SIZE = 512
# размер перекрытия между чанками для избежания потери контекста
CHUNK_OVERLAP = 64
TOP_K = 5