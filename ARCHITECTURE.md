# System Architecture 🏗️

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI PERSONAL ASSISTANT                        │
│                  with Conversation Search 🧠                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                                                                  │
│  ┌──────────────────┐              ┌──────────────────┐         │
│  │   Chat Mode 💬   │              │  Search Mode 🔍  │         │
│  │                  │              │                  │         │
│  │ • Multi-chat     │              │ • Semantic       │         │
│  │ • Auto-title     │              │ • Reranking      │         │
│  │ • Model select   │              │ • Summarization  │         │
│  │ • Persistent     │              │ • Filtering      │         │
│  └──────────────────┘              └──────────────────┘         │
│                                                                  │
│                      [Streamlit Web UI]                          │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ ChatManager  │  │ConvSearcher  │  │ ConvIndexer  │          │
│  │              │  │              │  │              │          │
│  │ • Create     │  │ • Search     │  │ • Embed      │          │
│  │ • Rename     │  │ • Rerank     │  │ • Chunk      │          │
│  │ • Delete     │  │ • Summarize  │  │ • Index      │          │
│  │ • Switch     │  │ • Filter     │  │ • Update     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │  Ollama    │  │ ChromaDB   │  │ LangChain  │                │
│  │            │  │            │  │            │                │
│  │ • LLMs     │  │ • Vectors  │  │ • Prompts  │                │
│  │ • Embed    │  │ • Search   │  │ • Chains   │                │
│  │ • Local    │  │ • Store    │  │ • Memory   │                │
│  └────────────┘  └────────────┘  └────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   chats.json │  │ master.jsonl │  │  chroma_db/  │          │
│  │              │  │              │  │              │          │
│  │ User chats   │  │ All convos   │  │ Vector store │          │
│  │ Sessions     │  │ Normalized   │  │ Embeddings   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────┐
│ ChatGPT Export  │
│ (conversations  │
│     .json)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         INGESTION PIPELINE              │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  ConversationIngester           │   │
│  │                                 │   │
│  │  1. Load JSON file              │   │
│  │  2. Parse ChatGPT structure     │   │
│  │  3. Extract messages            │   │
│  │  4. Check for duplicates        │   │
│  │  5. Normalize format            │   │
│  │  6. Append to JSONL             │   │
│  │  7. Archive original            │   │
│  └─────────────────────────────────┘   │
│                                         │
│         ingest.py                       │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌────────────────────┐
         │ master_             │
         │ conversations.jsonl│
         │                    │
         │ • Normalized       │
         │ • One per line     │
         │ • Deduplicated     │
         └─────────┬──────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         INDEXING PIPELINE               │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  ConversationIndexer            │   │
│  │                                 │   │
│  │  1. Load conversations          │   │
│  │  2. Create chunks               │   │
│  │     • Full conversation         │   │
│  │     • Individual messages       │   │
│  │  3. Generate embeddings         │   │
│  │  4. Store in ChromaDB           │   │
│  │  5. Update statistics           │   │
│  └─────────────────────────────────┘   │
│                                         │
│         index.py                        │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌────────────────────┐
         │    chroma_db/      │
         │                    │
         │ • Vector index     │
         │ • Metadata         │
         │ • Fast search      │
         └─────────┬──────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│        WEB APPLICATION                  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Search Mode                    │   │
│  │                                 │   │
│  │  1. User enters query           │   │
│  │  2. Generate query embedding    │   │
│  │  3. Search ChromaDB             │   │
│  │  4. Retrieve top matches        │   │
│  │  5. (Optional) Rerank with LLM  │   │
│  │  6. (Optional) Summarize        │   │
│  │  7. Display results             │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Chat Mode                      │   │
│  │                                 │   │
│  │  1. User sends message          │   │
│  │  2. Add to conversation context │   │
│  │  3. Send to Ollama LLM          │   │
│  │  4. Get response                │   │
│  │  5. Display & save              │   │
│  │  6. (Auto-title if first msg)   │   │
│  └─────────────────────────────────┘   │
│                                         │
│         app.py                          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌────────────────────┐
         │    chats.json      │
         │                    │
         │ • All chats        │
         │ • Messages         │
         │ • Metadata         │
         └────────────────────┘
