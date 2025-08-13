import asyncio
import logging
from typing import List
from langchain.embeddings import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts"""
        try:
            embeddings = await asyncio.to_thread(
                self.embeddings.embed_documents, 
                texts
            )
            return embeddings
        except Exception as e:
            logger.error(f"Failed to create embeddings: {str(e)}")
            raise
    
    async def create_query_embedding(self, query: str) -> List[float]:
        """Create embedding for a single query"""
        try:
            embedding = await asyncio.to_thread(
                self.embeddings.embed_query, 
                query
            )
            return embedding
        except Exception as e:
            logger.error(f"Failed to create query embedding: {str(e)}")
            raise