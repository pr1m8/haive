# demo_among_us.py

import time
import random
import argparse
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table
from src.haive.games.among_us.factory import create_among_us_game
from src.haive.games.among_us.models import AmongUsGamePhase, PlayerRole, TaskStatus


def run_among_us_demo(
    player_count: int = 6,
    impostor_count: int = 1,
    map_name: str = "skeld",
    save_path: str = None,
    load_path: str = None,
    interactive: bool = True,
    max_rounds: int = 15,
    speed: float = 1.0
):
    """
    Run a demo of the Among Us game with AI agents and enhanced visibility.
    
    Args:
        player_count: Number of players (4-10)
        impostor_count: Number of impostors (1-3)
        map_name: Name of map to use
        save_path: Path to save game at the end
        load_path: Path to load a saved game
        interactive: Whether to run in interactive mode
        max_rounds: Maximum number of rounds
        speed: Simulation speed multiplier
    """
    console = Console()
    
    console.print(Panel.fit(
        "[bold magenta]Among Us AI Game Demo[/bold magenta]\n\n"
        "This demo simulates an Among Us game with AI agents and enhanced visibility.",
        title="Welcome"
    ))
    
    # Load game if specified
    if load_path and os.path.exists(load_path):
        console.print(f"Loading game from {load_path}...")
        import json
        with open(load_path, 'r') as f:
            saved_game = json.load(f)
            
        player_names = saved_game.get("players", [f"Player{i+1}" for i in range(player_count)])
        game_config = saved_game.get("game_config", {})
    else:
        # Get player names
        colors = ["Red", "Blue", "Green", "Yellow", "Orange", "Purple", 
                  "White", "Black", "Pink", "Brown", "Cyan", "Lime"]
        player_names = colors[:player_count]
        
        # Configure game parameters
        game_config = {
            "map_name": map_name,
            "num_impostors": impostor_count,
            "task_bar_updates": "always",
        }
        
        # Use different map layouts based on map name
        if map_name.lower() == "skeld":
            game_config["map_locations"] = [
                "cafeteria", "admin", "electrical", "storage", "medbay", 
                "navigation", "shields", "weapons", "o2", "security"
            ]
        elif map_name.lower() == "polus":
            game_config["map_locations"] = [
                "dropship", "office", "laboratory", "storage", "communications", 
                "weapons", "o2", "electrical", "security", "specimen"
            ]
        elif map_name.lower() == "mira":
            game_config["map_locations"] = [
                "launchpad", "medbay", "communications", "locker", "laboratory", 
                "office", "admin", "cafeteria", "storage", "reactor"
            ]
    
    # Create the game agent
    console.print(f"Creating game with {len(player_names)} players and {impostor_count} impostors...")
    agent = create_among_us_game(
        player_names=player_names,
        game_config=game_config
    )
    
    # Initialize the game or load saved state
    if load_path and os.path.exists(load_path):
        state = saved_game.get("state")
        
        # Convert to state object
        from src.haive.games.among_us.state import AmongUsState
        state = AmongUsState(**state)
    else:
        console.print("Initializing new game...")
        state = agent.initialize(player_names)
    
    # Display initial game state
    agent.visualize_state(state)
    
    # Main game loop
    round_number = state.round_number
    
    # Display roles for player information (normally hidden in game)
    console.print("\n[bold]Player Roles (For Demo Purposes):[/bold]")
    role_table = Table()
    role_table.add_column("Player", style="cyan")
    role_table.add_column("Role", style="yellow")
    
    for player_id, player_state in state.player_states.items():
        role = player_state.role
        role_text = "CREWMATE" if role == PlayerRole.CREWMATE else "IMPOSTOR"
        role_style = "green" if role == PlayerRole.CREWMATE else "red"
        role_table.add_row(player_id, f"[{role_style}]{role_text}[/{role_style}]")
    
    console.print(role_table)
    
    # Wait for user to press enter to continue in interactive mode
    if interactive:
        console.print("[bold cyan]Press Enter to start the game...[/bold cyan]")
        input()
    
    while state.game_phase != AmongUsGamePhase.GAME_OVER and round_number < max_rounds:
        round_number += 1
        console.print(f"\n[bold cyan]--- Round {round_number} ---[/bold cyan]")
        
        # Process based on game phase
        if state.game_phase == AmongUsGamePhase.TASKS:
            # Process each player's turn if in task phase
            for player_id in state.players:
                if state.game_phase != AmongUsGamePhase.TASKS:
                    # Phase might have changed (e.g., emergency meeting)
                    break
                
                # Process player turn with enhanced visibility
                state = process_player_turn(agent, state, player_id, console, interactive, speed)
        
        elif state.game_phase == AmongUsGamePhase.MEETING:
            # Process meeting discussion phase
            state = process_meeting_discussion(agent, state, console, interactive, speed)
            
        elif state.game_phase == AmongUsGamePhase.VOTING:
            # Process voting phase
            state = process_voting_phase(agent, state, console, interactive, speed)
        
        # Check for random events at end of round when in task phase
        if state.game_phase == AmongUsGamePhase.TASKS:
            state = process_random_events(agent, state, console, interactive, speed)
    
    # Game over
    console.print("[bold green]Game Over![/bold green]")
    agent.visualize_state(state)
    
    if hasattr(state, "winner"):
        if state.winner == "crewmates":
            console.print("[bold green]CREWMATES WIN![/bold green]")
            if state.get_task_completion_percentage() >= 100:
                console.print("All tasks were completed successfully!")
            else:
                console.print("All impostors were eliminated!")
        else:
            console.print("[bold red]IMPOSTORS WIN![/bold red]")
            if state.crewmate_count == 0:
                console.print("All crewmates were eliminated!")
            else:
                console.print("Impostors have outnumbered the remaining crewmates!")
    
    # Display final statistics
    console.print("\n[bold]Game Statistics:[/bold]")
    stats_table = Table()
    stats_table.add_column("Statistic", style="cyan")
    stats_table.add_column("Value", style="yellow")
    
    stats_table.add_row("Rounds Played", str(round_number))
    stats_table.add_row("Task Completion", f"{state.get_task_completion_percentage():.1f}%")
    stats_table.add_row("Eliminated Players", ", ".join(state.eliminated_players) if state.eliminated_players else "None")
    
    console.print(stats_table)
    
    # Display roles
    console.print("\n[bold]Final Player Status:[/bold]")
    for pid, pstate in state.player_states.items():
        role = "CREWMATE" if pstate.role == PlayerRole.CREWMATE else "IMPOSTOR"
        role_style = "green" if pstate.role == PlayerRole.CREWMATE else "red"
        status = "ALIVE" if pstate.is_alive else "DEAD"
        status_style = "green" if pstate.is_alive else "red"
        console.print(f"[{role_style}]{pid}: {role}[/{role_style}] - [{status_style}]{status}[/{status_style}]")
    
    # Save game if requested
    if save_path:
        dir_path = os.path.dirname(save_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        import json
        with open(save_path, 'w') as f:
            json.dump({
                "players": player_names,
                "game_config": game_config,
                "state": state.dict() if hasattr(state, "dict") else state
            }, f, indent=2)
        
        console.print(f"\nGame saved to {save_path}")
def format_action(move, verbose=False):
    """Format an action for display."""
    action_type = move.get("action", "unknown")
    
    if action_type == "move":
        location = move.get("location", "unknown")
        return f"Move to [cyan]{location}[/cyan]"
    
    elif action_type == "complete_task":
        task_id = move.get("task_id", "unknown")
        return f"Complete task [yellow]{task_id}[/yellow]"
    
    elif action_type == "kill":
        target = move.get("target_id", "unknown")
        return f"[red]Kill {target}[/red]"
    
    elif action_type == "report_body":
        return "[magenta]Report dead body[/magenta]"
    
    elif action_type == "call_emergency_meeting":
        return "[magenta]Call emergency meeting[/magenta]"
    
    elif action_type == "discuss":
        message = move.get("message", "")
        if verbose:
            return f"Say: \"[italic]{message}[/italic]\""
        else:
            short_msg = message[:50] + "..." if len(message) > 50 else message
            return f"Discuss: \"[italic]{short_msg}[/italic]\""
    
    elif action_type == "vote":
        target = move.get("vote_for", "unknown")
        return f"Vote for [bold]{target}[/bold]"
    
    elif action_type == "sabotage":
        sabotage_type = move.get("sabotage_type", "unknown")
        return f"[red]Sabotage {sabotage_type}[/red]"
    
    else:
        return f"{action_type} {str(move)}"

def get_role_color(role):
    """Get color for a player role."""
    if role == PlayerRole.CREWMATE:
        return "green"
    else:
        return "red"
def process_player_turn(agent, state, player_id, console, interactive, speed):
    """Process a single player's turn with enhanced visibility into AI thoughts."""
    # Skip dead players during task phase
    player_state = state.player_states.get(player_id)
    if state.game_phase == AmongUsGamePhase.TASKS and player_state and not player_state.is_alive:
        return state
    
    console.print(f"\n[bold {get_role_color(player_state.role)}]{player_id}'s turn[/bold {get_role_color(player_state.role)}]")
    
    # Display player status first
    console.print(f"Location: [cyan]{player_state.location}[/cyan]")
    
    if player_state.role == PlayerRole.CREWMATE:
        console.print(f"Role: [green]CREWMATE[/green]")
        task_completion = agent._get_task_completion_percentage(state)
        console.print(f"Task completion: [yellow]{task_completion:.1f}%[/yellow]")
    else:
        console.print(f"Role: [red]IMPOSTOR[/red]")
        fellow_impostors = [
            pid for pid, pstate in state.player_states.items() 
            if pstate.role == PlayerRole.IMPOSTOR and pid != player_id
        ]
        if fellow_impostors:
            console.print(f"Fellow impostors: [red]{', '.join(fellow_impostors)}[/red]")
        else:
            console.print("[red]You are the only impostor![/red]")
    
    # Show player's tasks
    console.print("\n[bold]Tasks:[/bold]")
    for i, task in enumerate(player_state.tasks):
        status = "✓" if task.status == TaskStatus.COMPLETED else "□"
        style = "green" if task.status == TaskStatus.COMPLETED else "yellow"
        highlight = " [bold cyan](current location)[/bold cyan]" if task.location == player_state.location else ""
        console.print(f"{i+1}. [{style}]{status} {task.description} (in {task.location}){highlight}[/{style}]")
    
    # Show observations
    if player_state.observations:
        console.print("\n[bold]Recent observations:[/bold]")
        for obs in player_state.observations[-3:]:  # Show last 3 observations
            console.print(f"• [italic]{obs}[/italic]")
    
    # Show available actions
    console.print("\n[bold]Available actions:[/bold]")
    legal_moves = agent.get_legal_moves(state, player_id)
    for i, move in enumerate(legal_moves[:5]):  # Show first 5 actions for brevity
        action_str = format_action(move)
        console.print(f"{i+1}. {action_str}")
    if len(legal_moves) > 5:
        console.print(f"...and {len(legal_moves)-5} more actions")
        
    # Get player's move
    move_context = agent.prepare_move_context(state, player_id)
    
    # Get the appropriate engine for this player and phase
    player_role = state.player_states[player_id].role
    engine_key = "player"
    
    if state.game_phase == AmongUsGamePhase.MEETING:
        engine_key = "meeting"
    elif state.game_phase == AmongUsGamePhase.VOTING:
        engine_key = "voting"
    
    # Get the engine
    engine = agent.get_engine_for_player(player_role, engine_key)
    if not engine:
        console.print(f"[bold red]No engine found for {player_id} (role={player_role}, key={engine_key})[/bold red]")
        return state
    
    # Invoke the engine
    console.print(f"\n[bold]AI thinking for {player_id}...[/bold]")
    response = engine.invoke(move_context)
    
    # Print the AI's thought process
    if isinstance(response, str):
        console.print(f"\n[dim italic]{response}[/dim italic]")
    elif hasattr(response, 'content'):
        console.print(f"\n[dim italic]{response.content}[/dim italic]")
    
    # Extract structured move
    move = agent.extract_move(response, player_role)
    console.print(f"\n[bold]{player_id} decided to:[/bold] {format_action(move, verbose=True)}")
    
    # Apply the move
    new_state = agent.apply_move(state, player_id, move)
    
    # Check for phase transitions
    if (new_state.game_phase == AmongUsGamePhase.MEETING and 
        player_id == new_state.players[-1]):  # Last player in discussion
        # Transition to voting
        new_state = agent.advance_phase(new_state)
    
    elif (new_state.game_phase == AmongUsGamePhase.VOTING and 
            len(new_state.votes) >= len([pid for pid, pstate in new_state.player_states.items() 
                                       if pstate.is_alive])):
        # Transition back to tasks
        new_state = agent.advance_phase(new_state)
    
    # Check for game over
    new_state = agent.check_game_status(new_state)
    
    # Display updated game state
    agent.visualize_state(new_state)
    
    # Add a delay for readability, scaled by speed setting
    delay = 1.0 / speed
    if interactive:
        if delay > 0.5:
            time.sleep(delay)
        else:
            console.print("[bold cyan]Press Enter to continue...[/bold cyan]")
            input()
    else:
        time.sleep(min(0.5, delay))  # Cap at 0.5 seconds for non-interactive mode
    
    return new_state
def process_meeting_discussion(agent, state, console, interactive, speed):
    """
    Process a meeting's discussion phase with enhanced visibility.
    
    Args:
        agent: The AmongUsAgent instance
        state: Current game state
        console: Rich console for display
        interactive: Whether in interactive mode
        speed: Simulation speed multiplier
    
    Returns:
        Updated state
    """
    # Display meeting information
    if state.reported_body:
        console.print(f"\n[bold red]BODY REPORTED![/bold red]")
        console.print(f"[bold]{state.meeting_caller}[/bold] found the body of [bold]{state.reported_body}[/bold]")
    else:
        console.print(f"\n[bold yellow]EMERGENCY MEETING CALLED![/bold yellow]")
        console.print(f"[bold]{state.meeting_caller}[/bold] called an emergency meeting")
    
    # Create a table for player positions
    from rich.table import Table
    location_table = Table(title="Player Locations at Time of Meeting")
    location_table.add_column("Player", style="cyan")
    location_table.add_column("Location", style="green")
    location_table.add_column("Status", style="yellow")
    
    for player_id, player_state in state.player_states.items():
        role_style = "green" if player_state.role == PlayerRole.CREWMATE else "red"
        status = "[green]ALIVE[/green]" if player_state.is_alive else "[red]DEAD[/red]"
        location_table.add_row(
            f"[{role_style}]{player_id}[/{role_style}]",
            player_state.location,
            status
        )
    
    console.print(location_table)
    console.print("\n[bold]DISCUSSION PHASE[/bold]")
    
    # Process each player's discussion contribution
    alive_players = [pid for pid, pstate in state.player_states.items() if pstate.is_alive]
    
    for player_id in alive_players:
        player_state = state.player_states[player_id]
        role = player_state.role
        
        # Show whose turn it is to speak
        role_style = "green" if role == PlayerRole.CREWMATE else "red"
        console.print(f"\n[bold {role_style}]{player_id}'s turn to speak[/bold {role_style}]")
        
        # Create context for the player
        move_context = agent.prepare_move_context(state, player_id)
        
        # Get the discussion engine
        engine = agent.get_engine_for_player(role, "meeting")
        if not engine:
            console.print(f"[bold red]No discussion engine found for {player_id}[/bold red]")
            continue
        
        # Generate the player's statement
        console.print(f"[dim]Thinking...[/dim]")
        response = engine.invoke(move_context)
        
        # Create a structured move
        if isinstance(response, str):
            move = {"action": "discuss", "message": response}
        elif hasattr(response, "content"):
            move = {"action": "discuss", "message": response.content}
        else:
            move = agent.extract_move(response, role)
        
        # Get the player's message
        message = move.get("message", "No comment.")
        
        # Display the message in a speech bubble style
        console.print(f"[bold {role_style}]{player_id}:[/bold {role_style}] [italic]\"{message}\"[/italic]")
        
        # Update the state with the discussion
        state = agent.apply_move(state, player_id, move)
        
        # Add delay for readability
        if interactive:
            console.print("[cyan]Press Enter to continue...[/cyan]")
            input()
        else:
            time.sleep(1.0 / speed)
    
    # Transition to voting phase
    console.print("\n[bold yellow]Discussion complete. Moving to voting phase...[/bold yellow]")
    state = agent.advance_phase(state)
    
    return state

def process_voting_phase(agent, state, console, interactive, speed):
    """
    Process a meeting's voting phase with enhanced visibility.
    
    Args:
        agent: The AmongUsAgent instance
        state: Current game state
        console: Rich console for display
        interactive: Whether in interactive mode
        speed: Simulation speed multiplier
    
    Returns:
        Updated state
    """
    console.print("\n[bold]VOTING PHASE[/bold]")
    
    # Show discussion summary
    if hasattr(state, "discussion_history") and state.discussion_history:
        console.print("\n[bold]Discussion Summary:[/bold]")
        for msg in state.discussion_history[-len(state.player_states):]:  # Show last messages
            player_id = msg.get("player_id", "Unknown")
            message = msg.get("message", "")
            
            player_style = "red"
            if player_id in state.player_states:
                role = state.player_states[player_id].role
                player_style = "green" if role == PlayerRole.CREWMATE else "red"
            
            console.print(f"[{player_style}]{player_id}[/{player_style}]: [dim]{message[:100]}{'...' if len(message) > 100 else ''}[/dim]")
    
    # Process each player's vote
    alive_players = [pid for pid, pstate in state.player_states.items() if pstate.is_alive]
    
    for player_id in alive_players:
        player_state = state.player_states[player_id]
        role = player_state.role
        
        # Skip players who already voted
        if player_id in state.votes:
            vote_target = state.votes[player_id]
            console.print(f"[dim]{player_id} already voted for {vote_target}[/dim]")
            continue
        
        # Show whose turn it is to vote
        role_style = "green" if role == PlayerRole.CREWMATE else "red"
        console.print(f"\n[bold {role_style}]{player_id}'s turn to vote[/bold {role_style}]")
        
        # Create context for the player
        move_context = agent.prepare_move_context(state, player_id)
        
        # Get the voting engine
        engine = agent.get_engine_for_player(role, "voting")
        if not engine:
            console.print(f"[bold red]No voting engine found for {player_id}[/bold red]")
            continue
        
        # Generate the player's vote
        console.print(f"[dim]Thinking about vote...[/dim]")
        response = engine.invoke(move_context)
        
        # Extract the vote
        move = agent.extract_move(response, role)
        vote_target = move.get("vote_for", "skip")
        
        # Display the vote
        vote_style = "yellow" if vote_target == "skip" else "bold"
        console.print(f"[{role_style}]{player_id}[/{role_style}] votes for [{vote_style}]{vote_target}[/{vote_style}]")
        
        # Update the state with the vote
        state = agent.apply_move(state, player_id, move)
        
        # Add delay for readability
        if interactive:
            console.print("[cyan]Press Enter to continue...[/cyan]")
            input()
        else:
            time.sleep(0.5 / speed)
    
    # Count votes
    console.print("\n[bold]Vote Results:[/bold]")
    vote_counts = {}
    for target in state.votes.values():
        vote_counts[target] = vote_counts.get(target, 0) + 1
    
    for target, count in sorted(vote_counts.items(), key=lambda x: x[1], reverse=True):
        style = "yellow" if target == "skip" else "cyan"
        console.print(f"[{style}]{target}[/{style}]: {count} votes")
    
    # Determine ejection
    max_votes = 0
    ejected_player = None
    
    for player, count in vote_counts.items():
        if player != "skip" and count > max_votes:
            max_votes = count
            ejected_player = player
    
    skip_votes = vote_counts.get("skip", 0)
    if ejected_player and skip_votes < max_votes:
        # Check for ties
        tied_players = [p for p, c in vote_counts.items() 
                      if p != "skip" and p != ejected_player and c == max_votes]
        
        if not tied_players:  # No tie
            player_role = "unknown"
            if ejected_player in state.player_states:
                role = state.player_states[ejected_player].role
                player_role = "CREWMATE" if role == PlayerRole.CREWMATE else "IMPOSTOR"
                role_style = "green" if role == PlayerRole.CREWMATE else "red"
            
            console.print(f"\n[bold red]EJECTED: {ejected_player} - {player_role}[/bold red]")
        else:
            console.print(f"\n[bold yellow]TIE VOTE - No one ejected[/bold yellow]")
            console.print(f"Tied between: {ejected_player} and {', '.join(tied_players)}")
    else:
        console.print(f"\n[bold yellow]SKIPPED - No one ejected[/bold yellow]")
    
    # Return to task phase
    state = agent.advance_phase(state)
    
    return state

def process_random_events(agent, state, console, interactive, speed):
    """Process random events that might occur during the task phase."""
    # Check if a random event should occur
    if random.random() < 0.3 and not state.meeting_active:
        # Random player calls meeting or reports body
        alive_players = [pid for pid, pstate in state.player_states.items() if pstate.is_alive]
        if alive_players:
            caller = random.choice(alive_players)
            console.print(f"[bold yellow]{caller} discovered something suspicious![/bold yellow]")
            
            # Check for dead bodies in caller's location
            caller_location = state.player_states[caller].location
            dead_bodies = [
                pid for pid, pstate in state.player_states.items()
                if not pstate.is_alive and pstate.location == caller_location
            ]
            
            if dead_bodies:
                # Report body
                move = {"action": "report_body"}
                console.print(f"[bold red]{caller} found a body![/bold red]")
            else:
                # Call emergency meeting
                move = {"action": "call_emergency_meeting"}
                console.print(f"[bold yellow]{caller} called an emergency meeting![/bold yellow]")
            
            state = agent.apply_move(state, caller, move)
            
            # Check phase transition
            if state.game_phase == AmongUsGamePhase.MEETING:
                agent.visualize_state(state)
                
                if interactive:
                    console.print("[bold cyan]Press Enter to continue to meeting...[/bold cyan]")
                    input()
                else:
                    time.sleep(2.0 / speed)
    
    return state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an Among Us AI game simulation")
    parser.add_argument("--players", type=int, default=6, help="Number of players (4-10)")
    parser.add_argument("--impostors", type=int, default=1, help="Number of impostors (1-3)")
    parser.add_argument("--map", type=str, default="skeld", choices=["skeld", "polus", "mira"], help="Map name")
    parser.add_argument("--save", type=str, help="Path to save game")
    parser.add_argument("--load", type=str, help="Path to load game")
    parser.add_argument("--non-interactive", action="store_true", help="Run in non-interactive mode")
    parser.add_argument("--rounds", type=int, default=15, help="Maximum number of rounds")
    parser.add_argument("--speed", type=float, default=1.0, help="Simulation speed multiplier")
    
    args = parser.parse_args()
    
    run_among_us_demo(
        player_count=args.players,
        impostor_count=args.impostors,
        map_name=args.map,
        save_path=args.save,
        load_path=args.load,
        interactive=not args.non_interactive,
        max_rounds=args.rounds,
        speed=args.speed
    )