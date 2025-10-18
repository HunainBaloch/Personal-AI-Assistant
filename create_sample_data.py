"""
Create sample conversation data for testing
This script generates a sample conversations.json file in ChatGPT format
"""

import json
from pathlib import Path
from datetime import datetime, timedelta


def create_sample_conversations():
    """Generate sample conversations in ChatGPT export format"""
    
    conversations = []
    base_time = datetime.now().timestamp()
    
    # Sample conversation 1: Python programming
    conversations.append({
        "id": "sample_conv_1",
        "title": "Python List Comprehensions",
        "create_time": base_time - 86400 * 7,  # 7 days ago
        "update_time": base_time - 86400 * 7,
        "mapping": {
            "node_1": {
                "id": "node_1",
                "message": {
                    "id": "msg_1",
                    "author": {"role": "user"},
                    "create_time": base_time - 86400 * 7,
                    "content": {
                        "content_type": "text",
                        "parts": ["How do I use list comprehensions in Python?"]
                    }
                },
                "parent": None,
                "children": ["node_2"]
            },
            "node_2": {
                "id": "node_2",
                "message": {
                    "id": "msg_2",
                    "author": {"role": "assistant"},
                    "create_time": base_time - 86400 * 7 + 10,
                    "content": {
                        "content_type": "text",
                        "parts": [
                            "List comprehensions in Python provide a concise way to create lists. "
                            "Here's the basic syntax:\n\n"
                            "[expression for item in iterable if condition]\n\n"
                            "Example:\n"
                            "squares = [x**2 for x in range(10)]\n"
                            "# Creates [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]\n\n"
                            "With condition:\n"
                            "even_squares = [x**2 for x in range(10) if x % 2 == 0]\n"
                            "# Creates [0, 4, 16, 36, 64]"
                        ]
                    }
                },
                "parent": "node_1",
                "children": []
            }
        }
    })
    
    # Sample conversation 2: AI and Machine Learning
    conversations.append({
        "id": "sample_conv_2",
        "title": "Introduction to Neural Networks",
        "create_time": base_time - 86400 * 5,  # 5 days ago
        "update_time": base_time - 86400 * 5,
        "mapping": {
            "node_1": {
                "id": "node_1",
                "message": {
                    "id": "msg_1",
                    "author": {"role": "user"},
                    "create_time": base_time - 86400 * 5,
                    "content": {
                        "content_type": "text",
                        "parts": ["Explain how neural networks work"]
                    }
                },
                "parent": None,
                "children": ["node_2"]
            },
            "node_2": {
                "id": "node_2",
                "message": {
                    "id": "msg_2",
                    "author": {"role": "assistant"},
                    "create_time": base_time - 86400 * 5 + 15,
                    "content": {
                        "content_type": "text",
                        "parts": [
                            "Neural networks are computing systems inspired by biological neural networks. "
                            "They consist of:\n\n"
                            "1. **Input Layer**: Receives input data\n"
                            "2. **Hidden Layers**: Process information through weighted connections\n"
                            "3. **Output Layer**: Produces final results\n\n"
                            "Each connection has a weight that gets adjusted during training. "
                            "The network learns by:\n"
                            "- Forward propagation: passing data through layers\n"
                            "- Calculating error: comparing output to expected result\n"
                            "- Backpropagation: adjusting weights to minimize error\n\n"
                            "This process repeats thousands of times until the network can make accurate predictions."
                        ]
                    }
                },
                "parent": "node_1",
                "children": ["node_3"]
            },
            "node_3": {
                "id": "node_3",
                "message": {
                    "id": "msg_3",
                    "author": {"role": "user"},
                    "create_time": base_time - 86400 * 5 + 30,
                    "content": {
                        "content_type": "text",
                        "parts": ["What's the difference between CNN and RNN?"]
                    }
                },
                "parent": "node_2",
                "children": ["node_4"]
            },
            "node_4": {
                "id": "node_4",
                "message": {
                    "id": "msg_4",
                    "author": {"role": "assistant"},
                    "create_time": base_time - 86400 * 5 + 45,
                    "content": {
                        "content_type": "text",
                        "parts": [
                            "Great question! CNNs and RNNs are specialized neural network architectures:\n\n"
                            "**CNNs (Convolutional Neural Networks):**\n"
                            "- Best for: Image and video processing\n"
                            "- Key feature: Convolutional layers that detect patterns (edges, shapes)\n"
                            "- Use cases: Image classification, object detection, face recognition\n\n"
                            "**RNNs (Recurrent Neural Networks):**\n"
                            "- Best for: Sequential data and time series\n"
                            "- Key feature: Memory of previous inputs (feedback loops)\n"
                            "- Use cases: Natural language processing, speech recognition, time series prediction\n\n"
                            "Modern variants include:\n"
                            "- LSTM/GRU (improved RNNs)\n"
                            "- Transformers (replacing RNNs for many NLP tasks)"
                        ]
                    }
                },
                "parent": "node_3",
                "children": []
            }
        }
    })
    
    # Sample conversation 3: Web Development
    conversations.append({
        "id": "sample_conv_3",
        "title": "RESTful API Design Best Practices",
        "create_time": base_time - 86400 * 3,  # 3 days ago
        "update_time": base_time - 86400 * 3,
        "mapping": {
            "node_1": {
                "id": "node_1",
                "message": {
                    "id": "msg_1",
                    "author": {"role": "user"},
                    "create_time": base_time - 86400 * 3,
                    "content": {
                        "content_type": "text",
                        "parts": ["What are the best practices for designing a REST API?"]
                    }
                },
                "parent": None,
                "children": ["node_2"]
            },
            "node_2": {
                "id": "node_2",
                "message": {
                    "id": "msg_2",
                    "author": {"role": "assistant"},
                    "create_time": base_time - 86400 * 3 + 12,
                    "content": {
                        "content_type": "text",
                        "parts": [
                            "Here are key REST API design best practices:\n\n"
                            "1. **Use Proper HTTP Methods:**\n"
                            "   - GET: Retrieve resources\n"
                            "   - POST: Create resources\n"
                            "   - PUT/PATCH: Update resources\n"
                            "   - DELETE: Remove resources\n\n"
                            "2. **Meaningful URLs:**\n"
                            "   - Use nouns, not verbs: /users not /getUsers\n"
                            "   - Hierarchical structure: /users/123/orders/456\n"
                            "   - Lowercase and hyphens: /user-profiles\n\n"
                            "3. **Status Codes:**\n"
                            "   - 200: Success\n"
                            "   - 201: Created\n"
                            "   - 400: Bad request\n"
                            "   - 401: Unauthorized\n"
                            "   - 404: Not found\n"
                            "   - 500: Server error\n\n"
                            "4. **Versioning:** Include version in URL (/api/v1/users)\n\n"
                            "5. **Pagination:** For large datasets, use limit/offset or cursor-based\n\n"
                            "6. **Error Handling:** Return consistent error response format"
                        ]
                    }
                },
                "parent": "node_1",
                "children": []
            }
        }
    })
    
    # Sample conversation 4: Data Science
    conversations.append({
        "id": "sample_conv_4",
        "title": "Data Cleaning Techniques",
        "create_time": base_time - 86400 * 1,  # Yesterday
        "update_time": base_time - 86400 * 1,
        "mapping": {
            "node_1": {
                "id": "node_1",
                "message": {
                    "id": "msg_1",
                    "author": {"role": "user"},
                    "create_time": base_time - 86400 * 1,
                    "content": {
                        "content_type": "text",
                        "parts": ["How do I handle missing data in pandas?"]
                    }
                },
                "parent": None,
                "children": ["node_2"]
            },
            "node_2": {
                "id": "node_2",
                "message": {
                    "id": "msg_2",
                    "author": {"role": "assistant"},
                    "create_time": base_time - 86400 * 1 + 8,
                    "content": {
                        "content_type": "text",
                        "parts": [
                            "Pandas offers several methods for handling missing data:\n\n"
                            "**1. Detection:**\n"
                            "```python\n"
                            "df.isnull().sum()  # Count missing values per column\n"
                            "df.info()          # Overview including null counts\n"
                            "```\n\n"
                            "**2. Removal:**\n"
                            "```python\n"
                            "df.dropna()              # Remove rows with any NaN\n"
                            "df.dropna(axis=1)        # Remove columns with any NaN\n"
                            "df.dropna(thresh=2)      # Keep rows with at least 2 non-NaN values\n"
                            "```\n\n"
                            "**3. Filling:**\n"
                            "```python\n"
                            "df.fillna(0)             # Fill with zero\n"
                            "df.fillna(df.mean())     # Fill with mean\n"
                            "df.fillna(method='ffill') # Forward fill\n"
                            "df.fillna(method='bfill') # Backward fill\n"
                            "```\n\n"
                            "Choose based on your data and analysis needs!"
                        ]
                    }
                },
                "parent": "node_1",
                "children": []
            }
        }
    })
    
    return conversations


def main():
    """Create sample conversations file"""
    print("🎨 Creating sample conversation data...")
    
    # Create conversations
    conversations = create_sample_conversations()
    
    # Ensure _intake directory exists
    intake_dir = Path("_intake")
    intake_dir.mkdir(exist_ok=True)
    
    # Save to file
    output_file = intake_dir / "sample_conversations.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {len(conversations)} sample conversations")
    print(f"📁 Saved to: {output_file}")
    print(f"\n💡 Next steps:")
    print(f"   1. Run: python ingest.py")
    print(f"   2. Run: python index.py")
    print(f"   3. Run: streamlit run app.py")


if __name__ == "__main__":
    main()

