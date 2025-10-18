"""
Vector Database Indexing for AI Conversation Archive
Creates searchable embeddings using ChromaDB and Ollama
"""

import json
from pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import OllamaEmbeddings
from datetime import datetime


class ConversationIndexer:
    """Indexes conversations into ChromaDB for semantic search"""
    
    def __init__(
        self,
        master_file: str = "data/master_conversations.jsonl",
        db_path: str = "data/chroma_db",
        collection_name: str = "conversations",
        embedding_model: str = "mxbai-embed-large"
    ):
        self.master_file = Path(master_file)
        self.db_path = Path(db_path)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        
        # Initialize embeddings
        print(f"🔧 Initializing embeddings with {embedding_model}...")
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        
        # Initialize ChromaDB
        print(f"🗄️  Initializing ChromaDB at {db_path}...")
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        print(f"✅ Collection '{collection_name}' ready")
    
    def load_conversations(self) -> List[Dict]:
        """Load all conversations from master JSONL file"""
        if not self.master_file.exists():
            print(f"❌ Master file not found: {self.master_file}")
            print("   Please run ingest.py first to create the master file")
            return []
        
        conversations = []
        with open(self.master_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    conversations.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        
        print(f"📚 Loaded {len(conversations)} conversations from {self.master_file.name}")
        return conversations
    
    def create_searchable_chunks(self, conversation: Dict) -> List[Dict]:
        """
        Create searchable chunks from a conversation
        
        Strategy:
        1. Full conversation summary (title + all messages combined)
        2. Individual messages with context
        """
        chunks = []
        conv_id = conversation['conversation_id']
        title = conversation.get('title', 'Untitled')
        messages = conversation.get('messages', [])
        platform = conversation.get('platform', 'unknown')
        created_at = conversation.get('created_at', '')
        
        # Chunk 1: Full conversation summary
        full_text = f"Title: {title}\n\n"
        for msg in messages:
            role = msg.get('role', 'unknown').capitalize()
            content = msg.get('content', '')
            full_text += f"{role}: {content}\n\n"
        
        chunks.append({
            'id': f"{conv_id}_full",
            'text': full_text.strip(),
            'type': 'full_conversation',
            'conversation_id': conv_id,
            'title': title,
            'platform': platform,
            'created_at': created_at,
            'message_count': len(messages)
        })
        
        # Chunk 2-N: Individual messages with context window
        for idx, msg in enumerate(messages):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            # Skip empty messages
            if not content or len(content.strip()) < 3:
                continue
            
            # Add context (title + previous message if available)
            context_text = f"Conversation: {title}\n\n"
            
            if idx > 0:
                prev_msg = messages[idx - 1]
                prev_role = prev_msg.get('role', 'unknown').capitalize()
                prev_content = prev_msg.get('content', '')
                context_text += f"Previous {prev_role}: {prev_content[:200]}...\n\n"
            
            context_text += f"{role.capitalize()}: {content}"
            
            chunks.append({
                'id': f"{conv_id}_msg_{idx}",
                'text': context_text,
                'type': 'message',
                'conversation_id': conv_id,
                'title': title,
                'platform': platform,
                'created_at': created_at,
                'message_index': idx,
                'role': role
            })
        
        return chunks
    
    def index_conversations(self, conversations: List[Dict], batch_size: int = 50):
        """Index conversations into ChromaDB with embeddings"""
        if not conversations:
            print("⚠️  No conversations to index")
            return
        
        print(f"\n🚀 Starting indexing process...")
        print(f"📊 Processing {len(conversations)} conversations\n")
        
        # Get existing IDs in collection
        existing_ids = set()
        try:
            existing = self.collection.get()
            if existing and 'ids' in existing:
                existing_ids = set(existing['ids'])
                print(f"📝 Found {len(existing_ids)} existing chunks in database")
        except:
            pass
        
        all_chunks = []
        
        # Create chunks from all conversations
        for idx, conv in enumerate(conversations, 1):
            chunks = self.create_searchable_chunks(conv)
            all_chunks.extend(chunks)
            
            if idx % 10 == 0:
                print(f"  📦 Processed {idx}/{len(conversations)} conversations...")
        
        print(f"\n✅ Created {len(all_chunks)} searchable chunks")
        
        # Filter out already-indexed chunks
        new_chunks = [chunk for chunk in all_chunks if chunk['id'] not in existing_ids]
        
        if not new_chunks:
            print("✨ All conversations already indexed!")
            return
        
        print(f"🆕 Indexing {len(new_chunks)} new chunks...")
        
        # Index in batches
        for i in range(0, len(new_chunks), batch_size):
            batch = new_chunks[i:i + batch_size]
            
            # Prepare data for ChromaDB
            ids = [chunk['id'] for chunk in batch]
            documents = [chunk['text'] for chunk in batch]
            metadatas = [{
                'type': chunk['type'],
                'conversation_id': chunk['conversation_id'],
                'title': chunk['title'],
                'platform': chunk['platform'],
                'created_at': chunk.get('created_at', ''),
                'message_index': chunk.get('message_index', -1),
                'role': chunk.get('role', ''),
                'indexed_at': datetime.now().isoformat()
            } for chunk in batch]
            
            # Generate embeddings and add to collection
            try:
                # Get embeddings
                embeddings = self.embeddings.embed_documents(documents)
                
                # Add to ChromaDB
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
                
                print(f"  ✅ Indexed batch {i//batch_size + 1} ({len(batch)} chunks)")
            
            except Exception as e:
                print(f"  ❌ Error indexing batch {i//batch_size + 1}: {e}")
                continue
        
        print(f"\n✨ Indexing complete!")
        print(f"📊 Total chunks in database: {self.collection.count()}")
        print(f"💾 Database location: {self.db_path.absolute()}")
    
    def rebuild_index(self):
        """Rebuild the entire index from scratch"""
        print("🔄 Rebuilding index from scratch...")
        
        # Delete and recreate collection
        try:
            self.client.delete_collection(self.collection_name)
            print(f"🗑️  Deleted old collection")
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"✅ Created fresh collection")
        
        # Load and index all conversations
        conversations = self.load_conversations()
        self.index_conversations(conversations)
    
    def get_stats(self):
        """Display statistics about the indexed data"""
        print(f"\n📊 Index Statistics")
        print(f"─" * 50)
        print(f"Collection: {self.collection_name}")
        print(f"Total chunks: {self.collection.count()}")
        print(f"Database path: {self.db_path.absolute()}")
        print(f"Embedding model: {self.embedding_model}")
        print(f"─" * 50)


def main():
    """Main entry point for indexing pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Index AI conversations for semantic search")
    parser.add_argument('--rebuild', action='store_true', help='Rebuild index from scratch')
    parser.add_argument('--stats', action='store_true', help='Show index statistics')
    args = parser.parse_args()
    
    indexer = ConversationIndexer()
    
    if args.stats:
        indexer.get_stats()
    elif args.rebuild:
        indexer.rebuild_index()
    else:
        conversations = indexer.load_conversations()
        indexer.index_conversations(conversations)
        indexer.get_stats()


if __name__ == "__main__":
    main()

