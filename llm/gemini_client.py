from ._prompt import SYSTEM_INSTRUCTION, prompt_generator


class GeminiClient:
    def __init__(
        self,
        temperature,
        max_output_tokens,
    ):
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def generate_answer(self, question, retrieved_documents):
        if not retrieved_documents:
            return "I don't have enough information to answer this question."
        response = self.client.models.generate_content(
            model=self.llm_model,
            contents=prompt_generator(question, retrieved_documents),
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": self.temperature,
                "max_output_tokens": self.max_output_tokens,
            },
        )
        return response.text
