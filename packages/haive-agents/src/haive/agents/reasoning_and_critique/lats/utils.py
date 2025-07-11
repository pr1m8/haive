from typing import Any

from agents.lats.models import Reflection
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate


def create_reflection_chain():
    """Create a chain for generating reflections on responses."""
    # Template for reflection
    reflection_template = """You are an objective evaluator. Your task is to evaluate a candidate response based on how well it addresses a given query.

    Query:
    {input}

    Candidate Solution:
    {candidate}

    Please evaluate and rate the candidate solution's effectiveness at addressing the query. Consider:
    1. Clarity and comprehensiveness of the response
    2. Factual accuracy and relevance
    3. Intelligent reasoning
    4. Whether it fully addresses all aspects of the query

    Provide:
    1. Reflections: A paragraph with your thoughts on the response's strengths and weaknesses
    2. A score from 0-10 (where 10 is perfect)
    3. Whether the solution fully addresses the question (true/false)

    Output must be in JSON format:
    ```json
    {{
      "reflections": "your reflections here",
      "score": 0-10,
      "found_solution": true/false
    }}
    ```
    """

    # Create the chat prompt
    reflection_prompt = ChatPromptTemplate.from_template(reflection_template)

    # Create the reflection model (use a specific model for good evaluations)

    # Create parser for Reflection
    parser = PydanticOutputParser(pydantic_object=Reflection)
    model = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0}).instantiate()
    # Build and return the reflection chain
    return reflection_prompt | model | parser


def format_messages_for_chain(messages: list[Any]) -> str:
    """Format a list of messages as a string for input to a chain."""
    formatted_msgs = []

    for msg in messages:
        if hasattr(msg, "content") and msg.content:
            msg_type = getattr(msg, "type", "message").upper()
            formatted_msgs.append(f"{msg_type}: {msg.content}")
        elif isinstance(msg, dict) and "content" in msg:
            msg_type = msg.get("type", "MESSAGE").upper()
            formatted_msgs.append(f"{msg_type}: {msg['content']}")
        else:
            # Try to handle unexpected types gracefully
            formatted_msgs.append(str(msg))

    return "\n\n".join(formatted_msgs)


"""
Factory functions for creating LATS agents.
"""
from agents.lats.config import LATSAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.tools.search_tools import tavily_search_tool
from langchain_core.tools import BaseTool


def create_lats_agent(
    system_prompt: str = "You are a helpful assistant that can answer questions and help with tasks.",
    tools: list[BaseTool] | None = None,
    max_depth: int = 3,
    max_iterations: int = 3,
    n_candidates: int = 3,
    exploration_weight: float = 1.0,
    name: str = "lats_agent",
    model: str = "gpt-4o",
) -> "LATSAgent":
    """Create a LATS agent with the specified configuration.

    Args:
        system_prompt: System prompt for the agent
        tools: Optional list of tools for the agent to use
        max_depth: Maximum depth of the search tree
        max_iterations: Maximum number of iterations for the search
        n_candidates: Number of candidates to generate at each expansion
        exploration_weight: Weight for exploration in UCB calculation
        name: Name for the agent
        model: Model name to use

    Returns:
        A configured LATS agent
    """
    # Create LLM config
    if tools is None:
        tools = [tavily_search_tool]
    if tools is None:
        tools = [tavily_search_tool]
    if tools is None:
        tools = [tavily_search_tool]
    if tools is None:
        tools = [tavily_search_tool]
    if tools is None:
        tools = [tavily_search_tool]
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": 0.7})

    # Create reflection engine
    reflection_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an objective evaluator tasked with analyzing responses.",
            ),
            (
                "user",
                "Analyze how well the following response addresses the query:\n\nQuery: {input}\n\nResponse: {candidate}",
            ),
        ]
    )

    reflection_engine = AugLLMConfig(
        name="reflection_engine",
        llm_config=llm_config.model_copy(update={"parameters": {"temperature": 0.1}}),
        prompt_template=reflection_prompt,
    )

    # Create action engine
    action_prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", "{input}")]
    )

    action_engine = AugLLMConfig(
        name="action_engine",
        llm_config=llm_config,
        prompt_template=action_prompt,
        tools=tools or [],
    )

    # Create main engine (same as action for simplicity)
    main_engine = AugLLMConfig(
        name="main_engine", llm_config=llm_config, prompt_template=action_prompt
    )

    # Create agent config
    config = LATSAgentConfig(
        name=name,
        engine=main_engine,
        reflection_engine=reflection_engine,
        action_engine=action_engine,
        tools=tools or [],
        max_depth=max_depth,
        max_iterations=max_iterations,
        n_candidates=n_candidates,
        exploration_weight=exploration_weight,
    )

    # Build and return the agent
    return config.build_agent()
