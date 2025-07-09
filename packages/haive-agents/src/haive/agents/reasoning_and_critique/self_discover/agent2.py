# src/haive/agents/selfdiscover/agent.py

import logging

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END
from langgraph.types import Command

from haive.agents.reasoning_and_critique.self_discover.config import (
    SelfDiscoverAgentConfig,
)
from haive.agents.reasoning_and_critique.self_discover.models import (
    ModuleAdaptationResult,
    ModuleSelectionResult,
    ReasoningOutput,
    ReasoningStructure,
)
from haive.agents.reasoning_and_critique.self_discover.state import SelfDiscoverState

# Set up logging
logger = logging.getLogger(__name__)


@register_agent(SelfDiscoverAgentConfig)
class SelfDiscoverAgent(Agent[SelfDiscoverAgentConfig]):
    """An agent that implements the SelfDiscover methodology with structured output models.

    This agent follows a four-stage approach:
    1. Select appropriate reasoning modules for the task
    2. Adapt the modules to better fit the task
    3. Structure the reasoning into a step-by-step plan
    4. Execute the plan to solve the task

    Each stage uses a dedicated LLM with structured output models to ensure
    consistent, high-quality reasoning.
    """

    def setup_workflow(self) -> None:
        """Set up the workflow graph for the SelfDiscover agent."""
        # Create a builder with our schema
        gb = DynamicGraph(name=self.config.name, state_schema=self.state_schema)

        # Define node functions for each stage
        def select_modules(state: SelfDiscoverState) -> Command:
            """Select appropriate reasoning modules for the task."""
            try:
                # Prepare inputs
                inputs = {
                    "reasoning_modules": state.reasoning_modules,
                    "task_description": state.task_description,
                }

                # Create runnable from AugLLMConfig and invoke it
                select_runnable = self.config.select_engine.create_runnable()
                result = select_runnable.invoke(inputs)

                # The result should be a ModuleSelectionResult object
                if isinstance(result, ModuleSelectionResult):
                    # Format the result for the next stage
                    formatted_result = result.format_for_next_stage()

                    # Store both the structured object and formatted string
                    metadata = state.metadata.copy()
                    metadata["selection_result"] = result.model_dump()

                    # Return command with updated state
                    return Command(
                        update={
                            "selected_modules": formatted_result,
                            "metadata": metadata,
                        },
                        goto="adapt",
                    )
                # Fall back to string representation
                selected_modules = self._extract_string_result(result)
                return Command(
                    update={"selected_modules": selected_modules}, goto="adapt"
                )

            except Exception as e:
                logger.error(f"Error in select_modules: {e!s}")
                return Command(
                    update={"error": f"Error in module selection: {e!s}"}, goto=END
                )

        def adapt_modules(state: SelfDiscoverState) -> Command:
            """Adapt the selected modules for the specific task."""
            try:
                # Check if we have selected modules
                if not state.selected_modules:
                    return Command(
                        update={"error": "No modules selected for adaptation"}, goto=END
                    )

                # Prepare inputs
                inputs = {
                    "selected_modules": state.selected_modules,
                    "task_description": state.task_description,
                }

                # Create runnable from AugLLMConfig and invoke it
                adapt_runnable = self.config.adapt_engine.create_runnable()
                result = adapt_runnable.invoke(inputs)

                # The result should be a ModuleAdaptationResult object
                if isinstance(result, ModuleAdaptationResult):
                    # Format the result for the next stage
                    formatted_result = result.format_for_next_stage()

                    # Store both the structured object and formatted string
                    metadata = state.metadata.copy()
                    metadata["adaptation_result"] = result.model_dump()

                    # Return command with updated state
                    return Command(
                        update={
                            "adapted_modules": formatted_result,
                            "metadata": metadata,
                        },
                        goto="structure",
                    )
                # Fall back to string representation
                adapted_modules = self._extract_string_result(result)
                return Command(
                    update={"adapted_modules": adapted_modules}, goto="structure"
                )

            except Exception as e:
                logger.error(f"Error in adapt_modules: {e!s}")
                return Command(
                    update={"error": f"Error in module adaptation: {e!s}"}, goto=END
                )

        def create_structure(state: SelfDiscoverState) -> Command:
            """Create a structured reasoning plan."""
            try:
                # Check if we have adapted modules
                if not state.adapted_modules:
                    return Command(
                        update={"error": "No adapted modules for structure creation"},
                        goto=END,
                    )

                # Prepare inputs
                inputs = {
                    "adapted_modules": state.adapted_modules,
                    "task_description": state.task_description,
                }

                # Create runnable from AugLLMConfig and invoke it
                structure_runnable = self.config.structure_engine.create_runnable()
                result = structure_runnable.invoke(inputs)

                # The result should be a ReasoningStructure object
                if isinstance(result, ReasoningStructure):
                    # Format the result for the next stage
                    formatted_result = result.format_for_next_stage()

                    # Store both the structured object and formatted string
                    metadata = state.metadata.copy()
                    metadata["structure_result"] = result.model_dump()

                    # Return command with updated state
                    return Command(
                        update={
                            "reasoning_structure": formatted_result,
                            "metadata": metadata,
                        },
                        goto="reason",
                    )
                # Fall back to string representation
                reasoning_structure = self._extract_string_result(result)
                return Command(
                    update={"reasoning_structure": reasoning_structure}, goto="reason"
                )

            except Exception as e:
                logger.error(f"Error in create_structure: {e!s}")
                return Command(
                    update={"error": f"Error in structure creation: {e!s}"}, goto=END
                )

        def execute_reasoning(state: SelfDiscoverState) -> Command:
            """Execute the reasoning plan to solve the task."""
            try:
                # Check if we have a reasoning structure
                if not state.reasoning_structure:
                    return Command(
                        update={"error": "No reasoning structure for execution"},
                        goto=END,
                    )

                # Prepare inputs
                inputs = {
                    "reasoning_structure": state.reasoning_structure,
                    "task_description": state.task_description,
                }

                # Create runnable from AugLLMConfig and invoke it
                reasoning_runnable = self.config.reasoning_engine.create_runnable()
                result = reasoning_runnable.invoke(inputs)

                # The result should be a ReasoningOutput object
                if isinstance(result, ReasoningOutput):
                    # Format the result for the final answer
                    formatted_result = result.format_complete_reasoning()

                    # Store both the structured object and formatted string
                    metadata = state.metadata.copy()
                    metadata["reasoning_result"] = result.model_dump()

                    # Prepare update with answer and metadata
                    update = {"answer": result.final_answer, "metadata": metadata}

                    # Also add as message if we have messages
                    if hasattr(state, "messages") and state.messages is not None:
                        messages = list(state.messages)
                        messages.append(AIMessage(content=formatted_result))
                        update["messages"] = messages

                    # Return command with updated state
                    return Command(update=update, goto=END)
                # Fall back to string representation
                answer = self._extract_string_result(result)

                # Prepare update with answer
                update = {"answer": answer}

                # Also add as message if we have messages
                if hasattr(state, "messages") and state.messages is not None:
                    messages = list(state.messages)
                    messages.append(AIMessage(content=answer))
                    update["messages"] = messages

                # Return command with updated state
                return Command(update=update, goto=END)

            except Exception as e:
                logger.error(f"Error in execute_reasoning: {e!s}")
                error_msg = f"Error in reasoning execution: {e!s}"

                # Prepare update with error
                update = {"error": error_msg}

                # Also add error as message if we have messages
                if hasattr(state, "messages") and state.messages is not None:
                    messages = list(state.messages)
                    messages.append(AIMessage(content=f"Error: {error_msg}"))
                    update["messages"] = messages

                # Return command with updated state
                return Command(update=update, goto=END)

        # Add nodes to the graph
        gb.add_node("select", select_modules)
        gb.add_node("adapt", adapt_modules)
        gb.add_node("structure", create_structure)
        gb.add_node("reason", execute_reasoning)

        # Set entry point and build graph
        gb.set_entry_point("select")
        self.graph = gb.build()

        # Compile the graph
        # self.app = self.graph.compile(checkpointer=self.memory)

        logger.info(f"Set up SelfDiscover workflow for {self.config.name}")


