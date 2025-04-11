# src/haive/api/app.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.api.registry import agent_registry
from src.api.api.router import create_agent_router
from langgraph.prebuilt import T
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(
        title="Haive Agent API",
        description="Universal API for interacting with Haive agents",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update with proper origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Discover and register all agents
    search_paths = ["src.haive.agents", "src.haive.games"]
    agent_registry.discover_agents(search_paths)
    logger.info(f"Discovered agents: {agent_registry.list_available_agents()}")
    
    # Include the agent router
    app.include_router(create_agent_router())
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting Haive Agent API")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Haive Agent API")
    
    return app

# Main application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8500)
