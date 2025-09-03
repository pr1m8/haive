
:py:mod:`haive.core.engine.output_parser`
========================

.. py:module:: haive.core.engine.output_parser

.. autoapi-nested-parse::

   Output parser engine module for the Haive framework.

   This module provides engine implementations for LangChain output parsers,
   enabling structured output parsing from LLM responses within the Haive framework.

   Output parsers transform raw LLM text outputs into structured data formats,
   including JSON, Pydantic models, enums, lists, and custom formats. This module
   wraps LangChain's output parser functionality in Haive's engine system for
   consistent usage across the framework.

   Key Components:
       OutputParserEngine: Engine wrapper for LangChain output parsers
       OutputParserType: Enumeration of supported parser types

   Supported Parser Types:
       - JSON: Parse output as JSON objects
       - PydanticOutputParser: Parse into Pydantic model instances
       - EnumOutputParser: Parse into enum values
       - DatetimeOutputParser: Parse datetime strings
       - BooleanOutputParser: Parse boolean values
       - CommaSeparatedListOutputParser: Parse comma-separated lists
       - MarkdownListOutputParser: Parse markdown formatted lists
       - NumberedListOutputParser: Parse numbered lists
       - XMLOutputParser: Parse XML formatted output

   .. admonition:: Examples

      JSON output parsing::
      
          from haive.core.engine.output_parser import OutputParserEngine, OutputParserType
      
          parser = OutputParserEngine(
              parser_type=OutputParserType.JSON,
              name="json_parser"
          )
      
          result = parser.invoke('{"name": "John", "age": 30}')
          # Returns: {"name": "John", "age": 30}
      
      Pydantic model parsing::
      
          from pydantic import BaseModel, Field
          from haive.core.engine.output_parser import OutputParserEngine, OutputParserType
      
          class Person(BaseModel):
              name: str = Field(description="Person's name")
              age: int = Field(description="Person's age")
      
          parser = OutputParserEngine(
              parser_type=OutputParserType.PYDANTIC,
              pydantic_object=Person,
              name="person_parser"
          )
      
          result = parser.invoke("name: John\\nage: 30")
          # Returns: Person(name="John", age=30)

   .. seealso::

      - LangChain output parsers documentation
      - Output parser types: types.py
      - Base implementation: base.py





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.output_parser.base   haive.core.engine.output_parser.types
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/output_parser/base/index   /api_clean/haive/core/engine/output_parser/types/index





Package Contents
----------------

.. rubric:: haive.core.engine.output_parser.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.output_parser.OutputParserEngine   haive.core.engine.output_parser.OutputParserType

.. automodule:: haive.core.engine.output_parser
   :members:
   :undoc-members:
   :show-inheritance: