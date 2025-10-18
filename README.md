# 🧠 Personal AI Assistant with Conversation Search

<div align="center">

**A powerful, privacy-focused AI conversation archive and search engine**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Python](https://img.shields.io/badge/code%20style-python-blue.svg)](https://www.python.org/)

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## 📖 Overview

Personal AI Assistant is a **100% local, privacy-first** application that allows you to:
- 💬 **Chat with AI models** running locally on your machine
- 🔍 **Search through your entire ChatGPT conversation history** using semantic search
- 📚 **Archive and organize** all your AI conversations in one place
- 🔐 **Maintain complete privacy** - no data leaves your computer

Unlike cloud-based solutions, everything runs on your machine: the AI models, the vector database, and all your data. You have complete control and ownership.

---

## ✨ Features

### 🗨️ Multi-Session Chat Interface
- Create and manage unlimited chat sessions
- Switch between conversations seamlessly
- Auto-generate intelligent chat titles using AI
- Persistent storage of all chat history
- Support for multiple Ollama models (Llama3, DeepSeek, Mistral, etc.)

### 🔍 Semantic Conversation Search
- **Vector-based semantic search** through all imported conversations
- Find conversations by meaning, not just keywords
- **AI-powered reranking** for more relevant results
- **Automatic summarization** of search results
- Adjustable result count (3-20 results)
- Similarity scoring for each result

### 📥 Conversation Import & Management
- Import ChatGPT conversation exports (JSON format)
- Automatic deduplication prevents duplicate imports
- Support for nested ChatGPT conversation structures
- Archive system for processed files
- Easy to extend for other platforms (Gemini, Claude, Grok)

### 🔐 Privacy & Security
- ✅ **100% Local Processing** - No external API calls
- ✅ **No Data Transmission** - Everything stays on your machine
- ✅ **Open Source** - Fully auditable code
- ✅ **No Telemetry** - No tracking or analytics
- ✅ **Complete Data Ownership** - You control everything

### ⚡ Performance & Scalability
- Efficient JSONL storage format
- Incremental indexing (only new conversations)
- Batch processing for large datasets
- Fast vector similarity search with ChromaDB
- Tested with 1000+ conversations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)                │
│  ┌──────────────────┐              ┌──────────────────┐     │
│  │   Chat Mode 💬   │              │  Search Mode 🔍  │     │
│  │ • Multi-session  │              │ • Semantic       │     │
│  │ • Auto-title     │              │ • Reranking      │     │
│  │ • Model select   │              │ • Summarization  │     │
│  └──────────────────┘              └──────────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                   APPLICATION LAYER                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ChatManager │  │ConvSearcher│  │ConvIndexer │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    SERVICE LAYER                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Ollama   │  │  ChromaDB  │  │ LangChain  │            │
│  │   (LLMs)   │  │  (Vector)  │  │(Orchestr.) │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  chats.json  │  │master.jsonl  │  │ chroma_db/   │      │
│  │ (Your chats) │  │(All convos)  │  │(Embeddings)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

Get up and running in 5 minutes!

### Prerequisites

