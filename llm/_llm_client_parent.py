from abc import ABC, abstractmethod


class LLMClientParent(ABC):
    def __init__(
        self,
        temperature,
        max_output_tokens,
    ):
        super().__init__()
        self._temperature = temperature
        self._max_output_tokens = max_output_tokens
        self._client = None
        self._llm_model_name = None

    @abstractmethod
    def generate_answer(self, question, retrieved_documents):
        pass
