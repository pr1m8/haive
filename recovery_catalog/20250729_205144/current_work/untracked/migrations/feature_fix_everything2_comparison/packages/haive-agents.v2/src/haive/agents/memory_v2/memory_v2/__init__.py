"""Memory V2 System - BaseRAGAgent-based Memory Architecture.

This package provides memory-capable agents built on BaseRAGAgent as requested:

**Working Components (BaseRAGAgent-based):**
- UnifiedMemoryRAGAgent: Complete memory system using BaseRAGAgent
- ConversationMemoryAgent: Conversation history with BaseRAGAgent
- FactualMemoryAgent: Factual storage with BaseRAGAgent
- PreferencesMemoryAgent: User preferences with SimpleRAGAgent
- StandaloneMemoryItem: Memory model without broken dependencies

**Key Features:**
- Real BaseRAGAgent integration with vector stores
- Time-weighted retrieval for temporal queries
- Multi-modal memory storage (conversation, facts, preferences)
- Agent-as-tool pattern support
- No mocks - all real components

**Quick Start:**

    from haive.agents.memory_v2 import create_unified_memory_agent
    from langchain_core.messages import HumanMessage

    # Create unified memory agent using BaseRAGAgent
    agent = create_unified_memory_agent(user_id="user123")
    await agent.initialize()

    # Process conversation and extract memories
    messages = [HumanMessage("I work at Google as a software engineer")]
    result = await agent.process_conversation(messages)

    # Retrieve context
    context = await agent.retrieve_context("Where do I work?")

**Agent-as-Tool Pattern:**

    # Use memory as a tool in other agents
    memory_tool = UnifiedMemoryRAGAgent.as_tool(
        name="user_memory",
        description="Search user memory"
    )

    # Use in ReactAgent or other agents
    coordinator = ReactAgent(tools=[memory_tool])
"""

# Import working standalone RAG memory components
from haive.agents.memory_v2.standalone_rag_memory import (
    ConversationMemoryAgent,
    FactualMemoryAgent,
    ImportanceLevel,
    MemoryRAGConfig,
    MemoryType,
    PreferencesMemoryAgent,
    StandaloneMemoryItem,
    UnifiedMemoryRAGAgent,
    create_conversation_memory_agent,
    create_unified_memory_agent,
)

# Optional components that may have import issues - try to import gracefully
try:
    from haive.agents.memory_v2.time_weighted_retriever import (  # noqa: F401
        TimeWeightConfig,
        TimeWeightedRetriever,
    )

    TIME_RETRIEVER_AVAILABLE = True
except ImportError:
    TIME_RETRIEVER_AVAILABLE = False

try:
    from haive.agents.memory_v2.message_document_converter import (  # noqa: F401
        MessageDocumentConverter,
        TimestampedDocument,
    )

    DOCUMENT_CONVERTER_AVAILABLE = True
except ImportError:
    DOCUMENT_CONVERTER_AVAILABLE = False

try:
    from haive.agents.memory_v2.extraction_prompts import (  # noqa: F401
        EXTRACTION_PROMPTS,
        get_all_extraction_types,
        get_extraction_prompt,
    )

    EXTRACTION_AVAILABLE = True
except ImportError:
    EXTRACTION_AVAILABLE = False

# Core exports (always available with BaseRAGAgent)
__all__ = [
    # RAG-based memory agents (working)
    "UnifiedMemoryRAGAgent",
    "ConversationMemoryAgent",
    "FactualMemoryAgent",
    "PreferencesMemoryAgent",
    "StandaloneMemoryItem",
    "MemoryRAGConfig",
    "MemoryType",
    "ImportanceLevel",
    # Factory functions
    "create_unified_memory_agent",
    "create_conversation_memory_agent",
]

# Add optional exports if available
if TIME_RETRIEVER_AVAILABLE:
    __all__.extend(["TimeWeightConfig", "TimeWeightedRetriever"])

if DOCUMENT_CONVERTER_AVAILABLE:
    __all__.extend(["MessageDocumentConverter", "TimestampedDocument"])

if EXTRACTION_AVAILABLE:
    __all__.extend(
        ["EXTRACTION_PROMPTS", "get_all_extraction_types", "get_extraction_prompt"]
    )
