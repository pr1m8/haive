# Quick Start Examples

This guide provides practical, copy-and-paste examples to get you started with Haive quickly.

## Basic Agent Example

```python
"""
Basic agent creation and usage example.
PyCon 2024 - Building AI Agents with Haive
"""

import asyncio
from haive.agents.simple import SimpleAgent
from haive.core.config import AgentConfig

async def basic_agent_demo():
    """Demonstrate basic agent creation and conversation."""

    # Create a simple conversational agent
    agent = SimpleAgent(
        config=AgentConfig(
            name="Assistant",
            description="A helpful AI assistant",
            model="gpt-4",
            temperature=0.7
        )
    )

    # Have a conversation
    response = await agent.chat("What's the weather like today?")
    print(f"Agent: {response}")

    # Continue the conversation with context
    response = await agent.chat("Should I bring an umbrella?")
    print(f"Agent: {response}")

# Run the demo
if __name__ == "__main__":
    asyncio.run(basic_agent_demo())
```

## Multi-Agent Collaboration

```python
"""
Multi-agent collaboration example.
Shows how agents can work together on complex tasks.
"""

import asyncio
from haive.agents.multi import MultiAgentOrchestrator
from haive.agents.simple import SimpleAgent
from haive.agents.reasoning_and_critique.reflexion import ReflexionAgent

async def multi_agent_demo():
    """Demonstrate multiple agents working together."""

    # Create specialized agents
    researcher = SimpleAgent(
        config=AgentConfig(
            name="Researcher",
            description="Expert at finding and analyzing information",
            tools=["web_search", "arxiv_search"]
        )
    )

    analyst = ReflexionAgent(
        config=AgentConfig(
            name="Analyst",
            description="Critical thinker who validates findings",
            reflection_depth=2
        )
    )

    writer = SimpleAgent(
        config=AgentConfig(
            name="Writer",
            description="Creates clear, engaging content",
            temperature=0.8
        )
    )

    # Create orchestrator to coordinate agents
    orchestrator = MultiAgentOrchestrator(
        agents=[researcher, analyst, writer],
        workflow="sequential"  # Agents work in sequence
    )

    # Execute a complex task
    result = await orchestrator.execute(
        task="Research the latest developments in quantum computing "
             "and write a blog post for a general audience"
    )

    print("Final Result:")
    print(result.final_output)

    # Show how each agent contributed
    print("\nAgent Contributions:")
    for contribution in result.agent_contributions:
        print(f"\n{contribution.agent_name}:")
        print(contribution.output[:200] + "...")

asyncio.run(multi_agent_demo())
```

## Tool Integration Example

```python
"""
Tool integration example.
Shows how to create and use custom tools with agents.
"""

import asyncio
from typing import Dict, Any
from haive.tools.base import BaseTool, ToolConfig
from haive.agents.react import ReactAgent
from haive.core.config import AgentConfig

class WeatherTool(BaseTool):
    """Custom weather tool for demonstration."""

    def __init__(self):
        super().__init__(
            config=ToolConfig(
                name="weather",
                description="Get current weather for a location",
                parameters={
                    "location": {
                        "type": "string",
                        "description": "City name or coordinates"
                    }
                }
            )
        )

    async def execute(self, location: str) -> Dict[str, Any]:
        """Simulate weather API call."""
        # In real implementation, call actual weather API
        return {
            "location": location,
            "temperature": "72°F",
            "conditions": "Partly cloudy",
            "humidity": "45%",
            "wind": "10 mph NW"
        }

class RestaurantTool(BaseTool):
    """Custom restaurant finder tool."""

    def __init__(self):
        super().__init__(
            config=ToolConfig(
                name="find_restaurants",
                description="Find restaurants near a location",
                parameters={
                    "location": {
                        "type": "string",
                        "description": "Search location"
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "Type of cuisine (optional)"
                    }
                }
            )
        )

    async def execute(self, location: str, cuisine: str = None) -> Dict[str, Any]:
        """Simulate restaurant search."""
        restaurants = [
            {"name": "The Garden Bistro", "cuisine": "Italian", "rating": 4.5},
            {"name": "Sushi Paradise", "cuisine": "Japanese", "rating": 4.7},
            {"name": "Burger Haven", "cuisine": "American", "rating": 4.2}
        ]

        if cuisine:
            restaurants = [r for r in restaurants if r["cuisine"].lower() == cuisine.lower()]

        return {"restaurants": restaurants, "total": len(restaurants)}

async def tool_integration_demo():
    """Demonstrate custom tool integration with agents."""

    # Create agent with custom tools
    agent = ReactAgent(
        config=AgentConfig(
            name="Travel Assistant",
            description="Helps with travel planning",
            tools=[WeatherTool(), RestaurantTool()],
            verbose=True  # Show reasoning process
        )
    )

    # Complex query requiring multiple tools
    query = """I'm visiting San Francisco tomorrow.
    What's the weather like and can you recommend some good Italian restaurants?"""

    response = await agent.chat(query)
    print(f"Assistant: {response}")

    # Show tool usage
    print("\nTool Usage:")
    for tool_call in agent.last_tool_calls:
        print(f"- {tool_call.tool}: {tool_call.arguments}")

asyncio.run(tool_integration_demo())
```

