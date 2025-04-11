from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime
import json
import logging
import uuid
import asyncio
# Import generic API framework
from src.api.api.game_agent import GenericAgentAPI, AgentResponseBase

# Import Connect4 components
from src.haive.games.connect4.agent import Connect4Agent
from src.haive.games.connect4.config import Connect4AgentConfig
from src.haive.games.connect4.state import Connect4State
from src.haive.games.connect4.models import Connect4Move

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("connect4-api")

# =============================================
# Connect4 Specific Models
# =============================================

class Connect4MoveRequest(BaseModel):
    """Request to make a move in Connect4"""
    column: int = Field(..., description="Column index (0-6) for the move")
    explanation: Optional[str] = Field(None, description="Optional explanation for the move")

class Connect4Request(BaseModel):
    """Request to create new Connect4 game"""
    thread_id: Optional[str] = None
    persistence_type: str = "postgres"
    config_overrides: Optional[Dict[str, Any]] = None
    first_player: Literal["red", "yellow"] = "red"
    enable_analysis: bool = True

class Connect4Response(AgentResponseBase):
    """Response for Connect4 game"""
    board: List[List[Optional[str]]]
    turn: str
    winner: Optional[str]
    game_status: str
    move_history: List[Dict[str, Any]]
    red_analysis: Optional[List[Dict[str, Any]]]
    yellow_analysis: Optional[List[Dict[str, Any]]]
    error_message: Optional[str]

# =============================================
# Connect4 API Class
# =============================================