1. **Python 3.9+** - [Download here](https://www.python.org/downloads/)
2. **Ollama** - [Download here](https://ollama.ai)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Personal-AI-Assistant.git
cd Personal-AI-Assistant

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install required Ollama models
ollama pull mxbai-embed-large
ollama pull deepseek-r1:1.5b
```

### First Run with Sample Data

```bash
# 1. Generate sample conversations
python create_sample_data.py

# 2. Import conversations
python ingest.py

# 3. Create searchable index
python index.py

# 4. Launch the application
streamlit run app.py
```

The app will open automatically at `http://localhost:8501` 🎉

---

## 📥 Importing Your ChatGPT History

### Step 1: Export from ChatGPT
1. Go to [ChatGPT Settings](https://chat.openai.com/settings)
2. Navigate to **Data Controls**
3. Click **Export data**
4. Download the `conversations.json` file

### Step 2: Import into the App
```bash
# 1. Place the file in the _intake directory
cp ~/Downloads/conversations.json _intake/

# 2. Run the ingestion pipeline
python ingest.py

# 3. Index the conversations
python index.py

# 4. Launch the app
streamlit run app.py
```

---

## 💡 Usage

### Chat Mode 💬

1. **Create a new chat**: Click "➕ New Chat" in the sidebar
2. **Select a model**: Choose from available Ollama models
3. **Start chatting**: Type your message and press Enter
4. **Auto-titling**: First message automatically generates a title
5. **Manage chats**: Rename, switch between, or delete chats

### Search Mode 🔍

1. **Toggle search**: Click "🔍 Search" in the sidebar
2. **Enter your query**: Type what you're looking for
3. **Configure options**:
   - Adjust number of results (3-20)
   - Enable AI reranking for better relevance
   - Enable summarization for quick overview
4. **View results**: Expandable cards show matching conversations
5. **See similarity**: Each result shows a relevance score

### Example Search Queries

```
"How do I deploy a Python app to production?"
"Conversations about machine learning"
"React component optimization"
"What did I learn about Docker?"
"Security best practices"
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | [Streamlit](https://streamlit.io) | Beautiful web interface |
| **LLM Runtime** | [Ollama](https://ollama.ai) | Local AI model execution |
| **LLM Framework** | [LangChain](https://python.langchain.com) | AI orchestration |
| **Vector Database** | [ChromaDB](https://www.trychroma.com) | Semantic search |
| **Embeddings** | mxbai-embed-large | Text-to-vector conversion |
| **Data Processing** | Pandas | Data manipulation |
| **Storage** | JSON/JSONL | Persistent data storage |

---

## 📁 Project Structure

```
Personal-AI-Assistant/
│
├── 📄 Core Application
│   ├── app.py                  # Main Streamlit application
│   ├── ingest.py              # Conversation import pipeline
│   └── index.py               # Vector database indexing
│
├── 📄 Helper Scripts
│   ├── create_sample_data.py  # Generate test data
│   ├── check_setup.py         # Verify installation
│   ├── run.bat                # Windows launcher
│   └── run.sh                 # Linux/Mac launcher
│
├── 📄 Configuration
│   ├── requirements.txt       # Python dependencies
│   └── .gitignore            # Git ignore rules
│
├── 📄 Documentation
│   ├── README.md             # This file
│   ├── QUICKSTART.md         # Quick start guide
│   ├── INSTALLATION.md       # Detailed installation
│   ├── ARCHITECTURE.md       # System architecture
│   └── PROJECT_STRUCTURE.md  # Project layout
│
├── 📁 _intake/               # Drop conversation exports here
│   └── processed/            # Archived processed files
│
└── 📁 data/                  # Generated data (auto-created)
    ├── master_conversations.jsonl  # All conversations
    ├── chroma_db/                  # Vector embeddings
    └── chats.json                  # Your chat sessions
```

---

## 🔧 Advanced Usage

### Rebuild Search Index

If you need to completely rebuild the vector index:

```bash
python index.py --rebuild
```

### View Index Statistics

```bash
python index.py --stats
```

### Check Setup

Verify your installation and configuration:

```bash
python check_setup.py
```

### Use Different Models

Edit the model selection in the app sidebar or modify `app.py`:

```python
# Available models (must be installed via Ollama)
- deepseek-r1:1.5b    # Fast, lightweight
- llama3.1           # Balanced performance
- llama3.2           # Latest version
- mistral            # Alternative option
- codellama          # Code-focused
```

Install new models:
```bash
ollama pull llama3.1
ollama pull mistral
```

---

## 🐛 Troubleshooting

### Ollama Connection Error

**Problem**: `Could not connect to Ollama`

**Solution**:
```bash
# Check if Ollama is running
ollama serve

# In another terminal, verify models
ollama list
```

### Model Not Found

**Problem**: `Model 'xxx' not found`

**Solution**:
```bash
# Pull the required models
ollama pull mxbai-embed-large
ollama pull deepseek-r1:1.5b
```

### Search Not Available

**Problem**: `Search is not available`

**Solution**:
```bash
# Run indexing first
python index.py
```

### Import Errors

**Problem**: `No conversations found to ingest`

**Solution**:
- Ensure `conversations.json` is in the `_intake/` directory
- Check file format (should be ChatGPT export format)
- Try generating sample data: `python create_sample_data.py`

---

## 🗺️ Roadmap

### Current Features ✅
- ✅ ChatGPT conversation import
- ✅ Semantic search with vector embeddings
- ✅ Multi-session chat interface
- ✅ Auto-titling with AI
- ✅ Result reranking and summarization
- ✅ Multiple model support

### Planned Features 🚧
- [ ] Support for other platforms (Gemini, Claude, Grok)
- [ ] Conversation export functionality
- [ ] Advanced filtering (date ranges, platforms)
- [ ] Analytics dashboard
- [ ] Tagging and categorization system
- [ ] Conversation RAG (use past conversations as context)
- [ ] Batch conversation analysis
- [ ] Custom embedding models
- [ ] Multi-language support
- [ ] Dark mode toggle

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Areas for Contribution
- 🌐 Add parsers for other AI platforms (Gemini, Claude, etc.)
- 🎨 UI/UX improvements
- 📊 Analytics and visualization features
- 🌍 Internationalization
- 📝 Documentation improvements
- 🐛 Bug fixes
- ✨ New features

---

## 📋 Requirements

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 5-20GB (depending on models)
- **CPU**: Modern multi-core processor (GPU optional but beneficial)

### Software Requirements
- Python 3.9 or higher
- Ollama (latest version)
- 5GB+ free disk space for models

---

## 🔒 Privacy & Security

This application is designed with privacy as a top priority:

- **No External API Calls**: All processing happens locally
- **No Data Collection**: We don't collect any usage data or telemetry
- **No Internet Required**: Works completely offline (after models are downloaded)
- **Open Source**: Full code transparency - audit it yourself
- **Local Storage**: All data stored on your machine
- **No Tracking**: No analytics, no cookies, no tracking pixels

### Data Storage Locations

- **Conversations**: `data/master_conversations.jsonl`
- **Vector Index**: `data/chroma_db/`
- **Chat Sessions**: `data/chats.json`
- **Processed Files**: `_intake/processed/`

You can backup, export, or delete any of these at any time.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Personal AI Assistant Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

This project is built on the shoulders of giants:

- **[Ollama](https://ollama.ai)** - For making local LLMs accessible
- **[Streamlit](https://streamlit.io)** - For the amazing web framework
- **[LangChain](https://python.langchain.com)** - For LLM orchestration
- **[ChromaDB](https://www.trychroma.com)** - For vector database capabilities
- **The Open Source Community** - For countless libraries and tools

Special thanks to:
- OpenAI for ChatGPT and the conversation export feature
- The Ollama team for local AI democratization
- All contributors and users of this project

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/Personal-AI-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Personal-AI-Assistant/discussions)
- **Documentation**: Check the `/docs` directory for detailed guides

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

It helps others discover the project and motivates continued development.

---

## 📊 Project Status

![Status](https://img.shields.io/badge/status-active-success.svg)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**Current Version**: 1.0.0  
**Last Updated**: October 2024  
**Status**: Production Ready ✅

---

<div align="center">

**Built with ❤️ for AI enthusiasts who value privacy and control**

[⬆ Back to Top](#-personal-ai-assistant-with-conversation-search)

</div>
