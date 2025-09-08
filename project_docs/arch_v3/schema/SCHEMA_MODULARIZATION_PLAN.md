# Schema Modularization Implementation Plan

**Domain**: Schema Separation  
**Estimated Days**: 6-7 days  
**Target LOC**: 4,000 LOC (from 6,000 LOC - 33% reduction)  
**Dependencies**: [Contracts](../contracts/PROTOCOL_CONTRACTS_PLAN.md)

## 🎯 Overview

Separate mixed state, configuration, and message schemas into focused, domain-specific modules with clear composition patterns. This enables better type safety, reusability, and maintainability across the entire architecture.

## 📊 Current State Analysis

### The Schema Mixing Problem

```bash
# Current schema structure (6,000 total LOC)
packages/haive-core/src/haive/core/schema/
├── base/
│   ├── base_schema.py                 # 800 LOC - Mixed base classes
│   └── state_schema.py                # 600 LOC - Generic state
├── prebuilt/
│   ├── messages_state.py              # 900 LOC - Message + state mixed
│   ├── meta_state.py                  # 1,200 LOC - Meta state + config
│   ├── agent_state.py                 # 700 LOC - Agent state + config
│   └── workflow_state.py              # 500 LOC - Workflow state
├── config/
│   ├── agent_config.py                # 600 LOC - Agent config + validation
│   ├── engine_config.py               # 400 LOC - Engine config + state
│   └── tool_config.py                 # 300 LOC - Tool config + metadata
└── validation/
    ├── schema_validator.py            # 500 LOC - Validation + schema logic
    └── field_validators.py            # 400 LOC - Field validation + config
```

### Key Problems Identified

1. **Mixed Concerns**: State, config, and validation logic all together
2. **Circular Dependencies**: Schema modules importing each other
3. **Type Confusion**: Same types used for different purposes
4. **Poor Reusability**: Can't use schema components independently
5. **No Composition**: Difficult to build complex schemas from simple ones

### Schema Responsibility Matrix

| Current Schema | State Management | Configuration | Message Handling | Validation |
| -------------- | ---------------- | ------------- | ---------------- | ---------- |
| MessagesState  | ✅               | ❌            | ✅               | ✅         |
| MetaState      | ✅               | ✅            | ❌               | ✅         |
| AgentState     | ✅               | ✅            | ✅               | ✅         |
| WorkflowState  | ✅               | ❌            | ❌               | ✅         |

**Problem**: Every schema tries to handle everything.

## 🏗️ Target Architecture

### Separated Schema Structure (4,000 total LOC)

```
packages/haive-core/src/haive/core/schema/
├── __init__.py                        # Schema exports (100 LOC)
├── state/                             # State schemas only
│   ├── __init__.py                   # State exports (30 LOC)
│   ├── base_state.py                 # Core state pattern (200 LOC)
│   ├── message_state.py              # Message state (150 LOC)
│   ├── agent_state.py                # Agent state (200 LOC)
│   ├── workflow_state.py             # Workflow state (150 LOC)
│   └── meta_state.py                 # Meta state pattern (250 LOC)
├── config/                           # Configuration schemas only
│   ├── __init__.py                   # Config exports (30 LOC)
│   ├── base_config.py                # Core config pattern (150 LOC)
│   ├── engine_config.py              # Engine configuration (200 LOC)
│   ├── agent_config.py               # Agent configuration (180 LOC)
│   ├── tool_config.py                # Tool configuration (120 LOC)
│   └── workflow_config.py            # Workflow configuration (100 LOC)
├── message/                          # Message schemas only
│   ├── __init__.py                   # Message exports (30 LOC)
│   ├── base_message.py               # Core message pattern (150 LOC)
│   ├── conversation.py               # Conversation messages (200 LOC)
│   ├── tool_message.py               # Tool messages (100 LOC)
│   └── system_message.py             # System messages (80 LOC)
├── composition/                      # Schema composition tools
│   ├── __init__.py                   # Composition exports (30 LOC)
│   ├── state_composer.py             # State composition (250 LOC)
│   ├── config_composer.py            # Config composition (200 LOC)
│   ├── schema_merger.py              # Schema merging (150 LOC)
│   └── field_mapper.py               # Field mapping (100 LOC)
├── validation/                       # Pure validation logic
│   ├── __init__.py                   # Validation exports (30 LOC)
│   ├── validators.py                 # Core validators (300 LOC)
│   ├── rules.py                      # Validation rules (200 LOC)
│   └── decorators.py                 # Validation decorators (100 LOC)
└── types/                           # Shared type definitions
    ├── __init__.py                   # Type exports (30 LOC)
    ├── primitives.py                 # Basic types (100 LOC)
    ├── enums.py                      # Enum definitions (150 LOC)
    └── unions.py                     # Union types (100 LOC)
```