```

## Component Architecture

### 1. Ingestion Module (ingest.py)

```
ConversationIngester
│
├── __init__()
│   ├── Set paths (_intake/, data/)
│   ├── Create directories
│   └── Load existing IDs
│
├── _load_existing_ids()
│   └── Read master.jsonl for deduplication
│
├── parse_chatgpt_export()
│   ├── Load JSON file
│   ├── For each conversation:
│   │   ├── Extract metadata
│   │   ├── Parse mapping structure
│   │   ├── Extract messages
│   │   ├── Check duplicates
│   │   └── Create normalized record
│   └── Return records
│
├── _extract_messages_from_mapping()
│   ├── Traverse nested structure
│   ├── Extract role and content
│   ├── Sort by timestamp
│   └── Return messages
│
├── save_records()
│   └── Append to JSONL
│
├── archive_processed_file()
│   └── Move to processed/
│
└── process_all()
    ├── Find JSON files
    ├── Process each file
    └── Report statistics
```

### 2. Indexing Module (index.py)

```
ConversationIndexer
│
├── __init__()
│   ├── Initialize Ollama embeddings
│   ├── Initialize ChromaDB client
│   └── Get/create collection
│
├── load_conversations()
│   └── Read master.jsonl
│
├── create_searchable_chunks()
│   ├── Chunk 1: Full conversation
│   │   └── Title + all messages
│   └── Chunk 2-N: Individual messages
│       └── Title + context + message
│
├── index_conversations()
│   ├── Create chunks for all conversations
│   ├── Filter already-indexed
│   ├── Batch process (50 at a time):
│   │   ├── Generate embeddings
│   │   └── Add to ChromaDB
│   └── Report statistics
│
├── rebuild_index()
│   ├── Delete collection
│   ├── Create new collection
│   └── Index all conversations
│
└── get_stats()
    └── Display index statistics
```

### 3. Web Application (app.py)

```
ChatManager
│
├── __init__()
│   └── Load chats.json
│
├── create_chat()
│   ├── Generate unique ID
│   ├── Create chat record
│   └── Save to storage
│
├── get_current_chat()
│   └── Return active chat
│
├── switch_chat()
│   └── Change current_chat_id
│
├── rename_chat()
│   └── Update title
│
├── delete_chat()
│   ├── Remove chat
│   └── Switch to another
│
├── add_message()
│   ├── Append message
│   └── Update timestamp
│
└── auto_title_chat()
    ├── Get first message
    ├── Generate title with LLM
    └── Update chat

ConversationSearcher
│
├── __init__()
│   ├── Initialize embeddings
│   └── Connect to ChromaDB
│
├── search()
│   ├── Generate query embedding
│   ├── Query ChromaDB
│   ├── Format results
│   └── Calculate similarity
│
├── rerank_results()
│   ├── Create reranking prompt
│   ├── Ask LLM to reorder
│   └── Return reranked list
│
└── summarize_results()
    ├── Combine top results
    ├── Create summary prompt
    └── Generate summary with LLM

Streamlit UI
│
├── Sidebar
│   ├── Model selection
│   ├── New chat button
│   ├── Search toggle
│   ├── Chat list
│   └── Statistics
│
├── Main Area (Chat Mode)
│   ├── Chat title
│   ├── Message display
│   ├── Chat input
│   └── Rename button
│
└── Main Area (Search Mode)
    ├── Search input
    ├── Configuration
    ├── Search button
    ├── Summary (optional)
    └── Results list
