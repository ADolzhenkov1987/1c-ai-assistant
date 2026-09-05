# src/rag_pipeline.py
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from config import *

def init_llm():
    """Подключаем локальную LLM через нативную интеграцию Ollama."""
    return Ollama(
        model=LLM_MODEL,
        base_url="http://localhost:11434",
        request_timeout=120.0,
        context_window=32768,    # Qwen 2.5 поддерживает до 32K
    )

def init_embed_model():
    """Локальные эмбеддинги через sentence-transformers."""
    return HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

def build_index():
    Settings.llm = init_llm()
    Settings.embed_model = init_embed_model()

    db = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))
    chroma_collection = db.get_or_create_collection(CHROMA_COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    documents = []
    for f in DOCS_DIR.rglob("*.md"):
        documents.append(Document(
            text=f.read_text(encoding="utf-8"),
            metadata={"source": str(f), "type": "doc"}
        ))
    for f in CODE_EXAMPLES_DIR.rglob("*.bsl"):
        documents.append(Document(
            text=f.read_text(encoding="utf-8"),
            metadata={"source": str(f), "type": "code_example"}
        ))

    if documents:
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True,
        )
    else:
        index = VectorStoreIndex.from_vector_store(vector_store)

    return index

def get_query_engine(index):
    return index.as_query_engine(similarity_top_k=TOP_K)
