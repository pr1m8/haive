"""Augmented LLM configurations for the Battleship game.

This module provides LLM configurations and prompt templates for different
roles in the Battleship game. It includes specialized prompts for ship
placement, move selection, and strategic analysis, along with structured
output models for each role.

Key Components:
    - Ship Placement: Strategic ship positioning prompts
    - Move Selection: Targeting decision prompts
    - Analysis: Strategic game state analysis
    - LLM Configs: Role-specific configurations

Example:
    >>> from src.haive.games.battleship.aug_llms import aug_llm_configs
    >>> 
    >>> # Get player 1's ship placement configuration
    >>> placement_config = aug_llm_configs["player1_ship_placement"]
    >>> 
    >>> # Get player 2's move selection configuration
    >>> move_config = aug_llm_configs["player2"]
"""

from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.games.battleship.models import (
    BattleshipPlacement,
    BattleshipMoveModel, 
    BattleshipAnalysis
)

def generate_battleship_ship_placement_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for strategic ship placement.
    
    Creates a prompt template that guides the LLM in placing ships
    optimally on the game board. The prompt emphasizes:
    - Strategic positioning
    - Ship survivability
    - Board coverage
    - Valid placement rules
    
    Args:
        player (str): Name/identifier of the player placing ships
        
    Returns:
        ChatPromptTemplate: Template for ship placement decisions
        
    Example:
        >>> prompt = generate_battleship_ship_placement_prompt("Player 1")
        >>> messages = prompt.format_messages(
        ...     ship_name="Carrier",
        ...     board_size=10,
        ...     occupied_positions=[]
        ... )
    """
    return ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are {player}, setting up your fleet for Battleship with a **winning strategy**.\n"
            "Your goal is to **maximize survivability** and **make enemy detection harder**.\n"
            "The board is 10x10, 0-indexed (0-9). The first row and column are 0,0 and the last row and column are 9,9.\n"
            "YOU CANNOT DO anything with (1,10) or (10,1) or (10,10) because 10 is out of bounds.\n"
            "🚀 **Strategic Guidelines:**\n"
            "1️⃣ **Avoid the edges too much** – it's easy for opponents to scan row 0/9 or col 0/9.\n"
            "2️⃣ **Do not cluster ships together** – spread them across the board.\n"
            "3️⃣ **Use a mix of horizontal & vertical ships** – avoid making it too predictable.\n"
            "4️⃣ **Avoid placing ships perfectly aligned next to each other.**\n"
            "5️⃣ **Ensure all ships fit without overlapping existing ones.**\n"
            "\n"
            "📌 **Ship Placement Format:**\n"
            "You must return a JSON function call for `BattleshipPlacement` with:\n"
            "  - `ship_name`: The ship being placed.\n"
            "  - `ship_size`: The size of the ship.\n"
            "  - `coordinates`: A list of `(row, col)` positions in a straight line.\n"
            "  - `occupied_positions`: A list of already placed ship positions.\n"
            "\n"
            "🚨 **Constraints:**\n"
            "✅ Ships must be placed **in a straight line** (horizontal or vertical).\n"
            "✅ Ships **must not overlap with**: {occupied_positions}\n"
            "✅ Ensure **strategic positioning** based on the game board.\n"
            "\n"
            "🎯 Example JSON Response:\n"
            "{{\n"
            "  \"ship_name\": \"Carrier\",\n"
            "  \"ship_size\": 5,\n"
            "  \"coordinates\": [\n"
            "    {{ \"row\": 1, \"col\": 2 }},\n"
            "    {{ \"row\": 1, \"col\": 3 }},\n"
            "    {{ \"row\": 1, \"col\": 4 }},\n"
            "    {{ \"row\": 1, \"col\": 5 }},\n"
            "    {{ \"row\": 1, \"col\": 6 }}\n"
            "  ]\n"
            "}}\n"
        ),
        (
            "human",
            "📌 **Your Turn:**\n"
            "You are placing `{ship_name}` on a `{board_size}x{board_size}` board.\n"
            "🚧 **Occupied Positions:** {occupied_positions}\n"
            "⚡ **Strategy Required:**\n"
            "  - Ensure the ship is **not too easy to find**.\n"
            "  - Consider **defensive positioning**.\n"
            "  - Choose a **direction that maximizes unpredictability**.\n"
            "  - **No overlapping** with existing ships.\n"
            "\n"
            "🎯 **Respond with a valid JSON structure.**\n"
        )
    ])

def generate_battleship_move_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for move selection.
    
    Creates a prompt template that guides the LLM in choosing optimal attack coordinates.
    
    Args:
        player (str): Name/identifier of the player making the move
        
    Returns:
        ChatPromptTemplate: Template for move selection
    """
    return ChatPromptTemplate.from_messages([
        (
            'system', 
            f"You are {player} in a game of Battleship. Your goal is to select the best attack coordinates.\n\n"
            "# BOARD INFORMATION\n"
            "- The board is 10x10 and 0-indexed (0-9)\n"
            "- Valid coordinates range from (0,0) to (9,9)\n"
            "- Ships are placed horizontally or vertically\n\n"
            
            "# TARGETING RULES\n"
            "1. NEVER target a position you've already attacked (check your hits and misses lists)\n"
            "2. If you have hits that might be part of a ship, prioritize adjacent squares\n"
            "3. Use probability to find likely ship locations\n"
            "4. When you find a hit, explore horizontally and vertically from that position\n\n"
            
            "# RESPONSE FORMAT\n"
            "You must respond with a valid JSON containing row and col coordinates:\n"
            "```json\n"
            "{{\n"
            "  \"row\": 3,  // Integer between 0-9\n"
            "  \"col\": 5   // Integer between 0-9\n"
            "}}\n"
            "```"
        ),
        (
            'human',
            "# CURRENT GAME STATE\n\n"
            "## Board Information\n"
            "- Board Size: {board_size}x{board_size}\n\n"
            
            "## Your Attack History\n"
            "- Your Hits: {your_hits}\n"
            "- Your Misses: {your_misses}\n"
            "- Opponent's Sunken Ships: {opponent_sunken_ships}\n\n"
            
            "## Opponent's Attacks Against You\n"
            "- Opponent's Hits (on your board): {opponent_hits}\n"
            "- Opponent's Misses (on your board): {opponent_misses}\n"
            "- Your Sunken Ships: {your_sunken_ships}\n\n"
            
            "## Your Strategy Notes\n"
            "{strategic_thoughts}\n\n"
            
            "# YOUR TASK\n"
            "Choose your next attack coordinates (row, col)."
        )
    ])

