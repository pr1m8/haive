"""FastAPI example for chess game with configurable LLMs.

This module demonstrates how to create API endpoints for chess games
with configurable LLM providers and models.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from haive.games.chess.agent import ChessAgent
from haive.games.chess.config import ChessConfig
from haive.games.chess.llm_utils import (
    create_chess_engines_simple,
    get_available_chess_providers,
)
from haive.games.chess.state import ChessState

# Create FastAPI app
app = FastAPI(
    title="Chess Game API",
    description="API for playing chess with configurable LLM agents",
    version="1.0.0",
)

# Store active games
active_games: Dict[str, Dict[str, Any]] = {}


class LLMConfig(BaseModel):
    """LLM configuration for a player."""

    provider: str = Field(default="anthropic", description="LLM provider")
    model: Optional[str] = Field(default=None, description="Model name")
    temperature: Optional[float] = Field(default=None, description="Temperature")


class CreateGameRequest(BaseModel):
    """Request to create a new chess game."""

    white_llm: LLMConfig = Field(default_factory=LLMConfig)
    black_llm: LLMConfig = Field(default_factory=LLMConfig)
    enable_analysis: bool = Field(default=True, description="Enable position analysis")
    max_moves: int = Field(default=200, description="Maximum moves before draw")


class GameResponse(BaseModel):
    """Response with game information."""

    game_id: str
    status: str
    created_at: str
    config: Dict[str, Any]


class GameStateResponse(BaseModel):
    """Response with current game state."""

    game_id: str
    status: str
    board_fen: str
    move_history: List[tuple[str, str]]
    current_player: str
    game_result: Optional[str]
    move_count: int


class MoveStreamEvent(BaseModel):
    """Event streamed during game execution."""

    event: str
    data: Dict[str, Any]


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "title": "Chess Game API",
        "endpoints": {
            "GET /providers": "List available LLM providers",
            "POST /games": "Create a new game",
            "GET /games/{game_id}": "Get game state",
            "POST /games/{game_id}/stream": "Stream game execution",
            "DELETE /games/{game_id}": "Delete a game",
        },
    }


@app.get("/providers")
async def list_providers():
    """List available LLM providers."""
    providers = get_available_chess_providers()
    return {
        "providers": providers,
        "example_config": {
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20240620",
            "temperature": 0.7,
        },
    }


@app.post("/games", response_model=GameResponse)
async def create_game(request: CreateGameRequest):
    """Create a new chess game."""
    game_id = f"chess_{uuid.uuid4().hex[:8]}"

    try:
        # Create engines from request
        engines = create_chess_engines_simple(
            white_provider=request.white_llm.provider,
            white_model=request.white_llm.model,
            black_provider=request.black_llm.provider,
            black_model=request.black_llm.model,
            temperature=request.white_llm.temperature,  # Applied to both
            enable_analysis=request.enable_analysis,
        )

        # Create game configuration
        config = ChessConfig(
            name=f"API Game {game_id}",
            engines=engines,
            enable_analysis=request.enable_analysis,
            max_moves=request.max_moves,
        )

        # Store game info
        active_games[game_id] = {
            "id": game_id,
            "config": config,
            "agent": ChessAgent(config),
            "state": ChessState(),
            "created_at": datetime.utcnow().isoformat(),
            "status": "created",
            "request": request.dict(),
        }

        return GameResponse(
            game_id=game_id,
            status="created",
            created_at=active_games[game_id]["created_at"],
            config=request.dict(),
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/games/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """Get the current state of a game."""
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = active_games[game_id]
    state = game["state"]

    return GameStateResponse(
        game_id=game_id,
        status=game["status"],
        board_fen=state.board_fen,
        move_history=state.move_history,
        current_player=state.current_player,
        game_result=state.game_result,
        move_count=len(state.move_history),
    )


@app.post("/games/{game_id}/stream")
async def stream_game(game_id: str, background_tasks: BackgroundTasks):
    """Stream game execution events."""
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = active_games[game_id]

    if game["status"] not in ["created", "paused"]:
        raise HTTPException(
            status_code=400, detail=f"Game is {game['status']}, cannot start streaming"
        )

    async def event_generator():
        """Generate SSE events for game progress."""
        try:
            # Update status
            game["status"] = "running"
            yield f"data: {json.dumps({'event': 'game_started', 'game_id': game_id})}\n\n"

            # Get agent and state
            agent = game["agent"]
            state = game["state"]
            app = agent.app

            # Stream game execution
            move_count = 0
            for step in app.stream(
                state.model_dump(),
                config=game["config"].runnable_config,
                stream_mode="values",
            ):
                # Update stored state
                game["state"] = ChessState(**step)

                # Emit move events
                if "move_history" in step:
                    current_moves = len(step["move_history"])
                    if current_moves > move_count:
                        move_count = current_moves
                        last_move = step["move_history"][-1]
                        event_data = {
                            "event": "move",
                            "move_number": move_count,
                            "player": last_move[0],
                            "move": last_move[1],
                            "board_fen": step.get("board_fen"),
                        }
                        yield f"data: {json.dumps(event_data)}\n\n"

                # Check for game end
                if step.get("game_result"):
                    game["status"] = "completed"
                    event_data = {
                        "event": "game_ended",
                        "result": step["game_result"],
                        "total_moves": move_count,
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"
                    break

        except Exception as e:
            game["status"] = "error"
            error_data = {
                "event": "error",
                "message": str(e),
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.delete("/games/{game_id}")
async def delete_game(game_id: str):
    """Delete a game."""
    if game_id not in active_games:
        raise HTTPException(status_code=404, detail="Game not found")

    del active_games[game_id]
    return {"message": f"Game {game_id} deleted"}


@app.get("/games")
async def list_games():
    """List all active games."""
    games_list = []
    for game_id, game in active_games.items():
        games_list.append(
            {
                "game_id": game_id,
                "status": game["status"],
                "created_at": game["created_at"],
                "move_count": len(game["state"].move_history),
                "players": {
                    "white": game["request"]["white_llm"],
                    "black": game["request"]["black_llm"],
                },
            }
        )

    return {"games": games_list, "total": len(games_list)}


# Example usage in main
if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Chess API server...")
    print("📚 API docs available at: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
