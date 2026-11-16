import hashlib

from constants.common_constatnts_names import (
    CHUNK_INDEX_KEY_NAME,
    SOURCE_KEY_NAME,
    TEXT_KEY_NAME,
)


class DocumentIndexer:
    def __init__(
        self,
        batch_size,
        embeddings_model,
        vector_store,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.embeddings_model = embeddings_model
        self.vector_store = vector_store

    def index_documents(self, documents):
        if not documents:
            return
        for start in range(0, len(documents), self.batch_size):
            batch = documents[start : start + self.batch_size]
            texts = [document[TEXT_KEY_NAME] for document in batch]
            embeddings = self.embeddings_model.generate_text_embeddings(texts)
            ids = [
                hashlib.sha256(
                    (
                        document[SOURCE_KEY_NAME]
                        + str(document[CHUNK_INDEX_KEY_NAME])
                        + document[TEXT_KEY_NAME]
                    ).encode("utf-8")
                ).hexdigest()
                for document in batch
            ]
            metadatas = [
                {
                    SOURCE_KEY_NAME: document[SOURCE_KEY_NAME],
                    CHUNK_INDEX_KEY_NAME: document[CHUNK_INDEX_KEY_NAME],
                }
                for document in batch
            ]
            self.vector_store.add(
                ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas
            )
