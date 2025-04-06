from typing import Any, Dict, List, Optional, Tuple, Type
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticToolsParser
from pydantic import BaseModel

from src.haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from src.haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from src.haive.agents.rec_plan.models import (
    ReasoningModule, PlanNode, ExecutionPlan, PlannerOutput, 
    ExecutorOutput, ReflectionOutput, FinalAnswer, ModuleSelectionOutput
)

# =============================================
# Module Selection Engine
# =============================================
# This is a partial fix for the module_selection engine in engines.py

def create_module_selection_engine(llm_config: Optional[LLMConfig] = None) -> AugLLMConfig:
    """Create an engine for selecting appropriate reasoning modules."""
    if llm_config is None:
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3})
    
    # Define the prompt with explicit instructions for the justifications field
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are tasked with selecting the most appropriate reasoning modules for a given task.

The task is: {task}

Available reasoning modules:
{reasoning_modules}

Select the most appropriate modules for this task based on their relevance to the task requirements.

IMPORTANT: Your output MUST include:
1. A list of selected modules in 'selected_modules' field
2. A dictionary of justifications in 'justifications' field with module names as keys

The output format must be:
```json
{{
  "selected_modules": ["Module Name 1", "Module Name 2"],
  "justifications": {{
    "Module Name 1": "Justification for this module",
    "Module Name 2": "Justification for this module"
  }}
}}
```

Both fields are required. Ensure your output includes both 'selected_modules' and 'justifications' fields.
"""),
        MessagesPlaceholder(variable_name="messages")
    ])
    
  
    return AugLLMConfig(
        name="module_selection_engine",
        llm_config=llm_config,
        prompt_template=prompt,
        structured_output_model=ModuleSelectionOutput
    )
# =============================================
# Planning Engine
# =============================================

PLANNING_SYSTEM_PROMPT = """
You are an expert recursive planner. Your task is to create a detailed, step-by-step plan to solve the given task using 
a DAG (Directed Acyclic Graph) structure that allows for parallel execution when possible.

Task: {task}

You will use the following reasoning modules to structure your approach:
{selected_modules}

Available tools:
{available_tools}

