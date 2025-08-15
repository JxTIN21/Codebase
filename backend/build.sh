#!/usr/bin/env bash
# build.sh

set -o errexit  # exit on error

# Force install setuptools first
python -m pip install --upgrade pip
python -m pip install --no-build-isolation setuptools>=68.0.0 wheel>=0.40.0

# Install dependencies one by one to avoid build issues
python -m pip install --no-build-isolation fastapi==0.104.1
python -m pip install --no-build-isolation uvicorn==0.24.0
python -m pip install --no-build-isolation python-multipart==0.0.6
python -m pip install --no-build-isolation python-dotenv==1.0.0
python -m pip install --no-build-isolation pydantic==2.5.0
python -m pip install --no-build-isolation aiofiles==23.2.1
python -m pip install --no-build-isolation groq==0.4.1

# Install the more complex packages
python -m pip install numpy==1.24.3
python -m pip install torch==2.1.2
python -m pip install transformers==4.36.2
python -m pip install sentence-transformers==2.2.2
python -m pip install "huggingface_hub<=0.19.4"
python -m pip install langchain
python -m pip install langchain-community==0.0.38
python -m pip install chromadb==0.4.18