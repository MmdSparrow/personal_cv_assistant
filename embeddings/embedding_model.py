from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(
        self,
        embedding_model_name,
    ):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.__INSTRUCTION_PREFIX = (
            "Represent this sentence for searching relevant passages: "
        )

    def generate_text_embeddings(self, texts):
        return self.embedding_model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False
        ).tolist()

    def generate_query_embeddings(self, question):
        return self.embedding_model.encode(
            [self.__INSTRUCTION_PREFIX + question],
            normalize_embeddings=True,
        )[0].tolist()
