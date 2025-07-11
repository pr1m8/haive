"""Test that reproduces the exact LangGraph scenario."""

import logging
from typing import TYPE_CHECKING, Any, Optional

from langchain_core.output_parsers.base import BaseOutputParser
from langgraph.graph import StateGraph
from pydantic import BaseModel, ConfigDict, Field

logging.basicConfig(level=logging.INFO)


# Test different approaches
class Approach1_DirectImport(BaseModel):
    """Direct import approach."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    output_parser: BaseOutputParser | None = Field(default=None)


class Approach2_StringAnnotation(BaseModel):
    """String annotation approach."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    output_parser: Optional["BaseOutputParser"] = Field(default=None)


class Approach3_AnyType(BaseModel):
    """Any type approach."""

    output_parser: Any | None = Field(default=None)


class Approach4_Excluded(BaseModel):
    """Excluded field approach."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    output_parser: BaseOutputParser | None = Field(default=None, exclude=True)


# Approach 5: Private attribute (not part of schema)
class Approach5_PrivateAttr(BaseModel):
    """Private attribute approach."""

    _output_parser: BaseOutputParser | None = None

    def set_output_parser(self, parser: BaseOutputParser):
        self._output_parser = parser

    def get_output_parser(self) -> BaseOutputParser | None:
        return self._output_parser


# Approach 6: Dict field that stores parser
class Approach6_DictField(BaseModel):
    """Dict field approach."""

    config: dict = Field(default_factory=dict)

    def set_output_parser(self, parser: BaseOutputParser):
        self.config["output_parser"] = parser

    def get_output_parser(self) -> BaseOutputParser | None:
        return self.config.get("output_parser")


# Test each approach with LangGraph
approaches = [
    (Approach1_DirectImport, "Direct import"),
    (Approach2_StringAnnotation, "String annotation"),
    (Approach3_AnyType, "Any type"),
    (Approach4_Excluded, "Excluded field"),
    (Approach5_PrivateAttr, "Private attribute"),
    (Approach6_DictField, "Dict field"),
]

for approach_class, name in approaches:

    class TestState(BaseModel):
        engine: approach_class = Field(...)
        messages: list = Field(default_factory=list)

    try:
        # This is where LangGraph evaluates types
        graph = StateGraph(TestState)

        # Add a simple node to test
        def process(state):
            return {"messages": [*state.messages, "processed"]}

        graph.add_node("process", process)
        graph.set_entry_point("process")
        graph.set_finish_point("process")

        # Compile the graph
        compiled = graph.compile()


        # Test actual execution
        result = compiled.invoke({"engine": approach_class(), "messages": []})

    except NameError as e:
        pass")
    except Exception as e:
        pass")

# Test the actual AugLLMConfig scenario

try:
    from haive.core.engine.aug_llm import AugLLMConfig

    class RealScenarioState(BaseModel):
        engine: AugLLMConfig = Field(...)
        messages: list = Field(default_factory=list)

    graph = StateGraph(RealScenarioState)

except Exception as e:
    pass")