class Connect4API(GenericAgentAPI[Connect4Agent, Connect4AgentConfig]):
    """API for Connect4 agent"""
    
    def __init__(self):
        super().__init__(
            app_name="Connect4",
            agent_class=Connect4Agent,
            config_class=Connect4AgentConfig,
            state_schema=Connect4State,
            response_model=Connect4Response,
            default_persistence="postgres"
        )
        
        # Register additional Connect4-specific routes
        self._register_connect4_routes()
    
    def _register_connect4_routes(self):
        """Register Connect4-specific routes"""
        app = self.app
        
        @app.post("/games/", response_model=Connect4Response)
        async def create_game(request: Connect4Request):
            """Create a new Connect4 game"""
            try:
                # Generate thread ID if not provided
                thread_id = request.thread_id or f"connect4_{uuid.uuid4().hex[:8]}"
                
                # Create agent
                agent = self.agent_manager.get_or_create_agent(
                    thread_id=thread_id,
                    config_overrides={
                        "enable_analysis": request.enable_analysis,
                        **(request.config_overrides or {})
                    }
                )
                
                # Initialize game state
                initial_state = {
                    "board": [[None for _ in range(7)] for _ in range(6)],
                    "turn": request.first_player,
                    "move_history": [],
                    "red_analysis": [],
                    "yellow_analysis": [],
                    "game_status": "ongoing",
                    "winner": None,
                    "captured": None,
                    "error_message": None
                }
                
                # Run agent to initialize
                state = agent.run(initial_state, thread_id=thread_id)
                
                # Return response
                return {
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now(),
                    **state
                }
                
            except Exception as e:
                logger.error(f"Error creating Connect4 game: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error creating Connect4 game: {str(e)}")
        
        @app.post("/games/{thread_id}/move", response_model=Connect4Response)
        async def make_move(thread_id: str, move: Connect4MoveRequest):
            """Make a move in a Connect4 game"""
            try:
                # Get agent
                agent = self.agent_manager.get_or_create_agent(thread_id)
                
                # Create move request
                move_data = {
                    "move": {
                        "column": move.column,
                        "explanation": move.explanation
                    }
                }
                
                # Make move
                state = agent.run(move_data, thread_id=thread_id)
                
                # Return response
                return {
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now(),
                    **state
                }
                
            except Exception as e:
                logger.error(f"Error making Connect4 move: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error making Connect4 move: {str(e)}")
        
        @app.get("/games/{thread_id}/ai-move", response_model=Connect4Response)
        async def make_ai_move(thread_id: str):
            """Let AI make a move in Connect4 game"""
            try:
                # Get agent
                agent = self.agent_manager.get_or_create_agent(thread_id)
                
                # AI makes a move (empty input triggers AI move)
                state = agent.run({}, thread_id=thread_id)
                
                # Return response
                return {
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now(),
                    **state
                }
                
            except Exception as e:
                logger.error(f"Error making AI move: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error making AI move: {str(e)}")
        
        @app.get("/games/{thread_id}", response_model=Connect4Response)
        async def get_game(thread_id: str):
            """Get the current state of a Connect4 game"""
            try:
                # Get agent
                agent = self.agent_manager.get_or_create_agent(thread_id)
                
                # Get current state
                state = agent.run({}, thread_id=thread_id)
                
                # Return response
                return {
                    "thread_id": thread_id,
                    "state": state,
                    "timestamp": datetime.now(),
                    **state
                }
                
            except Exception as e:
                logger.error(f"Error getting Connect4 game: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error getting Connect4 game: {str(e)}")
        
        @app.get("/games/", response_model=List[Dict[str, Any]])
        async def list_games():
            """List all Connect4 games"""
            try:
                from src.api.api.game_agent import CheckpointDB  # ensure this is imported

                return await CheckpointDB.get_threads()

            except Exception as e:
                logger.error(f"Error listing Connect4 games: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error listing Connect4 games: {str(e)}")
        
        # Enhance WebSocket for Connect4
        # Note: We're not overriding but adding a separate specialized endpoint
        @app.websocket("/ws/games/{thread_id}")
        async def connect4_websocket(websocket: WebSocket, thread_id: str):
            """WebSocket endpoint for Connect4 game with enhanced features"""
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
                    
                    # Process message based on type
                    if message["type"] == "make_move":
                        # Process move
                        move = message.get("move", {})
                        column = move.get("column")
                        explanation = move.get("explanation")
                        
                        if column is not None:
                            # Format move request
                            move_request = {
                                "move": {
                                    "column": column,
                                    "explanation": explanation
                                }
                            }
                            
                            # Make move
                            state = agent.run(move_request, thread_id=thread_id)
                            
                            # Send updated state
                            await websocket.send_json({
                                "type": "state_update",
                                "thread_id": thread_id,
                                "state": state,
                                "timestamp": datetime.now().isoformat(),
                                "last_action": "player_move",
                                "move": {
                                    "column": column,
                                    "explanation": explanation
                                }
                            })
                            
                            # If game is still ongoing, let AI make a move after a short delay
                            if state.get("game_status") == "ongoing":
                                await asyncio.sleep(1)  # Small delay for better UX
                                
                                # AI makes a move
                                state = agent.run({}, thread_id=thread_id)
                                
                                # Send AI move state
                                await websocket.send_json({
                                    "type": "state_update",
                                    "thread_id": thread_id,
                                    "state": state,
                                    "timestamp": datetime.now().isoformat(),
                                    "last_action": "ai_move"
                                })
                    
                    elif message["type"] == "ai_move":
                        # AI makes a move
                        state = agent.run({}, thread_id=thread_id)
                        
                        # Send updated state
                        await websocket.send_json({
                            "type": "state_update",
                            "thread_id": thread_id,
                            "state": state,
                            "timestamp": datetime.now().isoformat(),
                            "last_action": "ai_move"
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
                    
                    elif message["type"] == "visualize":
                        # Get state
                        state = agent.run({}, thread_id=thread_id)
                        
                        # Visualize state
                        agent.visualize_state(state)
                        
                        # Send confirmation
                        await websocket.send_json({
                            "type": "visualize_confirm",
                            "thread_id": thread_id,
                            "timestamp": datetime.now().isoformat()
                        })
                    
            except WebSocketDisconnect:
                # Handle disconnection
                self.agent_manager.unregister_connection(websocket)
                logger.info(f"Client disconnected from Connect4 game {thread_id}")
                
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

# =============================================
# Main Entry Point
# =============================================

# Create Connect4 API instance
connect4_api = Connect4API()

def run():
    """Run the Connect4 API server"""
    import uvicorn
    import asyncio
    
    # Fix for Windows asyncio issues
    if __name__ == "__main__":
        import platform
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Run server
    uvicorn.run(connect4_api.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run()