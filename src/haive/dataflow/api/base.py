from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, Union, List
from enum import Enum
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('.env')

# Import necessary LLM configurations
from src.haive.core.models.llm.base import (
    LLMConfig, AzureLLMConfig, OpenAILLMConfig, 
    AnthropicLLMConfig, GeminiLLMConfig, DeepSeekLLMConfig,
    MistralLLMConfig
)
from src.haive.core.aug_llm.base import AugLLMConfig
from src.haive.core.models.llm.provider_types import LLMProvider

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import BaseTool

import uvicorn
import traceback

# Create FastAPI app with more detailed metadata
app = FastAPI(
    title="Dynamic LLM Generation API",
    description="""
    A flexible API for generating responses using configurable Language Models (LLMs).
    
    ## Features
    - Support multiple LLM providers
    - Configurable system prompts
    - Dynamic temperature settings
    - Optional tool integration
    
    ## Supported Providers and Models
    ### Azure OpenAI
    - GPT-4 Turbo
    - gpt-35-turbo
    - gpt-35-turbo-16k
    - gpt-4-32k

    ### Anthropic
    - Claude 3.7 Sonnet
    - Claude 3.5 Haiku
    - Claude 3 Opus
    - Claude 3 Haiku

    ### Google Gemini
    - Gemini 2.5 Pro Experimental
    - Gemini API (Vertex AI)

    ### Mistral AI
    - Mistral Small 3.1 (24B)
    - Mistral Large 2 (123B)
    - Ministral 8B
    - Ministral 3B
    - Codestral Mamba (7B)

    ### DeepSeek
    - DeepSeek-R1
    - DeepSeek-R1-Zero
    - DeepSeek-R1-Distill (1.5–70B)
    - DeepSeek-V3-Base
    - DeepSeek-V3 Chat
    - DeepSeek-MoE Base (16B)
    - DeepSeek-MoE Chat (16B)
    - Mathstral (7B)
    """,
    version="1.0.0",
    contact={
        "name": "AI Solutions Team",
        "email": "ai-support@example.com",
    },
    license_info={
        "name": "MIT License",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Root route redirects to Swagger UI
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Predefined model mappings
AI_MODELS = {
    "azure": [
        "GPT-4 Turbo",
        "gpt-35-turbo",
        "gpt-35-turbo-16k",
        "gpt-4-32k",
        "gpt-4o",
    ],
    "anthropic": [
        "claude-3-7-sonnet-20250219",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-2.1",
        "claude-2.0"
    ],
     # Google Gemini models (2025 experimental releases)
     "gemini": [
      "gemini-pro",
      "gemini-pro-vision",
      "gemini-1.5-pro"
    ],
    "deepseek": [
      "deepseek-chat",
      "deepseek-reasoner",
      "deepseek-coder"],
    "mistralai": [
      "mistral-large-latest",
      "mistral-small-latest",
      #"mistral-8b-latest",
      #"mistral-3b-latest",
      #"codestral-mamba-latest"
    ]
}

class ToolConfig(BaseModel):
    """Configuration for a tool to be used with the LLM"""
    name: str = Field(..., description="Name of the tool", example="calculator")
    description: Optional[str] = Field(None, description="Description of the tool's functionality")
    result: Optional[str] = Field(None, description="Mock result for the tool (for demonstration)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "weather_tool",
                "description": "Retrieves current weather information",
                "result": "Sunny with 75°F in New York"
            }
        }
    )

class LLMConfigRequest(BaseModel):
    """Request model for LLM configuration"""
    provider: LLMProvider = Field(
        default=LLMProvider.AZURE,
        description="The LLM provider to use",
        examples=list(LLMProvider)
    )
    model: str = Field(
        default="gpt-4o", 
        description="Specific model to use from the selected provider",
        examples=[
            # Default models
            "gpt-4o", 
            "claude-3-opus", 
            "gpt-35-turbo", 
            "mistral-large-latest",
            # Dynamically add models from AI_MODELS
            *[model for models in AI_MODELS.values() for model in models]
        ]
    )
    api_key: Optional[str] = Field(
        default=None, 
        description="Optional API key for the selected provider. If not provided, will use environment variables."
    )
    temperature: Optional[float] = Field(
        default=0.7, 
        ge=0.0, 
        le=1.0, 
        description="Controls randomness in generation. Lower values make output more focused, higher values more random."
    )
    system_prompt: Optional[str] = Field(
        default="You are a helpful AI assistant.", 
        description="Initial instruction for the LLM to set its behavior"
    )
    extra_params: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional parameters to pass to the LLM"
    )
    tools: Optional[List[ToolConfig]] = Field(
        default=None, 
        description="Optional tools to be used by the LLM"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "provider": "azure",
                "model": "GPT-4 Turbo",
                "temperature": 0.7,
                "system_prompt": "You are a helpful assistant specializing in technical explanations.",
                "tools": [
                    {
                        "name": "code_explainer",
                        "description": "Explains complex code snippets",
                        "result": "Here's a breakdown of the code..."
                    }
                ]
            }
        }
    )