**Total**: 20 focused files, ~4,000 LOC (33% reduction)

## 📋 Detailed Implementation Steps

### Step 1: Core Type Definitions (Day 1)

#### 1.1 Primitive Types

**File**: `types/primitives.py`

```python
from typing import Dict, List, Any, Optional, Union
from typing_extensions import TypedDict, Literal
from pydantic import Field
from datetime import datetime

# Basic type aliases
AgentId = str
MessageId = str
WorkflowId = str
ExecutionId = str
ToolId = str

# Common field types
Timestamp = datetime
Score = float  # 0.0 to 1.0
Duration = float  # seconds
TokenCount = int

# Metadata types
class BaseMetadata(TypedDict, total=False):
    """Base metadata structure."""
    created_at: Timestamp
    updated_at: Timestamp
    version: str
    tags: List[str]

class ExecutionMetadata(BaseMetadata, total=False):
    """Execution-specific metadata."""
    execution_id: ExecutionId
    start_time: Timestamp
    end_time: Optional[Timestamp]
    duration_ms: Optional[int]
    success: bool
    error: Optional[str]

class AgentMetadata(BaseMetadata, total=False):
    """Agent-specific metadata."""
    agent_id: AgentId
    agent_type: str
    capabilities: List[str]
    model: str
    temperature: float

# Common data structures
class KeyValuePair(TypedDict):
    """Generic key-value pair."""
    key: str
    value: Any

class NamedItem(TypedDict):
    """Item with name and optional description."""
    name: str
    description: Optional[str]

class ScoredItem(TypedDict):
    """Item with confidence score."""
    item: Any
    score: Score
    source: Optional[str]

# Validation types
ValidationResult = TypedDict('ValidationResult', {
    'valid': bool,
    'errors': List[str],
    'warnings': List[str]
})
```

#### 1.2 Enum Definitions

**File**: `types/enums.py`

```python
from enum import Enum

class MessageRole(str, Enum):
    """Message roles in conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class AgentType(str, Enum):
    """Types of agents."""
    SIMPLE = "simple"
    REACT = "react"
    RAG = "rag"
    PLANNING = "planning"
    MULTI = "multi"

class ExecutionStatus(str, Enum):
    """Execution status values."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowMode(str, Enum):
    """Workflow execution modes."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"

class ToolType(str, Enum):
    """Types of tools."""
    FUNCTION = "function"
    PYDANTIC = "pydantic"
    STRUCTURED = "structured"
    RETRIEVER = "retriever"

class StateScope(str, Enum):
    """Scope of state visibility."""
    PRIVATE = "private"    # Only accessible to owning component
    SHARED = "shared"      # Accessible to related components
    PUBLIC = "public"      # Accessible to all components

class ConfigCategory(str, Enum):
    """Configuration categories."""
    ENGINE = "engine"
    AGENT = "agent"
    WORKFLOW = "workflow"
    TOOL = "tool"
    VALIDATION = "validation"
```

### Step 2: Message Schemas (Day 2)

#### 2.1 Base Message Schema

**File**: `message/base_message.py`

