"""Safe Agent Compatibility Testing.

This module provides comprehensive compatibility testing for RAG agents using the
compatibility module without modifying or breaking existing agents.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from haive.core.schema.compatibility import (
    ConverterRegistry,
    TypeAnalyzer,
)
from haive.core.schema.compatibility.reports import generate_report

from haive.agents.base.agent import Agent
from haive.agents.rag.multi_agent_rag.agents import DocumentGradingAgent
from haive.agents.rag.multi_agent_rag.state import MultiAgentRAGState

logger = logging.getLogger(__name__)


class CompatibilityLevel(str, Enum):
    """Levels of compatibility between agents."""

    PERFECT = "perfect"  # Fully compatible, no issues
    COMPATIBLE = "compatible"  # Compatible with minor issues
    ADAPTABLE = "adaptable"  # Can be made compatible with adapters
    PROBLEMATIC = "problematic"  # Significant compatibility issues
    INCOMPATIBLE = "incompatible"  # Cannot be made compatible


@dataclass
class AgentCompatibilityReport:
    """Comprehensive compatibility report for agent pairs."""

    source_agent: str
    target_agent: str
    compatibility_level: CompatibilityLevel
    compatibility_score: float
    issues: list[str]
    missing_fields: list[str]
    conflicting_fields: list[str]
    suggested_mappings: dict[str, str]
    recommended_adapters: list[str]
    safe_to_chain: bool
    quality_assessment: str
    detailed_analysis: dict[str, Any]


@dataclass
class MultiAgentCompatibilityReport:
    """Compatibility report for multiple agents in a workflow."""

    workflow_name: str
    overall_compatible: bool
    total_agents: int
    compatible_pairs: int
    total_pairs: int
    compatibility_matrix: dict[tuple[str, str], AgentCompatibilityReport]
    workflow_recommendations: list[str]
    required_adapters: list[dict[str, Any]]
    risk_assessment: str


class SafeCompatibilityTester:
    """Safe compatibility testing that doesn't modify original agents.

    This class provides comprehensive compatibility analysis between agents
    without risking damage to existing systems.
    """

    def __init__(self) -> None:
        self.analyzer = TypeAnalyzer()
        self.converter_registry = ConverterRegistry()
        self._test_cache = {}

    def test_agent_pair_compatibility(
        self, source_agent: Agent, target_agent: Agent, safe_mode: bool = True
    ) -> AgentCompatibilityReport:
        """Safely test compatibility between two agents.

        Args:
            source_agent: The source agent in the workflow
            target_agent: The target agent in the workflow
            safe_mode: If True, uses read-only testing without modifications

        Returns:
            Detailed compatibility report
        """
        source_name = getattr(source_agent, "name", source_agent.__class__.__name__)
        target_name = getattr(target_agent, "name", target_agent.__class__.__name__)

        # Create cache key for this test
        cache_key = f"{source_name}_{target_name}"
        if cache_key in self._test_cache:
            return self._test_cache[cache_key]

        try:
            # Safely extract schemas without modifying agents
            source_schema = self._safe_extract_output_schema(source_agent)
            target_schema = self._safe_extract_input_schema(target_agent)

            if not source_schema or not target_schema:
                return self._create_error_report(
                    source_name, target_name, "Could not safely extract agent schemas"
                )

            # Perform basic compatibility check
            compat_result = self._basic_schema_compatibility_check(
                source_schema, target_schema
            )

            # Analyze schemas in detail
            source_analysis = self.analyzer.analyze_schema(source_schema)
            target_analysis = self.analyzer.analyze_schema(target_schema)

            # Generate detailed report
            detailed_report = generate_report(source_schema, target_schema)

            # Assess compatibility level
            level = self._assess_compatibility_level(compat_result, detailed_report)

            # Create comprehensive report
            report = AgentCompatibilityReport(
                source_agent=source_name,
                target_agent=target_name,
                compatibility_level=level,
                compatibility_score=self._calculate_compatibility_score(compat_result),
                issues=self._extract_issues(compat_result, detailed_report),
                missing_fields=getattr(compat_result, "missing_required_fields", []),
                conflicting_fields=self._find_conflicting_fields(
                    source_analysis, target_analysis
                ),
                suggested_mappings=self._generate_field_mappings(
                    source_analysis, target_analysis
                ),
                recommended_adapters=self._recommend_adapters(compat_result),
                safe_to_chain=level
                in [CompatibilityLevel.PERFECT, CompatibilityLevel.COMPATIBLE],
                quality_assessment=self._assess_quality(compat_result),
                detailed_analysis={
                    "source_fields": len(source_analysis.fields),
                    "target_fields": len(target_analysis.fields),
                    "shared_fields": len(
                        set(source_analysis.fields.keys())
                        & set(target_analysis.fields.keys())
                    ),
                    "conversion_paths": self._find_conversion_paths(
                        source_schema, target_schema
                    ),
                },
            )

            # Cache the result
            self._test_cache[cache_key] = report
            return report

        except Exception as e:
            logger.exception(
                f"Error testing compatibility between {source_name} and {target_name}: {e!s}"
            )
            return self._create_error_report(
                source_name, target_name, f"Compatibility test failed: {e!s}"
            )

    def test_workflow_compatibility(
        self, agents: list[Agent], workflow_name: str = "RAG Workflow"
    ) -> MultiAgentCompatibilityReport:
        """Test compatibility across an entire workflow of agents.

        Args:
            agents: List of agents in workflow order
            workflow_name: Name of the workflow being tested

        Returns:
            Comprehensive workflow compatibility report
        """
        if len(agents) < 2:
            return MultiAgentCompatibilityReport(
                workflow_name=workflow_name,
                overall_compatible=True,
                total_agents=len(agents),
                compatible_pairs=0,
                total_pairs=0,
                compatibility_matrix={},
                workflow_recommendations=[
                    "Single agent workflow - no compatibility issues"
                ],
                required_adapters=[],
                risk_assessment="Low - single agent workflow",
            )

        compatibility_matrix = {}
        compatible_pairs = 0
        total_pairs = len(agents) - 1

        # Test each adjacent pair
        for i in range(len(agents) - 1):
            source_agent = agents[i]
            target_agent = agents[i + 1]

            report = self.test_agent_pair_compatibility(source_agent, target_agent)

            key = (report.source_agent, report.target_agent)
            compatibility_matrix[key] = report

            if report.safe_to_chain:
                compatible_pairs += 1

        # Assess overall workflow
        overall_compatible = compatible_pairs == total_pairs

        # Generate workflow recommendations
        recommendations = self._generate_workflow_recommendations(
            compatibility_matrix, agents
        )

        # Identify required adapters
        required_adapters = self._identify_required_adapters(compatibility_matrix)

        # Assess risk
        risk_assessment = self._assess_workflow_risk(compatibility_matrix)

        return MultiAgentCompatibilityReport(
            workflow_name=workflow_name,
            overall_compatible=overall_compatible,
            total_agents=len(agents),
            compatible_pairs=compatible_pairs,
            total_pairs=total_pairs,
            compatibility_matrix=compatibility_matrix,
            workflow_recommendations=recommendations,
            required_adapters=required_adapters,
            risk_assessment=risk_assessment,
        )

    def test_rag_agents_safely(self) -> dict[str, Any]:
        """Safely test compatibility of common RAG agent combinations.

        Returns:
            Comprehensive test results for common RAG patterns
        """
        # Import agents safely
        try:
            from haive.agents.rag.multi_agent_rag.agents import (
                SIMPLE_RAG_AGENT,
                SIMPLE_RAG_ANSWER_AGENT,
            )

            # Test basic RAG chain
            basic_chain_report = self.test_agent_pair_compatibility(
                SIMPLE_RAG_AGENT, SIMPLE_RAG_ANSWER_AGENT
            )

            # Test with grading agent
            grading_agent = DocumentGradingAgent()
            with_grading_report = self.test_workflow_compatibility(
                [SIMPLE_RAG_AGENT, grading_agent, SIMPLE_RAG_ANSWER_AGENT],
                "RAG with Document Grading",
            )

            # Test state compatibility
            state_compatibility = self._test_state_compatibility()

            return {
                "basic_rag_chain": basic_chain_report,
                "rag_with_grading": with_grading_report,
                "state_compatibility": state_compatibility,
                "test_timestamp": self._get_timestamp(),
                "safety_status": "All tests completed safely",
            }

        except Exception as e:
            logger.exception(f"Error in safe RAG testing: {e!s}")
            return {
                "error": str(e),
                "safety_status": "Tests failed but no agents were modified",
                "recommendation": "Check agent imports and schema definitions",
            }

    def _safe_extract_output_schema(self, agent: Agent) -> type | None:
        """Safely extract output schema without modifying agent."""
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
        except Exception as e:
            logger.warning(f"Could not extract output schema from {agent}: {e!s}")
            return None

    def _safe_extract_input_schema(self, agent: Agent) -> type | None:
        """Safely extract input schema without modifying agent."""
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
        except Exception as e:
            logger.warning(f"Could not extract input schema from {agent}: {e!s}")
            return None

    def _assess_compatibility_level(
        self, compat_result, detailed_report
    ) -> CompatibilityLevel:
        """Assess the compatibility level based on results."""
        if getattr(compat_result, "is_compatible", False):
            if not getattr(compat_result, "missing_required_fields", []):
                return CompatibilityLevel.PERFECT
            return CompatibilityLevel.COMPATIBLE
        missing_count = len(getattr(compat_result, "missing_required_fields", []))
        if missing_count <= 2:
            return CompatibilityLevel.ADAPTABLE
        if missing_count <= 5:
            return CompatibilityLevel.PROBLEMATIC
        return CompatibilityLevel.INCOMPATIBLE

    def _calculate_compatibility_score(self, compat_result) -> float:
        """Calculate a numeric compatibility score."""
        if getattr(compat_result, "is_compatible", False):
            base_score = 0.8
            missing_fields = len(getattr(compat_result, "missing_required_fields", []))
            penalty = min(0.3, missing_fields * 0.1)
            return max(0.0, base_score - penalty)
        # Partial compatibility based on what can be adapted
        missing_fields = len(getattr(compat_result, "missing_required_fields", []))
        return max(0.0, 0.5 - (missing_fields * 0.05))

    def _extract_issues(self, compat_result, detailed_report) -> list[str]:
        """Extract compatibility issues from results."""
        issues = []

        if hasattr(compat_result, "issues"):
            issues.extend(compat_result.issues)

        missing_fields = getattr(compat_result, "missing_required_fields", [])
        if missing_fields:
            issues.append(f"Missing required fields: {', '.join(missing_fields)}")

        return issues

    def _find_conflicting_fields(self, source_analysis, target_analysis) -> list[str]:
        """Find fields that exist in both schemas but with different types."""
        conflicts = []

        for field_name in source_analysis.fields:
            if field_name in target_analysis.fields:
                source_field = source_analysis.fields[field_name]
                target_field = target_analysis.fields[field_name]

                # Check for type conflicts
                if getattr(source_field, "type", None) != getattr(
                    target_field, "type", None
                ):
                    conflicts.append(field_name)

        return conflicts

    def _generate_field_mappings(
        self, source_analysis, target_analysis
    ) -> dict[str, str]:
        """Generate suggested field mappings between schemas."""
        mappings = {}

        source_fields = set(source_analysis.fields.keys())
        target_fields = set(target_analysis.fields.keys())

        # Find similar field names
        for source_field in source_fields:
            for target_field in target_fields:
                if self._fields_similar(source_field, target_field):
                    mappings[source_field] = target_field

        return mappings

    def _fields_similar(self, field1: str, field2: str) -> bool:
        """Check if two field names are similar enough to suggest mapping."""
        # Simple similarity check
        if field1 == field2:
            return True

        # Check for common synonyms
        synonyms = {
            "query": ["question", "q", "search"],
            "documents": ["docs", "results", "data"],
            "answer": ["response", "result", "output"],
        }

        for base, syns in synonyms.items():
            if (field1 == base and field2 in syns) or (
                field2 == base and field1 in syns
            ):
                return True

        return False

    def _recommend_adapters(self, compat_result) -> list[str]:
        """Recommend adapter strategies for compatibility issues."""
        adapters = []

        missing_fields = getattr(compat_result, "missing_required_fields", [])
        if missing_fields:
            adapters.append("FieldMappingAdapter")

        if not getattr(compat_result, "is_compatible", False):
            adapters.append("SchemaTransformationAdapter")

        return adapters

    def _assess_quality(self, compat_result) -> str:
        """Assess the quality of the compatibility."""
        if getattr(compat_result, "is_compatible", False):
            missing_count = len(getattr(compat_result, "missing_required_fields", []))
            if missing_count == 0:
                return "Excellent - Perfect compatibility"
            if missing_count <= 2:
                return "Good - Minor compatibility issues"
            return "Fair - Some compatibility concerns"
        return "Poor - Significant compatibility issues"

    def _find_conversion_paths(self, source_schema, target_schema) -> list[str]:
        """Find possible conversion paths between schemas."""
        paths = []

        try:
            # Check if direct conversion is possible
            if self.converter_registry.can_convert(source_schema, target_schema):
                paths.append("Direct conversion available")

            # Check for multi-step conversions
            # This is a simplified check - real implementation would be more sophisticated
            common_types = [str, int, float, dict, list]
            for intermediate in common_types:
                if self.converter_registry.can_convert(
                    source_schema, intermediate
                ) and self.converter_registry.can_convert(intermediate, target_schema):
                    paths.append(f"Conversion via {intermediate.__name__}")
        except Exception:
            paths.append("Conversion analysis failed")

        return paths

    def _generate_workflow_recommendations(
        self, compatibility_matrix, agents
    ) -> list[str]:
        """Generate recommendations for improving workflow compatibility."""
        recommendations = []

        for _key, report in compatibility_matrix.items():
            if not report.safe_to_chain:
                recommendations.append(
                    f"Add adapter between {report.source_agent} and {report.target_agent}"
                )

                if report.recommended_adapters:
                    recommendations.append(
                        f"Consider using: {', '.join(report.recommended_adapters)}"
                    )

        if not recommendations:
            recommendations.append("Workflow is fully compatible - no changes needed")

        return recommendations

    def _identify_required_adapters(self, compatibility_matrix) -> list[dict[str, Any]]:
        """Identify specific adapters needed for workflow compatibility."""
        adapters = []

        for _key, report in compatibility_matrix.items():
            if not report.safe_to_chain:
                adapter_spec = {
                    "source": report.source_agent,
                    "target": report.target_agent,
                    "type": "FieldMappingAdapter",
                    "mappings": report.suggested_mappings,
                    "missing_fields": report.missing_fields,
                }
                adapters.append(adapter_spec)

        return adapters

    def _assess_workflow_risk(self, compatibility_matrix) -> str:
        """Assess the risk level of the workflow."""
        incompatible_count = sum(
            1 for report in compatibility_matrix.values() if not report.safe_to_chain
        )

        total_connections = len(compatibility_matrix)

        if incompatible_count == 0:
            return "Low - All agents are compatible"
        if incompatible_count <= total_connections * 0.3:
            return "Medium - Some compatibility issues"
        return "High - Significant compatibility problems"

    def _test_state_compatibility(self) -> dict[str, Any]:
        """Test compatibility with the RAG state schema."""
        try:
            state_analysis = self.analyzer.analyze_schema(MultiAgentRAGState)

            return {
                "state_schema": "MultiAgentRAGState",
                "total_fields": len(state_analysis.fields),
                "shared_fields": state_analysis.shared_fields,
                "reducer_fields": getattr(state_analysis, "reducer_fields", {}),
                "compatibility_status": "Schema analysis successful",
            }
        except Exception as e:
            return {"error": str(e), "compatibility_status": "Schema analysis failed"}

    def _create_error_report(
        self, source_name: str, target_name: str, error_msg: str
    ) -> AgentCompatibilityReport:
        """Create an error report for failed compatibility tests."""
        return AgentCompatibilityReport(
            source_agent=source_name,
            target_agent=target_name,
            compatibility_level=CompatibilityLevel.INCOMPATIBLE,
            compatibility_score=0.0,
            issues=[error_msg],
            missing_fields=[],
            conflicting_fields=[],
            suggested_mappings={},
            recommended_adapters=[],
            safe_to_chain=False,
            quality_assessment="Error - Could not complete compatibility test",
            detailed_analysis={"error": error_msg},
        )

    def _basic_schema_compatibility_check(self, source_schema, target_schema):
        """Basic schema compatibility check without CompatibilityChecker."""

        class BasicResult:
            def __init__(self) -> None:
                self.is_compatible = True
                self.missing_required_fields = []
                self.issues = []

        result = BasicResult()

        try:
            # Simple field-based compatibility check
            if hasattr(source_schema, "__fields__") and hasattr(
                target_schema, "__fields__"
            ):
                source_fields = set(source_schema.__fields__.keys())
                target_fields = set(target_schema.__fields__.keys())

                missing = target_fields - source_fields
                if missing:
                    result.missing_required_fields = list(missing)
                    result.is_compatible = False
                    result.issues.append(f"Missing fields: {', '.join(missing)}")

        except Exception as e:
            result.is_compatible = False
            result.issues.append(f"Schema analysis failed: {e}")

        return result

    def _get_timestamp(self) -> str:
        """Get current timestamp for reports."""
        from datetime import datetime

        return datetime.now().isoformat()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def safe_test_rag_compatibility() -> dict[str, Any]:
    """Safely test RAG agent compatibility without breaking anything.

    This is the main function to use for testing RAG agent compatibility.
    """
    tester = SafeCompatibilityTester()
    return tester.test_rag_agents_safely()


def test_custom_agent_workflow(
    agents: list[Agent], workflow_name: str
) -> MultiAgentCompatibilityReport:
    """Test compatibility of a custom agent workflow.

    Args:
        agents: List of agents to test
        workflow_name: Name for the workflow

    Returns:
        Comprehensive compatibility report
    """
    tester = SafeCompatibilityTester()
    return tester.test_workflow_compatibility(agents, workflow_name)


def quick_agent_compatibility_check(agent1: Agent, agent2: Agent) -> bool:
    """Quick compatibility check between two agents.

    Returns:
        True if agents are safe to chain, False otherwise
    """
    tester = SafeCompatibilityTester()
    report = tester.test_agent_pair_compatibility(agent1, agent2)
    return report.safe_to_chain
