# Project Structure 📁

## Directory Layout

```
ai-personal-assistant/
│
├── 📄 Core Application Files
│   ├── app.py                          # Main Streamlit web application
│   ├── ingest.py                       # Data ingestion pipeline
│   ├── index.py                        # Vector database indexing
│   └── check_setup.py                  # Setup verification script
│
├── 📄 Helper Scripts
│   ├── create_sample_data.py           # Generate sample conversations
│   ├── run.bat                         # Windows launch script
│   └── run.sh                          # Linux/Mac launch script
│
├── 📄 Configuration & Dependencies
│   ├── requirements.txt                # Python dependencies
│   └── .gitignore                      # Git ignore rules
│
├── 📄 Documentation
│   ├── README.md                       # Complete documentation
│   ├── QUICKSTART.md                   # Quick start guide
│   └── PROJECT_STRUCTURE.md            # This file
│
├── 📁 _intake/                         # Input directory for conversation files
│   ├── conversations.json              # (Place ChatGPT exports here)
│   └── processed/                      # Archived processed files
│
└── 📁 data/                            # Generated data (created automatically)
    ├── master_conversations.jsonl      # Normalized conversation database
    ├── chroma_db/                      # Vector embeddings for search
    └── chats.json                      # Your chat sessions
```

## File Descriptions

### Core Application Files

#### `app.py` (Web Application)
- **Purpose**: Main Streamlit interface
- **Features**:
  - Multi-chat management
  - Semantic conversation search
  - AI chat interface
  - Model selection
  - Auto-titling
  - Persistent storage
- **Dependencies**: Streamlit, LangChain, ChromaDB, Ollama
- **Usage**: `streamlit run app.py`

#### `ingest.py` (Data Ingestion)
- **Purpose**: Process conversation exports
- **Features**:
  - Parse ChatGPT JSON format
  - Deduplicate conversations
  - Normalize to JSONL format
  - Archive processed files
- **Input**: `_intake/*.json`
- **Output**: `data/master_conversations.jsonl`
- **Usage**: `python ingest.py`

#### `index.py` (Vector Indexing)
- **Purpose**: Create searchable embeddings
- **Features**:
  - Generate vector embeddings
  - Create searchable chunks
  - ChromaDB storage
  - Incremental updates
- **Input**: `data/master_conversations.jsonl`
- **Output**: `data/chroma_db/`
- **Usage**: 
  - `python index.py` - Index new conversations
  - `python index.py --rebuild` - Rebuild entire index
  - `python index.py --stats` - Show statistics

### Helper Scripts

#### `create_sample_data.py`
- **Purpose**: Generate sample conversations for testing
- **Output**: `_intake/sample_conversations.json`
- **Usage**: `python create_sample_data.py`
- **Sample Topics**:
  - Python programming
  - Neural networks
  - REST API design
  - Data science with pandas

#### `check_setup.py`
- **Purpose**: Verify installation and prerequisites
- **Checks**:
  - Python version (3.9+)
  - Required Python packages
  - Ollama installation
  - Ollama models
  - Directory structure
  - Data files
- **Usage**: `python check_setup.py`

#### `run.bat` / `run.sh`
- **Purpose**: One-click launch scripts
- **Features**:
  - Auto-create virtual environment
  - Auto-install dependencies
  - Launch Streamlit app
- **Usage**: 
  - Windows: `run.bat`
  - Linux/Mac: `./run.sh`

### Data Directories

#### `_intake/`
- **Purpose**: Input folder for conversation exports
- **Contents**:
  - Drop `conversations.json` files here
  - Files are automatically processed by `ingest.py`
- **Subdirectories**:
  - `processed/` - Archived files with timestamps

#### `data/`
- **Purpose**: Generated data storage
- **Files**:
  - `master_conversations.jsonl` - All conversations in normalized format
  - `chats.json` - Your chat sessions from the app
- **Subdirectories**:
  - `chroma_db/` - Vector database for semantic search

## Data Flow

```
ChatGPT Export
     ↓
conversations.json
     ↓
_intake/
     ↓
[ingest.py] → Parses & Normalizes
     ↓
data/master_conversations.jsonl
     ↓
[index.py] → Creates Embeddings
     ↓
data/chroma_db/
     ↓
[app.py] → Search & Chat
```

