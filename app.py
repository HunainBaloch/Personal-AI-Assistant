"""
AI Personal Assistant with Conversation Search
Streamlit web application for searching and chatting with AI
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage


# Page config
st.set_page_config(
    page_title="AI Personal Assistant 🧠",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


class ChatManager:
    """Manages multiple chat sessions with persistent storage"""
    
    def __init__(self, storage_file: str = "data/chats.json"):
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.chats = self.load_chats()
    
    def load_chats(self) -> Dict:
        """Load all chats from storage"""
        if not self.storage_file.exists():
            return {
                "current_chat_id": None,
                "chats": {}
            }
        
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "current_chat_id": None,
                "chats": {}
            }
    
    def save_chats(self):
        """Save all chats to storage"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.chats, f, indent=2, ensure_ascii=False)
    
    def create_chat(self, title: str = None) -> str:
        """Create a new chat and return its ID"""
        chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.chats["chats"][chat_id] = {
            "id": chat_id,
            "title": title or "New Chat",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
            "auto_titled": False
        }
        
        self.chats["current_chat_id"] = chat_id
        self.save_chats()
        return chat_id
    
    def get_current_chat(self) -> Optional[Dict]:
        """Get the currently active chat"""
        chat_id = self.chats.get("current_chat_id")
        if chat_id and chat_id in self.chats["chats"]:
            return self.chats["chats"][chat_id]
        return None
    
    def get_all_chats(self) -> List[Dict]:
        """Get all chats sorted by update time (most recent first)"""
        chats = list(self.chats["chats"].values())
        chats.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return chats
    
    def switch_chat(self, chat_id: str):
        """Switch to a different chat"""
        if chat_id in self.chats["chats"]:
            self.chats["current_chat_id"] = chat_id
            self.save_chats()
    
    def rename_chat(self, chat_id: str, new_title: str):
        """Rename a chat"""
        if chat_id in self.chats["chats"]:
            self.chats["chats"][chat_id]["title"] = new_title
            self.chats["chats"][chat_id]["updated_at"] = datetime.now().isoformat()
            self.save_chats()
    
    def delete_chat(self, chat_id: str):
        """Delete a chat"""
        if chat_id in self.chats["chats"]:
            del self.chats["chats"][chat_id]
            
            # Switch to another chat or create new one
            if self.chats["current_chat_id"] == chat_id:
                remaining_chats = self.get_all_chats()
                if remaining_chats:
                    self.chats["current_chat_id"] = remaining_chats[0]["id"]
                else:
                    self.chats["current_chat_id"] = None
            
            self.save_chats()
    
    def add_message(self, chat_id: str, role: str, content: str):
        """Add a message to a chat"""
        if chat_id in self.chats["chats"]:
            self.chats["chats"][chat_id]["messages"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            self.chats["chats"][chat_id]["updated_at"] = datetime.now().isoformat()
            self.save_chats()
    
    def auto_title_chat(self, chat_id: str, llm):
        """Automatically generate a title for a chat based on first message"""
        if chat_id not in self.chats["chats"]:
            return
        
        chat = self.chats["chats"][chat_id]
        
        # Only auto-title once and if there are messages
        if chat.get("auto_titled") or not chat.get("messages"):
            return
        
        # Get first user message
        first_message = None
        for msg in chat["messages"]:
            if msg["role"] == "user":
                first_message = msg["content"]
                break
        
        if not first_message:
            return
        
        try:
            # Generate title
            prompt = f"Generate a short, concise title (max 6 words) for a conversation that starts with: '{first_message[:200]}'. Only output the title, nothing else."
            title = llm.invoke(prompt).strip().strip('"\'')
            
            # Clean up title
            if len(title) > 60:
                title = title[:60] + "..."
            
            self.rename_chat(chat_id, title)
            chat["auto_titled"] = True
            self.save_chats()
        
        except Exception as e:
            print(f"Error auto-titling chat: {e}")


class ConversationSearcher:
    """Semantic search over conversation history"""
    
    def __init__(
        self,
        db_path: str = "data/chroma_db",
        collection_name: str = "conversations",
        embedding_model: str = "mxbai-embed-large"
    ):
        self.db_path = Path(db_path)
        self.collection_name = collection_name
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        
        # Initialize ChromaDB
        try:
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_collection(name=collection_name)
            self.available = True
        except Exception as e:
            print(f"Search not available: {e}")
            self.available = False
    
    def search(self, query: str, n_results: int = 10) -> List[Dict]:
        """Search conversations using semantic similarity"""
        if not self.available:
            return []
        
        try:
            # Get query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            formatted_results = []
            if results and 'ids' in results:
                for idx in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][idx],
                        'text': results['documents'][0][idx],
                        'metadata': results['metadatas'][0][idx],
                        'distance': results['distances'][0][idx],
                        'similarity': 1 - results['distances'][0][idx]  # Convert distance to similarity
                    })
            
            return formatted_results
        
        except Exception as e:
            st.error(f"Search error: {e}")
            return []
    
    def rerank_results(self, query: str, results: List[Dict], llm) -> List[Dict]:
        """Use LLM to rerank search results for better relevance"""
        if not results:
            return []
        
        try:
            # Create prompt for reranking
            prompt = f"""Given the query: "{query}"

Rank the following conversation excerpts from most to least relevant (1-{len(results)}):

"""
            for idx, result in enumerate(results, 1):
                prompt += f"\n{idx}. {result['text'][:300]}...\n"
            
            prompt += "\nOutput only the numbers in order of relevance (e.g., '3,1,5,2,4'):"
            
            # Get reranking from LLM
            response = llm.invoke(prompt).strip()
            
            # Parse the response
            order = [int(x.strip()) - 1 for x in response.split(',') if x.strip().isdigit()]
            
            # Reorder results
            reranked = []
            for idx in order:
                if 0 <= idx < len(results):
                    reranked.append(results[idx])
            
            # Add any missing results at the end
            for result in results:
                if result not in reranked:
                    reranked.append(result)
            
            return reranked
        
        except:
            return results
    
    def summarize_results(self, query: str, results: List[Dict], llm) -> str:
        """Generate a summary of search results"""
        if not results:
            return "No results found."
        
        try:
            # Combine top results
            context = "\n\n".join([r['text'][:500] for r in results[:5]])
            
            prompt = f"""Based on the following conversation excerpts, provide a concise summary relevant to the query: "{query}"

Excerpts:
{context}

Summary:"""
            
            summary = llm.invoke(prompt)
            return summary.strip()
        
        except Exception as e:
            return f"Error generating summary: {e}"


