"""
Data Ingestion Pipeline for AI Conversation Archive
Processes ChatGPT conversation exports into normalized JSONL format
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set
import hashlib


class ConversationIngester:
    """Handles ingestion of conversation data from various AI platforms"""
    
    def __init__(
        self,
        intake_dir: str = "_intake",
        output_file: str = "data/master_conversations.jsonl",
        processed_dir: str = "_intake/processed"
    ):
        self.intake_dir = Path(intake_dir)
        self.output_file = Path(output_file)
        self.processed_dir = Path(processed_dir)
        
        # Ensure directories exist
        self.intake_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing conversation IDs for deduplication
        self.existing_ids: Set[str] = self._load_existing_ids()
    
    def _load_existing_ids(self) -> Set[str]:
        """Load IDs of already-processed conversations for deduplication"""
        if not self.output_file.exists():
            return set()
        
        ids = set()
        with open(self.output_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    ids.add(record.get('conversation_id', ''))
                except json.JSONDecodeError:
                    continue
        
        print(f"📚 Loaded {len(ids)} existing conversation IDs")
        return ids
    
    def _generate_message_hash(self, message: Dict) -> str:
        """Generate unique hash for a message to prevent duplicates"""
        content = json.dumps(message, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def parse_chatgpt_export(self, file_path: Path) -> List[Dict]:
        """
        Parse ChatGPT conversations.json export file
        
        ChatGPT Export Structure:
        [
            {
                "title": "Conversation Title",
                "create_time": 1234567890.0,
                "update_time": 1234567890.0,
                "mapping": {
                    "node_id": {
                        "id": "node_id",
                        "message": {
                            "id": "message_id",
                            "author": {"role": "user"|"assistant"},
                            "create_time": 1234567890.0,
                            "content": {"content_type": "text", "parts": ["message text"]}
                        },
                        "parent": "parent_node_id",
                        "children": ["child_node_id"]
                    }
                }
            }
        ]
        """
        print(f"📖 Parsing ChatGPT export: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        
        normalized_records = []
        new_count = 0
        duplicate_count = 0
        
        for conv in conversations:
            conv_id = conv.get('id', self._generate_message_hash(conv))
            
            # Check for duplicates
            if conv_id in self.existing_ids:
                duplicate_count += 1
                continue
            
            # Extract messages from the mapping structure
            messages = self._extract_messages_from_mapping(conv.get('mapping', {}))
            
            if not messages:
                continue
            
            # Create normalized record
            record = {
                'conversation_id': conv_id,
                'title': conv.get('title', 'Untitled Conversation'),
                'platform': 'chatgpt',
                'created_at': self._format_timestamp(conv.get('create_time')),
                'updated_at': self._format_timestamp(conv.get('update_time')),
                'messages': messages,
                'metadata': {
                    'message_count': len(messages),
                    'imported_at': datetime.now().isoformat()
                }
            }
            
            normalized_records.append(record)
            self.existing_ids.add(conv_id)
            new_count += 1
        
        print(f"  ✅ New conversations: {new_count}")
        print(f"  ⏭️  Duplicates skipped: {duplicate_count}")
        
        return normalized_records
    
    def _extract_messages_from_mapping(self, mapping: Dict) -> List[Dict]:
        """Extract and order messages from ChatGPT's nested mapping structure"""
        if not mapping:
            return []
        
        messages = []
        
        for node_id, node in mapping.items():
            message_data = node.get('message')
            if not message_data:
                continue
            
            author = message_data.get('author', {})
            role = author.get('role', 'unknown')
            
            # Skip system messages
            if role == 'system':
                continue
            
            content = message_data.get('content', {})
            parts = content.get('parts', [])
            
            # Combine all parts into single text
            text = '\n'.join([str(part) for part in parts if part])
            
            if not text or text == 'None':
                continue
            
            messages.append({
                'role': role,
                'content': text,
                'timestamp': self._format_timestamp(message_data.get('create_time'))
            })
        
        # Sort by timestamp if available
        messages.sort(key=lambda m: m.get('timestamp', ''))
        
        return messages
    
    def _format_timestamp(self, timestamp) -> str:
        """Convert Unix timestamp to ISO format"""
        if timestamp is None:
            return datetime.now().isoformat()
        
        try:
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp).isoformat()
            return str(timestamp)
        except:
            return datetime.now().isoformat()
    
    def save_records(self, records: List[Dict]):
        """Append normalized records to master JSONL file"""
        if not records:
            print("⚠️  No new records to save")
            return
        
        with open(self.output_file, 'a', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        print(f"💾 Saved {len(records)} conversations to {self.output_file}")
    
    def archive_processed_file(self, file_path: Path):
        """Move processed file to archive directory"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        archive_path = self.processed_dir / archive_name
        
        shutil.move(str(file_path), str(archive_path))
        print(f"📦 Archived: {archive_name}")
    
    def process_all(self):
        """Process all JSON files in intake directory"""
        json_files = list(self.intake_dir.glob('*.json'))
        
        if not json_files:
            print("❌ No JSON files found in _intake/ directory")
            print(f"   Please drop your ChatGPT conversations.json file into: {self.intake_dir.absolute()}")
            return
        
        print(f"\n🚀 Starting ingestion process...")
        print(f"📂 Found {len(json_files)} file(s) to process\n")
        
        total_processed = 0
        
        for file_path in json_files:
            try:
                # Parse the file (currently supports ChatGPT format)
                records = self.parse_chatgpt_export(file_path)
                
                # Save to master file
                self.save_records(records)
                
                # Archive the processed file
                self.archive_processed_file(file_path)
                
                total_processed += len(records)
                
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
                continue
        
        print(f"\n✨ Ingestion complete!")
        print(f"📊 Total conversations processed: {total_processed}")
        print(f"📁 Master file: {self.output_file.absolute()}")
        print(f"📦 Processed files archived to: {self.processed_dir.absolute()}")


def main():
    """Main entry point for the ingestion pipeline"""
    ingester = ConversationIngester()
    ingester.process_all()


if __name__ == "__main__":
    main()

