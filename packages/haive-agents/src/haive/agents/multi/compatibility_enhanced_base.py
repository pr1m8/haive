"""Compatibility-Enhanced Multi-Agent Base.

This module extends the multi-agent base with built-in compatibility checking,
ensuring agents are compatible before building workflows and providing
automatic adaptation when possible.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from haive.core.schema.compatibility import (
    CompatibilityChecker,
    FieldMapper,
    TypeAnalyzer,
    check_compatibility,
)

from haive.agents.base.agent import Agent

from .base import ExecutionMode, MultiAgent

logger = logging.getLogger(__name__)


class CompatibilityMode(str, Enum):
    """Modes for handling compatibility issues."""

    STRICT = "strict"  # Fail if any incompatibilities
    ADAPTIVE = "adaptive"  # Try to adapt incompatible agents
    PERMISSIVE = "permissive"  # Allow incompatibilities with warnings
    AUTO_FIX = "auto_fix"  # Automatically fix compatibility issues


@dataclass
class CompatibilityResult:
    """Result of compatibility checking."""

    is_compatible: bool
    compatibility_score: float
    issues: list[str]
    warnings: list[str]
    suggested_adapters: list[dict[str, Any]]
    auto_fixes_applied: list[str]


class CompatibilityEnhancedMultiAgent(MultiAgent):
    """Multi-agent system with built-in compatibility checking and automatic adaptation.

    This class extends the base MultiAgent with comprehensive compatibility checking
    that runs automatically when agents are added, when graphs are built, and during
    runtime to ensure smooth agent interaction.

    Key Features:
    - Automatic compatibility checking when agents are added
    - Built-in adapter creation for incompatible agents
    - Runtime compatibility monitoring
    - Detailed compatibility reporting
    - Multiple compatibility modes (strict, adaptive, permissive, auto-fix)

    Example:
        >>> system = CompatibilityEnhancedMultiAgent(
        ...     agents=[retrieval_agent, grading_agent, answer_agent],
        ...     compatibility_mode=CompatibilityMode.ADAPTIVE
        ... )
        >>> # Compatibility is automatically checked and issues are resolved
    """

    # Compatibility configuration
    compatibility_mode: CompatibilityMode = CompatibilityMode.ADAPTIVE
    auto_check_compatibility: bool = True
    compatibility_threshold: float = 0.7
    enable_auto_adapters: bool = True
    compatibility_report_level: str = "summary"  # "none", "summary", "detailed"

    def __init__(self, **kwargs):
        # Initialize compatibility components
        self._compatibility_checker = CompatibilityChecker()
        self._type_analyzer = TypeAnalyzer()
        self._compatibility_cache = {}
        self._applied_adapters = []
        self._compatibility_results = []

        super().__init__(**kwargs)

    def add_agent(self, agent: Agent, check_compatibility: bool | None = None) -> None:
        """Add an agent to the multi-agent system with automatic compatibility checking.

        Args:
            agent: The agent to add
            check_compatibility: Whether to check compatibility (defaults to auto_check_compatibility)
        """
        should_check = (
            check_compatibility
            if check_compatibility is not None
            else self.auto_check_compatibility
        )

        if should_check and self.agents:
            # Check compatibility with existing agents
            compatibility_result = self._check_agent_compatibility(agent)

            if not compatibility_result.is_compatible:
                if self.compatibility_mode == CompatibilityMode.STRICT:
                    raise ValueError(
                        f"Agent {agent.name} is incompatible with existing agents: "
                        f"{'; '.join(compatibility_result.issues)}"
                    )
                if self.compatibility_mode == CompatibilityMode.ADAPTIVE:
                    self._adapt_agent_for_compatibility(agent, compatibility_result)
                elif self.compatibility_mode == CompatibilityMode.AUTO_FIX:
                    self._auto_fix_compatibility(agent, compatibility_result)
                elif self.compatibility_mode == CompatibilityMode.PERMISSIVE:
                    logger.warning(
                        f"Adding incompatible agent {agent.name}: "
                        f"{'; '.join(compatibility_result.issues)}"
                    )

            self._compatibility_results.append(compatibility_result)

        # Add agent to the list
        agents_list = list(self.agents) if self.agents else []
        agents_list.append(agent)
        self.agents = agents_list

        logger.info(f"Added agent {agent.name} to multi-agent system")

    def _check_agent_compatibility(self, new_agent: Agent) -> CompatibilityResult:
        """Check compatibility of a new agent with existing agents."""
        issues = []
        warnings = []
        suggested_adapters = []
        auto_fixes_applied = []
        min_score = 1.0

        # Check compatibility with each existing agent (for sequential workflows)
        for existing_agent in self.agents:
            if self.execution_mode == ExecutionMode.SEQUENCE:
                # Check if existing agent output is compatible with new agent input
                result = self._check_agent_pair_compatibility(existing_agent, new_agent)

                if not result["compatible"]:
                    issues.extend(result["issues"])
                    suggested_adapters.extend(result["suggested_adapters"])

                min_score = min(min_score, result["score"])
                warnings.extend(result["warnings"])

        # For the new agent, check if it can work with the shared state schema
        if self.state_schema:
            state_compatibility = self._check_state_schema_compatibility(new_agent)
            if not state_compatibility["compatible"]:
                issues.extend(state_compatibility["issues"])
                suggested_adapters.extend(state_compatibility["suggested_adapters"])
                min_score = min(min_score, state_compatibility["score"])

        return CompatibilityResult(
            is_compatible=len(issues) == 0,
            compatibility_score=min_score,
            issues=issues,
            warnings=warnings,
            suggested_adapters=suggested_adapters,
            auto_fixes_applied=auto_fixes_applied,
        )

    def _check_agent_pair_compatibility(
        self, source_agent: Agent, target_agent: Agent
    ) -> dict[str, Any]:
        """Check compatibility between two specific agents."""
        try:
            # Get schemas safely
            source_schema = self._get_agent_output_schema(source_agent)
            target_schema = self._get_agent_input_schema(target_agent)

            if not source_schema or not target_schema:
                return {
                    "compatible": False,
                    "score": 0.0,
                    "issues": ["Could not extract schemas for compatibility checking"],
                    "warnings": [],
                    "suggested_adapters": [],
                }

            # Use compatibility module
            compat_result = check_compatibility(source_schema, target_schema)

            return {
                "compatible": getattr(compat_result, "is_compatible", False),
                "score": getattr(compat_result, "compatibility_score", 0.0),
                "issues": getattr(compat_result, "issues", []),
                "warnings": getattr(compat_result, "warnings", []),
                "suggested_adapters": self._extract_adapter_suggestions(compat_result),
            }

        except Exception as e:
            logger.exception(
                f"Error checking compatibility between {source_agent.name} and {target_agent.name}: {e}"
            )
            return {
                "compatible": False,
                "score": 0.0,
                "issues": [f"Compatibility check failed: {e!s}"],
                "warnings": [],
                "suggested_adapters": [],
            }

    def _check_state_schema_compatibility(self, agent: Agent) -> dict[str, Any]:
        """Check if agent is compatible with the shared state schema."""
        try:
            agent_schema = self._get_agent_state_schema(agent)

            if not agent_schema:
                return {
                    "compatible": True,  # No schema to check
                    "score": 1.0,
                    "issues": [],
                    "suggested_adapters": [],
                }

            # Check compatibility with multi-agent state schema
            compat_result = check_compatibility(self.state_schema, agent_schema)

            return {
                "compatible": getattr(compat_result, "is_compatible", False),
                "score": getattr(compat_result, "compatibility_score", 0.0),
                "issues": getattr(compat_result, "issues", []),
                "suggested_adapters": self._extract_adapter_suggestions(compat_result),
            }

        except Exception as e:
            logger.exception(
                f"Error checking state schema compatibility for {agent.name}: {e}"
            )
            return {
                "compatible": False,
                "score": 0.0,
                "issues": [f"State schema compatibility check failed: {e!s}"],
                "suggested_adapters": [],
            }

    def _get_agent_output_schema(self, agent: Agent) -> type | None:
        """Safely extract agent output schema."""
        try:
            if hasattr(agent, "output_schema") and agent.output_schema:
                return agent.output_schema
            if hasattr(agent, "state_schema") and agent.state_schema:
                return agent.state_schema
            if hasattr(agent, "engine") and agent.engine:
                if hasattr(agent.engine, "output_schema"):
                    return agent.engine.output_schema
                if hasattr(agent.engine, "derive_output_schema"):
                    return agent.engine.derive_output_schema()
            return None
        except Exception:
            return None

    def _get_agent_input_schema(self, agent: Agent) -> type | None:
        """Safely extract agent input schema."""
        try:
            if hasattr(agent, "input_schema") and agent.input_schema:
                return agent.input_schema
            if hasattr(agent, "state_schema") and agent.state_schema:
                return agent.state_schema
            if hasattr(agent, "engine") and agent.engine:
                if hasattr(agent.engine, "input_schema"):
                    return agent.engine.input_schema
                if hasattr(agent.engine, "derive_input_schema"):
                    return agent.engine.derive_input_schema()
            return None
        except Exception:
            return None

    def _get_agent_state_schema(self, agent: Agent) -> type | None:
        """Safely extract agent state schema."""
        try:
            if hasattr(agent, "state_schema") and agent.state_schema:
                return agent.state_schema
            return None
        except Exception:
            return None

    def _extract_adapter_suggestions(self, compat_result) -> list[dict[str, Any]]:
        """Extract adapter suggestions from compatibility result."""
        adapters = []

        missing_fields = getattr(compat_result, "missing_required_fields", [])
        if missing_fields:
            adapters.append(
                {
                    "type": "FieldMappingAdapter",
                    "purpose": "Map missing required fields",
                    "missing_fields": missing_fields,
                }
            )

        suggested_mappings = getattr(compat_result, "suggested_mappings", {})
        if suggested_mappings:
            adapters.append(
                {
                    "type": "FieldMappingAdapter",
                    "purpose": "Apply suggested field mappings",
                    "mappings": suggested_mappings,
                }
            )

        return adapters

    def _adapt_agent_for_compatibility(
        self, agent: Agent, compatibility_result: CompatibilityResult
    ) -> None:
        """Adapt an agent to improve compatibility."""
        logger.info(f"Adapting agent {agent.name} for compatibility...")

        for adapter_spec in compatibility_result.suggested_adapters:
            try:
                if adapter_spec["type"] == "FieldMappingAdapter":
                    self._apply_field_mapping_adapter(agent, adapter_spec)
                # Could add more adapter types here

            except Exception as e:
                logger.exception(
                    f"Failed to apply adapter {adapter_spec['type']} to {agent.name}: {e}"
                )

    def _apply_field_mapping_adapter(
        self, agent: Agent, adapter_spec: dict[str, Any]
    ) -> None:
        """Apply a field mapping adapter to an agent."""
        # This is a simplified implementation
        # In practice, you might create wrapper classes or modify agent behavior

        mapper = FieldMapper()

        if "mappings" in adapter_spec:
            for source_field, target_field in adapter_spec["mappings"].items():
                mapper.add_mapping(source_field, target_field)

        # Store the adapter for later use
        self._applied_adapters.append(
            {
                "agent": agent.name,
                "adapter_type": "FieldMappingAdapter",
                "mapper": mapper,
                "spec": adapter_spec,
            }
        )

        logger.info(f"Applied field mapping adapter to {agent.name}")

    def _auto_fix_compatibility(
        self, agent: Agent, compatibility_result: CompatibilityResult
    ) -> None:
        """Automatically fix compatibility issues where possible."""
        logger.info(f"Auto-fixing compatibility issues for agent {agent.name}...")

        # Start with adaptive approach
        self._adapt_agent_for_compatibility(agent, compatibility_result)

        # Add additional auto-fixes here
        # For example, automatic schema updates, field transformations, etc.

    def build_graph(self):
        """Build graph with pre-build compatibility validation."""
        if self.auto_check_compatibility:
            self._validate_workflow_compatibility()

        return super().build_graph()

    def _validate_workflow_compatibility(self) -> None:
        """Validate compatibility of the entire workflow before building."""
        logger.info("Validating workflow compatibility...")

        incompatible_pairs = []

        if self.execution_mode == ExecutionMode.SEQUENCE:
            # Check sequential compatibility
            for i in range(len(self.agents) - 1):
                source_agent = self.agents[i]
                target_agent = self.agents[i + 1]

                result = self._check_agent_pair_compatibility(
                    source_agent, target_agent
                )

                if (
                    not result["compatible"]
                    and result["score"] < self.compatibility_threshold
                ):
                    incompatible_pairs.append(
                        (source_agent.name, target_agent.name, result)
                    )

        if incompatible_pairs and self.compatibility_mode == CompatibilityMode.STRICT:
            issues = [
                f"{pair[0]} -> {pair[1]}: {'; '.join(pair[2]['issues'])}"
                for pair in incompatible_pairs
            ]
            raise ValueError(f"Workflow has compatibility issues: {'; '.join(issues)}")

        if incompatible_pairs:
            logger.warning(
                f"Workflow has {len(incompatible_pairs)} compatibility issues"
            )
            for source, target, result in incompatible_pairs:
                logger.warning(f"  {source} -> {target}: score {result['score']:.2f}")

    def get_compatibility_report(self, detailed: bool | None = None) -> dict[str, Any]:
        """Generate a comprehensive compatibility report."""
        if detailed is None:
            detailed = self.compatibility_report_level == "detailed"

        report = {
            "workflow_name": self.name,
            "execution_mode": self.execution_mode.value,
            "compatibility_mode": self.compatibility_mode.value,
            "total_agents": len(self.agents),
            "total_compatibility_checks": len(self._compatibility_results),
            "applied_adapters": len(self._applied_adapters),
            "overall_compatible": all(
                result.is_compatible for result in self._compatibility_results
            ),
        }

        if detailed:
            report.update(
                {
                    "agent_names": [agent.name for agent in self.agents],
                    "compatibility_results": [
                        {
                            "is_compatible": result.is_compatible,
                            "score": result.compatibility_score,
                            "issues_count": len(result.issues),
                            "warnings_count": len(result.warnings),
                            "adapters_suggested": len(result.suggested_adapters),
                        }
                        for result in self._compatibility_results
                    ],
                    "applied_adapters": self._applied_adapters,
                    "recommendations": self._generate_compatibility_recommendations(),
                }
            )

        return report

    def _generate_compatibility_recommendations(self) -> list[str]:
        """Generate recommendations for improving compatibility."""
        recommendations = []

        if not self._compatibility_results:
            recommendations.append("No compatibility checks have been performed yet")
            return recommendations

        incompatible_count = sum(
            1 for result in self._compatibility_results if not result.is_compatible
        )

        if incompatible_count == 0:
            recommendations.append("All agents are compatible - no action needed")
        else:
            recommendations.append(
                f"{incompatible_count} agents have compatibility issues"
            )

            if self.compatibility_mode == CompatibilityMode.PERMISSIVE:
                recommendations.append(
                    "Consider switching to ADAPTIVE mode for automatic fixes"
                )

            if not self.enable_auto_adapters:
                recommendations.append(
                    "Enable auto_adapters for automatic compatibility fixes"
                )

        return recommendations

    def visualize_compatibility(self) -> None:
        """Visualize the compatibility status of the multi-agent system."""
        from rich.console import Console
        from rich.table import Table
        from rich.tree import Tree

        console = Console()

        # Create compatibility tree
        tree = Tree(f"[bold blue]{self.name}[/bold blue] - Compatibility Status")

        # Add overall status
        overall_compatible = all(
            result.is_compatible for result in self._compatibility_results
        )
        status_color = "green" if overall_compatible else "red"
        status_text = "✅ Compatible" if overall_compatible else "❌ Has Issues"

        tree.add(f"[{status_color}]{status_text}[/{status_color}]")

        # Add agent details
        agents_branch = tree.add("[cyan]Agents[/cyan]")
        for i, agent in enumerate(self.agents):
            agent_status = (
                "✅"
                if i < len(self._compatibility_results)
                and self._compatibility_results[i].is_compatible
                else "⚠️"
            )
            agents_branch.add(f"{agent_status} {agent.name}")

        # Add adapter information
        if self._applied_adapters:
            adapters_branch = tree.add("[yellow]Applied Adapters[/yellow]")
            for adapter in self._applied_adapters:
                adapters_branch.add(
                    f"🔧 {adapter['adapter_type']} for {adapter['agent']}"
                )

        console.print(tree)

        # Add detailed table if there are issues
        if not overall_compatible:
            table = Table(title="Compatibility Issues")
            table.add_column("Agent", style="cyan")
            table.add_column("Score", style="magenta")
            table.add_column("Issues", style="red")

            for i, result in enumerate(self._compatibility_results):
                if not result.is_compatible:
                    agent_name = (
                        self.agents[i].name if i < len(self.agents) else f"Agent {i}"
                    )
                    table.add_row(
                        agent_name,
                        f"{result.compatibility_score:.2f}",
                        "; ".join(result.issues[:2]),  # Show first 2 issues
                    )

            console.print(table)


# ============================================================================
# ENHANCED AGENT SUBCLASSES
# ============================================================================


class CompatibilityEnhancedSequentialAgent(CompatibilityEnhancedMultiAgent):
    """Sequential agent with built-in compatibility checking."""

    def __init__(self, **kwargs):
        kwargs["execution_mode"] = ExecutionMode.SEQUENCE
        super().__init__(**kwargs)


class CompatibilityEnhancedConditionalAgent(CompatibilityEnhancedMultiAgent):
    """Conditional agent with built-in compatibility checking."""

    def __init__(self, **kwargs):
        kwargs["execution_mode"] = ExecutionMode.CONDITIONAL
        super().__init__(**kwargs)


class CompatibilityEnhancedParallelAgent(CompatibilityEnhancedMultiAgent):
    """Parallel agent with built-in compatibility checking."""

    def __init__(self, **kwargs):
        kwargs["execution_mode"] = ExecutionMode.PARALLEL
        super().__init__(**kwargs)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def create_compatible_multi_agent(
    agents: list[Agent],
    execution_mode: ExecutionMode = ExecutionMode.SEQUENCE,
    compatibility_mode: CompatibilityMode = CompatibilityMode.ADAPTIVE,
    **kwargs,
) -> CompatibilityEnhancedMultiAgent:
    """Create a multi-agent system with automatic compatibility checking.

    This function creates a multi-agent system and automatically checks and fixes
    compatibility issues based on the specified compatibility mode.
    """
    system = CompatibilityEnhancedMultiAgent(
        execution_mode=execution_mode, compatibility_mode=compatibility_mode, **kwargs
    )

    # Add agents one by one with compatibility checking
    for agent in agents:
        system.add_agent(agent)

    return system
