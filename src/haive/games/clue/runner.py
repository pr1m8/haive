"""
Runner script for the Clue game.

This script demonstrates how to initialize and run a Clue game.
"""
import asyncio
import json
from typing import List, Dict, Any

from src.haive.games.clue.controller import ClueGameController
from src.haive.games.clue.models import ClueGuess

async def run_clue_game(player_names: List[str], max_turns: int = 20, num_ai_players: int = 0) -> Dict[str, Any]:
    """Run a complete Clue game with the specified players.
    
    Args:
        player_names: Names of the players
        max_turns: Maximum number of turns
        num_ai_players: Number of AI players (the first n players will be AI)
        
    Returns:
        Final game state information
    """
    controller = ClueGameController(player_names, max_turns)
    game_state = controller.get_game_state()
    
    print(f"Starting Clue game with players: {', '.join(player_names)}")
    print(f"Solution (hidden): {game_state.solution}")
    
    while game_state.status == "IN_PROGRESS":
        current_player_idx = game_state.current_player_index
        current_player = game_state.players[current_player_idx]
        
        print(f"\n--- Turn {game_state.current_turn} | Player: {current_player.name} ---")
        
        # For AI players
        if current_player_idx < num_ai_players:
            # Generate AI guess
            guess = await controller.generate_ai_guess(current_player_idx)
            print(f"AI player {current_player.name} guesses: "
                  f"{guess.suspect.name}, {guess.weapon.name}, {guess.room.name}")
            
            # Make the guess
            response = controller.make_guess(current_player_idx, guess)
            
            if response.is_correct:
                print(f"Correct guess! {current_player.name} wins!")
            elif response.responding_player:
                print(f"Player {response.responding_player} refutes with card: {response.refuting_card.name}")
            else:
                print("No player could refute this guess.")
            
            # Generate analysis for demonstration
            analysis = await controller.generate_ai_analysis(current_player_idx)
            print(f"AI analysis: Most likely solution is "
                  f"{analysis.prime_suspect.name if analysis.prime_suspect else 'Unknown'}, "
                  f"{analysis.prime_weapon.name if analysis.prime_weapon else 'Unknown'}, "
                  f"{analysis.prime_room.name if analysis.prime_room else 'Unknown'} "
                  f"(Confidence: {analysis.confidence:.2f})")
        
        # For human players (for demonstration, we'll make a random guess)
        else:
            # In a real application, this would get input from the user
            # For this example, we'll simulate the player seeing their cards
            player_view = controller.get_player_view(current_player_idx)
            print(f"Player cards: {', '.join(card.name for card in player_view['player_cards'])}")
            
            # Here you would get input from the user to make a guess
            # For this example, we'll just make a random guess
            import random
            from src.haive.games.clue.models import ValidSuspect, ValidWeapon, ValidRoom
            
            # Make all choices from the enums
            guess = ClueGuess(
                suspect=random.choice(list(ValidSuspect)),
                weapon=random.choice(list(ValidWeapon)),
                room=random.choice(list(ValidRoom))
            )
            
            print(f"Human player {current_player.name} guesses: "
                  f"{guess.suspect.name}, {guess.weapon.name}, {guess.room.name}")
            
            # Make the guess
            response = controller.make_guess(current_player_idx, guess)
            
            if response.is_correct:
                print(f"Correct guess! {current_player.name} wins!")
            elif response.responding_player:
                print(f"Player {response.responding_player} refutes with card: {response.refuting_card.name}")
            else:
                print("No player could refute this guess.")
        
        # Update game state after the turn
        game_state = controller.get_game_state()
    
    # Game over
    print("\n--- Game Over ---")
    if game_state.winner:
        print(f"Winner: {game_state.winner}")
    else:
        print("No winner. Maximum number of turns reached.")
    
    print(f"The solution was: {game_state.solution.suspect.name}, "
          f"{game_state.solution.weapon.name}, {game_state.solution.room.name}")
    
    return {
        "winner": game_state.winner,
        "solution": {
            "suspect": game_state.solution.suspect.name,
            "weapon": game_state.solution.weapon.name,
            "room": game_state.solution.room.name
        },
        "turns_played": game_state.current_turn - 1,
        "max_turns": game_state.max_turns
    }

async def main():
    """Run the Clue game as a demonstration."""
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    result = await run_clue_game(player_names, max_turns=10, num_ai_players=2)
    print(f"\nGame summary: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main()) 