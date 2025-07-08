# Issues and Solutions - Dynamic Supervisor

## Issue 1: Tool Docstring Error
**Problem**: @tool decorator requires docstring when description not provided
**Error**: "Function must have a docstring if description not provided"
**Solution**: Replace f-string docstrings with regular strings
```python
# Bad
@tool
def route_to_agent(task: str) -> str:
    f"""Route to {agent_name}"""  # Error!

# Good
@tool
def route_to_agent(task: str) -> str:
    """Route task to agent"""  # Works
```

## Issue 2: Import Error
**Problem**: Cannot import 'tavily_search' from search_tools
**Error**: "cannot import name 'tavily_search'"
**Solution**: Use correct import name 'tavily_search_tool'
```python
# Bad
from haive.tools.tools.search_tools import tavily_search

# Good
from haive.tools.tools.search_tools import tavily_search_tool
```

## Issue 3: Pydantic Pattern
**Problem**: Using __init__ in Pydantic models
**Solution**: Use @model_validator(mode="after")
```python
# Bad
class Supervisor(ReactAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

# Good
class Supervisor(ReactAgent):
    @model_validator(mode="after")
    def setup_supervisor(self):
        # Setup logic here
        return self
```

## Issue 4: Agent Activation Pattern
**Challenge**: How to make supervisor recognize missing capabilities
**Solution**: Implement three-step process:
1. check_required_capabilities tool analyzes task
2. Supervisor compares required vs available
3. activate_dormant_agent tool brings agents online

## Issue 5: Tool Synchronization
**Problem**: Handoff tools don't update when agents activated
**Solution**: Call _update_available_tools() after any registry change
- Clears old handoff tools
- Creates new ones for active agents only
- Updates capability model