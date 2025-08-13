import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

# Database Configuration
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = "codebase_collection"

# Embedding Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Free local embedding model

# LLM Configuration
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # Options: llama3-8b-8192, mixtral-8x7b-32768, gemma-7b-it

# File Processing Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB per file
SUPPORTED_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', 
    '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.html', 
    '.css', '.sql', '.json', '.yaml', '.yml', '.md', '.txt'
}

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Search Configuration
MAX_SEARCH_RESULTS = 10
SIMILARITY_THRESHOLD = 0.7

# Upload Configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
DEBUG = os.getenv("DEBUG", "false").lower() == "true"