def generate_battleship_analysis_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for strategic analysis.
    
    Creates a prompt template that guides the LLM in analyzing the current game state
    and providing strategic advice.
    
    Args:
        player (str): Name/identifier of the player requesting analysis
        
    Returns:
        ChatPromptTemplate: Template for strategic analysis
    """
    return ChatPromptTemplate.from_messages([
        (
            'system', 
            f"You are the strategic analyst for {player} in a Battleship game.\n\n"
            "# YOUR ROLE\n"
            "Analyze the current board state and provide actionable strategic advice.\n\n"
            
            "# FOCUS AREAS\n"
            "1. PATTERN ANALYSIS: Identify patterns in hits and misses\n"
            "2. SHIP LOCATION: Determine likely locations of remaining enemy ships\n"
            "3. TARGETING ADVICE: Suggest specific coordinates for next attacks\n"
            "4. PROBABILITY ASSESSMENT: Evaluate which board areas likely contain ships\n\n"
            
            "# IMPORTANT NOTES\n"
            "- Opponent's hits and misses are on YOUR board, not their board\n"
            "- The board is 0-indexed (0,0 to 9,9)\n"
            "- Ships are placed horizontally or vertically\n"
            "- Respond with clear, actionable analysis in 3-5 paragraphs"
        ),
        (
            'human',
            "# CURRENT GAME STATE\n\n"
            
            "## Your Attack History\n"
            "- Your Hits: {your_hits}\n"
            "- Your Misses: {your_misses}\n"
            "- Opponent's Sunken Ships: {opponent_sunken_ships}\n\n"
            
            "## Opponent's Attacks Against You\n"
            "- Opponent's Hits (on your board): {opponent_hits}\n"
            "- Opponent's Misses (on your board): {opponent_misses}\n"
            "- Your Sunken Ships: {your_sunken_ships}\n\n"
            
            "## Strategy Information\n"
            "- Previous Thoughts: {strategic_thoughts}\n"
            "- Current Board Size: {board_size}\n\n"
            
            "# YOUR TASK\n"
            "Provide strategic analysis and targeting recommendations for the next moves."
        )
    ])
# LLM configurations for different roles in the game
aug_llm_configs = {
    # Ship placement configurations
    "player1_ship_placement": AugLLMConfig(
        name="player1_ship_placement",
        prompt_template=generate_battleship_ship_placement_prompt("Player 1"),
        structured_output_model=BattleshipPlacement
    ),
    "player2_ship_placement": AugLLMConfig(
        name="player2_ship_placement",
        prompt_template=generate_battleship_ship_placement_prompt("Player 2"),
        structured_output_model=BattleshipPlacement
    ),
    
    # Move selection configurations
    "player1": AugLLMConfig(
        name="player1",
        prompt_template=generate_battleship_move_prompt("Player 1"),
        structured_output_model=BattleshipMoveModel
    ),
    "player2": AugLLMConfig(
        name="player2",
        prompt_template=generate_battleship_move_prompt("Player 2"),
        structured_output_model=BattleshipMoveModel
    ),
    
    # Strategic analysis configurations
    "player1_analyzer": AugLLMConfig(
        name="player1_analyzer",
        prompt_template=generate_battleship_analysis_prompt("Player 1"),
        structured_output_model=BattleshipAnalysis
    ),
    "player2_analyzer": AugLLMConfig(
        name="player2_analyzer",
        prompt_template=generate_battleship_analysis_prompt("Player 2"),
        structured_output_model=BattleshipAnalysis
    )
}
