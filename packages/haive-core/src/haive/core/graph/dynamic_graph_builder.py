# src/haive/core/graph/dynamic_graph_builder.py

import inspect
import logging
import os
import time
import traceback
import uuid
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    Union,
)

from pydantic import BaseModel, Field

try:
    import matplotlib.pyplot as plt
    import networkx as nx
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

from langgraph.graph import END, START, StateGraph

from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.base import Engine, EngineRegistry
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory

#from haive.core.graph.node.registry import NodeTypeRegistry
from haive.core.schema.schema_composer import SchemaComposer

# Configure logger with file and console handlers
logger = logging.getLogger("DynamicGraph")

# Set up detailed file handler
file_handler = logging.FileHandler('dynamic_graph.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Set up console handler (less verbose)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

# Debug level enum
class DebugLevel(str, Enum):
    """Debug level for the graph builder."""
    NONE = "none"     # No debugging output except errors
    BASIC = "basic"   # Basic information and warnings
    VERBOSE = "verbose"  # Detailed information about operations
    TRACE = "trace"   # Complete trace of all operations with entry/exit logging
    PERFORMANCE = "performance"  # Include timing information for operations

# Edge representation
class DynamicGraphEdge(BaseModel):
    """Edge representation with enhanced debugging properties."""
    source: str
    target: str
    condition: Optional[Callable] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def __str__(self):
        """String representation for debugging."""
        base = f"{self.source} → {self.target}"
        if self.condition:
            cond_name = getattr(self.condition, "__name__", "condition")
            return f"{base} [conditional: {cond_name}]"
        return base
    
    class Config:
        arbitrary_types_allowed = True

# Component reference model
class ComponentRef(BaseModel):
    """Reference to a component that can be resolved at runtime."""
    name: str
    type: Optional[str] = None
    id: Optional[str] = None
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Node status tracking
class NodeStatus(str, Enum):
    """Status of nodes in the graph."""
    ADDED = "added"
    CONNECTED = "connected"
    UNREACHABLE = "unreachable"
    ERROR = "error"

class DynamicGraph:
    """
    Dynamic graph builder with enhanced error tracing and node system integration.
    
    This class provides a builder interface for creating StateGraph instances
    with improved error diagnostics, tracing, and full integration with the
    advanced node system.
    """
    
    def __init__(
        self,
        name: Union[str,int] = None,
        components: List[Any] = None,
        state_schema: Optional[Type[BaseModel]] = None,
        input_schema: Optional[Type[BaseModel]] = None,
        output_schema: Optional[Type[BaseModel]] = None, 
        description: Optional[str] = None,
        default_runnable_config: Optional[Dict[str, Any]] = None,
        visualize: bool = False,
        debug_level: Union[str, DebugLevel] = DebugLevel.BASIC,
        **kwargs
    ):
        """
        Initialize a new DynamicGraph builder with enhanced node support.
        
        Args:
            name: Unique name for this graph
            components: List of engines, component references, or other components
            state_schema: Optional explicit schema class (otherwise derived from components)
            description: Optional description
            default_runnable_config: Default runtime configuration for nodes
            visualize: Whether to automatically visualize the graph
            debug_level: Level of debugging information
            **kwargs: Additional keyword arguments
        """
        try:
            logger.info(f"Initializing DynamicGraph: {name}")
            logger.debug(f"Parameters: components={len(components) if components else 0}, "
                        f"state_schema={'provided' if state_schema else 'None'}, "
                        f"debug_level={debug_level}, visualize={visualize}")
            
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.name = name if name else self.id
            self.description = description
            self.components = components or []
            self.visualize = visualize
            self.default_runnable_config = default_runnable_config or {}
            self.debug_level = DebugLevel(debug_level) if isinstance(debug_level, str) else debug_level
            
            # State tracking
            self.engines = {}  # name -> engine
            self.engines_by_id = {}  # id -> engine
            self.nodes = {}  # name -> node_config
            self.node_statuses = {}  # name -> NodeStatus
            self.edges = []  # list of DynamicGraphEdge
            self.branches = []  # list of branch conditions
            self.applied_patterns = []  # list of applied pattern names
            
            # Error tracking
            self.errors = []  # track errors with traces
            self.warnings = []  # track warnings
            self.operation_counts = {}  # count of operations by type
            self.created_at = datetime.now()
            self.last_modified = self.created_at
            self.metadata = {}  # Additional metadata
            
            # Configure logger based on debug level
            self._configure_logger()
            
            # Initialize registries and node system
            self._initialize_registries()
            if not input_schema:
                self.input_schema = state_schema
            else:
                self.input_schema = input_schema
            if not output_schema:
                self.output_schema = state_schema
            else:
                self.output_schema = output_schema
            # Process components and initialize schemas
            try:
                logger.debug("Processing components...")
                self._process_components()
                
                logger.debug("Initializing schemas...")
                self._initialize_schemas(state_schema)
                
                logger.debug("Initializing graph...")
                self._initialize_graph()
                
                logger.info(f"DynamicGraph initialized: {self.name}")
            except Exception as e:
                tb = traceback.format_exc()
                logger.error(f"Initialization failed: {str(e)}\n{tb}")
                # Re-raise with context
                raise ValueError(f"Failed to initialize DynamicGraph: {str(e)}") from e
                
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error in DynamicGraph.__init__: {str(e)}\n{tb}")
            raise
    
    def _configure_logger(self):
        """Configure logger based on debug level."""
        try:
            if self.debug_level == DebugLevel.NONE:
                logger.setLevel(logging.WARNING)
            elif self.debug_level == DebugLevel.BASIC:
                logger.setLevel(logging.INFO)
            elif self.debug_level in [DebugLevel.VERBOSE, DebugLevel.TRACE]:
                logger.setLevel(logging.DEBUG)
            elif self.debug_level == DebugLevel.PERFORMANCE:
                logger.setLevel(logging.DEBUG)
                
            logger.debug(f"Logger configured with level: {self.debug_level}")
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error configuring logger: {str(e)}\n{tb}")
    
    def _initialize_registries(self):
        """Initialize registries used by the graph builder."""
        try:
            logger.debug("Initializing node registry...")
            
            # Get the NodeTypeRegistry instance
            #self.node_registry = NodeTypeRegistry.get_instance()
            
            # Ensure default processors are registered
            #if not self.node_registry.node_processors:
                #logger.debug("Registering default node processors...")
                #self.node_registry.register_default_processors()

            # Set up NodeFactory to use our registry
            #NodeFactory.set_registry(self.node_registry)
            
            logger.debug("Node registry and factory initialized successfully")
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error initializing registries: {str(e)}\n{tb}")
            # Store error but continue
            self._log_error("Registry initialization failed", e)
    
    def _log_error(self, message: str, error: Exception, is_warning: bool = False):
        """
        Log error with detailed traceback.
        
        Args:
            message: Error message
            error: Exception that occurred
            is_warning: Whether this is a warning (otherwise error)
        """
        try:
            error_message = f"{message}: {str(error)}"
            
            # Get traceback
            tb = traceback.format_exc()
            error_with_tb = f"{error_message}\n{tb}"
            
            if is_warning:
                logger.warning(error_message)
                for line in tb.split('\n'):
                    logger.warning(f"  {line}")
                self.warnings.append(error_with_tb)
            else:
                logger.error(error_message)
                for line in tb.split('\n'):
                    logger.error(f"  {line}")
                self.errors.append(error_with_tb)
        except Exception as e:
            logger.error(f"Error in _log_error: {str(e)}")
    
    def _process_components(self):
        """Process and resolve component references to engines."""
        try:
            component_count = len(self.components)
            logger.debug(f"Processing {component_count} components")
            
            registry = EngineRegistry.get_instance()
            
            resolved_components = 0
            
            for i, component in enumerate(self.components):
                try:
                    logger.debug(f"Processing component {i+1}/{component_count}: {type(component).__name__}")
                    
                    # Handle string references
                    if isinstance(component, str):
                        # Try to lookup in registry by name
                        engine = registry.find(component)
                        if engine:
                            logger.debug(f"Resolved component string '{component}' to engine: {engine.name}")
                            component = engine
                            resolved_components += 1
                        else:
                            logger.warning(f"Could not resolve component string: {component}")
                            continue
                    
                    # Handle ComponentRef objects
                    elif isinstance(component, ComponentRef):
                        engine = None
                        # Try to lookup by ID first
                        if component.id:
                            engine = registry.find(component.id)
                        
                        # Try to lookup by name
                        if not engine and component.name:
                            engine = registry.find(component.name)
                        
                        if engine:
                            logger.debug(f"Resolved ComponentRef '{component.name}' to engine: {engine.name}")
                            component = engine
                            resolved_components += 1
                        else:
                            logger.warning(f"Could not resolve ComponentRef: {component.name}")
                            continue
                    
                    # If it's an Engine, register it by name and ID
                    if isinstance(component, Engine):
                        self.engines[component.name] = component
                        # Register by ID if available
                        engine_id = getattr(component, "id", None)
                        if engine_id:
                            logger.debug(f"Registering engine by ID: {engine_id}")
                            self.engines_by_id[engine_id] = component
                        else:
                            logger.debug(f"Engine {component.name} has no ID")
                    
                    # Replace in components list (if changed)
                    self.components[i] = component
                    
                except Exception as e:
                    self._log_error(f"Error processing component {i}", e)
                    # Continue with other components
            
            logger.info(f"Processed {len(self.components)} components, resolved {resolved_components}")
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error in _process_components: {str(e)}\n{tb}")
            raise
    
    def _initialize_schemas(self, state_schema=None):
        """Initialize state and I/O schemas."""
        try:
            # Use provided schema if available
            if state_schema:
                self.state_model = state_schema
                logger.info(f"Using provided state schema: {state_schema.__name__}")
            else:
                # Auto-derive schema from components
                schema_name = f"{self.name.replace('-', '_').title()}State"
                logger.info(f"Deriving state schema from components as '{schema_name}'")
                
                try:
                    self.schema_composer = SchemaComposer(name=schema_name)
                    self.schema_composer.from_components(self.components)
                    self.state_model = self.schema_composer.build()
                    
                    logger.info(f"Successfully derived state schema: {self.state_model.__name__}")
                except Exception as e:
                    self._log_error("Error deriving state schema", e, is_warning=True)
                    
                    # Create minimal backup schema
                    logger.warning("Creating backup minimal schema due to derivation failure")
                    self.schema_composer = SchemaComposer(name=schema_name)
                    self.schema_composer.add_field("messages", list, default_factory=list)
                    self.schema_composer.add_field("input", str, default="")
                    self.schema_composer.add_field("output", str, default="")
                    self.state_model = self.schema_composer.build()
                    
                    logger.debug(f"Backup schema created: {self.state_model.__name__}")
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error in _initialize_schemas: {str(e)}\n{tb}")
            raise
    # TODO: Fix
    def _initialize_graph(self):
        """Initialize the underlying StateGraph."""
        try:
            logger.debug(f"Initializing StateGraph with schema: {self.state_model.__name__}")
            
            self.graph_builder = StateGraph(state_schema=self.state_model, input=self.input_schema,
                                            output=self.output_schema)
            logger.info(f"Initialized StateGraph with schema: {self.state_model.__name__}")
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error initializing StateGraph: {str(e)}\n{tb}")
            
            # Analyze common initialization errors
            if "required positional argument" in str(e):
                logger.error("StateGraph initialization failed due to missing required arguments")
                logger.error(f"StateGraph expected args: {inspect.signature(StateGraph.__init__)}")
            elif "not callable" in str(e):
                logger.error("StateGraph initialization failed due to non-callable schema")
                logger.error(f"Schema type: {type(self.state_model)}")
            
            # Re-raise with context
            raise ValueError(f"Failed to initialize StateGraph: {str(e)}") from e
    
    def with_runnable_config(self, config: Dict[str, Any]) -> 'DynamicGraph':
        """
        Create a new DynamicGraph with the specified runnable config.
        
        Args:
            config: Runnable configuration to use
            
        Returns:
            New DynamicGraph instance with the specified config
        """
        try:
            logger.debug("Creating new graph with custom runnable config")
            
            # Create a new graph with the same settings but different config
            new_graph = DynamicGraph(
                name=self.name,
                components=self.components,
                state_schema=self.state_model,
                description=self.description,
                default_runnable_config=config,
                visualize=self.visualize,
                debug_level=self.debug_level,
                id=str(uuid.uuid4())  # New ID for new instance
            )
            
            # Copy existing nodes, edges, and branches
            new_graph.nodes = self.nodes.copy()
            new_graph.node_statuses = self.node_statuses.copy()
            new_graph.edges = self.edges.copy()
            new_graph.branches = self.branches.copy()
            new_graph.applied_patterns = self.applied_patterns.copy()
            
            logger.info(f"Created new graph with custom runnable config: {new_graph.id}")
            
            return new_graph
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error in with_runnable_config: {str(e)}\n{tb}")
            raise
    
    def set_default_runnable_config(self, config: Dict[str, Any]) -> 'DynamicGraph':
        """
        Set the default runnable config for this graph.
        
        Args:
            config: Runnable configuration to set as default
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug("Setting default runnable config")
            
            self.default_runnable_config = config
            logger.info("Updated default runnable config")
            
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error in set_default_runnable_config: {str(e)}\n{tb}")
            raise
    
    def update_default_runnable_config(self, **kwargs) -> 'DynamicGraph':
        """
        Update the default runnable config with new values.
        
        Args:
            **kwargs: Key-value pairs to update in the config
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug(f"Updating default runnable config with keys: {list(kwargs.keys())}")
            
            # Convert to RunnableConfig if not already
            if not self.default_runnable_config:
                self.default_runnable_config = RunnableConfigManager.create(**kwargs)
            else:
                # Ensure configurable section exists
                if "configurable" not in self.default_runnable_config:
                    self.default_runnable_config = {"configurable": {}}
                elif not isinstance(self.default_runnable_config["configurable"], dict):
                    # Fix misconfigured configurable
                    logger.warning("Found invalid configurable section, resetting")
                    self.default_runnable_config["configurable"] = {}
                
                # Add each kwarg to the configurable section
                for key, value in kwargs.items():
                    self.default_runnable_config["configurable"][key] = value
            
            logger.info(f"Updated default runnable config with: {', '.join(kwargs.keys())}")
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error in update_default_runnable_config: {str(e)}\n{tb}")
            raise
    
    def add_node(
        self,
        name: str,
        config: Union[NodeConfig, Engine, str, Callable, Any],
        command_goto: Optional[Union[str, Literal["END"]]] = None,
        input_mapping: Optional[Dict[str, str]] = None,
        output_mapping: Optional[Dict[str, str]] = None,
        runnable_config: Optional[Dict[str, Any]] = None,
        debug: bool = False,
        **kwargs
    ) -> 'DynamicGraph':
        """
        Add a node to the graph with enhanced error tracking and processor support.
        
        Args:
            name: Name of the node
            config: NodeConfig, Engine, or callable function for the node
            command_goto: Optional next node to go to (ignored if NodeConfig provided)
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            runnable_config: Optional runtime configuration
            debug: Enable debug logging for this node
            **kwargs: Additional parameters for NodeConfig
            
        Returns:
            Self for chaining
        """
        start_time = time.time()
        try:
            logger.debug(f"Adding node: {name} (type: {type(config).__name__})")
            
            # Check if node already exists
            if name in self.nodes:
                logger.warning(f"Node '{name}' already exists. Overwriting.")
            
            # Handle END constant conversion
            if command_goto == "END":
                logger.debug("Converting 'END' string to END constant")
                command_goto = END
            
            # Create NodeConfig if not already
            if not isinstance(config, NodeConfig) and isinstance(config, Engine):
                logger.debug(f"Creating NodeConfig for {name}")
                node_config = NodeConfig(
                    name=name,
                    engine=config,
                    command_goto=command_goto,
                    input_mapping=input_mapping,
                    output_mapping=output_mapping,
                    runnable_config=runnable_config,
                    debug=debug or self.debug_level in [DebugLevel.VERBOSE, DebugLevel.TRACE],
                    #registry=self.node_registry,
                    **kwargs
                )
                logger.debug(f"Created NodeConfig: {node_config.name}")
            elif isinstance(config,Callable):
                logger.debug(f"Creating NodeConfig for {name} from callable")
                node_config = NodeConfig(
                    name=name,
                    callable_func=config,
                    command_goto=command_goto,
                )
            else:
                logger.debug(f"Using provided NodeConfig: {config.name}")
                node_config = config
                # If this is already a NodeConfig, ensure END is properly set
                if getattr(node_config, "command_goto", None) == "END":
                    node_config.command_goto = END
            
            # Set registry reference 
            #node_config.registry = self.node_registry
            
            # Resolve engine reference
            logger.debug(f"Resolving engine reference for node: {name}")
            engine, engine_id = node_config.get_engine()
            logger.debug(f"Resolved engine: {type(engine).__name__}, id: {engine_id}")
            
            # Create node function using NodeFactory
            logger.debug(f"Creating node function with NodeFactory for: {name}")
            #print('--------------------------------')
            #print(node_config)
            #print('--------------------------------')
            #breakpoint()
            node_function = NodeFactory().create_node_function(node_config)
            
            # Add to StateGraph
            try:
                logger.debug(f"Adding node to StateGraph: {name}")
                self.graph_builder.add_node(name, node_function)
                logger.debug(f"Successfully added node to StateGraph: {name}")
            except Exception as sg_error:
                self._log_error(f"Error adding node '{name}' to StateGraph", sg_error)
                # Re-raise with more context
                raise ValueError(f"Failed to add node to StateGraph: {str(sg_error)}") from sg_error
            
            # Store node config for debugging
            self.nodes[name] = node_config
            self.node_statuses[name] = NodeStatus.ADDED
            
            # Update node function storage
            self.metadata.setdefault("node_functions", {})[name] = {
                "type": node_config.node_type, 
                "created_at": datetime.now().isoformat()
            }
            
            logger.info(f"Added node: {name}")
            
            # If node has command_goto set to END, explicitly add an edge to END
            if node_config.command_goto is END:
                logger.debug(f"Node '{name}' has command_goto=END, adding explicit edge")
                self.add_edge(name, END)
            
            # Log performance
            if self.debug_level == DebugLevel.PERFORMANCE:
                elapsed = time.time() - start_time
                logger.debug(f"Node addition took {elapsed:.4f} seconds")
            
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error adding node '{name}': {str(e)}\n{tb}")
            
            # Track error
            self._log_error(f"Error adding node '{name}'", e)
            
            # Update node status to ERROR if it was partially added
            if name in self.nodes:
                self.node_statuses[name] = NodeStatus.ERROR
            
            raise
    
    def add_mapping_node(
        self,
        name: str,
        item_provider: str,
        target_node: str,
        item_key: str = "item",
        **kwargs
    ) -> 'DynamicGraph':
        """
        Add a node that maps items to parallel processing.
        
        Args:
            name: Name for the node
            item_provider: State key containing the items list
            target_node: Target node to send items to
            item_key: Key to use for each item in the target
            **kwargs: Additional node configuration options
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug(f"Creating mapping node: {name} → {target_node}")
            
            # Create the mapping node function
            node_function = NodeFactory.create_mapping_node(
                item_provider=item_provider,
                target_node=target_node,
                item_key=item_key,
                name=name
            )
            
            # Add to graph
            try:
                logger.debug(f"Adding mapping node to StateGraph: {name}")
                self.graph_builder.add_node(name, node_function)
                logger.debug(f"Successfully added mapping node: {name}")
            except Exception as sg_error:
                self._log_error(f"Error adding mapping node '{name}' to StateGraph", sg_error)
                raise ValueError(f"Failed to add mapping node: {str(sg_error)}") from sg_error
            
            # Store node config (create minimal one for tracking)
            self.nodes[name] = NodeConfig(
                name=name,
                engine=node_function.__node_config__.engine,
                node_type="mapping",
                metadata={"item_provider": item_provider, "target_node": target_node},
                registry=self.node_registry
            )
            self.node_statuses[name] = NodeStatus.ADDED
            
            logger.info(f"Added mapping node: {name} → {target_node}")
            
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error adding mapping node '{name}': {str(e)}\n{tb}")
            self._log_error(f"Error adding mapping node '{name}'", e)
            raise
    
    def add_conditional_node(
        self,
        name: str,
        condition_func: Callable,
        routes: Dict[Any, str],
        default_route: Optional[str] = None,
        **kwargs
    ) -> 'DynamicGraph':
        """
        Add a node that routes based on a condition function.
        
        Args:
            name: Name for the node
            condition_func: Function that takes state and returns a key
            routes: Mapping from condition results to node names
            default_route: Default route if no match
            **kwargs: Additional node configuration options
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug(f"Creating conditional node: {name} with {len(routes)} routes")
            
            # Create the conditional node function
            node_function = NodeFactory.create_conditional_node(
                condition_func=condition_func,
                routes=routes,
                default_route=default_route,
                name=name
            )
            
            # Add to graph
            try:
                logger.debug(f"Adding conditional node to StateGraph: {name}")
                self.graph_builder.add_node(name, node_function)
                logger.debug(f"Successfully added conditional node: {name}")
            except Exception as sg_error:
                self._log_error(f"Error adding conditional node '{name}' to StateGraph", sg_error)
                raise ValueError(f"Failed to add conditional node: {str(sg_error)}") from sg_error
            
            # Store node config (create minimal one for tracking)
            self.nodes[name] = NodeConfig(
                name=name,
                engine=node_function.__node_config__.engine,
                metadata={"routes": routes, "default_route": default_route},
                registry=self.node_registry
            )
            self.node_statuses[name] = NodeStatus.ADDED
            
            logger.info(f"Added conditional node: {name} with {len(routes)} routes")
            
            # Add edges for visualization (doesn't affect logic which is in the node)
            for route_name, target in routes.items():
                edge = DynamicGraphEdge(
                    source=name,
                    target=target,
                    condition=condition_func,
                    metadata={"condition_key": route_name}
                )
                self.edges.append(edge)
                
            # Add default route if provided
            if default_route:
                edge = DynamicGraphEdge(
                    source=name,
                    target=default_route,
                    condition=condition_func,
                    metadata={"is_default": True}
                )
                self.edges.append(edge)
            
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error adding conditional node '{name}': {str(e)}\n{tb}")
            self._log_error(f"Error adding conditional node '{name}'", e)
            raise
    
    def add_error_handler(
        self,
        name: str,
        fallback_node: str = "END",
        **kwargs
    ) -> 'DynamicGraph':
        """
        Add an error handling node to the graph.
        
        Args:
            name: Name for the node
            fallback_node: Node to route to after handling error
            **kwargs: Additional node configuration options
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug(f"Creating error handler node: {name} → {fallback_node}")
            
            # Handle END constant conversion
            if fallback_node == "END":
                fallback_node = END
            
            # Create the error handler node function
            node_function = NodeFactory.create_error_handler_node(
                fallback_node=fallback_node,
                name=name
            )
            
            # Add to graph
            try:
                logger.debug(f"Adding error handler node to StateGraph: {name}")
                self.graph_builder.add_node(name, node_function)
                logger.debug(f"Successfully added error handler node: {name}")
            except Exception as sg_error:
                self._log_error(f"Error adding error handler '{name}' to StateGraph", sg_error)
                raise ValueError(f"Failed to add error handler: {str(sg_error)}") from sg_error
            
            # Store node config
            self.nodes[name] = NodeConfig(
                name=name,
                engine=node_function.__node_config__.engine,
                command_goto=fallback_node,
                metadata={"handler_type": "error", "fallback": str(fallback_node)},
                registry=self.node_registry
            )
            self.node_statuses[name] = NodeStatus.ADDED
            
            # Add edge to fallback for visualization
            self.edges.append(DynamicGraphEdge(
                source=name, 
                target=str(fallback_node)
            ))
            
            logger.info(f"Added error handler node: {name} → {fallback_node}")
            
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error adding error handler '{name}': {str(e)}\n{tb}")
            self._log_error(f"Error adding error handler '{name}'", e)
            raise
    
    def add_edge(self, from_node: str, to_node: Union[str, Literal["END"]]) -> 'DynamicGraph':
        """
        Add an edge between two nodes with enhanced validation.
        
        Args:
            from_node: Source node name
            to_node: Target node name
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug(f"Adding edge: {from_node} → {to_node}")
            
            # Convert "START" to special constant
            original_from = from_node
            if from_node == "START":
                logger.debug("Converting 'START' string to START constant")
                from_node = START
            
            # Convert "END" to special constant
            original_to = to_node
            if to_node == "END":
                logger.debug("Converting 'END' string to END constant")
                to_node = END
            
            # Validate nodes exist (except START/END)
            # First, recognize both "END" and "__end__" as valid special nodes
            is_end_node = original_to == "END" or original_to == "__end__"
            is_start_node = original_from == "START" or original_from == "__start__"
            
            # Check if we have any undefined nodes
            if (not is_start_node and original_from not in self.nodes) or \
               (not is_end_node and original_to not in self.nodes):
                error_nodes = []
                
                if not is_start_node and original_from not in self.nodes:
                    error_nodes.append(f"'{original_from}' (source)")
                    
                if not is_end_node and original_to not in self.nodes:
                    error_nodes.append(f"'{original_to}' (target)")
                
                # Only log warning if we have actual undefined nodes
                if error_nodes:
                    logger.warning(f"Cannot add edge between undefined nodes: {', '.join(error_nodes)}")
                    logger.warning("Edge will be added, but graph may not compile")
            
            # Add to StateGraph
            try:
                logger.debug(f"Adding edge to StateGraph: {from_node} → {to_node}")
                self.graph_builder.add_edge(from_node, to_node)
                logger.debug("Successfully added edge to StateGraph")
            except Exception as sg_error:
                self._log_error(f"Error adding edge {from_node} → {to_node} to StateGraph", sg_error)
                
                # Additional error analysis
                if "is not in graph" in str(sg_error):
                    if "from_node" in str(sg_error):
                        logger.error(f"Source node '{from_node}' is not in the graph")
                        logger.error("Add the source node first with add_node()")
                    else:
                        logger.error(f"Target node '{to_node}' is not in the graph")
                        logger.error("Add the target node first with add_node()")
                
                raise ValueError(f"Failed to add edge: {str(sg_error)}") from sg_error
            
            # Update node statuses
            if original_from != "START" and original_from in self.nodes:
                self.node_statuses[original_from] = NodeStatus.CONNECTED
            
            if original_to != "END" and original_to in self.nodes:
                self.node_statuses[original_to] = NodeStatus.CONNECTED
            
            # Store edge for debugging
            edge = DynamicGraphEdge(
                source=str(original_from), 
                target=str(original_to)
            )
            self.edges.append(edge)
            
            logger.info(f"Added edge: {original_from} → {original_to}")
            
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error adding edge {from_node} → {to_node}: {str(e)}\n{tb}")
            self._log_error(f"Error adding edge {from_node} → {to_node}", e)
            raise
    
    def add_conditional_edges(
        self,
        from_node: str,
        condition: Callable,
        routes: Dict[str, str]
    ) -> 'DynamicGraph':
        """
        Add conditional routing based on a condition function.
        
        Args:
            from_node: Source node name
            condition: Function that takes state and returns a key
            routes: Mapping from condition results to target nodes
            
        Returns:
            Self for chaining
        """
        try:
            # Get condition name for better logging
            condition_name = getattr(condition, "__name__", "anonymous_condition")
            logger.debug(f"Adding conditional edges from {from_node} using '{condition_name}'")
            
            # Validate source node
            if from_node not in self.nodes:
                logger.warning(f"Conditional source node '{from_node}' doesn't exist yet")
            
            # Validate target nodes
            missing_targets = []
            for key, target in routes.items():
                if target != "END" and target not in self.nodes:
                    missing_targets.append(target)
            
            if missing_targets:
                logger.warning(f"Conditional targets don't exist yet: {', '.join(missing_targets)}")
            
            # Validate condition function takes a state parameter
            try:
                sig = inspect.signature(condition)
                if len(sig.parameters) < 1:
                    logger.warning(f"Condition function '{condition_name}' doesn't accept state parameter")
            except Exception as sig_error:
                logger.warning(f"Couldn't inspect condition function: {str(sig_error)}")
            
            # Convert END strings to constants
            routes_with_constants = {}
            for key, target in routes.items():
                if target == "END":
                    routes_with_constants[key] = END
                else:
                    routes_with_constants[key] = target
            
            # Add to StateGraph
            try:
                logger.debug(f"Adding conditional edges to StateGraph from: {from_node}")
                self.graph_builder.add_conditional_edges(
                    from_node,
                    condition,
                    routes_with_constants
                )
                logger.debug("Successfully added conditional edges to StateGraph")
            except Exception as sg_error:
                self._log_error(f"Error adding conditional edges from {from_node} to StateGraph", sg_error)
                
                # Enhanced error analysis
                if "not in graph" in str(sg_error):
                    logger.error(f"Node '{from_node}' is not in the graph")
                    logger.error("Add the source node first with add_node()")
                elif "callable" in str(sg_error):
                    logger.error("Condition must be a callable function")
                    logger.error(f"Got {type(condition).__name__} instead")
                
                raise ValueError(f"Failed to add conditional edges: {str(sg_error)}") from sg_error
            
            # Store branch info for debugging
            self.branches.append({
                "source": from_node,
                "condition": condition,
                "condition_name": condition_name,
                "routes": routes,
                "created_at": datetime.now()
            })
            
            # Add edges with special formatting for conditional edges
            for key, target in routes.items():
                target_str = str(target) if target != END else "END"
                
                self.edges.append(
                    DynamicGraphEdge(
                        source=from_node,
                        target=target_str,
                        condition=condition,
                        metadata={
                            "condition_key": key,
                            "condition_name": condition_name
                        }
                    )
                )
                
                # Update node statuses
                if from_node in self.nodes:
                    self.node_statuses[from_node] = NodeStatus.CONNECTED
                
                if target != "END" and target != END and target in self.nodes:
                    self.node_statuses[target] = NodeStatus.CONNECTED
            
            logger.info(f"Added conditional edges from: {from_node} using '{condition_name}'")
            
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error adding conditional edges from {from_node}: {str(e)}\n{tb}")
            self._log_error(f"Error adding conditional edges from {from_node}", e)
            raise
    
    def set_entry_point(self, node_name: str) -> 'DynamicGraph':
        """
        Set the entry point for the graph.
        
        Args:
            node_name: Name of the node to set as entry point
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug(f"Setting entry point to: {node_name}")
            
            # Validate node exists
            if node_name not in self.nodes:
                logger.warning(f"Entry point node '{node_name}' doesn't exist yet")
            
            # Check for existing START edges
            existing_start_edges = []
            for edge in self.edges:
                if edge.source in ["START", "__start__", str(START)]:
                    existing_start_edges.append(edge)
            
            # Log warning if overriding existing entry points
            if existing_start_edges:
                target_list = ", ".join(edge.target for edge in existing_start_edges)
                logger.warning(f"Overriding existing entry point(s): {target_list}")
            
            # Add edge from START to the node
            self.add_edge(START, node_name)
            
            logger.info(f"Set entry point to: {node_name}")
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error setting entry point to {node_name}: {str(e)}\n{tb}")
            self._log_error(f"Error setting entry point to {node_name}", e)
            raise
    
    def apply_pattern(self, pattern_name: str, **kwargs) -> 'DynamicGraph':
        """
        Apply a registered workflow pattern to the graph.
        
        This method applies a pre-defined workflow pattern from the pattern registry,
        with support for customizing nodes created by the pattern. Patterns provide
        reusable graph structures that can be applied consistently across different graphs.
        
        Args:
            pattern_name: Name of the pattern to apply
            **kwargs: Pattern-specific parameters and customization options
            
        Returns:
            Self for chaining
        """
        try:
            # Import pattern registry
            from haive.core.graph.patterns.registry import GraphPatternRegistry

            # Get pattern registry and ensure registry is initialized
            registry = GraphPatternRegistry.get_instance()
            
            # Log pattern application
            logger.info(f"Applying pattern: {pattern_name}")
            
            # Extract node configuration options
            node_configs = {}
            pattern_kwargs = kwargs.copy()
            
            # Extract node_configs if provided
            if "node_configs" in pattern_kwargs:
                node_configs = pattern_kwargs.pop("node_configs")
                logger.debug(f"Found node configs for: {', '.join(node_configs.keys())}")
            
            # Get the pattern from registry
            pattern = registry.get_pattern(pattern_name)
            if not pattern:
                logger.warning(f"Pattern not found: {pattern_name}")
                # List available patterns as a suggestion
                try:
                    available_patterns = registry.list_patterns()
                    if available_patterns:
                        logger.warning(f"Available patterns: {', '.join(available_patterns)}")
                except Exception as e:
                    logger.debug(f"Error listing patterns: {e}")
                
                # Exit early but don't raise exception
                return self
            
            # Track state before applying pattern for change detection
            initial_state = {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "branch_count": len(self.branches)
            }
            
            # Check compatibility between pattern and available components
            if hasattr(pattern, "check_compatibility"):
                compatibility_result = pattern.check_compatibility(self, **pattern_kwargs)
                if not compatibility_result.get("compatible", True):
                    warnings = compatibility_result.get("warnings", [])
                    for warning in warnings:
                        logger.warning(f"Compatibility issue: {warning}")
                    
                    # Check if we should continue despite warnings
                    if not kwargs.get("force", False) and not compatibility_result.get("continue", True):
                        logger.warning(f"Pattern {pattern_name} is not compatible with this graph")
                        return self
            
            # Apply the pattern with node configuration options
            try:
                # Try newer pattern application method with node configs
                if hasattr(pattern, "apply_with_configs"):
                    logger.debug("Using apply_with_configs pattern method")
                    result = pattern.apply_with_configs(self, node_configs=node_configs, **pattern_kwargs)
                # Try integration method
                elif hasattr(pattern, "apply_to_graph"):
                    logger.debug("Using apply_to_graph pattern method")
                    result = pattern.apply_to_graph(self, node_configs=node_configs, **pattern_kwargs)
                # Fallback to basic apply method
                else:
                    logger.debug("Using standard apply pattern method")
                    # Add node_configs back as a parameter for newer patterns that might use it
                    pattern_kwargs["node_configs"] = node_configs
                    result = pattern.apply(self, **pattern_kwargs)
            except Exception as e:
                self._log_error(f"Error applying pattern {pattern_name}", e)
                raise ValueError(f"Failed to apply pattern {pattern_name}: {str(e)}") from e
            
            # Track changes for detailed logging
            changes = {
                "new_nodes": len(self.nodes) - initial_state["node_count"],
                "new_edges": len(self.edges) - initial_state["edge_count"],
                "new_branches": len(self.branches) - initial_state["branch_count"]
            }
            
            # Track applied pattern in history
            if pattern_name not in self.applied_patterns:
                pattern_entry = {
                    "name": pattern_name,
                    "timestamp": datetime.now().isoformat(),
                    "parameters": {k: v for k, v in pattern_kwargs.items() 
                                if not isinstance(v, (Callable, type))},
                    "changes": changes
                }
                self.applied_patterns.append(pattern_name)
                
                # Store detailed pattern application in metadata if available
                if "pattern_applications" not in self.metadata:
                    self.metadata["pattern_applications"] = []
                self.metadata["pattern_applications"].append(pattern_entry)
            
            # Log pattern application results
            logger.info(f"Applied pattern '{pattern_name}'")
            if changes["new_nodes"] > 0:
                logger.info(f"Added {changes['new_nodes']} nodes")
            if changes["new_edges"] > 0:
                logger.info(f"Added {changes['new_edges']} edges")
            if changes["new_branches"] > 0:
                logger.info(f"Added {changes['new_branches']} conditional branches")
            
            # Apply any post-pattern hooks if defined
            if hasattr(pattern, "post_apply") and callable(pattern.post_apply):
                try:
                    pattern.post_apply(self, result, **pattern_kwargs)
                except Exception as e:
                    logger.warning(f"Error in post-apply hook: {e}")
            
            # Return self for method chaining
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error applying pattern {pattern_name}: {str(e)}\n{tb}")
            
            # Enhanced error analysis
            if "has no attribute 'apply'" in str(e):
                logger.error("Pattern doesn't have required method")
                logger.error("Verify pattern implementation")
            elif "TypeError" in str(e) and "unexpected keyword argument" in str(e):
                import re
                param_match = re.search(r"unexpected keyword argument '(.*?)'", str(e))
                if param_match:
                    invalid_param = param_match.group(1)
                    logger.error(f"Invalid parameter: '{invalid_param}'")
                    logger.error("Check pattern documentation for supported parameters")
            
            # Re-raise with context for proper error tracking
            raise ValueError(f"Failed to apply pattern '{pattern_name}': {str(e)}") from e
    
    def debug_node(self, node_name: str, enable: bool = True) -> 'DynamicGraph':
        """
        Enable or disable debugging for a specific node.
        
        Args:
            node_name: Name of the node to debug
            enable: Whether to enable or disable debugging
            
        Returns:
            Self for chaining
        """
        try:
            logger.debug(f"{'Enabling' if enable else 'Disabling'} debug for node: {node_name}")
            
            if node_name in self.nodes:
                node_config = self.nodes[node_name]
                if isinstance(node_config, NodeConfig):
                    # Set debug flag
                    node_config.debug = enable
                    
                    # Re-create node function
                    node_function = NodeFactory.create_node_function(node_config)
                    
                    # Replace in graph
                    self.graph_builder.add_node(node_name, node_function)
                    
                    logger.info(f"{'Enabled' if enable else 'Disabled'} debugging for node: {node_name}")
                else:
                    logger.warning(f"Node {node_name} does not have a NodeConfig")
            else:
                logger.warning(f"Node {node_name} not found")
                
            return self
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error {'enabling' if enable else 'disabling'} debug for node {node_name}: {str(e)}\n{tb}")
            self._log_error(f"Error changing debug state for node {node_name}", e)
            raise
    
    def validate_node_config(self, node_name: str) -> Dict[str, Any]:
        """
        Validate a node configuration and provide detailed diagnostic information.
        
        Args:
            node_name: Name of the node to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            logger.debug(f"Validating node configuration: {node_name}")
            
            if node_name not in self.nodes:
                logger.warning(f"Node {node_name} not found")
                return {"valid": False, "error": "Node not found"}
            
            node_config = self.nodes[node_name]
            
            # Check if it's a NodeConfig
            if not isinstance(node_config, NodeConfig):
                logger.warning(f"Node {node_name} does not have a NodeConfig")
                return {"valid": False, "error": "Not a NodeConfig", "type": type(node_config).__name__}
            
            # Check engine reference
            engine, engine_id = node_config.resolve_engine()
            
            results = {
                "valid": True,
                "node_name": node_name,
                "node_type": node_config.determine_node_type(),
                "engine_type": str(getattr(engine, "engine_type", "unknown")),
                "engine_id": engine_id,
                "command_goto": str(node_config.command_goto) if node_config.command_goto else None,
                "status": self.node_statuses.get(node_name, NodeStatus.ADDED).value,
                "input_mapping": node_config.input_mapping,
                "output_mapping": node_config.output_mapping,
                "debug": node_config.debug
            }
            
            # Test node creation 
            try:
                node_function = NodeFactory.create_node_function(node_config)
                results["node_function"] = "created"
                results["node_function_type"] = type(node_function).__name__
            except Exception as e:
                results["valid"] = False
                results["error"] = f"Failed to create node function: {str(e)}"
            
            logger.debug(f"Node validation results: {results}")
            return results
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error validating node {node_name}: {str(e)}\n{tb}")
            return {"valid": False, "error": str(e), "traceback": tb}
    
    def _validate_graph(self) -> List[str]:
        """
        Perform validation of graph structure before compilation.
        
        Returns:
            List of validation issues found
        """
        try:
            logger.info("Validating graph structure...")
            
            validation_issues = []
            
            # 1. Check for START edges
            start_edges = []
            for edge in self.edges:
                if edge.source in ["START", "__start__", str(START)]:
                    start_edges.append(edge)
            
            if not start_edges:
                warning_msg = "Graph has no START edges - compilation will likely fail"
                logger.warning(warning_msg)
                validation_issues.append(warning_msg)
                
                # Try to suggest a fix
                if len(self.nodes) > 0:
                    first_node = next(iter(self.nodes.keys()))
                    suggestion = f"Add entry point with 'graph.add_edge(START, \"{first_node}\")'"
                    logger.warning(f"Suggestion: {suggestion}")
            else:
                logger.info(f"Found {len(start_edges)} START edge(s)")
            
            # 2. Check for unreachable nodes
            reachable_nodes = set()
            
            # Start with nodes directly connected to START
            for edge in self.edges:
                if edge.source in ["START", "__start__", str(START)]:
                    reachable_nodes.add(edge.target)
            
            # Iteratively add nodes reachable from current set until no more are found
            new_nodes_found = True
            iteration = 0
            max_iterations = 100  # Prevent infinite loop
            
            while new_nodes_found and iteration < max_iterations:
                iteration += 1
                new_nodes_found = False
                
                for edge in self.edges:
                    if edge.source in reachable_nodes and edge.target not in ["END", "__end__", str(END)]:
                        if edge.target not in reachable_nodes:
                            reachable_nodes.add(edge.target)
                            new_nodes_found = True
            
            # Find unreachable nodes
            unreachable_nodes = set(self.nodes.keys()) - reachable_nodes
            if unreachable_nodes:
                warning_msg = f"Found {len(unreachable_nodes)} unreachable node(s)"
                logger.warning(warning_msg)
                validation_issues.append(warning_msg)
                
                # Show the list of unreachable nodes
                logger.warning(f"Unreachable nodes: {', '.join(unreachable_nodes)}")
                
                # Try to suggest a fix
                for node in unreachable_nodes:
                    # Update node status for visualization
                    self.node_statuses[node] = NodeStatus.UNREACHABLE
            else:
                logger.info("All nodes are reachable from START")
            
            return validation_issues
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error validating graph: {str(e)}\n{tb}")
            validation_issues.append(f"Validation error: {str(e)}")
            return validation_issues
    
    def build(self, checkpointer=None, **kwargs) -> Any:
        """
        Build the graph (not compiled) with validation.
        
        Args:
            checkpointer: Optional checkpointer for state persistence
            **kwargs: Additional build parameters
            
        Returns:
            Built but not compiled graph
        """
        try:
            logger.info(f"Building graph: {self.name}")
            
            # Run validation before building
            validation_issues = self._validate_graph()
            
            # Log build statistics
            logger.info(f"Built graph: {self.name}")
            logger.info(f"Nodes: {len(self.nodes)}")
            logger.info(f"Edges: {len(self.edges)}")
            logger.info(f"Branches: {len(self.branches)}")
            
            if validation_issues:
                logger.warning(f"{len(validation_issues)} validation issues detected")
            
            # Return built graph
            return self.graph_builder
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error building graph: {str(e)}\n{tb}")
            
            # Enhanced error analysis
            self._analyze_build_error(e)
            
            raise ValueError(f"Failed to build graph: {str(e)}") from e
    
    def _analyze_build_error(self, error: Exception) -> None:
        """Analyze build error and provide diagnostic information."""
        try:
            error_str = str(error)
            
            # Check for common build errors
            if "Graph must have an entrypoint" in error_str:
                logger.error("Graph is missing an entry point (START edge)")
                logger.error("Add at least one edge from START to a node")
                
                # Suggest a fix if possible
                if self.nodes:
                    first_node = next(iter(self.nodes.keys()))
                    logger.error(f"Try adding: graph.add_edge(START, \"{first_node}\")")
            elif "No transitions defined" in error_str:
                logger.error("Graph has no transitions (edges) defined")
                logger.error("Add edges between nodes")
            elif "Node" in error_str and "is not in graph" in error_str:
                # Extract node name if possible
                import re
                node_match = re.search(r"Node ['\"](.*?)['\"] is not in graph", error_str)
                if node_match:
                    node_name = node_match.group(1)
                    logger.error(f"Node '{node_name}' referenced in edges but not added to graph")
                    logger.error("Add this node first with graph.add_node()")
        except Exception as e:
            logger.error(f"Error analyzing build error: {str(e)}")
    
    
    
    def _analyze_compilation_error(self, error: Exception) -> None:
        """
        Analyze compilation error and provide targeted debugging guidance.
        
        Args:
            error: The exception that occurred
        """
        try:
            error_str = str(error)
            
            # Format issue header
            logger.error("COMPILATION DIAGNOSTIC")
            
            # Handle specific known error patterns with enhanced diagnosis
            if "Graph must have an entrypoint" in error_str:
                logger.error("CRITICAL: Graph is missing an entry point (START edge)")
                logger.error("SOLUTION: Add at least one edge from START to a node:")
                
                if self.nodes:
                    first_node = next(iter(self.nodes.keys()))
                    logger.error(f"    graph.add_edge(START, \"{first_node}\")")
                    
                    # Suggest entry point
                    logger.error(f"SUGGESTION: Consider using '{first_node}' as entry point")
                else:
                    logger.error("    No nodes found. Add nodes before setting entry point.")
                    
            elif "Node" in error_str and "is unreachable" in error_str:
                # Extract node name from error message
                import re
                node_match = re.search(r"Node ['\"](.*?)['\"] is unreachable", error_str)
                if node_match:
                    unreachable_node = node_match.group(1)
                    logger.error(f"CRITICAL: Node '{unreachable_node}' is unreachable")
                    logger.error("SOLUTION: Ensure there is a path from START to this node:")
                    
                    # Attempt to find closest connected node to suggest a fix
                    connected_nodes = set()
                    for edge in self.edges:
                        if edge.source in ["START", "__start__", str(START)]:
                            connected_nodes.add(edge.target)
                    
                    if connected_nodes:
                        closest_node = next(iter(connected_nodes))
                        logger.error(f"    graph.add_edge(\"{closest_node}\", \"{unreachable_node}\")")
                        logger.error(f"SUGGESTION: Consider connecting '{unreachable_node}' to '{closest_node}'")
                    else:
                        logger.error(f"    graph.add_edge(START, \"{unreachable_node}\")")
                else:
                    logger.error("CRITICAL: Some node is unreachable")
            
            # General advice
            logger.error("GENERAL DEBUGGING STEPS")
            #logger.
        except Exception as e:
            logger.error(f"Error analyzing compilation error: {str(e)}")
            tb = traceback.format_exc()
            logger.error(f"Traceback: {tb}")
            raise ValueError(f"Failed to analyze compilation error: {str(e)}") from e
        
    def visualize_graph(self, output_file=None, open_browser=False, include_legend=True, 
                    format="png", include_stats=True):
        """
        Visualize the graph using Mermaid diagrams.
        
        Args:
            output_file: Path to save the visualization (optional)
            open_browser: Whether to open the visualization in browser
            include_legend: Whether to include a legend 
            format: Output format ('html' or 'png')
            include_stats: Whether to include graph statistics
            
        Returns:
            Path to the generated file or None if visualization failed
        """
        try:
            # Generate timestamp-based filename if none provided
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = "graph_visualizations"
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f"{self.name.replace(' ', '_')}_{timestamp}.{format}")
            
            logger.info(f"Visualizing graph: {self.name}")
            
            # Check if we have a compiled graph
            if hasattr(self, "compiled_graph") and self.compiled_graph is not None:
                # Import the visualization utility
                from haive.core.utils.visualize_graph_utils import (
                    render_and_display_graph,
                )

                # Use the visualization utility
                result_file = render_and_display_graph(
                    compiled_graph=self.compiled_graph,
                    output_dir=os.path.dirname(output_file),
                    output_name=os.path.basename(output_file),
                    open_browser=open_browser,
                    include_legend=include_legend,
                    include_stats=include_stats,
                    format=format
                )
                
                logger.info(f"Graph visualization saved to: {result_file}")
                return result_file
            else:
                # Attempt to visualize uncompiled graph for development purposes
                logger.warning("Graph has not been compiled yet. Attempting to visualize uncompiled graph.")
                
                try:
                    # Try to use the uncompiled builder's visualization (experimental)
                    if hasattr(self.graph_builder, "get_graph"):
                        from haive.core.utils.visualize_graph_utils import (
                            render_uncompiled_graph,
                        )
                        
                        result_file = render_uncompiled_graph(
                            graph_builder=self.graph_builder,
                            nodes=self.nodes,
                            edges=self.edges,
                            output_file=output_file,
                            include_legend=include_legend
                        )
                        
                        if result_file:
                            logger.info(f"Uncompiled graph visualization saved to: {result_file}")
                            logger.warning("This is an experimental visualization of an uncompiled graph and may be incomplete.")
                            return result_file
                    
                    # If we couldn't visualize the uncompiled graph through utilities
                    logger.warning("Unable to visualize uncompiled graph. Please compile the graph first.")
                    return None
                    
                except Exception as e:
                    logger.warning(f"Failed to visualize uncompiled graph: {str(e)}")
                    logger.warning("Please compile the graph first for accurate visualization.")
                    return None
        
        except ImportError:
            logger.warning("Visualization utilities not available, falling back to basic visualization")
            
            # Fallback to basic visualization if available
            if hasattr(self, "compiled_graph") and self.compiled_graph is not None:
                try:
                    # Use the compiled graph's basic visualization capabilities
                    png_data = self.compiled_graph.get_graph(xray=True).draw_mermaid_png()
                    
                    # Save the PNG data to a file
                    with open(output_file, "wb") as f:
                        f.write(png_data)
                        
                    logger.info(f"Basic graph visualization saved to: {output_file}")
                    return output_file
                except Exception as e:
                    logger.warning(f"Error visualizing compiled graph: {str(e)}")
                    return None
            else:
                logger.warning("Graph has not been compiled and visualization utilities are not available")
                return None
                
        except Exception as e:
            logger.warning(f"Error visualizing graph: {str(e)}")
            return None
    def compile(self, checkpointer=None, **kwargs):
        """
        Build and compile the graph with validation and diagnostics.
        
        Args:
            checkpointer: Optional checkpointer for state persistence
            **kwargs: Additional compile parameters
            
        Returns:
            Compiled graph
        """
        try:
            logger.info(f"Compiling graph: {self.name}")
            
            # Perform pre-compilation checks
            validation_issues = self._validate_graph()
            
            # Log detailed pre-compilation state
            if self.debug_level in [DebugLevel.VERBOSE, DebugLevel.TRACE]:
                self.debug_graph()
            
            # Compilation banner
            logger.info("COMPILING GRAPH WORKFLOW")
            
            # Handle validation issues
            if validation_issues:
                logger.warning(f"Proceeding with compilation despite {len(validation_issues)} validation issues")
            
            # Compile the graph with detailed error trapping
            try:
                logger.debug(f"Starting compilation process with checkpointer: {checkpointer is not None}")
                compiled_graph = self.graph_builder.compile(checkpointer=checkpointer, **kwargs)
                
                # Store the compiled graph for future use
                self.compiled_graph = compiled_graph
                
                # Log success
                logger.info("COMPILATION SUCCESSFUL")
                logger.info(f"Compiled graph: {self.name}")
                logger.info(f"Nodes: {len(self.nodes)}")
                logger.info(f"Edges: {len(self.edges)}")
                logger.info(f"Branches: {len(self.branches)}")
                
                # Visualize if enabled
                if self.visualize and VISUALIZATION_AVAILABLE:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_dir = "graph_visualizations"
                    os.makedirs(output_dir, exist_ok=True)
                    output_file = os.path.join(output_dir, f"{self.name.replace(' ', '_')}_{timestamp}.png")
                    
                    try:
                        result_file = self.visualize_graph(
                            output_file=output_file, 
                            open_browser=False
                        )
                        if result_file:
                            logger.info(f"Graph visualization saved to: {result_file}")
                    except Exception as viz_error:
                        logger.warning(f"Error creating visualization: {str(viz_error)}")
                
                return compiled_graph
                
            except Exception as compile_error:
                # Detailed compile error handling
                self._log_error("Compilation error", compile_error)
                
                # Analyze the most common compilation issues with enhanced diagnostics
                self._analyze_compilation_error(compile_error)
                
                raise ValueError(f"Failed to compile graph: {str(compile_error)}") from compile_error
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Error during graph compilation process: {str(e)}\n{tb}")
            
            # Debug detailed graph state for troubleshooting
            logger.error("Graph state at compilation failure:")
            self.debug_graph()
            
            raise ValueError(f"Failed to compile graph: {str(e)}") from e
    def debug_graph(self) -> str:
        """
        Print comprehensive debug information about the graph state.
        
        This method displays a detailed overview of the current state
        of the DynamicGraph, including nodes, edges, connections, and potential issues.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"\n===== DEBUG GRAPH: {self.name} ({timestamp}) =====")
        
        # Basic info
        logger.debug(f"Graph ID: {self.id}")
        logger.debug(f"Name: {self.name}")
        logger.debug(f"Description: {self.description}")
        logger.debug(f"State Model: {getattr(self.state_model, '__name__', 'None')}")
        logger.debug(f"Debug Level: {self.debug_level}")
        
        # Components
        logger.debug(f"\n--- Components ({len(self.components)}) ---")
        for i, component in enumerate(self.components):
            component_name = getattr(component, '__name__', str(component))
            component_type = type(component).__name__
            logger.debug(f"  {i+1}. {component_name} ({component_type})")
        
        # Registered engines
        logger.debug(f"\n--- Registered Engines ({len(self.engines)}) ---")
        for name, engine_id in self.engines.items():
            if engine_id in self.engine_objects:
                engine_type = type(self.engine_objects[engine_id]).__name__
                logger.debug(f"  {name} (ID: {engine_id}, Type: {engine_type})")
        
        # Nodes
        logger.debug(f"\n--- Nodes ({len(self.nodes)}) ---")
        node_status = {}
        for name, node_config in self.nodes.items():
            # Determine node status
            has_incoming = any(edge.target == name for edge in self.edges if edge.source != "START")
            has_outgoing = any(edge.source == name for edge in self.edges)
            
            if not has_incoming and name != self.entry_point:
                status = NodeStatus.UNREACHABLE
            elif not has_outgoing and node_config.command_goto != "END":
                status = NodeStatus.DEAD_END
            else:
                status = NodeStatus.CONNECTED
                
            node_status[name] = status
            
            # Get node details
            node_type = node_config.type
            engine_name = node_config.engine or 'None'
            engine_type = 'N/A'
            if engine_name in self.engines and self.engines[engine_name] in self.engine_objects:
                engine_type = type(self.engine_objects[self.engines[engine_name]]).__name__
            
            goto_str = node_config.command_goto or 'None'
            
            logger.debug(f"  {name} ({status.value}):")
            logger.debug(f"    Type: {node_type}")
            logger.debug(f"    Engine: {engine_name} ({engine_type})")
            logger.debug(f"    Command Goto: {goto_str}")
            
            # Log mappings if they exist
            if node_config.input_mapping:
                logger.debug(f"    Input Mapping: {node_config.input_mapping}")
            if node_config.output_mapping:
                logger.debug(f"    Output Mapping: {node_config.output_mapping}")
        
        # Edges
        logger.debug(f"\n--- Edges ({len(self.edges)}) ---")
        
        # Group edges by source
        edges_by_source = {}
        for edge in self.edges:
            if edge.source not in edges_by_source:
                edges_by_source[edge.source] = []
            edges_by_source[edge.source].append(edge)
        
        # Log edges organized by source
        for source, edges in sorted(edges_by_source.items()):
            logger.debug(f"  From {source}:")
            for edge in edges:
                target = edge.target
                condition_name = edge.condition_name
                if condition_name:
                    logger.debug(f"    → {target} [conditional: {condition_name}]")
                else:
                    logger.debug(f"    → {target}")
        
        # Check for START edges
        start_edges = [e for e in self.edges if e.source == "START"]
        if not start_edges:
            logger.debug("\nWARNING: No START edges found - this will cause compilation failure")
        else:
            logger.debug(f"\nFound {len(start_edges)} START edge(s)")
        
        # Check for END edges
        end_edges = [e for e in self.edges if e.target == "END"]
        end_goto_nodes = [n for n, cfg in self.nodes.items() if cfg.command_goto == "END"]
        if not end_edges and not end_goto_nodes:
            logger.debug("\nWARNING: No END edges found - graph may loop indefinitely")
        else:
            logger.debug(f"\nFound {len(end_edges)} END edge(s):")
            for edge in end_edges:
                logger.debug(f"  {edge.source} → END")
                
        # List nodes with command_goto=END
        if end_goto_nodes:
            logger.debug(f"\nNodes with command_goto=END: {len(end_goto_nodes)}")
            for node in end_goto_nodes:
                logger.debug(f"  {node}")
        
        # Analyze graph connectivity
        all_node_names = set(self.nodes.keys())
        entry_nodes = set()
        
        # Add entry point
        if self.entry_point:
            entry_nodes.add(self.entry_point)
            
        # Add targets of START edges
        for edge in self.edges:
            if edge.source == "START":
                entry_nodes.add(edge.target)
        
        # Find reachable nodes
        reachable = set()
        to_visit = list(entry_nodes)
        
        while to_visit:
            current = to_visit.pop()
            if current in reachable:
                continue
            reachable.add(current)
            
            # Add all targets of edges from current node
            for edge in self.edges:
                if edge.source == current and edge.target != "END":
                    if edge.target not in reachable:
                        to_visit.append(edge.target)
                        
        # Find unreachable nodes
        unreachable_nodes = all_node_names - reachable
        if unreachable_nodes:
            logger.debug(f"\nWARNING: Found {len(unreachable_nodes)} unreachable node(s):")
            for node in sorted(unreachable_nodes):
                logger.debug(f"  {node}")
        
        # Errors
        if self.errors:
            logger.debug(f"\n--- Errors ({len(self.errors)}) ---")
            for i, error in enumerate(self.errors):
                logger.debug(f"  {i+1}. {error.split('\n')[0]}")
        
        # Compilation status
        compiled = hasattr(self, '_compiled_graph') and self._compiled_graph is not None
        logger.debug(f"\nCompilation Status: {'COMPILED' if compiled else 'NOT COMPILED'}")
        
        # Optionally generate visualization
        if self.visualize:
            try:
                # Generate unique filename
                timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"debug_graph_{self.name}_{timestamp_file}.html"
                
                logger.debug(f"\nGenerating debug visualization: {output_file}")
                
                # Use existing visualization method
                if hasattr(self, 'visualize_graph'):
                    self.visualize_graph(output_file=output_file)
                    logger.debug(f"Debug visualization saved to: {output_file}")
            except Exception as viz_error:
                logger.debug(f"Visualization error: {str(viz_error)}")
        
        logger.debug("\n===== END DEBUG GRAPH =====\n")
        
    