```

## Data Models

### Conversation Record (JSONL)

```json
{
  "conversation_id": "unique_string",
  "title": "Conversation Title",
  "platform": "chatgpt",
  "created_at": "2024-10-14T10:30:00",
  "updated_at": "2024-10-14T10:35:00",
  "messages": [
    {
      "role": "user|assistant",
      "content": "Message text",
      "timestamp": "2024-10-14T10:30:00"
    }
  ],
  "metadata": {
    "message_count": 2,
    "imported_at": "2024-10-14T12:00:00"
  }
}
```

### Chat Session (JSON)

```json
{
  "current_chat_id": "chat_20241014_120000",
  "chats": {
    "chat_20241014_120000": {
      "id": "chat_20241014_120000",
      "title": "Chat Title",
      "created_at": "2024-10-14T12:00:00",
      "updated_at": "2024-10-14T12:05:00",
      "messages": [...],
      "auto_titled": true
    }
  }
}
```

### Search Result

```python
{
  "id": "conv_id_chunk_0",
  "text": "Full chunk text",
  "metadata": {
    "type": "full_conversation|message",
    "conversation_id": "conv_id",
    "title": "Title",
    "platform": "chatgpt",
    "created_at": "2024-10-14T10:30:00",
    "message_index": 0,
    "role": "user|assistant"
  },
  "distance": 0.15,
  "similarity": 0.85
}
```

## External Dependencies

```
┌─────────────────────────────────────────┐
│              OLLAMA                     │
│                                         │
│  Models:                                │
│  ┌────────────────────────────────┐    │
│  │ mxbai-embed-large              │    │
│  │ • Embedding generation         │    │
│  │ • 1024-dim vectors             │    │
│  └────────────────────────────────┘    │
│                                         │
│  ┌────────────────────────────────┐    │
│  │ deepseek-r1:1.5b               │    │
│  │ • Fast chat model              │    │
│  │ • Low resource usage           │    │
│  └────────────────────────────────┘    │
│                                         │
│  ┌────────────────────────────────┐    │
│  │ llama3.1 / llama3.2            │    │
│  │ • Advanced chat models         │    │
│  │ • Better quality               │    │
│  └────────────────────────────────┘    │
│                                         │
│  API: HTTP (localhost:11434)           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│            CHROMADB                     │
│                                         │
│  Collections:                           │
│  ┌────────────────────────────────┐    │
│  │ conversations                  │    │
│  │ • Embeddings                   │    │
│  │ • Metadata                     │    │
│  │ • Documents                    │    │
│  └────────────────────────────────┘    │
│                                         │
│  Storage: Persistent (data/chroma_db)  │
│  Search: Cosine similarity (HNSW)      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           LANGCHAIN                     │
│                                         │
│  Components:                            │
│  • OllamaEmbeddings                    │
│  • Ollama LLM                          │
│  • ChatPromptTemplate                  │
│  • Message types                       │
│                                         │
│  Purpose: LLM orchestration            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           STREAMLIT                     │
│                                         │
│  Features:                              │
│  • Web server                          │
│  • UI components                       │
│  • Session state                       │
│  • File uploads                        │
│                                         │
│  Port: 8501 (default)                  │
└─────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│         SECURITY LAYERS                 │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  LOCAL-ONLY PROCESSING         │    │
│  │  • No external API calls       │    │
│  │  • No data transmission        │    │
│  │  • Ollama runs locally         │    │
│  └────────────────────────────────┘    │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  DATA OWNERSHIP                │    │
│  │  • All files on disk           │    │
│  │  • User controls everything    │    │
│  │  • Easy backup                 │    │
│  └────────────────────────────────┘    │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  PRIVACY BY DESIGN             │    │
│  │  • No telemetry                │    │
│  │  • No tracking                 │    │
│  │  • No analytics                │    │
│  └────────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

## Scalability Considerations

### Current Limits
- **Conversations**: No hard limit (tested with 1000+)
- **Messages per conversation**: No hard limit
- **Search results**: 3-20 (configurable)
- **Concurrent chats**: Unlimited

### Performance Optimization
- **Batch processing**: 50 chunks at a time
- **Incremental indexing**: Only new data
- **JSONL format**: Append-only, efficient
- **Vector index**: HNSW for fast search

### Storage Requirements
- **Per conversation**: ~1-2KB (JSONL)
- **Per chunk**: ~10-50KB (ChromaDB)
- **Models**: 1-10GB (Ollama)

### Bottlenecks
1. **Embedding generation**: Limited by Ollama speed
2. **LLM inference**: Model size vs speed tradeoff
3. **Disk I/O**: JSONL append operations
4. **Memory**: Model loading and ChromaDB

---

## Design Principles

1. **Local-First**: All processing happens locally
2. **Privacy-Focused**: No external data transmission
3. **Modular**: Clear separation of concerns
4. **Extensible**: Easy to add new features
5. **User-Friendly**: Simple installation and usage
6. **Well-Documented**: Comprehensive documentation
7. **Production-Ready**: Error handling and validation
8. **Efficient**: Batch processing and incremental updates

---

This architecture provides a **robust, scalable, and privacy-focused** solution for AI conversation management and search. 🏗️

