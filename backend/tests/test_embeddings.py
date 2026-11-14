
from app.services.embedding_service import generate_embeddings

sample_texts = [
    "Artificial intelligence enables machines to perform intelligent tasks.",
    "Machine learning allows computers to learn patterns from data.",
    "Pakistan is located in South Asia."
]

embeddings = generate_embeddings(sample_texts)

print("Total embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))
print("First embedding:", embeddings[0][:10])
