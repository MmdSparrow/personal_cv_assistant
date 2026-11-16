import os

from dotenv import load_dotenv
from google import genai

from ._llm_client_parent import LLMClientParent
from ._prompt import SYSTEM_INSTRUCTION, prompt_generator


class GeminiClient(LLMClientParent):
    def __init__(
        self,
        temperature,
        max_output_tokens,
    ):
        super().__init__(temperature, max_output_tokens)
        load_dotenv()
        self._client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self._llm_model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    def generate_answer(self, question, retrieved_documents):
        if not retrieved_documents:
            return "I don't have enough information to answer this question."
        response = self._client.models.generate_content(
            model=self._llm_model_name,
            contents=prompt_generator(question, retrieved_documents),
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": self._temperature,
                "max_output_tokens": self._max_output_tokens,
            },
        )
        return response.text
