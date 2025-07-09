#!/usr/bin/env python3
"""
Test the fixed MCP RAG agent with proper VectorStoreConfig pattern
"""
import asyncio
import sys
from pathlib import Path

# Add the correct path for imports
sys.path.insert(0, str(Path(__file__).parent))

async def test_mcp_rag_agent():
    """Test the MCP RAG agent with proper configuration."""
    
    print("🧪 Testing MCP RAG Agent with VectorStoreConfig...")
    
    try:
        # Import after path setup
        sys.path.insert(0, str(Path(__file__).parent / "packages" / "haive-mcp" / "src"))
        from haive.mcp.mcp_simple_rag_agent import create_mcp_rag_agent
        
        print("✅ Import successful!")
        
        # Create the agent
        print("\n🔧 Creating MCP RAG agent...")
        agent = create_mcp_rag_agent()
        
        print(f"✅ Agent created: {agent.name}")
        print(f"📊 Agent engine: {type(agent.engine)}")
        
        # Test with a simple query
        test_queries = [
            "python database",
            "SQLAlchemy",
            "PostgreSQL server",
            "GitHub integration"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"🔍 Testing query: '{query}'")
            print(f"{'='*60}")
            
            try:
                # Test with proper input format
                result = await agent.arun(query)
                
                print(f"✅ Query successful!")
                print(f"📊 Result type: {type(result)}")
                
                # Check if we got retrieved documents
                if hasattr(result, 'retrieved_documents'):
                    docs = result.retrieved_documents
                    print(f"📚 Retrieved {len(docs)} documents")
                    
                    if docs:
                        print(f"🎯 First result: {docs[0].metadata.get('server_name', 'Unknown')}")
                        print(f"📝 Category: {docs[0].metadata.get('category', 'Unknown')}")
                        print(f"⭐ Stars: {docs[0].metadata.get('stars', 0)}")
                    else:
                        print("⚠️ No documents found in retrieved_documents")
                        
                        # Try direct vector store test
                        print("\n🔧 Testing direct vector store access...")
                        if hasattr(agent.engine, 'vector_store_config'):
                            vs_config = agent.engine.vector_store_config
                            vectorstore = vs_config.create_vectorstore()
                            direct_results = vectorstore.similarity_search(query, k=3)
                            print(f"📊 Direct search found {len(direct_results)} results")
                            
                            if direct_results:
                                for i, doc in enumerate(direct_results[:2], 1):
                                    print(f"  {i}. {doc.metadata.get('server_name', 'Unknown')}")
                else:
                    print(f"📄 Result content: {str(result)[:200]}...")
                    
            except Exception as e:
                print(f"❌ Query failed: {e}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting MCP RAG Agent test...")
    asyncio.run(test_mcp_rag_agent())