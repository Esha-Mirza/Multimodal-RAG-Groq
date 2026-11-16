
from app.services.retrieval_service import search_chunks
from app.services.generation_service import generate_answer


def ask_question(question, n_results=3):

    retrieved_chunks = search_chunks(
        query=question,
        n_results=n_results
    )

    if not retrieved_chunks:
        return {
            "question": question,
            "answer": "No relevant documents were found.",
            "sources": []
        }

    context = ""
    sources = []

    for index, result in enumerate(retrieved_chunks):

        metadata = result["metadata"]

        context += f"""
Source {index + 1}:
{result["text"]}
"""

        source_info = {
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "text": result["text"]
        }

        if "page_number" in metadata:
            source_info["page_number"] = metadata["page_number"]

        sources.append(source_info)

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
