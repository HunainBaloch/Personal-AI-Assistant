# Quick Start Guide 🚀

Get up and running in 5 minutes!

## Prerequisites Check ✓

```bash
# 1. Check Python version (need 3.9+)
python --version

# 2. Check if Ollama is installed
ollama --version

# 3. If Ollama is installed, pull required models
ollama pull mxbai-embed-large
ollama pull deepseek-r1:1.5b
```

## Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Verify directory structure was created
ls -la _intake data
```

## First Run (with sample data)

### Option A: Use Sample Data (for testing)

```bash
# 1. Create a sample conversation file
python create_sample_data.py

# 2. Run ingestion
python ingest.py

# 3. Create index
python index.py

# 4. Launch app
streamlit run app.py
```

### Option B: Use Your ChatGPT Data

```bash
# 1. Export your ChatGPT conversations
#    Go to: https://chat.openai.com/settings
#    Data Controls → Export data → Download conversations.json

# 2. Place file in _intake folder
cp ~/Downloads/conversations.json _intake/

# 3. Run ingestion
python ingest.py

# 4. Create index
python index.py

# 5. Launch app
streamlit run app.py
```

## Using the App

1. **Browser opens automatically** at `http://localhost:8501`

2. **Create your first chat**: Click "➕ New Chat" in sidebar

3. **Start chatting**: Type a message and press Enter

4. **Try search**: 
   - Click "🔍 Search"
   - Enter: "conversations about programming"
   - Click "🔎 Search"

## Common Commands

```bash
# Add more conversations (re-run anytime)
python ingest.py

# Update search index
python index.py

# Rebuild index from scratch
python index.py --rebuild

# Show index statistics
python index.py --stats

# Run the app
streamlit run app.py
```

## Troubleshooting

### "Ollama not found"
```bash
# Install from: https://ollama.ai
# Then start the server:
ollama serve
```

### "Model not found"
```bash
ollama pull mxbai-embed-large
ollama pull deepseek-r1:1.5b
```

### "Search not available"
```bash
# Run indexing first
python index.py
```

## Next Steps

- Read the full [README.md](README.md)
- Explore different models in Settings
- Export more ChatGPT conversations
- Try semantic search with different queries

---

**Questions?** Check the main README.md or troubleshooting section.

