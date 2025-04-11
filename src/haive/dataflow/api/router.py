# src/haive/api/router.py
from fastapi import APIRouter, HTTPException, Body, Query, Path, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, Any, List, Optional
import uuid
import json
import logging

from src.api.api.registry import agent_registry

logger = logging.getLogger(__name__)

def create_agent_router(prefix: str = "/agents") -> APIRouter:
    """Create a FastAPI router for interacting with agents."""
    router = APIRouter(prefix=prefix, tags=["agents"])
    
    # List available agents
    @router.get("/")
    async def list_agents():
        """List all available agent configurations."""
        return {"agents": agent_registry.list_available_agents()}
    
    # Get agent information
    @router.get("/{agent_name}")
    async def get_agent_info(agent_name: str):
        """Get information about a specific agent configuration."""
        config_class = agent_registry.get_agent_config(agent_name)
        if not config_class:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        # Return basic info about the agent
        config_info = {
            "name": agent_name,
            "config_class": config_class.__name__,
            "description": getattr(config_class, "__doc__", "No description available")
        }
        
        # Try to extract fields from the config class
        try:
            from inspect import signature
            sig = signature(config_class.__init__)
            params = {}
            for name, param in sig.parameters.items():
                if name not in ["self", "args", "kwargs"]:
                    params[name] = {
                        "required": param.default == param.empty,
                        "default": None if param.default == param.empty else param.default,
                        "type": str(param.annotation)
                    }
            config_info["parameters"] = params
        except Exception as e:
            logger.debug(f"Error extracting parameters: {e}")
        
        return config_info
    
    # Create a new thread
    @router.post("/{agent_name}/threads")
    async def create_thread(
        agent_name: str,
        config: Dict[str, Any] = Body({}, description="Agent configuration parameters"),
        initial_state: Optional[Dict[str, Any]] = Body(None, description="Optional initial state")
    ):
        """Create a new thread with optional configuration and initial state."""
        agent = agent_registry.get_or_create_agent(agent_name, **config)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        thread_id = str(uuid.uuid4())
        
        # Initialize thread with initial state if provided
        if initial_state:
            try:
                await agent.arun(input_data=initial_state, thread_id=thread_id)
            except Exception as e:
                logger.error(f"Error initializing thread: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        return {
            "thread_id": thread_id,
            "agent_name": agent_name,
            "config": config
        }
    
    # Get thread state
    @router.get("/{agent_name}/threads/{thread_id}")
    async def get_thread_state(
        agent_name: str,
        thread_id: str,
        config: Dict[str, Any] = Body({}, description="Agent configuration parameters")
    ):
        """Get the current state of a thread."""
        agent = agent_registry.get_or_create_agent(agent_name, thread_id=thread_id, **config)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        try:
            # Create runtime config with thread_id
            runtime_config = {
                "configurable": {"thread_id": thread_id}
            }
            
            # Get state using the runtime config
            state = agent.app.get_state(runtime_config)
            if not state:
                raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found")
            
            return state
        except Exception as e:
            logger.error(f"Error getting thread state: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Run agent with input
    @router.post("/{agent_name}/threads/{thread_id}/run")
    async def run_agent(
        agent_name: str,
        thread_id: str,
        input_data: Dict[str, Any] = Body(..., description="Input data for the agent"),
        stream: bool = Query(False, description="Whether to stream the response"),
        config: Dict[str, Any] = Body({}, description="Agent configuration parameters")
    ):
        """Run the agent with the given input data."""
        agent = agent_registry.get_or_create_agent(agent_name, thread_id=thread_id, **config)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        # Handle streaming request
        if stream:
            async def stream_generator():
                try:
                    async for chunk in agent.astream(
                        input_data=input_data,
                        thread_id=thread_id,
                        stream_mode="updates"
                    ):
                        yield f"data: {json.dumps(chunk)}\n\n"
                    
                    # Send a final "done" message
                    yield f"data: {json.dumps({'done': True, 'thread_id': thread_id})}\n\n"
                except Exception as e:
                    logger.error(f"Error streaming agent response: {e}")
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            return StreamingResponse(
                stream_generator(),
                media_type="text/event-stream"
            )
        
        # Non-streaming response
        try:
            result = await agent.arun(
                input_data=input_data,
                thread_id=thread_id
            )
            return result
        except Exception as e:
            logger.error(f"Error running agent {agent_name}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Convenience endpoint for text input
    @router.post("/{agent_name}/threads/{thread_id}/text")
    async def send_text(
        agent_name: str,
        thread_id: str,
        text: str = Body(..., embed=True, description="Text input"),
        stream: bool = Query(False, description="Whether to stream the response"),
        config: Dict[str, Any] = Body({}, description="Agent configuration parameters")
    ):
        """Send text input to the agent."""
        agent = agent_registry.get_or_create_agent(agent_name, thread_id=thread_id, **config)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        # Try to determine the right format for this agent
        input_data = {}
        
        # Check if agent has a messages field in state schema
        has_messages = False
        if hasattr(agent, 'state_schema') and hasattr(agent.state_schema, '__annotations__'):
            has_messages = 'messages' in agent.state_schema.__annotations__
        
        # Format appropriately
        if has_messages:
            from langchain_core.messages import HumanMessage
            input_data = {"messages": [HumanMessage(content=text)]}
        else:
            # Try common input field names
            for field in ['input', 'text', 'query', 'content']:
                if hasattr(agent, 'state_schema') and hasattr(agent.state_schema, '__annotations__') and field in agent.state_schema.__annotations__:
                    input_data = {field: text}
                    break
            
            # Default fallback
            if not input_data:
                input_data = {"input": text}
        
        # Run the agent with the formatted input
        return await run_agent(agent_name, thread_id, input_data, stream, config)

    # Get agent types
    @router.get("/types")
    async def get_agent_types():
        """Get all agent types."""
        if hasattr(agent_registry, 'db') and agent_registry.db_connection:
            try:
                with agent_registry.db.connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM ai.agent_types ORDER BY name"
                    )
                    types = [{"id": row[0], "name": row[1], "description": row[2]} 
                            for row in cursor.fetchall()]
                    return {"types": types}
            except Exception as e:
                logger.error(f"Error getting agent types: {e}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        else:
            # Fallback to in-memory tracking
            return {
                "types": [
                    {"name": "agent", "description": "Standard agent"},
                    {"name": "game", "description": "Game agent"}
                ]
            }

    # Get agents by type
    @router.get("/by-type/{agent_type}")
    async def get_agents_by_type(agent_type: str):
        """Get all agents of a specific type."""
        if hasattr(agent_registry, 'db') and agent_registry.db_connection:
            try:
                configs = agent_registry.db.get_agent_configs(agent_type)
                return {"agents": configs}
            except Exception as e:
                logger.error(f"Error getting agents by type: {e}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        else:
            # Fallback to in-memory tracking
            agents = agent_registry.list_agents_by_type(agent_type)
            return {"agents": agents}

    # Get all agent configs from database
    @router.get("/configs")
    async def get_agent_configs():
        """Get all agent configurations from the database."""
        if hasattr(agent_registry, 'db') and agent_registry.db_connection:
            try:
                configs = agent_registry.db.get_agent_configs()
                return {"configs": configs}
            except Exception as e:
                logger.error(f"Error getting agent configs: {e}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        else:
            # Fallback to in-memory data
            configs = []
            for name, info in agent_registry.agent_configs.items():
                config_class = info['class']
                configs.append({
                    "name": name,
                    "class_name": config_class.__name__,
                    "module_path": config_class.__module__,
                    "agent_type": info['type'],
                    "description": getattr(config_class, "__doc__", "")
                })
            return {"configs": configs}
    return router

