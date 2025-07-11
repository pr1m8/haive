"""Tool integration for ReWOO evidence system.

This module provides the integration between ReWOO's evidence-based planning
and the tool execution system.
"""

from typing import Any, Dict, List, Optional, Union

from haive.core.tools import tool
from pydantic import Field

from haive.agents.planning.rewoo.models import Evidence, EvidenceStatus, ToolCall
from haive.agents.planning.rewoo.state import ReWOOState


class ReWOOToolExecutor:
    """Executes tools for ReWOO evidence collection."""

    def __init__(self, state: ReWOOState):
        self.state = state

    async def execute_evidence_collection(self, evidence: Evidence) -> dict[str, Any]:
        """Execute tool to collect evidence.

        Args:
            evidence: Evidence to collect

        Returns:
            Result dict with status and content
        """
        # Get tool for this evidence
        tool = self.state.get_tool_by_name(evidence.source)
        if not tool:
            return {"status": "error", "error": f"Tool '{evidence.source}' not found"}

        # Resolve evidence references in collection method
        resolved_method = evidence.resolve_references(self.state.evidence_map)

        try:
            # Execute tool
            result = await self._execute_tool(tool, resolved_method)

            # Update evidence
            self.state.update_evidence(
                evidence.id, status=EvidenceStatus.COLLECTED, content=result
            )

            # Track in tool results
            self.state.add_tool_result(evidence.source, result)

            return {"status": "success", "content": result, "evidence_id": evidence.id}

        except Exception as e:
            # Update evidence with error
            self.state.update_evidence(
                evidence.id, status=EvidenceStatus.FAILED, error=str(e)
            )

            return {"status": "error", "error": str(e), "evidence_id": evidence.id}

    async def _execute_tool(self, tool: Any, resolved_method: str) -> Any:
        """Execute a tool with resolved arguments.

        This is a simplified implementation - in practice would
        parse the method string and execute properly.
        """
        # For now, just return a placeholder
        # Real implementation would parse and execute
        return f"Result of {resolved_method}"

    async def execute_tool_call(
        self, tool_call: ToolCall, evidence_id: str | None = None
    ) -> dict[str, Any]:
        """Execute a tool call with evidence tracking.

        Args:
            tool_call: Tool call to execute
            evidence_id: Optional evidence ID this contributes to

        Returns:
            Execution result
        """
        # Get the tool
        tool = self.state.get_tool_by_name(tool_call.tool_name)
        if not tool:
            return {
                "status": "error",
                "error": f"Tool '{tool_call.tool_name}' not found",
            }

        # Resolve arguments
        resolved_args = tool_call.resolve_arguments(self.state.evidence_map)

        try:
            # Execute based on tool type
            if tool_call.is_llm_call:
                result = await self._execute_llm_reasoning(resolved_args)
            else:
                result = await self._execute_standard_tool(tool, resolved_args)

            # Validate output if schema provided
            if tool_call.expected_output_schema:
                if not tool_call.validate_output(result):
                    return {
                        "status": "error",
                        "error": "Output validation failed",
                        "result": result,
                    }

            # Update evidence if linked
            if evidence_id:
                self.state.update_evidence(
                    evidence_id, status=EvidenceStatus.COLLECTED, content=result
                )

            # Track result
            self.state.add_tool_result(tool_call.tool_name, result)

            return {
                "status": "success",
                "result": result,
                "tool_name": tool_call.tool_name,
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tool_name": tool_call.tool_name,
            }

    async def _execute_llm_reasoning(self, args: dict[str, Any]) -> str:
        """Execute LLM reasoning."""
        # Use the main engine from state for reasoning
        # This is simplified - real implementation would format prompt
        return "LLM reasoning result"

    async def _execute_standard_tool(self, tool: Any, args: dict[str, Any]) -> Any:
        """Execute a standard tool."""
        # Simplified - real implementation would handle different tool types
        if hasattr(tool, "ainvoke"):
            return await tool.ainvoke(**args)
        if hasattr(tool, "invoke"):
            return tool.invoke(**args)
        if callable(tool):
            return tool(**args)
        raise ValueError(f"Don't know how to execute tool: {tool}")

    def get_ready_evidence(self) -> list[Evidence]:
        """Get evidence ready for collection."""
        return self.state.ready_evidence

    def is_collection_complete(self) -> bool:
        """Check if all evidence collection is complete."""
        return self.state.is_evidence_complete


# Example tool definitions for ReWOO
@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"


@tool
def calculate_tool(expression: str) -> float:
    """Calculate mathematical expression."""
    # Simplified - use safe evaluation in production
    return eval(expression, {"__builtins__": {}})


@tool
def analyze_tool(data: str, method: str = "summary") -> str:
    """Analyze data with specified method."""
    return f"Analysis of {data} using {method}"


# Tool registry for ReWOO agents
REWOO_TOOLS = [
    search_tool,
    calculate_tool,
    analyze_tool,
]
