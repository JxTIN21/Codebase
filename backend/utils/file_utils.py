import os
import shutil
import logging
from pathlib import Path
from typing import List, Set

logger = logging.getLogger(__name__)

def get_supported_files(directory: Path, extensions: Set[str]) -> List[Path]:
    """Recursively get all supported files from directory"""
    supported_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
            'node_modules', '__pycache__', 'build', 'dist', 'target',
            '.git', '.svn', '.hg', 'venv', 'env', '.env'
        }]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = Path(root) / file
            if file_path.suffix.lower() in extensions:
                supported_files.append(file_path)
    
    return supported_files

def clean_filename(filename: str) -> str:
    """Clean filename for safe storage"""
    import re
    # Remove or replace unsafe characters
    cleaned = re.sub(r'[<>:"|?*]', '_', filename)
    cleaned = cleaned.replace('\\', '/')
    return cleaned

def ensure_directory(path: Path) -> None:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)

def cleanup_temp_files(temp_dir: Path) -> None:
    """Clean up temporary files"""
    try:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temp directory: {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to cleanup temp directory {temp_dir}: {str(e)}")

def get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB"""
    return file_path.stat().st_size / (1024 * 1024)

def is_binary_file(file_path: Path) -> bool:
    """Check if file is binary"""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except Exception:
        return True