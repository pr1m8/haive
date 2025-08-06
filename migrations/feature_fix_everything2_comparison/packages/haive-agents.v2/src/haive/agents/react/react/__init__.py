"""React - ReAct agent implementation with enhanced v3 capabilities.

ReAct (Reasoning and Acting) agents that can use tools, reason about actions,
and provide structured output with comprehensive debugging and observability.

Available Implementations:
    - ReactAgent: Original implementation extending SimpleAgent
    - ReactAgentV3: Enhanced implementation with structured output, hooks, and advanced features

Examples:
    Basic ReactAgent usage::

        from haive.agents.react import ReactAgent
        from haive.core.engine.aug_llm import AugLLMConfig

        agent = ReactAgent(name="react_agent", engine=AugLLMConfig())

    Enhanced ReactAgentV3 with structured output::

        from haive.agents.react import ReactAgentV3, create_react_agent
        from langchain_core.tools import tool
        from pydantic import BaseModel, Field

        @tool
        def calculator(expr: str) -> str:
            return str(eval(expr))

        class Analysis(BaseModel):
            reasoning: str = Field(description="Step-by-step reasoning")
            result: str = Field(description="Final answer")

        # Factory function approach
        agent = create_react_agent(
            name="enhanced_react",
            tools=[calculator],
            structured_output_model=Analysis,
            max_iterations=8,
            debug=True
        )

        # Direct instantiation approach
        agent = ReactAgentV3(
            name="direct_react",
            engine=AugLLMConfig(
                tools=[calculator],
                structured_output_model=Analysis
            ),
            max_iterations=6
        )

See Also:
    haive.agents.simple: SimpleAgent and SimpleAgentV3 implementations
    haive.core.engine.aug_llm: AugLLMConfig for engine configuration
"""

from haive.agents.react.agent import ReactAgent
from haive.agents.react.agent_v3 import (
    ReactAgentV3,
    create_react_agent,
    create_research_agent,
)

__all__ = ["ReactAgent", "ReactAgentV3", "create_react_agent", "create_research_agent"]
