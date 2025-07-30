"""SimpleMemoryAgent with token-aware memory management and summarization.

This agent follows V3 enhanced patterns with automatic summarization when approaching
token limits, similar to LangMem's approach.
"""

import logging
from datetime import datetime
from typing import Any

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema import StateSchema
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent

from ..base.memory_state_original import (  # Import original models for compatibility
    EnhancedMemoryItem,
    ImportanceLevel,
    MemoryState,
    MemoryType,
)
from ..base.token_state import MemoryStateWithTokens
from ..core.memory_tools import (
    MemoryConfig,
    classify_memory,
    get_memory_stats,
    retrieve_memory,
    search_memory,
    store_memory,
)
from ..core.token_tracker import TokenThresholds, TokenTracker

# Graph transformer imports - optional
try:
    from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
    from haive.agents.document_modifiers.kg.kg_map_merge.models import (
        EntityNode,
        EntityRelationship,
        KnowledgeGraph,
    )

    HAS_GRAPH_MODELS = True
except ImportError:
    # Create basic fallback models
    class EntityNode(BaseModel):
        name: str = Field(...)
        properties: dict[str, Any] = Field(default_factory=dict)

    class EntityRelationship(BaseModel):
        source: str = Field(...)
        target: str = Field(...)
        relationship: str = Field(...)
        properties: dict[str, Any] = Field(default_factory=dict)

    class KnowledgeGraph(BaseModel):
        nodes: list[EntityNode] = Field(default_factory=list)
        relationships: list[EntityRelationship] = Field(default_factory=list)

    GraphTransformer = None
    HAS_GRAPH_MODELS = False

from langchain_core.documents import Document

logger = logging.getLogger(__name__)


# ============================================================================
# SUMMARIZATION PROMPTS (LangMem-style)
# ============================================================================

MEMORY_SUMMARIZATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""You are a memory summarization expert. Your task is to create concise yet comprehensive summaries of conversation memories while preserving all important information.

Guidelines:
1. Preserve key facts, preferences, and relationships
2. Maintain temporal context and causality
3. Combine related memories into coherent summaries
4. Use clear, direct language
5. Prioritize actionable and personally relevant information
6. Note any important patterns or recurring themes
7. Maintain the original meaning and nuance

Output a summary that captures the essence of the memories while reducing token usage by approximately 70%."""), HumanMessage(
            content="Please summarize the following memories:\n\n{memories_text}\n\nTarget token count: {target_tokens}"), ])

RUNNING_SUMMARY_UPDATE_PROMPT = ChatPromptTemplate.from_messages([SystemMessage(
    content="""You are updating a running summary of conversation memories. You need to integrate new information into the existing summary while keeping it concise and comprehensive.

Guidelines:
1. Merge new information with existing summary
2. Update any changed facts or preferences
3. Preserve all important information
4. Remove redundancies
5. Maintain chronological awareness
6. Keep the summary coherent and well-structured"""), HumanMessage(content="""Current Summary:
{current_summary}

New Memories to Integrate:
{new_memories}

Updated Summary (target tokens: {target_tokens}):"""), ])

MEMORY_REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""You are rewriting memories for efficient storage. Compress the content while maintaining all semantic meaning and important details.

Guidelines:
1. Use concise language without losing meaning
2. Combine related facts into single statements
3. Remove unnecessary words and phrases
4. Preserve all entities, relationships, and key information
5. Maintain the original intent and nuance"""), HumanMessage(
            content="Rewrite this memory more concisely:\n\n{memory_content}\n\nCompression target: {compression_ratio}% of original"), ])


# ============================================================================
# TOKEN-AWARE MEMORY CONFIG
# ============================================================================


class TokenAwareMemoryConfig(MemoryConfig):
    """Configuration for token-aware memory management.

    Extends base MemoryConfig with token tracking and summarization settings.
    """

    # Token management
    max_context_tokens: int = Field(
        default=8000, ge=1000, description="Maximum tokens for context window"
    )

    # Summarization thresholds (following LangMem pattern)
    max_tokens_before_summary: int = Field(
        default=6000, description="Token count that triggers summarization"
    )

    warning_threshold: float = Field(
        default=0.7, description="Warn at 70% of max tokens"
    )

    critical_threshold: float = Field(
        default=0.85, description="Critical at 85% of max tokens"
    )

    # Summarization settings
    summarization_strategy: str = Field(
        default="progressive",
        pattern="^(progressive|aggressive|selective)$",
        description="How to summarize: progressive, aggressive, or selective",
    )

    target_compression_ratio: float = Field(
        default=0.3,
        ge=0.1,
        le=0.8,
        description="Target size after summarization (30% of original)",
    )

    preserve_recent_memories: int = Field(
        default=10,
        ge=0,
        description="Number of recent memories to preserve unsummarized",
    )

    # Running summary
    enable_running_summary: bool = Field(
        default=True, description="Maintain a running summary of all memories"
    )

    running_summary_max_tokens: int = Field(
        default=1000, description="Maximum tokens for running summary"
    )


# ============================================================================
# SIMPLE MEMORY AGENT
# ============================================================================


