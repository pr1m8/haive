"""Example of setting up a Chess API with the new configuration system.

This example demonstrates:
1. Creating a chess game with different LLM configurations
2. Setting up the API endpoints
3. Running games with various model combinations
"""

import asyncio

import uvicorn
from fastapi import FastAPI
from haive.games.api import create_chess_api


async def main():
    """Run example chess API configurations."""
    # Create FastAPI app
    app = FastAPI(title="Chess Game API Example")

    # Example 1: Simple model configuration
    create_chess_api(
        app,
        config_overrides={
            "white_model": "gpt-4",
            "black_model": "claude-3-opus",
            "enable_analysis": True,
            "max_moves": 150,
        },
    )

    # Example 2: Using example configurations
    create_chess_api(
        app,
        config_overrides={
            "example_config": "budget",
            "enable_analysis": False,  # Disable analysis for faster, cheaper games
        },
    )

    # Example 3: Advanced configuration with full player configs
    from haive.games.core.agent.player_agent import PlayerAgentConfig

    player_configs = {
        "white_player": PlayerAgentConfig(
            llm_config="openai:gpt-4o",
            temperature=0.7,
            player_name="Aggressive White",
            system_message="You are an aggressive chess player who favors tactical combinations.",
        ),
        "black_player": PlayerAgentConfig(
            llm_config="anthropic:claude-3-opus-20240229",
            temperature=0.3,
            player_name="Defensive Black",
            system_message="You are a defensive chess player who excels at positional play.",
        ),
        "white_analyzer": PlayerAgentConfig(
            llm_config="gpt-4", temperature=0.2, player_name="White Strategic Analyst"
        ),
        "black_analyzer": PlayerAgentConfig(
            llm_config="claude-3-opus",
            temperature=0.2,
            player_name="Black Tactical Analyst",
        ),
    }

    create_chess_api(
        app,
        config_overrides={"player_configs": player_configs, "config_mode": "advanced"},
    )

    # Example 4: Legacy mode (backward compatibility)
    create_chess_api(app, config_overrides={"use_legacy_engines": True})

    # Add root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Chess API Examples",
            "endpoints": {
                "create_game": "POST /api/chess/",
                "make_move": "POST /api/chess/{thread_id}/move",
                "ai_move": "GET /api/chess/{thread_id}/ai-move",
                "get_state": "GET /api/chess/{thread_id}",
                "websocket": "ws://localhost:8000/ws/chess/{thread_id}",
            },
            "examples": {
                "simple": "GPT-4 vs Claude-3-Opus",
                "budget": "Cost-effective models",
                "advanced": "Custom player personalities",
                "legacy": "Hardcoded engines",
            },
        }

    # Example of programmatic game creation
    from haive.games.chess.agent import ChessAgent
    from haive.games.chess.config import ChessAgentConfig

    # Create a game config
    config = ChessAgentConfig(
        white_model="gpt-3.5-turbo",
        black_model="gpt-3.5-turbo",
        enable_analysis=False,
        max_moves=50,
    )

    # Create agent
    agent = ChessAgent(config)

    # Make a test move
    thread_id = "test-game-001"
    agent.run({}, thread_id=thread_id)

    return app


if __name__ == "__main__":
    # For running the example
    app = asyncio.run(main())

    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
