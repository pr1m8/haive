"""Configuration for the LLMCompiler agent using AugLLMConfig system."""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate

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
    structured_output_model=None,  # Will be set in agent
    structured_output_params={"method": "function_calling"},
)
