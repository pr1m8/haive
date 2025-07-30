"""ReactAgent with memory tools for dynamic memory management.

This implementation follows LangChain's long-term memory patterns but uses
ReactAgent with tools for flexible memory operations.
"""

from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool

from haive.agents.memory_v2.time_weighted_retriever import TimeWeightedRetriever
from haive.agents.react.agent import ReactAgent


class ReactMemoryAgent:
    """ReactAgent with memory management tools.

    This agent uses tools to:
    - Load relevant memories before responding
    - Store new memories from conversations
    - Update existing memories
    - Delete outdated memories
    - Search memories by semantic similarity
    - Search memories by time range
    """

    def __init__(
        self,
        name: str = "react_memory_agent",
        engine: AugLLMConfig | None = None,
        user_id: str | None = None,
        memory_store_path: str | None = None,
        k: int = 5,
        decay_rate: float = 0.01,
        use_time_weighting: bool = True,
    ):
        self.name = name
        self.engine = engine or AugLLMConfig(temperature=0.7)
        self.user_id = user_id or "default_user"
        self.k = k
        self.decay_rate = decay_rate
        self.use_time_weighting = use_time_weighting

        # Initialize vector store
        self.embeddings = OpenAIEmbeddings()

        # Initialize or load vector store
        if memory_store_path:
            try:
                self.vector_store = FAISS.load_local(
                    memory_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
            except:
                # Create new if doesn't exist
                self.vector_store = FAISS.from_documents(
                    [
                        Document(
                            page_content="Initial memory",
                            metadata={"timestamp": datetime.now().isoformat()},
                        )
                    ],
                    self.embeddings,
                )
        else:
            self.vector_store = FAISS.from_documents(
                [
                    Document(
                        page_content="Initial memory",
                        metadata={"timestamp": datetime.now().isoformat()},
                    )
                ],
                self.embeddings,
            )

        # Initialize retrievers
        if self.use_time_weighting:
            self.retriever = TimeWeightedRetriever(
                vectorstore=self.vector_store, decay_rate=self.decay_rate, k=self.k
            )
        else:
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": self.k})

        # Create memory tools
        self.memory_tools = self._create_memory_tools()

        # Create ReactAgent with memory tools
        self.agent = ReactAgent(
            name=self.name,
            engine=self.engine,
            tools=self.memory_tools,
            system_message=self._get_system_message(),
        )

    def _get_system_message(self) -> str:
        """Get system message that instructs agent on memory usage."""
        return f"""You are an AI assistant with access to long-term memory for user {self.user_id}.

IMPORTANT: For EVERY user query, you should:
1. First use the 'search_memories' tool to find relevant past conversations and facts
2. Use the retrieved memories to provide more personalized and contextual responses
3. After responding, use 'store_memory' to save important information from the conversation
4. Use 'update_memory' if you need to correct or enhance existing memories
5. Use 'delete_memory' if information is outdated or incorrect

Your memory tools allow you to:
- search_memories: Find relevant past information
- search_memories_by_time: Find memories from specific time periods
- store_memory: Save new important information
- update_memory: Modify existing memories
- delete_memory: Remove outdated information
- list_recent_memories: See the most recent memories

Always strive to use memories to provide more helpful, personalized responses."""

    def _create_memory_tools(self) -> list[Any]:
        """Create memory management tools."""

        @tool
        def search_memories(query: str, k: int | None = None) -> str:
            """Search memories by semantic similarity.

            Args:
                query: Search query
                k: Number of memories to retrieve (default: 5)

            Returns:
                Retrieved memories as formatted string
            """
            k = k or self.k
            try:
                # Use time-weighted retriever if enabled
                if self.use_time_weighting:
                    self.retriever.k = k
                    docs = self.retriever.get_relevant_documents(query)
                else:
                    docs = self.vector_store.similarity_search(query, k=k)

                if not docs:
                    return "No relevant memories found."

                # Format memories
                memories = []
                for i, doc in enumerate(docs, 1):
                    timestamp = doc.metadata.get("timestamp", "Unknown time")
                    memory_type = doc.metadata.get("type", "general")
                    importance = doc.metadata.get("importance", "normal")

                    memories.append(
                        f"Memory {i} [{memory_type}] (from {timestamp}, importance: {importance}):\n"
                        f"{doc.page_content}"
                    )

                return "\n\n".join(memories)
            except Exception as e:
                return f"Error searching memories: {e!s}"

        @tool
        def search_memories_by_time(
            start_date: str, end_date: str | None = None, k: int | None = None
        ) -> str:
            """Search memories within a time range.

            Args:
                start_date: Start date (ISO format: YYYY-MM-DD)
                end_date: End date (ISO format: YYYY-MM-DD), defaults to now
                k: Maximum number of memories to retrieve

            Returns:
                Memories from the specified time range
            """
            k = k or self.k
            try:
                from datetime import datetime

                start = datetime.fromisoformat(start_date)
                end = datetime.fromisoformat(end_date) if end_date else datetime.now()

                # Get all documents
                all_docs = self.vector_store.similarity_search("", k=1000)

                # Filter by time range
                filtered_docs = []
                for doc in all_docs:
                    timestamp_str = doc.metadata.get("timestamp")
                    if timestamp_str:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if start <= timestamp <= end:
                            filtered_docs.append(doc)

                # Sort by timestamp and limit
                filtered_docs.sort(
                    key=lambda d: d.metadata.get("timestamp", ""), reverse=True
                )
                filtered_docs = filtered_docs[:k]

                if not filtered_docs:
                    return f"No memories found between {start_date} and {end_date or 'now'}."

                # Format memories
                memories = []
                for i, doc in enumerate(filtered_docs, 1):
                    timestamp = doc.metadata.get("timestamp", "Unknown time")
                    memory_type = doc.metadata.get("type", "general")

                    memories.append(
                        f"Memory {i} [{memory_type}] (from {timestamp}):\n"
                        f"{doc.page_content}"
                    )

                return "\n\n".join(memories)
            except Exception as e:
                return f"Error searching memories by time: {e!s}"

        @tool
        def store_memory(
            content: str,
            memory_type: str = "conversation",
            importance: str = "normal",
            tags: str | None = None,
        ) -> str:
            """Store a new memory.

            Args:
                content: Memory content to store
                memory_type: Type of memory (conversation, fact, preference, skill)
                importance: Importance level (low, normal, high, critical)
                tags: Comma-separated tags for categorization

            Returns:
                Confirmation message
            """
            try:
                # Create metadata
                metadata = {
                    "timestamp": datetime.now().isoformat(),
                    "type": memory_type,
                    "importance": importance,
                    "user_id": self.user_id,
                }

                if tags:
                    metadata["tags"] = [t.strip() for t in tags.split(",")]

                # Create document
                doc = Document(page_content=content, metadata=metadata)

                # Add to vector store
                self.vector_store.add_documents([doc])

                return f"Successfully stored {memory_type} memory with {importance} importance."
            except Exception as e:
                return f"Error storing memory: {e!s}"

        @tool
        def update_memory(memory_id: str, new_content: str) -> str:
            """Update an existing memory.

            Args:
                memory_id: ID or unique identifier of the memory
                new_content: New content for the memory

            Returns:
                Confirmation message
            """
            try:
                # Note: FAISS doesn't support direct updates, so we'll store a new version
                # with update metadata
                metadata = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "update",
                    "original_memory_id": memory_id,
                    "user_id": self.user_id,
                }

                doc = Document(
                    page_content=f"[UPDATED MEMORY] {new_content}", metadata=metadata
                )

                self.vector_store.add_documents([doc])

                return "Successfully updated memory. New version stored."
            except Exception as e:
                return f"Error updating memory: {e!s}"

        @tool
        def delete_memory(memory_id: str) -> str:
            """Mark a memory as deleted.

            Args:
                memory_id: ID or description of the memory to delete

            Returns:
                Confirmation message
            """
            try:
                # FAISS doesn't support deletion, so we add a deletion marker
                metadata = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "deletion",
                    "deleted_memory_id": memory_id,
                    "user_id": self.user_id,
                }

                doc = Document(
                    page_content=f"[DELETED] Memory identified by: {memory_id}",
                    metadata=metadata,
                )

                self.vector_store.add_documents([doc])

                return f"Memory marked as deleted: {memory_id}"
            except Exception as e:
                return f"Error deleting memory: {e!s}"

        @tool
        def list_recent_memories(k: int = 10) -> str:
            """List the most recent memories.

            Args:
                k: Number of recent memories to retrieve

            Returns:
                Recent memories formatted as string
            """
            try:
                # Get all documents (limited search)
                all_docs = self.vector_store.similarity_search("", k=100)

                # Sort by timestamp
                sorted_docs = sorted(
                    all_docs,
                    key=lambda d: d.metadata.get("timestamp", ""),
                    reverse=True,
                )[:k]

                if not sorted_docs:
                    return "No memories found."

                memories = []
                for i, doc in enumerate(sorted_docs, 1):
                    timestamp = doc.metadata.get("timestamp", "Unknown time")
                    memory_type = doc.metadata.get("type", "general")
                    importance = doc.metadata.get("importance", "normal")

                    memories.append(
                        f"{i}. [{memory_type}] {timestamp} (importance: {importance}):\n"
                        f"   {doc.page_content[:100]}..."
                    )

                return "Recent memories:\n" + "\n".join(memories)
            except Exception as e:
                return f"Error listing recent memories: {e!s}"

        return [
            search_memories,
            search_memories_by_time,
            store_memory,
            update_memory,
            delete_memory,
            list_recent_memories,
        ]

    async def arun(
        self, query: str, auto_save: bool = True, include_metadata: bool = False
    ) -> dict[str, Any]:
        """Run the ReactAgent with memory tools.

        Args:
            query: User query
            auto_save: Automatically save conversation to memory
            include_metadata: Include metadata in response

        Returns:
            Agent response with optional metadata
        """
        # Run the agent
        response = await self.agent.arun(query)

        # Auto-save conversation if enabled
        if auto_save:
            # Create conversation memory
            conversation_memory = f"User: {query}\nAssistant: {response}"

            # Use store_memory tool to save
            await self.agent.arun(
                f"Please store this conversation as a memory: {conversation_memory}"
            )

        if include_metadata:
            return {
                "response": response,
                "user_id": self.user_id,
                "timestamp": datetime.now().isoformat(),
                "tools_used": (
                    self.agent.get_tool_usage_stats()
                    if hasattr(self.agent, "get_tool_usage_stats")
                    else None
                ),
            }

        return response

    def save_vector_store(self, path: str):
        """Save the vector store to disk."""
        self.vector_store.save_local(path)

    @classmethod
    def create_with_custom_tools(
        cls,
        name: str = "custom_memory_agent",
        engine: AugLLMConfig | None = None,
        custom_tools: list[Any] | None = None,
        **kwargs,
    ) -> "ReactMemoryAgent":
        """Create ReactMemoryAgent with additional custom tools.

        Args:
            name: Agent name
            engine: LLM configuration
            custom_tools: Additional tools to include
            **kwargs: Other ReactMemoryAgent parameters

        Returns:
            ReactMemoryAgent with custom tools
        """
        # Create base agent
        agent = cls(name=name, engine=engine, **kwargs)

        # Add custom tools if provided
        if custom_tools:
            all_tools = agent.memory_tools + custom_tools
            agent.agent = ReactAgent(
                name=name,
                engine=agent.engine,
                tools=all_tools,
                system_message=agent._get_system_message(),
            )

        return agent