```python
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..types.primitives import MessageId, Timestamp, BaseMetadata
from ..types.enums import MessageRole

class BaseMessage(BaseModel):
    """Base message schema for all message types."""

    # Core message fields
    id: MessageId = Field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole = Field(..., description="Message role")
    content: str = Field(..., description="Message content")

    # Optional fields
    name: Optional[str] = Field(default=None, description="Message sender name")
    timestamp: Timestamp = Field(default_factory=datetime.now)

    # Metadata
    metadata: BaseMetadata = Field(default_factory=dict, description="Message metadata")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        extra = "forbid"
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseMessage':
        """Create message from dictionary."""
        return cls.model_validate(data)

    def is_system_message(self) -> bool:
        """Check if this is a system message."""
        return self.role == MessageRole.SYSTEM

    def is_user_message(self) -> bool:
        """Check if this is a user message."""
        return self.role == MessageRole.USER

    def is_assistant_message(self) -> bool:
        """Check if this is an assistant message."""
        return self.role == MessageRole.ASSISTANT

    def is_tool_message(self) -> bool:
        """Check if this is a tool message."""
        return self.role == MessageRole.TOOL
```

#### 2.2 Conversation Messages

**File**: `message/conversation.py`

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .base_message import BaseMessage
from ..types.primitives import MessageId
from ..types.enums import MessageRole

class ConversationMessage(BaseMessage):
    """Enhanced message for conversations."""

    # Conversation-specific fields
    parent_id: Optional[MessageId] = Field(default=None, description="Parent message ID")
    thread_id: Optional[str] = Field(default=None, description="Thread identifier")

    # Response metadata
    response_time_ms: Optional[int] = Field(default=None, description="Response generation time")
    token_count: Optional[int] = Field(default=None, description="Token count")

    def create_response(self, content: str, **kwargs) -> 'ConversationMessage':
        """Create response message."""
        return ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=content,
            parent_id=self.id,
            thread_id=self.thread_id,
            **kwargs
        )

class SystemMessage(ConversationMessage):
    """System message with special handling."""

    role: MessageRole = Field(default=MessageRole.SYSTEM, frozen=True)
    priority: int = Field(default=0, description="System message priority")

    def __init__(self, content: str, **kwargs):
        super().__init__(role=MessageRole.SYSTEM, content=content, **kwargs)

class UserMessage(ConversationMessage):
    """User message with input metadata."""

    role: MessageRole = Field(default=MessageRole.USER, frozen=True)
    user_id: Optional[str] = Field(default=None, description="User identifier")

    def __init__(self, content: str, **kwargs):
        super().__init__(role=MessageRole.USER, content=content, **kwargs)

class AssistantMessage(ConversationMessage):
    """Assistant message with generation metadata."""

    role: MessageRole = Field(default=MessageRole.ASSISTANT, frozen=True)
    model: Optional[str] = Field(default=None, description="Model used for generation")
    finish_reason: Optional[str] = Field(default=None, description="Why generation stopped")

    def __init__(self, content: str, **kwargs):
        super().__init__(role=MessageRole.ASSISTANT, content=content, **kwargs)

