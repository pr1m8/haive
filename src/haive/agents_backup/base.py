from __future__ import annotations
import os
import json
import uuid
import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union, ClassVar, TypeVar, Generic

from pydantic import BaseModel, Field, field_validator

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.haive.core.aug_llm.base import AugLLMConfig, compose_runnable
from src.haive.core.graph.StateSchemaManager import SchemaComposer, StateSchemaManager
from src.haive.utils.visualize_graph_utils import render_and_display_graph
from config.settings import RESOURCES_DIR

# Type variables for generics
TConfig = TypeVar('TConfig', bound='AgentConfig')

# -----------------------------------------------------
# Agent Registry - Maps config classes to agent classes
# -----------------------------------------------------
AGENT_REGISTRY: Dict[Type['AgentConfig'], Type['AgentArchitecture']] = {}

def register_agent(config_class: Type['AgentConfig']):
    """Register an agent class with its configuration class."""
    def decorator(agent_class: Type['AgentArchitecture']):
        AGENT_REGISTRY[config_class] = agent_class
        return agent_class
    return decorator


class AgentConfig(BaseModel, ABC):
    """
    Base configuration for an agent architecture.
    Defines what an agent can do - its capabilities and parameters.
    """
    name: str = Field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:8]}")
    
    engine: Union[AugLLMConfig, 'AgentConfig'] = Field(
        ...,  # Make this required
        description="Engine powering this agent (AugLLMConfig or nested agent config)."
    )
    
    components: List[Union[AugLLMConfig, 'AgentConfig', BaseModel, Dict[str, Any]]] = Field(
        default_factory=list,
        description="Additional components to include in the state schema."
    )
    
    schema: Optional[Union[Type[BaseModel], Dict[str, Any], StateSchemaManager]] = Field(
        default=None,
        description="Optional explicit schema. If None, derived from components."
    )
    
    save_history: bool = Field(
        default=True,
        description="Whether to save state history after execution."
    )
    
    visualize: bool = Field(
        default=False,
        description="Whether to generate a graph visualization."
    )
    
    graph_path: Optional[str] = Field(
        default=None,
        description="Path to save the graph visualization."
    )
    
    runtime_config: Dict[str, Any] = Field(
        default_factory=lambda: {"configurable": {"thread_id": str(uuid.uuid4())}},
        description="Configuration passed to the graph executor at runtime."
    )
    
    # Class variable to store the associated agent class
    agent_class: ClassVar[Optional[Type['AgentArchitecture']]] = None

    @field_validator("engine", mode="after")
    def check_engine_present(cls, v):
        if v is None:
            raise ValueError("An 'engine' must be provided.")
        return v
        
    def derive_schema(self) -> Type[BaseModel]:
        """
        Derive state schema from components and engine.
        
        Returns:
            Pydantic model for the state
        """
        # Collect all components including the engine
        all_components = [self.engine] + self.components
        
        # Use SchemaComposer to build schema
        return SchemaComposer.compose_schema(all_components, name=f"{self.name}State")

    def build_engine(self) -> Any:
        """
        Build the engine based on its type.
        - If it's AugLLMConfig, use compose_runnable().
        - If it's another AgentConfig, recursively build that agent.
        """
        if isinstance(self.engine, AugLLMConfig):
            return compose_runnable(self.engine)
        elif isinstance(self.engine, AgentConfig):
            return self.engine.build_agent()
        else:
            raise ValueError(f"Unsupported engine type: {type(self.engine)}")

    def build_agent(self) -> AgentArchitecture:
        """
        Build an agent instance based on this configuration.
        Uses the agent registry to determine which agent class to instantiate.
        """
        # First, try the registry
        agent_class = AGENT_REGISTRY.get(self.__class__)
        
        # If not in registry, try the class attribute
        if agent_class is None:
            agent_class = self.__class__.agent_class
            
        # If still not found, raise an error
        if agent_class is None:
            raise TypeError(
                f"No agent class registered for config class {self.__class__.__name__}. "
                f"Use @register_agent decorator or set {self.__class__.__name__}.agent_class."
            )
            
        # Instantiate and return the agent
        return agent_class(config=self)


