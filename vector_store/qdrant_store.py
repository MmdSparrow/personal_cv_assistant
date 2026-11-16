import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointIdsList,
    PointStruct,
    VectorParams,
)

from constants.base_directories_names_constants import QDRANT_DATABASE_DIRECTORY


class QdrantStore:
    def __init__(
        self,
        collection_name,
    ):
        QDRANT_DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        self.client = QdrantClient(path=QDRANT_DATABASE_DIRECTORY)
        self.collection_name = collection_name

    @staticmethod
    def __convert_id(id):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(id)))

    def _create_collection(self, vector_size):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add(self, ids, documents, embeddings, metadatas):
        if not embeddings:
            return

        self._create_collection(len(embeddings[0]))

        points = [
            PointStruct(
                id=self.__convert_id(id),
                vector=embedding,
                payload={
                    "text": document,
                    "metadata": metadata,
                    "original_id": str(id),
                },
            )
            for id, document, embedding, metadata in zip(
                ids, documents, embeddings, metadatas
            )
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query_embedding, top_k):
        if self.count() == 0:
            return []

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=min(top_k, self.count()),
            with_payload=True,
        )

        return [
            {"text": point.payload["text"], "similarity": point.score}
            for point in results.points
        ]

    def count(self):
        if not self.client.collection_exists(self.collection_name):
            return 0

        return self.client.count(
            collection_name=self.collection_name,
            exact=True,
        ).count

    def delete(self, ids):
        if not self.client.collection_exists(self.collection_name):
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=PointIdsList(points=[self.__convert_id(id) for id in ids]),
        )

    def close(self):
        self.client.close()
