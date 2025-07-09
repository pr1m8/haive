# src/haive/agents/simple/chain_agent.py
import json
import logging
from datetime import datetime
from typing import Any

from agents.simple.agent import SimpleAgent, SimpleAgentConfig, SimpleAgentStateSchema
from haive.core.engine.agent.agent import register_agent
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)

# =============================================
# Chain Agent Schema - Extends SimpleAgentSchema
# =============================================


class ChainAgentSchema(SimpleAgentStateSchema):
    """Schema for chain agents with intermediate results, extending SimpleAgentSchema."""

    # Inherit messages field from SimpleAgentSchema

    # Add chain-specific fields
    output: str | None = Field(default="", description="Final output from the chain")
    intermediate_results: dict[str, Any] = Field(
        default_factory=dict, description="Results from each engine in the chain"
    )
    current_step: int = Field(default=0, description="Current step in the chain")
    chain_data: dict[str, Any] = Field(
        default_factory=dict, description="Data passed between chain steps"
    )
    error: str | None = Field(
        default=None, description="Error message if any step fails"
    )


# =============================================
# Chain Agent Config - Extends SimpleAgentConfig
# =============================================


class ChainAgentConfig(SimpleAgentConfig):
    """Configuration for a chain agent that processes input through multiple engines in sequence.
    Extends SimpleAgentConfig to inherit its capabilities.
    """

    # Chain configuration
    engines: list[AugLLMConfig] = Field(
        default_factory=list,
        description="List of AugLLMConfig engines to chain together",
    )

    # Step configuration
    step_names: list[str] | None = Field(
        default=None,
        description="Optional names for each step (defaults to engine names)",
    )

    # Override state schema with chain-specific schema
    state_schema: type[BaseModel] = Field(
        default=ChainAgentSchema, description="Schema for the agent state"
    )

    @classmethod
    def from_engines(
        cls,
        engines: list[AugLLMConfig],
        name: str | None = None,
        system_prompt: str | None = None,
        **kwargs,
    ) -> "ChainAgentConfig":
        """Create a ChainAgentConfig from a list of AugLLMConfig engines."""
        # Set first engine as the primary engine
        primary_engine = engines[0] if engines else AugLLMConfig()

        return cls(
            name=name or f"chain_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            engine=primary_engine,  # Use first engine as primary
            engines=engines,  # Store all engines
            system_prompt=system_prompt or "You are a helpful assistant.",
            **kwargs,
        )


# =============================================
# Chain Agent Implementation
# =============================================


