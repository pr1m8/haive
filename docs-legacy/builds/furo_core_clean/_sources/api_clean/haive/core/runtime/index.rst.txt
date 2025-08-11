
:py:mod:`haive.core.runtime`
========================

.. py:module:: haive.core.runtime

.. autoapi-nested-parse::

   Runtime execution module for the Haive framework.

   This module provides runtime execution components and extensions for the Haive
   framework. It handles the execution of engines and components at runtime,
   providing base classes and protocols for building runtime execution systems.

   The runtime system bridges the gap between engine configurations and actual
   execution, providing a standardized way to run engines with proper lifecycle
   management, error handling, and extensibility.

   Key Components:
       RuntimeComponent: Base class for runtime components built from engine configs
       RuntimeProtocol: Protocol interface for runtime implementations
       ExtensionBase: Base class for runtime extensions
       ExtensionProtocol: Protocol for runtime extensions

   Features:
       - Engine configuration to runtime conversion
       - Lifecycle management (initialize, execute, cleanup)
       - Extension system for customization
       - Type-safe execution with generics
       - Runnable integration with LangChain
       - Error handling and recovery
       - Resource management

   .. admonition:: Examples

      Creating a runtime component::
      
          from haive.core.runtime import RuntimeComponent
          from haive.core.engine import AugLLMConfig
      
          class LLMRuntime(RuntimeComponent[AugLLMConfig, str, str]):
              def invoke(self, input_data: str, config: RunnableConfig = None) -> str:
                  # Execute the LLM engine
                  return self.config.create_runnable().invoke(input_data, config)
      
          # Create and use runtime
          llm_config = AugLLMConfig(model="gpt-4")
          runtime = LLMRuntime(llm_config)
          result = runtime.invoke("Hello!")
      
      Using runtime extensions::
      
          from haive.core.runtime import ExtensionBase
      
          class LoggingExtension(ExtensionBase):
              def before_invoke(self, input_data, config):
                  logger.info(f"Executing with input: {input_data}")
      
              def after_invoke(self, result, config):
                  logger.info(f"Execution result: {result}")
      
          # Add extension to runtime
          runtime.add_extension(LoggingExtension())
      
      Custom runtime implementation::
      
          from haive.core.runtime import RuntimeProtocol
          from typing import TypeVar, Generic
      
          T = TypeVar('T')
      
          class CustomRuntime(Generic[T]):
              def __init__(self, config: T):
                  self.config = config
      
              def execute(self, input_data, **kwargs):
                  # Custom execution logic
                  return self.process(input_data)

   .. seealso::

      - Engine configuration documentation
      - LangChain Runnable interface
      - Extension development guide










Package Contents
----------------

.. rubric:: haive.core.runtime.__all__

.. autosummary::
   :nosignatures:

   haive.core.runtime.ExtensionBase   haive.core.runtime.ExtensionProtocol   haive.core.runtime.RuntimeComponent   haive.core.runtime.RuntimeProtocol

.. automodule:: haive.core.runtime
   :members:
   :undoc-members:
   :show-inheritance: