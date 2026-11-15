# import chromadb


# class ChromaStore:
#     def __init__(
#         self,
#         database_directory,
#         collection_name,
#     ):
#         self.client = chromadb.PersistentClient(path=database_directory)
#         self.collection = self.client.get_or_create_collection(
#             name=collection_name, metadata={"hnsw:space": "cosine"}
#         )

#     def add(self, ids, documents, embeddings, metadatas):
#         self.collection.upsert(
#             ids=ids,
#             documents=documents,
#             embeddings=embeddings,
#             metadatas=metadatas,
#         )

#     def search(self, query_embedding, top_k):
#         if self.collection.count() == 0:
#             return []
#         results = self.collection.query(
#             query_embeddings=[query_embedding],
#             n_results=min(top_k, self.collection.count()),
#             include=["documents", "distances"],
#         )

#         return [
#             {"text": document, "distance": distance}
#             for document, distance in zip(
#                 results["documents"][0],
#                 results["distances"][0],
#             )
#         ]

#     def count(self):
#         return self.collection.count()

#     def delete(self, ids):
#         self.collection.delete(ids=ids)

