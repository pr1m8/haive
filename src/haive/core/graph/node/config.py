"""
Node configuration with simplified schema integration.

This module provides a streamlined NodeConfig class that supports StateSchema,
proper Command/Send typing, and engine integration.
"""

import logging
from typing import Any, Callable, Dict, List, Literal, Optional, Set, Tuple, Type, Union

from langgraph.graph import END
from langgraph.types import Command, Send
from pydantic import BaseModel, Field, model_validator

from haive.core.engine.base import Engine
from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)


class NodeConfig(BaseModel):
    """
    Configuration for a node in a graph with schema integration.
    
    NodeConfig provides a standardized way to configure nodes with proper typing
    for Command/Send, StateSchema support, and registry integration.
    """
    
    # Basic node configuration
    name: str = Field(description="Name of the node")
    engine: Optional[Union[Engine, str, Callable]] = Field(
        default=None,
        description="Engine, engine name, or callable function for this node",
    )
    
    # Type information
    node_type: Optional[str] = Field(
        default=None, 
        description="Type of node (auto-detected if None)"
    )
    is_async: bool = Field(
        default=False,
        description="Whether the node is asynchronous"
    )
    
    # Control flow configuration with proper Command/Send typing
    command_goto: Optional[Union[str, Literal["END"], Command, Send, List[Send]]] = Field(
        default=None,
        description="Next node to go to after this node"
    )
    
    # Schema integration
    input_mapping: Optional[Dict[str, str]] = Field(
        default=None, 
        description="Mapping from state keys to engine input keys"
    )
    output_mapping: Optional[Dict[str, str]] = Field(
        default=None, 
        description="Mapping from engine output keys to state keys"
    )
    preserve_schema: bool = Field(
        default=True,
        description="Preserve StateSchema instances instead of converting to dict"
    )
    
    # Engine configuration
    engine_id: Optional[str] = Field(
        default=None,
        description="Unique ID of the engine instance"
    )
    runnable_config: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Runtime configuration for this node"
    )
    
    # Additional settings
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata for this node"
    )
    registry: Optional[Any] = Field(
        default=None, 
        exclude=True,
        description="Registry reference for engine lookup"
    )
    
    # Required field to enable arbitrary_types
    model_config = {"arbitrary_types_allowed": True}
    
    @model_validator(mode="after")
    def validate_config(self):
        """Validate and normalize the configuration."""
        # Convert "END" string to END constant
        if self.command_goto == "END":
            self.command_goto = END
        
        # Auto-detect node type if not provided
        if self.node_type is None:
            self.node_type = self._determine_node_type()
        
        # Auto-detect async mode if not explicitly set
        if hasattr(self.engine, "ainvoke") and callable(getattr(self.engine, "ainvoke")):
            self.is_async = True
        elif callable(self.engine):
            import asyncio
            self.is_async = asyncio.iscoroutinefunction(self.engine)
            
        return self
    
    def _determine_node_type(self) -> str:
        """Determine the most appropriate node type based on engine."""
        engine = self.engine
        
        # Handle Engine instances
        if isinstance(engine, Engine):
            if hasattr(engine, "engine_type"):
                engine_type = getattr(engine, "engine_type")
                if engine_type:
                    return f"{engine_type.value}_engine"
            return "engine"
            
        # Handle callable functions
        if callable(engine):
            import asyncio
            if asyncio.iscoroutinefunction(engine):
                return "async_callable"
            return "callable"
            
        # Handle string references
        if isinstance(engine, str):
            return "engine_ref"
            
        # Default type
        return "generic"
    
    def resolve_engine(self) -> Tuple[Any, Optional[str]]:
        """
        Resolve engine reference to actual engine and its ID.
        
        Returns:
            Tuple of (resolved engine, engine_id)
        """
        # Already resolved to a non-string 
        if not isinstance(self.engine, str):
            engine_id = None
            # Extract engine ID if possible
            if isinstance(self.engine, Engine) and hasattr(self.engine, "id"):
                engine_id = self.engine.id
                self.engine_id = engine_id
            
            return self.engine, engine_id
        
        # Try to lookup in registry
        engine_name = self.engine
        
        if self.registry is None:
            # Try to import from haive.core if possible
            try:
                from haive.core.engine.base import EngineRegistry
                registry = EngineRegistry.get_instance()
                logger.debug("Using global EngineRegistry")
            except ImportError:
                logger.warning("No registry available for engine lookup")
                return self.engine, None
        else:
            registry = self.registry
        
        # Try to find engine by name or ID
        engine = registry.find_by_id(engine_name) if hasattr(registry, "find_by_id") else None
        
        if engine:
            # Update engine reference
            self.engine = engine
            
            # Extract engine ID if available
            engine_id = None
            if hasattr(engine, "id"):
                engine_id = engine.id
                self.engine_id = engine_id
                
            return engine, engine_id
        
        # Try other lookup methods
        engine = registry.find(engine_name) if hasattr(registry, "find") else None
        if engine:
            self.engine = engine
            self.engine_id = getattr(engine, "id", None)
            
            return engine, self.engine_id
        
        # Not found
        logger.warning(f"Engine '{engine_name}' not found in registry")
        return self.engine, None