@register_agent(ChainAgentConfig)
class ChainAgent(SimpleAgent):
    """An agent that chains multiple engines together, passing output from one to the next.
    Extends SimpleAgent to inherit its base functionality.
    """

    def setup_workflow(self) -> None:
        """Set up a chain workflow with multiple steps using DynamicGraph."""
        logger.debug(f"Setting up workflow for ChainAgent {self.config.name}")

        # Store references to step names for use in processor creation
        self.step_names = []

        # Validate configuration
        if not self.config.engines:
            raise ValueError("No engines provided to chain agent")

        # Get or generate step names
        step_names = self.config.step_names or [
            f"step_{i}_{engine.name}" for i, engine in enumerate(self.config.engines)
        ]

        # Ensure we have the right number of step names
        if len(step_names) != len(self.config.engines):
            logger.warning(
                f"Number of step names ({len(step_names)}) does not match number of engines ({len(self.config.engines)})"
            )
            # Generate missing step names
            if len(step_names) < len(self.config.engines):
                step_names.extend(
                    [
                        f"step_{i+len(step_names)}_{engine.name}"
                        for i, engine in enumerate(
                            self.config.engines[len(step_names) :]
                        )
                    ]
                )
            else:
                step_names = step_names[: len(self.config.engines)]

        # Store step names for use in processors
        self.step_names = step_names

        # Create DynamicGraph with our state schema
        gb = DynamicGraph(
            components=self.config.engines, state_schema=self.state_schema
        )

        # Add nodes for each engine in the chain
        for i, (step_name, engine) in enumerate(
            zip(step_names, self.config.engines, strict=False)
        ):
            # Create a processor for this step
            processor = self._create_step_processor(i, step_name, engine)

            # Determine next step for routing
            next_step_idx = i + 1
            next_step = (
                step_names[next_step_idx] if next_step_idx < len(step_names) else END
            )

            # Add the step processor as a node
            gb.add_node(name=step_name, config=processor, command_goto=next_step)

        # Create an initialization node to set up the first step
        def init_node(state):
            """Initialize the chain state."""
            # Extract text from messages
            if hasattr(state, "messages") and state.messages:
                messages_text = "\n".join(
                    [
                        m.content if hasattr(m, "content") else str(m)
                        for m in state.messages
                    ]
                )

                # Initialize chain_data with input text
                return {"current_step": 0, "chain_data": {"input_text": messages_text}}
            return {"current_step": 0}

        # Add init node and edge to first step
        first_step = step_names[0]
        gb.add_node("init", init_node, command_goto=first_step)

        # Build the graph
        self.graph = gb.build()

        # Compile the graph
        self.app = self.graph.compile(checkpointer=self.memory)

        logger.info(
            f"Set up chain workflow for {self.config.name} with {len(self.config.engines)} steps"
        )

    def _create_step_processor(self, step_idx, step_name, engine_config):
        """Create a processor function for the given step."""

        def process_step(state):
            """Process the current step with its engine."""
            try:
                # Get step data
                step_data = {}

                # Check if we have chain data
                chain_data = {}
                if hasattr(state, "chain_data"):
                    chain_data = state.chain_data

                # First step processing
                if step_idx == 0:
                    # For first step, get data from input
                    if "input_text" in chain_data:
                        input_text = chain_data["input_text"]

                        # Check what this engine expects as input
                        if hasattr(engine_config, "prompt_template") and hasattr(
                            engine_config.prompt_template, "input_variables"
                        ):
                            input_vars = engine_config.prompt_template.input_variables

                            # Map to the right variable name
                            if input_vars and len(input_vars) > 0:
                                primary_var = input_vars[0]  # Use first variable
                                step_data = {primary_var: input_text}
                            else:
                                step_data = {"text": input_text}
                        else:
                            # Default to standard input
                            step_data = {"input": input_text}
                    # Try to use messages directly
                    elif hasattr(state, "messages") and state.messages:
                        step_data = {"messages": state.messages}

                # Subsequent steps
                else:
                    # Get the previous step's result from chain_data
                    prev_step = self.step_names[step_idx - 1]
                    if prev_step in chain_data:
                        prev_result = chain_data[prev_step]

                        # Check what this engine expects as input
                        if hasattr(engine_config, "prompt_template") and hasattr(
                            engine_config.prompt_template, "input_variables"
                        ):
                            input_vars = engine_config.prompt_template.input_variables

                            # Map to the right variable name
                            if input_vars and len(input_vars) > 0:
                                primary_var = input_vars[0]  # Use first variable
                                step_data = {primary_var: prev_result}
                            else:
                                step_data = {"text": prev_result}
                        else:
                            # Default to standard input
                            step_data = {"input": prev_result}

                # Log the data being passed to the engine
                logger.debug(f"Running step {step_idx}: {step_name}")
                logger.debug(f"Input data keys: {list(step_data.keys())}")

                # Create engine runnable
                runnable = compose_runnable(engine_config)

                # Invoke the engine
                result = runnable.invoke(step_data)

                # Extract a string result regardless of the return type
                if isinstance(result, str):
                    result_str = result
                elif isinstance(result, dict):
                    # For structured output models
                    if "output" in result:
                        result_str = result["output"]
                    else:
                        # Serialize to JSON
                        result_str = json.dumps(result)
                elif hasattr(result, "model_dump"):
                    # Pydantic model
                    result_str = json.dumps(result.model_dump())
                elif hasattr(result, "dict"):
                    # Pydantic v1 model
                    result_str = json.dumps(result.dict())
                elif hasattr(result, "content"):
                    # Message with content
                    result_str = result.content
                else:
                    # Fallback
                    result_str = str(result)

                # Update chain data with this step's result
                updated_chain_data = dict(chain_data)
                updated_chain_data[step_name] = result_str

                # For diagnostic purposes, also store raw result
                if not isinstance(result, str):
                    updated_chain_data[f"{step_name}_raw"] = str(result)

                # Update intermediate results
                intermediate_results = {}
                if hasattr(state, "intermediate_results"):
                    intermediate_results = dict(state.intermediate_results)
                intermediate_results[step_name] = result_str

                # Create updated state
                updated_state = {
                    "intermediate_results": intermediate_results,
                    "chain_data": updated_chain_data,
                    "current_step": step_idx + 1,
                }

                # If this is the last step, also update output and add to messages
                if step_idx == len(self.config.engines) - 1:
                    updated_state["output"] = result_str

                    # Add as AI message if we have messages
                    if hasattr(state, "messages"):
                        messages = list(state.messages)
                        messages.append(AIMessage(content=result_str))
                        updated_state["messages"] = messages

                return updated_state

            except Exception as e:
                logger.error(f"Error in step {step_idx} ({step_name}): {e!s}")
                error_msg = f"Error in step {step_idx} ({step_name}): {e!s}"

                # Add error as AI message if we have messages
                updated_state = {
                    "error": error_msg,
                    "current_step": len(self.config.engines),  # Skip to end
                }

                if hasattr(state, "messages"):
                    messages = list(state.messages)
                    messages.append(AIMessage(content=f"Error: {error_msg}"))
                    updated_state["messages"] = messages

                return updated_state

        return process_step

    def _prepare_input(
        self, input_data: str | list[str] | dict[str, Any] | BaseModel
    ) -> Any:
        """Override the prepare_input method to handle chain-specific input preparation."""
        # Use the parent's method as base
        if isinstance(input_data, str):
            # Single string to messages
            return self.state_schema(
                messages=[HumanMessage(content=input_data)],
                current_step=0,
                chain_data={"input_text": input_data},
            )
        if isinstance(input_data, list) and all(
            isinstance(item, str) for item in input_data
        ):
            # List of strings to messages
            messages = [HumanMessage(content=item) for item in input_data]
            combined_text = "\n".join(input_data)
            return self.state_schema(
                messages=messages,
                current_step=0,
                chain_data={"input_text": combined_text},
            )
        if isinstance(input_data, dict):
            # Make sure current_step and chain_data are set
            input_data_copy = dict(input_data)
            if "current_step" not in input_data_copy:
                input_data_copy["current_step"] = 0
            if "chain_data" not in input_data_copy:
                input_data_copy["chain_data"] = {}
            return self.state_schema(**input_data_copy)
        if isinstance(input_data, BaseModel):
            # Convert BaseModel to dict and set current_step
            data = (
                input_data.model_dump()
                if hasattr(input_data, "model_dump")
                else input_data.dict()
            )
            if "current_step" not in data:
                data["current_step"] = 0
            if "chain_data" not in data:
                data["chain_data"] = {}
            return self.state_schema(**data)
        raise ValueError(f"Invalid input type: {type(input_data)}")


