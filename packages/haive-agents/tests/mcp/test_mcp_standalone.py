"""
Standalone test for MCP RAG functionality
"""
import asyncio
import json
from pathlib import Path

# Use direct imports from haive
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document


def create_mcp_documents():
    """Create documents from MCP server data."""
    print("📚 Loading MCP server data...")
    
    # Direct path to the MCP servers data
    all_servers_path = Path("packages/haive-mcp/data/mcp_servers/ALL_MCP_SERVERS_COMPLETE.json")
    
    with open(all_servers_path, 'r') as f:
        data = json.load(f)
        servers = data.get('all_servers', [])
    
    print(f"📊 Processing {len(servers)} MCP servers...")
    
    documents = []
    for server in servers[:100]:  # Just test with first 100
        # Get server details
        name = server.get('name', 'Unknown')
        description = server.get('description', 'No description available')
        category = server.get('category', 'general')
        language = server.get('language', 'unknown')
        
        # Create simple content
        content = f"""
MCP Server: {name}
Description: {description}
Category: {category}
Language: {language}
Keywords: {category} {language} MCP server {name.lower().replace('-', ' ')} database python
"""
        
        doc = Document(
            page_content=content,
            metadata={
                "server_name": name,
                "category": category,
                "language": language,
                "type": "mcp_server"
            }
        )
        documents.append(doc)
    
    print(f"✅ Created {len(documents)} documents")
    return documents


async def test_mcp_rag():
    """Test MCP RAG functionality."""
    # Create documents
    documents = create_mcp_documents()
    
    # Create embedding config
    embedding_model = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cuda'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    print("\n📊 Creating RAG agent...")
    
    # Create agent using from_documents
    agent = BaseRAGAgent.from_documents(
        documents=documents,
        embedding_model=embedding_model,
        name="MCP_Test_Agent",
        vector_store_provider=VectorStoreProvider.FAISS,
        retriever_kwargs={"k": 5}
    )
    
    print("✅ Agent created!")
    
    # Test queries
    queries = [
        "python database",
        "SQLAlchemy",
        "PostgreSQL",
        "database connections"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"🔍 Query: {query}")
        print(f"{'='*60}")
        
        result = await agent.arun(query)
        
        print(f"\nResult type: {type(result)}")
        
        if hasattr(result, 'retrieved_documents'):
            docs = result.retrieved_documents
            print(f"📚 Retrieved {len(docs)} documents")
            
            for i, doc in enumerate(docs[:3], 1):
                print(f"\n{i}. {doc.metadata.get('server_name', 'Unknown')}")
                print(f"   Category: {doc.metadata.get('category', 'unknown')}")
                print(f"   Preview: {doc.page_content[:100]}...")
        else:
            print(f"Result: {result}")


if __name__ == "__main__":
    print("🧪 Testing MCP RAG Agent directly...")
    asyncio.run(test_mcp_rag())