# Initialize session state
if 'chat_manager' not in st.session_state:
    st.session_state.chat_manager = ChatManager()

if 'searcher' not in st.session_state:
    st.session_state.searcher = ConversationSearcher()

if 'show_search' not in st.session_state:
    st.session_state.show_search = False


# Sidebar
with st.sidebar:
    st.title("🧠 AI Assistant")
    
    # Model selection
    st.subheader("⚙️ Settings")
    model = st.selectbox(
        "Model",
        ["deepseek-r1:1.5b", "llama3.1", "llama3.2", "qwen2.5"],
        index=0
    )
    
    # Initialize LLM
    if 'llm' not in st.session_state or st.session_state.get('current_model') != model:
        st.session_state.llm = Ollama(model=model, temperature=0.7)
        st.session_state.current_model = model
    
    llm = st.session_state.llm
    
    st.divider()
    
    # Chat management
    st.subheader("💬 Chats")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("➕ New Chat", use_container_width=True):
            chat_id = st.session_state.chat_manager.create_chat()
            st.rerun()
    
    with col2:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.show_search = not st.session_state.show_search
            st.rerun()
    
    # List all chats
    all_chats = st.session_state.chat_manager.get_all_chats()
    current_chat = st.session_state.chat_manager.get_current_chat()
    
    if not all_chats:
        st.info("No chats yet. Create one to start!")
    else:
        for chat in all_chats:
            is_current = current_chat and chat['id'] == current_chat['id']
            
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if st.button(
                        f"{'📌' if is_current else '💬'} {chat['title'][:30]}",
                        key=f"chat_{chat['id']}",
                        use_container_width=True,
                        type="primary" if is_current else "secondary"
                    ):
                        st.session_state.chat_manager.switch_chat(chat['id'])
                        st.session_state.show_search = False
                        st.rerun()
                
                with col2:
                    if st.button("🗑️", key=f"del_{chat['id']}"):
                        st.session_state.chat_manager.delete_chat(chat['id'])
                        st.rerun()
    
    st.divider()
    
    # Stats
    st.caption(f"💾 {len(all_chats)} chat(s)")
    if st.session_state.searcher.available:
        st.caption(f"📚 {st.session_state.searcher.collection.count()} indexed chunks")


