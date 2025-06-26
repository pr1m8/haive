# Pydantic v2 Migration Guide

## Overview

Haive uses Pydantic v2 throughout the codebase, which brings significant improvements in performance and features compared to v1. This document outlines key differences and migration patterns when working with the framework.

## Key Changes in Pydantic v2

### 1. Model Configuration

**v1 Style (avoid):**

```python
class MyModel(BaseModel):
    field: str

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"
```

**v2 Style (use):**

```python
class MyModel(BaseModel):
    field: str

    model_config = {
        "arbitrary_types_allowed": True,
        "extra": "forbid"
    }
```

Or with `ConfigDict`:

```python
from pydantic import BaseModel, ConfigDict

class MyModel(BaseModel):
    field: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid"
    )
```

### 2. Field Validation

**v1 Style (avoid):**

```python
from pydantic import BaseModel, validator

class MyModel(BaseModel):
    field: str

    @validator("field")
    def validate_field(cls, v):
        return v.strip()
```

**v2 Style (use):**

```python
from pydantic import BaseModel, field_validator

class MyModel(BaseModel):
    field: str

    @field_validator("field")
    def validate_field(cls, v):
        return v.strip()
```

### 3. Model Methods

**v1 Style (avoid):**

```python
data_dict = model.dict()
json_str = model.json()
new_model = MyModel.parse_obj(data)
```

**v2 Style (use):**

```python
data_dict = model.model_dump()
json_str = model.model_dump_json()
new_model = MyModel.model_validate(data)
```

### 4. Field Definition

**v1 Style (avoid):**

```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    field: str = Field(..., description="Required field")
    optional: Optional[int] = Field(None, ge=0)
```

**v2 Style (use):**

```python
from pydantic import BaseModel, Field
from typing import Optional

class MyModel(BaseModel):
    field: str = Field(description="Required field")
    optional: Optional[int] = Field(default=None, ge=0)
```

### 5. Root Validators

**v1 Style (avoid):**

```python
from pydantic import BaseModel, root_validator

class MyModel(BaseModel):
    x: int
    y: int

    @root_validator
    def validate_coordinates(cls, values):
        x, y = values.get("x"), values.get("y")
        if x == y:
            raise ValueError("x and y cannot be equal")
        return values
```

**v2 Style (use):**

```python
from pydantic import BaseModel, model_validator

class MyModel(BaseModel):
    x: int
    y: int

    @model_validator(mode="after")
    def validate_coordinates(self):
        if self.x == self.y:
            raise ValueError("x and y cannot be equal")
        return self
```

## Working with State Schemas

### State Schema Definition

```python
from haive.core.schema.state_schema import StateSchema
from pydantic import Field
from typing import List, Dict, Any, Optional

class MyAgentState(StateSchema):
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    counter: int = Field(default=0)
    result: Optional[str] = Field(default=None)

    # Field reducers
    __reducer_fields__ = {
        "messages": operator.add,
        "counter": operator.add
    }
```

### Field Annotation with Metadata

```python
from typing import Annotated, List
import operator
from pydantic import Field

class AnnotatedState(StateSchema):
    # Using Annotated for reducers
    messages: Annotated[List[Dict[str, Any]], operator.add] = Field(default_factory=list)

    # Using Annotated for multiple metadata
    counter: Annotated[int, operator.add, Field(description="Operation counter")] = 0
```

### Serialization and Deserialization

```python
# Serialize to dict
state_dict = state.model_dump()

# Serialize to JSON
state_json = state.model_dump_json()

# Create from dict
new_state = MyAgentState.model_validate(state_dict)

# Create from JSON
new_state = MyAgentState.model_validate_json(state_json)
```

## Transitioning Existing Code

### Step 1: Update Model Configuration

```python
# Update any classes using Config
class MyClass(BaseModel):
    # v1 style
    # class Config:
    #     arbitrary_types_allowed = True

    # v2 style
    model_config = {"arbitrary_types_allowed": True}
```

### Step 2: Update Validators

```python
# Change validator decorators
class MyClass(BaseModel):
    field: str

    # v1 style
    # @validator("field")
    # def validate_field(cls, v):
    #     return v

    # v2 style
    @field_validator("field")
    def validate_field(cls, v):
        return v

    # Change root validators
    # v1 style
    # @root_validator
    # def validate_all(cls, values):
    #     return values

    # v2 style
    @model_validator(mode="after")
    def validate_all(self):
        return self
```

### Step 3: Update Method Calls

```python
# Change method calls on model instances
def process_model(model: BaseModel):
    # v1 style
    # data = model.dict()
    # json_data = model.json()

    # v2 style
    data = model.model_dump()
    json_data = model.model_dump_json()
```

### Step 4: Update Creation Methods

```python
# Change model creation methods
def create_model(data: dict):
    # v1 style
    # model = MyModel.parse_obj(data)
    # model = MyModel.parse_raw(json_str)

    # v2 style
    model = MyModel.model_validate(data)
    model = MyModel.model_validate_json(json_str)
```

## Common Patterns in Haive

### Engine Configuration

```python
from haive.core.engine.base import InvokableEngine, EngineType
from pydantic import Field

class MyEngine(InvokableEngine):
    engine_type: EngineType = Field(default=EngineType.LLM)
    model: str = Field(default="gpt-4o")

    model_config = {"arbitrary_types_allowed": True}

    def get_input_fields(self):
        return {"prompt": (str, None)}

    def get_output_fields(self):
        return {"completion": (str, None)}
```

### Node Configuration

```python
from haive.core.graph.node.config import NodeConfig
from pydantic import Field

node_config = NodeConfig(
    debug=True,
    rich_debug=True,
    preserve_model=True,
    metadata={"description": "This is a test node"}
)
```

### Agent State

```python
from haive.core.schema.state_schema import StateSchema
from pydantic import Field
from typing import List, Dict, Any

class AgentState(StateSchema):
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

    # v2 style model configuration
    model_config = {"extra": "allow"}

    # Field reducers
    __reducer_fields__ = {
        "messages": operator.add,
        "context": operator.or_
    }
```
