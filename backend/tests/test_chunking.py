
from app.services.text_processor import split_text

sample_text = """
Retrieval Augmented Generation (RAG) is an AI technique.
It combines information retrieval with language generation.
A RAG system retrieves relevant information from a knowledge
base and provides it to a language model as context.
This helps the model generate more relevant and grounded answers.
"""

chunks = split_text(sample_text,chunk_size=100,overlap=20)

for i, chunk in enumerate(chunks):
    print(f"\nCHUNK {i + 1}")
    print(chunk)
    print("Characters:", len(chunk))

print("\nTotal chunks:", len(chunks))
