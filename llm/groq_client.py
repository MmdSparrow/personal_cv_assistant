import os

from dotenv import load_dotenv
from openai import OpenAI

from ._prompt import SYSTEM_INSTRUCTION, prompt_generator


class GroqClient:
    def __init__(
        self,
        temperature,
        max_output_tokens,
    ):
        super().__init__(temperature, max_output_tokens)
        load_dotenv()
        self._client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )
        self._llm_model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    def generate_answer(self, question, retrieved_documents):
        if not retrieved_documents:
            return "I don't have enough information to answer this question."
        response = self._client.chat.completions.create(
            model=self._llm_model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_INSTRUCTION,
                },
                {
                    "role": "user",
                    "content": prompt_generator(
                        question,
                        retrieved_documents,
                    ),
                },
            ],
            temperature=self._temperature,
            max_tokens=self._max_output_tokens,
        )
        return response.choices[0].message.content
