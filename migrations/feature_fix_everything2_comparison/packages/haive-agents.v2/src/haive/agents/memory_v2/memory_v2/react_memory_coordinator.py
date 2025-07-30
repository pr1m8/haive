"""ReactAgent Memory Coordinator with Tool Integration.

This implements the ReactAgent version with memory tools as requested:
- Uses ReactAgent for reasoning and planning
- Integrates LongTermMemoryAgent as a tool
- Provides memory search, storage, and analysis capabilities
- Follows the "get into the react version with the tools" directive

Architecture:
- ReactAgent with memory tools for reasoning about memory operations
- LongTermMemoryAgent tool for persistent memory operations
- ConversationMemoryAgent tool for conversation context
- Memory analysis and coordination through ReactAgent reasoning
"""

import asyncio
import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.memory_v2.conversation_memory_agent import ConversationMemoryAgent

# Import our memory agents
from haive.agents.memory_v2.long_term_memory_agent import (
    LongTermMemoryAgent,
    MemoryEntry,
)

# Import ReactAgent for coordination
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class MemoryCoordinatorConfig(BaseModel):
    """Configuration for ReactMemoryCoordinator."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # LLM configuration for ReactAgent
    llm_config: LLMConfig | None = Field(default=None)

    # Memory storage paths
    long_term_memory_path: str = Field(default="./long_term_memory")
    conversation_memory_path: str = Field(default="./conversation_memory")

    # Memory coordination settings
    enable_conversation_memory: bool = Field(default=True)
    enable_long_term_memory: bool = Field(default=True)
    auto_extract_memories: bool = Field(default=True)

    # ReactAgent settings
    max_iterations: int = Field(default=3)
    temperature: float = Field(default=0.7)


class ReactMemoryCoordinator:
    """ReactAgent-based memory coordinator with tool integration.

    This implements the ReactAgent pattern for memory coordination:
    1. Uses ReactAgent for reasoning about memory operations
    2. Provides memory tools for search, storage, and analysis
    3. Coordinates between different memory types
    4. Enables complex memory reasoning and planning

    Key Features:
    - ReactAgent with memory tools for reasoning
    - Long-term memory search and storage
    - Conversation memory retrieval
    - Memory analysis and insights
    - Cross-memory coordination

    Examples:
        Basic usage::

            coordinator = ReactMemoryCoordinator(user_id="user123")
            await coordinator.initialize()

            # Memory-enhanced conversation with reasoning
            response = await coordinator.run(
                "What do you remember about my work preferences and how should I schedule my week?"
            )

        With custom LLM config::

            config = MemoryCoordinatorConfig(
                llm_config=AzureLLMConfig(deployment_name="gpt-4"),
                temperature=0.3  # Lower temp for more focused reasoning
            )
            coordinator = ReactMemoryCoordinator(user_id="user123", config=config)
    """

    def __init__(
        self,
        user_id: str,
        config: MemoryCoordinatorConfig | None = None,
        name: str = "react_memory_coordinator",
    ):
        """Initialize ReactMemoryCoordinator."""
        self.user_id = user_id
        self.name = name
        self.config = config or MemoryCoordinatorConfig()

        # Memory agents (initialized later)
        self.long_term_memory: LongTermMemoryAgent | None = None
        self.conversation_memory: ConversationMemoryAgent | None = None

        # ReactAgent coordinator (initialized later)
        self.react_agent: ReactAgent | None = None
        self._initialized = False

        logger.info(f"Created ReactMemoryCoordinator for user {user_id}")

    async def initialize(self) -> None:
        """Initialize the ReactAgent and memory agents."""
        if self._initialized:
            return

        # Step 1: Initialize memory agents
        if self.config.enable_long_term_memory:
            self.long_term_memory = LongTermMemoryAgent(
                user_id=self.user_id,
                llm_config=self.config.llm_config,
                storage_path=self.config.long_term_memory_path,
                name=f"{self.name}_ltm",
            )
            await self.long_term_memory.initialize()
            logger.info("✅ Long-term memory agent initialized")

        if self.config.enable_conversation_memory:
            self.conversation_memory = ConversationMemoryAgent.create(
                user_id=self.user_id, name=f"{self.name}_conv"
            )
            await self.conversation_memory.initialize()
            logger.info("✅ Conversation memory agent initialized")

        # Step 2: Create memory tools for ReactAgent
        memory_tools = self._create_memory_tools()

        # Step 3: Initialize ReactAgent with memory tools
        llm_config = self.config.llm_config
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        aug_llm_config = AugLLMConfig(
            llm_config=llm_config,
            temperature=self.config.temperature,
            system_message=self._get_system_message(),
        )

        self.react_agent = ReactAgent(
            name=self.name, engine=aug_llm_config, tools=memory_tools
        )

        self._initialized = True
        logger.info(
            f"✅ ReactMemoryCoordinator initialized with {len(memory_tools)} memory tools"
        )

    def _create_memory_tools(self) -> list:
        """Create memory tools for ReactAgent."""
        tools = []

        # Long-term memory search tool
        if self.long_term_memory:

            @tool
            async def search_long_term_memory(query: str) -> str:
                """Search long-term memory for relevant information."""
                try:
                    result = await self.long_term_memory.run(
                        query, extract_memories=False
                    )
                    memory_context = result.get("memory_context", [])
                    if memory_context:
                        return (
                            f"Found {len(memory_context)} relevant memories:\n"
                            + "\n".join(f"- {mem}" for mem in memory_context[:3])
                        )
                    return "No relevant long-term memories found."
                except Exception as e:
                    return f"Error searching long-term memory: {e!s}"

            tools.append(search_long_term_memory)

        # Conversation memory search tool
        if self.conversation_memory:

            @tool
            async def search_conversation_memory(query: str) -> str:
                """Search conversation memory for relevant context."""
                try:
                    docs = await self.conversation_memory.retrieve_context(query, k=3)
                    if docs:
                        results = []
                        for doc in docs:
                            msg_type = doc.metadata.get("message_type", "unknown")
                            content = doc.page_content[:100]
                            results.append(f"[{msg_type}] {content}")
                        return (
                            f"Found {len(docs)} relevant conversation messages:\n"
                            + "\n".join(results)
                        )
                    return "No relevant conversation history found."
                except Exception as e:
                    return f"Error searching conversation memory: {e!s}"

            tools.append(search_conversation_memory)

        # Memory storage tool
        @tool
        async def store_memory(
            content: str, memory_type: str = "factual", importance: float = 0.7
        ) -> str:
            """Store new information in long-term memory."""
            try:
                if self.long_term_memory:
                    memory = MemoryEntry(
                        content=content,
                        memory_type=memory_type,
                        importance=min(max(importance, 0.0), 1.0),  # Clamp to [0,1]
                        user_id=self.user_id,
                        tags=[memory_type],
                    )
                    self.long_term_memory.memory_store.add_memory(memory)
                    return (
                        f"✅ Stored {memory_type} memory with importance {importance}"
                    )
                return "❌ Long-term memory not enabled"
            except Exception as e:
                return f"❌ Error storing memory: {e!s}"

        tools.append(store_memory)

        # Memory analysis tool
        @tool
        async def analyze_memory_patterns() -> str:
            """Analyze memory patterns and provide insights."""
            try:
                insights = []

                if self.long_term_memory:
                    ltm_summary = self.long_term_memory.get_memory_summary()
                    insights.append(
                        f"Long-term: {ltm_summary['total_memories']} memories, types: {ltm_summary['memory_types']}"
                    )

                if self.conversation_memory:
                    conv_summary = (
                        await self.conversation_memory.get_conversation_summary()
                    )
                    insights.append(
                        f"Conversation: {conv_summary['total_messages']} messages across {conv_summary['conversations']} conversations"
                    )

                return (
                    "Memory Analysis:\n" + "\n".join(insights)
                    if insights
                    else "No memory data available for analysis."
                )

            except Exception as e:
                return f"❌ Error analyzing memory: {e!s}"

        tools.append(analyze_memory_patterns)

        return tools

    def _get_system_message(self) -> str:
        """Get system message for ReactAgent."""
        return """You are an intelligent memory coordinator that helps users manage and retrieve their memories.

