"""Example chess game runner.

This module provides an example of how to run a complete chess game
using the Haive chess module, demonstrating:
    - Agent configuration
    - State initialization
    - Game streaming
    - Event monitoring

This is intended as a basic demonstration of the chess module's capabilities
and can be used as a starting point for more complex implementations.
"""

import uuid

from haive.games.chess.agent import ChessAgent
from haive.games.chess.config import ChessConfig
from haive.games.chess.state import ChessState


def run_chess_game(thread_id: str = None):
    """Run a complete chess game with LLM players.

    Creates and runs a chess game between two LLM players, streaming
    the game events and tracking the game status until completion.

    Args:
        thread_id (str, optional): Unique identifier for the game thread.
            If not provided, a random ID will be generated. Defaults to None.

    Returns:
        None: The function outputs game progress to the console.

    Examples:
        >>> # Run a game with a random thread ID
        >>> run_chess_game()

        >>> # Run a game with a specific thread ID
        >>> run_chess_game("chess_custom_id")

    Note:
        This function will run a full chess game with the following configuration:
        - Both white and black players powered by LLMs
        - Position analysis enabled
        - Maximum 200 moves before forcing a draw
        - Streaming output of game events

    The function handles errors gracefully and reports the final game result.
    """
    # Create thread ID
    thread_id = thread_id or f"chess_{uuid.uuid4().hex[:8]}"
    print(f"🧵 Starting chess game with thread_id: {thread_id}")

    # Create configuration
    config = ChessConfig(name="Chess Game", enable_analysis=True, max_moves=200)

    # Create agent
    agent = ChessAgent(config)

    # Create initial state
    initial_state = ChessState()

    # Compile the agent
    app = agent.app

    # Run the game
    try:
        # Stream the game
        for step in app.stream(
            initial_state.model_dump(),
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="values",
        ):
            # Print current status
            if "game_status" in step:
                print(f"📊 Game status: {step['game_status']}")

            # Check for game end
            if step.get("game_result"):
                print(f"\n🏁 Game ended: {step['game_result']}")
                break

    except Exception as e:
        print(f"❌ Error during game: {e}")
        import traceback

        traceback.print_exc()

    print("\n✅ Game completed!")


if __name__ == "__main__":
    """Execute the chess game when the script is run directly.

    Running this module as a script will start a complete chess game
    between two LLM players and output the progress to the console.

    Example:
        $ python -m haive.games.chess.example
    """
    run_chess_game()