## Game Development Example

```python
"""
Game development example.
Create an AI-powered chess game with different AI personalities.
"""

import asyncio
from haive.games.chess import ChessGame, ChessAI
from haive.games.chess.strategies import MinimaxStrategy, MonteCarloStrategy
from haive.games.base import GameConfig

async def chess_game_demo():
    """Demonstrate AI game development with Chess."""

    # Create AI players with different strategies
    aggressive_ai = ChessAI(
        name="Magnus",
        strategy=MinimaxStrategy(depth=4, aggressive=True),
        personality="aggressive"
    )

    defensive_ai = ChessAI(
        name="Anatoly",
        strategy=MinimaxStrategy(depth=4, defensive=True),
        personality="defensive"
    )

    creative_ai = ChessAI(
        name="Mikhail",
        strategy=MonteCarloStrategy(simulations=1000),
        personality="creative"
    )

    # Create game configuration
    game_config = GameConfig(
        time_limit=300,  # 5 minutes per player
        allow_draws=True,
        log_moves=True
    )

    # Run a tournament
    print("Chess AI Tournament Starting!")
    print("=" * 50)

    players = [aggressive_ai, defensive_ai, creative_ai]
    results = {}

    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players[i+1:], i+1):
            print(f"\nMatch: {player1.name} vs {player2.name}")

            game = ChessGame(
                white_player=player1,
                black_player=player2,
                config=game_config
            )

            result = await game.play()

            print(f"Winner: {result.winner or 'Draw'}")
            print(f"Moves: {result.total_moves}")
            print(f"Duration: {result.duration:.1f}s")

            # Store results
            match_key = f"{player1.name} vs {player2.name}"
            results[match_key] = result

    # Show tournament summary
    print("\n" + "=" * 50)
    print("Tournament Summary:")
    for match, result in results.items():
        print(f"{match}: {result.winner or 'Draw'} ({result.total_moves} moves)")

asyncio.run(chess_game_demo())
```

## RAG (Retrieval-Augmented Generation) Example

```python
"""
RAG pipeline example.
Build a document Q&A system with retrieval-augmented generation.
"""

import asyncio
from pathlib import Path
from haive.agents.rag import AdaptiveRAGAgent
from haive.core.document import DocumentLoader, PDFLoader
from haive.core.vectorstore import ChromaVectorStore
from haive.core.embeddings import OpenAIEmbeddings

async def rag_pipeline_demo():
    """Demonstrate building a RAG pipeline for document Q&A."""

    # Step 1: Load documents
    print("Loading documents...")
    loaders = [
        PDFLoader("research_papers/quantum_computing.pdf"),
        PDFLoader("research_papers/machine_learning.pdf"),
        DocumentLoader("docs/", glob="*.md")  # Load markdown files
    ]

    documents = []
    for loader in loaders:
        docs = await loader.load()
        documents.extend(docs)
    print(f"Loaded {len(documents)} documents")

    # Step 2: Create vector store
    print("\nCreating vector store...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = ChromaVectorStore(
        collection_name="research_docs",
        embedding_function=embeddings
    )

    # Add documents to vector store
    await vectorstore.add_documents(documents)
    print(f"Added {len(documents)} documents to vector store")

    # Step 3: Create RAG agent
    rag_agent = AdaptiveRAGAgent(
        vectorstore=vectorstore,
        config=AgentConfig(
            name="Research Assistant",
            description="Expert at answering questions from documents",
            model="gpt-4",
            retrieval_k=5,  # Retrieve top 5 relevant chunks
            adaptive_retrieval=True  # Dynamically adjust retrieval
        )
    )

    # Step 4: Ask questions
    questions = [
        "What are the latest developments in quantum error correction?",
        "How do transformer models differ from RNNs?",
        "What are the practical applications of quantum computing?",
        "Explain the attention mechanism in neural networks"
    ]

    for question in questions:
        print(f"\nQ: {question}")

        # Get answer with sources
        result = await rag_agent.answer_with_sources(question)

        print(f"A: {result.answer}")
        print(f"Sources: {', '.join(result.sources)}")
        print(f"Confidence: {result.confidence:.2f}")

    # Step 5: Interactive Q&A session
    print("\n" + "=" * 50)
    print("Interactive Q&A Session (type 'quit' to exit)")
    print("=" * 50)

    while True:
        question = input("\nYour question: ")
        if question.lower() == 'quit':
            break

        result = await rag_agent.answer_with_sources(question)
        print(f"\nAnswer: {result.answer}")
        print(f"Based on: {', '.join(result.sources)}")

asyncio.run(rag_pipeline_demo())
```

