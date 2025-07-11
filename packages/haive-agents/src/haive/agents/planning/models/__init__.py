# src/haive/agents/unified_planner/models/base.py
"""Base models for the unified planning system.

This module provides the foundation for a tree-based planning and execution system
that unifies Plan-and-Execute, ReWOO, and LLM Compiler patterns into a single,
resource-aware framework.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    computed_field,
    field_validator,
    model_validator,
)

# ============================================================================
# ENUMS
# ============================================================================


class NodeStatus(str, Enum):
    """Execution status of any plan node."""

    PENDING = "pending"  # Not yet started
    ANALYZING = "analyzing"  # Being analyzed for resource needs
    SCHEDULED = "scheduled"  # Scheduled for execution
    WAITING = "waiting"  # Waiting for dependencies
    READY = "ready"  # Ready to execute
    RUNNING = "running"  # Currently executing
    COMPLETED = "completed"  # Successfully completed
    FAILED = "failed"  # Execution failed
    SKIPPED = "skipped"  # Skipped due to conditions
    CANCELLED = "cancelled"  # Cancelled by user/system
    REPLANNING = "replanning"  # Being replanned due to failure


class ResourceType(str, Enum):
    """Types of resources that nodes can require."""

    TOKENS = "tokens"  # LLM tokens
    COMPUTE = "compute"  # CPU/GPU compute units
    MEMORY = "memory"  # Memory in MB
    TIME = "time"  # Time in seconds
    EXPERTS = "experts"  # Number of expert agents
    API_CALLS = "api_calls"  # External API call quota
    TOOLS = "tools"  # Specific tool availability


class CompletionCriteria(str, Enum):
    """How to determine if a container node is complete."""

    ALL = "all"  # All children must complete
    ANY = "any"  # Any child completion is enough
    MAJORITY = "majority"  # More than half must complete
    CUSTOM = "custom"  # Custom completion function
    THRESHOLD = "threshold"  # Specific number must complete


# ============================================================================
# RESOURCE MODELS
# ============================================================================


class ResourceRequirement(BaseModel):
    """Resource requirements for a node."""

    model_config = ConfigDict(validate_assignment=True)

    resource_type: ResourceType = Field(..., description="Type of resource needed")

    amount: float = Field(..., description="Amount of resource required", gt=0)

    priority: int = Field(
        default=1, description="Priority for resource allocation (1-10)", ge=1, le=10
    )

    flexible: bool = Field(
        default=False, description="Whether the amount can be reduced if needed"
    )

    minimum: float | None = Field(
        default=None, description="Minimum amount if flexible", gt=0
    )

    @model_validator(mode="after")
    def validate_minimum(self) -> ResourceRequirement:
        """Ensure minimum is less than amount if flexible."""
        if self.flexible and self.minimum is not None and self.minimum > self.amount:
            raise ValueError("Minimum must be less than requested amount")
        return self


class ResourceAllocation(BaseModel):
    """Actual resources allocated to a node."""

    model_config = ConfigDict(validate_assignment=True)

    allocations: dict[ResourceType, float] = Field(
        default_factory=dict, description="Allocated amounts by resource type"
    )

    allocated_at: datetime = Field(
        default_factory=datetime.now, description="When resources were allocated"
    )

    expires_at: datetime | None = Field(
        default=None, description="When allocation expires"
    )

    utilization: dict[ResourceType, float] = Field(
        default_factory=dict, description="Actual utilization (0-1)"
    )


# ============================================================================
# EXECUTION METADATA
# ============================================================================


class ExecutionMetrics(BaseModel):
    """Metrics collected during node execution."""

    model_config = ConfigDict(validate_assignment=True)

    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)

    tokens_used: int = Field(default=0, description="Total tokens consumed", ge=0)

    api_calls_made: int = Field(
        default=0, description="Number of external API calls", ge=0
    )

    errors_encountered: list[str] = Field(
        default_factory=list, description="Errors during execution"
    )

    retry_count: int = Field(default=0, description="Number of retry attempts", ge=0)

    @computed_field
    @property
    def duration_seconds(self) -> float | None:
        """Calculate execution duration."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    @computed_field
    @property
    def success_rate(self) -> float:
        """Calculate success rate based on retries."""
        if self.retry_count == 0:
            return 1.0 if not self.errors_encountered else 0.0
        return 0.0 if self.errors_encountered else 1.0 / (self.retry_count + 1)


# ============================================================================
# BASE PLAN NODE
# ============================================================================


class PlanNode(BaseModel):
    """Base class for all nodes in the planning tree.

    This is the fundamental building block that enables AutoTree integration.
    All plan elements inherit from this, creating a unified tree structure.
    """

    model_config = ConfigDict(
        validate_assignment=True, use_enum_values=True, extra="forbid"
    )

    # ========================================================================
    # IDENTITY
    # ========================================================================

    id: str = Field(
        default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}",
        description="Unique identifier for this node",
    )

    name: str = Field(
        ..., description="Human-readable name", min_length=1, max_length=200
    )

    description: str = Field(
        default="", description="Detailed description of purpose", max_length=1000
    )

    node_type: str = Field(
        default="base", description="Type identifier for polymorphic handling"
    )

    # ========================================================================
    # EXECUTION STATE
    # ========================================================================

    status: NodeStatus = Field(
        default=NodeStatus.PENDING, description="Current execution status"
    )

    result: Any | None = Field(
        default=None, description="Execution result (type depends on node)"
    )

    error: str | None = Field(default=None, description="Error message if failed")

    # ========================================================================
    # DEPENDENCIES
    # ========================================================================

    depends_on: set[str] = Field(
        default_factory=set, description="IDs of nodes that must complete first"
    )

    blocks: set[str] = Field(
        default_factory=set, description="IDs of nodes blocked by this one"
    )

    # ========================================================================
    # RESOURCES
    # ========================================================================

    resource_requirements: list[ResourceRequirement] = Field(
        default_factory=list, description="Resources needed for execution"
    )

    resource_allocation: ResourceAllocation | None = Field(
        default=None, description="Actually allocated resources"
    )

    # ========================================================================
    # SCHEDULING
    # ========================================================================

    earliest_start: datetime | None = Field(
        default=None, description="Earliest this can start"
    )

    latest_start: datetime | None = Field(
        default=None, description="Latest this should start"
    )

    estimated_duration: float | None = Field(
        default=None, description="Estimated execution time in seconds", gt=0
    )

    priority: int = Field(
        default=5, description="Execution priority (1-10)", ge=1, le=10
    )

    # ========================================================================
    # EXECUTION METADATA
    # ========================================================================

    metrics: ExecutionMetrics = Field(
        default_factory=ExecutionMetrics, description="Execution metrics"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    # ========================================================================
    # PRIVATE ATTRIBUTES
    # ========================================================================

    _parent: PlanNode | None = PrivateAttr(default=None)
    _children: list[PlanNode] = PrivateAttr(default_factory=list)
    _tree_depth: int = PrivateAttr(default=0)

    # ========================================================================
    # VALIDATORS
    # ========================================================================

    @field_validator("depends_on", "blocks")
    @classmethod
    def validate_node_refs(cls, v: set[str]) -> set[str]:
        """Ensure node references are valid IDs."""
        for node_id in v:
            if not node_id or not isinstance(node_id, str):
                raise ValueError(f"Invalid node reference: {node_id}")
        return v

    @field_validator("resource_requirements")
    @classmethod
    def validate_unique_resources(
        cls, v: list[ResourceRequirement]
    ) -> list[ResourceRequirement]:
        """Ensure no duplicate resource types."""
        seen_types = set()
        for req in v:
            if req.resource_type in seen_types:
                raise ValueError(f"Duplicate resource requirement: {req.resource_type}")
            seen_types.add(req.resource_type)
        return v

    @model_validator(mode="after")
    def validate_dependencies(self) -> PlanNode:
        """Ensure node doesn't depend on itself."""
        if self.id in self.depends_on:
            raise ValueError("Node cannot depend on itself")
        if self.id in self.blocks:
            raise ValueError("Node cannot block itself")
        return self

    # ========================================================================
    # METHODS
    # ========================================================================

    def add_dependency(self, node_id: str) -> None:
        """Add a dependency to this node."""
        if node_id != self.id:
            self.depends_on.add(node_id)

    def remove_dependency(self, node_id: str) -> None:
        """Remove a dependency from this node."""
        self.depends_on.discard(node_id)

    def is_ready(self, completed_nodes: set[str]) -> bool:
        """Check if all dependencies are satisfied."""
        return self.depends_on.issubset(completed_nodes)

    def add_resource_requirement(
        self,
        resource_type: ResourceType,
        amount: float,
        priority: int = 5,
        flexible: bool = False,
        minimum: float | None = None,
    ) -> None:
        """Add or update a resource requirement."""
        # Remove existing if present
        self.resource_requirements = [
            r for r in self.resource_requirements if r.resource_type != resource_type
        ]
        # Add new requirement
        self.resource_requirements.append(
            ResourceRequirement(
                resource_type=resource_type,
                amount=amount,
                priority=priority,
                flexible=flexible,
                minimum=minimum,
            )
        )

    def get_resource_requirement(self, resource_type: ResourceType) -> float | None:
        """Get required amount for a resource type."""
        for req in self.resource_requirements:
            if req.resource_type == resource_type:
                return req.amount
        return None

    def estimate_total_tokens(self) -> int:
        """Estimate total tokens needed (including children)."""
        total = 0
        for req in self.resource_requirements:
            if req.resource_type == ResourceType.TOKENS:
                total += int(req.amount)
        return total

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "node_type": self.node_type,
            "status": self.status,
            "depends_on": list(self.depends_on),
            "resource_requirements": [
                {"type": r.resource_type, "amount": r.amount}
                for r in self.resource_requirements
            ],
            "metrics": {
                "duration": self.metrics.duration_seconds,
                "tokens": self.metrics.tokens_used,
                "success_rate": self.metrics.success_rate,
            },
        }

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"{self.__class__.__name__}("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"status={self.status}"
            f")"
        )
