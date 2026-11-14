
from FlagEmbedding import BGEM3FlagModel

# Load the BGE-M3 model
model = BGEM3FlagModel(
    "BAAI/bge-m3",
    use_fp16=False
)


def generate_embeddings(texts):

    results = model.encode(
        texts,
        batch_size=2,
        max_length=8192)

    embeddings = results["dense_vecs"]

    return embeddings.tolist()
