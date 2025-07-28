"""Example client for the Chess API.

This shows how to interact with the chess API to create and play games.
"""

import json
from typing import Optional

import requests


class ChessAPIClient:
    """Simple client for the Chess API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def list_providers(self):
        """Get available LLM providers."""
        response = requests.get(f"{self.base_url}/providers")
        return response.json()

    def create_game(
        self,
        white_provider: str = "anthropic",
        white_model: Optional[str] = None,
        black_provider: str = "anthropic",
        black_model: Optional[str] = None,
        enable_analysis: bool = True,
        max_moves: int = 200,
    ):
        """Create a new game."""
        payload = {
            "white_llm": {
                "provider": white_provider,
                "model": white_model,
            },
            "black_llm": {
                "provider": black_provider,
                "model": black_model,
            },
            "enable_analysis": enable_analysis,
            "max_moves": max_moves,
        }

        response = requests.post(f"{self.base_url}/games", json=payload)
        return response.json()

    def get_game_state(self, game_id: str):
        """Get current game state."""
        response = requests.get(f"{self.base_url}/games/{game_id}")
        return response.json()

    def stream_game(self, game_id: str, callback=None):
        """Stream game events."""
        url = f"{self.base_url}/games/{game_id}/stream"

        with requests.post(url, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        event_data = json.loads(line_str[6:])
                        if callback:
                            callback(event_data)
                        else:
                            print(f"Event: {event_data}")

    def list_games(self):
        """List all active games."""
        response = requests.get(f"{self.base_url}/games")
        return response.json()

    def delete_game(self, game_id: str):
        """Delete a game."""
        response = requests.delete(f"{self.base_url}/games/{game_id}")
        return response.json()


def main():
    """Example usage of the Chess API client."""
    client = ChessAPIClient()

    print("🎮 Chess API Client Example")
    print("=" * 50)

    # List available providers
    print("\n📋 Available providers:")
    providers = client.list_providers()
    for provider in providers["providers"]:
        print(f"  • {provider}")

    # Create a game
    print("\n🎯 Creating a new game...")
    game = client.create_game(
        white_provider="anthropic",
        black_provider="openai",
        enable_analysis=False,  # Faster without analysis
        max_moves=50,  # Quick game
    )

    game_id = game["game_id"]
    print(f"✅ Created game: {game_id}")

    # Get initial state
    print("\n📊 Initial game state:")
    state = client.get_game_state(game_id)
    print(f"  Board: {state['board_fen']}")
    print(f"  Current player: {state['current_player']}")

    # Stream the game
    print("\n🎮 Starting game stream...")
    print("-" * 50)

    def handle_event(event_data):
        """Handle game events."""
        event_type = event_data.get("event")

        if event_type == "move":
            print(
                f"Move {event_data['move_number']}: "
                f"{event_data['player']} played {event_data['move']}"
            )
        elif event_type == "game_ended":
            print("\n🏁 Game Over!")
            print(f"Result: {event_data['result']}")
            print(f"Total moves: {event_data['total_moves']}")
        elif event_type == "error":
            print(f"\n❌ Error: {event_data['message']}")
        else:
            print(f"Event: {event_type}")

    try:
        client.stream_game(game_id, callback=handle_event)
    except KeyboardInterrupt:
        print("\n\n⚠️ Stream interrupted")

    # Get final state
    print("\n📊 Final game state:")
    final_state = client.get_game_state(game_id)
    print(f"  Move count: {final_state['move_count']}")
    print(f"  Result: {final_state['game_result']}")

    # List all games
    print("\n📋 All active games:")
    games = client.list_games()
    for game_info in games["games"]:
        print(
            f"  • {game_info['game_id']}: {game_info['status']} "
            f"({game_info['move_count']} moves)"
        )

    # Clean up
    print(f"\n🗑️ Deleting game {game_id}...")
    client.delete_game(game_id)
    print("✅ Game deleted")


if __name__ == "__main__":
    main()
