import asyncio
import logging
from typing import List, Dict, Any
from groq import Groq
from langchain_core.documents import Document

from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
    
    async def generate_explanation(
        self, 
        query: str, 
        search_results: List[Document]
    ) -> str:
        """Generate AI explanation based on search results"""
        try:
            # Prepare context from search results
            context_parts = []
            for i, doc in enumerate(search_results[:5]):  # Limit to top 5 results
                file_path = doc.metadata.get("file_path", "Unknown")
                content = doc.page_content[:800]  # Limit content length
                context_parts.append(f"File: {file_path}\n{content}\n---")
            
            context = "\n".join(context_parts)
            
            system_prompt = """You are a senior software engineer helping developers understand their codebase. 
You will be given a query about a codebase and relevant code snippets. 
Your task is to provide a clear, comprehensive explanation that answers the query.

Guidelines:
1. Be specific and technical when appropriate
2. Reference specific files and code patterns
3. Explain the "why" behind implementation choices
4. If you see architectural patterns, mention them
5. Keep explanations practical and actionable
6. If the code shows security considerations, highlight them
7. Format your response clearly with proper structure
8. Be concise but thorough"""
            
            user_prompt = f"""Query: {query}

Relevant Code:
{context}

Please provide a comprehensive explanation that answers the query based on the provided code snippets."""
            
            # Make async call to Groq
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Failed to generate explanation: {str(e)}")
            return f"Failed to generate explanation: {str(e)}. Please try again."
    
    async def extract_code_examples(
        self, 
        query: str, 
        search_results: List[Document]
    ) -> List[Dict[str, Any]]:
        """Extract relevant code examples from search results"""
        try:
            code_examples = []
            
            # Look for specific code patterns
            for doc in search_results[:3]:
                content = doc.page_content
                file_path = doc.metadata.get("file_path", "")
                
                # Try to extract meaningful code blocks
                if self._looks_like_function(content):
                    # Use Groq to generate a better explanation for this code
                    explanation = await self._generate_code_explanation(content, query)
                    
                    example = {
                        "title": f"Code from {file_path}",
                        "code": content[:500],
                        "file_path": file_path,
                        "explanation": explanation
                    }
                    code_examples.append(example)
            
            return code_examples[:3]  # Limit to 3 examples
            
        except Exception as e:
            logger.error(f"Failed to extract code examples: {str(e)}")
            return []
    
    async def _generate_code_explanation(self, code: str, query: str) -> str:
        """Generate explanation for a specific code snippet"""
        try:
            prompt = f"""Explain this code snippet in the context of the query: "{query}"

Code:
{code[:400]}

Provide a brief, technical explanation of what this code does and how it relates to the query."""

            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Failed to generate code explanation: {str(e)}")
            return f"Code section from file"
    
    def _looks_like_function(self, content: str) -> bool:
        """Check if content contains function-like code"""
        function_indicators = [
            'def ', 'function ', 'const ', 'class ', 'public ', 'private ',
            'async ', 'export ', 'import ', '=>', '{', '}'
        ]
        return any(indicator in content for indicator in function_indicators)