class SimpleMemoryAgent(EnhancedSimpleAgent):
    """Memory agent with token tracking and automatic summarization.

    This agent follows V3 enhanced patterns and implements LangMem-style
    memory management with:

    - Automatic token tracking for all operations
    - Progressive summarization when approaching limits
    - Running summary maintenance
    - Memory rewriting for compression
    - Smart retrieval with token awareness

    The agent monitors token usage and automatically triggers summarization
    or memory rewriting to stay within context limits while preserving
    important information.

    Examples:
        Basic usage::

            agent = SimpleMemoryAgent(
                name="assistant_memory",
                memory_config=TokenAwareMemoryConfig(
                    max_context_tokens=4000,
                    summarization_strategy="progressive"
                )
            )

            # Store memories
            agent.run("Remember that I prefer coffee over tea")
            agent.run("My favorite coffee is Ethiopian single origin")

            # Retrieve with token awareness
            response = agent.run("What beverages do I like?")

        With custom thresholds::

            config = TokenAwareMemoryConfig(
                max_context_tokens=8000,
                warning_threshold=0.6,
                critical_threshold=0.8,
                preserve_recent_memories=20
            )

            agent = SimpleMemoryAgent(
                name="long_term_memory",
                memory_config=config,
                debug_mode=True
            )
    """

    # Use MemoryStateWithTokens as prebuilt base schema
    state_schema: type[StateSchema] = Field(
        default=MemoryStateWithTokens, exclude=True)
    use_prebuilt_base: bool = Field(default=True, exclude=True)

    # Memory-specific configuration
    memory_config: TokenAwareMemoryConfig = Field(
        default_factory=TokenAwareMemoryConfig,
        description="Token-aware memory configuration",
    )

    token_tracker: TokenTracker = Field(
        default_factory=lambda: TokenTracker(max_context_tokens=8000),
        description="Token usage tracker",
    )

    # State tracking
    running_summary: Optional[str] = Field(
        default=None, description="Running summary of all memories"
    )

    last_summarization: dict[str, Any] | None = Field(
        default=None, description="Details of last summarization operation"
    )

    # Graph transformation components
    graph_transformer: Optional[GraphTransformer] = Field(
        default=None,
        description="Graph transformer for converting content to knowledge graphs",
    )

    graph_enabled: bool = Field(
        default=True,
        description="Whether to enable graph transformation capabilities")

    # Prompts storage (since we can't add to engine)
    memory_summarization_prompt: Optional[ChatPromptTemplate] = Field(
        default=None, description="Prompt for memory summarization"
    )

    running_summary_prompt: Optional[ChatPromptTemplate] = Field(
        default=None, description="Prompt for running summary updates"
    )

    memory_rewrite_prompt: Optional[ChatPromptTemplate] = Field(
        default=None, description="Prompt for memory rewriting/compression"
    )

    # Graph prompts
    entity_extraction_prompt: Optional[ChatPromptTemplate] = Field(
        default=None, description="Prompt for entity extraction"
    )

    relationship_extraction_prompt: Optional[ChatPromptTemplate] = Field(
        default=None, description="Prompt for relationship extraction"
    )

    # ========================================================================
    # SETUP AND CONFIGURATION
    # ========================================================================

    def _prepare_input(self, input_data: Any) -> dict[str, Any]:
        """Prepare input for MemoryStateWithTokens.

        Override parent to ensure proper message format for our state schema.
        """
        from langchain_core.messages import HumanMessage

        # Handle string input
        if isinstance(input_data, str):
            return {"messages": [HumanMessage(content=input_data)]}

        # Handle dict input - ensure it has messages
        if isinstance(input_data, dict):
            if "messages" not in input_data:
                # If no messages, try to extract from other fields
                content = (
                    input_data.get("input")
                    or input_data.get("query")
                    or input_data.get("content", "")
                )
                if content:
                    input_data["messages"] = [
                        HumanMessage(content=str(content))]
                else:
                    input_data["messages"] = []
            return input_data

        # For state objects, return as dict
        if hasattr(input_data, "model_dump"):
            return input_data.model_dump()

        # Default - wrap in messages
        return {"messages": [HumanMessage(content=str(input_data))]}

    def setup_agent(self) -> None:
        """Setup memory agent with token tracking and tools.
        """
        logger.info(f"Setting up SimpleMemoryAgent: {self.name}")

        # Call parent setup
        super().setup_agent()

        # Configure token tracker
        self.token_tracker.max_context_tokens = self.memory_config.max_context_tokens
        self.token_tracker.thresholds = TokenThresholds(
            warning=self.memory_config.warning_threshold,
            critical=self.memory_config.critical_threshold,
        )

        # Add memory tools to engine
        if self.engine:
            # Create tool instances with config
            tools = [
                store_memory,
                retrieve_memory,
                search_memory,
                classify_memory,
                get_memory_stats,
            ]

            # Add tools if not already present
            if hasattr(self.engine, "tools"):
                if self.engine.tools is None:
                    self.engine.tools = []
                for tool in tools:
                    if tool not in self.engine.tools:
                        self.engine.tools.append(tool)

            # Token tracking is handled by the state schema, not engine

            # Add summarization prompts
            self._setup_summarization_prompts()

        # Setup graph transformer if enabled
        if self.graph_enabled:
            self._setup_graph_transformer()

        # State schema is already set as a class attribute

        logger.info(
            f"Memory agent setup complete with {
                self.memory_config.max_context_tokens} max tokens"
        )

    def _setup_summarization_prompts(self) -> None:
        """Setup summarization prompts.
        """
        # Store prompts in agent, not engine
        self.memory_summarization_prompt = MEMORY_SUMMARIZATION_PROMPT
        self.running_summary_prompt = RUNNING_SUMMARY_UPDATE_PROMPT
        self.memory_rewrite_prompt = MEMORY_REWRITE_PROMPT

    def _setup_graph_transformer(self) -> None:
        """Setup graph transformer for knowledge graph generation.
        """
        try:
            if not hasattr(
                    self,
                    "graph_transformer") or self.graph_transformer is None:
                # Initialize the graph transformer
                self.graph_transformer = GraphTransformer()
                logger.info("Graph transformer initialized successfully")

            # Add graph-related prompts to engine if available
            if self.engine:
                self._setup_graph_prompts()

        except Exception as e:
            logger.warning(f"Failed to setup graph transformer: {e}")
            self.graph_enabled = False

    def _setup_graph_prompts(self) -> None:
        """Setup graph-specific prompts for entity and relationship extraction.
        """
        # Entity extraction prompt
        self.entity_extraction_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are an expert at extracting entities from conversational content and memories.

