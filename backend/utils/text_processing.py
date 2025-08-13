import re
import logging
from typing import List, Tuple, Dict, Any

logger = logging.getLogger(__name__)

def clean_code(content: str) -> str:
    """Clean and normalize code content"""
    # Remove excessive whitespace while preserving structure
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove trailing whitespace
        cleaned_line = line.rstrip()
        cleaned_lines.append(cleaned_line)
    
    # Remove excessive empty lines (max 2 consecutive)
    result_lines = []
    empty_count = 0
    
    for line in cleaned_lines:
        if line.strip() == '':
            empty_count += 1
            if empty_count <= 2:
                result_lines.append(line)
        else:
            empty_count = 0
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def extract_functions_and_classes(content: str, file_ext: str) -> Tuple[List[str], List[str]]:
    """Extract function and class names from code"""
    functions = []
    classes = []
    
    try:
        if file_ext == '.py':
            functions, classes = _extract_python_structures(content)
        elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
            functions, classes = _extract_javascript_structures(content)
        elif file_ext == '.java':
            functions, classes = _extract_java_structures(content)
        elif file_ext in ['.cpp', '.c', '.h']:
            functions, classes = _extract_cpp_structures(content)
    except Exception as e:
        logger.warning(f"Failed to extract structures from {file_ext}: {str(e)}")
    
    return functions, classes

def _extract_python_structures(content: str) -> Tuple[List[str], List[str]]:
    """Extract Python functions and classes"""
    functions = []
    classes = []
    
    # Function pattern: def function_name(
    func_pattern = r'^[ \t]*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    for match in re.finditer(func_pattern, content, re.MULTILINE):
        functions.append(match.group(1))
    
    # Class pattern: class ClassName(
    class_pattern = r'^[ \t]*class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    for match in re.finditer(class_pattern, content, re.MULTILINE):
        classes.append(match.group(1))
    
    return functions, classes

def _extract_javascript_structures(content: str) -> Tuple[List[str], List[str]]:
    """Extract JavaScript/TypeScript functions and classes"""
    functions = []
    classes = []
    
    # Function patterns
    patterns = [
        r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
        r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s+)?\(',
        r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?:async\s+)?function',
        r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*=>'
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            functions.append(match.group(1))
    
    # Class pattern
    class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    for match in re.finditer(class_pattern, content):
        classes.append(match.group(1))
    
    return functions, classes

def _extract_java_structures(content: str) -> Tuple[List[str], List[str]]:
    """Extract Java functions and classes"""
    functions = []
    classes = []
    
    # Method pattern (simplified)
    method_pattern = r'(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    for match in re.finditer(method_pattern, content):
        method_name = match.group(1)
        if method_name not in ['if', 'for', 'while', 'switch']:  # Filter out keywords
            functions.append(method_name)
    
    # Class pattern
    class_pattern = r'(?:public|private|protected|\s)*class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    for match in re.finditer(class_pattern, content):
        classes.append(match.group(1))
    
    return functions, classes

def _extract_cpp_structures(content: str) -> Tuple[List[str], List[str]]:
    """Extract C++ functions and classes"""
    functions = []
    classes = []
    
    # Function pattern (simplified)
    func_pattern = r'^\s*(?:[\w:*&<>]+\s+)*([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*[{;]'
    for match in re.finditer(func_pattern, content, re.MULTILINE):
        func_name = match.group(1)
        if func_name not in ['if', 'for', 'while', 'switch', 'return']:
            functions.append(func_name)
    
    # Class pattern
    class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    for match in re.finditer(class_pattern, content):
        classes.append(match.group(1))
    
    return functions, classes

def extract_key_terms(content: str) -> List[str]:
    """Extract key technical terms from code"""
    # Common technical terms and patterns
    terms = set()
    
    # API/HTTP terms
    api_patterns = [
        r'@app\.route', r'@router\.', r'app\.get|post|put|delete',
        r'fetch\(', r'axios\.|requests\.', r'HttpClient',
        r'REST|GraphQL|API', r'endpoint', r'middleware'
    ]
    
    # Database terms
    db_patterns = [
        r'SELECT|INSERT|UPDATE|DELETE', r'FROM\s+\w+',
        r'mongoose\.|sequelize\.', r'db\.|database\.',
        r'collection\.|query\.|find\('
    ]
    
    # Authentication/Security terms
    auth_patterns = [
        r'authenticate|authorization|login|logout',
        r'password|hash|bcrypt|jwt|token',
        r'session|cookie|csrf'
    ]
    
    all_patterns = api_patterns + db_patterns + auth_patterns
    
    for pattern in all_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        terms.update(matches)
    
    return list(terms)[:20]  # Limit to top 20 terms