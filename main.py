from rag.rag_pipeline import RAGPipeline

rag_pipeline = RAGPipeline()
rag_pipeline.generate_vectors()
print(rag_pipeline.ask("At which university did he study?"))
