import chromadb
import hashlib


DB_PATH = "chroma_db"
COLLECTION_NAME = "enterprise_docs"


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


def make_chunk_id(chunk):
    source = chunk["metadata"].get("source", "unknown")
    page = chunk["metadata"].get("page", 1)
    chunk_index = chunk["metadata"].get("chunk_index", 0)

    raw_id = f"{source}-{page}-{chunk_index}"
    return hashlib.md5(raw_id.encode()).hexdigest()


def save_chunks(chunks, embeddings):
    collection = get_collection()

    ids = [make_chunk_id(chunk) for chunk in chunks]
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return len(chunks)