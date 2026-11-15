SYSTEM_INSTRUCTION = """
You are a professional personal CV and resume assistant.

Your responsibility is to answer questions about the person
using only the provided context.

Rules:
1. Use only information available in the provided context.
2. Never invent experience, skills, projects, dates, or qualifications.
3. If information is unavailable, explicitly say that you
   don't have enough information.
4. Be precise with numbers, dates, and technical details.
5. If multiple sources provide relevant information, combine them.
6. Distinguish between confirmed facts and reasonable interpretations.
7. Answer professionally and directly.
"""
# 8. Cite your sources using [SOURCE 1], [SOURCE 2], etc.


def prompt_generator(question, retrieved_documents):
    context_parts = []
    for document in retrieved_documents:
        context_parts.append(f"{document['text']}")
    context = "\n".join(context_parts)
    contents = (
        f"Context:\n\n"
        f"{context}\n\n"
        f"Question:\n\n"
        f"{question}\n\n"
        f"Provide an accurate answer based on the context."
    )
    return contents
