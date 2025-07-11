#!/usr/bin/env python3
"""Test to reproduce the exact BaseOutputParser error with LangGraph."""

from typing import Optional, get_type_hints

from pydantic import BaseModel, Field

# Test 1: Simple type hints without forward references


class SimpleConfig(BaseModel):
    name: str = Field(default="test")
    value: int = Field(default=42)


try:
    hints = get_type_hints(SimpleConfig)
    for name, hint in hints.items():
        pass
except Exception as e:
    pass

# Test 2: Type hints with imported class

from langchain_core.output_parsers.base import BaseOutputParser


class ConfigWithParser(BaseModel):
    parser: BaseOutputParser | None = Field(default=None)


try:
    hints = get_type_hints(ConfigWithParser)
    for name, hint in hints.items():
        pass
except Exception as e:
    pass

# Test 3: Simulate LangGraph's namespace issue

# Create a class in a separate namespace
exec_namespace = {}
try:
    exec(
        """
from pydantic import BaseModel, Field
from typing import Optional

class IsolatedConfig(BaseModel):
    # This will fail because BaseOutputParser isn't in the exec namespace
    parser: Optional[BaseOutputParser] = Field(default=None)
""",
        exec_namespace,
    )
except NameError as e:

try:
    # This simulates what LangGraph does
    hints = get_type_hints(exec_namespace["IsolatedConfig"])
except NameError as e:

# Test 4: Forward reference solution

exec_namespace2 = {}
exec(
    """
from pydantic import BaseModel, Field
from typing import Optional

class ForwardRefConfig(BaseModel):
    # Using string annotation (forward reference)
    parser: Optional["BaseOutputParser"] = Field(default=None)
""",
    exec_namespace2,
)

print(exec_namespace2)

try:
    # This will also fail because BaseOutputParser still isn't available
    hints = get_type_hints(exec_namespace2["ForwardRefConfig"])
except NameError as e:
    pass
# Test 5: The real solution - import in the namespace

exec_namespace3 = {"BaseOutputParser": BaseOutputParser}
exec(
    """
from pydantic import BaseModel, Field
from typing import Optional

class WorkingConfig(BaseModel):
    parser: Optional[BaseOutputParser] = Field(default=None)
""",
    exec_namespace3,
)

try:
    hints = get_type_hints(exec_namespace3["WorkingConfig"], globalns=exec_namespace3)
    for name, hint in hints.items():
        pass
except Exception as e:
    pass

# Test 6: What happens in our actual code

from haive.core.schema.prebuilt.llm_state import LLMState


# Create a state that includes an engine field
class TestState(LLMState):
    test_field: str = Field(default="test")


for name, field in TestState.model_fields.items():
    pass

# Now simulate what LangGraph does
try:
    # LangGraph creates a new namespace and tries to evaluate types
    hints = get_type_hints(TestState, localns={"TestState": TestState})
except NameError as e:
    