import asyncio
import logging
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import json

from config import *

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self):
        # Use free local embeddings instead of OpenAI
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.client = None
        self.vectorstores = {}
    
    async def initialize(self):
        """Initialize ChromaDB client"""
        try:
            self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
            logger.info("ChromaDB initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            raise
    
    def _clean_metadata(self, metadata):
        """Clean metadata to ensure all values are simple types (str, int, float, bool)"""
        if not metadata:
            return {}
            
        cleaned = {}
        
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                # Simple types are fine as-is
                cleaned[key] = value
            elif isinstance(value, list):
                # Convert lists to comma-separated strings
                if all(isinstance(item, (str, int, float)) for item in value):
                    cleaned[key] = ", ".join(str(item) for item in value)
                else:
                    # If complex list, convert to JSON string (truncated if too long)
                    json_str = json.dumps(value)
                    cleaned[key] = json_str[:500] + "..." if len(json_str) > 500 else json_str
            elif isinstance(value, dict):
                # Convert dictionaries to JSON strings (truncated if too long)
                json_str = json.dumps(value)
                cleaned[key] = json_str[:500] + "..." if len(json_str) > 500 else json_str
            elif value is None:
                # Skip None values
                continue
            else:
                # Convert other types to strings
                cleaned[key] = str(value)[:1000]  # Limit string length
                
        return cleaned
    
    def _clean_documents(self, documents: List[Document]) -> List[Document]:
        """Clean all documents' metadata"""
        cleaned_documents = []
        
        for doc in documents:
            try:
                # Create a new document with cleaned metadata
                cleaned_metadata = self._clean_metadata(doc.metadata) if doc.metadata else {}
                
                cleaned_doc = Document(
                    page_content=doc.page_content,
                    metadata=cleaned_metadata
                )
                
                cleaned_documents.append(cleaned_doc)
                
            except Exception as e:
                logger.warning(f"Failed to clean document metadata: {e}")
                # If cleaning fails, create a document with minimal metadata
                minimal_doc = Document(
                    page_content=doc.page_content,
                    metadata={"file_path": str(doc.metadata.get("file_path", "unknown"))}
                )
                cleaned_documents.append(minimal_doc)
        
        return cleaned_documents
    
    async def add_documents(self, codebase_id: str, documents: List[Document]):
        """Add documents to vector database with cleaned metadata"""
        try:
            if not documents:
                return
            
            # Clean all documents' metadata first
            logger.info(f"Cleaning metadata for {len(documents)} documents...")
            cleaned_documents = self._clean_documents(documents)
            
            # Create collection name for this codebase
            collection_name = f"{COLLECTION_NAME}_{codebase_id}"
            
            # Create vectorstore
            vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=CHROMA_PERSIST_DIR
            )
            
            # Add documents in batches
            batch_size = 50
            for i in range(0, len(cleaned_documents), batch_size):
                batch = cleaned_documents[i:i + batch_size]
                await asyncio.to_thread(vectorstore.add_documents, batch)
                logger.info(f"Added batch {i//batch_size + 1}/{(len(cleaned_documents)-1)//batch_size + 1} for codebase {codebase_id}")
            
            # Persist the vectorstore
            await asyncio.to_thread(vectorstore.persist)
            
            # Store reference
            self.vectorstores[codebase_id] = vectorstore
            
            logger.info(f"Successfully added {len(cleaned_documents)} documents to codebase {codebase_id}")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            raise
    
    async def search(
        self, 
        codebase_id: str, 
        query: str, 
        k: int = 10
    ) -> List[Document]:
        """Search for relevant documents"""
        try:
            # Get or create vectorstore
            vectorstore = self.vectorstores.get(codebase_id)
            if not vectorstore:
                collection_name = f"{COLLECTION_NAME}_{codebase_id}"
                vectorstore = Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=CHROMA_PERSIST_DIR
                )
                self.vectorstores[codebase_id] = vectorstore
            
            # Perform similarity search
            results = await asyncio.to_thread(
                vectorstore.similarity_search_with_score, 
                query, 
                k=k
            )
            
            # Add score to metadata and filter by threshold
            documents = []
            for doc, score in results:
                doc.metadata["score"] = score
                if score < 1.5:  # ChromaDB uses distance, lower is better
                    documents.append(doc)
            
            logger.info(f"Found {len(documents)} relevant documents for query: {query}")
            return documents
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise
    
    async def delete_codebase(self, codebase_id: str):
        """Delete codebase from vector database"""
        try:
            collection_name = f"{COLLECTION_NAME}_{codebase_id}"
            
            if self.client:
                self.client.delete_collection(collection_name)
            
            if codebase_id in self.vectorstores:
                del self.vectorstores[codebase_id]
            
            logger.info(f"Deleted codebase {codebase_id}")
            
        except Exception as e:
            logger.error(f"Failed to delete codebase: {str(e)}")