# Example usage functions
async def example_basic_usage():
    """Example of basic ReactMemoryAgent usage."""
    # Create agent
    agent = ReactMemoryAgent(
        name="personal_assistant", user_id="alice_smith", k=5, use_time_weighting=True
    )

    # First conversation
    response1 = await agent.arun(
        "Hi, I'm Alice. I work as a data scientist at TechCorp and I love hiking.",
        auto_save=True,
    )
    print("Response 1:", response1)

    # Later conversation - agent should remember
    response2 = await agent.arun("What do you remember about my job?", auto_save=True)
    print("Response 2:", response2)

    # Search specific memories
    response3 = await agent.arun(
        "Search my memories for information about hiking", auto_save=False
    )
    print("Response 3:", response3)

    # Save vector store
    agent.save_vector_store("alice_memories")


async def example_with_custom_tools():
    """Example with custom tools added."""

    # Define custom tool
    @tool
    def calculate_days_since(date_str: str) -> str:
        """Calculate days since a given date."""
        from datetime import datetime

        try:
            past_date = datetime.fromisoformat(date_str)
            days = (datetime.now() - past_date).days
            return f"{days} days have passed since {date_str}"
        except:
            return "Invalid date format. Use YYYY-MM-DD"

    # Create agent with custom tool
    agent = ReactMemoryAgent.create_with_custom_tools(
        name="enhanced_assistant",
        custom_tools=[calculate_days_since],
        user_id="bob_jones",
    )

    # Use both memory and custom tools
    response = await agent.arun(
        "Store a memory that I started my new job on 2024-01-15, "
        "then calculate how many days I've been working there."
    )
    print("Response:", response)


if __name__ == "__main__":
    import asyncio

    # Run examples
    asyncio.run(example_basic_usage())
    # asyncio.run(example_with_custom_tools())
