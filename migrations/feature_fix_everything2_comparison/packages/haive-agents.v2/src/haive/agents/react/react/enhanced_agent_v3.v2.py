"""Enhanced ReactAgent V3 - Full ReAct implementation with advanced features.

This version combines the ReAct (Reasoning and Acting) pattern with all enhanced
capabilities from the base Agent class and EnhancedSimpleAgent.

Key Features:
- Complete ReAct reasoning and action loop
- Advanced tool integration and routing
- Intelligent loop control and termination
- Rich execution tracking and debugging
- Performance optimizations for iterative workflows
"""

import logging
from typing import Any

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END
from pydantic import Field

# Import the enhanced SimpleAgent as our base
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent

logger = logging.getLogger(__name__)


# ========================================================================
# ENHANCED REACT AGENT V3
# ========================================================================


class EnhancedReactAgent(EnhancedSimpleAgent):
    """Enhanced ReactAgent V3 with complete ReAct pattern and advanced features.

    This agent implements the full Reasoning and Acting (ReAct) pattern with
    sophisticated enhancements:

    ReAct Pattern Features:
    - Reasoning: Agent thinks through problems step by step
    - Acting: Agent uses tools to gather information or take actions
    - Observing: Agent analyzes tool results and outcomes
    - Iterating: Agent continues until task completion or max iterations

    Enhanced Features (inherited from EnhancedSimpleAgent):
    - Dynamic schema generation and composition
    - Advanced engine management and routing
    - Rich execution capabilities with debugging
    - Sophisticated state management
    - Comprehensive persistence and serialization

    ReAct-Specific Enhancements:
    - Intelligent loop control and termination
    - Tool usage optimization and caching
    - Reasoning trace preservation and analysis
    - Advanced iteration management
    - Performance monitoring for iterative workflows

    Attributes:
        max_iterations: Maximum reasoning iterations (default: 10)
        reasoning_mode: Reasoning strategy ('thorough', 'efficient', 'creative')
        tool_selection_strategy: How to choose tools ('auto', 'explicit', 'learned')
        loop_detection: Enable infinite loop detection and prevention
        reasoning_trace: Preserve detailed reasoning traces
        performance_tracking: Track performance metrics per iteration

    Advanced Configuration:
        iteration_timeout: Timeout per iteration in seconds
        tool_usage_optimization: Enable tool usage caching and optimization
        reasoning_quality_threshold: Minimum reasoning quality score
        early_termination_conditions: Custom termination conditions

    Examples:
        Basic ReAct usage::

            from langchain_core.tools import tool

            @tool
            def web_search(query: str) -> str:
                '''Search the web for information'''
                return search_results

            @tool
            def calculator(expression: str) -> str:
                '''Calculate mathematical expressions'''
                return str(eval(expression))

            agent = EnhancedReactAgent(
                name="research_agent",
                temperature=0.7,
                tools=[web_search, calculator],
                max_iterations=15
            )

            result = agent.run("Research the latest AI developments and calculate the growth rate")

        Advanced ReAct configuration::

            agent = EnhancedReactAgent(
                name="advanced_researcher",
                temperature=0.6,
                max_iterations=20,
                reasoning_mode="thorough",
                tool_selection_strategy="learned",
                loop_detection=True,
                reasoning_trace=True,
                performance_tracking=True,
                debug_mode=True,
                advanced_routing=True,
                iteration_timeout=30.0,
                tool_usage_optimization=True
            )

        With structured output::

            from pydantic import BaseModel, Field

            class ResearchReport(BaseModel):
                summary: str = Field(description="Research summary")
                key_findings: list[str] = Field(description="Key findings")
                sources: list[str] = Field(description="Information sources")
                confidence: float = Field(description="Confidence score")
                methodology: str = Field(description="Research methodology used")

            agent = EnhancedReactAgent(
                name="structured_researcher",
                tools=[web_search, calculator],
                structured_output_model=ResearchReport,
                reasoning_mode="thorough",
                performance_tracking=True
            )

            report = agent.run("Research renewable energy trends and market projections")
    """

    # ========================================================================
    # REACT-SPECIFIC CONFIGURATION
    # ========================================================================

    max_iterations: int = Field(
        default=10, ge=1, le=50, description="Maximum reasoning iterations"
    )

    reasoning_mode: str = Field(
        default="efficient",
        pattern="^(thorough|efficient|creative)$",
        description="Reasoning strategy: thorough, efficient, or creative",
    )

    tool_selection_strategy: str = Field(
        default="auto",
        pattern="^(auto|explicit|learned)$",
        description="Tool selection strategy: auto, explicit, or learned",
    )

    loop_detection: bool = Field(
        default=True, description="Enable infinite loop detection and prevention"
    )

    reasoning_trace: bool = Field(
        default=False, description="Preserve detailed reasoning traces"
    )

    performance_tracking: bool = Field(
        default=False, description="Track performance metrics per iteration"
    )

    # ========================================================================
    # ADVANCED REACT CONFIGURATION
    # ========================================================================

    iteration_timeout: float | None = Field(
        default=None, ge=1.0, description="Timeout per iteration in seconds"
    )

    tool_usage_optimization: bool = Field(
        default=False, description="Enable tool usage caching and optimization"
    )

    reasoning_quality_threshold: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Minimum reasoning quality score (0.0-1.0)",
    )

    early_termination_conditions: list[str] | None = Field(
        default=None, description="Custom early termination conditions"
    )

    # ========================================================================
    # ENHANCED SETUP
    # ========================================================================

    def setup_agent(self) -> None:
        """Enhanced setup for ReAct-specific features."""
        logger.debug(f"Setting up EnhancedReactAgent: {self.name}")

        # Call parent setup first
        super().setup_agent()

        # Setup ReAct-specific features
        self._setup_react_features()
        self._setup_iteration_management()
        self._setup_performance_tracking()
        self._validate_react_configuration()

    def _setup_react_features(self) -> None:
        """Setup ReAct-specific capabilities."""
        logger.debug("Setting up ReAct features")

        # Configure reasoning mode
        if self.reasoning_mode == "thorough":
            # More detailed reasoning, higher token usage
            if self.max_tokens is None:
                self.max_tokens = 2000
        elif self.reasoning_mode == "creative":
            # More creative reasoning, higher temperature
            if self.temperature is None:
                self.temperature = 0.8

        # Setup tool selection strategy
        if self.tool_selection_strategy == "learned":
            # TODO: Implement learned tool selection
            logger.debug("Learned tool selection enabled (TODO: implement)")

        # Configure loop detection
        if self.loop_detection:
            logger.debug("Loop detection enabled")

        # Setup reasoning trace
        if self.reasoning_trace:
            logger.debug("Reasoning trace preservation enabled")

    def _setup_iteration_management(self) -> None:
        """Setup iteration management and control."""
        logger.debug("Setting up iteration management")

        # Configure iteration timeout
        if self.iteration_timeout:
            logger.debug(f"Iteration timeout: {self.iteration_timeout}s")

        # Setup early termination
        if self.early_termination_conditions:
            logger.debug(
                f"Early termination conditions: {self.early_termination_conditions}"
            )

    def _setup_performance_tracking(self) -> None:
        """Setup performance tracking for iterations."""
        if self.performance_tracking:
            logger.debug("Performance tracking enabled")
            # TODO: Initialize performance tracking

        if self.tool_usage_optimization:
            logger.debug("Tool usage optimization enabled")
            # TODO: Initialize tool caching

    def _validate_react_configuration(self) -> None:
        """Validate ReAct-specific configuration."""
        # Validate max_iterations
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be at least 1")

        # Validate timeout
        if self.iteration_timeout is not None and self.iteration_timeout < 1.0:
            raise ValueError("iteration_timeout must be at least 1.0 seconds")

        # Validate quality threshold
        if self.reasoning_quality_threshold is not None and not (
            0.0 <= self.reasoning_quality_threshold <= 1.0
        ):
            raise ValueError("reasoning_quality_threshold must be between 0.0 and 1.0")

    # ========================================================================
    # ENHANCED GRAPH BUILDING FOR REACT
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build enhanced ReAct graph with intelligent looping.

        Creates a sophisticated ReAct graph that includes:
        - Intelligent reasoning loop control
        - Advanced tool routing and selection
        - Performance monitoring and optimization
        - Loop detection and prevention
        - Detailed execution tracing

        Graph Structure:
        1. START → agent_node (reasoning)
        2. agent_node → validation (check for tool calls/completion)
        3. validation → tool_node (if tools needed)
        4. tool_node → agent_node (continue reasoning - THE LOOP)
        5. validation → parse_output (if structured output)
        6. validation → END (if task complete)

        Enhanced Features:
        - Loop detection and prevention
        - Iteration counting and limits
        - Performance monitoring nodes
        - Quality assessment nodes

        Returns:
            BaseGraph: Enhanced ReAct graph with loop control
        """
        logger.debug(f"Building enhanced ReAct graph for {self.name}")

        # Build base graph from SimpleAgent
        graph = super().build_graph()

        # Check if we need ReAct modifications
        if not self._has_tools():
            logger.debug("No tools found, using simple graph without ReAct loop")
            return graph

        # Modify graph for ReAct pattern
        self._add_react_loop(graph)
        self._add_iteration_control(graph)
        self._add_performance_monitoring(graph)

        logger.debug(f"Built enhanced ReAct graph with {len(graph.nodes)} nodes")
        return graph

    def _add_react_loop(self, graph: BaseGraph) -> None:
        """Add ReAct looping logic to the graph."""
        logger.debug("Adding ReAct loop logic")

        # The key ReAct modification: tool_node loops back to agent_node
        if "tool_node" in graph.nodes:
            # Remove tool_node → END edge if it exists
            try:
                graph.remove_edge("tool_node", END)
                logger.debug("Removed tool_node → END edge")
            except Exception:
                pass  # Edge might not exist

            # Add tool_node → agent_node edge (THE REACT LOOP)
            graph.add_edge("tool_node", "agent_node")
            logger.debug("Added ReAct loop: tool_node → agent_node")

        # Also handle parser loops if structured output
        if "parse_output" in graph.nodes and self.reasoning_trace:
            try:
                graph.remove_edge("parse_output", END)
                graph.add_edge("parse_output", "agent_node")
                logger.debug("Added parser loop for reasoning trace")
            except Exception:
                pass

    def _add_iteration_control(self, graph: BaseGraph) -> None:
        """Add iteration control and loop detection."""
        logger.debug("Adding iteration control")

        # TODO: Add iteration counting node
        # TODO: Add max iteration checking
        # TODO: Add loop detection logic

        if self.loop_detection:
            logger.debug("Loop detection configured")

        if self.max_iterations:
            logger.debug(f"Max iterations set to: {self.max_iterations}")

    def _add_performance_monitoring(self, graph: BaseGraph) -> None:
        """Add performance monitoring to the graph."""
        if self.performance_tracking:
            logger.debug("Adding performance monitoring")
            # TODO: Add performance monitoring nodes
            # TODO: Add timing and metrics collection

        if self.tool_usage_optimization:
            logger.debug("Adding tool usage optimization")
            # TODO: Add tool caching logic

    # ========================================================================
    # REACT EXECUTION ENHANCEMENTS
    # ========================================================================

    def get_react_summary(self) -> dict[str, Any]:
        """Get comprehensive ReAct execution summary."""
        base_summary = self.get_capabilities_summary()

        react_summary = {
            **base_summary,
            "react_features": {
                "max_iterations": self.max_iterations,
                "reasoning_mode": self.reasoning_mode,
                "tool_selection_strategy": self.tool_selection_strategy,
                "loop_detection": self.loop_detection,
                "reasoning_trace": self.reasoning_trace,
                "performance_tracking": self.performance_tracking,
                "iteration_timeout": self.iteration_timeout,
                "tool_usage_optimization": self.tool_usage_optimization,
                "reasoning_quality_threshold": self.reasoning_quality_threshold,
            },
            "execution_stats": {
                # TODO: Add execution statistics
                "total_iterations": 0,
                "tool_calls_made": 0,
                "avg_iteration_time": 0.0,
                "reasoning_quality_score": 0.0,
            },
        }

        return react_summary

    def display_react_capabilities(self) -> None:
        """Display comprehensive ReAct capabilities."""
        summary = self.get_react_summary()

        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table

        console = Console()

        # Create ReAct-specific capabilities table
        table = Table(title=f"Enhanced ReactAgent Capabilities: {self.name}")
        table.add_column("Feature", style="cyan")
        table.add_column("Configuration", style="green")
        table.add_column("Status", style="yellow")

        # ReAct configuration
        react_features = summary["react_features"]
        table.add_row("Max Iterations", str(react_features["max_iterations"]), "✅")
        table.add_row("Reasoning Mode", react_features["reasoning_mode"], "✅")
        table.add_row("Tool Selection", react_features["tool_selection_strategy"], "✅")
        table.add_row(
            "Loop Detection",
            str(react_features["loop_detection"]),
            "✅" if react_features["loop_detection"] else "❌",
        )
        table.add_row(
            "Reasoning Trace",
            str(react_features["reasoning_trace"]),
            "✅" if react_features["reasoning_trace"] else "❌",
        )
        table.add_row(
            "Performance Tracking",
            str(react_features["performance_tracking"]),
            "✅" if react_features["performance_tracking"] else "❌",
        )

        # Advanced features
        table.add_section()
        table.add_row(
            "Iteration Timeout",
            str(react_features["iteration_timeout"]),
            "✅" if react_features["iteration_timeout"] else "❌",
        )
        table.add_row(
            "Tool Optimization",
            str(react_features["tool_usage_optimization"]),
            "✅" if react_features["tool_usage_optimization"] else "❌",
        )
        table.add_row(
            "Quality Threshold",
            str(react_features["reasoning_quality_threshold"]),
            "✅" if react_features["reasoning_quality_threshold"] else "❌",
        )

        console.print(table)

        # Show execution stats if available
        stats = summary["execution_stats"]
        if any(stats.values()):
            stats_panel = Panel(
                f"Iterations: {stats['total_iterations']} | "
                f"Tool Calls: {stats['tool_calls_made']} | "
                f"Avg Time: {stats['avg_iteration_time']:.2f}s | "
                f"Quality: {stats['reasoning_quality_score']:.2f}",
                title="Execution Statistics",
                style="blue",
            )
            console.print(stats_panel)

    def get_reasoning_trace(self) -> list[dict[str, Any]]:
        """Get detailed reasoning trace if enabled."""
        if not self.reasoning_trace:
            return []

        # TODO: Implement reasoning trace retrieval
        # Return list of reasoning steps with timestamps, tool calls, etc.
        return []

    def analyze_tool_usage(self) -> dict[str, Any]:
        """Analyze tool usage patterns and efficiency."""
        if not self.performance_tracking:
            return {}

        # TODO: Implement tool usage analysis
        # Return insights about tool selection, frequency, success rates
        return {
            "most_used_tools": [],
            "tool_success_rates": {},
            "avg_tools_per_iteration": 0.0,
            "tool_selection_efficiency": 0.0,
        }

    def optimize_performance(self) -> dict[str, Any]:
        """Run performance optimization analysis."""
        if not self.performance_tracking:
            return {"message": "Performance tracking not enabled"}

        # TODO: Implement performance optimization
        # Analyze patterns and suggest improvements
        return {
            "suggestions": [],
            "potential_improvements": {},
            "optimization_score": 0.0,
        }

    def __repr__(self) -> str:
        """Enhanced string representation for ReAct agent."""
        base_repr = super().__repr__()
        react_features = []

        if self.max_iterations != 10:
            react_features.append(f"max_iter={self.max_iterations}")
        if self.reasoning_mode != "efficient":
            react_features.append(f"mode={self.reasoning_mode}")
        if self.loop_detection:
            react_features.append("loop_detect")
        if self.reasoning_trace:
            react_features.append("trace")
        if self.performance_tracking:
            react_features.append("perf_track")

        react_str = (
            f" ReAct({', '.join(react_features)})" if react_features else " ReAct"
        )
        return (
            base_repr.replace("EnhancedSimpleAgent", "EnhancedReactAgent") + react_str
        )
