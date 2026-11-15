from constants.common_constatnts_names import (
    CHUNK_INDEX_KEY_NAME,
    SOURCE_KEY_NAME,
    TEXT_KEY_NAME,
)
from utils.ingestion_utils import json_to_text, load_json

from ._document_ingester_parent import DocumentIngesterParent


class JSONIngester(DocumentIngesterParent):
    def __init__(self, documents_directory, chunk_size, chunk_overlap):
        super().__init__(
            documents_directory,
            chunk_size,
            chunk_overlap,
        )

    def process_files(self):
        documents = []
        for json_path in sorted(self._documents_directory.rglob("*.json")):
            data = load_json(json_path)
            records = data if isinstance(data, list) else [data]
            for record in records:
                text = "\n".join(json_to_text(record))
                chunks = self._text_splitter.split_text(text)
                for chunk_index, chunk in enumerate(chunks):
                    documents.append(
                        {
                            TEXT_KEY_NAME: chunk,
                            SOURCE_KEY_NAME: str(json_path),
                            CHUNK_INDEX_KEY_NAME: chunk_index,
                        }
                    )
        return documents
