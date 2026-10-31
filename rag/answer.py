import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from rag.retriever import retrieve_documents
from rag.evidence import check_evidence
from rag.conflict import detect_conflicts
from rag.prompt import SYSTEM_PROMPT, build_user_prompt


load_dotenv()


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=api_key
    )


def answer_question(question, top_k=5):
    # Step 1: Retrieve relevant document chunks
    retrieved_documents = retrieve_documents(
        question=question,
        top_k=top_k
    )

    # Step 2: Check whether evidence looks sufficient
    evidence_result = check_evidence(retrieved_documents)

    if not evidence_result["sufficient"]:
        return {
            "status": "insufficient_evidence",
            "answer": (
                "I couldn't find enough information in the provided "
                "documents to answer that."
            ),
            "sources": [],
            "conflict_detected": False,
            "evidence_sufficient": False,
            "reason": evidence_result["reason"]
        }

    # Step 3: Check for possible conflicts
    conflict_result = detect_conflicts(retrieved_documents)

    # Step 4: Prepare context and ask Groq
    llm = get_llm()

    user_prompt = build_user_prompt(
        question,
        retrieved_documents
    )

    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", user_prompt)
    ])

    answer_text = response.content

    # Step 5: Build source list for the UI
    sources = []

    for index, document in enumerate(retrieved_documents, start=1):
        metadata = document["metadata"]

        sources.append({
            "citation": f"[{index}]",
            "document": metadata.get("source", "Unknown source"),
            "page": metadata.get("page", "Unknown page"),
            "section": metadata.get("section", "Unknown section"),
            "version": metadata.get("version", "Unknown version"),
            "status": metadata.get("status", "Unknown status")
        })

    # Step 6: Return a consistent response for Streamlit
    return {
        "status": "answered",
        "answer": answer_text,
        "sources": sources,
        "conflict_detected": conflict_result["conflict_detected"],
        "conflicts": conflict_result["conflicts"],
        "evidence_sufficient": True,
        "reason": evidence_result["reason"]
    }