You have access to several memory tools:
- search_long_term_memory: Search persistent memories across conversations
- search_conversation_memory: Search recent conversation history
- store_memory: Store new important information
- analyze_memory_patterns: Analyze memory patterns and insights

Your role is to:
1. Help users find relevant information from their memories
2. Store important new information for future recall
3. Provide insights about memory patterns and relationships
4. Coordinate between different types of memory (long-term, conversational)

When users ask questions:
- First search relevant memories to provide context
- Combine information from different memory sources
- Store any new important information mentioned
- Provide thoughtful responses based on memory context

Be helpful, insightful, and proactive about memory management."""

    async def run(self, query: str, add_to_conversation: bool = True) -> dict[str, Any]:
        """Run memory-enhanced conversation with ReactAgent reasoning.

        This implements the ReactAgent pattern for memory operations:
        1. ReactAgent reasons about what memory operations are needed
        2. Uses memory tools to search, store, and analyze information
        3. Provides comprehensive response with memory context
        4. Optionally stores the conversation for future reference
        """
        await self.initialize()

        # Step 1: Use ReactAgent to reason about memory operations and respond
        react_result = await self.react_agent.arun(query)

        # Step 2: Add conversation to memory if enabled
        if add_to_conversation and self.conversation_memory:
            messages = [HumanMessage(query), AIMessage(str(react_result))]
            await self.conversation_memory.add_conversation(messages)

        # Step 3: Extract and store memories if enabled
        if self.config.auto_extract_memories and self.long_term_memory:
            await self.long_term_memory._extract_and_store_memories(
                query, str(react_result)
            )

        return {
            "response": react_result,
            "user_id": self.user_id,
            "memory_tools_used": (
                self.react_agent.tool_calls_made
                if hasattr(self.react_agent, "tool_calls_made")
                else 0
            ),
            "coordinator_name": self.name,
        }

    async def add_conversation_batch(
        self, messages: list[BaseMessage]
    ) -> dict[str, Any]:
        """Add a batch of conversation messages to memory."""
        results = {"conversation_stored": False, "memories_extracted": 0}

        # Add to conversation memory
        if self.conversation_memory:
            await self.conversation_memory.add_conversation(messages)
            results["conversation_stored"] = True

        # Extract long-term memories
        if self.long_term_memory:
            extracted = await self.long_term_memory.add_conversation(messages)
            results["memories_extracted"] = len(extracted)

        return results

    async def get_comprehensive_memory_summary(self) -> dict[str, Any]:
        """Get comprehensive summary of all memory systems."""
        summary = {
            "user_id": self.user_id,
            "coordinator_name": self.name,
            "initialized": self._initialized,
            "memory_systems": {},
        }

        if self.long_term_memory:
            summary["memory_systems"][
                "long_term"
            ] = self.long_term_memory.get_memory_summary()

        if self.conversation_memory:
            summary["memory_systems"][
                "conversation"
            ] = await self.conversation_memory.get_conversation_summary()

        return summary

    # Factory methods for easy creation
    @classmethod
    def create(
        cls,
        user_id: str,
        llm_config: LLMConfig | None = None,
        enable_all_memory: bool = True,
        name: str = "react_memory_coordinator",
    ) -> "ReactMemoryCoordinator":
        """Factory method to create ReactMemoryCoordinator."""
        config = MemoryCoordinatorConfig(
            llm_config=llm_config,
            enable_conversation_memory=enable_all_memory,
            enable_long_term_memory=enable_all_memory,
        )

        return cls(user_id=user_id, config=config, name=name)

    @classmethod
    def create_focused(
        cls,
        user_id: str,
        llm_config: LLMConfig | None = None,
        name: str = "focused_memory_coordinator",
    ) -> "ReactMemoryCoordinator":
        """Create coordinator optimized for focused reasoning."""
        config = MemoryCoordinatorConfig(
            llm_config=llm_config,
            temperature=0.3,  # Lower temperature for focused reasoning
            max_iterations=2,  # Fewer iterations for efficiency
        )

        return cls(user_id=user_id, config=config, name=name)


# Demo function showing ReactAgent memory coordination
async def demo_react_memory_coordinator():
    """Demo ReactAgent memory coordinator functionality."""
    print("🤖 Demo: ReactAgent Memory Coordinator")

    # Create coordinator
    coordinator = ReactMemoryCoordinator.create(
        user_id="demo_user", name="demo_coordinator"
    )

    # Initialize
    await coordinator.initialize()
    print("✅ ReactMemoryCoordinator initialized")

    # Add some initial conversation context
    initial_messages = [
        HumanMessage("Hi, I'm Alex and I work as a data scientist at Netflix"),
        HumanMessage(
            "I prefer working in the morning and I love collaborative projects"
        ),
        HumanMessage(
            "I'm currently working on a recommendation system for documentaries"
        ),
    ]

    batch_result = await coordinator.add_conversation_batch(initial_messages)
    print(f"✅ Added initial context: {batch_result}")

    # Test ReactAgent memory coordination
    queries = [
        "What do you know about my work and preferences?",
        "How should I structure my workday based on my preferences?",
        "What projects am I working on and how do they relate to my background?",
        "Store this new information: I just got promoted to senior data scientist",
    ]

    for query in queries:
        try:
            print(f"\n🔍 Query: {query}")
            result = await coordinator.run(query)

            response = result["response"]
            if hasattr(response, "content"):
                response_text = response.content
            else:
                response_text = str(response)

            print(f"🤖 Response: {response_text[:200]}...")
            print(f"🔧 Tools used: {result.get('memory_tools_used', 0)}")

        except Exception as e:
            print(f"⚠️  Query failed: {str(e)[:150]}...")

    # Get comprehensive summary
    summary = await coordinator.get_comprehensive_memory_summary()
    print("\n📊 Comprehensive Summary:")
    print(f"   User: {summary['user_id']}")
    print(f"   Systems: {list(summary['memory_systems'].keys())}")

    if "long_term" in summary["memory_systems"]:
        ltm = summary["memory_systems"]["long_term"]
        print(f"   Long-term memories: {ltm['total_memories']}")

    if "conversation" in summary["memory_systems"]:
        conv = summary["memory_systems"]["conversation"]
        print(f"   Conversation messages: {conv['total_messages']}")

    print("\n✅ ReactAgent Memory Coordinator demo completed!")


if __name__ == "__main__":
    asyncio.run(demo_react_memory_coordinator())