## Complete Application Example

```python
"""
Complete application example.
Build a customer support system with multiple specialized agents.
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from haive.agents.multi import MultiAgentOrchestrator
from haive.agents.simple import SimpleAgent
from haive.agents.rag import FilteredRAGAgent
from haive.core.persistence import PostgresCheckpointer
from haive.core.config import AgentConfig, OrchestratorConfig

class CustomerSupportSystem:
    """Complete customer support system with specialized agents."""

    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = knowledge_base_path
        self.checkpointer = PostgresCheckpointer(
            connection_string="postgresql://user:pass@localhost/support"
        )
        self.agents = self._create_agents()
        self.orchestrator = self._create_orchestrator()
        self.conversation_history = []

    def _create_agents(self) -> List[SimpleAgent]:
        """Create specialized support agents."""

        # Technical support agent with access to documentation
        tech_agent = FilteredRAGAgent(
            config=AgentConfig(
                name="Tech Support",
                description="Handles technical issues and troubleshooting",
                knowledge_base=self.knowledge_base_path + "/technical/",
                filter_categories=["technical", "troubleshooting", "errors"]
            )
        )

        # Billing support agent
        billing_agent = SimpleAgent(
            config=AgentConfig(
                name="Billing Support",
                description="Handles billing, subscriptions, and payments",
                tools=["billing_api", "subscription_lookup"],
                system_prompt="""You are a billing support specialist.
                Be helpful and empathetic when dealing with payment issues."""
            )
        )

        # General support agent
        general_agent = SimpleAgent(
            config=AgentConfig(
                name="General Support",
                description="Handles general inquiries and routes complex issues",
                temperature=0.7,
                system_prompt="""You are a friendly customer support agent.
                Help users and escalate to specialists when needed."""
            )
        )

        return [tech_agent, billing_agent, general_agent]

    def _create_orchestrator(self) -> MultiAgentOrchestrator:
        """Create orchestrator with routing logic."""

        def route_to_agent(query: str) -> str:
            """Route customer query to appropriate agent."""
            query_lower = query.lower()

            if any(word in query_lower for word in ["bug", "error", "crash", "not working"]):
                return "Tech Support"
            elif any(word in query_lower for word in ["payment", "bill", "subscription", "charge"]):
                return "Billing Support"
            else:
                return "General Support"

        return MultiAgentOrchestrator(
            agents=self.agents,
            config=OrchestratorConfig(
                routing_function=route_to_agent,
                enable_collaboration=True,
                checkpointer=self.checkpointer
            )
        )

    async def handle_customer_query(self,
                                  customer_id: str,
                                  query: str,
                                  context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle a customer support query."""

        # Create session context
        session_context = {
            "customer_id": customer_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "context": context or {}
        }

        # Process query through orchestrator
        result = await self.orchestrator.process(
            query=query,
            context=session_context,
            save_checkpoint=True
        )

        # Store in conversation history
        self.conversation_history.append({
            "session": session_context,
            "result": result
        })

        return {
            "response": result.final_response,
            "handled_by": result.primary_agent,
            "confidence": result.confidence,
            "suggested_actions": result.suggested_actions,
            "session_id": result.session_id
        }

    async def escalate_to_human(self, session_id: str, reason: str):
        """Escalate a conversation to human support."""
        # Implementation for escalation logic
        pass

async def support_system_demo():
    """Demonstrate the complete customer support system."""

    # Initialize support system
    support = CustomerSupportSystem(
        knowledge_base_path="/path/to/knowledge/base"
    )

    # Simulate customer queries
    test_queries = [
        {
            "customer_id": "CUST123",
            "query": "My app keeps crashing when I try to upload files",
            "context": {"app_version": "2.3.1", "os": "iOS 15.2"}
        },
        {
            "customer_id": "CUST456",
            "query": "I was charged twice for my subscription last month",
            "context": {"subscription_plan": "Premium", "billing_cycle": "monthly"}
        },
        {
            "customer_id": "CUST789",
            "query": "How do I export my data?",
            "context": {"account_type": "Business"}
        }
    ]

    print("Customer Support System Demo")
    print("=" * 50)

    for query_data in test_queries:
        print(f"\nCustomer {query_data['customer_id']}: {query_data['query']}")

        result = await support.handle_customer_query(**query_data)

        print(f"Agent: {result['handled_by']}")
        print(f"Response: {result['response']}")
        print(f"Confidence: {result['confidence']:.2f}")

        if result['suggested_actions']:
            print(f"Suggested Actions: {', '.join(result['suggested_actions'])}")

    # Show conversation history summary
    print("\n" + "=" * 50)
    print("Session Summary:")
    for i, conv in enumerate(support.conversation_history):
        print(f"\n{i+1}. Customer: {conv['session']['customer_id']}")
        print(f"   Handled by: {conv['result'].primary_agent}")
        print(f"   Resolution time: {conv['result'].processing_time:.2f}s")

asyncio.run(support_system_demo())
```

