import requests
import json
import time

BASE_URL = "http://localhost:8000"  # Adjust port if different

def test_debug():
    """Test the debug endpoint to see available codebases"""
    try:
        response = requests.get(f"{BASE_URL}/api/debug/codebases")
        print(f"Debug Response Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Available Codebases: {json.dumps(data, indent=2)}")
            return data.get("codebases", {})
        else:
            print(f"Debug endpoint failed: {response.text}")
            return {}
    except Exception as e:
        print(f"Error calling debug endpoint: {e}")
        return {}

def test_search_with_existing_codebase():
    """Test search with any existing codebase"""
    codebases = test_debug()
    
    if not codebases:
        print("No codebases found. Upload one first.")
        return
    
    # Get the first available codebase
    codebase_id = list(codebases.keys())[0]
    codebase_info = codebases[codebase_id]
    
    print(f"\nTesting with codebase: {codebase_id}")
    print(f"Status: {codebase_info}")
    
    if codebase_info.get("status") != "completed":
        print("Codebase is not ready for search")
        return
    
    # Test search
    search_payload = {
        "codebase_id": codebase_id,
        "query": "function"
    }
    
    print(f"\nSending search request: {json.dumps(search_payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/search",
            json=search_payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Search Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Search successful!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Search failed: {response.text}")
            
    except Exception as e:
        print(f"Error during search: {e}")

def test_upload_and_search():
    """Upload a simple file and test search"""
    print("Testing upload...")
    
    # Create a simple test file
    test_content = """
def hello_world():
    '''A simple greeting function'''
    print("Hello, World!")
    return "Hello, World!"

class Calculator:
    '''A simple calculator class'''
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
"""
    
    files = [
        ("files", ("test_code.py", test_content, "text/plain"))
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/api/upload-codebase", files=files)
        print(f"Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            codebase_id = data.get("codebase_id")
            print(f"Codebase ID: {codebase_id}")
            
            # Wait for processing
            print("Waiting for processing to complete...")
            max_wait = 30  # seconds
            waited = 0
            
            while waited < max_wait:
                status_response = requests.get(f"{BASE_URL}/api/codebase/{codebase_id}/status")
                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"Status: {status}")
                    
                    if status.get("status") == "completed":
                        print("Processing completed! Testing search...")
                        
                        # Now test search
                        search_payload = {
                            "codebase_id": codebase_id,
                            "query": "hello world function"
                        }
                        
                        search_response = requests.post(
                            f"{BASE_URL}/api/search",
                            json=search_payload,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        print(f"Search Status: {search_response.status_code}")
                        if search_response.status_code == 200:
                            print("Search successful!")
                            result = search_response.json()
                            print(f"Explanation: {result.get('explanation', 'No explanation')}")
                            print(f"Files found: {len(result.get('relevant_files', []))}")
                        else:
                            print(f"Search failed: {search_response.text}")
                        break
                        
                    elif status.get("status") == "error":
                        print("Processing failed!")
                        break
                
                time.sleep(2)
                waited += 2
            
            if waited >= max_wait:
                print("Timeout waiting for processing to complete")
                
        else:
            print(f"Upload failed: {response.text}")
            
    except Exception as e:
        print(f"Error during upload/search test: {e}")

if __name__ == "__main__":
    print("=== Testing Codebase Search API ===")
    
    # First, check what's already available
    print("\n1. Checking existing codebases...")
    test_search_with_existing_codebase()
    
    # Then test a fresh upload
    print("\n2. Testing fresh upload and search...")
    test_upload_and_search()