import re


def clean_text(text):
    # Normalize Windows and Unix line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove repeated spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines, but preserve paragraph breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_documents(documents):
    cleaned = []

    for document in documents:
        text = clean_text(document["text"])

        if text:
            cleaned.append({
                "text": text,
                "metadata": document["metadata"]
            })

    return cleaned