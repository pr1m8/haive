"""
Models for the Haive Registry System.

This module defines the core models used by the registry system to represent
different types of entities, configurations, dependencies, etc.
"""

import uuid
from enum import Enum, auto
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    """Types of entities that can be registered."""
    AGENT = "agent"
    TOOL = "tool"
    TOOLKIT = "toolkit"
    ENGINE = "engine"
    GAME = "game"
    LLM_MODEL = "llm_model"
    LLM_PROVIDER = "llm_provider"


class ConfigType(str, Enum):
    """Types of configurations."""
    STATE_SCHEMA = "state_schema"
    INPUT_SCHEMA = "input_schema"
    OUTPUT_SCHEMA = "output_schema"
    ENGINE = "engine"
    PROMPT = "prompt"
    NODE = "node"
    GRAPH = "graph"


class DependencyType(str, Enum):
    """Types of dependencies between entities."""
    REQUIRES = "requires"  # Hard dependency
    USES = "uses"          # Soft dependency
    EXTENDS = "extends"    # Extension relationship


class ImportStatus(str, Enum):
    """Import operation status."""
    SUCCESS = "success"
    FAILURE = "failure"


class RegistryItem(BaseModel):
    """Base model for registry items."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: EntityType
    description: Optional[str] = None
    module_path: Optional[str] = None
    class_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Configuration(BaseModel):
    """Configuration for a registry item."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    registry_id: str
    config_type: ConfigType
    config_data: Dict[str, Any]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GraphDefinition(BaseModel):
    """Graph definition for a registry item."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    registry_id: str
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Dependency(BaseModel):
    """Dependency between registry items."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    registry_id: str
    dependent_id: str
    dependency_type: DependencyType
    created_at: Optional[datetime] = None


class EnvironmentVar(BaseModel):
    """Environment variable requirement for a registry item."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    registry_id: str
    env_name: str
    is_required: bool = False
    default_value: Optional[str] = None
    created_at: Optional[datetime] = None


class ImportLogItem(BaseModel):
    """Log entry for import operations."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    import_session: str
    entity_name: str
    entity_type: str
    status: ImportStatus
    message: Optional[str] = None
    traceback: Optional[str] = None
    created_at: Optional[datetime] = None