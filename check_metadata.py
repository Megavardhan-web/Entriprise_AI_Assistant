from ingestion.loader import load_document

docs = load_document("data/sample_documents/HR_Policy_v2.txt")

print(docs[0]["metadata"])