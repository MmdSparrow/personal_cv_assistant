from constants.common_constatnts_names import (
    DATABASE_CHROMA_NAME,
    DATABASE_QDRANT_NAME,
    LLM_CLIENT_GEMINI_NAME,
    LLM_CLIENT_GROQ_NAME,
)
from llm import GeminiClient, GroqClient
from vector_store import QdrantStore


def database_selector(database_name):
    if database_name == DATABASE_CHROMA_NAME:
        return None
    if database_name == DATABASE_QDRANT_NAME:
        return QdrantStore


def llm_client_selector(llm_client_name):
    if llm_client_name == LLM_CLIENT_GEMINI_NAME:
        return GeminiClient
    if llm_client_name == LLM_CLIENT_GROQ_NAME:
        return GroqClient