class Conversation(BaseModel):
    """Collection of conversation messages."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = Field(default=None, description="Conversation title")
    messages: List[ConversationMessage] = Field(default_factory=list)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    participant_count: int = Field(default=2, description="Number of participants")

    def add_message(self, message: ConversationMessage) -> None:
        """Add message to conversation."""
        self.messages.append(message)
        self.updated_at = datetime.now()

    def add_user_message(self, content: str, **kwargs) -> UserMessage:
        """Add user message."""
        message = UserMessage(content=content, thread_id=self.id, **kwargs)
        self.add_message(message)
        return message

    def add_assistant_message(self, content: str, **kwargs) -> AssistantMessage:
        """Add assistant message."""
        message = AssistantMessage(content=content, thread_id=self.id, **kwargs)
        self.add_message(message)
        return message

    def get_messages_by_role(self, role: MessageRole) -> List[ConversationMessage]:
        """Get messages by role."""
        return [msg for msg in self.messages if msg.role == role]

    def get_recent_messages(self, count: int = 10) -> List[ConversationMessage]:
        """Get recent messages."""
        return self.messages[-count:]

    def to_langchain_format(self) -> List[Dict[str, str]]:
        """Convert to LangChain message format."""
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in self.messages
        ]
```

### Step 3: State Schemas (Day 3)

#### 3.1 Base State Schema

**File**: `state/base_state.py`

```python
from typing import Any, Dict, List, Optional, TypeVar
from pydantic import BaseModel, Field
from ..types.primitives import Timestamp, ExecutionId, BaseMetadata
from ..types.enums import StateScope
from datetime import datetime
import uuid

StateT = TypeVar('StateT', bound='BaseState')

class BaseState(BaseModel):
    """Base state schema for all stateful components."""

    # Core state identification
    state_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    component_name: str = Field(..., description="Name of owning component")
    component_type: str = Field(..., description="Type of owning component")

    # State lifecycle
    created_at: Timestamp = Field(default_factory=datetime.now)
    updated_at: Timestamp = Field(default_factory=datetime.now)
    version: int = Field(default=1, description="State version")

    # State scope and visibility
    scope: StateScope = Field(default=StateScope.PRIVATE, description="State visibility scope")

    # Core state data
    data: Dict[str, Any] = Field(default_factory=dict, description="Component state data")

    # Metadata and tracking
    metadata: BaseMetadata = Field(default_factory=dict, description="State metadata")
    execution_history: List[ExecutionId] = Field(default_factory=list, description="Execution history")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        extra = "forbid"
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def update_data(self, updates: Dict[str, Any]) -> None:
        """Update state data."""
        self.data.update(updates)
        self.updated_at = datetime.now()
        self.version += 1

    def get_data(self, key: str, default: Any = None) -> Any:
        """Get data by key."""
        return self.data.get(key, default)

    def set_data(self, key: str, value: Any) -> None:
        """Set data by key."""
        self.data[key] = value
        self.updated_at = datetime.now()
        self.version += 1

    def clear_data(self) -> None:
        """Clear all state data."""
        self.data.clear()
        self.updated_at = datetime.now()
        self.version += 1

    def add_execution(self, execution_id: ExecutionId) -> None:
        """Record execution in history."""
        self.execution_history.append(execution_id)
        self.updated_at = datetime.now()

    def create_snapshot(self) -> Dict[str, Any]:
        """Create immutable state snapshot."""
        return {
            "state_id": self.state_id,
            "component_name": self.component_name,
            "snapshot_time": datetime.now(),
            "version": self.version,
            "data": self.data.copy(),
            "metadata": self.metadata.copy()
        }

    def is_shared(self) -> bool:
        """Check if state is shared."""
        return self.scope in [StateScope.SHARED, StateScope.PUBLIC]

    def is_public(self) -> bool:
        """Check if state is public."""
        return self.scope == StateScope.PUBLIC
```

#### 3.2 Agent State Schema

**File**: `state/agent_state.py`

```python
from typing import Dict, List, Any, Optional
from pydantic import Field
from .base_state import BaseState
from ..message.conversation import Conversation, ConversationMessage
from ..types.primitives import AgentId, ExecutionMetadata
from ..types.enums import AgentType, ExecutionStatus

class AgentState(BaseState):
    """State schema specific to agents."""

    # Agent identification
    agent_id: AgentId = Field(..., description="Agent identifier")
    agent_type: AgentType = Field(..., description="Agent type")

    # Agent execution state
    current_execution: Optional[str] = Field(default=None, description="Current execution ID")
    execution_status: ExecutionStatus = Field(default=ExecutionStatus.PENDING)

    # Conversation state
    conversation: Conversation = Field(default_factory=Conversation)

    # Agent-specific data
    context: Dict[str, Any] = Field(default_factory=dict, description="Agent context")
    memory: Dict[str, Any] = Field(default_factory=dict, description="Agent memory")

    # Execution tracking
    execution_count: int = Field(default=0, description="Number of executions")
    last_execution_metadata: Optional[ExecutionMetadata] = Field(default=None)

    def add_user_message(self, content: str, **kwargs) -> ConversationMessage:
        """Add user message to conversation."""
        message = self.conversation.add_user_message(content, **kwargs)
        self.updated_at = datetime.now()
        return message

    def add_assistant_message(self, content: str, **kwargs) -> ConversationMessage:
        """Add assistant message to conversation."""
        message = self.conversation.add_assistant_message(content, **kwargs)
        self.updated_at = datetime.now()
        return message

    def update_context(self, updates: Dict[str, Any]) -> None:
        """Update agent context."""
        self.context.update(updates)
        self.updated_at = datetime.now()
        self.version += 1

    def set_memory(self, key: str, value: Any) -> None:
        """Set memory value."""
        self.memory[key] = value
        self.updated_at = datetime.now()
        self.version += 1

    def get_memory(self, key: str, default: Any = None) -> Any:
        """Get memory value."""
        return self.memory.get(key, default)

    def start_execution(self, execution_id: str) -> None:
        """Start new execution."""
        self.current_execution = execution_id
        self.execution_status = ExecutionStatus.RUNNING
        self.execution_count += 1
        self.add_execution(execution_id)

    def complete_execution(self, metadata: ExecutionMetadata) -> None:
        """Complete execution."""
        self.execution_status = ExecutionStatus.COMPLETED
        self.last_execution_metadata = metadata
        self.current_execution = None
        self.updated_at = datetime.now()

    def fail_execution(self, error: str, metadata: ExecutionMetadata) -> None:
        """Fail execution."""
        self.execution_status = ExecutionStatus.FAILED
        self.last_execution_metadata = metadata
        self.current_execution = None
        self.set_data("last_error", error)

    def get_recent_messages(self, count: int = 10) -> List[ConversationMessage]:
        """Get recent conversation messages."""
        return self.conversation.get_recent_messages(count)

    def clear_conversation(self) -> None:
        """Clear conversation history."""
        self.conversation = Conversation()
        self.updated_at = datetime.now()
```

### Step 4: Configuration Schemas (Day 4)

#### 4.1 Base Configuration Schema

**File**: `config/base_config.py`

```python
from typing import Any, Dict, List, Optional, TypeVar
from pydantic import BaseModel, Field, validator
from ..types.primitives import BaseMetadata
from ..types.enums import ConfigCategory
from ..validation.validators import ConfigValidator

ConfigT = TypeVar('ConfigT', bound='BaseConfig')

class BaseConfig(BaseModel):
    """Base configuration schema for all configurable components."""

    # Core configuration identification
    name: str = Field(..., min_length=1, max_length=100, description="Configuration name")
    category: ConfigCategory = Field(..., description="Configuration category")

    # Configuration metadata
    version: str = Field(default="1.0", description="Configuration version")
    description: Optional[str] = Field(default=None, max_length=500, description="Configuration description")

    # Validation settings
    strict_validation: bool = Field(default=True, description="Enable strict validation")
    allow_extra_fields: bool = Field(default=False, description="Allow extra fields")

    # Configuration data
    settings: Dict[str, Any] = Field(default_factory=dict, description="Configuration settings")

    # Metadata
    metadata: BaseMetadata = Field(default_factory=dict, description="Configuration metadata")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        extra = "forbid"
        validate_assignment = True

    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate configuration name."""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Name must be alphanumeric with underscores or hyphens")
        return v

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get configuration setting."""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set configuration setting."""
        self.settings[key] = value

    def update_settings(self, updates: Dict[str, Any]) -> None:
        """Update multiple settings."""
        self.settings.update(updates)

    def validate_settings(self) -> List[str]:
        """Validate configuration settings."""
        validator = ConfigValidator()
        return validator.validate_config(self)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseConfig':
        """Create configuration from dictionary."""
        return cls.model_validate(data)
