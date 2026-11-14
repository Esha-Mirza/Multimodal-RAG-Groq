
from app.services.retrieval_service import search_chunks
from app.services.generation_service import generate_answer


def ask_question(question, n_results=3):

    # Retrieve relevant chunks from ChromaDB
    retrieved_chunks = search_chunks(
        query=question,
        n_results=n_results
    )

    # Handle an empty database
    if not retrieved_chunks:
        return {
            "question": question,
            "answer": "No relevant documents were found.",
            "sources": []
        }

    # Prepare context for the Groq model
    context = ""

    sources = []

    for index, result in enumerate(retrieved_chunks):

        context += f"""
Source {index + 1}:
{result["text"]}
"""

        sources.append({
            "source": result["metadata"]["source"],
            "chunk_index": result["metadata"]["chunk_index"],
            "text": result["text"]
        })

    # Generate an answer using the retrieved context
    answer = generate_answer(
        question=question,
        context=context)

    return {
        "question": question,
        "answer": answer,
        "sources": sources}
