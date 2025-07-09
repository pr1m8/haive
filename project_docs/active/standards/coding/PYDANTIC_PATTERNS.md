# Pydantic Patterns and Best Practices

**Version**: 1.0  
**Purpose**: Comprehensive Pydantic usage patterns and anti-patterns  
**Last Updated**: 2025-01-09

## 🚨 CRITICAL: Research First, Code Second

### Before Creating ANY Pydantic Model
```bash
# 1. Check existing similar models
find packages/ -name "*.py" | xargs grep -l "class.*BaseModel" | head -10

# 2. Look for existing config patterns
find packages/ -name "*config*.py" | head -5

# 3. Check existing field validation
grep -r "Field(" packages/ | head -10

# 4. Look at similar use cases
grep -r "your_use_case" packages/ | head -5
```

## ❌ Common Pydantic Mistakes (NEVER DO)

### 1. Manual __init__ Override
```python
# ❌ ABSOLUTELY WRONG - Breaks Pydantic completely
class AgentConfig(BaseModel):
    name: str
    temperature: float
    
    def __init__(self, name, temperature):  # ❌ DESTROYS PYDANTIC
        self.name = name
        self.temperature = temperature
        # This breaks validation, serialization, everything!
```

### 2. Ignoring Existing Patterns
```python
# ❌ WRONG - Not checking existing patterns
class MyConfig(BaseModel):
    model: str  # Reinventing existing ModelConfig
    
# ✅ CORRECT - Using existing patterns
from haive.core.config import BaseEngineConfig
class MyConfig(BaseEngineConfig):
    my_field: str = Field(...)
```

### 3. No Validation
```python
# ❌ WRONG - No field validation
class AgentConfig(BaseModel):
    name: str
    temperature: float
    tools: list

# ✅ CORRECT - Proper validation
class AgentConfig(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    tools: List[str] = Field(default_factory=list)
```

### 4. Missing ConfigDict
```python
# ❌ WRONG - No configuration
class AgentConfig(BaseModel):
    name: str

# ✅ CORRECT - Proper configuration
class AgentConfig(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    name: str = Field(...)
```

## ✅ Proper Pydantic Patterns

### Research Existing Patterns
```bash
# Check what already exists before creating
find packages/ -name "*.py" -exec grep -l "class.*Config.*BaseModel" {} \;
find packages/ -name "*.py" -exec grep -l "StateSchema" {} \;
find packages/ -name "*.py" -exec grep -l "EngineConfig" {} \;
```

### Standard Model Template
```python
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import datetime

class ModelType(str, Enum):
    """Enum for model types - check existing enums first!"""
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    CLAUDE_3 = "claude-3"

class AgentConfig(BaseModel):
    """Agent configuration with comprehensive validation.
    
    This model defines configuration for AI agents with full validation,
    type safety, and error handling.
    
    Attributes:
        name: Agent identifier (3-50 chars, alphanumeric + underscore)
        model: LLM model from supported ModelType enum
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum response tokens (100-4000, None for default)
        tools: List of available tool names
        system_prompt: Optional system prompt override
        metadata: Optional metadata dictionary
        
    Examples:
        Basic configuration::
        
            config = AgentConfig(
                name="research_agent",
                model=ModelType.GPT4,
                temperature=0.7,
                tools=["web_search", "calculator"]
            )
            
        With validation::
        
            try:
                config = AgentConfig(
                    name="test",
                    temperature=3.0  # Will raise ValidationError
                )
            except ValidationError as e:
                print(f"Validation failed: {e}")
                
    Note:
        Always validate against existing tool registry when specifying tools.
        Use environment variables for sensitive configuration.
    """
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid",  # Prevent unknown fields
        json_schema_extra={
            "examples": [
                {
                    "name": "research_agent",
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "tools": ["web_search", "calculator"]
                }
            ]
        }
    )
    
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Agent identifier (alphanumeric + underscore)",
        examples=["research_agent", "chat_bot_v2"]
    )
    
    model: ModelType = Field(
        default=ModelType.GPT4,
        description="LLM model selection",
        examples=[ModelType.GPT4, ModelType.CLAUDE_3]
    )
    
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0.0=deterministic, 2.0=creative)",
        examples=[0.1, 0.7, 1.0]
    )
    
    max_tokens: Optional[int] = Field(
        default=None,
        ge=100,
        le=4000,
        description="Maximum response tokens (None for model default)",
        examples=[500, 1000, 2000]
    )
    
    tools: List[str] = Field(
        default_factory=list,
        description="Available tool names",
        examples=[["web_search"], ["calculator", "file_reader"]]
    )
    
    system_prompt: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Custom system prompt override",
        examples=["You are a helpful assistant.", None]
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata dictionary",
        examples=[{"version": "1.0"}, {"department": "research"}]
    )
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate agent name format."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric with underscores only")
        return v
    
    @field_validator("tools")
    @classmethod
    def validate_tools(cls, v: List[str]) -> List[str]:
        """Validate tool names against registry."""
        # Check against existing tool registry
        from haive.core.tools import get_available_tools
        try:
            available = get_available_tools()
            invalid = set(v) - set(available)
            if invalid:
                raise ValueError(f"Unknown tools: {', '.join(invalid)}")
        except ImportError:
            # If registry not available, skip validation
            pass
        return v
    
    @model_validator(mode="after")
    def validate_model_compatibility(self) -> "AgentConfig":
        """Validate cross-field compatibility."""
        # Example: certain models have constraints
        if self.model == ModelType.CLAUDE_3 and self.max_tokens and self.max_tokens > 2000:
            raise ValueError("Claude-3 models support maximum 2000 tokens")
        return self
```

