from ingestion.embeddings import load_embedding_model
from ingestion.vector_store import get_collection


# Load once when this module is imported
_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = load_embedding_model()

    return _embedding_model


def retrieve_documents(question, top_k=5):
    collection = get_collection()

    if collection.count() == 0:
        return []

    model = get_embedding_model()

    # Convert the question into a vector using the same model as ingestion
    question_embedding = model.encode(
        question,
        convert_to_numpy=True
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    retrieved = []

    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved