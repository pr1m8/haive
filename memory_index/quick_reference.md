# Quick Reference - Most Used Patterns and Fixes

## BaseModel Tool Routing (2025-01-29)

```python
# Three distinct routes for BaseModel:
if route == "parse_output":
    # Structured output model for LLM response parsing
elif route == "pydantic_model":
    # BaseModel without __call__ - error (cannot execute)
elif route == "pydantic_tool":
    # BaseModel with __call__ - executable tool
    # Still needs conversion to StructuredTool by ToolEngine
```

## Pydantic Forward Reference Fix (2025-01-29)

```python
# Problem: Mixins using __init__ cause forward reference errors
# Solution: Use model_post_init instead
def model_post_init(self, __context: Any) -> None:
    super().model_post_init(__context)
    # Initialize mixin attributes here
```

## ReactAgent Loop Pattern (2025-01-29)

```python
# Simple pattern: Change edges to loop back
if "tool_node" in graph.nodes:
    graph.remove_edge("tool_node", END)
    graph.add_edge("tool_node", "agent_node")  # Loop!
```

## Common Commands

```bash
# Always use poetry run
poetry run pytest packages/haive-agents/tests/ -xvs

# Git safety
git status && git diff
git add specific_file.py
git commit --no-verify -m "feat: description"

# Find patterns
find packages/ -name "*.py" | xargs grep -l "pattern"
```

## Import Patterns

```python
# Always explicit imports
from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent_v3 import SimpleAgentV3

# For typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from haive.agents.base.enhanced_agent import Agent
```
