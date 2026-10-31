SYSTEM_PROMPT = """
You are NexaCore Technologies' Enterprise Documentation Assistant.

Answer employee questions using ONLY the supplied document context.

Rules:
1. Do not invent facts or use outside knowledge.
2. If the context does not support an answer, clearly say:
   "I couldn't find enough information in the provided documents to answer that."
3. Cite every factual claim using the source labels provided in the context,
   for example [1] or [2].
4. Do not invent document names, page numbers, or section names.
5. If documents disagree, clearly explain the disagreement and cite both sources.
6. Do not assume that the newest-looking document is authoritative unless
   its metadata identifies it as current.
7. Keep answers clear, concise, and useful.
"""


def build_user_prompt(question, retrieved_documents):
    context_parts = []

    for index, document in enumerate(retrieved_documents, start=1):
        metadata = document["metadata"]

        source = metadata.get("source", "Unknown source")
        page = metadata.get("page", "Unknown page")
        section = metadata.get("section", "Unknown section")
        version = metadata.get("version", "Unknown version")
        status = metadata.get("status", "Unknown status")

        context_parts.append(
            f"""
[{index}]
Source: {source}
Page: {page}
Section: {section}
Version: {version}
Status: {status}

Content:
{document["text"]}
"""
        )

    context = "\n".join(context_parts)

    return f"""
Question:
{question}

Document context:
{context}

Answer the question using only this context and cite the sources.
"""