```

#### 4.2 Engine Configuration Schema

**File**: `config/engine_config.py`

```python
from typing import Dict, List, Any, Optional
from pydantic import Field, validator
from .base_config import BaseConfig
from ..types.enums import ConfigCategory
from ..types.primitives import TokenCount

class LLMConfig(BaseConfig):
    """LLM engine configuration."""

    category: ConfigCategory = Field(default=ConfigCategory.ENGINE, frozen=True)

    # Core LLM settings
    model: str = Field(..., description="LLM model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[TokenCount] = Field(default=None, ge=1, description="Maximum tokens")

    # Advanced settings
    top_p: float = Field(default=1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="Presence penalty")

    # System configuration
    system_message: Optional[str] = Field(default=None, description="System message")

    # Request settings
    timeout_seconds: int = Field(default=60, gt=0, description="Request timeout")
    max_retries: int = Field(default=3, ge=0, description="Maximum retries")

    @validator('model')
    def validate_model(cls, v: str) -> str:
        """Validate model name."""
        if not v:
            raise ValueError("Model name cannot be empty")
        return v

class ToolConfig(BaseConfig):
    """Tool configuration."""

    category: ConfigCategory = Field(default=ConfigCategory.TOOL, frozen=True)

    # Tool settings
    tool_timeout_seconds: int = Field(default=30, gt=0, description="Tool execution timeout")
    max_tool_calls: int = Field(default=10, gt=0, description="Maximum tool calls per execution")
    allow_parallel_tools: bool = Field(default=False, description="Allow parallel tool execution")

    # Validation settings
    validate_tool_inputs: bool = Field(default=True, description="Validate tool inputs")
    validate_tool_outputs: bool = Field(default=True, description="Validate tool outputs")
    strict_tool_routing: bool = Field(default=True, description="Strict tool routing")

    # Tool registry
    registered_tools: Dict[str, str] = Field(default_factory=dict, description="Registered tool routes")

class StructuredOutputConfig(BaseConfig):
    """Structured output configuration."""

    category: ConfigCategory = Field(default=ConfigCategory.ENGINE, frozen=True)

    # Output settings
    output_format: str = Field(default="json", description="Output format")
    strict_mode: bool = Field(default=True, description="Strict parsing mode")

    # Validation settings
    validate_output: bool = Field(default=True, description="Validate output structure")
    retry_on_validation_error: bool = Field(default=True, description="Retry on validation errors")
    max_validation_retries: int = Field(default=3, ge=0, description="Maximum validation retries")

    # Schema settings
    include_schema_in_prompt: bool = Field(default=True, description="Include schema in prompt")
    schema_format: str = Field(default="json_schema", description="Schema format")

    @validator('output_format')
    def validate_output_format(cls, v: str) -> str:
        """Validate output format."""
        allowed_formats = ["json", "yaml", "xml"]
        if v not in allowed_formats:
            raise ValueError(f"Output format must be one of: {', '.join(allowed_formats)}")
        return v

class CompositeEngineConfig(BaseConfig):
    """Composite engine configuration combining all aspects."""

    category: ConfigCategory = Field(default=ConfigCategory.ENGINE, frozen=True)

    # Component configurations
    llm_config: LLMConfig = Field(default_factory=LLMConfig)
    tool_config: ToolConfig = Field(default_factory=ToolConfig)
    structured_output_config: StructuredOutputConfig = Field(default_factory=StructuredOutputConfig)

    def update_llm_config(self, **kwargs) -> None:
        """Update LLM configuration."""
        for key, value in kwargs.items():
            if hasattr(self.llm_config, key):
                setattr(self.llm_config, key, value)

    def update_tool_config(self, **kwargs) -> None:
        """Update tool configuration."""
        for key, value in kwargs.items():
            if hasattr(self.tool_config, key):
                setattr(self.tool_config, key, value)

    def update_structured_config(self, **kwargs) -> None:
        """Update structured output configuration."""
        for key, value in kwargs.items():
            if hasattr(self.structured_output_config, key):
                setattr(self.structured_output_config, key, value)
```

### Step 5: Schema Composition (Days 5-6)

#### 5.1 State Composer

**File**: `composition/state_composer.py`

```python
from typing import Dict, List, Any, Type, Optional, TypeVar
from ..state.base_state import BaseState
from ..state.agent_state import AgentState
from ..state.workflow_state import WorkflowState
from ..types.enums import StateScope

StateT = TypeVar('StateT', bound=BaseState)

class StateComposer:
    """Compose complex states from simpler state schemas."""

    def __init__(self):
        self._state_registry: Dict[str, Type[BaseState]] = {}
        self._composition_rules: Dict[str, Dict[str, Any]] = {}

    def register_state_type(self, name: str, state_class: Type[BaseState]) -> None:
        """Register a state type."""
        self._state_registry[name] = state_class

    def create_composite_state(
        self,
        name: str,
        state_types: List[str],
        field_mappings: Optional[Dict[str, str]] = None,
        scope: StateScope = StateScope.PRIVATE
    ) -> Type[BaseState]:
        """Create composite state from multiple state types."""

        # Get state classes
        base_classes = []
        for state_type in state_types:
            if state_type not in self._state_registry:
                raise ValueError(f"Unknown state type: {state_type}")
            base_classes.append(self._state_registry[state_type])

        # Create dynamic class
        class CompositeState(*base_classes):
            """Dynamically created composite state."""

            def __init__(self, **kwargs):
                # Initialize all base classes
                for base_class in base_classes:
                    base_class.__init__(self, **kwargs)

                # Set scope
                self.scope = scope

                # Apply field mappings
                if field_mappings:
                    self._apply_field_mappings(field_mappings)

            def _apply_field_mappings(self, mappings: Dict[str, str]) -> None:
                """Apply field mappings between states."""
                for source_field, target_field in mappings.items():
                    if hasattr(self, source_field):
                        value = getattr(self, source_field)
                        setattr(self, target_field, value)

        # Set class name
        CompositeState.__name__ = name
        CompositeState.__qualname__ = name

        return CompositeState

    def merge_states(self, states: List[BaseState]) -> BaseState:
        """Merge multiple state instances."""
        if not states:
            raise ValueError("Cannot merge empty state list")

        # Use first state as base
        merged_state = states[0].model_copy()

        # Merge data from other states
        for state in states[1:]:
            # Merge data fields
            merged_state.data.update(state.data)

            # Merge metadata
            merged_state.metadata.update(state.metadata)

            # Merge execution history
            merged_state.execution_history.extend(state.execution_history)

            # Update version
            merged_state.version = max(merged_state.version, state.version)

        return merged_state

    def project_state(
        self,
        source_state: BaseState,
        target_fields: List[str],
        field_mappings: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Project state to specific fields."""
        projection = {}
        mappings = field_mappings or {}

        for field in target_fields:
            source_field = mappings.get(field, field)

            if hasattr(source_state, source_field):
                projection[field] = getattr(source_state, source_field)
            elif source_field in source_state.data:
                projection[field] = source_state.data[source_field]

        return projection

    def create_state_view(
        self,
        source_state: BaseState,
        view_name: str,
        visible_fields: List[str],
        scope: StateScope = StateScope.SHARED
    ) -> BaseState:
        """Create filtered view of state."""

        # Create view class dynamically
        class StateView(BaseState):
            def __init__(self, source: BaseState, visible: List[str]):
                # Initialize with projected data
                projected_data = {}
                for field in visible:
                    if hasattr(source, field):
                        projected_data[field] = getattr(source, field)
                    elif field in source.data:
                        projected_data[field] = source.data[field]

                super().__init__(
                    component_name=f"{source.component_name}_view",
                    component_type=f"{source.component_type}_view",
                    data=projected_data,
                    scope=scope
                )

                # Store reference to source
                self._source = source
                self._visible_fields = visible

            def sync_with_source(self) -> None:
                """Sync view with source state."""
                for field in self._visible_fields:
                    if hasattr(self._source, field):
                        setattr(self, field, getattr(self._source, field))
                    elif field in self._source.data:
                        self.data[field] = self._source.data[field]

        StateView.__name__ = view_name
        StateView.__qualname__ = view_name

        return StateView(source_state, visible_fields)

# Factory functions for common state compositions
def create_agent_workflow_state(agent_id: str, workflow_id: str) -> Type[BaseState]:
    """Create composite state for agent-workflow combination."""
    composer = StateComposer()
    composer.register_state_type("agent", AgentState)
    composer.register_state_type("workflow", WorkflowState)

    return composer.create_composite_state(
        name="AgentWorkflowState",
        state_types=["agent", "workflow"],
        field_mappings={
            "agent_id": "agent_id",
            "workflow_id": "workflow_id"
        },
        scope=StateScope.SHARED
    )

def create_multi_agent_state(agent_ids: List[str]) -> Type[BaseState]:
    """Create state for multi-agent scenarios."""
    composer = StateComposer()

    # Register individual agent states
    for i, agent_id in enumerate(agent_ids):
        composer.register_state_type(f"agent_{i}", AgentState)

    # Create composite for all agents
    return composer.create_composite_state(
        name="MultiAgentState",
        state_types=[f"agent_{i}" for i in range(len(agent_ids))],
        scope=StateScope.SHARED
    )
```

## 📊 Success Metrics

### Technical Metrics

- [ ] **33% LOC reduction** (6,000 → 4,000 LOC)
- [ ] **Domain separation** - state, config, message schemas separate
- [ ] **Zero circular imports** between schema modules
- [ ] **100% type coverage** with proper TypeVar usage
- [ ] **Composition patterns** working for complex schemas

### Quality Metrics

- [ ] **Single responsibility** - each schema has one clear purpose
- [ ] **Reusable components** - schemas composable across domains
- [ ] **Type safety** - proper generic types and constraints
- [ ] **Clear interfaces** - well-defined schema contracts

### Developer Experience

- [ ] **Easy schema creation** - factory functions for common patterns
- [ ] **Clear documentation** - purpose and usage of each schema
- [ ] **Type hints** - full IDE support with type checking
- [ ] **Migration support** - clear upgrade path from mixed schemas

## 🔗 Integration Points

### With Engine Domain

- Engine configurations use config schemas
- Engine state managed by state schemas
- Message handling via message schemas

### With Agent Domain

- Agents use agent state and config schemas
- Agent messages handled by conversation schemas
- Agent composition via state composition patterns

### With Workflow Domain

- Workflows use workflow state and config schemas
- Workflow execution state tracked via state schemas
- Cross-workflow communication via message schemas

## 🚨 Common Pitfalls

### 1. Over-composition

**Problem**: Making schemas too complex with too many composition layers
**Solution**: Keep composition simple, favor explicit over implicit

### 2. Type Safety Loss

**Problem**: Dynamic schema creation breaking type checking
**Solution**: Use proper TypeVar bounds and protocols

### 3. Circular Schema Dependencies

**Problem**: Schemas importing each other in cycles
**Solution**: Use forward references and protocol-based interfaces

### 4. Migration Complexity

**Problem**: Moving from mixed schemas being too disruptive
**Solution**: Gradual migration with compatibility adapters

## 🔄 Rollback Strategy

### If Schema Separation Issues Arise

1. **Module-by-module rollback**: Each schema domain is independent
2. **Gradual reversion**: Move one schema type back at a time
3. **Compatibility layer**: Maintain old schema interfaces during transition
4. **Type checking**: Use mypy to catch issues early

### Risk Mitigation

- Maintain compatibility adapters during transition
- Comprehensive testing of new vs old schema behavior
- Type checking integration with CI/CD
- Clear migration guides for each schema transformation

---

**Next Steps**:

1. Start with type definitions (foundation layer)
2. Build message schemas (most isolated)
3. Create state schemas with composition patterns
4. Validate type safety and schema composition works correctly
