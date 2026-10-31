import re


def extract_numbers(text):
    """
    Extract numbers, percentages, and simple date-like values.
    Example: 20 days, 90%, 1 July 2026
    """
    pattern = r"\b\d+(?:\.\d+)?(?:\s?(?:days?|hours?|weeks?|months?|years?|%))?\b"
    return set(re.findall(pattern, text.lower()))


def detect_conflicts(retrieved_documents):
    conflicts = []

    for i in range(len(retrieved_documents)):
        for j in range(i + 1, len(retrieved_documents)):
            doc_a = retrieved_documents[i]
            doc_b = retrieved_documents[j]

            metadata_a = doc_a["metadata"]
            metadata_b = doc_b["metadata"]

            source_a = metadata_a.get("source", "Unknown source")
            source_b = metadata_b.get("source", "Unknown source")

            text_a = doc_a["text"]
            text_b = doc_b["text"]

            numbers_a = extract_numbers(text_a)
            numbers_b = extract_numbers(text_b)

            # Only flag a possible conflict when both chunks contain
            # numeric policy-like information and come from different sources.
            shared_policy_terms = {
                "leave", "approval", "purchase", "password",
                "remote", "employee", "policy", "days"
            }

            words_a = set(re.findall(r"\b[a-z]+\b", text_a.lower()))
            words_b = set(re.findall(r"\b[a-z]+\b", text_b.lower()))

            common_terms = words_a & words_b & shared_policy_terms

            if (
                source_a != source_b
                and common_terms
                and numbers_a
                and numbers_b
                and numbers_a != numbers_b
            ):
                conflicts.append({
                    "source_a": source_a,
                    "source_b": source_b,
                    "possible_conflict": True,
                    "shared_terms": sorted(common_terms),
                    "numbers_a": sorted(numbers_a),
                    "numbers_b": sorted(numbers_b)
                })

    return {
        "conflict_detected": len(conflicts) > 0,
        "conflicts": conflicts
    }