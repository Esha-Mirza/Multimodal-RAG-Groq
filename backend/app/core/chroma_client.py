
import chromadb
from app.core.config import CHROMA_DB_PATH

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

documents_collection = chroma_client.get_or_create_collection(
    name="multimodal_documents",
    embedding_function=None
)