Your plan should:
1. Break the task into a clear sequence of steps in a DAG structure
2. Specify explicit dependencies between steps
3. Use the ReWOO style variable substitution (#E1, #E2, etc.) to pass information between steps
4. Identify opportunities for parallel execution
5. Include "join" points where parallel threads of execution must synchronize
6. Specify which tool to use for each step, with appropriate arguments

Task: {task}

For each step in your plan, provide:
1. A clear description
2. The reasoning module being applied
3. The tool to use (if any)
4. The arguments for the tool (using variable substitution where appropriate)
5. Dependencies on previous steps

Structure your plan using the given schema and ensure it forms a valid DAG.
"""

def create_planning_engine(llm_config: Optional[LLMConfig] = None) -> AugLLMConfig:
    """Create an engine for recursive planning."""
    if llm_config is None:
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.4})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", PLANNING_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    return AugLLMConfig(
        name="planning_engine",
        llm_config=llm_config,
        prompt_template=prompt,
        structured_output_model=PlannerOutput
    )

# =============================================
# Execution Engine
# =============================================

EXECUTION_SYSTEM_PROMPT = """
You are an expert reasoning agent that executes steps in a plan. Your task is to execute the current step 
by applying the specified reasoning module and using the appropriate tools.

Task: {task}

Current step to execute:
{current_step}

Context from the plan:
{plan_context}

Available variables from previous steps:
{variables}

To execute this step:
1. Apply the specified reasoning module to think through the problem
2. Use the specified tool with the correct arguments
3. Provide detailed reasoning about your approach
4. Process the results appropriately

Remember to substitute any variable references (like #E1) with their actual values from previous steps.
"""

def create_execution_engine(llm_config: Optional[LLMConfig] = None) -> AugLLMConfig:
    """Create an engine for executing plan steps."""
    if llm_config is None:
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXECUTION_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    return AugLLMConfig(
        name="execution_engine",
        llm_config=llm_config,
        prompt_template=prompt,
        structured_output_model=ExecutorOutput
    )

# =============================================
# Replanning Engine
# =============================================

REPLANNING_SYSTEM_PROMPT = """
You are an expert recursive planner specializing in plan refinement. Your task is to improve an existing execution plan
based on reflections and execution results.

Task: {task}

Original Plan:
{original_plan}

Execution Results:
{execution_results}

Reflections:
{reflections}

Based on these reflections, create an improved execution plan that:
1. Addresses the weaknesses identified in the reflections
2. Builds on the strengths of the original plan
3. Leverages the successful parts of the execution
4. Maintains the DAG structure with clear dependencies
5. Includes join points for parallel execution paths

Your improved plan should maintain the same overall structure but with refinements to make it more effective.
"""

def create_replanning_engine(llm_config: Optional[LLMConfig] = None) -> AugLLMConfig:
    """Create an engine specifically for refining plans based on reflection."""
    if llm_config is None:
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.4})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REPLANNING_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    return AugLLMConfig(
        name="replanning_engine",
        llm_config=llm_config,
        prompt_template=prompt,
        structured_output_model=PlannerOutput
    )

# =============================================
# Final Answer Engine
# =============================================

FINAL_ANSWER_SYSTEM_PROMPT = """
You are an expert synthesizer that creates comprehensive final answers from execution results.
Your task is to synthesize the results of the executed plan into a clear, concise final answer.

Task: {task}

Execution results:
{execution_results}

Synthesize the execution results into a comprehensive final answer that:
1. Directly addresses the original task
2. Incorporates relevant information from the execution
3. Is well-structured and easy to understand
4. Includes a confidence assessment
5. Provides the reasoning behind your answer
"""

def create_final_answer_engine(llm_config: Optional[LLMConfig] = None) -> AugLLMConfig:
    """Create an engine for generating final answers."""
    if llm_config is None:
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", FINAL_ANSWER_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    return AugLLMConfig(
        name="final_answer_engine",
        llm_config=llm_config,
        prompt_template=prompt,
        structured_output_model=FinalAnswer
    )

# =============================================
# ReAct Execution Engine
# =============================================

REACT_EXECUTION_SYSTEM_PROMPT = """
You are an expert reasoning agent that executes steps using a ReAct approach (Reasoning + Acting).
Your task is to execute the current step by:
1. Reasoning through the problem step by step
2. Applying the specified reasoning module
3. Taking appropriate actions using the specified tools
4. Reflecting on the results

Task: {task}

Current step to execute:
{current_step}

Context from the plan:
{plan_context}

Available variables from previous steps:
{variables}

Think through this step carefully, reason about different approaches, 
and use the specified tools to complete the step effectively.
"""

def create_react_execution_engine(llm_config: Optional[LLMConfig] = None, tools: List[Dict[str, Any]] = None) -> AugLLMConfig:
    """Create a ReAct engine for executing plan steps."""
    if llm_config is None:
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REACT_EXECUTION_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    return AugLLMConfig(
        name="react_execution_engine",
        llm_config=llm_config,
        prompt_template=prompt,
        structured_output_model=ExecutorOutput,
        tools=tools or []
    )
REFLECTION_PROMPT = """
You are analyzing the execution of a plan for a complex task.

The task is: {task}

Plan structure:
{plan_structure}

Execution results:
{execution_results}

Reflect on the plan and its execution, identifying:
1. Strengths of the plan
2. Weaknesses of the plan
3. Potential improvements for future plans

Based on your reflection, decide if a new plan should be created.

IMPORTANT: Your output MUST include ALL of the following fields:
- "reflection" - An object with "strengths", "weaknesses", and "improvements" arrays
- "should_replan" - A boolean indicating whether to create a new plan
- "reasoning" - Your detailed explanation of the reflection and recommendation

Return your reflection in this format:
```json
{{
  "reflection": {{
    "strengths": ["Strength 1", "Strength 2"],
    "weaknesses": ["Weakness 1", "Weakness 2"],
    "improvements": ["Improvement 1", "Improvement 2"]
  }},
  "should_replan": true,
  "reasoning": "Your detailed explanation of why replanning is needed or not..."
}}
```

ALL THREE FIELDS ("reflection", "should_replan", and "reasoning") are required in your response.
"""

def create_reflection_engine(llm_config: Optional[LLMConfig] = None) -> AugLLMConfig:
    """Create an engine for reflecting on plans and executions."""
    if llm_config is None:
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.5})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", REFLECTION_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    return AugLLMConfig(
        name="reflection_engine",
        llm_config=llm_config,
        prompt_template=prompt,
        structured_output_model=ReflectionOutput
    )

# =============================================
# Create Engine Registry
# =============================================

def create_engine_registry(llm_config: Optional[LLMConfig] = None) -> Dict[str, AugLLMConfig]:
    """Create a registry of all engines used by the recursive tree planner."""
    registry = {
        "module_selection": create_module_selection_engine(llm_config),
        "planning": create_planning_engine(llm_config),
        "execution": create_execution_engine(llm_config),
        "react_execution": create_react_execution_engine(llm_config),
        "reflection": create_reflection_engine(llm_config),
        "replanning": create_replanning_engine(llm_config),
        "final_answer": create_final_answer_engine(llm_config)
    }
    
    return registry