from constants.common_constatnts_names import (
    CHUNK_INDEX_KEY_NAME,
    SOURCE_KEY_NAME,
    TEXT_KEY_NAME,
)
from utils.ingestion_utils import load_pdf

from ._document_ingester_parent import DocumentIngesterParent


class PDFIngester(DocumentIngesterParent):
    def __init__(
        self,
        pdfs_documents_directory,
        chunk_size,
        chunk_overlap,
    ):
        super().__init__(pdfs_documents_directory, chunk_size, chunk_overlap)

    def process_files(self):
        documents = []
        for pdf_file_path in sorted(self._documents_directory.rglob("*.pdf")):
            pages = load_pdf(pdf_file_path)
            for text in pages:
                chunks = self._text_splitter.split_text(text)
                for chunk_index, chunk in enumerate(chunks):
                    documents.append(
                        {
                            TEXT_KEY_NAME: chunk,
                            SOURCE_KEY_NAME: str(pdf_file_path),
                            CHUNK_INDEX_KEY_NAME: chunk_index,
                        }
                    )
        return documents
