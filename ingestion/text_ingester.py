from ._document_ingester_parent import DocumentIngesterParent


class TextIngester(DocumentIngesterParent):
    def __init__(self, documents_directory, chunk_size, chunk_overlap):
        super().__init__(
            documents_directory,
            chunk_size,
            chunk_overlap,
        )

    @staticmethod
    def _load(txt_file_path):
        with open(txt_file_path, "r", encoding="utf-8") as file_to_read:
            return file_to_read.read()

    def process_files(self):
        documents = []
        for txt_file_path in sorted(self._documents_directory.rglob("*.pdf")):
            text = self._load(txt_file_path)
            chunks = self.text_splitter.split_text(text)
            for chunk_index, chunk in enumerate(chunks):
                documents.append(
                    {
                        "text": chunk,
                        "source": str(txt_file_path),
                        "chunk_index": chunk_index,
                    }
                )
        return documents
