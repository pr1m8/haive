LLM Models
==========

Language model configurations and providers.

Module path: ``haive.core.models.llm``

Overview
--------

The LLM module provides a unified interface for various language models:

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3 family)
- Google (Gemini)
- Local models (Ollama, LlamaCpp)
- Custom endpoints

Model Configuration
-------------------

.. code-block:: python

   from haive.core.models.llm import LLMConfig, LLMProvider
   
   # OpenAI configuration
   openai_config = LLMConfig(
       provider=LLMProvider.OPENAI,
       model="gpt-4o",
       temperature=0.7,
       max_tokens=2000,
       api_key="sk-..."  # Or use env: OPENAI_API_KEY
   )
   
   # Anthropic configuration
   claude_config = LLMConfig(
       provider=LLMProvider.ANTHROPIC,
       model="claude-3-opus-20240229",
       temperature=0.5,
       max_tokens=4000,
       api_key="..."  # Or use env: ANTHROPIC_API_KEY
   )
   
   # Local Ollama
   ollama_config = LLMConfig(
       provider=LLMProvider.OLLAMA,
       model="llama2:70b",
       base_url="http://localhost:11434"
   )

Structured Output
-----------------

LLMs can generate structured outputs using Pydantic models:

.. code-block:: python

   from pydantic import BaseModel
   from haive.core.models.llm import create_llm
   
   class Analysis(BaseModel):
       sentiment: str
       confidence: float
       keywords: list[str]
   
   llm = create_llm(config)
   
   # Generate structured output
   result = await llm.agenerate_structured(
       prompt="Analyze this text: 'Haive is amazing!'",
       output_schema=Analysis
   )
   # result is an Analysis instance

Model Registry
--------------

.. code-block:: python

   from haive.core.models.llm import LLMRegistry
   
   # Register custom model
   LLMRegistry.register(
       name="my-custom-model",
       provider=LLMProvider.CUSTOM,
       config={
           "base_url": "https://api.mymodel.com",
           "headers": {"Authorization": "Bearer ..."}
       }
   )
   
   # Use registered model
   llm = LLMRegistry.get("my-custom-model")

Streaming Support
-----------------

.. code-block:: python

   # Stream responses
   async for chunk in llm.astream("Tell me a story"):
       print(chunk.content, end="")

Cost Tracking
-------------

.. code-block:: python

   from haive.core.models.llm import TokenUsage
   
   # Track token usage
   response = await llm.agenerate("Hello")
   usage = response.usage
   
   print(f"Prompt tokens: {usage.prompt_tokens}")
   print(f"Completion tokens: {usage.completion_tokens}")
   print(f"Estimated cost: ${usage.estimated_cost}")

Available Models
----------------

**OpenAI:**
- gpt-4o, gpt-4o-mini
- gpt-4-turbo, gpt-4
- gpt-3.5-turbo

**Anthropic:**
- claude-3-opus, claude-3-sonnet, claude-3-haiku
- claude-2.1, claude-2

**Google:**
- gemini-1.5-pro, gemini-1.5-flash
- gemini-1.0-pro

**Open Source (via Ollama):**
- llama2, llama3, mistral, mixtral
- phi-2, neural-chat, starling-lm

Module Documentation
--------------------

.. automodule:: haive.core.models.llm
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

.. autosummary::
   :nosignatures:
   :toctree: _autosummary
   
   LLMConfig
   LLMProvider
   LLMRegistry
   TokenUsage

Functions
---------

.. autosummary::
   :nosignatures:
   :toctree: _autosummary
   
   create_llm
   get_model_info

See Also
--------

- :doc:`/api/haive/core/engine/aug_llm` - Augmented LLM engine
- :doc:`/api/haive/core/models/index` - Models overview
- :doc:`/guides/core_concepts` - Core concepts guide