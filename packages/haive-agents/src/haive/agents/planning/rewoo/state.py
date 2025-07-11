"""ReWOO State Schema.

This module defines the state schema for ReWOO agents, tracking evidence
collection, tool execution, and reasoning progress.
"""

import logging
from typing import Any, Dict, Generic, List, Optional, Set, TypeVar

from haive.core.schema import StateSchema
from haive.core.schema.prebuilt.tool_state import ToolState
from pydantic import Field, computed_field, field_validator, model_validator

logger = logging.getLogger(__name__)

from haive.agents.planning.rewoo.models import (
    Evidence,
    EvidenceStatus,
    ReWOOPlan,
    ReWOOReasoning,
    ToolCall,
)


class ReWOOState(ToolState):
    """State for ReWOO agent with evidence tracking.

    This state extends ToolState to track:
    - Evidence collection progress
    - Tool execution results
    - Reasoning chain
    - Token usage across evidence gathering
    - Tool routing and validation

    Leverages existing ToolState functionality for:
    - Tool management and routing
    - Token tracking
    - Message history
    - Tool validation
    """

    # ========================================================================
    # PLANNING & OBJECTIVE
    # ========================================================================

    objective: str = Field(..., description="Main objective to achieve")

    plan: ReWOOPlan | None = Field(default=None, description="Current ReWOO plan")

    # ========================================================================
    # EVIDENCE TRACKING
    # ========================================================================

    evidence_map: dict[str, Evidence] = Field(
        default_factory=dict, description="Map of evidence ID to evidence objects"
    )

    evidence_collection_order: list[str] = Field(
        default_factory=list, description="Order in which evidence was collected"
    )

    failed_evidence_attempts: dict[str, list[str]] = Field(
        default_factory=dict, description="Map of evidence ID to error messages"
    )

    @field_validator("evidence_map")
    @classmethod
    def validate_evidence_map(cls, v: dict[str, Evidence]) -> dict[str, Evidence]:
        """Validate evidence map structure."""
        for eid, evidence in v.items():
            if evidence.id != eid:
                raise ValueError(f"Evidence ID mismatch: {eid} != {evidence.id}")
        return v

    # ========================================================================
    # TOOL EXECUTION - Inherits from ToolState
    # ========================================================================
    # tool_routes is inherited from ToolState
    # tools is inherited from ToolState
    # tool_types/tool_routes functionality is inherited

    tool_results: dict[str, Any] = Field(
        default_factory=dict, description="Raw results from tool executions"
    )

    active_tool_calls: list[ToolCall] = Field(
        default_factory=list, description="Currently executing tool calls"
    )

    # Evidence-specific tool mapping
    evidence_tool_mapping: dict[str, str] = Field(
        default_factory=dict, description="Map evidence IDs to specific tool names"
    )

    # ========================================================================
    # REASONING & OUTPUT
    # ========================================================================

    reasoning_chain: list[str] = Field(
        default_factory=list, description="Chain of reasoning steps"
    )

    final_reasoning: ReWOOReasoning | None = Field(
        default=None, description="Final structured reasoning output"
    )

    # ========================================================================
    # EXECUTION CONTROL
    # ========================================================================

    max_evidence_collection_rounds: int = Field(
        default=10, description="Maximum rounds of evidence collection"
    )

    current_collection_round: int = Field(
        default=0, description="Current evidence collection round"
    )

    allow_parallel_collection: bool = Field(
        default=True, description="Whether to collect evidence in parallel"
    )

    skip_failed_evidence: bool = Field(
        default=False, description="Whether to skip failed evidence and continue"
    )

    # ========================================================================
    # VALIDATORS
    # ========================================================================

    @model_validator(mode="after")
    def setup_rewoo_state(self) -> "ReWOOState":
        """Setup ReWOO-specific state after parent initialization."""
        # Initialize plan evidence map if needed
        if self.plan and not self.evidence_map:
            self.evidence_map = self.plan.evidence_map.copy()

        return self

    # ========================================================================
    # COMPUTED PROPERTIES
    # ========================================================================

    @computed_field
    @property
    def collected_evidence_ids(self) -> set[str]:
        """Get IDs of successfully collected evidence."""
        return {
            eid
            for eid, evidence in self.evidence_map.items()
            if evidence.status == EvidenceStatus.COLLECTED
        }

    @computed_field
    @property
    def pending_evidence_ids(self) -> set[str]:
        """Get IDs of pending evidence."""
        return {
            eid
            for eid, evidence in self.evidence_map.items()
            if evidence.status == EvidenceStatus.PLANNED
        }

    @computed_field
    @property
    def evidence_completion_rate(self) -> float:
        """Calculate evidence collection completion rate."""
        if not self.evidence_map:
            return 0.0

        collected = len(self.collected_evidence_ids)
        total = len(self.evidence_map)

        return (collected / total) * 100

    @computed_field
    @property
    def ready_evidence(self) -> list[Evidence]:
        """Get evidence ready for collection (dependencies met)."""
        if not self.plan:
            return []

        ready = []
        for evidence in self.evidence_map.values():
            if evidence.status != EvidenceStatus.PLANNED:
                continue

            # Check dependencies
            deps_met = all(
                dep_id in self.collected_evidence_ids for dep_id in evidence.depends_on
            )

            if deps_met:
                ready.append(evidence)

        return ready

    @computed_field
    @property
    def is_evidence_complete(self) -> bool:
        """Check if all evidence collection is complete."""
        if not self.evidence_map:
            return True

        # All evidence either collected or failed (if skipping)
        for evidence in self.evidence_map.values():
            if evidence.status == EvidenceStatus.PLANNED:
                return False
            if (
                evidence.status == EvidenceStatus.FAILED
                and not self.skip_failed_evidence
            ):
                return False

        return True

    @computed_field
    @property
    def evidence_summary(self) -> dict[str, str]:
        """Get summary of collected evidence."""
        summary = {}

        for eid in self.evidence_collection_order:
            if eid in self.evidence_map:
                evidence = self.evidence_map[eid]
                if evidence.content is not None:
                    # Truncate long content
                    content_str = str(evidence.content)
                    if len(content_str) > 200:
                        content_str = content_str[:200] + "..."
                    summary[eid] = content_str

        return summary

    @computed_field
    @property
    def can_reason(self) -> bool:
        """Check if we have enough evidence to reason."""
        # Need at least some evidence collected
        if not self.collected_evidence_ids:
            return False

        # If we're skipping failed evidence, check if we have enough
        if self.skip_failed_evidence:
            # At least 50% collected
            return self.evidence_completion_rate >= 50.0
        # All evidence must be complete
        return self.is_evidence_complete

    # ========================================================================
    # STATE METHODS
    # ========================================================================

    def add_evidence(self, evidence: Evidence) -> None:
        """Add evidence to state."""
        self.evidence_map[evidence.id] = evidence

        # Map evidence to tool if specified
        if evidence.source:
            self.evidence_tool_mapping[evidence.id] = evidence.source

    def update_evidence(
        self,
        evidence_id: str,
        status: EvidenceStatus | None = None,
        content: Any | None = None,
        error: str | None = None,
    ) -> bool:
        """Update evidence in state."""
        if evidence_id not in self.evidence_map:
            return False

        evidence = self.evidence_map[evidence_id]

        if status is not None:
            evidence.status = status

        if content is not None:
            evidence.content = content
            if evidence_id not in self.evidence_collection_order:
                self.evidence_collection_order.append(evidence_id)

        if error is not None:
            evidence.error = error
            if evidence_id not in self.failed_evidence_attempts:
                self.failed_evidence_attempts[evidence_id] = []
            self.failed_evidence_attempts[evidence_id].append(error)

        return True

    def add_tool_result(self, tool_name: str, result: Any) -> None:
        """Add tool execution result."""
        self.tool_results[tool_name] = result

    def add_reasoning_step(self, step: str) -> None:
        """Add a reasoning step."""
        self.reasoning_chain.append(step)

    def resolve_evidence_in_text(self, text: str) -> str:
        """Resolve evidence references in text."""
        resolved = text

        for eid, evidence in self.evidence_map.items():
            if evidence.content is not None:
                # Replace #E1 with actual content
                resolved = resolved.replace(eid, str(evidence.content))

        return resolved

    def get_evidence_context(self) -> str:
        """Get formatted evidence context for prompts."""
        lines = ["Collected Evidence:"]

        for eid in self.evidence_collection_order:
            if eid in self.evidence_map:
                evidence = self.evidence_map[eid]
                if evidence.content is not None:
                    lines.append(f"{eid}: {evidence.description}")
                    lines.append(f"   Content: {evidence.content}")

        if self.failed_evidence_attempts:
            lines.append("\nFailed Evidence:")
            for eid, errors in self.failed_evidence_attempts.items():
                if eid in self.evidence_map:
                    evidence = self.evidence_map[eid]
                    lines.append(f"{eid}: {evidence.description}")
                    lines.append(f"   Errors: {'; '.join(errors)}")

        return "\n".join(lines)

    def increment_collection_round(self) -> bool:
        """Increment collection round and check if we should continue."""
        self.current_collection_round += 1
        return self.current_collection_round < self.max_evidence_collection_rounds

    def to_reasoning_context(self) -> dict[str, Any]:
        """Create context for final reasoning."""
        return {
            "objective": self.objective,
            "evidence_summary": self.evidence_summary,
            "evidence_context": self.get_evidence_context(),
            "reasoning_chain": self.reasoning_chain,
            "completion_rate": self.evidence_completion_rate,
            "failed_evidence": list(self.failed_evidence_attempts.keys()),
        }


# Type variable for generic ReWOO states
TReWOOState = TypeVar("TReWOOState", bound=ReWOOState)


class ReWOOStateWithRouting(ReWOOState):
    """Extended ReWOO state with advanced tool routing capabilities.

    This leverages ToolState's existing routing capabilities while adding
    ReWOO-specific routing features.
    """

    # Additional routing fields
    tool_route_overrides: dict[str, str] = Field(
        default_factory=dict, description="Override routes for specific tools"
    )

    failed_tool_fallbacks: dict[str, list[str]] = Field(
        default_factory=dict, description="Fallback tools for failed executions"
    )

    @computed_field
    @property
    def effective_tool_routes(self) -> dict[str, str]:
        """Get effective tool routes with overrides applied."""
        # Use parent's tool_routes from ToolState
        routes = self.tool_routes.copy() if hasattr(self, "tool_routes") else {}
        routes.update(self.tool_route_overrides)
        return routes

    def get_tool_for_evidence(self, evidence_id: str) -> Any | None:
        """Get the designated tool for collecting specific evidence."""
        tool_name = self.evidence_tool_mapping.get(evidence_id)
        if tool_name:
            # Use parent's get_tool_by_name from ToolState
            return self.get_tool_by_name(tool_name)
        return None

    def get_fallback_tools(self, tool_name: str) -> list[str]:
        """Get fallback tools for a failed tool."""
        return self.failed_tool_fallbacks.get(tool_name, [])
