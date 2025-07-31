# Pydantic **init** Override Error

**Error Type**: Pydantic validation bypass  
**Impact**: Breaks all Pydantic features  
**Rule**: NEVER override `__init__` in Pydantic models

## The Problem

```python
# ❌ ABSOLUTELY WRONG
class AgentConfig(BaseModel):
    name: str
    temperature: float

    def __init__(self, name, temperature):  # DESTROYS PYDANTIC
        self.name = name
        self.temperature = temperature
```

This completely bypasses:

- Field validation
- Type checking
- Serialization/deserialization
- Default values
- Field constraints

## The Solution

```python
# ✅ CORRECT - Let Pydantic handle initialization
class AgentConfig(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    # Use validators for custom logic
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric")
        return v

# Pydantic handles everything
config = AgentConfig(name="my_agent", temperature=0.8)
```

## Custom Initialization Patterns

### Use `model_validator` for post-init logic

```python
@model_validator(mode="after")
def post_init_setup(self) -> "AgentConfig":
    """Run after Pydantic initialization."""
    # Custom logic here
    return self
```

### Use factory methods

```python
@classmethod
def from_env(cls) -> "AgentConfig":
    """Create from environment variables."""
    return cls(
        name=os.getenv("AGENT_NAME", "default"),
        temperature=float(os.getenv("TEMPERATURE", "0.7"))
    )
```

### Use `__post_init__` in dataclasses

```python
# Only for dataclasses, not Pydantic
@dataclass
class MyClass:
    def __post_init__(self):
        # Custom initialization
        pass
```

## Common Mistakes

1. **Trying to add custom validation in **init\*\*\*\*
   - Use `@field_validator` instead

2. **Setting computed fields in **init\*\*\*\*
   - Use `@computed_field` decorator

3. **Initializing from different formats**
   - Use `model_validate` or factory methods

## Related Memories

- @memory_index/by_pattern/pydantic_patterns.md
- @memory_index/by_task/validation/field_validators.md
- @memory_index/by_error/validation_errors.md

## Tags

#pydantic #error #validation #critical-rule #init
