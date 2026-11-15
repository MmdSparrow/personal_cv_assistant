from configs.configs import (
    BATCH_SIZE,
    BEST_RESULTS_TOP_K,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
)
from constants.base_directories_names_constants import (
    CHROMA_DATABASE_DIRECTORY,
    JSON_RESOURCES_DIRECTORY,
    PDF_RESOURCES_DIRECTORY,
    TEXT_RESOURCES_DIRECTORY,
)
from embeddings import EmbeddingModel
from indexing.document_indexer import DocumentIndexer
from ingestion import JSONIngester, PDFIngester, TextIngester
from llm.gemini_client import GeminiClient
from vector_store import ChromaStore


class RAGPipeline:
    def __init__(
        self,
        embedding_model_name=EMBEDDING_MODEL_NAME,
        database_directory=CHROMA_DATABASE_DIRECTORY,
        collection_name=COLLECTION_NAME,
        best_results_top_k=BEST_RESULTS_TOP_K,
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    ):
        self.embedding_model = EmbeddingModel(embedding_model_name)
        self.vector_store = ChromaStore(database_directory, collection_name)
        self.best_results_top_k = best_results_top_k
        self.gemini_client = GeminiClient(temperature, max_output_tokens)

    def create_vector_db(
        self,
        batch_size=BATCH_SIZE,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        json_resources_directory=JSON_RESOURCES_DIRECTORY,
        pdf_resources_directory=PDF_RESOURCES_DIRECTORY,
        text_resources_directory=TEXT_RESOURCES_DIRECTORY,
    ):
        json_ingester = JSONIngester(
            documents_directory=json_resources_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        pdf_ingester = PDFIngester(
            documents_directory=pdf_resources_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        text_ingester = TextIngester(
            documents_directory=text_resources_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        documents = []

        documents.extend(json_ingester.process_files())
        documents.extend(pdf_ingester.process_files())
        documents.extend(text_ingester.process_files())

        document_indexer = DocumentIndexer(
            batch_size=batch_size,
            embeddings_model=self.embedding_model,
            vector_store=self.vector_store,
        )

        document_indexer.index_documents(documents)

    def ask(self, question):
        query_embeddings = self.embedding_model.generate_query_embeddings(question)
        retrieved_documents = self.vector_store.search(
            query_embeddings, self.best_results_top_k
        )
        answer = self.gemini_client.generate_answer(question, retrieved_documents)
        return {"question": question, "answer": answer}
