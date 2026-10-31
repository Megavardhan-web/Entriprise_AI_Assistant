from pathlib import Path

from ingestion.loader import load_document
from ingestion.cleaner import clean_documents
from ingestion.chunker import chunk_documents
from ingestion.embeddings import load_embedding_model, generate_embeddings
from ingestion.vector_store import save_chunks


def ingest_documents(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    supported_extensions = {".pdf", ".html", ".htm", ".md", ".txt"}

  
    documents = []

    for file_path in folder.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            print(f"Loading: {file_path.name}")
            documents.extend(load_document(file_path))

    if not documents:
        print("No readable documents found.")
        return 0

    documents = clean_documents(documents)

    # 3. Chunk text
    chunks = chunk_documents(documents)

    if not chunks:
        print("No chunks were created.")
        return 0

    # 4. Generate embeddings
    print("Loading embedding model...")
    model = load_embedding_model()

    texts = [chunk["text"] for chunk in chunks]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = generate_embeddings(texts, model)

    # 5. Save to ChromaDB
    saved_count = save_chunks(chunks, embeddings)

    print(f"Done! Stored {saved_count} chunks in ChromaDB.")
    return saved_count


if __name__ == "__main__":
    ingest_documents("data/sample_documents")