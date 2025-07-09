"""Multi-Agent System Components for the Haive Framework.

This module provides a comprehensive framework for building and orchestrating
multi-agent systems with intelligent state management, message preservation,
and flexible execution patterns.

The multi-agent system enables complex agent coordination patterns while
maintaining proper isolation between agents, preserving message integrity
(including tool_call_id fields), and providing automatic schema composition.

Key Components:
    - MultiAgent: Abstract base class for all multi-agent patterns
    - SequentialAgent: Execute agents one after another
    - ParallelAgent: Execute agents independently (future)
    - ConditionalAgent: Route based on conditions
    - ExecutionMode: Enum defining execution patterns

Example:
    >>> from haive.agents.multi import SequentialAgent
    >>> from haive.agents.react.agent import ReactAgent
    >>> from haive.agents.simple.agent import SimpleAgent
    >>>
    >>> # Create a multi-agent pipeline
    >>> system = SequentialAgent(
    ...     name="Analysis Pipeline",
    ...     agents=[
    ...         SimpleAgent(name="Researcher", engine=research_engine),
    ...         ReactAgent(name="Analyzer", engine=analysis_engine),
    ...         SimpleAgent(name="Reporter", engine=report_engine)
    ...     ]
    ... )
    >>>
    >>> # Run the system - messages flow between agents with tool_call_id preserved
    >>> result = system.run({"messages": [HumanMessage(content="Analyze trends")]})

Features:
    - Automatic schema composition with field separation strategies
    - Message preservation ensuring tool_call_id integrity
    - Engine isolation preventing tool contamination
    - Flexible routing with conditional branching
    - Meta state for agent coordination

Note:
    The multi-agent system uses AgentSchemaComposer with preserve_messages_reducer
    to ensure proper message handling across agent boundaries. This prevents the
    loss of critical fields like tool_call_id in ToolMessage objects.
"""

# Import base multi-agent implementation
from haive.agents.multi.base import (
    ConditionalAgent,
    ExecutionMode,
    MultiAgent,
    ParallelAgent,
    SequentialAgent,
)

# Future implementations
# from haive.agents.multi.haive import Haive, create_haive
# from haive.agents.multi.supervisor import SupervisorAgent

__all__ = [
    # Base classes
    "MultiAgent",
    "ExecutionMode",
    # Concrete implementations
    "SequentialAgent",
    "ParallelAgent",
    "ConditionalAgent",
    # Future
    # "SupervisorAgent",
    # "Haive",
    # "create_haive",
]
