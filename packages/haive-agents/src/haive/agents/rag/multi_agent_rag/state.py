"""Enhanced RAG State Schema for Multi-Agent RAG Systems.

This module provides comprehensive state management for complex RAG workflows,
supporting document processing, grading, multi-step retrieval, and conditional routing.
"""

import operator
from enum import Enum
from typing import Annotated, Any

from haive.core.schema.state_schema import StateSchema
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class RAGOperationType(str, Enum):
    """Types of RAG operations that can be performed."""

    RETRIEVE = "retrieve"
    GRADE = "grade"
    GENERATE = "generate"
    REFINE = "refine"
    VERIFY = "verify"
    ROUTE = "route"


class QueryStatus(str, Enum):
    """Status of query processing."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REFINEMENT = "needs_refinement"


class DocumentGradingResult(BaseModel):
    """Result of document grading process."""

    document_id: str = Field(description="Document identifier")
    document: Document = Field(description="The original document")
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score")
    is_relevant: bool = Field(description="Whether document passed relevance check")
    grading_reason: str = Field(description="Reason for grading decision")
    grader_type: str = Field(description="Type of grader used (binary, numeric, etc.)")


class RAGStep(BaseModel):
    """Represents a single step in the RAG workflow."""

    step_id: str = Field(description="Unique identifier for this step")
    operation_type: RAGOperationType = Field(description="Type of operation performed")
    input_data: dict[str, Any] = Field(
        default_factory=dict, description="Input data for this step"
    )
    output_data: dict[str, Any] = Field(
        default_factory=dict, description="Output data from this step"
    )
    timestamp: str | None = Field(
        default=None, description="When this step was executed"
    )
    agent_name: str | None = Field(
        default=None, description="Which agent performed this step"
    )


class MultiAgentRAGState(StateSchema):
    """Comprehensive state schema for multi-agent RAG systems.

    Supports complex RAG workflows with document grading, multi-step retrieval,
    conditional routing, and state tracking across multiple agents.
    """

    # Core RAG Fields
    query: str = Field(description="The original user query")
    queries: Annotated[list[str], operator.add] = Field(
        default_factory=list,
        description="All queries processed (original + refined/decomposed)",
    )

    # Document Management
    documents: Annotated[list[Document], operator.add] = Field(
        default_factory=list, description="All available documents in the system"
    )
    retrieved_documents: Annotated[list[Document], operator.add] = Field(
        default_factory=list, description="Documents retrieved for current query"
    )
    graded_documents: Annotated[list[DocumentGradingResult], operator.add] = Field(
        default_factory=list,
        description="Documents that have been graded for relevance",
    )
    filtered_documents: Annotated[list[Document], operator.add] = Field(
        default_factory=list, description="Documents that passed relevance filtering"
    )

    # Generation and Responses
    generated_answer: str = Field(
        default="", description="Generated answer from RAG process"
    )
    intermediate_answers: Annotated[list[str], operator.add] = Field(
        default_factory=list,
        description="Intermediate answers during multi-step generation",
    )

    # Workflow Control
    query_status: QueryStatus = Field(
        default=QueryStatus.PENDING, description="Current status of query processing"
    )
    current_operation: RAGOperationType | None = Field(
        default=None, description="Currently executing operation"
    )
    next_operation: RAGOperationType | None = Field(
        default=None, description="Next planned operation"
    )

    # Step Tracking
    workflow_steps: Annotated[list[RAGStep], operator.add] = Field(
        default_factory=list, description="Complete workflow history"
    )

    # Quality Metrics
    retrieval_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence in document retrieval quality",
    )
    generation_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence in answer generation quality",
    )
    overall_quality_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Overall quality assessment of the RAG process",
    )

    # Agent Coordination
    active_agent: str | None = Field(
        default=None, description="Currently active agent name"
    )
    agent_decisions: Annotated[dict[str, Any], operator.add] = Field(
        default_factory=dict, description="Decisions made by different agents"
    )
    routing_decisions: Annotated[list[dict[str, Any]], operator.add] = Field(
        default_factory=list, description="History of routing decisions"
    )

    # Error Handling
    errors: Annotated[list[str], operator.add] = Field(
        default_factory=list, description="Any errors encountered during processing"
    )
    warnings: Annotated[list[str], operator.add] = Field(
        default_factory=list, description="Warnings generated during processing"
    )

    # Messages (inherited from StateSchema)
    messages: Annotated[list[BaseMessage], operator.add] = Field(
        default_factory=list, description="Conversation messages"
    )

    # Configuration and Context
    retrieval_config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for retrieval process"
    )
    generation_config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for generation process"
    )
    grading_config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for document grading"
    )

    # Schema Metadata
    __shared_fields__ = [
        "messages",
        "queries",
        "documents",
        "retrieved_documents",
        "graded_documents",
        "filtered_documents",
        "workflow_steps",
        "intermediate_answers",
        "agent_decisions",
        "routing_decisions",
        "errors",
        "warnings",
    ]

    __reducer_fields__ = {
        "queries": operator.add,
        "documents": operator.add,
        "retrieved_documents": operator.add,
        "graded_documents": operator.add,
        "filtered_documents": operator.add,
        "workflow_steps": operator.add,
        "intermediate_answers": operator.add,
        "agent_decisions": operator.add,
        "routing_decisions": operator.add,
        "errors": operator.add,
        "warnings": operator.add,
        "messages": operator.add,
    }

    def add_workflow_step(
        self,
        operation_type: RAGOperationType,
        agent_name: str,
        input_data: dict[str, Any] | None = None,
        output_data: dict[str, Any] | None = None,
    ) -> str:
        """Add a new workflow step."""
        import uuid
        from datetime import datetime

        step_id = str(uuid.uuid4())[:8]
        step = RAGStep(
            step_id=step_id,
            operation_type=operation_type,
            agent_name=agent_name,
            input_data=input_data or {},
            output_data=output_data or {},
            timestamp=datetime.now().isoformat(),
        )
        self.workflow_steps.append(step)
        return step_id

    def get_relevant_documents(self, min_score: float = 0.5) -> list[Document]:
        """Get documents that passed relevance threshold."""
        return [
            result.document
            for result in self.graded_documents
            if result.relevance_score >= min_score and result.is_relevant
        ]

    def update_quality_metrics(self) -> None:
        """Update quality metrics based on current state."""
        if self.graded_documents:
            # Calculate retrieval confidence based on graded documents
            relevant_count = sum(1 for doc in self.graded_documents if doc.is_relevant)
            self.retrieval_confidence = relevant_count / len(self.graded_documents)

        # Overall quality is average of retrieval and generation confidence
        if self.retrieval_confidence > 0 and self.generation_confidence > 0:
            self.overall_quality_score = (
                self.retrieval_confidence + self.generation_confidence
            ) / 2

    def should_refine_query(self) -> bool:
        """Determine if query should be refined based on state."""
        return (
            self.retrieval_confidence < 0.3
            or len(self.get_relevant_documents()) == 0
            or self.query_status == QueryStatus.NEEDS_REFINEMENT
        )

    def get_latest_step(
        self, operation_type: RAGOperationType | None = None
    ) -> RAGStep | None:
        """Get the most recent workflow step, optionally filtered by operation type."""
        steps = self.workflow_steps
        if operation_type:
            steps = [step for step in steps if step.operation_type == operation_type]

        return steps[-1] if steps else None


# Convenience aliases for backward compatibility
RAGState = MultiAgentRAGState
EnhancedRAGState = MultiAgentRAGState
