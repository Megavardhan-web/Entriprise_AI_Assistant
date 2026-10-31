def chunk_documents(documents, chunk_size=180, overlap=30):
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    chunks = []

    for document in documents:
        words = document["text"].split()
        start = 0
        chunk_index = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            metadata = document["metadata"].copy()
            metadata["chunk_index"] = chunk_index

            chunks.append({
                "text": chunk_text,
                "metadata": metadata
            })

            chunk_index += 1
            start += chunk_size - overlap

    return chunks