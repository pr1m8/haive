# Haive LLM Module

This module provides a comprehensive framework for working with Large Language Models (LLMs) from various providers. It includes configuration classes, metadata handling, and provider-specific implementations.

## Core Components

- **Base Classes**: Abstract base classes and interfaces for LLM configurations
- **Provider Support**: Implementations for 15+ LLM providers
- **Metadata System**: Comprehensive model capability and context window tracking
- **Security Features**: Secure handling of API keys and credentials
- **Caching System**: Response caching for efficiency

## Supported Providers

The module supports a wide range of LLM providers:

- **OpenAI**: GPT-4, GPT-3.5, etc.
- **Azure OpenAI**: Microsoft's hosted OpenAI services
- **Anthropic**: Claude models
- **Google**: Gemini models
- **Mistral AI**: Mistral models
- **DeepSeek**: DeepSeek models
- **Groq**: High-performance LLM API
- **Cohere**: Command models
- **Together AI**: Access to open models
- **Fireworks AI**: High-performance inference
- **Perplexity**: Sonar models
- **HuggingFace**: Open models via HF inference API
- **AI21**: Jurassic models
- **Aleph Alpha**: Luminous models
- **Others**: GooseAI, MosaicML, NLP Cloud, OpenLM, Petals, Replicate, and Vertex AI

## Usage Examples

### Creating an OpenAI LLM

```python
from haive.core.models.llm.base import OpenAILLMConfig

# Configure the LLM
config = OpenAILLMConfig(
    model="gpt-4o",
    cache_enabled=True
)

# Create the LLM
llm = config.instantiate()

# Generate text
response = llm.generate("Explain quantum computing in simple terms.")
```

### Using Azure OpenAI

```python
from haive.core.models.llm.base import AzureLLMConfig

config = AzureLLMConfig(
    model="gpt-4",  # This is the deployment name in Azure
    api_version="2024-02-15-preview",
    api_base="https://your-resource.openai.azure.com/"
)

llm = config.instantiate()
```

### Accessing Model Metadata

```python
from haive.core.models.llm.base import AnthropicLLMConfig

config = AnthropicLLMConfig(model="claude-3-opus-20240229")

# Get context window information
context_window = config.get_context_window()
max_input = config.get_max_input_tokens()
max_output = config.get_max_output_tokens()

# Check model capabilities
supports_vision = config.supports_vision
supports_function_calling = config.supports_function_calling

# Get pricing information
input_cost, output_cost = config.get_token_pricing()
```

## Model Metadata

The metadata system provides access to:

- Context window sizes (total, input, output)
- Token pricing information
- Model capabilities (vision, function calling, etc.)
- Supported modalities (text, image, audio)
- Deprecation dates
- And more

## Performance Considerations

- Response caching is enabled by default to avoid redundant API calls
- Context window awareness prevents token limit errors
- Debug mode provides detailed model information

## Security

API keys are handled securely via:

- Environment variable resolution with fallbacks
- SecretStr type for preventing accidental exposure
- Support for custom credential providers

## Extending with New Providers

To add a new LLM provider:

1. Add the provider to the `LLMProvider` enum in `provider_types.py`
2. Create a new configuration class extending `LLMConfig`
3. Implement the `instantiate()` method to return the appropriate LLM instance

Example:

```python
class NewProviderLLMConfig(LLMConfig):
    provider: LLMProvider = LLMProvider.NEW_PROVIDER
    model: str = Field(default="default-model")

    def instantiate(self, **kwargs) -> Any:
        from langchain_newprovider import ChatNewProvider

        return ChatNewProvider(
            model=self.model,
            api_key=self.get_api_key(),
            **kwargs
        )
```
