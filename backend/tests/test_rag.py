
from app.services.rag_service import ask_question


question = "How do computers learn patterns from data?"

result = ask_question(question)

print("\nUSER QUESTION:")
print(result["question"])

print("\nGENERATED ANSWER:")
print(result["answer"])

print("\nRETRIEVED SOURCES:")

for source in result["sources"]:

    print("\nSource:", source["source"])
    print("Chunk:", source["chunk_index"])
    print("Text:", source["text"])
