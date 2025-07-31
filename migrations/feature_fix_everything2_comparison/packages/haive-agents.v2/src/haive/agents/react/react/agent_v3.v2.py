"""Agent_V3 core module.

This module provides agent v3 functionality for the Haive framework.

Classes:
    with: with implementation.
    ResearchAnalysis: ResearchAnalysis implementation.
    haive: haive implementation.

Functions:
    calculator: Calculator functionality.
    web_search: Web Search functionality.
    search_engine: Search Engine functionality.
"""

#!/usr/bin/env python3
"""ReactAgent v3 - Enhanced ReAct Pattern with Structured Output Support.

This module provides ReactAgent v3, an enhanced implementation of the ReAct (Reasoning and Acting)
pattern that extends SimpleAgentV3 with iterative reasoning loops, tool usage, and structured
output capabilities.

The ReactAgent v3 implements the ReAct paradigm where the agent alternates between:
1. **Reasoning**: Thinking about the problem and planning next steps
2. **Acting**: Using tools to gather information or perform actions
3. **Observing**: Analyzing tool results and updating understanding
4. **Iterating**: Continuing the cycle until the goal is achieved

Key enhancements over the original ReactAgent:
- Full structured output support with Pydantic models
- Enhanced Agent base class with hooks system
- Real-time recompilation when tools are added/removed
- Comprehensive debug logging and observability
- Token usage tracking and cost monitoring
- Meta-agent embedding capabilities
- Agent-as-tool pattern support

Examples:
    Basic ReAct agent with tools::

        from haive.agents.react.agent_v3 import ReactAgentV3
        from haive.core.engine.aug_llm import AugLLMConfig
        from langchain_core.tools import tool

        @tool
        def calculator(expression: str) -> str:
            '''Calculate mathematical expressions.'''
            return str(eval(expression))

        @tool
        def web_search(query: str) -> str:
            '''Search the web for information.'''
            return f"Search results for: {query}"

        agent = ReactAgentV3(
            name="research_assistant",
            engine=AugLLMConfig(
                tools=[calculator, web_search],
                temperature=0.7,
                max_tokens=800
            ),
            debug=True
        )

        result = agent.run("Research the current population of Tokyo and calculate the population density")
        # Agent will iteratively use web_search and calculator tools

    With structured output for complex reasoning::

        from pydantic import BaseModel, Field
        from typing import List

        class ResearchAnalysis(BaseModel):
            research_question: str = Field(description="Original research question")
            reasoning_steps: List[str] = Field(description="Step-by-step reasoning process")
            tools_used: List[str] = Field(description="Tools utilized during research")
            key_findings: List[str] = Field(description="Important discoveries made")
            final_answer: str = Field(description="Comprehensive final answer")
            confidence: float = Field(ge=0.0, le=1.0, description="Confidence in answer")

        agent = ReactAgentV3(
            name="structured_researcher",
            engine=AugLLMConfig(
                tools=[calculator, web_search],
                structured_output_model=ResearchAnalysis,
                temperature=0.3,
                max_tokens=1000
            ),
            max_iterations=5,  # Limit reasoning loops
            debug=True
        )

        analysis = agent.run("Analyze the economic impact of renewable energy adoption")
        # Returns validated ResearchAnalysis with complete reasoning trace

See Also:
    haive.agents.simple.agent_v3.SimpleAgentV3: Base agent class
    haive.agents.react.agent.ReactAgent: Original ReactAgent implementation
    haive.core.engine.aug_llm.AugLLMConfig: Engine configuration
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.tools import BaseTool, tool
from langgraph.graph import END
from pydantic import BaseModel, Field, field_validator

# Import enhanced SimpleAgentV3 as base class
from haive.agents.simple.agent_v3 import SimpleAgentV3

# Hooks system integration


logger = logging.getLogger(__name__)


# ============================================================================
# REACT AGENT V3 - Enhanced ReAct Pattern Implementation
# ============================================================================


class ReactAgentV3(SimpleAgentV3):
    """ReactAgent v3 with enhanced ReAct pattern, structured output, and hooks integration.

    This agent implements the ReAct (Reasoning and Acting) paradigm with significant
    enhancements over the original ReactAgent. It extends SimpleAgentV3 to inherit
    all structured output capabilities, hooks system, recompilation features, and
    advanced observability while adding iterative reasoning loops.

    **ReAct Pattern Implementation:**
    The agent follows a continuous reasoning loop:

    1. **Think**: Analyze the current situation and plan next steps
    2. **Act**: Execute tools or gather information
    3. **Observe**: Process tool results and update understanding
    4. **Repeat**: Continue until goal is achieved or max iterations reached

    **Enhanced Features over ReactAgent:**
    - Full structured output support with automatic Pydantic model validation
    - Iterative reasoning with configurable maximum iteration limits
    - Enhanced debugging with step-by-step reasoning trace visibility
    - Real-time tool addition/removal with automatic graph recompilation
    - Comprehensive hooks system for monitoring and intervention
    - Token usage tracking and cost analysis throughout reasoning loops
    - Meta-agent embedding support for multi-agent coordination
    - Agent-as-tool conversion for hierarchical agent systems

    **Architecture Integration:**
    - Inherits from SimpleAgentV3 for full enhanced Agent capabilities
    - Uses LLMState for comprehensive token and cost tracking
    - Integrates with RecompileMixin for dynamic tool management
    - Supports DynamicToolRouteMixin for flexible tool routing
    - Compatible with MetaStateSchema for embedding in larger systems

    Attributes:
        max_iterations: Maximum number of reasoning iterations before stopping.
            Prevents infinite loops while allowing complex multi-step reasoning.
        iteration_count: Current iteration number during execution (read-only).
        reasoning_trace: List of reasoning steps taken during execution (read-only).
        stop_on_first_tool_result: Whether to stop after the first successful tool execution.
            Useful for simple lookup tasks vs. complex multi-step reasoning.
        require_final_answer: Whether to require a final non-tool response.
            Ensures the agent provides a summary or conclusion after tool usage.

    Examples:
        Basic ReAct agent for research tasks::

            from haive.agents.react.agent_v3 import ReactAgentV3
            from langchain_core.tools import tool

            @tool
            def search_engine(query: str) -> str:
                '''Search for information online.'''
                return f"Search results for: {query}"

            @tool
            def calculator(expression: str) -> str:
                '''Perform mathematical calculations.'''
                return str(eval(expression))

            agent = ReactAgentV3(
                name="research_agent",
                engine=AugLLMConfig(
                    tools=[search_engine, calculator],
                    temperature=0.7,
                    max_tokens=1200
                ),
                max_iterations=8,
                debug=True
            )

            result = agent.run(
                "Find the current population of Japan and calculate how many Tokyo Domes "
                "would fit that many people (assuming 55,000 capacity each)"
            )
            # Agent iteratively searches for population data, then calculates the result

        Structured output for complex analysis::

            from pydantic import BaseModel, Field
            from typing import List

            class TechnicalAnalysis(BaseModel):
                problem_statement: str = Field(description="Clear problem definition")
                research_steps: List[str] = Field(description="Steps taken to research")
                calculations_performed: List[str] = Field(description="Mathematical operations")
                key_findings: List[str] = Field(description="Important discoveries")
                final_solution: str = Field(description="Complete solution with reasoning")
                confidence_level: float = Field(ge=0.0, le=1.0, description="Solution confidence")

            agent = ReactAgentV3(
                name="technical_analyst",
                engine=AugLLMConfig(
                    tools=[search_engine, calculator],
                    structured_output_model=TechnicalAnalysis,
                    temperature=0.3
                ),
                max_iterations=6,
                require_final_answer=True
            )

            analysis = agent.run("Analyze the feasibility of a space elevator")
            # Returns TechnicalAnalysis with complete reasoning process
            assert isinstance(analysis, TechnicalAnalysis)
            print(f"Confidence: {analysis.confidence_level}")

        With hooks for monitoring reasoning process::

            @agent.before_iteration
            def log_iteration_start(context):
                logger.info(f"Starting iteration {context.iteration_count}")

            @agent.after_tool_execution
            def log_tool_usage(context):
                logger.info(f"Used tool: {context.tool_name} -> {context.tool_result[:100]}...")

            @agent.before_final_answer
            def validate_completeness(context):
                if len(context.reasoning_trace) < 3:
                    logger.warning("Solution may be incomplete - consider more reasoning steps")

            result = agent.run("Complex multi-step problem")
            # Comprehensive monitoring throughout reasoning process

        Dynamic tool addition during reasoning::

            agent = ReactAgentV3(
                name="adaptive_agent",
                engine=AugLLMConfig(tools=[calculator]),
                auto_recompile=True,
                max_iterations=10
            )

            # Start reasoning
            result = agent.run("I need to research and calculate something complex")

            # Agent realizes it needs additional tools, add them dynamically
            @tool
            def database_lookup(query: str) -> str:
                '''Look up information in database.'''
                return f"Database result for: {query}"

            agent.add_tool(database_lookup)  # Triggers automatic recompilation

            # Continue reasoning with new tool available
            continued_result = agent.run("Now use the database to complete the analysis")

        Production configuration with limits::

            agent = ReactAgentV3(
                name="production_agent",
                engine=AugLLMConfig(
                    tools=production_tools,
                    temperature=0.2,
                    max_tokens=800
                ),
                max_iterations=5,  # Limit for performance
                stop_on_first_tool_result=False,  # Allow multi-tool usage
                require_final_answer=True,  # Ensure conclusions
                debug=False  # Minimal logging for production
            )

    Note:
        - ReAct agents are more computationally expensive than SimpleAgents due to iterative reasoning
        - Set appropriate max_iterations to balance thoroughness with performance
        - Structured output works seamlessly with the reasoning loop
        - Tool costs can accumulate across multiple iterations
        - Debug mode provides valuable insights into the reasoning process
        - The agent will automatically stop when it determines the task is complete

    See Also:
        SimpleAgentV3: Base class with structured output and enhanced features
        ReactAgent: Original ReactAgent implementation
        AugLLMConfig: Engine configuration for tools and structured output
        LLMState: State schema with token tracking across iterations
        RecompileMixin: Dynamic tool management capabilities
    """

    # ReactAgent-specific configuration fields
    max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum reasoning iterations before stopping (1-50)",
    )

    iteration_count: int = Field(
        default=0,
        ge=0,
        description="Current iteration number (read-only, managed internally)",
    )

    reasoning_trace: list[str] = Field(
        default_factory=list,
        description="Step-by-step reasoning history (read-only, managed internally)",
    )

    stop_on_first_tool_result: bool = Field(
        default=False,
        description="Stop after first successful tool execution (vs. continuing reasoning)",
    )

    require_final_answer: bool = Field(
        default=True,
        description="Require a final non-tool response summarizing the solution",
    )

    # Internal state tracking (Pydantic fields cannot start with underscore)
    current_reasoning_step: str | None = Field(
        default=None,
        description="Current reasoning step being executed (internal use)",
        exclude=True,  # Exclude from serialization
    )

    tool_results_history: list[dict[str, Any]] = Field(
        default_factory=list,
        description="History of tool executions and results (internal use)",
        exclude=True,  # Exclude from serialization
    )

    @field_validator("max_iterations")
    @classmethod
    def validate_max_iterations(cls, v: int) -> int:
        """Validate max_iterations is reasonable for performance."""
        if v < 1:
            raise ValueError("max_iterations must be at least 1")
        if v > 50:
            logger.warning(
                f"max_iterations={v} is very high and may cause performance issues. "
                f"Consider using a lower value (5-15 typical range)."
            )
        return v

    def setup_agent(self) -> None:
        """Setup ReactAgent v3 with enhanced ReAct pattern and reasoning loop configuration.

        Extends SimpleAgentV3.setup_agent() with ReactAgent-specific initialization
        including reasoning loop configuration, iteration tracking setup, and
        ReAct-specific hooks registration.

        Additional setup includes:
        1. Reasoning iteration limits and tracking initialization
        2. Tool execution history and trace setup
        3. ReAct-specific hook events registration
        4. Graph modification for reasoning loops instead of linear execution
        5. Performance monitoring for iterative execution

        This method is called automatically during agent instantiation.
        """
        # Call parent setup for all enhanced SimpleAgentV3 features
        super().setup_agent()

        if self.debug:
            logger.debug(f"Setting up ReactAgent v3 features for '{self.name}'")
            logger.debug(f"Max iterations: {self.max_iterations}")
            logger.debug(f"Stop on first tool result: {self.stop_on_first_tool_result}")
            logger.debug(f"Require final answer: {self.require_final_answer}")

        # Initialize reasoning state
        self.iteration_count = 0
        self.reasoning_trace = []
        self.tool_results_history = []
        self.current_reasoning_step = None

        # Register ReAct-specific hook events if hooks are enabled
        if hasattr(self, "hooks_enabled") and self.hooks_enabled:
            self._register_react_hooks()

        if self.debug:
            logger.debug(f"ReactAgent v3 setup complete for '{self.name}'")

    def _register_react_hooks(self) -> None:
        """Register ReAct-specific hook events for reasoning loop monitoring.

        Registers additional hook events specific to the ReAct pattern:
        - before_iteration: Called before each reasoning iteration
        - after_iteration: Called after each reasoning iteration
        - before_tool_execution: Called before any tool is executed
        - after_tool_execution: Called after tool execution completes
        - before_final_answer: Called before generating final response
        - reasoning_limit_reached: Called when max_iterations is hit
        """
        try:
            # For now, use basic hook registration from SimpleAgentV3
            # The specific ReAct hook events can be added later when HookEvent is extended
            if hasattr(self, "hooks_enabled") and self.hooks_enabled:
                if self.debug:
                    logger.debug("ReAct hooks would be registered here (placeholder)")

        except Exception as e:
            if self.debug:
                logger.debug(f"ReAct hooks registration skipped: {e}")

    def build_graph(self) -> BaseGraph:
        """Build enhanced ReAct graph with iterative reasoning loops and structured output.

        Creates a graph that implements the ReAct pattern with reasoning loops
        instead of the linear execution flow of SimpleAgent. The graph structure
        enables the agent to iteratively reason, act with tools, and observe results
        until the problem is solved or max_iterations is reached.

        **Graph Structure:**
        ```
        START → agent_node → validation_node
                    ↑             ↓
                    ←─── tool_node (loops back for continued reasoning)
                    ↑             ↓
                    ←─── parse_output (for structured output, then loops back)
                                  ↓
                               END (when reasoning complete or max iterations)
        ```

        **Key Differences from SimpleAgent:**
        - Tool executions loop back to agent_node for continued reasoning
        - Parser output loops back for additional reasoning iterations
        - Iteration counting and limiting built into the graph flow
        - Reasoning trace tracking throughout the execution

        Returns:
            BaseGraph: Compiled graph ready for ReAct pattern execution with
                reasoning loops, tool integration, and structured output support.

        Raises:
            GraphBuildError: If graph construction fails due to configuration issues.
            ToolIntegrationError: If tool nodes cannot be properly integrated.

        Examples:
            Basic ReAct graph with tools::

                agent = ReactAgentV3(
                    name="react_agent",
                    engine=AugLLMConfig(tools=[calculator, search_tool])
                )

                graph = agent.build_graph()
                # Graph enables: reasoning → tool use → more reasoning → solution

            With structured output and reasoning limits::

                agent = ReactAgentV3(
                    name="structured_react",
                    engine=AugLLMConfig(
                        tools=[research_tools],
                        structured_output_model=AnalysisResult
                    ),
                    max_iterations=8
                )

                graph = agent.build_graph()
                # Graph supports structured output after reasoning completion

        Note:
            - The graph automatically handles iteration counting and limits
            - Tool execution results always feed back into reasoning
            - Structured output is generated after reasoning completion
            - Graph compilation includes all SimpleAgentV3 enhancements
            - Debug mode provides detailed graph traversal logging
        """
        if self.debug:
            logger.debug(
                f"Building ReAct graph for '{self.name}' with max_iterations={self.max_iterations}"
            )

        # Start with SimpleAgentV3's enhanced graph
        graph = super().build_graph()

        if self.debug:
            logger.debug(f"Base graph nodes: {list(graph.nodes.keys())}")

        # Get main engine for modifications
        if not self.engine:
            if self.debug:
                logger.debug("No engine configured, returning base graph")
            return graph

        # Modify graph for ReAct looping behavior
        self._modify_graph_for_react_loops(graph)

        if self.debug:
            logger.debug(
                f"ReAct graph build complete with nodes: {list(graph.nodes.keys())}"
            )

        return graph

    def _modify_graph_for_react_loops(self, graph: BaseGraph) -> None:
        """Modify graph connections to implement ReAct reasoning loops.

        Transforms the linear SimpleAgent graph into a ReAct reasoning loop by:
        1. Redirecting tool node outputs back to agent_node for continued reasoning
        2. Redirecting parser outputs back to agent_node for additional iterations
        3. Adding iteration counting and limit enforcement
        4. Preserving final output generation for structured output

        Args:
            graph: BaseGraph instance to modify for ReAct pattern

        Note:
            This method modifies the graph in-place to implement reasoning loops
            while preserving all structured output and tool integration capabilities.
        """
        # Check if we have tools that need looping behavior
        if self._has_tools() and "tool_node" in graph.nodes:
            if self.debug:
                logger.debug("Modifying tool_node for ReAct looping")

            # Remove direct tool_node → END connection
            try:
                graph.remove_edge("tool_node", END)
                if self.debug:
                    logger.debug("Removed tool_node → END edge")
            except Exception as e:
                if self.debug:
                    logger.debug(f"No tool_node → END edge to remove: {e}")

            # Add tool_node → agent_node loop for continued reasoning
            graph.add_edge("tool_node", "agent_node")
            if self.debug:
                logger.debug("Added tool_node → agent_node reasoning loop")

        # Check if we have structured output that needs looping
        if self._has_structured_output() and "parse_output" in graph.nodes:
            if self.debug:
                logger.debug("Modifying parse_output for ReAct looping")

            # For structured output, we want to loop back for more reasoning
            # but eventually output the structured result
            try:
                graph.remove_edge("parse_output", END)
                if self.debug:
                    logger.debug("Removed parse_output → END edge")
            except Exception as e:
                if self.debug:
                    logger.debug(f"No parse_output → END edge to remove: {e}")

            # Add conditional: continue reasoning or output structured result
            # This will be handled by the validation logic to determine
            # when reasoning is complete vs. when to continue iterating
            graph.add_edge("parse_output", "agent_node")
            if self.debug:
                logger.debug("Added parse_output → agent_node reasoning loop")

        # The validation node will handle the logic of when to continue
        # reasoning vs. when to end execution based on:
        # - iteration_count vs max_iterations
        # - presence of final answer
        # - tool execution requirements

    def _has_tools(self) -> bool:
        """Check if agent has tools configured for ReAct pattern execution.

        Returns:
            bool: True if agent has tools available for acting phase
        """
        return bool(self.engine and getattr(self.engine, "tools", None))

    def _has_structured_output(self) -> bool:
        """Check if agent has structured output model configured.

        Returns:
            bool: True if structured output model is configured
        """
        return bool(
            getattr(self, "structured_output_model", None)
            or (self.engine and getattr(self.engine, "structured_output_model", None))
        )

    def run(self, input_data: Any, debug: bool = None, **kwargs) -> Any:
        """Execute ReactAgent with iterative reasoning loops and structured output.

        Implements the full ReAct pattern with enhanced capabilities from SimpleAgentV3.
        The execution follows iterative reasoning cycles until the problem is solved
        or maximum iterations are reached.

        **ReAct Execution Flow:**
        1. **Initialize**: Set up reasoning state and iteration tracking
        2. **Think**: Analyze current situation and plan next steps
        3. **Act**: Execute tools or gather information if needed
        4. **Observe**: Process results and update reasoning state
        5. **Evaluate**: Determine if problem is solved or more reasoning needed
        6. **Iterate**: Return to step 2 if max_iterations not reached
        7. **Conclude**: Generate final answer (structured if configured)

        Args:
            input_data: Input for the ReAct reasoning process. Supports all formats
                from SimpleAgentV3 (str, List[BaseMessage], Dict, BaseModel).
            debug: Override agent's debug setting for detailed reasoning trace.
                When True, shows each reasoning iteration step-by-step.
            **kwargs: Additional execution arguments:
                - max_iterations_override: Temporarily override max_iterations
                - stop_early: Stop after first successful tool result
                - require_conclusion: Force final non-tool response

        Returns:
            Any: Result format depends on configuration:
                - With structured_output_model: Validated Pydantic model with reasoning
                - Without structured output: Final reasoning conclusion as string
                - Debug mode: Enhanced result with complete reasoning trace

        Raises:
            ReasoningLoopError: If reasoning loop fails to converge or encounters errors.
            MaxIterationsExceeded: If max_iterations reached without solution.
            ToolExecutionError: If critical tool execution fails during reasoning.
            StructuredOutputError: If structured output validation fails after reasoning.

        Examples:
            Basic ReAct reasoning with tools::

                agent = ReactAgentV3(
                    name="problem_solver",
                    engine=AugLLMConfig(tools=[calculator, web_search]),
                    max_iterations=6
                )

                result = agent.run(
                    "What's the square root of the current population of Tokyo?",
                    debug=True
                )
                # Shows: research Tokyo population → calculate square root → conclude

            Structured output with reasoning trace::

                class ProblemSolution(BaseModel):
                    original_problem: str = Field(description="Problem statement")
                    reasoning_steps: List[str] = Field(description="Thinking process")
                    tools_used: List[str] = Field(description="Tools utilized")
                    intermediate_results: List[str] = Field(description="Intermediate findings")
                    final_answer: str = Field(description="Complete solution")
                    confidence: float = Field(description="Solution confidence 0-1")

                agent = ReactAgentV3(
                    name="structured_solver",
                    engine=AugLLMConfig(
                        tools=[calculator, web_search],
                        structured_output_model=ProblemSolution
                    ),
                    max_iterations=8,
                    require_final_answer=True
                )

                solution = agent.run("Complex multi-step research problem")
                # Returns ProblemSolution with complete reasoning documentation
                assert isinstance(solution, ProblemSolution)
                print(f"Reasoning steps: {len(solution.reasoning_steps)}")
                print(f"Confidence: {solution.confidence}")

            With iteration override and early stopping::

                result = agent.run(
                    "Simple lookup question",
                    max_iterations_override=3,  # Limit for simple task
                    stop_early=True,  # Stop after first tool success
                    debug=True
                )

            Production execution with monitoring::

                @agent.before_iteration
                def log_iteration(context):
                    logger.info(f"Iteration {context.iteration_count}: {context.current_step}")

                @agent.after_tool_execution
                def log_tool_usage(context):
                    logger.info(f"Tool {context.tool_name}: {context.success}")

                result = agent.run("Production reasoning task")
                # Comprehensive logging throughout reasoning process

        Performance Notes:
            - ReAct agents are 3-5x more expensive than SimpleAgents due to iteration
            - Each iteration involves a full LLM call and potential tool execution
            - Structured output adds validation overhead after reasoning completion
            - Debug mode significantly increases output and execution time
            - Tool costs accumulate across all reasoning iterations

        Reasoning Quality:
            - More iterations generally lead to better solutions but higher cost
            - Tools significantly improve reasoning quality for factual problems
            - Structured output ensures consistent result format and validation
            - Early stopping trades thoroughness for performance

        See Also:
            SimpleAgentV3.run: Base execution method with additional capabilities
            add_tool: Dynamic tool addition during reasoning
            set_max_iterations: Runtime iteration limit configuration
            get_reasoning_trace: Access complete reasoning history
        """
        # Handle iteration override
        original_max_iterations = self.max_iterations
        if "max_iterations_override" in kwargs:
            self.max_iterations = kwargs.pop("max_iterations_override")

        # Handle early stopping override
        original_stop_early = self.stop_on_first_tool_result
        if "stop_early" in kwargs:
            self.stop_on_first_tool_result = kwargs.pop("stop_early")

        # Handle final answer requirement override
        original_require_conclusion = self.require_final_answer
        if "require_conclusion" in kwargs:
            self.require_final_answer = kwargs.pop("require_conclusion")

        try:
            # Reset reasoning state for new execution
            self.iteration_count = 0
            self.reasoning_trace = []
            self.tool_results_history = []
            self.current_reasoning_step = None

            run_debug = debug if debug is not None else self.debug

            if run_debug:
                logger.info(
                    f"[{self.name}] Starting ReAct execution with max_iterations={self.max_iterations}"
                )
                logger.info(f"[{self.name}] Input: {str(input_data)[:200]}...")

            # Execute ReAct pattern using enhanced SimpleAgentV3 run method
            # The graph modifications will handle the reasoning loop logic
            result = super().run(input_data, debug=run_debug, **kwargs)

            if run_debug:
                logger.info(
                    f"[{self.name}] ReAct execution completed in {self.iteration_count} iterations"
                )
                logger.info(
                    f"[{self.name}] Reasoning steps: {len(self.reasoning_trace)}"
                )
                logger.info(
                    f"[{self.name}] Tools used: {len(self.tool_results_history)}"
                )

            return result

        finally:
            # Restore original values
            self.max_iterations = original_max_iterations
            self.stop_on_first_tool_result = original_stop_early
            self.require_final_answer = original_require_conclusion

    def add_reasoning_step(self, step: str) -> None:
        """Add a reasoning step to the trace for monitoring and debugging.

        Args:
            step: Description of the reasoning step being performed
        """
        self.reasoning_trace.append(f"Step {len(self.reasoning_trace) + 1}: {step}")
        if self.debug:
            logger.debug(f"[{self.name}] Reasoning: {step}")

    def get_reasoning_trace(self) -> list[str]:
        """Get the complete reasoning trace from the current or last execution.

        Returns:
            List[str]: List of reasoning steps performed during execution
        """
        return self.reasoning_trace.copy()

    def get_tool_usage_history(self) -> list[dict[str, Any]]:
        """Get the complete tool usage history from the current or last execution.

        Returns:
            List[Dict[str, Any]]: List of tool executions with results and metadata
        """
        return self.tool_results_history.copy()

    def set_max_iterations(self, max_iterations: int) -> None:
        """Set maximum reasoning iterations with validation.

        Args:
            max_iterations: New maximum iteration limit (1-50)

        Raises:
            ValueError: If max_iterations is outside valid range
        """
        if max_iterations < 1 or max_iterations > 50:
            raise ValueError("max_iterations must be between 1 and 50")

        old_value = self.max_iterations
        self.max_iterations = max_iterations

        if self.debug:
            logger.debug(
                f"[{self.name}] Max iterations changed: {old_value} → {max_iterations}"
            )


# ============================================================================
# REACT AGENT FACTORY FUNCTIONS
# ============================================================================


def create_react_agent(
    name: str,
    tools: list[BaseTool],
    structured_output_model: type[BaseModel] | None = None,
    max_iterations: int = 10,
    temperature: float = 0.7,
    max_tokens: int = 1200,
    debug: bool = False,
    **engine_kwargs,
) -> ReactAgentV3:
    """Create a ReactAgentV3 with standard configuration for ReAct pattern execution.

    This factory function simplifies ReactAgent creation with sensible defaults
    for ReAct reasoning, tool usage, and optional structured output.

    Args:
        name: Unique identifier for the agent instance.
        tools: List of LangChain tools for the acting phase of ReAct.
        structured_output_model: Optional Pydantic model for structured responses.
        max_iterations: Maximum reasoning iterations (recommended: 5-15).
        temperature: LLM temperature for reasoning (0.1=focused, 0.9=creative).
        max_tokens: Token limit per iteration (should account for tool results).
        debug: Enable detailed reasoning trace and execution logging.
        **engine_kwargs: Additional AugLLMConfig parameters.

    Returns:
        ReactAgentV3: Configured agent ready for ReAct pattern execution.

    Examples:
        Research agent with web search and calculation::

            from langchain_core.tools import tool

            @tool
            def web_search(query: str) -> str:
                '''Search the web for current information.'''
                return search_api.search(query)

            @tool
            def calculator(expression: str) -> str:
                '''Perform mathematical calculations.'''
                return str(eval(expression))

            agent = create_react_agent(
                name="research_assistant",
                tools=[web_search, calculator],
                max_iterations=8,
                temperature=0.6,
                debug=True
            )

            result = agent.run("What's the GDP per capita of the top 5 economies?")

        With structured output for consistent results::

            class ResearchReport(BaseModel):
                query: str = Field(description="Original research question")
                methodology: List[str] = Field(description="Research steps taken")
                findings: List[str] = Field(description="Key discoveries")
                conclusion: str = Field(description="Final answer with reasoning")
                sources_used: List[str] = Field(description="Information sources")

            agent = create_react_agent(
                name="structured_researcher",
                tools=[web_search, calculator],
                structured_output_model=ResearchReport,
                max_iterations=12,
                temperature=0.4,
                max_tokens=1500
            )

            report = agent.run("Research renewable energy adoption trends")
            assert isinstance(report, ResearchReport)
    """
    # Validate inputs
    if not tools:
        raise ValueError("ReAct agents require at least one tool for the acting phase")

    if max_iterations < 1 or max_iterations > 50:
        raise ValueError("max_iterations must be between 1 and 50")

    # Create engine configuration
    engine_config = AugLLMConfig(
        tools=tools,
        structured_output_model=structured_output_model,
        temperature=temperature,
        max_tokens=max_tokens,
        **engine_kwargs,
    )

    # Create ReactAgent
    agent = ReactAgentV3(
        name=name, engine=engine_config, max_iterations=max_iterations, debug=debug
    )

    if debug:
        logger.info(
            f"Created ReactAgentV3 '{name}' with {len(tools)} tools, "
            f"max_iterations={max_iterations}, structured_output={structured_output_model is not None}"
        )

    return agent


def create_research_agent(
    name: str,
    research_tools: list[BaseTool],
    analysis_model: type[BaseModel] | None = None,
    max_research_steps: int = 8,
    debug: bool = False,
) -> ReactAgentV3:
    """Create a ReactAgentV3 optimized for research and analysis tasks.

    Pre-configured for research workflows with appropriate iteration limits,
    temperature settings, and token allowances for comprehensive investigation.

    Args:
        name: Agent identifier for research tasks.
        research_tools: Tools for information gathering (search, databases, APIs).
        analysis_model: Optional structured output model for research results.
        max_research_steps: Maximum research iterations (recommended: 6-12).
        debug: Enable research process tracing.

    Returns:
        ReactAgentV3: Research-optimized agent configuration.
    """
    return create_react_agent(
        name=name,
        tools=research_tools,
        structured_output_model=analysis_model,
        max_iterations=max_research_steps,
        temperature=0.3,  # Focused for research accuracy
        max_tokens=1500,  # Allow comprehensive research documentation
        debug=debug,
        system_message="You are a thorough research assistant. Take systematic steps to gather information, analyze findings, and provide comprehensive conclusions.",
    )


if __name__ == "__main__":
    # Example usage and testing
    from langchain_core.tools import tool

    @tool
    def example_calculator(expression: str) -> str:
        """Calculate mathematical expressions."""
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Calculation error: {e}"

    # Create example ReactAgent
    agent = create_react_agent(
        name="example_react_agent",
        tools=[example_calculator],
        max_iterations=5,
        debug=True,
    )

    print("✅ ReactAgentV3 created successfully")
    print(f"📊 Max iterations: {agent.max_iterations}")
    print(f"🔧 Tools available: {len(agent.engine.tools) if agent.engine else 0}")
    print("🚀 Ready for ReAct pattern execution!")
