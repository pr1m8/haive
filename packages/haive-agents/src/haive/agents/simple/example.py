"""Example usage of SimpleAgent implementation with enhanced debugging.

This script demonstrates how to create and use SimpleAgent with custom state schema.
"""

import logging
import uuid

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

# Setup enhanced logging with rich
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.traceback import install as install_rich_traceback

from haive.agents.simple import (
    SimpleAgent,
    SimpleAgentConfig,
)

# Install rich traceback for better error display
install_rich_traceback(show_locals=True, width=120, suppress=[])

# Create console
console = Console()

# Configure logging with rich handler
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more verbose output
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
)

# Get logger
logger = logging.getLogger("SimpleAgentDebug")


def debug_print(title, obj, expand=False):
    """Print debugging information in a rich panel."""
    if isinstance(obj, dict):
        from rich.pretty import Pretty

        console.print(
            Panel(Pretty(obj, expand_all=expand), title=title, border_style="cyan")
        )
    else:
        console.print(Panel(str(obj), title=title, border_style="cyan"))


def example_with_custom_state_schema():
    """Create an agent with a custom state schema with enhanced debugging."""
    console.rule("[bold cyan]Creating agent with custom state schema")

    # Define a minimal custom state schema with just what we need
    class CustomAgentState(BaseModel):
        messages: list[BaseMessage] = Field(default_factory=list)
        input: str = Field(default="")
        context: list[str] = Field(default_factory=list)
        # The field that will receive the LLM output
        answer: str = Field(default="")

    # Create prompt template
    prompt = PromptTemplate.from_template(
        """
        Context information: {context}
        
        User query: {input}
        
        Please provide a helpful response based on the context and query.
        """
    )

    # Create the LLM chain with output field explicitly set to answer
    aug_llm = AugLLMConfig(
        name="custom_state_llm",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=prompt,
        output_parser=StrOutputParser(),
        output_field_name="answer",  # Put output directly in answer field
        system_prompt="You are a helpful assistant.",
    )

    # Debug info
    debug_print(
        "AugLLMConfig",
        {
            "name": aug_llm.name,
            "output_field_name": "answer",
            "prompt_variables": prompt.input_variables,
        },
    )

    # Create the agent
    console.print("[bold green]Creating SimpleAgent with custom schema")

    # Define our processor directly as a factory function that will be called
    async def custom_process(state, inputs):
        """Custom process function that ensures the answer is stored"""
        # Call the LLM directly
        result = await aug_llm.ainvoke(inputs)
        console.print(f"[bold blue]LLM Result:[/bold blue] {result}")

        # Store the result
        state.answer = result

        # Debug what's in the state
        console.print(
            f"[bold green]State after process:[/bold green] answer={state.answer}"
        )

        return state

    # Create the agent config with all necessary parameters
    agent_config = SimpleAgentConfig(
        name="custom_state_agent",
        engine=aug_llm,
        state_schema=CustomAgentState,
        debug=True,
        # Explicitly set additional fields for output mapping
        output_mapping={"answer": "answer"},
        # Set the process function directly in the config
        process_func=custom_process,
    )

    # Create the agent with our config
    agent = SimpleAgent(config=agent_config)

    # Set a thread ID for consistent state tracking
    thread_id = str(uuid.uuid4())
    agent.runnable_config["configurable"]["thread_id"] = thread_id
    console.print(f"[bold]Set thread ID:[/bold] {thread_id}")

    # Debug print the input data
    input_data = {
        "input": "What is the capital of Slovakia",
        "context": ["Slovakia is a country in Central Europe."],
    }
    debug_print("Input Data", input_data)

    # Use the agent
    console.print("[bold green]Running the agent...")
    try:
        response = agent.run(input_data, debug=True)

        # Print results
        console.print("[bold green]Agent completed successfully!")
        debug_print("Response", response)

    except Exception:
        console.print("[bold red]Error running agent:")
        console.print_exception(show_locals=True)

    return agent


if __name__ == "__main__":
    console.rule("[bold magenta]SimpleAgent Debug Example")
    example_with_custom_state_schema()
