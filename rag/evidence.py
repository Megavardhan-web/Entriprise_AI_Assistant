MIN_DISTANCE = 0.75


def check_evidence(retrieved_documents, min_distance=MIN_DISTANCE):
    if not retrieved_documents:
        return {
            "sufficient": False,
            "reason": "No relevant documents were retrieved."
        }

    best_distance = min(
        document["distance"]
        for document in retrieved_documents
    )

    if best_distance > min_distance:
        return {
            "sufficient": False,
            "reason": "Retrieved documents may not contain enough relevant evidence."
        }

    return {
        "sufficient": True,
        "reason": "Relevant evidence was retrieved."
    }