class LLMGenerationResponse(BaseModel):
    """Response model for LLM generation"""
    response: str = Field(..., description="Generated response from the LLM")
    model: str = Field(..., description="Model used for generation")
    provider: LLMProvider = Field(..., description="Provider of the LLM")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "Hello! How can I assist you today?",
                "model": "GPT-4 Turbo",
                "provider": "azure"
            }
        }
    )
def get_env_api_key(provider: LLMProvider) -> Optional[str]:
    """
    Retrieve API key from environment variables based on provider
    """
    env_key_map = {
        LLMProvider.AZURE.value: 'AZURE_OPENAI_API_KEY',
        LLMProvider.OPENAI.value: 'OPENAI_API_KEY',
        LLMProvider.ANTHROPIC.value: 'ANTHROPIC_API_KEY',
        LLMProvider.GEMINI.value: 'GOOGLE_API_KEY',
        LLMProvider.DEEPSEEK.value: 'DEEPSEEK_API_KEY',
        LLMProvider.MISTRALAI.value: 'MISTRAL_API_KEY',
    }
    
    # Get the environment variable name for the provider
    env_var = env_key_map.get(provider.value)
    
    # Return the API key if the environment variable exists
    return os.getenv(env_var) if env_var else None
@app.post(
    "/generate", 
    response_model=LLMGenerationResponse,
    summary="Generate a response using a configurable LLM",
    description="Generate a response by configuring an LLM with various parameters"
)
async def generate_response(
    request: LLMConfigRequest, 
    query: str = Query(..., description="The input query or message to generate a response for")
):
    """
    Generate a response using dynamically configured LLM
    
    Args:
        request: LLM configuration details
        query: User's input query
    """
    try:
        # Select the appropriate LLM configuration based on provider
        extra_params = request.extra_params or {}
        extra_params['temperature'] = request.temperature

        # Dynamic LLM config selection
        llm_config_map = {
            LLMProvider.AZURE.value: AzureLLMConfig,
            LLMProvider.OPENAI.value: OpenAILLMConfig,
            LLMProvider.ANTHROPIC.value: AnthropicLLMConfig,
            LLMProvider.GEMINI.value: GeminiLLMConfig,
            LLMProvider.DEEPSEEK.value: DeepSeekLLMConfig,
            LLMProvider.MISTRALAI.value: MistralLLMConfig,
        }

        # Get the configuration class
        LLMConfigClass = llm_config_map.get(request.provider.value)

        if not LLMConfigClass:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {request.provider}")

        # Determine API key - prioritize provided key, then environment variable
        api_key = request.api_key or get_env_api_key(request.provider)

        # Raise error if no API key is found
        if not api_key:
            raise HTTPException(
                status_code=401, 
                detail=f"No API key found for provider {request.provider}. "
                       "Please provide an API key or set the corresponding environment variable."
            )

        # Create LLM configuration
        llm_config = LLMConfigClass(
            model=request.model, 
            api_key=api_key,
            parameters=extra_params
        )

        # Create prompt template with system and human messages
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=request.system_prompt or "You are a helpful AI assistant."),
            MessagesPlaceholder(variable_name="messages")
        ])

        # Prepare AugLLMConfig
        aug_llm_config = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=prompt_template
        )

        # Add tools if provided
        if request.tools:
            # Convert tool configurations to actual tool objects
            from langchain_core.tools import Tool
            tools = []
            for tool_config in request.tools:
                tool = Tool(
                    name=tool_config.name,
                    description=tool_config.description or '',
                    func=lambda x: tool_config.result or 'Tool execution not implemented'
                )
                tools.append(tool)
            aug_llm_config.tools = tools

        # Create runnable
        runnable = aug_llm_config.create_runnable()

        # Generate response
        response = runnable.invoke({
            "messages": [HumanMessage(content=query)]
        })

        # Return the response content
        return LLMGenerationResponse(
            response=response.content if hasattr(response, 'content') else str(response),
            model=request.model,
            provider=request.provider
        )

    except HTTPException:
        # Re-raise HTTP exceptions as is
        raise
    except Exception as e:
        # Log the full traceback
        print(f"Error in generate_response: {e}")
        print(traceback.format_exc())
        
        # Raise an HTTP exception with more detailed error
        raise HTTPException(status_code=500, detail=str(e))

# Add tags for better Swagger UI organization
app.openapi()["tags"] = [
    {
        "name": "LLM Generation",
        "description": "Endpoints for generating responses using configurable Language Models"
    }
]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)