Extract all relevant entities (people, places, concepts, organizations, etc.) from the provided content.

For each entity, provide:
1. ID: A unique, consistent identifier
2. Type: The category of entity (Person, Place, Concept, Organization, etc.)
3. Properties: Key attributes and facts about the entity

Focus on entities that are meaningful and likely to appear in future conversations."""), HumanMessage(
                    content="Extract entities from this content:\n\n{content}"), ])

        # Relationship extraction prompt
        self.relationship_extraction_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are an expert at identifying relationships between entities in conversational content.

Extract meaningful relationships between entities from the provided content.

For each relationship, provide:
1. Source: ID of the source entity
2. Target: ID of the target entity
3. Type: The type of relationship (WORKS_AT, LIVES_IN, KNOWS, RELATED_TO, etc.)
4. Confidence: How confident you are in this relationship (0.0 to 1.0)
5. Evidence: Brief text supporting this relationship

Focus on relationships that are explicitly mentioned or strongly implied."""), HumanMessage(
                    content="Extract relationships from this content:\n\n{content}\n\nKnown entities:\n{entities}"), ])

    # ========================================================================
    # GRAPH BUILDING
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build memory graph with pre-hook system and token-aware branching.

        The graph implements a pre-hook pattern:
        1. Pre-hook node (checks tokens, decides routing)
        2. Branching based on pre-hook decisions
        3. Memory processing (store/retrieve/search)
        4. Summarization (when triggered by pre-hook)
        5. Running summary updates

        Flow:
            START -> pre_hook -> {process_memory, summarize_critical, summarize_warning}
                              -> [optional: update_summary] -> END
        """
        logger.debug(
            f"Building memory graph with pre-hook system for {self.name}")

        graph = BaseGraph(
            name=f"{
                self.name}_graph",
            state_schema=self.state_schema,
        )

        # PRE-HOOK NODE: Token checking and route decision
        graph.add_node("pre_hook", self.pre_hook_node)

        # MAIN PROCESSING NODES
        graph.add_node("process_memory", self.process_memory_node)

        # SUMMARIZATION NODES
        graph.add_node("summarize_critical", self.summarize_critical_node)
        graph.add_node("summarize_warning", self.summarize_warning_node)
        graph.add_node("emergency_compress", self.emergency_compress_node)

        # MEMORY MANAGEMENT NODES
        graph.add_node("consolidate_memories", self.consolidate_memories_node)
        graph.add_node("create_summary", self.create_summary_node)
        graph.add_node("update_summary", self.update_summary_node)

        # GRAPH TRANSFORMATION NODES
        if self.graph_enabled:
            graph.add_node("transform_to_graph", self.transform_to_graph_node)
            graph.add_node("update_graph", self.update_graph_node)
            graph.add_node("extract_entities", self.extract_entities_node)
            graph.add_node(
                "extract_relationships",
                self.extract_relationships_node)

        # START WITH PRE-HOOK
        graph.add_edge(START, "pre_hook")

        # CONDITIONAL ROUTING FROM PRE-HOOK
        routing_map = {
            # Normal processing
            "process": "process_memory",
            # Summarization routes
            "summarize_critical": "summarize_critical",
            "summarize_warning": "summarize_warning",
            "emergency_compress": "emergency_compress",
            # Memory management routes
            "consolidate_memories": "consolidate_memories",
            "create_summary": "create_summary",
            "update_summary": "update_summary",
        }

        # Add graph routes if enabled
        if self.graph_enabled:
            routing_map.update(
                {
                    "transform_to_graph": "transform_to_graph",
                    "update_graph": "update_graph",
                }
            )

        graph.add_conditional_edges(
            "pre_hook", self.route_from_pre_hook, routing_map)

        # ALL ROUTES END (or continue to optional summary update)
        if self.memory_config.enable_running_summary:
            # Routes that should update running summary after
            summary_routes = [
                "summarize_critical",
                "summarize_warning",
                "consolidate_memories",
            ]
            if self.graph_enabled:
                summary_routes.extend(["transform_to_graph"])

            for route in summary_routes:
                graph.add_edge(route, "update_summary")

            # Routes that end directly
            direct_routes = [
                "process_memory",
                "emergency_compress",
                "create_summary",
                "update_summary",
            ]
            if self.graph_enabled:
                direct_routes.extend(["update_graph"])

            for route in direct_routes:
                graph.add_edge(route, END)
        else:
            # All routes end directly
            all_routes = [
                "process_memory",
                "summarize_critical",
                "summarize_warning",
                "emergency_compress",
                "consolidate_memories",
                "create_summary",
                "update_summary",
            ]
            if self.graph_enabled:
                all_routes.extend(["transform_to_graph", "update_graph"])

            for route in all_routes:
                graph.add_edge(route, END)

        logger.debug(
            f"Memory graph built with {len(graph.nodes)} nodes and pre-hook branching"
        )
        return graph

    # ========================================================================
    # NODE IMPLEMENTATIONS
    # ========================================================================

    def pre_hook_node(self, state: MemoryStateWithTokens) -> Command:
        """Pre-hook node that analyzes state and decides routing.

        This is the core of the pre-hook system. It:
        1. Analyzes current token usage
        2. Examines incoming messages
        3. Decides the appropriate route
        4. Prepares any necessary data for downstream nodes

        Args:
            state: Current memory state with token tracking

        Returns:
            Command to update state with routing decisions
        """
        try:
            logger.debug(f"Pre-hook: analyzing state for {self.name}")

            # Get the most recent message (if any)
            last_message = state.messages[-1] if state.messages else None

            # Get comprehensive status
            status = state.get_comprehensive_status()

            # Run the pre-hook analysis
            if last_message:
                hook_result = state.pre_message_hook(last_message)
            else:
                # No message to analyze, use current state
                hook_result = {
                    "current_tokens": status["estimated_total_tokens"],
                    "incoming_tokens": 0,
                    "projected_total": status["estimated_total_tokens"],
                    "projected_ratio": status["token_usage_ratio"],
                    "current_status": status["token_status"],
                    "action_needed": status["needs_action"],
                    "recommended_route": status["recommended_route"],
                }

            # Determine final route
            route = hook_result["recommended_route"]

            # Log the decision
            logger.info(
                f"Pre-hook decision: {route} "
                f"(tokens: {hook_result['current_tokens']}/{state.max_context_tokens}, "
                f"ratio: {hook_result.get('projected_ratio', 0):.1%})"
            )

            # Prepare route-specific data
            route_data = {
                "pre_hook_analysis": hook_result,
                "routing_decision": route,
                "routing_timestamp": datetime.now().isoformat(),
                "comprehensive_status": status,
            }

            # Add route-specific preparation
            if route in [
                "summarize_critical",
                "summarize_warning",
                "emergency_compress",
            ]:
                # Prepare for summarization
                prep_data = state.prepare_for_summarization()
                route_data["summarization_prep"] = prep_data

            elif route in ["consolidate_memories", "create_summary", "update_summary"]:
                # Prepare memory management data
                route_data["memory_consolidation_prep"] = {
                    "current_memory_count": len(state.current_memories),
                    "old_memories": len(
                        [
                            m
                            for m in state.current_memories
                            if m.metadata.memory_type != "meta"
                        ]
                    ),
                    "recent_memories": len(state.current_memories[-10:]),
                    "has_running_summary": state.running_summary is not None,
                }

            return Command(update=route_data)

        except Exception as e:
            logger.exception(f"Error in pre_hook_node: {e}")
            # Fallback to safe processing
            return Command(
                update={
                    "pre_hook_error": str(e),
                    "routing_decision": "process",  # Safe fallback
                    "routing_timestamp": datetime.now().isoformat(),
                }
            )

    def route_from_pre_hook(self, state: MemoryStateWithTokens) -> str:
        """Route based on pre-hook analysis.

        Args:
            state: State with pre-hook analysis results

        Returns:
            Route name for conditional edge routing
        """
        # Get routing decision from pre-hook
        route = state.get("routing_decision", "process")

        logger.debug(f"Routing from pre-hook: {route}")

        # Validate route is one of our defined routes
        valid_routes = {
            "process",
            "summarize_critical",
            "summarize_warning",
            "emergency_compress",
            "consolidate_memories",
            "create_summary",
            "update_summary",
        }

        # Add graph routes if enabled
        if self.graph_enabled:
            valid_routes.update({"transform_to_graph", "update_graph"})

        if route not in valid_routes:
            logger.warning(
                f"Invalid route '{route}', falling back to 'process'")
            return "process"

        return route

    def process_memory_node(self, state: MemoryStateWithTokens) -> Command:
        """Process memory operations (store/retrieve/search).

        This is the main node that handles all memory operations based on the user's
        input, using the appropriate memory tools.
        """
        try:
            messages = state.messages
            if not messages:
                return Command(update={})

            last_message = messages[-1]
            if not isinstance(last_message, HumanMessage | str):
                return Command(update={})

            content = (
                last_message.content
                if hasattr(last_message, "content")
                else str(last_message)
            )

            # Determine operation type and execute
            operation_result = {
                "operation_timestamp": datetime.now().isoformat()}

            if any(word in content.lower()
                   for word in ["remember", "store", "save"]):
                # Store memory operation
                result = store_memory.invoke(
                    {
                        "content": content,
                        "memory_type": "semantic",
                        "importance": "medium",
                        "namespace": self.name,
                        "config": self.memory_config.model_dump(),
                    }
                )
                operation_result["last_operation"] = {
                    "type": "store",
                    "result": result,
                    "timestamp": datetime.now().isoformat(),
                }

            elif any(
                word in content.lower() for word in ["what", "recall", "retrieve"]
            ):
                # Retrieve memory operation
                memories = retrieve_memory.invoke(
                    {
                        "query": content,
                        "limit": 5,
                        "namespace": self.name,
                        "config": self.memory_config.model_dump(),
                    }
                )
                operation_result["retrieved_memories"] = memories
                operation_result["last_operation"] = {
                    "type": "retrieve",
                    "count": len(memories),
                    "timestamp": datetime.now().isoformat(),
                }

            elif any(
                word in content.lower() for word in ["search", "find", "look fof"]
            ):
                # Search memory operation
                memories = search_memory.invoke(
                    {
                        "query": content,
                        "limit": 10,
                        "namespace": self.name,
                        "config": self.memory_config.model_dump(),
                    }
                )
                operation_result["retrieved_memories"] = memories
                operation_result["last_operation"] = {
                    "type": "search",
                    "count": len(memories),
                    "timestamp": datetime.now().isoformat(),
                }

            logger.info(
                f"Memory operation: {
                    operation_result['last_operation']['type']}"
            )

            return Command(update=operation_result)

        except Exception as e:
            logger.exception(f"Error in process_memory_node: {e}")
            return Command(update={"operation_error": str(e)})

    def summarize_critical_node(self, state: MemoryStateWithTokens) -> Command:
        """Critical summarization when approaching token limits.
        """
        try:
            logger.info("Executing critical summarization")

            # Get prepared summarization data from pre-hook
            prep_data = state.get("summarization_prep", {})

            if not prep_data:
                logger.warning("No summarization prep data found")
                return Command(
                    update={
                        "summarization_skipped": "No prep data"})

            # Get data to summarize
            messages_to_summarize = prep_data.get("messages_to_summarize", [])
            memories_to_summarize = prep_data.get("memories_to_summarize", [])
            target_tokens = prep_data.get("target_tokens", 1000)

            if not messages_to_summarize and not memories_to_summarize:
                return Command(
                    update={
                        "summarization_skipped": "Nothing to summarize"})

            # Create comprehensive summary using engine
            if self.engine and self.memory_summarization_prompt:
                # Combine messages and memories into text
                content_parts = []

                # Add messages
                for msg in messages_to_summarize:
                    content_parts.append(
                        f"[Message] {getattr(msg, 'content', str(msg))}"
                    )

                # Add memories
                for mem in memories_to_summarize:
                    content_parts.append(
                        f"[{mem.metadata.memory_type}] {mem.content}")

                content_text = "\n\n".join(content_parts)

                # Generate summary
                prompt = self.memory_summarization_prompt
                summary_input = prompt.format_messages(
                    memories_text=content_text, target_tokens=target_tokens
                )

                response = self.engine.invoke(summary_input)
                summary_text = getattr(response, "content", str(response))

                # Apply summarization results
                message_ids = [
                    getattr(msg, "id", f"msg_{i}")
                    for i, msg in enumerate(messages_to_summarize)
                ]
                memory_ids = [mem.id for mem in memories_to_summarize]

                state.apply_summarization_result(
                    summary=summary_text,
                    summarized_message_ids=message_ids,
                    summarized_memory_ids=memory_ids,
                )

                logger.info(
                    f"Critical summarization complete: {
                        len(content_text)} → {
                        len(summary_text)} chars"
                )

                return Command(
                    update={
                        "summarization_completed": True,
                        "summarization_type": "critical",
                        "original_content_length": len(content_text),
                        "summary_length": len(summary_text),
                        "compression_ratio": (
                            len(summary_text) /
                            len(content_text) if content_text else 0),
                    })

            return Command(
                update={
                    "summarization_error": "No engine available"})

        except Exception as e:
            logger.exception(f"Error in critical summarization: {e}")
            return Command(update={"summarization_error": str(e)})

    def summarize_warning_node(self, state: MemoryStateWithTokens) -> Command:
        """Warning-level summarization for memory consolidation.
        """
        try:
            logger.info("Executing warning-level summarization")

            # Similar to critical but less aggressive
            prep_data = state.get("summarization_prep", {})

            if not prep_data:
                return Command(
                    update={
                        "summarization_skipped": "No prep data"})

            # For warning level, only summarize older content
            memories_to_summarize = prep_data.get("memories_to_summarize", [])

            if len(memories_to_summarize) < 5:
                return Command(
                    update={"summarization_skipped": "Not enough old memories"}
                )

            # Keep it lighter - only summarize memories, not recent messages
            content_text = "\n\n".join(
                [
                    f"[{mem.metadata.memory_type}] {mem.content}"
                    for mem in memories_to_summarize
                ]
            )

            if self.engine and self.memory_summarization_prompt:
                prompt = self.memory_summarization_prompt
                summary_input = prompt.format_messages(
                    memories_text=content_text,
                    target_tokens=int(
                        len(content_text) * 0.4
                    ),  # Less aggressive compression
                )

                response = self.engine.invoke(summary_input)
                summary_text = getattr(response, "content", str(response))

                # Apply only memory summarization
                memory_ids = [mem.id for mem in memories_to_summarize]

                state.apply_summarization_result(
                    summary=summary_text,
                    summarized_message_ids=[],  # No messages summarized
                    summarized_memory_ids=memory_ids,
                )

                logger.info(
                    f"Warning summarization complete: {
                        len(memories_to_summarize)} memories"
                )

                return Command(
                    update={
                        "summarization_completed": True,
                        "summarization_type": "warning",
                        "memories_summarized": len(memories_to_summarize),
                    }
                )

            return Command(
                update={
                    "summarization_error": "No engine available"})

        except Exception as e:
            logger.exception(f"Error in warning summarization: {e}")
            return Command(update={"summarization_error": str(e)})

    def emergency_compress_node(self, state: MemoryStateWithTokens) -> Command:
        """Emergency compression when critically over limits.
        """
        logger.info("Executing emergency compression")

        # Drastic measures: keep only essential content
        essential_memories = []

        # Keep only high-importance memories and summaries
        for memory in state.current_memories:
            if (
                memory.metadata.importance == "high"
                or memory.metadata.memory_type == "meta"
                or "summary" in memory.metadata.tags
            ):
                essential_memories.append(memory)

        # Keep only last 2 messages
        essential_messages = (
            state.messages[-2:] if len(state.messages) > 2 else state.messages
        )

        # Reset state aggressively
        return Command(
            update={
                "current_memories": essential_memories,
                "messages": essential_messages,
                "emergency_compression": True,
                "memories_before": len(state.current_memories),
                "memories_after": len(essential_memories),
                "messages_before": len(state.messages),
                "messages_after": len(essential_messages),
            }
        )

    def consolidate_memories_node(
            self, state: MemoryStateWithTokens) -> Command:
        """Consolidate related memories to reduce count.
        """
        logger.info("Consolidating related memories")

        # Group memories by type and similarity
        grouped_memories = {}
        for memory in state.current_memories:
            key = memory.metadata.memory_type
            if key not in grouped_memories:
                grouped_memories[key] = []
            grouped_memories[key].append(memory)

        # Consolidate each group
        consolidated = []
        for mem_type, memories in grouped_memories.items():
            if len(memories) > 3:
                # Combine into single consolidated memory
                combined_content = f"Consolidated {mem_type} memories:\n" + "\n".join(
                    [f"- {mem.content[:100]}..." for mem in memories])

                consolidated_memory = EnhancedMemoryItem(
                    id=f"consolidated_{mem_type}_{datetime.now().timestamp()}",
                    content=combined_content,
                    source="consolidation",
                    memory_type=MemoryType.META,
                    importance=ImportanceLevel.MEDIUM,
                    tags=["consolidated"],
                    confidence=0.8,
                    metadata={"consolidation_type": mem_type},
                )
                consolidated.append(consolidated_memory)
            else:
                consolidated.extend(memories)

        return Command(
            update={
                "current_memories": consolidated,
                "consolidation_completed": True,
                "original_count": len(state.current_memories),
                "consolidated_count": len(consolidated),
            }
        )

    def create_summary_node(self, state: MemoryStateWithTokens) -> Command:
        """Create initial running summary.
        """
        logger.info("Creating initial running summary")

        if state.running_summary:
            return Command(
                update={"summary_creation_skipped": "Summary already exists"}
            )

        # Create initial summary from recent memories and messages
        recent_content = []

        # Add recent memories
        for memory in state.current_memories[-5:]:
            recent_content.append(f"[Memory] {memory.content}")

        # Add recent messages
        for message in state.messages[-3:]:
            content = getattr(message, "content", str(message))
            recent_content.append(f"[Message] {content}")

        summary = (
            f"Initial summary created at {datetime.now().isoformat()}:\n\n"
            + "\n".join(recent_content)
        )

        return Command(
            update={
                "running_summary": summary,
                "summary_created": True,
                "initial_summary_length": len(summary),
            }
        )

    def update_summary_node(self, state: MemoryStateWithTokens) -> Command:
        """Update existing running summary.
        """
        logger.info("Updating running summary")

        if not state.running_summary:
            # Create if doesn't exist
            return self.create_summary_node(state)

        # Update with recent activity
        recent_activity = f"\nUpdated {
            datetime.now().isoformat()}: Recent activity processed."

        if hasattr(state, "last_operation"):
            recent_activity += f" Last operation: {
                state.last_operation.get(
                    'type', 'unknown')}"

        updated_summary = state.running_summary + recent_activity

        # Trim if getting too long
        if len(updated_summary) > self.memory_config.running_summary_max_tokens * 4:
            # Keep first and last parts
            lines = updated_summary.split("\n")
            keep_start = lines[:10]
            keep_end = lines[-10:]
            updated_summary = "\n".join(
                [*keep_start, "...[trimmed]...", *keep_end])

        return Command(
            update={
                "running_summary": updated_summary,
                "summary_updated": True,
                "summary_length": len(updated_summary),
            }
        )

    # ========================================================================
    # GRAPH TRANSFORMATION NODES
    # ========================================================================

    def transform_to_graph_node(self, state: MemoryStateWithTokens) -> Command:
        """Transform memories and messages into a knowledge graph.
        """
        if not self.graph_enabled or not self.graph_transformer:
            return Command(
                update={
                    "graph_transform_skipped": "Graph transformer not available"})

        try:
            logger.info("Transforming content to knowledge graph")

            # Collect content to transform
            content_parts = []

            # Add recent messages
            for msg in state.messages[-10:]:  # Last 10 messages
                content = getattr(msg, "content", str(msg))
                if content and len(content) > 10:
                    content_parts.append(f"[Message] {content}")

            # Add current memories
            for memory in state.current_memories:
                content_parts.append(
                    f"[Memory:{memory.metadata.memory_type}] {memory.content}"
                )

            if not content_parts:
                return Command(
                    update={
                        "graph_transform_skipped": "No content to transform"})

            # Create document for graph transformation
            combined_content = "\n\n".join(content_parts)
            doc = Document(page_content=combined_content)

            # Transform using the graph transformer
            graph_docs = self.graph_transformer.transform_documents(
                documents=[doc], strict_mode=True, ignore_tool_usage=True
            )

            if not graph_docs:
                return Command(
                    update={
                        "graph_transform_skipped": "No graph generated"})

            # Extract nodes and relationships from graph documents
            all_nodes = []
            all_relationships = []

            for graph_doc in graph_docs:
                # Convert graph nodes to EntityNodes
                for node in graph_doc.nodes:
                    entity_node = EntityNode(
                        id=node.id, type=node.type, properties=node.properties or {})
                    all_nodes.append(entity_node)

                # Convert graph relationships to EntityRelationships
                for rel in graph_doc.relationships:
                    entity_rel = EntityRelationship(
                        source=rel.source.id,
                        target=rel.target.id,
                        type=rel.type,
                        properties=rel.properties or {},
                        confidence_score=0.8,  # Default confidence
                        supporting_evidence=f"Extracted from: {combined_content[:100]}...",
                    )
                    all_relationships.append(entity_rel)

            # Create knowledge graph
            knowledge_graph = KnowledgeGraph()
            for node in all_nodes:
                knowledge_graph.add_node(node)
            for rel in all_relationships:
                knowledge_graph.add_relationship(rel)

            # Update state
            update_data = {
                "knowledge_graph": knowledge_graph,
                "graph_nodes": all_nodes,
                "graph_relationships": all_relationships,
                "last_graph_update": {
                    "timestamp": datetime.now().isoformat(),
                    "nodes_extracted": len(all_nodes),
                    "relationships_extracted": len(all_relationships),
                    "content_processed": len(content_parts),
                    "memory_count": len(state.current_memories),
                },
                "graph_transform_completed": True,
            }

            logger.info(
                f"Graph transformation complete: {
                    len(all_nodes)} nodes, {
                    len(all_relationships)} relationships"
            )

            return Command(update=update_data)

        except Exception as e:
            logger.exception(f"Error in graph transformation: {e}")
            return Command(update={"graph_transform_error": str(e)})

    def update_graph_node(self, state: MemoryStateWithTokens) -> Command:
        """Update existing knowledge graph with new content.
        """
        if not self.graph_enabled or not self.graph_transformer:
            return Command(
                update={
                    "graph_update_skipped": "Graph transformer not available"})

        try:
            logger.info("Updating knowledge graph")

            # Get new content since last update
            last_update = state.last_graph_update
            if not last_update:
                # No previous update, do full transformation
                return self.transform_to_graph_node(state)

            # Get new memories since last update
            last_memory_count = last_update.get("memory_count", 0)
            new_memories = (
                state.current_memories[last_memory_count:]
                if last_memory_count < len(state.current_memories)
                else []
            )

            # Get recent messages
            recent_messages = (
                state.messages[-3:] if len(state.messages) > 3 else state.messages
            )

            if not new_memories and len(recent_messages) < 2:
                return Command(
                    update={
                        "graph_update_skipped": "No new content to process"})

            # Process new content only
            content_parts = []

            for msg in recent_messages:
                content = getattr(msg, "content", str(msg))
                if content and len(content) > 10:
                    content_parts.append(f"[Message] {content}")

            for memory in new_memories:
                content_parts.append(
                    f"[Memory:{memory.metadata.memory_type}] {memory.content}"
                )

            if not content_parts:
                return Command(
                    update={
                        "graph_update_skipped": "No new meaningful content"})

            # Extract entities and relationships from new content
            combined_content = "\n\n".join(content_parts)

            # Use direct extraction if available
            new_nodes = []
            new_relationships = []

            if self.engine and self.entity_extraction_prompt:
                # Extract entities
                try:
                    entity_response = self.engine.invoke(
                        self.entity_extraction_prompt.format_messages(
                            content=combined_content
                        )
                    )
                    # Parse entity response (would need structured output in
                    # real implementation)
                    logger.debug(
                        f"Entity extraction response: {entity_response}")
                except Exception as e:
                    logger.warning(f"Entity extraction failed: {e}")

                # Extract relationships
                try:
                    existing_entities = [
                        f"{node.id} ({node.type})" for node in state.graph_nodes[-10:]
                    ]  # Last 10 entities
                    entities_text = "\n".join(existing_entities)

                    rel_response = self.engine.invoke(
                        self.relationship_extraction_prompt.format_messages(
                            content=combined_content, entities=entities_text
                        )
                    )
                    logger.debug(
                        f"Relationship extraction response: {rel_response}")
                except Exception as e:
                    logger.warning(f"Relationship extraction failed: {e}")

            # For now, create a simple update entry in the existing graph
            if state.knowledge_graph:
                # Add a summary node for the new content
                summary_node = EntityNode(
                    id=f"update_{datetime.now().timestamp()}",
                    type="ContentUpdate",
                    properties={
                        "content_summary": combined_content[:200] + "...",
                        "timestamp": datetime.now().isoformat(),
                        "content_count": len(content_parts),
                    },
                )
                state.knowledge_graph.add_node(summary_node)
                new_nodes.append(summary_node)

            # Update tracking
            update_data = {
                "graph_nodes": state.graph_nodes +
                new_nodes,
                "graph_relationships": state.graph_relationships +
                new_relationships,
                "last_graph_update": {
                    "timestamp": datetime.now().isoformat(),
                    "nodes_added": len(new_nodes),
                    "relationships_added": len(new_relationships),
                    "content_processed": len(content_parts),
                    "memory_count": len(
                        state.current_memories),
                    "update_type": "incremental",
                },
                "graph_update_completed": True,
            }

            logger.info(
                f"Graph update complete: +{len(new_nodes)} nodes, +{len(new_relationships)} relationships"
            )

            return Command(update=update_data)

        except Exception as e:
            logger.exception(f"Error in graph update: {e}")
            return Command(update={"graph_update_error": str(e)})

    def extract_entities_node(self, state: MemoryStateWithTokens) -> Command:
        """Extract entities from content using LLM.
        """
        # This would be used for more granular entity extraction
        # Implementation would depend on structured output capabilities
        return Command(update={"entity_extraction_completed": True})

    def extract_relationships_node(
            self, state: MemoryStateWithTokens) -> Command:
        """Extract relationships from content using LLM.
        """
        # This would be used for more granular relationship extraction
        # Implementation would depend on structured output capabilities
        return Command(update={"relationship_extraction_completed": True})

    def check_tokens_node(self, state: MemoryState) -> dict[str, Any]:
        """Check token usage and determine if action needed.
        """
        status = self.token_tracker.get_status()
        usage_summary = self.token_tracker.get_usage_summary()

        logger.info(
            f"Token check: {status} - "
            f"{usage_summary['total_tokens']}/{usage_summary['max_tokens']} "
            f"({usage_summary['usage_ratio']:.1%})"
        )

        # Update state with token info
        state.token_usage.update(usage_summary)

        # Log recommendations if any
        if usage_summary["recommendations"]:
            for rec in usage_summary["recommendations"]:
                logger.info(f"Token recommendation: {rec}")

        return {"token_status": status, "token_usage": usage_summary}

    def route_by_token_status(self, state: dict[str, Any]) -> str:
        """Route based on token usage status.
        """
        status = state.get("token_status", "OK")

        if status == "EMERGENCY":
            return "rewrite"  # Most aggressive compression
        if status == "CRITICAL":
            return "summarize"  # Summarize memories
        if status == "WARNING" and self.memory_config.enable_running_summary:
            return "update_summary"  # Update running summary
        return "ok"

    def summarize_memories_node(self, state: MemoryState) -> dict[str, Any]:
        """Summarize memories to reduce token usage.
        """
        try:
            # Get memories to summarize (exclude recent ones)
            all_memories = state.current_memories
            if len(all_memories) <= self.memory_config.preserve_recent_memories:
                return {
                    "summarization_skipped": "Too few memories to summarize"}

            # Split into memories to summarize and preserve
            to_summarize = all_memories[: -
                                        self.memory_config.preserve_recent_memories]
            to_preserve = all_memories[-self.memory_config.preserve_recent_memories:]

            # Create text from memories to summarize
            memories_text = "\n\n".join(
                [f"[{m.metadata.memory_type}] {m.content}" for m in to_summarize]
            )

            # Calculate target tokens
            current_tokens = self.token_tracker.estimate_tokens_for_content(
                memories_text
            )
            target_tokens = int(
                current_tokens * self.memory_config.target_compression_ratio
            )

            # Use engine to summarize
            if self.engine and self.memory_summarization_prompt:
                prompt = self.memory_summarization_prompt
                summary_input = prompt.format_messages(
                    memories_text=memories_text, target_tokens=target_tokens
                )

                # Execute summarization
                summary_response = self.engine.invoke(summary_input)
                summary_text = (
                    summary_response.content
                    if hasattr(summary_response, "content")
                    else str(summary_response)
                )

                # Create summarized memory entry
                summarized_memory = EnhancedMemoryItem(
                    id=f"summary_{datetime.now().timestamp()}",
                    content=summary_text,
                    source="summarization",
                    memory_type=MemoryType.SUMMARY,
                    importance=ImportanceLevel.HIGH,
                    tags=["summary"],
                    confidence=0.9,
                    metadata={"summarization_type": "critical_threshold"},
                )

                # Update state with new memory list
                new_memories = [summarized_memory, *to_preserve]

                # Track summarization
                self.last_summarization = {
                    "timestamp": datetime.now().isoformat(),
                    "original_count": len(to_summarize),
                    "original_tokens": current_tokens,
                    "summary_tokens": self.token_tracker.estimate_tokens_for_content(
                        summary_text
                    ),
                    "compression_ratio": len(summary_text) / len(memories_text),
                }

                # Reset token tracker after summarization
                self.token_tracker.reset_tokens(keep_history=True)

                return {
                    "current_memories": new_memories,
                    "last_operation": {
                        "type": "summarization",
                        "details": self.last_summarization,
                    },
                }

            return {"summarization_skipped": "No summarization engine available"}

        except Exception as e:
            logger.exception(f"Error in summarization: {e}")
            return {"summarization_error": str(e)}

    def rewrite_memories_node(self, state: MemoryState) -> dict[str, Any]:
        """Rewrite memories for maximum compression.
        """
        try:
            # Similar to summarization but more aggressive
            # Rewrite each memory individually for compression
            rewritten_memories = []

            for memory in state.current_memories:
                if memory.metadata.memory_type == "meta":
                    # Skip already summarized memories
                    rewritten_memories.append(memory)
                    continue

                # Use rewrite prompt
                if self.engine and hasattr(
                        self.engine, "memory_rewrite_prompt"):
                    prompt = self.engine.memory_rewrite_prompt
                    rewrite_input = prompt.format_messages(
                        memory_content=memory.content,
                        compression_ratio=int(
                            self.memory_config.target_compression_ratio * 100
                        ),
                    )

                    response = self.engine.invoke(rewrite_input)
                    rewritten_content = (
                        response.content
                        if hasattr(response, "content")
                        else str(response)
                    )

                    # Create rewritten memory
                    rewritten_memory = EnhancedMemoryItem(
                        id=memory.id,
                        content=rewritten_content,
                        source="rewrite",
                        memory_type=memory.memory_type,
                        importance=memory.importance,
                        tags=memory.tags,
                        confidence=memory.confidence,
                        metadata={
                            **memory.metadata,
                            "original_source": memory.source},
                    )
                    rewritten_memories.append(rewritten_memory)
                else:
                    rewritten_memories.append(memory)

            # Reset token tracker
            self.token_tracker.reset_tokens(keep_history=True)

            return {
                "current_memories": rewritten_memories,
                "last_operation": {
                    "type": "rewrite",
                    "count": len(rewritten_memories),
                    "timestamp": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.exception(f"Error in memory rewriting: {e}")
            return {"rewrite_error": str(e)}

    def update_running_summary_node(
            self, state: MemoryState) -> dict[str, Any]:
        """Update the running summary with new memories.
        """
        try:
            if not self.memory_config.enable_running_summary:
                return {}

            # Get recent memories not in summary
            recent_memories = state.current_memories[-5:]  # Last 5 memories

            if not recent_memories:
                return {}

            new_memories_text = "\n".join(
                [f"[{m.metadata.memory_type}] {m.content}" for m in recent_memories]
            )

            # Update or create running summary
            if self.running_summary and self.engine:
                # Update existing summary
                prompt = self.engine.running_summary_prompt
                update_input = prompt.format_messages(
                    current_summary=self.running_summary,
                    new_memories=new_memories_text,
                    target_tokens=self.memory_config.running_summary_max_tokens,
                )

                response = self.engine.invoke(update_input)
                self.running_summary = (
                    response.content if hasattr(
                        response, "content") else str(response))
            else:
                # Create initial summary
                self.running_summary = f"Summary of memories:\n{new_memories_text}"

            # Store running summary in state
            state.memory_metadata["running_summary"] = self.running_summary

            return {
                "running_summary_updated": True,
                "summary_length": len(self.running_summary),
            }

        except Exception as e:
            logger.exception(f"Error updating running summary: {e}")
            return {"summary_error": str(e)}

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_memory_status(self) -> dict[str, Any]:
        """Get comprehensive memory and token status.
        """
        token_summary = self.token_tracker.get_usage_summary()

        return {
            "agent_name": self.name,
            "token_status": token_summary,
            "memory_config": {
                "max_tokens": self.memory_config.max_context_tokens,
                "summarization_threshold": self.memory_config.max_tokens_before_summary,
                "compression_ratio": self.memory_config.target_compression_ratio,
                "strategy": self.memory_config.summarization_strategy,
            },
            "last_summarization": self.last_summarization,
            "has_running_summary": self.running_summary is not None,
            "running_summary_tokens": (
                self.token_tracker.estimate_tokens_for_content(
                    self.running_summary) if self.running_summary else 0),
        }

    def __repr__(self) -> str:
        """String representation.
        """
        token_status = self.token_tracker.get_status()
        return (
            f"SimpleMemoryAgent(name='{self.name}', "
            f"max_tokens={self.memory_config.max_context_tokens}, "
            f"token_status={token_status}, "
            f"strategy={self.memory_config.summarization_strategy})"
        )
