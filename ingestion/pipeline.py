from pathlib import Path

from ingestion.loader import load_document
from ingestion.cleaner import clean_documents
from ingestion.chunker import chunk_documents
from ingestion.embeddings import load_embedding_model, generate_embeddings
from ingestion.vector_store import save_chunks


SUPPORTED_EXTENSIONS = {".pdf", ".html", ".htm", ".md", ".txt"}


def ingest_documents(folder_path):
    """
    Ingest every supported document inside a folder.
    Used for indexing the sample documents.
    """
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    documents = []

    for file_path in folder.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            print(f"Loading: {file_path.name}")
            documents.extend(load_document(file_path))

    return process_documents(documents)


def ingest_uploaded_files(file_paths):
    """
    Ingest only the files uploaded through the Streamlit UI.
    """
    documents = []

    for file_path in file_paths:
        path = Path(file_path)

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        print(f"Loading uploaded file: {path.name}")
        documents.extend(load_document(path))

    return process_documents(documents)


def process_documents(documents):
    """
    Shared processing pipeline:
    clean -> chunk -> embed -> save to ChromaDB
    """
    if not documents:
        print("No readable documents found.")
        return 0

    documents = clean_documents(documents)

    chunks = chunk_documents(documents)

    if not chunks:
        print("No chunks were created.")
        return 0

    print("Loading embedding model...")
    model = load_embedding_model()

    texts = [chunk["text"] for chunk in chunks]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = generate_embeddings(texts, model)

    saved_count = save_chunks(chunks, embeddings)

    print(f"Done! Stored {saved_count} chunks in ChromaDB.")

    return saved_count


if __name__ == "__main__":
    ingest_documents("data/sample_documents")