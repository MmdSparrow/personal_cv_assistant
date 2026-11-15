from abc import ABC, abstractmethod

from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentIngesterParent(ABC):
    def __init__(
        self,
        documents_directory,
        chunk_size,
        chunk_overlap,
    ):
        super().__init__()
        self._documents_directory = documents_directory
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    @abstractmethod
    @staticmethod
    def _load():
        pass

    @abstractmethod
    def process_files(self):
        pass
