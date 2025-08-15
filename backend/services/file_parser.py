import asyncio
from pathlib import Path
from typing import List, Dict, Any
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from config import CHUNK_SIZE, CHUNK_OVERLAP
from utils.text_processing import clean_code, extract_functions_and_classes

logger = logging.getLogger(__name__)

class FileParserService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    async def parse_file(
        self, 
        filename: str, 
        content: bytes, 
        codebase_id: str
    ) -> List[Document]:
        """Parse a single file and create documents"""
        try:
            # Decode content
            text_content = content.decode('utf-8', errors='ignore')
            
            if not text_content.strip():
                return []
            
            # Clean and process code
            cleaned_content = clean_code(text_content)
            
            # Extract structural information
            file_info = self._extract_file_info(filename, cleaned_content)
            
            # Create chunks
            chunks = self.text_splitter.split_text(cleaned_content)
            
            documents = []
            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                # Create metadata
                metadata = {
                    "file_path": filename,
                    "codebase_id": codebase_id,
                    "chunk_index": i,
                    "file_type": Path(filename).suffix.lower(),
                    "file_size": len(text_content),
                    **file_info
                }
                
                # Create document
                doc = Document(
                    page_content=chunk,
                    metadata=metadata
                )
                documents.append(doc)
            
            logger.info(f"Parsed {filename}: {len(documents)} chunks created")
            return documents
            
        except Exception as e:
            logger.error(f"Failed to parse {filename}: {str(e)}")
            return []
    
    def _extract_file_info(self, filename: str, content: str) -> Dict[str, Any]:
        """Extract structural information from file"""
        file_ext = Path(filename).suffix.lower()
        
        info = {
            "language": self._detect_language(file_ext),
            "functions": [],
            "classes": [],
            "imports": []
        }
        
        # Extract functions and classes based on language
        if file_ext in ['.py', '.js', '.jsx', '.ts', '.tsx']:
            functions, classes = extract_functions_and_classes(content, file_ext)
            info["functions"] = functions
            info["classes"] = classes
        
        # Extract imports/includes
        info["imports"] = self._extract_imports(content, file_ext)
        
        return info
    
    def _detect_language(self, file_ext: str) -> str:
        """Detect programming language from file extension"""
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
        }
        return language_map.get(file_ext, 'text')
    
    def _extract_imports(self, content: str, file_ext: str) -> List[str]:
        """Extract import statements from code"""
        imports = []
        lines = content.split('\n')
        
        for line in lines[:50]:  # Check first 50 lines
            line = line.strip()
            
            if file_ext == '.py':
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
            elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
                if line.startswith('import ') or line.startswith('const ') or line.startswith('require('):
                    imports.append(line)
            elif file_ext == '.java':
                if line.startswith('import '):
                    imports.append(line)
        
        return imports[:10]  # Limit to first 10 imports