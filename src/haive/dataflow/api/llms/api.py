"""
API endpoints for LLM model information and availability.

This module provides FastAPI endpoints to access and manage LLM model data
stored in Supabase. It helps bridge the client application with the database
while providing additional server-side logic.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from src.api.api.llms.models import Provider, Model, ModelCapabilities, Pricing, SearchPricing
# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="LLM Model API", description="API for LLM model information and availability")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")  # Use anon key for client-side access

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not found in environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



# Helper functions
def get_providers() -> List[Provider]:
    """Get all providers from the database."""
    response = supabase.table("llm_providers").select("*").execute()
    if hasattr(response, "data"):
        return [Provider(**p) for p in response.data]
    return []

def get_models(provider: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all models from the database.
    
    Args:
        provider: Optional provider name to filter by
    
    Returns:
        List of models with their capabilities and pricing
    """
    # Start with base query
    query = supabase.table("llm_models").select("*")
    
    # Add provider filter if provided
    if provider:
        query = query.eq("provider", provider)
    
    # Execute query
    response = query.execute()
    
    if not hasattr(response, "data"):
        return []
    
    # Extract model data
    models = response.data
    
    # Create a enriched model list with capabilities and pricing
    enriched_models = []
    
    for model in models:
        model_id = model["model_id"]
        
        # Get capabilities
        cap_response = supabase.table("llm_model_capabilities").select("*").eq("model_id", model_id).execute()
        capabilities = cap_response.data[0] if cap_response.data else {}
        
        # Get pricing
        price_response = supabase.table("llm_pricing").select("*").eq("model_id", model_id).execute()
        pricing = price_response.data[0] if price_response.data else {}
        
        # Get search pricing if applicable
        search_response = supabase.table("llm_search_pricing").select("*").eq("model_id", model_id).execute()
        search_pricing = search_response.data[0] if search_response.data else {}
        
        # Combine all data
        enriched_model = {
            **model,
            "capabilities": capabilities,
            "pricing": pricing,
            "search_pricing": search_pricing
        }
        
        enriched_models.append(enriched_model)
    
    return enriched_models

def get_model_by_id(model_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific model by ID with all related information.
    
    Args:
        model_id: The model ID to look up
    
    Returns:
        Model data with capabilities and pricing, or None if not found
    """
    # Get model
    model_response = supabase.table("llm_models").select("*").eq("model_id", model_id).execute()
    
    if not model_response.data:
        return None
    
    model = model_response.data[0]
    
    # Get capabilities
    cap_response = supabase.table("llm_model_capabilities").select("*").eq("model_id", model_id).execute()
    capabilities = cap_response.data[0] if cap_response.data else {}
    
    # Get pricing
    price_response = supabase.table("llm_pricing").select("*").eq("model_id", model_id).execute()
    pricing = price_response.data[0] if price_response.data else {}
    
    # Get search pricing if applicable
    search_response = supabase.table("llm_search_pricing").select("*").eq("model_id", model_id).execute()
    search_pricing = search_response.data[0] if search_response.data else {}
    
    # Combine all data
    enriched_model = {
        **model,
        "capabilities": capabilities,
        "pricing": pricing,
        "search_pricing": search_pricing
    }
    
    return enriched_model

# API endpoints
@app.get("/providers", response_model=List[Provider], tags=["providers"])
async def read_providers():
    """Get all LLM providers."""
    return get_providers()

@app.get("/models", response_model=List[Dict[str, Any]], tags=["models"])
async def read_models(provider: Optional[str] = None, capability: Optional[str] = None):
    """
    Get all models with optional filtering.
    
    Args:
        provider: Filter by provider name
        capability: Filter by capability (e.g., 'vision', 'function_calling')
    """
    models = get_models(provider)
    
    # Additional filtering by capability if requested
    if capability:
        capability_key = f"supports_{capability}"
        filtered_models = []
        
        for model in models:
            if (model.get("capabilities") and 
                model["capabilities"].get(capability_key) == True):
                filtered_models.append(model)
        
        return filtered_models
    
    return models

@app.get("/models/{model_id}", response_model=Dict[str, Any], tags=["models"])
async def read_model(model_id: str):
    """Get a specific model by ID."""
    model = get_model_by_id(model_id)
    
    if not model:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
    
    return model

@app.get("/models/recommended", response_model=List[Dict[str, Any]], tags=["models"])
async def recommended_models(
    task: Optional[str] = None,
    vision: Optional[bool] = False,
    function_calling: Optional[bool] = False,
    audio: Optional[bool] = False,
    web_search: Optional[bool] = False
):
    """
    Get recommended models based on capabilities and task requirements.
    
    Args:
        task: The type of task (chat, completion, embedding, etc.)
        vision: Whether vision capabilities are required
        function_calling: Whether function calling is required
        audio: Whether audio processing is required
        web_search: Whether web search is required
    """
    # Get all models
    all_models = get_models()
    
    # Filter by task (mode)
    if task:
        all_models = [m for m in all_models if m.get("mode") == task]
    
    # Start with capabilities filtering
    filtered_models = []
    
    for model in all_models:
        capabilities = model.get("capabilities", {})
        
        # Skip if model doesn't meet capability requirements
        if vision and not capabilities.get("supports_vision", False):
            continue
        
        if function_calling and not capabilities.get("supports_function_calling", False):
            continue
            
        if audio and not (capabilities.get("supports_audio_input", False) or 
                          capabilities.get("supports_audio_output", False)):
            continue
            
        if web_search and not capabilities.get("supports_web_search", False):
            continue
        
        # Check if provider is available
        provider_response = supabase.table("llm_providers").select("is_available").eq("name", model["provider"]).execute()
        if provider_response.data and not provider_response.data[0].get("is_available", False):
            # Mark as unavailable but still include
            model["is_available"] = False
        else:
            model["is_available"] = True
        
        filtered_models.append(model)
    
    # Sort: available models first, then by cost (lower is better)
    sorted_models = sorted(
        filtered_models,
        key=lambda x: (
            not x.get("is_available", True),  # Available models first
            x.get("pricing", {}).get("output_cost_per_token", 9999)  # Lower cost is better
        )
    )
    
    return sorted_models

@app.get("/capabilities", tags=["capabilities"])
async def get_capabilities():
    """Get all possible LLM capabilities."""
    return {
        "capabilities": [
            "function_calling",
            "parallel_function_calling",
            "vision",
            "audio_input",
            "audio_output",
            "prompt_caching",
            "response_schema",
            "system_messages",
            "web_search",
            "tool_choice"
        ]
    }

@app.get("/modes", tags=["modes"])
async def get_modes():
    """Get all possible LLM operation modes."""
    response = supabase.table("llm_models").select("mode").execute()
    
    if not hasattr(response, "data"):
        return {"modes": []}
    
    # Extract unique modes
    modes = list(set(item["mode"] for item in response.data if item.get("mode")))
    
    return {"modes": modes}

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)