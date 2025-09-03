#!/usr/bin/env python3
"""
Tic-Tac-Toe Game Example - AI vs AI gameplay demonstration.

This example shows how to create and run a Tic-Tac-Toe game with
AI agents playing against each other.
"""

import asyncio

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig


class TicTacToeGame:
    """Simple Tic-Tac-Toe game implementation."""

    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def display_board(self):
        """Display the current board state."""
        print("\n   |   |   ")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("   |   |   ")
        print("\nPositions: 1-9 (left to right, top to bottom)")

    def make_move(self, position: int, player: str) -> bool:
        """Make a move on the board."""
        if 1 <= position <= 9 and self.board[position - 1] == " ":
            self.board[position - 1] = player
            return True
        return False

    def check_winner(self) -> str | None:
        """Check if there's a winner."""
        # Winning combinations
        lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # Rows
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # Columns
            [0, 4, 8],
            [2, 4, 6],  # Diagonals
        ]

        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != " ":
                return self.board[line[0]]

        # Check for tie
        if " " not in self.board:
            return "TIE"

        return None

    def get_available_moves(self) -> list:
        """Get list of available positions."""
        return [i + 1 for i, spot in enumerate(self.board) if spot == " "]


async def create_game_agent(
    name: str, symbol: str, strategy: str = "smart"
) -> SimpleAgent:
    """Create a game-playing agent."""

    if strategy == "smart":
        system_message = f"""You are an expert Tic-Tac-Toe player using symbol '{symbol}'.

Rules:
- The board has positions 1-9 (left to right, top to bottom)
- You must choose an available position (1-9)
- Try to win by getting 3 in a row
- Block opponent from winning
- Take center (position 5) when possible
- Take corners when center is taken

Always respond with just the position number (1-9) for your move."""
    else:
        system_message = f"""You are playing Tic-Tac-Toe using symbol '{symbol}'.
        Choose any available position from 1-9.
        Respond with just the position number."""

    config = AugLLMConfig(
        model="gpt-4",
        temperature=0.3 if strategy == "smart" else 0.7,
        system_message=system_message,
    )

    return SimpleAgent(name=name, engine=config)


async def get_agent_move(agent: SimpleAgent, game: TicTacToeGame, symbol: str) -> int:
    """Get move from agent."""
    board_state = f"""
Current board:
{" | ".join([str(i + 1) if game.board[i] == " " else game.board[i] for i in range(3)])}
{" | ".join([str(i + 1) if game.board[i] == " " else game.board[i] for i in range(3, 6)])}
{" | ".join([str(i + 1) if game.board[i] == " " else game.board[i] for i in range(6, 9)])}

Available positions: {game.get_available_moves()}
Your symbol: {symbol}

Choose your move (1-9):"""

    response = await agent.arun(board_state)

    # Extract position from response
    try:
        # Look for a number in the response
        import re

        numbers = re.findall(r"\b[1-9]\b", response)
        if numbers:
            position = int(numbers[0])
            if position in game.get_available_moves():
                return position
    except:
        pass

    # Fallback: random available move
    import random

    available = game.get_available_moves()
    return random.choice(available) if available else 1


async def main():
    """Run the Tic-Tac-Toe game example."""
    print("🎮 Haive Tic-Tac-Toe Game Example")
    print("=" * 40)
    print("Watch two AI agents play against each other!")

    # Create the game
    game = TicTacToeGame()

    # Create two AI players with different strategies
    player_x = await create_game_agent("Strategic Player", "X", "smart")
    player_o = await create_game_agent("Creative Player", "O", "creative")

    print("\n🤖 Players:s:")
    print(f"   X: {player_x.name} (Strategic)")
    print(f"   O: {player_o.name} (Creative)")

    # Game loop
    current_agent = player_x
    current_symbol = "X"
    move_count = 0

    print("\n🎯 Game Start!t!")
    game.display_board()

    while True:
        move_count += 1
        print(f"\n--- Move {move_count} ---")
        print(f"🎲 {current_agent.name}'s turn ({current_symbol})")

        # Get move from current agent
        try:
            position = await get_agent_move(current_agent, game, current_symbol)
            print(f"📍 Chosen position: {position}")

            # Make the move
            if game.make_move(position, current_symbol):
                game.display_board()

                # Check for winner
                winner = game.check_winner()
                if winner:
                    if winner == "TIE":
                        print("\n🤝 Game ended in a tie!e!")
                    else:
                        winning_agent = player_x if winner == "X" else player_o
                        print(f"\n🏆 {winning_agent.name} ({winner}) wins!")
                    break

                # Switch players
                if current_symbol == "X":
                    current_agent = player_o
                    current_symbol = "O"
                else:
                    current_agent = player_x
                    current_symbol = "X"

            else:
                print(f"❌ Invalid move! Position {position} is not available.")
                break

        except Exception as e:
            print(f"❌ Error getting move: {e}")
            break

        # Safety check
        if move_count > 20:
            print("⚠️ Game taking too long, ending.")
            break

        # Small delay for readability
        await asyncio.sleep(1)

    print(f"\n✅ Game completed in {move_count} moves!")
    print("🎮 Thanks for watching the AI vs AI demonstration!")


if __name__ == "__main__":
    asyncio.run(main())