## Technology Stack

### Python Packages
- **streamlit**: Web interface
- **langchain**: LLM orchestration
- **langchain-community**: Community integrations
- **chromadb**: Vector database
- **ollama**: Local LLM client
- **pandas**: Data processing
- **numpy**: Numerical operations

### External Dependencies
- **Ollama**: Local LLM runtime
  - Models: `mxbai-embed-large`, `deepseek-r1:1.5b`

## Storage Format Details

### master_conversations.jsonl
Each line is a JSON object:
```json
{
  "conversation_id": "unique_id",
  "title": "Conversation Title",
  "platform": "chatgpt",
  "created_at": "2024-10-14T10:30:00",
  "updated_at": "2024-10-14T10:35:00",
  "messages": [
    {
      "role": "user",
      "content": "Message text",
      "timestamp": "2024-10-14T10:30:00"
    },
    {
      "role": "assistant",
      "content": "Response text",
      "timestamp": "2024-10-14T10:30:05"
    }
  ],
  "metadata": {
    "message_count": 2,
    "imported_at": "2024-10-14T12:00:00"
  }
}
```

### chats.json
```json
{
  "current_chat_id": "chat_20241014_120000",
  "chats": {
    "chat_20241014_120000": {
      "id": "chat_20241014_120000",
      "title": "Chat Title",
      "created_at": "2024-10-14T12:00:00",
      "updated_at": "2024-10-14T12:05:00",
      "messages": [
        {
          "role": "user",
          "content": "Message",
          "timestamp": "2024-10-14T12:00:00"
        }
      ],
      "auto_titled": true
    }
  }
}
```

## Module Architecture

### ChatManager (app.py)
- Manages multiple chat sessions
- Handles CRUD operations on chats
- Persistent storage in `chats.json`
- Auto-titling with LLM

### ConversationSearcher (app.py)
- Semantic search using ChromaDB
- Result reranking with LLM
- Search result summarization
- Similarity scoring

### ConversationIngester (ingest.py)
- File processing and parsing
- Deduplication logic
- Format normalization
- Archive management

### ConversationIndexer (index.py)
- Embedding generation
- Chunk creation strategies
- Batch processing
- Incremental updates

## Extensibility

### Adding New Platforms

To add support for other AI platforms (Gemini, Claude, Grok):

1. **Create parser in `ingest.py`**:
```python
def parse_gemini_export(self, file_path: Path) -> List[Dict]:
    # Parse Gemini format
    # Return normalized records
    pass
```

2. **Update detection logic**:
```python
if "gemini" in file_path.name.lower():
    records = self.parse_gemini_export(file_path)
```

3. **Ensure normalized output format matches**

### Custom Embedding Models

Change in `index.py` and `app.py`:
```python
ConversationIndexer(embedding_model="nomic-embed-text")
ConversationSearcher(embedding_model="nomic-embed-text")
```

### Custom LLM Models

Change in `app.py` sidebar:
```python
model = st.selectbox("Model", ["your-custom-model", "llama3.1"])
```

## Performance Considerations

### Indexing
- Batch size: 50 chunks (configurable)
- Incremental updates: Only new conversations
- Rebuild option: Full reindex when needed

### Search
- Default: 10 results
- Range: 3-20 results
- Optional reranking (adds latency)
- Optional summarization (adds latency)

### Storage
- JSONL format: Append-only, efficient
- ChromaDB: Optimized vector similarity
- Local files: Fast access, no network latency

## Security & Privacy

- ✅ All data stored locally
- ✅ No cloud API calls
- ✅ Ollama runs locally
- ✅ ChromaDB telemetry disabled
- ✅ No external network access required

## Backup Recommendations

### What to Backup
```
data/
├── master_conversations.jsonl  # Your imported conversations
├── chroma_db/                  # Search index (can be rebuilt)
└── chats.json                  # Your new chats
```

### Backup Strategy
- **Critical**: `master_conversations.jsonl`, `chats.json`
- **Rebuildable**: `chroma_db/` (can run `python index.py --rebuild`)
- **Frequency**: After each import or significant chat sessions