# =============================================
# Helper Functions
# =============================================


def create_chain_agent(
    engines: list[AugLLMConfig],
    name: str | None = None,
    system_prompt: str | None = None,
    step_names: list[str] | None = None,
    visualize: bool = True,
    **kwargs,
) -> ChainAgent:
    """Create a chain agent from a list of engines.

    Args:
        engines: List of AugLLMConfig engines to chain together
        name: Optional name for the agent
        system_prompt: Optional system prompt
        step_names: Optional names for each step
        visualize: Whether to generate a visualization
        **kwargs: Additional configuration parameters

    Returns:
        ChainAgent instance
    """
    # Create config
    config = ChainAgentConfig.from_engines(
        engines=engines,
        name=name,
        system_prompt=system_prompt,
        step_names=step_names,
        visualize=visualize,
        **kwargs,
    )

    # Build and return the agent
    return config.build_agent()


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Import necessary modules for examples
    from haive.core.models.llm.base import AzureLLMConfig
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    # Create a few example engines
    translator_prompt = ChatPromptTemplate.from_messages(
        [("human", "Translate the following text to French:\n\n{text}")]
    )

    translator_engine = AugLLMConfig(
        name="translator",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
        prompt_template=translator_prompt,
        output_parser=StrOutputParser(),
    )

    summarizer_prompt = ChatPromptTemplate.from_messages(
        [("human", "Summarize the following text in one sentence:\n\n{text}")]
    )

    summarizer_engine = AugLLMConfig(
        name="summarizer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.4}),
        prompt_template=summarizer_prompt,
        output_parser=StrOutputParser(),
    )

    # Create a chain agent that translates and then summarizes
    chain_agent = create_chain_agent(
        engines=[translator_engine, summarizer_engine],
        name="translate_then_summarize",
        step_names=["translate", "summarize"],
    )

    # Run the agent
    result = chain_agent.run(
        "The sky is blue and the clouds are white. The weather is nice today and I'm enjoying the sunshine."
    )

    # Print results
    print(f"\nOutput: {result.get('output', '')}")
    print("\nIntermediate results:")
    for step, output in result.get("intermediate_results", {}).items():
        print(f"  {step}: {output}")

    # Print messages
    print("\nMessages:")
    for msg in result.get("messages", []):
        if hasattr(msg, "content"):
            print(f"{msg.type.upper()}: {msg.content}")
