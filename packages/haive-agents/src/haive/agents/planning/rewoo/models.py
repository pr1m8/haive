"""ReWOO (Reasoning Without Observation) Models.

This module implements smart evidence-based planning with tool integration.
ReWOO separates planning from execution, creating evidence references that
get resolved during execution.
"""

from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Dict, List, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from haive.agents.planning.models.base import (
    BasePlan,
    BaseStep,
    Dependency,
    DependencyType,
    StepMetadata,
    StepStatus,
    StepType,
)

# ============================================================================
# EVIDENCE MODELS
# ============================================================================


class EvidenceType(str, Enum):
    """Type of evidence that can be collected."""

    TOOL_OUTPUT = "tool_output"  # Output from tool execution
    LLM_REASONING = "llm_reasoning"  # LLM-generated reasoning
    RETRIEVAL = "retrieval"  # Retrieved information
    COMPUTATION = "computation"  # Computed/derived value
    OBSERVATION = "observation"  # Direct observation
    REFERENCE = "reference"  # Reference to other evidence


class EvidenceStatus(str, Enum):
    """Status of evidence collection."""

    PLANNED = "planned"  # Evidence planned but not collected
    COLLECTING = "collecting"  # Currently being collected
    COLLECTED = "collected"  # Successfully collected
    FAILED = "failed"  # Collection failed
    INVALID = "invalid"  # Evidence invalidated
    REFERENCED = "referenced"  # Referenced by other evidence


class Evidence(BaseModel):
    """Represents a piece of evidence in the ReWOO system."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    # Identity
    id: str = Field(
        ..., description="Evidence identifier (e.g., #E1, #E2)", pattern=r"^#E\d+$"
    )

    description: str = Field(..., description="What this evidence represents")

    evidence_type: EvidenceType = Field(
        default=EvidenceType.TOOL_OUTPUT, description="Type of evidence"
    )

    # Collection details
    source: str = Field(..., description="Source of evidence (tool name, LLM, etc.)")

    collection_method: str = Field(..., description="How to collect this evidence")

    # Dependencies on other evidence
    depends_on: list[str] = Field(
        default_factory=list, description="Other evidence IDs this depends on"
    )

    # Status tracking
    status: EvidenceStatus = Field(
        default=EvidenceStatus.PLANNED, description="Current status"
    )

    # Actual evidence data
    content: Any | None = Field(default=None, description="The actual evidence content")

    error: str | None = Field(default=None, description="Error if collection failed")

    # Metadata
    collected_at: datetime | None = None
    confidence: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Confidence in this evidence"
    )

    @field_validator("depends_on")
    @classmethod
    def validate_evidence_refs(cls, v: list[str]) -> list[str]:
        """Ensure evidence references are valid."""
        for ref in v:
            if not ref.startswith("#E"):
                raise ValueError(f"Invalid evidence reference: {ref}")
        return v

    @computed_field
    @property
    def is_ready(self) -> bool:
        """Check if evidence is ready to be collected."""
        return self.status == EvidenceStatus.PLANNED and not self.depends_on

    def resolve_references(self, evidence_map: dict[str, "Evidence"]) -> str:
        """Resolve evidence references in collection method."""
        resolved = self.collection_method

        # Replace evidence references with actual content
        for dep_id in self.depends_on:
            if dep_id in evidence_map:
                dep_evidence = evidence_map[dep_id]
                if dep_evidence.content is not None:
                    # Replace #E1 with actual content
                    resolved = resolved.replace(dep_id, str(dep_evidence.content))

        return resolved


# ============================================================================
# TOOL CALL MODELS
# ============================================================================


class ToolCallType(str, Enum):
    """Type of tool call in ReWOO."""

    STANDARD = "standard"  # Regular tool with args
    LLM = "llm"  # LLM reasoning (no tool)
    FUNCTION = "function"  # Python function
    RETRIEVAL = "retrieval"  # Retrieval tool
    COMPUTATION = "computation"  # Computation/calculation


class ToolCall(BaseModel):
    """Smart tool call that integrates with evidence system."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    # Tool identification
    tool_name: str = Field(..., description="Name of tool or 'LLM' for reasoning")

    tool_type: ToolCallType = Field(
        default=ToolCallType.STANDARD, description="Type of tool call"
    )

    # Arguments can reference evidence
    arguments: dict[str, Any] = Field(
        default_factory=dict, description="Tool arguments (can include #E references)"
    )

    # Expected output
    expected_output_type: str | None = Field(
        default=None, description="Expected type of output (for validation)"
    )

    expected_output_schema: dict[str, Any] | None = Field(
        default=None, description="Expected schema for structured output"
    )

    # Execution constraints
    timeout_seconds: int | None = Field(
        default=None, description="Timeout for tool execution", gt=0
    )

    retry_on_failure: bool = Field(
        default=True, description="Whether to retry on failure"
    )

    max_retries: int = Field(default=3, description="Maximum retry attempts", ge=0)

    @computed_field
    @property
    def is_llm_call(self) -> bool:
        """Check if this is an LLM reasoning call."""
        return self.tool_name.upper() == "LLM" or self.tool_type == ToolCallType.LLM

    def resolve_arguments(self, evidence_map: dict[str, Evidence]) -> dict[str, Any]:
        """Resolve evidence references in arguments."""
        resolved_args = {}

        for key, value in self.arguments.items():
            if isinstance(value, str) and value.startswith("#E"):
                # This is an evidence reference
                if value in evidence_map:
                    evidence = evidence_map[value]
                    if evidence.content is not None:
                        resolved_args[key] = evidence.content
                    else:
                        # Keep reference if not resolved
                        resolved_args[key] = value
                else:
                    resolved_args[key] = value
            else:
                resolved_args[key] = value

        return resolved_args

    def validate_output(self, output: Any) -> bool:
        """Validate tool output against expected schema."""
        if self.expected_output_type:
            # Simple type checking
            expected_type = {
                "string": str,
                "number": (int, float),
                "boolean": bool,
                "array": list,
                "object": dict,
            }.get(self.expected_output_type)

            if expected_type and not isinstance(output, expected_type):
                return False

        if self.expected_output_schema and isinstance(output, dict):
            # Basic schema validation
            for key, _expected in self.expected_output_schema.items():
                if key not in output:
                    return False

        return True


# ============================================================================
# REWOO STEP MODEL
# ============================================================================


class ReWOOStep(BaseStep):
    """ReWOO-specific step with evidence generation."""

    step_type: StepType = Field(
        default=StepType.EVIDENCE, description="ReWOO steps are evidence-based"
    )

    # Evidence this step produces
    evidence: Evidence | None = Field(
        default=None, description="Evidence this step produces"
    )

    # Tool call for this step
    tool_call: ToolCall | None = Field(default=None, description="Tool call to execute")

    # Alternative: Multiple tool calls with fallback
    tool_calls: list[ToolCall] = Field(
        default_factory=list, description="Multiple tool calls (fallback options)"
    )

    # How to process tool output into evidence
    output_processor: str | None = Field(
        default=None, description="Python expression to process tool output"
    )

    @model_validator(mode="after")
    def validate_evidence_tool_consistency(self) -> "ReWOOStep":
        """Ensure evidence and tool calls are consistent."""
        if self.evidence and not (self.tool_call or self.tool_calls):
            raise ValueError("Evidence step must have tool call(s)")

        if self.tool_call and self.tool_calls:
            raise ValueError("Use either tool_call or tool_calls, not both")

        return self

    @computed_field
    @property
    def evidence_id(self) -> str | None:
        """Get evidence ID if this step produces evidence."""
        return self.evidence.id if self.evidence else None

    @computed_field
    @property
    def evidence_dependencies(self) -> list[str]:
        """Get all evidence dependencies for this step."""
        deps = []

        # From evidence
        if self.evidence:
            deps.extend(self.evidence.depends_on)

        # From tool arguments
        if self.tool_call:
            for value in self.tool_call.arguments.values():
                if isinstance(value, str) and value.startswith("#E"):
                    if value not in deps:
                        deps.append(value)

        for tc in self.tool_calls:
            for value in tc.arguments.values():
                if isinstance(value, str) and value.startswith("#E"):
                    if value not in deps:
                        deps.append(value)

        return deps

    def get_active_tool_call(self) -> ToolCall | None:
        """Get the tool call to execute."""
        if self.tool_call:
            return self.tool_call
        if self.tool_calls:
            # Return first non-failed tool call
            return self.tool_calls[0]
        return None

    def process_output(self, raw_output: Any) -> Any:
        """Process tool output using configured processor."""
        if not self.output_processor:
            return raw_output

        try:
            # Safe evaluation context
            context = {
                "output": raw_output,
                "str": str,
                "int": int,
                "float": float,
                "len": len,
                "sum": sum,
                "min": min,
                "max": max,
            }

            # Evaluate processor expression
            return eval(self.output_processor, {"__builtins__": {}}, context)
        except Exception:
            # Return raw output if processing fails
            return raw_output


# ============================================================================
# REWOO PLAN MODEL
# ============================================================================


class ReWOOPlan(BasePlan):
    """ReWOO plan with evidence management."""

    # Override steps to be ReWOO-specific
    steps: list[ReWOOStep] = Field(
        default_factory=list, description="ReWOO steps in the plan"
    )

    # Evidence registry
    evidence_map: dict[str, Evidence] = Field(
        default_factory=dict, description="Map of evidence ID to evidence"
    )

    # Tool registry (populated during initialization)
    available_tools: dict[str, Any] = Field(
        default_factory=dict, description="Available tools for execution"
    )

    # Execution mode
    parallel_evidence_collection: bool = Field(
        default=True, description="Whether to collect independent evidence in parallel"
    )

    max_parallel_collections: int = Field(
        default=5, description="Maximum parallel evidence collections", ge=1
    )

    @model_validator(mode="after")
    def build_evidence_map(self) -> "ReWOOPlan":
        """Build evidence map from steps."""
        for step in self.steps:
            if step.evidence:
                self.evidence_map[step.evidence.id] = step.evidence
        return self

    @computed_field
    @property
    def evidence_graph(self) -> dict[str, list[str]]:
        """Get evidence dependency graph."""
        graph = {}
        for eid, evidence in self.evidence_map.items():
            graph[eid] = evidence.depends_on
        return graph

    @computed_field
    @property
    def next_evidence_to_collect(self) -> list[Evidence]:
        """Get evidence that's ready to collect."""
        ready = []

        for evidence in self.evidence_map.values():
            if evidence.status != EvidenceStatus.PLANNED:
                continue

            # Check if dependencies are satisfied
            deps_satisfied = all(
                self.evidence_map.get(
                    dep_id, Evidence(id=dep_id, description="", source="")
                ).status
                == EvidenceStatus.COLLECTED
                for dep_id in evidence.depends_on
            )

            if deps_satisfied:
                ready.append(evidence)

        # Limit to max parallel
        return ready[: self.max_parallel_collections]

    @computed_field
    @property
    def evidence_completion_percentage(self) -> float:
        """Calculate evidence collection progress."""
        if not self.evidence_map:
            return 100.0

        collected = sum(
            1
            for e in self.evidence_map.values()
            if e.status == EvidenceStatus.COLLECTED
        )

        return (collected / len(self.evidence_map)) * 100

    def get_evidence_for_step(self, step_id: str) -> Evidence | None:
        """Get evidence produced by a specific step."""
        step = self.get_step(step_id)
        if isinstance(step, ReWOOStep) and step.evidence:
            return step.evidence
        return None

    def update_evidence_status(
        self,
        evidence_id: str,
        status: EvidenceStatus,
        content: Any | None = None,
        error: str | None = None,
    ) -> bool:
        """Update evidence status and content."""
        if evidence_id not in self.evidence_map:
            return False

        evidence = self.evidence_map[evidence_id]
        evidence.status = status

        if content is not None:
            evidence.content = content
            evidence.collected_at = datetime.now()

        if error is not None:
            evidence.error = error

        # Update corresponding step
        for step in self.steps:
            if (
                isinstance(step, ReWOOStep)
                and step.evidence
                and step.evidence.id == evidence_id
            ):
                if status == EvidenceStatus.COLLECTED:
                    step.mark_completed({"evidence": content})
                elif status == EvidenceStatus.FAILED:
                    step.mark_failed(error or "Evidence collection failed")
                break

        self.updated_at = datetime.now()
        return True

    def resolve_evidence_references(self, text: str) -> str:
        """Resolve all evidence references in text."""
        resolved = text

        for eid, evidence in self.evidence_map.items():
            if evidence.content is not None:
                resolved = resolved.replace(eid, str(evidence.content))

        return resolved

    def add_rewoo_step(
        self,
        name: str,
        evidence_id: str,
        evidence_description: str,
        tool_name: str,
        tool_args: dict[str, Any],
        depends_on: list[str] | None = None,
        output_processor: str | None = None,
    ) -> ReWOOStep:
        """Convenience method to add a ReWOO step."""
        # Create evidence
        evidence = Evidence(
            id=evidence_id,
            description=evidence_description,
            source=tool_name,
            collection_method=f"{tool_name}({tool_args})",
            depends_on=depends_on or [],
        )

        # Create tool call
        tool_call = ToolCall(tool_name=tool_name, arguments=tool_args)

        # Create step
        step = ReWOOStep(
            name=name,
            description=f"Collect {evidence_description}",
            evidence=evidence,
            tool_call=tool_call,
            output_processor=output_processor,
        )

        # Add dependencies based on evidence
        for dep_id in depends_on or []:
            # Find step that produces this evidence
            for existing_step in self.steps:
                if (
                    isinstance(existing_step, ReWOOStep)
                    and existing_step.evidence_id == dep_id
                ):
                    step.add_dependency(
                        existing_step.id, DependencyType.DATA, required_output=dep_id
                    )

        # Add to plan
        self.add_step(step)

        # Update evidence map
        self.evidence_map[evidence_id] = evidence

        return step

    def to_evidence_prompt(self) -> str:
        """Format plan focusing on evidence collection."""
        lines = [
            f"Objective: {self.objective}",
            f"Evidence Progress: {self.evidence_completion_percentage:.1f}%",
            "",
            "Evidence Collection Plan:",
        ]

        for eid in sorted(self.evidence_map.keys()):
            evidence = self.evidence_map[eid]
            status_marker = {
                EvidenceStatus.COLLECTED: "✓",
                EvidenceStatus.FAILED: "✗",
                EvidenceStatus.COLLECTING: "→",
                EvidenceStatus.PLANNED: "○",
            }.get(evidence.status, "?")

            lines.append(f"{status_marker} {eid}: {evidence.description}")

            if evidence.depends_on:
                lines.append(f"   Depends on: {', '.join(evidence.depends_on)}")

            if evidence.content is not None:
                content_str = str(evidence.content)[:100]
                if len(str(evidence.content)) > 100:
                    content_str += "..."
                lines.append(f"   Content: {content_str}")

            if evidence.error:
                lines.append(f"   Error: {evidence.error}")

        return "\n".join(lines)


# ============================================================================
# REASONING OUTPUT MODELS
# ============================================================================


class ReWOOReasoning(BaseModel):
    """Final reasoning output using collected evidence."""

    model_config = ConfigDict(extra="forbid")

    objective_restatement: str = Field(..., description="Restatement of the objective")

    evidence_summary: dict[str, str] = Field(
        ..., description="Summary of key evidence collected"
    )

    reasoning_steps: list[str] = Field(
        ..., description="Step-by-step reasoning using evidence"
    )

    conclusion: str = Field(..., description="Final conclusion based on evidence")

    confidence: float = Field(
        default=0.8, ge=0.0, le=1.0, description="Confidence in conclusion"
    )

    limitations: list[str] = Field(
        default_factory=list, description="Limitations or caveats"
    )

    next_steps: list[str] | None = Field(
        default=None, description="Suggested next steps if needed"
    )
