
def detect_conflicts(retrieved_documents):
    conflicts = []

    # Compare chunks from the same policy document only.
    for i in range(len(retrieved_documents)):
        for j in range(i + 1, len(retrieved_documents)):
            doc_a = retrieved_documents[i]
            doc_b = retrieved_documents[j]

            meta_a = doc_a.get("metadata", {})
            meta_b = doc_b.get("metadata", {})

            id_a = meta_a.get("document_id")
            id_b = meta_b.get("document_id")

            # Different policy documents are not automatically conflicts.
            if not id_a or id_a != id_b:
                continue

            version_a = meta_a.get("version", "Unknown")
            version_b = meta_b.get("version", "Unknown")

            status_a = meta_a.get("status", "Unknown").lower()
            status_b = meta_b.get("status", "Unknown").lower()

            # Only flag when both versions are current, or status is unknown.
            if status_a == "superseded" and status_b == "current":
                continue

            if status_b == "superseded" and status_a == "current":
                continue

            if version_a == version_b:
                continue

            conflicts.append({
                "document_id": id_a,
                "version_a": version_a,
                "version_b": version_b,
                "status_a": status_a,
                "status_b": status_b,
                "possible_conflict": True
            })

    return {
        "conflict_detected": len(conflicts) > 0,
        "conflicts": conflicts
    }
