import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from rag import answer_question


question = "How many annual leave days does a full-time employee receive?"

result = answer_question(question)

print("\nSTATUS:")
print(result["status"])

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print(source)

print("\nCONFLICT DETECTED:")
print(result["conflict_detected"])