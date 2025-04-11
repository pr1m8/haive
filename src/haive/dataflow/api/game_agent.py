from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, create_model
from typing import Dict, List, Optional, Any, Union, Type, Generic, TypeVar, Callable
import uuid
import asyncio
import json
import logging
from datetime import datetime
import inspect
import importlib

# Import persistence components
from src.haive.core.engine.agent.persistence.postgres_config import PostgresCheckpointerConfig
from src.haive.core.engine.agent.persistence.memory_config import MemoryCheckpointerConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent-api")

# Type variables for generics
T = TypeVar('T')  # Agent type
S = TypeVar('S')  # Agent config type

# =============================================
# Data Models
# =============================================

class AgentRequest(BaseModel):
    """Base model for agent requests"""
    thread_id: Optional[str] = None
    persistence_type: str = "postgres"
    config_overrides: Optional[Dict[str, Any]] = None
    initial_state: Optional[Dict[str, Any]] = None

from datetime import datetime
from pydantic import BaseModel, Field

class AgentResponseBase(BaseModel):
    thread_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class CheckpointInfo(BaseModel):
    """Information about a checkpoint"""
    thread_id: str
    checkpoint_id: str
    checkpoint_ns: Optional[str] = None
    parent_checkpoint_id: Optional[str] = None
    type: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

# =============================================
# Agent Manager Class
# =============================================

class AgentManager:
    """Manages agent instances and database connections"""
    
    def __init__(self, 
                 agent_class: Type,
                 config_class: Type,
                 default_persistence: str = "postgres"):
        """Initialize the agent manager"""
        self.agent_class = agent_class
        self.config_class = config_class
        self.default_persistence = default_persistence
        self.agents = {}  # thread_id -> agent instance
        self.active_connections = set()
        self.connection_thread_map = {}
        
    def get_or_create_agent(self, thread_id: str, config_overrides: Optional[Dict[str, Any]] = None) -> Any:
        """Get or create an agent for a thread ID"""
        if thread_id in self.agents:
            return self.agents[thread_id]
        
        # Configure persistence
        persistence_type = config_overrides.get("persistence_type", self.default_persistence) if config_overrides else self.default_persistence
        
        if persistence_type == "postgres":
            # Configure Postgres persistence
            db_config = config_overrides.get("db_config", {}) if config_overrides else {}
            persistence_config = PostgresCheckpointerConfig(
                db_host=db_config.get("db_host", "localhost"),
                db_port=db_config.get("db_port", 5432),
                db_name=db_config.get("db_name", "postgres"),
                db_user=db_config.get("db_user", "postgres"),
                db_pass=db_config.get("db_pass", "postgres"),
                ssl_mode=db_config.get("ssl_mode", "disable"),
                setup_needed=True,
            )
        else:
            # Use memory persistence
            persistence_config = MemoryCheckpointerConfig()
            
        # Create config with overrides
        config_kwargs = {
            "name": f"agent_{thread_id[:8]}",
            "persistence": persistence_config,
            "runnable_config": {
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 100
            }
        }
        
        # Apply any additional config overrides
        if config_overrides:
            for key, value in config_overrides.items():
                if key not in ["persistence_type", "db_config"]:
                    config_kwargs[key] = value
        
        # Create agent config
        config = self.config_class(**config_kwargs)
        
        # Create and cache agent
        agent = self.agent_class(config=config)
        self.agents[thread_id] = agent
        
        return agent
    
    def register_connection(self, websocket: WebSocket, thread_id: str):
        """Register a WebSocket connection"""
        self.active_connections.add(websocket)
        self.connection_thread_map[websocket] = thread_id
        
    def unregister_connection(self, websocket: WebSocket):
        """Unregister a WebSocket connection"""
        self.active_connections.discard(websocket)
        if websocket in self.connection_thread_map:
            del self.connection_thread_map[websocket]
    
    def get_agent_for_connection(self, websocket: WebSocket) -> Optional[Any]:
        """Get the agent for a WebSocket connection"""
        thread_id = self.connection_thread_map.get(websocket)
        if thread_id:
            return self.agents.get(thread_id)
        return None
    
    def get_active_threads(self) -> List[str]:
        """Get list of active thread IDs"""
        return list(self.agents.keys())
    
    def cleanup(self, thread_id: Optional[str] = None):
        """Clean up resources"""
        if thread_id:
            # Clean up specific thread
            if thread_id in self.agents:
                agent = self.agents[thread_id]
                if hasattr(agent, "checkpointer") and hasattr(agent.checkpointer, "conn"):
                    try:
                        agent.checkpointer.conn.close()
                    except:
                        pass
                del self.agents[thread_id]
        else:
            # Clean up all
            for agent in self.agents.values():
                if hasattr(agent, "checkpointer") and hasattr(agent.checkpointer, "conn"):
                    try:
                        agent.checkpointer.conn.close()
                    except:
                        pass
            self.agents = {}