# Main area
if st.session_state.show_search:
    # Search interface
    st.title("🔍 Search Conversations")
    
    query = st.text_input("Enter your search query:", placeholder="What are you looking for?")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        n_results = st.slider("Number of results", 3, 20, 10)
    with col2:
        use_rerank = st.checkbox("AI Reranking", value=True)
    with col3:
        use_summary = st.checkbox("Summarize", value=True)
    
    if st.button("🔎 Search", type="primary"):
        if not query:
            st.warning("Please enter a search query")
        elif not st.session_state.searcher.available:
            st.error("Search is not available. Please run index.py first.")
        else:
            with st.spinner("Searching..."):
                results = st.session_state.searcher.search(query, n_results)
                
                if not results:
                    st.info("No results found")
                else:
                    # Rerank if enabled
                    if use_rerank:
                        with st.spinner("Reranking results..."):
                            results = st.session_state.searcher.rerank_results(query, results, llm)
                    
                    # Generate summary if enabled
                    if use_summary:
                        with st.spinner("Generating summary..."):
                            summary = st.session_state.searcher.summarize_results(query, results, llm)
                            
                            st.subheader("📝 Summary")
                            st.info(summary)
                    
                    # Display results
                    st.subheader(f"📊 Results ({len(results)})")
                    
                    for idx, result in enumerate(results, 1):
                        with st.expander(
                            f"{idx}. {result['metadata'].get('title', 'Untitled')} "
                            f"(Similarity: {result['similarity']:.2%})"
                        ):
                            st.markdown(f"**Platform:** {result['metadata'].get('platform', 'unknown')}")
                            st.markdown(f"**Created:** {result['metadata'].get('created_at', 'unknown')}")
                            st.markdown(f"**Type:** {result['metadata'].get('type', 'unknown')}")
                            st.divider()
                            st.text_area("Content", result['text'], height=200, disabled=True, key=f"result_{idx}")

else:
    # Chat interface
    current_chat = st.session_state.chat_manager.get_current_chat()
    
    if not current_chat:
        # No chat selected - create one
        st.title("Welcome to AI Personal Assistant 🧠")
        st.info("👈 Create a new chat to get started!")
    
    else:
        # Display chat
        st.title(current_chat['title'])
        
        # Rename button
        if st.button("✏️ Rename Chat"):
            new_title = st.text_input("New title:", value=current_chat['title'])
            if st.button("Save"):
                st.session_state.chat_manager.rename_chat(current_chat['id'], new_title)
                st.rerun()
        
        # Display messages
        messages_container = st.container()
        with messages_container:
            for msg in current_chat['messages']:
                with st.chat_message(msg['role']):
                    st.markdown(msg['content'])
        
        # Chat input
        if prompt := st.chat_input("Type your message..."):
            # Add user message
            st.session_state.chat_manager.add_message(current_chat['id'], "user", prompt)
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Build conversation history for context
                    conversation_history = ""
                    for msg in current_chat['messages']:
                        role = msg['role'].capitalize()
                        conversation_history += f"{role}: {msg['content']}\n\n"
                    
                    # Generate response
                    try:
                        response = llm.invoke(conversation_history + f"User: {prompt}\n\nAssistant:")
                        st.markdown(response)
                        
                        # Save assistant message
                        st.session_state.chat_manager.add_message(current_chat['id'], "assistant", response)
                        
                        # Auto-title if first message
                        st.session_state.chat_manager.auto_title_chat(current_chat['id'], llm)
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.info("Make sure Ollama is running with the selected model.")
            
            st.rerun()


# Footer
st.divider()
st.caption("🧠 AI Personal Assistant | Powered by Ollama, ChromaDB & Streamlit")

