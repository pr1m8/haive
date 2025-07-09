"""Configuration for the LLMCompiler agent using AugLLMConfig system."""

import uuid
from typing import Any

from agents.llm_compiler.models import JoinerOutput
from agents.llm_compiler.state import CompilerState
from haive.core.engine.agent.agent import AgentArchitectureConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.tools.dev_tools import python_repl_tool
from haive.core.tools.search_tools import tavily_search_tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field, model_validator

# Base planner prompt template
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an AI assistant that creates detailed step-by-step plans to solve complex user queries.

Your task is to create a plan that maximizes parallelizability - execute as many steps in parallel as possible.

Available tools:
{tool_descriptions}

Also available:
{num_tools}. join(): Finalize the answer and respond to the user.

Your plan must meet these requirements:
1. Each step must use exactly one tool from the list above
2. Each step must have a unique ID starting from 1
3. Steps can depend on outputs from previous steps using ${{step_id}} syntax
4. The final step must be join() to finalize the answer
5. Organize steps to maximize parallel execution - don't make steps depend on others unless necessary

For each step, include:
- A thought explaining your reasoning (optional)
- The step ID and tool to call with proper arguments
- Any dependencies on previous steps using ${{step_id}} in arguments

Example plan format:
```
1. search(query="current GDP of Japan")
Thought: Now I need to find population data
2. search(query="current population of Japan")
3. math(problem="divide ${{1}} by ${{2}}")
4. join()
<END_OF_PLAN>
```

Your plan should accomplish the user's goal efficiently in as few steps as possible.
""",
        ),
        ("user", "{query}"),
    ]
)

# Replanner prompt template that adds context from previous plan
replanner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an AI assistant that improves existing plans based on execution results.

Your task is to create a new plan that builds on the previous execution results to solve the user's query.

Available tools:
{tool_descriptions}

Also available:
{num_tools}. join(): Finalize the answer and respond to the user.

Review the previous plan and its execution results carefully. Then create a new plan that:
1. DOES NOT repeat steps that were already successfully executed
2. Addresses any errors or issues from the previous execution
3. Continues from where the previous plan left off
4. Continues step numbering from {next_idx} (do not repeat previous step numbers)
5. Maximizes parallel execution where possible
6. Ends with a join() step to finalize the answer

For each new step, include:
- A thought explaining your reasoning (optional)
- The step ID (starting from {next_idx}) and tool to call with proper arguments
- Any dependencies on previous steps using ${{step_id}} in arguments

Example plan format:
```
Thought: The previous plan found GDP and population data but failed to calculate the ratio correctly.

{next_idx}. math(problem="properly format GDP from ${{1}} to a number")
{next_idx_plus_one}. math(problem="properly format population from ${{2}} to a number") 
{next_idx_plus_two}. math(problem="divide ${{3}} by ${{4}}")
{next_idx_plus_three}. join()
<END_OF_PLAN>
```

Your plan should efficiently solve the remaining parts of the user's query.
""",
        ),
        ("user", "{query}"),
        ("system", "{feedback}"),
    ]
)

# Joiner prompt template
joiner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You analyze execution results and decide whether to provide a final answer or request additional steps.

Your task is to:
1. Review the user's original query
2. Examine the results of the executed steps
3. Decide if you have enough information to provide a complete answer

If you have enough information, provide a comprehensive final response that directly answers the user's query.

If you DON'T have enough information:
- Identify what information is missing
- Explain why the current results are insufficient
- Recommend specific additional steps needed to answer the query

When providing a final answer:
- Synthesize information from all relevant steps
- Present the answer in a clear, concise format
- Include specific data points that support your answer
- Address all parts of the user's original query

Be decisive - either provide a complete answer or explicitly request additional specific information.
""",
        ),
        (
            "user",
            """
Original Query: {query}

Executed Steps:
{executed_tasks}

Results:
{results}

Based on these results, can I provide a complete answer or do I need more information?
""",
        ),
    ]
)

# Default planner LLM configuration
default_planner_config = AugLLMConfig(
    name="llm_compiler_planner",
    llm_config=AzureLLMConfig(
        model="gpt-4o", parameters={"temperature": 0.7, "max_tokens": 4096}
    ),
    prompt_template=planner_prompt,
    tools=None,  # Tools are registered separately
)

# Default replanner LLM configuration
default_replanner_config = AugLLMConfig(
    name="llm_compiler_replanner",
    llm_config=AzureLLMConfig(
        model="gpt-4o", parameters={"temperature": 0.7, "max_tokens": 4096}
    ),
    prompt_template=replanner_prompt,
    tools=None,  # Tools are registered separately
)

# Default joiner LLM configuration
default_joiner_config = AugLLMConfig(
    name="llm_compiler_joiner",
    llm_config=AzureLLMConfig(
        model="gpt-4o", parameters={"temperature": 0.7, "max_tokens": 2048}
    ),
    prompt_template=joiner_prompt,
    structured_output_model=JoinerOutput,  # Will be set in agent
    structured_output_params={"method": "function_calling"},
)


class LLMCompilerAgentConfig(AgentArchitectureConfig):
    """Configuration for the LLM Compiler Agent using AugLLMConfig system.

    The LLM Compiler agent creates a directed acyclic graph (DAG) of tasks
    and executes them in parallel when dependencies are satisfied.
    """

    planner_config: AugLLMConfig = Field(
        default=default_planner_config, description="Configuration for the planner LLM"
    )
    replanner_config: AugLLMConfig = Field(
        default=default_replanner_config,
        description="Configuration for the replanner LLM",
    )
    joiner_config: AugLLMConfig = Field(
        default=default_joiner_config, description="Configuration for the joiner LLM"
    )
    # Directly store tool instances in the config
    tool_instances: list[BaseTool | StructuredTool] = Field(
        default=[tavily_search_tool, python_repl_tool],
        description="Tool instances available to the agent",
    )
    tool_configs: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Configuration for tool instantiation"
    )
    max_execution_time: float = Field(
        default=60.0, description="Maximum time to wait for task execution in seconds"
    )
    max_replanning_attempts: int = Field(
        default=3, description="Maximum number of replanning attempts"
    )
    should_visualize_graph: bool = Field(
        default=True, description="Whether to visualize the agent graph"
    )
    visualize_graph_output_name: str = Field(
        default="llm_compiler_graph.png", description="Path to save graph visualization"
    )
    state_schema: type[BaseModel] = Field(
        default=CompilerState, description="The state schema for the agent"
    )
    runnable_config: RunnableConfig = Field(
        default={"configurable": {"thread_id": str(uuid.uuid4())}},
        description="The runnable config for the agent",
    )

    @model_validator(mode="after")
    def validate_configs(cls, values):
        """Ensure that the configurations are valid."""
        # Ensure planner config has the correct prompt template
        if not values.planner_config.prompt_template:
            values.planner_config.prompt_template = planner_prompt

        # Ensure replanner config has the correct prompt template
        if not values.replanner_config.prompt_template:
            values.replanner_config.prompt_template = replanner_prompt

        # Ensure joiner config has the correct prompt template
        if not values.joiner_config.prompt_template:
            values.joiner_config.prompt_template = joiner_prompt

        return values


# Default configuration that can be used without parameters
DEFAULT_CONFIG = LLMCompilerAgentConfig()
