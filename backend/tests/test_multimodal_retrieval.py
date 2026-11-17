
from app.services.rag_service import ask_question


question = "What are the eligibility requirements and minimum GPA for the Financial Assistance Scholarship?"

print("\nMULTIMODAL RAG TEST")
print("-------------------")

try:

    result = ask_question(
        question=question,
        n_results=5
    )

    print("\nQUESTION:")
    print(result["question"])

    print("\nGENERATED ANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:

        print("\nSource:", source["source"])
        print("Page:", source.get("page_number"))
        print("Content type:", source.get("content_type", "unknown"))

except Exception as error:

    print("\nERROR:")
    print(error)