# =============================================
# Database Utilities
# =============================================

class CheckpointDB:
    """Utilities for working with checkpoint database"""
    
    @staticmethod
    async def get_checkpoints(thread_id: str) -> List[CheckpointInfo]:
        """Get checkpoints for a thread"""
        import psycopg
        
        try:
            with psycopg.connect("dbname=postgres user=postgres password=postgres") as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT thread_id, id as checkpoint_id, checkpoint_ns, 
                               parent_id as parent_checkpoint_id, type,
                               metadata, created_at
                        FROM checkpoints
                        WHERE thread_id = %s
                        ORDER BY created_at DESC
                    """, (thread_id,))
                    
                    results = []
                    for row in cur.fetchall():
                        results.append(CheckpointInfo(
                            thread_id=row[0],
                            checkpoint_id=row[1],
                            checkpoint_ns=row[2],
                            parent_checkpoint_id=row[3],
                            type=row[4],
                            metadata=row[5],
                            created_at=row[6]
                        ))
                    
                    return results
        except Exception as e:
            logger.error(f"Error getting checkpoints: {e}")
            return []
    
    @staticmethod
    async def get_threads() -> List[Dict[str, Any]]:
        """Get all threads in the database"""
        import psycopg
        
        try:
            with psycopg.connect("dbname=postgres user=postgres password=postgres") as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT thread_id, name, metadata, created_at
                        FROM threads
                        ORDER BY created_at DESC
                    """)
                    
                    results = []
                    for row in cur.fetchall():
                        results.append({
                            "thread_id": row[0],
                            "name": row[1],
                            "metadata": row[2],
                            "created_at": row[3]
                        })
                    
                    return results
        except Exception as e:
            logger.error(f"Error getting threads: {e}")
            return []

# =============================================
# Generic Agent API Class
# =============================================

class GenericAgentAPI(Generic[T, S]):
    """Generic API framework for any agent type"""
    
    def __init__(self, 
                 app_name: str,
                 agent_class: Type[T],
                 config_class: Type[S],
                 state_schema: Optional[Type[BaseModel]] = None,
                 response_model: Optional[Type[BaseModel]] = None,
                 default_persistence: str = "postgres"):
        """
        Initialize the API framework.
        
        Args:
            app_name: Name of the API
            agent_class: Agent class to instantiate
            config_class: Agent config class to instantiate
            state_schema: Schema for agent state 
            response_model: Pydantic model for API responses
            default_persistence: Default persistence type ("postgres" or "memory")
        """
        self.app_name = app_name
        self.agent_class = agent_class
        self.config_class = config_class
        self.state_schema = state_schema
        self.response_model = response_model or AgentResponse
        self.default_persistence = default_persistence.lower()
        
        # Initialize FastAPI
        self.app = FastAPI(title=f"{app_name} API", version="1.0.0")
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Adjust for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Create agent manager
        self.agent_manager = AgentManager(
            agent_class=self.agent_class,
            config_class=self.config_class,
            default_persistence=self.default_persistence
        )
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register API routes"""
        app = self.app  # For convenience
        
        @app.post("/agents/", response_model=self.response_model)
        async def create_agent(request: AgentRequest):
            """Create a new agent instance"""
            try:
                # Generate thread ID if not provided
                thread_id = request.thread_id or f"{self.app_name}_{uuid.uuid4().hex[:8]}"
                
                # Create agent
                agent = self.agent_manager.get_or_create_agent(
                    thread_id=thread_id,
                    config_overrides=request.config_overrides
                )

                # Use provided initial state, or derive from schema if supported
                if request.initial_state:
                    input_state = request.initial_state
                elif self.state_schema and hasattr(self.state_schema, "initialize") and callable(getattr(self.state_schema, "initialize")):
                    input_state = self.state_schema.initialize().model_dump()
                else:
                    input_state = {}

                # Run agent to initialize
                state = agent.run(input_state, thread_id=thread_id)

                return {
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now()
                }

            except Exception as e:
                logger.error(f"Error creating agent: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")

                
        @app.post("/agents/{thread_id}/run", response_model=self.response_model)
        async def run_agent(thread_id: str, input_data: Dict[str, Any]):
            """Run agent with input data"""
            try:
                # Get or create agent
                agent = self.agent_manager.get_or_create_agent(thread_id)
                input_data = self.state_schema.initialize()
                # Run agent
                state = agent.run(input_data, thread_id=thread_id)
                
                # Return response
                return {
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now()
                }
                
            except Exception as e:
                logger.error(f"Error running agent: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error running agent: {str(e)}")
        
        @app.get("/agents/{thread_id}", response_model=self.response_model)
        async def get_agent_state(thread_id: str):
            """Get current agent state"""
            try:
                # Get or create agent
                agent = self.agent_manager.get_or_create_agent(thread_id)
                
                # Get current state
                state = agent.run({}, thread_id=thread_id)
                
                # Return response
                return {
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now()
                }
                
            except Exception as e:
                logger.error(f"Error getting agent state: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error getting agent state: {str(e)}")
        
        @app.get("/threads/", response_model=List[Dict[str, Any]])
        async def get_threads():
            """Get all threads"""
            try:
                return await CheckpointDB.get_threads()
            except Exception as e:
                logger.error(f"Error getting threads: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error getting threads: {str(e)}")
        
        @app.get("/threads/{thread_id}/checkpoints", response_model=List[CheckpointInfo])
        async def get_thread_checkpoints(thread_id: str):
            """Get checkpoints for a thread"""
            try:
                return await CheckpointDB.get_checkpoints(thread_id)
            except Exception as e:
                logger.error(f"Error getting checkpoints: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error getting checkpoints: {str(e)}")
        
        @app.websocket("/ws/agents/{thread_id}")
        async def websocket_endpoint(websocket: WebSocket, thread_id: str):
            """WebSocket endpoint for real-time agent updates"""
            await websocket.accept()
            
            try:
                # Register connection
                self.agent_manager.register_connection(websocket, thread_id)
                
                # Get or create agent
                agent = self.agent_manager.get_or_create_agent(thread_id)
                
                # Send initial state
                state = agent.run({}, thread_id=thread_id)
                await websocket.send_json({
                    "type": "state_update",
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Main WebSocket loop
                while True:
                    # Wait for messages
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Process message
                    if message["type"] == "run":
                        # Run agent with input
                        input_data = message.get("input", {})
                        state = agent.run(input_data, thread_id=thread_id)
                        
                        # Send updated state
                        await websocket.send_json({
                            "type": "state_update",
                            "thread_id": thread_id,
                            "state": state,
                            "timestamp": datetime.now().isoformat()
                        })
                    
                    elif message["type"] == "get_state":
                        # Get current state
                        state = agent.run({}, thread_id=thread_id)
                        
                        # Send state
                        await websocket.send_json({
                            "type": "state_update",
                            "thread_id": thread_id,
                            "state": state,
                            "timestamp": datetime.now().isoformat()
                        })
                    
            except WebSocketDisconnect:
                # Handle disconnection
                self.agent_manager.unregister_connection(websocket)
                logger.info(f"Client disconnected from agent {thread_id}")
                
            except Exception as e:
                # Handle other errors
                self.agent_manager.unregister_connection(websocket)
                logger.error(f"WebSocket error: {e}", exc_info=True)
                
                # Try to send error message
                try:
                    await websocket.send_json({
                        "type": "error",
                        "thread_id": thread_id,
                        "message": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
                except:
                    pass
        
        @app.on_event("startup")
        async def startup_event():
            """Startup event handler"""
            logger.info(f"{self.app_name} API starting up")
        
        @app.on_event("shutdown")
        async def shutdown_event():
            """Shutdown event handler"""
            logger.info(f"{self.app_name} API shutting down")
            
            # Clean up resources
            self.agent_manager.cleanup()
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the API server"""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)