from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from langchain_community.vectorstores.utils import DistanceStrategy 
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia import NVIDIAEmbeddings
from config import Config

class VectorDatabase:
    def __init__(self):
        self.api_key = Config.NVIDIA_API_KEY
        self.base_url = Config.NVIDIA_BASE_URL
        self.model_embedding = Config.NVIDIA_MODEL_EMBEDDING
        self.collection_name = "user_docs"
        self.vector_size = 2048
        self.embeddings = NVIDIAEmbeddings(
            model=self.model_embedding,
            nvidia_api_key=self.api_key,
            base_url=self.base_url
        )
        self.client = QdrantClient("./data/qdrant")
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size, 
                    distance=Distance.COSINE
                )
            )
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(
            documents=documents
        )
        
        