# Helper Functions
def create_self_discover_agent(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    name: str | None = None,
    reasoning_modules: list[str] | None = None,
    select_prompt: str | ChatPromptTemplate | None = None,
    adapt_prompt: str | ChatPromptTemplate | None = None,
    structure_prompt: str | ChatPromptTemplate | None = None,
    reasoning_prompt: str | ChatPromptTemplate | None = None,
    visualize: bool = True,
    **kwargs,
) -> SelfDiscoverAgent:
    """Create a SelfDiscover agent with customizable parameters.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        name: Optional name for the agent
        reasoning_modules: List of reasoning modules to use
        select_prompt: Custom prompt for the selection stage
        adapt_prompt: Custom prompt for the adaptation stage
        structure_prompt: Custom prompt for the structure stage
        reasoning_prompt: Custom prompt for the reasoning stage
        visualize: Whether to visualize the graph
        **kwargs: Additional configuration parameters

    Returns:
        SelfDiscoverAgent instance
    """
    # Create config with default settings
    config = SelfDiscoverAgentConfig.from_defaults(
        model=model,
        temperature=temperature,
        name=name,
        reasoning_modules=reasoning_modules,
        select_prompt=select_prompt,
        adapt_prompt=adapt_prompt,
        structure_prompt=structure_prompt,
        reasoning_prompt=reasoning_prompt,
        visualize=visualize,
        **kwargs,
    )

    # Build and return the agent
    return config.build_agent()
