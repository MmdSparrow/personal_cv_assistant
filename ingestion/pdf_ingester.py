import fitz

from ._document_ingester_parent import DocumentIngesterParent


class PDFIngester(DocumentIngesterParent):
    def __init__(
        self,
        pdfs_directory,
        chunk_size,
        chunk_overlap,
    ):
        super().__init__(pdfs_directory, chunk_size, chunk_overlap)

    @staticmethod
    def _load(pdf_file_path):
        pages = []
        with fitz.open(pdf_file_path) as pdf:
            for page_number, page in enumerate(pdf):
                text = page.get_text("text").strip()
                if text:
                    pages.append(
                        {"text": text, "page": page_number + 1, "source": str(pdf_file_path)}
                    )
        return pages

    def process_files(self):
        documents = []
        for pdf_path in sorted(self._documents_directory.rglob("*.pdf")):
            pages = self._load(pdf_path)
            for page in pages:
                chunks = self.text_splitter.split_text(page["text"])
                for chunk_index, chunk in enumerate(chunks):
                    documents.append(
                        {
                            "text": chunk,
                            "source": page["source"],
                            "page": page["page"],
                            "chunk_index": chunk_index,
                        }
                    )
        return documents
