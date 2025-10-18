# Installation Guide 🛠️

Complete step-by-step installation instructions for the AI Personal Assistant.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Verification](#verification)
4. [First Run](#first-run)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Python 3.9 or Higher

**Check your Python version:**
```bash
python --version
# or
python3 --version
```

**If you need to install Python:**
- Windows: Download from [python.org](https://www.python.org/downloads/)
- Mac: `brew install python` or download from python.org
- Linux: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### 2. Ollama

Ollama is required for running local AI models.

**Install Ollama:**

1. Go to [ollama.ai](https://ollama.ai)
2. Download for your platform:
   - Windows: Download installer
   - Mac: Download .dmg
   - Linux: `curl https://ollama.ai/install.sh | sh`

**Verify installation:**
```bash
ollama --version
```

**Pull required models:**
```bash
# Embedding model (for search)
ollama pull mxbai-embed-large

# Chat models (choose at least one)
ollama pull deepseek-r1:1.5b
ollama pull llama3.1
```

This may take several minutes depending on your internet connection.

---

## Installation Steps

### Option 1: Automated Setup (Recommended)

#### Windows
```batch
# 1. Double-click run.bat
# or from command prompt:
run.bat
```

#### Linux/Mac
```bash
# 1. Make script executable
chmod +x run.sh

# 2. Run the script
./run.sh
```

The script will:
- Create a virtual environment
- Install all dependencies
- Launch the application

### Option 2: Manual Setup

#### Step 1: Create Virtual Environment (Recommended)

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- streamlit
- langchain
- chromadb
- ollama
- pandas
- numpy
- and other dependencies

#### Step 3: Verify Installation

```bash
python check_setup.py
```

This script checks:
- ✅ Python version
- ✅ All Python packages
- ✅ Ollama installation
- ✅ Required Ollama models
- ✅ Directory structure

---

## Verification

Run the setup verification script:

```bash
python check_setup.py
```

**Expected output:**
```
========================================
  🧠 AI Personal Assistant - Setup Verification
========================================

🐍 Checking Python version...
   ✅ Python 3.11.0

📦 Checking Python packages...
   ✅ streamlit (1.31.0)
   ✅ langchain (0.1.9)
   ✅ chromadb (0.4.22)
   ✅ ollama (0.1.6)
   ✅ pandas (2.2.0)
   ✅ numpy (1.26.3)

🦙 Checking Ollama...
   ✅ Ollama installed (version 0.1.20)

🤖 Checking Ollama models...
   ✅ mxbai-embed-large
   ✅ deepseek-r1:1.5b

📁 Checking directory structure...
   ✅ _intake/
   ✅ _intake/processed/
   ✅ data/

📊 Summary
========================================

✅ All prerequisites are installed!
```

---

## First Run

### Option A: Quick Test with Sample Data

```bash
# 1. Generate sample conversations
python create_sample_data.py

# 2. Ingest the sample data
python ingest.py

# 3. Create search index
python index.py

# 4. Launch the application
streamlit run app.py
```

### Option B: Use Your ChatGPT Data

#### Step 1: Export ChatGPT Conversations

1. Go to [ChatGPT Settings](https://chat.openai.com/settings)
2. Navigate to **Data Controls**
3. Click **Export data**
4. Wait for email (can take a few minutes to hours)
5. Download the ZIP file
6. Extract `conversations.json`

#### Step 2: Place Export File

```bash
# Copy your conversations.json to the _intake folder
# Windows:
copy C:\Users\YourName\Downloads\conversations.json _intake\

# Linux/Mac:
cp ~/Downloads/conversations.json _intake/
```

#### Step 3: Process Data

```bash
# Ingest conversations
python ingest.py
```

**Expected output:**
```
🚀 Starting ingestion process...
📂 Found 1 file(s) to process

📖 Parsing ChatGPT export: conversations.json
  ✅ New conversations: 150
  ⏭️  Duplicates skipped: 0

💾 Saved 150 conversations to data\master_conversations.jsonl
📦 Archived: conversations_20241014_225700.json

✨ Ingestion complete!
```

#### Step 4: Create Search Index

```bash
python index.py
```

**Expected output:**
```
🔧 Initializing embeddings with mxbai-embed-large...
🗄️  Initializing ChromaDB at data/chroma_db...
✅ Collection 'conversations' ready
📚 Loaded 150 conversations

🚀 Starting indexing process...
📊 Processing 150 conversations

✅ Created 1250 searchable chunks
✨ Indexing complete!
```

#### Step 5: Launch Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## Troubleshooting

### Issue: `pip: command not found`

**Solution:**
```bash
# Try pip3 instead
pip3 --version

# Or install pip
python -m ensurepip --upgrade
```

### Issue: `Permission denied` (Linux/Mac)

**Solution:**
```bash
# Add execute permission
chmod +x run.sh

# Or use sudo for installation
sudo pip install -r requirements.txt
```

### Issue: `Ollama: connection refused`

**Solution:**
```bash
# Start Ollama server
ollama serve

# In another terminal, try again
```

### Issue: `Module not found` errors

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: `ChromaDB: database locked`

**Solution:**
```bash
# Close any running instances of the app
# Delete the lock file
rm data/chroma_db/chroma.sqlite3-wal

# Restart the app
```

### Issue: Models download very slowly

**Solution:**
```bash
# Models are large (several GB each)
# Use a stable internet connection
# You can download one at a time:

ollama pull mxbai-embed-large
# Wait for completion, then:
ollama pull deepseek-r1:1.5b
```

### Issue: Streamlit won't start

**Solution:**
```bash
# Check if port 8501 is in use
# Windows:
netstat -ano | findstr :8501

# Linux/Mac:
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

---

## Environment Variables (Optional)

You can customize behavior with environment variables:

```bash
# Change Ollama host (if running remotely)
export OLLAMA_HOST=http://your-server:11434

# Change Streamlit port
export STREAMLIT_SERVER_PORT=8502
```

---

## Updating

To update the project:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Update dependencies
pip install --upgrade -r requirements.txt

# Update Ollama models
ollama pull mxbai-embed-large
ollama pull deepseek-r1:1.5b
```

---

## Uninstallation

To completely remove the project:

```bash
# 1. Deactivate virtual environment
deactivate

# 2. Remove project directory
rm -rf /path/to/ai-personal-assistant  # Linux/Mac
rmdir /s /q "C:\path\to\ai-personal-assistant"  # Windows

# 3. (Optional) Remove Ollama models
ollama rm mxbai-embed-large
ollama rm deepseek-r1:1.5b
```

---

## Next Steps

After successful installation:

1. **Read the [QUICKSTART.md](QUICKSTART.md)** for a fast introduction
2. **Explore the [README.md](README.md)** for complete documentation
3. **Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** to understand the architecture
4. **Start using the app!**

---

## Getting Help

If you're still having issues:

1. Run `python check_setup.py` to diagnose problems
2. Check the error messages carefully
3. Ensure all prerequisites are installed
4. Verify Ollama is running: `ollama list`
5. Check Python version: `python --version`

---

**Happy chatting! 🧠**