## Testing and Debugging Example

```python
"""
Testing and debugging example.
Shows how to test agents and debug issues.
"""

import asyncio
import logging
from haive.agents.simple import SimpleAgent
from haive.core.config import AgentConfig
from haive.core.logging import setup_logging, LogConfig
from haive.testing import AgentTestHarness, TestScenario

# Set up detailed logging for debugging
setup_logging(
    config=LogConfig(
        level="DEBUG",
        format="detailed",
        include_timestamps=True,
        log_to_file="agent_debug.log"
    )
)

async def testing_demo():
    """Demonstrate agent testing and debugging."""

    # Create agent to test
    agent = SimpleAgent(
        config=AgentConfig(
            name="Test Agent",
            description="Agent for testing",
            model="gpt-3.5-turbo",
            temperature=0.3,
            debug=True  # Enable debug mode
        )
    )

    # Create test harness
    harness = AgentTestHarness(agent)

    # Define test scenarios
    scenarios = [
        TestScenario(
            name="Basic greeting",
            input="Hello, how are you?",
            expected_keywords=["hello", "hi", "greetings"],
            expected_sentiment="positive"
        ),
        TestScenario(
            name="Information request",
            input="What is the capital of France?",
            expected_keywords=["Paris"],
            expected_accuracy=0.95
        ),
        TestScenario(
            name="Error handling",
            input="",  # Empty input
            should_handle_gracefully=True
        )
    ]

    # Run tests
    print("Running Agent Tests")
    print("=" * 50)

    for scenario in scenarios:
        print(f"\nTest: {scenario.name}")
        result = await harness.run_scenario(scenario)

        print(f"Status: {'PASS' if result.passed else 'FAIL'}")
        print(f"Response: {result.response[:100]}...")

        if not result.passed:
            print(f"Failure reason: {result.failure_reason}")

        # Show performance metrics
        print(f"Response time: {result.response_time:.2f}s")
        print(f"Token usage: {result.token_usage}")

    # Debug specific interaction
    print("\n" + "=" * 50)
    print("Debugging Agent Interaction")
    print("=" * 50)

    # Enable verbose debugging
    agent.set_debug_level("TRACE")

    # Run interaction with full debugging
    response = await agent.chat(
        "Explain quantum entanglement in simple terms",
        debug_info=True
    )

    # Show debug information
    debug_info = agent.get_debug_info()
    print("\nDebug Information:")
    print(f"Model calls: {debug_info['model_calls']}")
    print(f"Total tokens: {debug_info['total_tokens']}")
    print(f"Processing steps: {len(debug_info['processing_steps'])}")

    for i, step in enumerate(debug_info['processing_steps']):
        print(f"\nStep {i+1}: {step['name']}")
        print(f"Duration: {step['duration']:.3f}s")
        if 'error' in step:
            print(f"Error: {step['error']}")

asyncio.run(testing_demo())
```

## Next Steps

After running these examples, explore:

1. **Advanced Agent Patterns** - See `/guides/agent_patterns.md`
2. **Custom Tool Development** - See `/guides/custom_tools.md`
3. **Production Deployment** - See `/guides/deployment.md`
4. **Performance Optimization** - See `/guides/optimization.md`

## Troubleshooting

Common issues and solutions:

```python
# Issue: Agent not responding
# Solution: Check API keys and model availability
import os
os.environ["OPENAI_API_KEY"] = "your-key-here"

# Issue: Slow performance
# Solution: Use caching and connection pooling
from haive.core.cache import RedisCache
cache = RedisCache("redis://localhost:6379")
agent.enable_caching(cache)

# Issue: Memory issues with large documents
# Solution: Use streaming and chunking
from haive.core.document import StreamingLoader
loader = StreamingLoader(chunk_size=1000)
```

For more help, see our [troubleshooting guide](/guides/troubleshooting.md) or visit our [community forum](https://community.haive.ai).
