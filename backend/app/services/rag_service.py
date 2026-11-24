
from app.services.retrieval_service import search_chunks
from app.services.generation_service import generate_answer


def ask_question(question, n_results=3, source=None):

    retrieved_chunks = search_chunks(
        query=question,
        n_results=n_results,
        source=source
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

        optional_fields = [
            "page_number",
            "content_type",
            "image_number",
            "block_index"
        ]

        for field in optional_fields:

            if field in metadata:
                source_info[field] = metadata[field]

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
