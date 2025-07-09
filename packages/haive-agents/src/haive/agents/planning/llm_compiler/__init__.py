"""LLM Compiler Agent Implementation

This module implements the LLM Compiler agent architecture from:
"LLM Compiler: An LLM Agent Architecture for Planning, Task Parallelization, and Execution"
by Kim et al.

The agent features:
1. Planner - Creates a DAG of tasks with dependencies
2. Task Fetching Unit - Executes tasks in parallel as their dependencies are met
3. Joiner - Processes results and decides whether to provide final answer or replan

Usage:
    from haive_agents.llm_compiler import LLMCompilerAgent, LLMCompilerAgentConfig

    # Create with default configuration
    agent = LLMCompilerAgent(LLMCompilerAgentConfig())

    # Run a query
    result = agent.run("What's the GDP of Japan divided by its population?")
    print(result)
"""

from agents.llm_compiler.agent import LLMCompilerAgent
from agents.llm_compiler.config import DEFAULT_CONFIG, LLMCompilerAgentConfig

__all__ = ["DEFAULT_CONFIG", "LLMCompilerAgent", "LLMCompilerAgentConfig"]
