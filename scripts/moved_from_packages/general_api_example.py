"""Example of using the general game API system.

This example shows how to:
1. Create a general API that discovers all games
2. List available games
3. Create games with different configurations
4. Use the OpenAPI documentation
"""

import asyncio
import json

import httpx
import uvicorn
from haive.games.api import create_general_game_api


async def demo_api_usage():
    """Demonstrate using the general game API."""

    # Create the general API
    app, game_api = create_general_game_api()

    print("=" * 60)
    print("HAIVE GAMES GENERAL API")
    print("=" * 60)

    # Show discovered games
    print(f"\nDiscovered {len(game_api.discovered_games)} games:")
    for game_id, info in game_api.discovered_games.items():
        print(f"  - {info['name']} ({game_id})")
        if info.get("example_configs"):
            print(f"    Examples: {', '.join(info['example_configs'])}")

    print("\n" + "=" * 60)
    print("API ENDPOINTS")
    print("=" * 60)

    # Simulate API calls
    base_url = "http://localhost:8000"

    # Example 1: List all games
    print("\n1. List all available games:")
    print(f"   GET {base_url}/api/games/")

    # Example 2: Create a chess game with simple config
    print("\n2. Create a chess game (simple mode):")
    print(f"   POST {base_url}/api/games/create")
    print("   Body:")
    chess_request = {
        "game_id": "chess",
        "config_mode": "simple",
        "player_models": {"player1": "gpt-4", "player2": "claude-3-opus"},
        "game_settings": {"enable_analysis": True, "max_moves": 100},
    }
    print(f"   {json.dumps(chess_request, indent=4)}")

    # Example 3: Create a tic-tac-toe game with example config
    print("\n3. Create a tic-tac-toe game (example mode):")
    print(f"   POST {base_url}/api/games/create")
    print("   Body:")
    ttt_request = {
        "game_id": "tic_tac_toe",
        "config_mode": "example",
        "example_config": "budget",
    }
    print(f"   {json.dumps(ttt_request, indent=4)}")

    # Example 4: Create a connect4 game with advanced config
    print("\n4. Create a Connect4 game (advanced mode):")
    print(f"   POST {base_url}/api/games/create")
    print("   Body:")
    connect4_request = {
        "game_id": "connect4",
        "config_mode": "advanced",
        "player_configs": {
            "red_player": {
                "llm_config": "openai:gpt-4o",
                "temperature": 0.7,
                "player_name": "Strategic Red",
                "system_message": "You are a strategic Connect4 player...",
            },
            "yellow_player": {
                "llm_config": "anthropic:claude-3-haiku",
                "temperature": 0.5,
                "player_name": "Defensive Yellow",
            },
        },
    }
    print(f"   {json.dumps(connect4_request, indent=4)}")

    print("\n" + "=" * 60)
    print("GAME-SPECIFIC ENDPOINTS")
    print("=" * 60)

    print("\nOnce a game is created, use these endpoints:")
    print("  - GET  /api/games/{game_id}/{thread_id} - Get game state")
    print("  - POST /api/games/{game_id}/{thread_id}/move - Make a move")
    print("  - GET  /api/games/{game_id}/{thread_id}/ai-move - AI makes move")
    print("  - WS   /ws/games/{game_id}/{thread_id} - WebSocket connection")

    print("\n" + "=" * 60)
    print("INTERACTIVE DEMO")
    print("=" * 60)

    # Add some demo endpoints
    @app.get("/demo/play-chess")
    async def demo_play_chess():
        """Demo endpoint that creates and plays a chess game."""
        # This would normally use the API client
        return {
            "message": "Chess game demo",
            "instructions": [
                "1. Create a game using POST /api/games/create",
                "2. Connect via WebSocket to /ws/games/chess/{thread_id}",
                "3. Send moves or request AI moves",
                "4. Watch the game progress in real-time!",
            ],
        }

    @app.get("/demo/quick-game/{game_id}")
    async def demo_quick_game(game_id: str):
        """Create a quick game with default settings."""
        if game_id not in game_api.discovered_games:
            return {"error": f"Game '{game_id}' not found"}

        import uuid

        thread_id = str(uuid.uuid4())

        return {
            "game_id": game_id,
            "thread_id": thread_id,
            "message": f"Quick {game_id} game created!",
            "endpoints": {
                "state": f"/api/games/{game_id}/{thread_id}",
                "move": f"/api/games/{game_id}/{thread_id}/move",
                "ai_move": f"/api/games/{game_id}/{thread_id}/ai-move",
                "websocket": f"ws://localhost:8000/ws/games/{game_id}/{thread_id}",
            },
        }

    return app


async def test_api_client():
    """Test the API with actual HTTP calls."""
    print("\n" + "=" * 60)
    print("TESTING API WITH HTTP CLIENT")
    print("=" * 60)

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        try:
            # List games
            response = await client.get("/api/games/")
            if response.status_code == 200:
                games = response.json()
                print(f"\nAvailable games: {len(games)}")
                for game in games[:3]:  # Show first 3
                    print(f"  - {game['name']} ({game['game_id']})")

            # Create a chess game
            response = await client.post(
                "/api/games/create",
                json={
                    "game_id": "chess",
                    "config_mode": "simple",
                    "player_models": {
                        "player1": "gpt-3.5-turbo",
                        "player2": "gpt-3.5-turbo",
                    },
                },
            )
            if response.status_code == 200:
                game_info = response.json()
                print("\nCreated chess game:")
                print(f"  Thread ID: {game_info['thread_id']}")
                print(f"  Status endpoint: {game_info['endpoints']['status']}")

        except httpx.ConnectError:
            print("\nNote: To test with real HTTP calls, run the server first:")
            print("  python general_api_example.py --serve")


def main():
    """Main entry point."""
    import sys

    if "--serve" in sys.argv:
        # Run the server
        app = asyncio.run(demo_api_usage())
        print("\n" + "=" * 60)
        print("STARTING API SERVER")
        print("=" * 60)
        print("\nServer running at: http://localhost:8000")
        print("API documentation: http://localhost:8000/docs")
        print("Interactive API: http://localhost:8000/redoc")
        print("\nPress Ctrl+C to stop")

        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # Just show the demo
        asyncio.run(demo_api_usage())
        print("\n" + "=" * 60)
        print("To run the server, use: python general_api_example.py --serve")


if __name__ == "__main__":
    main()
