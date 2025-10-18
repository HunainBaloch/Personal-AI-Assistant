"""
Setup Verification Script
Checks if all prerequisites and dependencies are properly installed
"""

import sys
import subprocess
from pathlib import Path
import importlib


def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def check_python_version():
    """Check if Python version is 3.9+"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro}")
        print(f"   ⚠️  Python 3.9+ required")
        return False


def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✅ {package_name} ({version})")
        return True
    except ImportError:
        print(f"   ❌ {package_name} - Not installed")
        return False


def check_python_packages():
    """Check if all required Python packages are installed"""
    print("\n📦 Checking Python packages...")
    
    packages = [
        ('streamlit', 'streamlit'),
        ('langchain', 'langchain'),
        ('chromadb', 'chromadb'),
        ('ollama', 'ollama'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
    ]
    
    all_installed = True
    for package, import_name in packages:
        if not check_package(package, import_name):
            all_installed = False
    
    return all_installed


def check_ollama():
    """Check if Ollama is installed and running"""
    print("\n🦙 Checking Ollama...")
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(
            ['ollama', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ Ollama installed ({version})")
        else:
            print(f"   ❌ Ollama not found")
            return False
    except FileNotFoundError:
        print(f"   ❌ Ollama not found")
        print(f"   💡 Install from: https://ollama.ai")
        return False
    except Exception as e:
        print(f"   ⚠️  Error checking Ollama: {e}")
        return False
    
    # Check if required models are available
    print("\n🤖 Checking Ollama models...")
    required_models = [
        'mxbai-embed-large',
        'deepseek-r1:1.5b'
    ]
    
    all_models_available = True
    
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        available_models = result.stdout.lower()
        
        for model in required_models:
            if model.lower() in available_models:
                print(f"   ✅ {model}")
            else:
                print(f"   ❌ {model} - Not found")
                print(f"      Run: ollama pull {model}")
                all_models_available = False
    
    except Exception as e:
        print(f"   ⚠️  Error checking models: {e}")
        all_models_available = False
    
    return all_models_available


def check_directory_structure():
    """Check if required directories exist"""
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        '_intake',
        '_intake/processed',
        'data'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ⚠️  {dir_path}/ - Will be created automatically")
    
    return True


def check_data_files():
    """Check if data files exist"""
    print("\n💾 Checking data files...")
    
    master_file = Path("data/master_conversations.jsonl")
    chroma_db = Path("data/chroma_db")
    chats_file = Path("data/chats.json")
    
    has_data = False
    
    if master_file.exists():
        # Count lines
        with open(master_file, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        print(f"   ✅ master_conversations.jsonl ({line_count} conversations)")
        has_data = True
    else:
        print(f"   ⚠️  master_conversations.jsonl - Not found (run ingest.py)")
    
    if chroma_db.exists():
        print(f"   ✅ chroma_db/ - Vector database exists")
        has_data = True
    else:
        print(f"   ⚠️  chroma_db/ - Not found (run index.py)")
    
    if chats_file.exists():
        print(f"   ✅ chats.json - Chat history exists")
    else:
        print(f"   ℹ️  chats.json - Will be created on first use")
    
    return has_data


def main():
    """Run all checks"""
    print_header("🧠 AI Personal Assistant - Setup Verification")
    
    results = {
        'python': check_python_version(),
        'packages': check_python_packages(),
        'ollama': check_ollama(),
        'directories': check_directory_structure(),
        'data': check_data_files()
    }
    
    # Summary
    print_header("📊 Summary")
    
    if results['python'] and results['packages'] and results['ollama']:
        print("\n✅ All prerequisites are installed!")
        
        if results['data']:
            print("\n🎉 You're ready to go!")
            print("\n💡 Next step: Run the app")
            print("   streamlit run app.py")
        else:
            print("\n⚠️  No data found. Follow these steps:")
            print("\n   1. Get your ChatGPT conversations:")
            print("      • Go to https://chat.openai.com/settings")
            print("      • Export your data")
            print("      • Download conversations.json")
            print("\n   2. OR create sample data for testing:")
            print("      python create_sample_data.py")
            print("\n   3. Run ingestion:")
            print("      python ingest.py")
            print("\n   4. Create search index:")
            print("      python index.py")
            print("\n   5. Launch the app:")
            print("      streamlit run app.py")
    else:
        print("\n⚠️  Some prerequisites are missing. Please fix the issues above.")
        
        if not results['python']:
            print("\n   📥 Install Python 3.9+: https://python.org")
        
        if not results['packages']:
            print("\n   📦 Install Python packages:")
            print("      pip install -r requirements.txt")
        
        if not results['ollama']:
            print("\n   🦙 Install Ollama: https://ollama.ai")
            print("      Then pull required models:")
            print("      ollama pull mxbai-embed-large")
            print("      ollama pull deepseek-r1:1.5b")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()

