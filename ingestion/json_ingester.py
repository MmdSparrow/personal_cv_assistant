import json

from ._document_ingester_parent import DocumentIngesterParent


class JSONIngester(DocumentIngesterParent):
    def __init__(self, documents_directory, chunk_size, chunk_overlap):
        super().__init__(
            documents_directory,
            chunk_size,
            chunk_overlap,
        )

    @staticmethod
    def _load(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as file_to_read:
            return json.load(file_to_read)

    @staticmethod
    def __json_to_text(data, parent_key=""):
        lines = []
        if isinstance(data, dict):
            for key, value in data.items():
                current_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, (dict, list)):
                    lines.extend(JSONIngester.__json_to_text(value, current_key))
                else:
                    lines.append(f"{current_key}: {value}")
        elif isinstance(data, list):
            for index, value in enumerate(data):
                current_key = f"{parent_key}[{index}]"
                if isinstance(value, (dict, list)):
                    lines.extend(JSONIngester.__json_to_text(value, current_key))
                else:
                    lines.append(f"{current_key}: {value}")
        else:
            lines.append(f"{parent_key}: {data}")
        return lines

    def process_files(self):
        documents = []
        for json_path in sorted(self._documents_directory.rglob("*.json")):
            data = self._load(json_path)
            records = data if isinstance(data, list) else [data]
            for record_index, record in enumerate(records):
                text = "\n".join(self.__json_to_text(record))
                chunks = self.text_splitter.split_text(text)
                for chunk_index, chunk in enumerate(chunks):
                    documents.append(
                        {
                            "text": chunk,
                            "source": str(json_path),
                            "record_index": record_index,
                            "chunk_index": chunk_index,
                        }
                    )
        return documents
