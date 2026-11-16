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
    JSON_RESOURCES_DIRECTORY,
    PDF_RESOURCES_DIRECTORY,
    TEXT_RESOURCES_DIRECTORY,
)
from constants.common_constatnts_names import DATABASE_QDRANT_NAME, LLM_CLIENT_GROQ_NAME
from embeddings import EmbeddingModel
from indexing.document_indexer import DocumentIndexer
from ingestion import JSONIngester, PDFIngester, TextIngester
from utils.rag_utils import database_selector, llm_client_selector


class RAGPipeline:
    def __init__(
        self,
        embedding_model_name=EMBEDDING_MODEL_NAME,
        database_name=DATABASE_QDRANT_NAME,
        collection_name=COLLECTION_NAME,
        best_results_top_k=BEST_RESULTS_TOP_K,
        llm_client_name=LLM_CLIENT_GROQ_NAME,
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    ):
        self.embedding_model = EmbeddingModel(embedding_model_name)
        DatabaseClass = database_selector(database_name)
        self.vector_store = DatabaseClass(collection_name)
        self.best_results_top_k = best_results_top_k
        LLMClientClass = llm_client_selector(llm_client_name)
        self.llm_client = LLMClientClass(temperature, max_output_tokens)

    def generate_vectors(
        self,
        batch_size=BATCH_SIZE,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        json_resources_directory=JSON_RESOURCES_DIRECTORY,
        pdf_resources_directory=PDF_RESOURCES_DIRECTORY,
        text_resources_directory=TEXT_RESOURCES_DIRECTORY,
    ):
        json_ingester = JSONIngester(
            jsons_documents_directory=json_resources_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        pdf_ingester = PDFIngester(
            pdfs_documents_directory=pdf_resources_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        text_ingester = TextIngester(
            texts_documents_directory=text_resources_directory,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        documents = []
        print("ingesters object created")
        documents.extend(json_ingester.process_files())
        documents.extend(pdf_ingester.process_files())
        documents.extend(text_ingester.process_files())
        print("documents process completed")

        document_indexer = DocumentIndexer(
            batch_size=batch_size,
            embeddings_model=self.embedding_model,
            vector_store=self.vector_store,
        )
        print("documents indexed")

        document_indexer.index_documents(documents)

    def ask(self, question):
        query_embeddings = self.embedding_model.generate_query_embeddings(question)
        retrieved_documents = self.vector_store.search(
            query_embeddings, self.best_results_top_k
        )
        print("searching done")
        answer = self.llm_client.generate_answer(question, retrieved_documents)
        print("answered by gemini")
        return {"question": question, "answer": answer}
