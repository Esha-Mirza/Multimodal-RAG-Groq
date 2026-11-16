
from app.services.rag_service import ask_question

question = "What does computer vision allow machines to do?"

result = ask_question(
    question=question,
    n_results=3
)

print("\nUSER QUESTION:")
print(result["question"])

print("\nGENERATED ANSWER:")
print(result["answer"])

print("\nSOURCE REFERENCES:")

for source in result["sources"]:
    print("\nSource:", source["source"])
    print("Chunk:", source["chunk_index"])
    print("Text:", source["text"])