class AgentArchitecture(Generic[TConfig]):
    """
    Base agent architecture class.
    Defines how an agent works - its implementation and behavior.
    """
    def __init__(self, config: TConfig):
        """Initialize the agent with its configuration."""
        self.config = config
        self.memory = MemorySaver()
        
        # Determine state schema - explicitly provided or derived
        if config.schema is None:
            self.state_schema = config.derive_schema()
        elif isinstance(config.schema, dict):
            # Create schema from dict
            schema_manager = StateSchemaManager(config.schema, name=f"{config.name}State")
            self.state_schema = schema_manager.get_model()
        elif isinstance(config.schema, StateSchemaManager):
            # Use schema manager directly
            self.state_schema = config.schema.get_model()
        else:
            # Use provided model class
            self.state_schema = config.schema
            
        # Initialize graph with state schema
        self.graph = StateGraph(self.state_schema)
        self.app = None  # Will hold the compiled application
        
        # Set up state history file path
        self.state_filename = self._make_state_filename()
        
        # Set up graph visualization path
        if config.graph_path:
            self.graph_image_path = config.graph_path
        else:
            self.graph_image_path = os.path.join(RESOURCES_DIR, f"{config.name}_graph.png")
            
        # Build the engine
        self.engine = config.build_engine()
        
        # Set up workflow graph
        self.setup_workflow()
        
        # Compile the graph
        self.compile()
        
        # Generate visualization if requested
        if config.visualize and self.app:
            self.visualize_graph()

    @abstractmethod
    def setup_workflow(self) -> None:
        """
        Set up the workflow graph for this agent.
        Must be implemented by concrete subclasses.
        """
        pass
        
    def compile(self) -> None:
        """Compile the workflow graph into an executable app."""
        if not self.graph:
            raise RuntimeError("Graph is not set up.")
        self.app = self.graph.compile(checkpointer=self.memory)
        print(f"✅ Workflow compiled successfully for {self.config.name}")

    def visualize_graph(self) -> None:
        """Generate and save a visualization of the graph."""
        if self.graph and self.app:
            render_and_display_graph(self.app, output_name=self.graph_image_path)
            print(f"✅ Graph visualization saved to {self.graph_image_path}")
        else:
            print("⚠️ Graph is not set up or compiled.")

    def _make_state_filename(self) -> str:
        """Generate a unique filepath for state history."""
        # Create the directory if it doesn't exist
        state_history_dir = os.path.join(RESOURCES_DIR, "State_History")
        os.makedirs(state_history_dir, exist_ok=True)

        # Generate a unique filename
        base_filename = os.path.join(state_history_dir, f"{self.config.name}.json")
        filename = base_filename
        counter = 1

        # Ensure we don't overwrite existing files
        while os.path.exists(filename):
            filename = os.path.join(state_history_dir, f"{self.config.name}_{counter}.json")
            counter += 1

        return filename

    def run(self, input_text: str, **kwargs) -> Any:
        """
        Run the agent with the given input.
        
        Args:
            input_text: Input text to pass to the agent
            **kwargs: Additional runtime configuration
            
        Returns:
            Final state or output
        """
        if not self.app:
            self.compile()
            
        # Create input according to schema expectations
        inputs = {"messages": [("user", input_text)]}
        
        # Merge runtime configs
        runtime_config = {**self.config.runtime_config, **kwargs}
        
        # Run the agent
        result = self.app.invoke(inputs, config=runtime_config)
        
        # Save state history if requested
        if self.config.save_history:
            self.save_state_history()
            
        return result
        
    def stream(self, input_text: str, **kwargs):
        """
        Stream the agent execution with the given input.
        
        Args:
            input_text: Input text to pass to the agent
            **kwargs: Additional runtime configuration
            
        Returns:
            Generator yielding states
        """
        if not self.app:
            self.compile()
            
        # Create input according to schema expectations
        inputs = {"messages": [("user", input_text)]}
        
        # Merge runtime configs
        runtime_config = {**self.config.runtime_config, **kwargs}
        
        # Stream the execution
        for output in self.app.stream(
            inputs,
            stream_mode="values",
            config=runtime_config
        ):
            yield output
            
        # Save state history if requested
        if self.config.save_history:
            self.save_state_history()

    async def arun(self, input_text: str, **kwargs) -> Any:
        """
        Run the agent asynchronously with the given input.
        
        Args:
            input_text: Input text to pass to the agent
            **kwargs: Additional runtime configuration
            
        Returns:
            Final state or output
        """
        if not self.app:
            self.compile()
            
        # Create input according to schema expectations
        inputs = {"messages": [("user", input_text)]}
        
        # Merge runtime configs
        runtime_config = {**self.config.runtime_config, **kwargs}
        
        # Run the agent asynchronously
        result = await self.app.ainvoke(inputs, config=runtime_config)
        
        # Save state history if requested
        if self.config.save_history:
            self.save_state_history()
            
        return result
        
    async def astream(self, input_text: str, **kwargs):
        """
        Stream the agent execution asynchronously with the given input.
        
        Args:
            input_text: Input text to pass to the agent
            **kwargs: Additional runtime configuration
            
        Returns:
            Async generator yielding states
        """
        if not self.app:
            self.compile()
            
        # Create input according to schema expectations
        inputs = {"messages": [("user", input_text)]}
        
        # Merge runtime configs
        runtime_config = {**self.config.runtime_config, **kwargs}
        
        # Stream the execution asynchronously
        async for output in self.app.astream(
            inputs,
            stream_mode="values",
            config=runtime_config
        ):
            yield output
            
        # Save state history if requested
        if self.config.save_history:
            self.save_state_history()

    def save_state_history(self) -> None:
        """Save the current agent state to a JSON file."""
        if not self.app or not self.memory:
            raise RuntimeError("Workflow graph not compiled or memory not initialized.")

        state_json = self.app.get_state(self.config.runtime_config)
        if not state_json:
            print("⚠️ No state history available.")
            return

        # Ensure state is JSON serializable
        state_json = self._ensure_json_serializable(state_json)

        # Save to file
        with open(self.state_filename, "w", encoding="utf-8") as f:
            json.dump(state_json, f, indent=4)

        print(f"✅ State history saved to: {self.state_filename}")

    def _ensure_json_serializable(self, obj: Any) -> Any:
        """Ensure object is JSON serializable, converting non-serializable objects."""
        try:
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            from pydantic import BaseModel
            if isinstance(obj, BaseModel):
                return obj.model_dump()
            elif isinstance(obj, dict):
                return {k: self._ensure_json_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [self._ensure_json_serializable(v) for v in obj]
            elif isinstance(obj, tuple):
                return [self._ensure_json_serializable(v) for v in obj]
            elif hasattr(obj, "__dict__"):
                return self._ensure_json_serializable(obj.__dict__)
            elif hasattr(obj, "__str__"):
                return str(obj)
            else:
                return "Unserializable Object"