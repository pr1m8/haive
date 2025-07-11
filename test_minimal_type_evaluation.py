"""Test the minimal case of type evaluation issue."""

from __future__ import annotations

from typing import Any, Optional, get_type_hints

from pydantic import BaseModel, ConfigDict, Field


# Simulate the problem structure
class SomeParser:
    """Represents BaseOutputParser."""



class ConfigWithParser(BaseModel):
    """Represents AugLLMConfig."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    output_parser: SomeParser | None = Field(default=None)


class StateWithConfig(BaseModel):
    """Represents LLMState."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    engine: ConfigWithParser = Field(...)


# Test 1: Direct type hints evaluation
try:
    hints = get_type_hints(StateWithConfig)
except NameError as e:
    passe)


# Test 2: Evaluation in different namespace (simulates LangGraph)
def evaluate_in_clean_namespace(cls):
    """Simulate LangGraph's evaluation environment."""
    namespace = {"Optional": Optional}  # Limited namespace
    import typing

    return typing.get_type_hints(cls, globalns=namespace, localns={})


try:
    hints = evaluate_in_clean_namespace(StateWithConfig)
except NameError as e:
    passe)


# Test 3: String annotations approach
class ConfigWithParserString(BaseModel):
    """Using string annotations."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    output_parser: "SomeParser" | None = Field(default=None)


class StateWithConfigString(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    engine: ConfigWithParserString = Field(...)


try:
    hints = evaluate_in_clean_namespace(StateWithConfigString)
except NameError as e:
    passe)

# Test 4: What if we provide the classes in namespace?
try:
    namespace = {
        "Optional": Optional,
        "SomeParser": SomeParser,
        "ConfigWithParser": ConfigWithParser,
        "ConfigWithParserString": ConfigWithParserString,
    }
    hints = get_type_hints(StateWithConfig, globalns=namespace, localns={})
except NameError as e:
    passe)


# Test 5: Using Any type
class ConfigWithAny(BaseModel):
    """Using Any type."""

    output_parser: Any | None = Field(default=None)


class StateWithAny(BaseModel):
    engine: ConfigWithAny = Field(...)


try:
    hints = evaluate_in_clean_namespace(StateWithAny)
except NameError as e:
    passe)


# Test 6: Excluding the field
class ConfigWithExcluded(BaseModel):
    """Excluding the field."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    output_parser: SomeParser | None = Field(default=None, exclude=True)


class StateWithExcluded(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    engine: ConfigWithExcluded = Field(...)


try:
    hints = evaluate_in_clean_namespace(StateWithExcluded)
except NameError as e:
    passe)
