from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import asyncio
import logging
from pathlib import Path
import uuid

from models.codebase import CodebaseCreate, CodebaseResponse
from models.search import SearchRequest, SearchResponse, RelevantFile, CodeExample
from services.file_parser import FileParserService
from services.vector_db import VectorDBService
from services.llm_service import LLMService
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
file_parser = FileParserService()
vector_db = VectorDBService()
llm_service = LLMService()

# In-memory storage for codebase processing status
codebase_status = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting up application...")
    await vector_db.initialize()
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    # Add any cleanup code here if needed
    # For example: await vector_db.close()
    logger.info("Application shutdown complete")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Codebase Search & Explainer API",
    description="RAG-based API for searching and explaining codebases",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-codebase", response_model=CodebaseResponse)
async def upload_codebase(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    """Upload and process codebase files"""
    try:
        # Generate unique codebase ID
        codebase_id = str(uuid.uuid4())
        
        # Validate files
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        valid_files = []
        for file in files:
            if file.size > MAX_FILE_SIZE:
                logger.warning(f"File {file.filename} exceeds size limit")
                continue
                
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in SUPPORTED_EXTENSIONS:
                logger.warning(f"File {file.filename} has unsupported extension")
                continue
                
            valid_files.append(file)
        
        if not valid_files:
            raise HTTPException(
                status_code=400, 
                detail="No valid files found. Supported extensions: " + 
                       ", ".join(SUPPORTED_EXTENSIONS)
            )
        
        # Initialize processing status
        codebase_status[codebase_id] = {
            "status": "processing",
            "total_files": len(valid_files),
            "processed_files": 0,
            "message": "Starting file processing..."
        }
        
        # Start background processing
        background_tasks.add_task(
            process_codebase_files, 
            codebase_id, 
            valid_files
        )
        
        return CodebaseResponse(
            codebase_id=codebase_id,
            status="processing",
            files_processed=0,
            total_files=len(valid_files),
            message="Codebase upload started. Processing in background."
        )
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

async def process_codebase_files(codebase_id: str, files: List[UploadFile]):
    """Background task to process uploaded files"""
    try:
        codebase_status[codebase_id]["message"] = "Parsing files..."
        
        # Parse files
        documents = []
        processed_count = 0
        
        for file in files:
            try:
                # Read file content
                content = await file.read()
                
                # Parse file
                parsed_docs = await file_parser.parse_file(
                    filename=file.filename,
                    content=content,
                    codebase_id=codebase_id
                )
                
                documents.extend(parsed_docs)
                processed_count += 1
                
                # Update status
                codebase_status[codebase_id].update({
                    "processed_files": processed_count,
                    "message": f"Processed {processed_count}/{len(files)} files..."
                })
                
            except Exception as e:
                logger.error(f"Failed to parse file {file.filename}: {str(e)}")
                continue
        
        if not documents:
            codebase_status[codebase_id].update({
                "status": "error",
                "message": "No documents could be processed"
            })
            return
        
        # Store in vector database
        codebase_status[codebase_id]["message"] = "Creating embeddings..."
        await vector_db.add_documents(codebase_id, documents)
        
        # Update final status
        codebase_status[codebase_id].update({
            "status": "completed",
            "processed_files": processed_count,
            "message": f"Successfully processed {processed_count} files"
        })
        
        logger.info(f"Codebase {codebase_id} processed successfully")
        
    except Exception as e:
        logger.error(f"Background processing failed: {str(e)}")
        codebase_status[codebase_id].update({
            "status": "error",
            "message": f"Processing failed: {str(e)}"
        })

@app.get("/api/codebase/{codebase_id}/status")
async def get_codebase_status(codebase_id: str):
    """Get processing status of a codebase"""
    if codebase_id not in codebase_status:
        raise HTTPException(status_code=404, detail="Codebase not found")
    
    return codebase_status[codebase_id]

@app.post("/api/search", response_model=SearchResponse)
async def search_codebase(request: SearchRequest):
    """Search codebase and get AI explanation"""
    try:
        # Add debugging
        logger.info(f"Received search request for codebase_id: {request.codebase_id}")
        logger.info(f"Available codebases: {list(codebase_status.keys())}")
        
        # Validate codebase exists and is ready
        if request.codebase_id not in codebase_status:
            logger.error(f"Codebase {request.codebase_id} not found in status dict")
            raise HTTPException(status_code=404, detail="Codebase not found")
        
        status = codebase_status[request.codebase_id]
        logger.info(f"Codebase status: {status}")
        
        if status["status"] != "completed":
            raise HTTPException(
                status_code=400, 
                detail=f"Codebase is not ready. Status: {status['status']}"
            )
        
        # Perform vector search
        search_results = await vector_db.search(
            codebase_id=request.codebase_id,
            query=request.query,
            k=MAX_SEARCH_RESULTS
        )
        
        if not search_results:
            return SearchResponse(
                query=request.query,
                explanation="No relevant code found for your query.",
                relevant_files=[],
                code_examples=[]
            )
        
        # Generate AI explanation
        explanation = await llm_service.generate_explanation(
            query=request.query,
            search_results=search_results
        )
        
        # Extract relevant files with proper RelevantFile model structure
        relevant_files = []
        for result in search_results:
            relevant_file = RelevantFile(
                file_path=result.metadata.get("file_path", "Unknown"),
                relevance_score=result.metadata.get("score", 0.0),
                snippet=result.page_content[:500] + "..." if len(result.page_content) > 500 else result.page_content,
                content=result.page_content
            )
            relevant_files.append(relevant_file)
        
        # Generate code examples with proper CodeExample model structure
        code_examples_data = await llm_service.extract_code_examples(
            query=request.query,
            search_results=search_results
        )
        
        # Convert to CodeExample objects if llm_service returns dict/raw data
        code_examples = []
        if code_examples_data:
            for example in code_examples_data:
                if isinstance(example, dict):
                    code_example = CodeExample(
                        title=example.get("title", "Code Example"),
                        code=example.get("code", ""),
                        explanation=example.get("explanation"),
                        file_path=example.get("file_path")
                    )
                else:
                    # If it's just a string, create a simple example
                    code_example = CodeExample(
                        title="Code Example",
                        code=str(example),
                        explanation=None,
                        file_path=None
                    )
                code_examples.append(code_example)
        
        return SearchResponse(
            query=request.query,
            explanation=explanation,
            relevant_files=relevant_files,
            code_examples=code_examples
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Add debugging endpoint
@app.get("/api/debug/codebases")
async def list_codebases():
    """Debug endpoint to list all codebases and their status"""
    return {
        "codebases": codebase_status,
        "total_count": len(codebase_status)
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Codebase Search API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )