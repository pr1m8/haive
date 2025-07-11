"""ReWOO Node Configuration.

This module provides node configurations for ReWOO agents following the
haive-core graph node pattern.
"""

import logging
from typing import Any, Dict, List, Optional, Type, Union

from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator

from haive.agents.planning.rewoo.models import (
    Evidence,
    EvidenceStatus,
    ReWOOPlan,
)
from haive.agents.planning.rewoo.models import ToolCall as ReWOOToolCall
from haive.agents.planning.rewoo.state import ReWOOState

logger = logging.getLogger(__name__)


# Input/Output Schemas for ReWOO nodes
class ReWOOPlanningInput(BaseModel):
    """Input schema for planning node."""

    objective: str = Field(..., description="Main objective to achieve")
    messages: list[BaseMessage] = Field(default_factory=list)
    tools: list[Any] = Field(default_factory=list, description="Available tools")


class ReWOOPlanningOutput(BaseModel):
    """Output schema for planning node."""

    plan: ReWOOPlan = Field(..., description="Generated ReWOO plan")
    evidence_map: dict[str, Evidence] = Field(default_factory=dict)
    messages: list[BaseMessage] = Field(default_factory=list)


class ReWOOEvidenceInput(BaseModel):
    """Input schema for evidence collection node."""

    plan: ReWOOPlan = Field(..., description="Current plan")
    evidence_map: dict[str, Evidence] = Field(default_factory=dict)
    messages: list[BaseMessage] = Field(default_factory=list)
    tools: list[Any] = Field(default_factory=list)
    tool_routes: dict[str, str] = Field(default_factory=dict)


class ReWOOEvidenceOutput(BaseModel):
    """Output schema for evidence collection node."""

    evidence_map: dict[str, Evidence] = Field(default_factory=dict)
    messages: list[BaseMessage] = Field(default_factory=list)
    current_evidence_id: str | None = Field(default=None)


class ReWOOReasoningInput(BaseModel):
    """Input schema for reasoning node."""

    objective: str = Field(..., description="Original objective")
    evidence_map: dict[str, Evidence] = Field(default_factory=dict)
    messages: list[BaseMessage] = Field(default_factory=list)


class ReWOOReasoningOutput(BaseModel):
    """Output schema for reasoning node."""

    messages: list[BaseMessage] = Field(default_factory=list)
    final_reasoning: str | None = Field(default=None)


# Node Configurations
class ReWOOPlanningNodeConfig(BaseNodeConfig[ReWOOPlanningInput, ReWOOPlanningOutput]):
    """Node config for ReWOO planning phase."""

    node_type: NodeType = Field(default=NodeType.AGENT, description="Node type")
    engine_name: str = Field(default="aug_llm", description="Engine for planning")

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get default input fields."""
        return [
            FieldDefinition(
                name="objective",
                field_type=str,
                description="Main objective to achieve",
            ),
            StandardFields.messages(use_enhanced=True),
            StandardFields.tools(),
        ]

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get default output fields."""
        return [
            FieldDefinition(
                name="plan", field_type=ReWOOPlan, description="Generated ReWOO plan"
            ),
            FieldDefinition(
                name="evidence_map",
                field_type=dict[str, Evidence],
                default_factory=dict,
                description="Evidence mapping",
            ),
            StandardFields.messages(use_enhanced=True),
        ]

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute planning node."""
        logger.info(f"ReWOO Planning Node: {self.name}")

        # Extract inputs
        objective = getattr(state, "objective", "")
        getattr(state, "tools", [])

        if not objective:
            return Command(update={"messages": ["No objective provided"]})

        # Create a simple plan for demo
        plan = ReWOOPlan(name="rewoo_plan", objective=objective)

        # Add evidence steps based on objective
        if any(word in objective.lower() for word in ["search", "find", "what", "who"]):
            # Add search evidence
            plan.add_rewoo_step(
                name="search_info",
                evidence_id="#E1",
                evidence_description=f"Search results for: {objective}",
                tool_name="search_tool",
                tool_args={"query": objective},
            )

            # Add analysis evidence that depends on search
            plan.add_rewoo_step(
                name="analyze_results",
                evidence_id="#E2",
                evidence_description="Analysis of search results",
                tool_name="analyze_tool",
                tool_args={"data": "#E1"},
                depends_on=["#E1"],
            )

        # Update state
        update = {
            "plan": plan,
            "evidence_map": plan.evidence_map.copy(),
            "messages": [f"Created plan with {len(plan.steps)} evidence steps"],
        }

        return Command(update=update, goto=self.command_goto)


class ReWOOEvidenceNodeConfig(BaseNodeConfig[ReWOOEvidenceInput, ReWOOEvidenceOutput]):
    """Node config for ReWOO evidence collection."""

    node_type: NodeType = Field(default=NodeType.TOOL, description="Node type")

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get default input fields."""
        return [
            FieldDefinition(
                name="plan", field_type=ReWOOPlan, description="Current plan"
            ),
            FieldDefinition(
                name="evidence_map",
                field_type=dict[str, Evidence],
                default_factory=dict,
                description="Evidence mapping",
            ),
            StandardFields.messages(use_enhanced=True),
            StandardFields.tools(),
            StandardFields.tool_routes(),
        ]

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get default output fields."""
        return [
            FieldDefinition(
                name="evidence_map",
                field_type=dict[str, Evidence],
                default_factory=dict,
                description="Updated evidence mapping",
            ),
            StandardFields.messages(use_enhanced=True),
            FieldDefinition(
                name="current_evidence_id",
                field_type=Optional[str],
                default=None,
                description="Currently collecting evidence ID",
            ),
        ]

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute evidence collection."""
        logger.info(f"ReWOO Evidence Node: {self.name}")

        # Get state data
        plan = getattr(state, "plan", None)
        evidence_map = getattr(state, "evidence_map", {})
        messages = getattr(state, "messages", [])
        getattr(state, "tools", [])

        if not plan:
            return Command(update={"messages": ["No plan available"]})

        # Find ready evidence
        ready_evidence = []
        for evidence in evidence_map.values():
            if evidence.status != EvidenceStatus.PLANNED:
                continue

            # Check dependencies
            deps_met = all(
                evidence_map.get(
                    dep_id, Evidence(id=dep_id, description="", source="")
                ).status
                == EvidenceStatus.COLLECTED
                for dep_id in evidence.depends_on
            )

            if deps_met:
                ready_evidence.append(evidence)

        if not ready_evidence:
            return Command(update={"messages": ["No evidence ready to collect"]})

        # Take first ready evidence
        evidence = ready_evidence[0]

        # Find corresponding step
        step = None
        for s in plan.steps:
            if hasattr(s, "evidence") and s.evidence and s.evidence.id == evidence.id:
                step = s
                break

        if not step or not step.tool_call:
            return Command(
                update={"messages": [f"No tool call for evidence {evidence.id}"]}
            )

        # Resolve arguments
        resolved_args = step.tool_call.resolve_arguments(evidence_map)

        # Create tool call message
        tool_call_data = {
            "name": step.tool_call.tool_name,
            "args": resolved_args,
            "id": f"call_{evidence.id}_{step.tool_call.tool_name}",
        }

        ai_message = AIMessage(
            content=f"Collecting evidence {evidence.id}: {evidence.description}",
            tool_calls=[tool_call_data],
        )

        # Mark as collecting
        evidence.status = EvidenceStatus.COLLECTING
        evidence_map[evidence.id] = evidence

        # Update messages
        updated_messages = [*list(messages), ai_message]

        update = {
            "evidence_map": evidence_map,
            "messages": updated_messages,
            "current_evidence_id": evidence.id,
        }

        return Command(update=update, goto=self.command_goto)


class ReWOOReasoningNodeConfig(
    BaseNodeConfig[ReWOOReasoningInput, ReWOOReasoningOutput]
):
    """Node config for ReWOO final reasoning."""

    node_type: NodeType = Field(default=NodeType.AGENT, description="Node type")
    engine_name: str = Field(default="aug_llm", description="Engine for reasoning")

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get default input fields."""
        return [
            FieldDefinition(
                name="objective", field_type=str, description="Original objective"
            ),
            FieldDefinition(
                name="evidence_map",
                field_type=dict[str, Evidence],
                default_factory=dict,
                description="Collected evidence",
            ),
            StandardFields.messages(use_enhanced=True),
        ]

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get default output fields."""
        return [
            StandardFields.messages(use_enhanced=True),
            FieldDefinition(
                name="final_reasoning",
                field_type=Optional[str],
                default=None,
                description="Final reasoning result",
            ),
        ]

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute final reasoning."""
        logger.info(f"ReWOO Reasoning Node: {self.name}")

        # Get inputs
        objective = getattr(state, "objective", "")
        evidence_map = getattr(state, "evidence_map", {})

        # Build evidence context
        evidence_lines = []
        for eid, evidence in evidence_map.items():
            if evidence.status == EvidenceStatus.COLLECTED and evidence.content:
                evidence_lines.append(f"{eid}: {evidence.description}")
                evidence_lines.append(f"   Content: {evidence.content}")

        evidence_context = "\n".join(evidence_lines)

        # Create final reasoning
        reasoning = f"""
Based on collected evidence:

{evidence_context}

Final answer for "{objective}":
The evidence shows that [reasoning based on collected data].
"""

        update = {"messages": [reasoning], "final_reasoning": reasoning}

        return Command(update=update, goto=self.command_goto)


# Factory functions
def create_rewoo_planning_node(
    name: str = "rewoo_planning", engine_name: str = "aug_llm", **kwargs
) -> ReWOOPlanningNodeConfig:
    """Create ReWOO planning node config."""
    return ReWOOPlanningNodeConfig(name=name, engine_name=engine_name, **kwargs)


def create_rewoo_evidence_node(
    name: str = "rewoo_evidence", **kwargs
) -> ReWOOEvidenceNodeConfig:
    """Create ReWOO evidence collection node config."""
    return ReWOOEvidenceNodeConfig(name=name, **kwargs)


def create_rewoo_reasoning_node(
    name: str = "rewoo_reasoning", engine_name: str = "aug_llm", **kwargs
) -> ReWOOReasoningNodeConfig:
    """Create ReWOO reasoning node config."""
    return ReWOOReasoningNodeConfig(name=name, engine_name=engine_name, **kwargs)
