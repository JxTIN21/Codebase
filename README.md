# 🔍 Codebase Search & Explainer

> A powerful web application that enables intelligent codebase exploration through natural language search and AI-powered explanations.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18%2B-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

- **🚀 Multi-Language Support**: Upload codebases in Python, JavaScript, Java, C++, TypeScript, and 15+ more languages
- **🧠 Natural Language Search**: Query your code using plain English instead of complex regex patterns
- **🤖 AI-Powered Explanations**: Get intelligent explanations for functions, classes, and code patterns
- **👀 Interactive Code Preview**: View syntax-highlighted code snippets with context
- **📋 One-Click Copy**: Copy code snippets directly to your clipboard
- **💡 Smart Suggestions**: Receive search tips and query suggestions
- **⚡ Fast Vector Search**: Powered by ChromaDB for lightning-fast semantic search
- **🎯 Contextual Results**: Find relevant code even when exact keywords don't match

## 🏗️ Architecture

```
project-root/
├── backend/                  # FastAPI backend service
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── .env                 # Environment variables (create from .env.example)
│   ├── services/            # Core business logic
│   │   ├── code_parser.py   # Code parsing and chunking
│   │   ├── embeddings.py    # Vector embeddings generation
│   │   └── search.py        # Search and retrieval logic
│   ├── models/              # Data models and schemas
│   │   ├── codebase.py      # Codebase data structures
│   │   └── search.py        # Search request/response models
│   ├── uploads/             # Temporary file storage
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── CodeViewer.jsx       # Syntax-highlighted code display
│   │   │   ├── LoadingSpinner.jsx   # Loading states
│   │   │   ├── ResultsDisplay.jsx   # Search results layout
│   │   │   ├── SearchInterface.jsx  # Search input and controls
│   │   │   └── CodebaseUpload.jsx   # File upload interface
│   │   ├── hooks/           # Custom React hooks
│   │   │   └── useCodebaseSearch.js # Search state management
│   │   ├── services/        # API communication
│   │   │   └── api.js       # Backend API client
│   │   └── App.jsx          # Main application component
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .env.example             # Environment variables template
├── .gitignore
├── docker-compose.yml       # Docker setup (optional)
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **GROQ API Key** (get one at [console.groq.com](https://console.groq.com))

### 1. Clone & Setup

```bash
git clone <repository-url>
cd codebase-search-explainer
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Linux/MacOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Setup environment variables
cp .env.example backend/.env
# Edit backend/.env with your API keys
```

**Environment Configuration (`backend/.env`):**
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
CHROMA_PERSIST_DIR=./chroma_db
DEBUG=true
MAX_FILE_SIZE_MB=10
SUPPORTED_EXTENSIONS=.py,.js,.jsx,.ts,.tsx,.java,.cpp,.c,.h,.cs,.php,.rb,.go,.rs,.swift,.kt,.html,.css,.sql,.json,.yaml,.yml,.md,.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Start the Application

**Terminal 1 (Backend):**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

🎉 **Access the application at** `http://localhost:3000`

## 📖 Usage Guide

### Uploading a Codebase

1. Navigate to the **Upload** tab
2. Choose your upload method:
   - **File Upload**: Select individual files or drag & drop
   - **Folder Upload**: Upload entire directories (where supported)
   - **Text Input**: Paste code directly

### Searching Your Code

Use natural language queries to find what you're looking for:

#### Example Queries

| What you want to find | Query example |
|----------------------|---------------|
| Authentication logic | `"How does user authentication work?"` |
| Database connections | `"Show me database connection setup"` |
| API endpoints | `"Where are the REST API routes defined?"` |
| Error handling | `"How are errors handled in this codebase?"` |
| Configuration | `"Where are configuration settings stored?"` |
| Utility functions | `"Show me helper functions for data validation"` |

### Understanding Results

Each search result includes:
- **📄 File Path**: Location of the relevant code
- **🔍 Relevance Score**: How well it matches your query
- **🤖 AI Explanation**: Context and explanation of the code
- **💻 Code Preview**: Syntax-highlighted code snippet
- **📋 Copy Button**: One-click copying to clipboard

## 🛠️ Advanced Configuration

### Supported File Types

| Language | Extensions |
|----------|------------|
| Python | `.py` |
| JavaScript/TypeScript | `.js`, `.jsx`, `.ts`, `.tsx` |
| Java | `.java` |
| C/C++ | `.c`, `.cpp`, `.h` |
| C# | `.cs` |
| PHP | `.php` |
| Ruby | `.rb` |
| Go | `.go` |
| Rust | `.rs` |
| Swift | `.swift` |
| Kotlin | `.kt` |
| Web | `.html`, `.css` |
| Data | `.sql`, `.json`, `.yaml`, `.yml` |
| Documentation | `.md`, `.txt` |

### Customization Options

Edit `backend/config.py` to adjust:

- **Chunk Size**: How code is split for processing
- **Search Results Limit**: Maximum results returned
- **Embedding Model**: Vector embedding configuration
- **File Size Limits**: Maximum upload sizes

## 🐳 Docker Deployment

For containerized deployment:

```bash
# Build and start services
docker-compose up -d

# Access the application
open http://localhost:3000
```

## 🔧 Troubleshooting

### Common Issues

**Backend won't start:**
- ✅ Check Python version (3.8+ required)
- ✅ Verify all environment variables are set
- ✅ Ensure GROQ API key is valid

**Search returns no results:**
- ✅ Confirm files were uploaded successfully
- ✅ Try different query phrasings
- ✅ Check file extensions are supported

**Upload fails:**
- ✅ Verify file size is under 10MB per file
- ✅ Check file extension is supported
- ✅ Ensure sufficient disk space

### Performance Tips

- **Large Codebases**: Consider uploading in smaller chunks
- **Search Speed**: More specific queries return faster results
- **Memory Usage**: Restart the backend periodically for large uploads

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r backend/requirements-dev.txt
cd frontend && npm install --include=dev

# Run tests
pytest backend/tests/
npm test --prefix frontend
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend
- [ChromaDB](https://www.trychroma.com/) for vector search
- [GROQ](https://groq.com/) for AI-powered explanations

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](../../issues)
- 💡 **Feature Requests**: [Start a discussion](../../discussions)
- 📧 **Contact**: [your-email@domain.com](mailto:your-email@domain.com)

---

**⭐ If this project helped you, please consider giving it a star!**