### State Schema Pattern
```python
# ALWAYS check existing state schemas first
# grep -r "StateSchema" packages/ | head -5

from haive.core.schema import StateSchema
from pydantic import Field
from typing import List, Dict, Any

class MyAgentState(StateSchema):
    """Agent state with proper inheritance.
    
    Extends StateSchema with agent-specific fields.
    ALWAYS inherit from existing base schemas.
    """
    
    messages: List[str] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    custom_field: str = Field(default="")
    
    def add_message(self, message: str) -> None:
        """Add message to state."""
        self.messages.append(message)
    
    def get_context(self, key: str) -> Any:
        """Get context value."""
        return self.context.get(key)
```

### Configuration Inheritance Pattern
```python
# Check existing base configs first
# find packages/ -name "*config*.py" | head -5

from haive.core.config import BaseEngineConfig

class MyEngineConfig(BaseEngineConfig):
    """Extend existing config patterns."""
    
    my_specific_field: str = Field(
        ...,
        description="My specific configuration"
    )
    
    @field_validator("my_specific_field")
    @classmethod
    def validate_my_field(cls, v: str) -> str:
        """Validate my specific field."""
        if not v.startswith("prefix_"):
            raise ValueError("Field must start with 'prefix_'")
        return v
```

## 🔍 Research Methodology

### Step 1: Check Existing Patterns
```bash
# Look for similar models
find packages/ -name "*.py" | xargs grep -l "class.*YourConcept.*BaseModel"

# Check existing field patterns
grep -r "Field.*your_field_type" packages/

# Look for similar validation
grep -r "field_validator.*your_field" packages/
```

### Step 2: Study Existing Implementation
```python
# Read existing similar classes
from haive.core.config import ExistingConfig  # Study this first

# Look at field definitions
# Look at validation patterns
# Look at usage examples in tests
```

### Step 3: Follow Existing Patterns
```python
# If similar config exists, inherit from it
class MyConfig(ExistingConfig):
    additional_field: str = Field(...)

# If no similar config, follow the template pattern
class MyConfig(BaseModel):
    model_config = ConfigDict(...)  # Always include this
    # ... rest of implementation
```

## 📋 Validation Patterns

### Field Validation
```python
@field_validator("field_name")
@classmethod
def validate_field(cls, v: FieldType) -> FieldType:
    """Validate individual field."""
    # Check existing validation patterns first
    if not meets_criteria(v):
        raise ValueError("Clear error message")
    return v
```

### Model Validation
```python
@model_validator(mode="after")
def validate_model(self) -> "ModelClass":
    """Validate cross-field dependencies."""
    # Check existing model validation patterns
    if self.field1 and self.field2:
        # Cross-field validation logic
        pass
    return self
```

### Custom Validation
```python
def validate_against_existing_data(value: Any) -> Any:
    """Validate against existing system data."""
    # Check existing validation functions
    from haive.core.validation import existing_validator
    return existing_validator(value)
```

## 🧪 Testing Pydantic Models

### Test Patterns
```python
import pytest
from pydantic import ValidationError

class TestAgentConfig:
    """Test Pydantic models thoroughly."""
    
    def test_valid_config_creation(self):
        """Test valid configuration creation."""
        config = AgentConfig(
            name="test_agent",
            model=ModelType.GPT4,
            temperature=0.7
        )
        assert config.name == "test_agent"
        assert config.model == ModelType.GPT4
        assert config.temperature == 0.7
    
    def test_invalid_temperature_raises_error(self):
        """Test temperature validation."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(
                name="test",
                temperature=3.0  # Invalid
            )
        assert "temperature" in str(exc_info.value)
    
    def test_field_validation(self):
        """Test field-specific validation."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(
                name="test-agent",  # Invalid (has dash)
                model=ModelType.GPT4
            )
        assert "alphanumeric" in str(exc_info.value)
```

## 📊 Performance Considerations

### Efficient Model Creation
```python
# Use model_validate for external data
config = AgentConfig.model_validate(external_data)

# Use model_construct for trusted data (skips validation)
config = AgentConfig.model_construct(**trusted_data)

# Use model_copy for efficient copying
new_config = existing_config.model_copy(update={"temperature": 0.8})
```

### Serialization
```python
# JSON serialization
json_data = config.model_dump()
config_from_json = AgentConfig.model_validate(json_data)

# Dictionary serialization
dict_data = config.model_dump(exclude={"sensitive_field"})
```

## 🚨 Common Debugging Tips

### ValidationError Debugging
```python
try:
    config = AgentConfig(**data)
except ValidationError as e:
    print(f"Validation errors: {e}")
    for error in e.errors():
        print(f"Field: {error['loc']}, Error: {error['msg']}")
```

### Model Inspection
```python
# Check model schema
print(AgentConfig.model_json_schema())

# Check field info
print(AgentConfig.model_fields)

# Validate specific data
result = AgentConfig.model_validate(data, strict=True)
```

---

**Remember**: ALWAYS research existing patterns before creating new Pydantic models. The codebase likely already has similar patterns you can extend or follow!