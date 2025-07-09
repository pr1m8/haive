# ============================================================================
# LTM AGENT - Long-Term Memory Agent
# ============================================================================
"""
Long-Term Memory Agent implementation following Haive patterns.

This agent integrates LangMem functionality within the Haive framework,
providing memory extraction, processing, and tool-based memory management.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


# ============================================================================
# STATE SCHEMA
# ============================================================================


class LTMState(BaseModel):
    """LTM Agent State following Haive patterns.

    This state schema tracks the progression through memory processing stages
    and maintains all necessary data for the LTM workflow.
    """

    # Core message state (required by LangGraph)
    messages: List[AnyMessage] = Field(
        default_factory=list, description="Conversation messages"
    )

    # Processing control
    processing_stage: str = Field(
        default="extract",
        description="Current processing stage: extract -> kg -> categorize -> consolidate -> store -> tools",
    )
    processing_complete: bool = Field(
        default=False, description="Whether all processing is complete"
    )

    # Memory data
    extracted_memories: List[Dict[str, Any]] = Field(
        default_factory=list, description="Extracted memories from conversation"
    )
    knowledge_graph: Optional[Dict[str, Any]] = Field(
        default=None, description="Extracted knowledge graph entities and relationships"
    )
    categories: List[str] = Field(
        default_factory=list, description="Memory categories from TNT classification"
    )
    consolidated_memories: List[Dict[str, Any]] = Field(
        default_factory=list, description="Consolidated and refined memories"
    )

    # Processing results
    processing_errors: List[str] = Field(
        default_factory=list, description="Any errors encountered during processing"
    )
    tool_calls_needed: bool = Field(
        default=False, description="Whether memory tools should be activated"
    )
    reflection_scheduled: bool = Field(
        default=False, description="Whether background reflection has been scheduled"
    )

    # Quality metrics
    extraction_quality: float = Field(
        default=0.0, description="Quality score for memory extraction (0.0-1.0)"
    )
    processing_quality: float = Field(
        default=0.0, description="Overall processing quality score (0.0-1.0)"
    )

    # Configuration flags
    enable_kg_processing: bool = Field(
        default=True, description="Enable knowledge graph processing"
    )
    enable_categorization: bool = Field(
        default=True, description="Enable memory categorization"
    )
    enable_consolidation: bool = Field(
        default=True, description="Enable memory consolidation"
    )
    enable_reflection: bool = Field(
        default=True, description="Enable background reflection"
    )

    # Metadata
    processing_started_at: Optional[datetime] = Field(
        default=None, description="When processing started"
    )
    processing_completed_at: Optional[datetime] = Field(
        default=None, description="When processing completed"
    )


# ============================================================================
# CONDITION FUNCTIONS (Following SimpleAgent Pattern)
# ============================================================================


def extraction_succeeded(state: LTMState) -> bool:
    """Check if memory extraction succeeded."""
    return bool(state.extracted_memories)


def has_processing_errors(state: LTMState) -> bool:
    """Check if there are critical processing errors."""
    return len(state.processing_errors) > 0


def needs_kg_processing(state: LTMState) -> bool:
    """Check if KG processing is needed."""
    return (
        state.enable_kg_processing
        and bool(state.extracted_memories)
        and not state.knowledge_graph
        and len(state.extracted_memories) >= 2
    )


def needs_categorization(state: LTMState) -> bool:
    """Check if categorization is needed."""
    return (
        state.enable_categorization
        and bool(state.extracted_memories)
        and not state.categories
        and len(state.extracted_memories) >= 3
    )


def needs_consolidation(state: LTMState) -> bool:
    """Check if consolidation is needed."""
    return (
        state.enable_consolidation
        and bool(state.extracted_memories)
        and len(state.extracted_memories) >= 5
    )


def needs_tool_activation(state: LTMState) -> bool:
    """Check if memory tools should be activated."""
    return state.tool_calls_needed


def processing_complete(state: LTMState) -> bool:
    """Check if all processing is complete."""
    return state.processing_complete


# ============================================================================
# LTM AGENT
# ============================================================================


class LTMAgent(Agent):
    """Long-Term Memory Agent with LangMem integration.

    This agent provides comprehensive memory management capabilities including:
    - Memory extraction from conversations using LangMem
    - Knowledge graph processing using Haive KG extraction
    - Memory categorization using TNT taxonomy
    - Memory consolidation and quality improvement
    - Tool-based memory management interface
    - Background reflection processing

    The agent follows Haive patterns with proper conditional edges and state management.
    """

    # Configuration fields
    enable_kg_processing: bool = Field(
        default=True, description="Enable knowledge graph extraction"
    )
    enable_categorization: bool = Field(
        default=True, description="Enable memory categorization"
    )
    enable_consolidation: bool = Field(
        default=True, description="Enable memory consolidation"
    )
    enable_reflection: bool = Field(
        default=True, description="Enable background reflection"
    )
    ltm_llm_config: Optional[LLMConfig] = Field(
        default=None, description="LLM configuration for memory processing"
    )

    def __init__(
        self,
        name: str = "LTM Agent",
        llm_config: Optional[LLMConfig] = None,
        enable_kg_processing: bool = True,
        enable_categorization: bool = True,
        enable_consolidation: bool = True,
        enable_reflection: bool = True,
        **kwargs,
    ):
        """Initialize LTM agent.

        Args:
            name: Agent name
            llm_config: LLM configuration for memory processing
            enable_kg_processing: Enable knowledge graph extraction
            enable_categorization: Enable memory categorization
            enable_consolidation: Enable memory consolidation
            enable_reflection: Enable background reflection
            **kwargs: Additional Agent arguments
        """
        # Set state schema
        kwargs.setdefault("state_schema", LTMState)

        # Set configuration values
        kwargs.update(
            {
                "enable_kg_processing": enable_kg_processing,
                "enable_categorization": enable_categorization,
                "enable_consolidation": enable_consolidation,
                "enable_reflection": enable_reflection,
                "ltm_llm_config": llm_config
                or LLMConfig(provider="anthropic", model="claude-3-haiku-20240307"),
            }
        )

        super().__init__(name=name, **kwargs)

        logger.info(
            f"LTMAgent '{self.name}' initialized with features: "
            f"KG={self.enable_kg_processing}, "
            f"Categorization={self.enable_categorization}, "
            f"Consolidation={self.enable_consolidation}, "
            f"Reflection={self.enable_reflection}"
        )

    def setup_agent(self):
        """Setup LTM agent engines and components."""
        logger.info("Setting up LTM agent engines...")

        # For now, we'll create placeholder engines
        # These will be replaced with actual LangMem and Haive components

        # Memory extraction engine (will use LangMem memory manager)
        self.engines["memory_extractor"] = AugLLMConfig(
            name="memory_extractor",
            llm_config=self.ltm_llm_config,
            system_message="You extract structured memories from conversations.",
        )

        logger.info("LTM agent setup complete")

    def build_graph(self) -> BaseGraph:
        """Build LTM graph with proper conditional edges.

        This is the FIRST PHASE - just memory extraction and basic routing.
        We'll add more nodes incrementally.
        """
        logger.info("Building LTM graph (Phase 1: Extraction only)...")

        graph = BaseGraph(name=self.name)

        # ============================================================================
        # PHASE 1 NODES - Start with just extraction
        # ============================================================================

        # Memory extraction node
        graph.add_node("extract_memories", self.extract_memories_node)

        # Simple completion node for now
        graph.add_node("complete_processing", self.complete_processing_node)

        # Error handling node
        graph.add_node("handle_errors", self.handle_errors_node)

        # ============================================================================
        # PHASE 1 EDGES - Simple extraction flow
        # ============================================================================

        # Start with extraction
        graph.add_edge(START, "extract_memories")

        # After extraction - route based on success/failure (following SimpleAgent pattern)
        graph.add_conditional_edges(
            "extract_memories",
            extraction_succeeded,
            {
                True: "complete_processing",  # For now, just complete after extraction
                False: "handle_errors",
            },
        )

        # Complete processing goes to end
        graph.add_edge("complete_processing", END)

        # Error handling goes to end (for now)
        graph.add_edge("handle_errors", END)

        logger.info("LTM graph built successfully (Phase 1)")
        return graph

    # ============================================================================
    # NODE IMPLEMENTATIONS - Phase 1
    # ============================================================================

    def extract_memories_node(self, state: LTMState) -> Dict[str, Any]:
        """Extract memories using LangMem memory manager (Phase 2 implementation)."""
        logger.info("Executing LangMem memory extraction...")

        try:
            # Import LangMem components
            from langmem import create_memory_manager

            from haive.agents.ltm.memory_schemas import DEFAULT_MEMORY_SCHEMAS

            if not state.messages:
                return {
                    "processing_errors": ["No messages to extract memories from"],
                    "processing_stage": "error",
                }

            # Create LangMem memory manager (model is positional argument)
            manager = create_memory_manager(
                self.ltm_llm_config.model,  # model as positional argument
                schemas=DEFAULT_MEMORY_SCHEMAS,
                instructions="Extract key memories, preferences, and important information from this conversation. Focus on facts, preferences, context, and actionable information.",
                enable_inserts=True,
                enable_updates=True,
            )

            # Prepare input state for LangMem
            input_state = {
                "messages": state.messages,
                "max_steps": 3,  # Control extraction depth
            }

            # Add existing memories if available for updates
            if state.extracted_memories:
                # Convert existing memories back to LangMem format if needed
                # For now, skip this - will implement in later phase
                pass

            # Extract memories using LangMem
            logger.info(f"Extracting memories from {len(state.messages)} messages...")
            extracted_memories = manager.invoke(input_state)  # Sync for now

            # Process LangMem results
            memories_data = []
            for memory in extracted_memories:
                memory_dict = {
                    "memory_id": memory.id,
                    "content": (
                        memory.content.model_dump()
                        if hasattr(memory.content, "model_dump")
                        else str(memory.content)
                    ),
                    "schema": memory.content.__class__.__name__,
                    "timestamp": datetime.now().isoformat(),
                    "source": "langmem_extraction",
                    "confidence": getattr(memory.content, "confidence", 0.8),
                }
                memories_data.append(memory_dict)

            # Calculate quality score based on extraction results
            quality = self._calculate_extraction_quality(memories_data, state.messages)

            logger.info(
                f"LangMem extracted {len(memories_data)} memories with quality {quality:.2f}"
            )

            return {
                "extracted_memories": memories_data,
                "extraction_quality": quality,
                "processing_stage": "complete",  # For Phase 2, still go to complete
                "processing_started_at": datetime.now(),
            }

        except Exception as e:
            logger.error(f"LangMem memory extraction failed: {e}")
            return {
                "processing_errors": [f"Extraction failed: {str(e)}"],
                "processing_stage": "error",
            }

    def _calculate_extraction_quality(
        self, memories: List[Dict], messages: List
    ) -> float:
        """Calculate quality score for extracted memories."""
        if not memories:
            return 0.0

        # Base quality on memory count vs message count ratio
        message_count = len(messages)
        memory_count = len(memories)

        # Expect roughly 1 memory per 2-3 messages for good quality
        expected_ratio = message_count / 2.5
        actual_ratio = memory_count

        # Quality based on how close we are to expected ratio
        if expected_ratio == 0:
            return 0.0

        ratio_quality = min(1.0, actual_ratio / expected_ratio)

        # Bonus for schema diversity
        schema_types = set(m.get("schema", "Unknown") for m in memories)
        diversity_bonus = min(0.2, len(schema_types) * 0.05)

        # Penalty for errors or low confidence
        avg_confidence = sum(m.get("confidence", 0.8) for m in memories) / len(memories)

        final_quality = min(1.0, ratio_quality + diversity_bonus) * avg_confidence
        return round(final_quality, 2)

    def complete_processing_node(self, state: LTMState) -> Dict[str, Any]:
        """Complete processing (Phase 1 implementation)."""
        logger.info("Completing LTM processing...")

        return {
            "processing_complete": True,
            "processing_completed_at": datetime.now(),
            "processing_quality": state.extraction_quality,
        }

    def handle_errors_node(self, state: LTMState) -> Dict[str, Any]:
        """Handle processing errors."""
        logger.error(f"Handling LTM processing errors: {state.processing_errors}")

        # For now, just log errors and mark as complete
        return {
            "processing_complete": True,
            "processing_completed_at": datetime.now(),
            "processing_quality": 0.0,
        }

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def get_processing_summary(self, state: LTMState) -> Dict[str, Any]:
        """Get summary of processing results."""
        return {
            "stage": state.processing_stage,
            "memories_extracted": len(state.extracted_memories),
            "quality_score": state.processing_quality,
            "errors": len(state.processing_errors),
            "completed": state.processing_complete,
        }

    def __repr__(self) -> str:
        return (
            f"LTMAgent(name='{self.name}', "
            f"kg={self.enable_kg_processing}, "
            f"categorization={self.enable_categorization}, "
            f"consolidation={self.enable_consolidation})"
        )
