"""
Battleship game prompt templates.

This module provides prompt templates for various game actions in Battleship, including:
    - Ship placement
    - Move selection
    - Strategic analysis
"""

from langchain_core.prompts import ChatPromptTemplate

def generate_ship_placement_prompt(player: str) -> ChatPromptTemplate:
    """
    Generate a prompt for strategic ship placement.
    
    Args:
        player: Player name/identifier
        
    Returns:
        ChatPromptTemplate for ship placement decisions
    """
    return ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are {player}, setting up your fleet for Battleship with a **winning strategy**.\n"
            "Your goal is to **maximize survivability** and **make enemy detection harder**.\n"
            "The board is 10x10, 0-indexed (0-9). The first row and column are 0,0 and the last row and column are 9,9.\n"
            "🚀 **Strategic Guidelines:**\n"
            "1️⃣ **Avoid the edges too much** – it's easy for opponents to scan row 0/9 or col 0/9.\n"
            "2️⃣ **Do not cluster ships together** – spread them across the board.\n"
            "3️⃣ **Use a mix of horizontal & vertical ships** – avoid making it too predictable.\n"
            "4️⃣ **Ensure all ships fit without overlapping existing ones.**\n"
            "\n"
            "📌 **Ship Placement Format:**\n"
            "You must return a JSON list of placements with:\n"
            "  - `ship_type`: The ship being placed (Carrier, Battleship, Cruiser, Submarine, Destroyer).\n"
            "  - `coordinates`: A list of `(row, col)` positions in a straight line.\n"
            "\n"
            "🚨 **Constraints:**\n"
            "✅ Ships must be placed **in a straight line** (horizontal or vertical).\n"
            "✅ Ships **must not overlap with**: {occupied_positions}\n"
            "✅ Ensure **strategic positioning**.\n"
            "✅ The ship size must match its standard length: Carrier (5), Battleship (4), Cruiser (3), Submarine (3), Destroyer (2).\n"
        ),
        (
            "human",
            "📌 **Your Turn:**\n"
            "You need to place all five ships: Carrier (5), Battleship (4), Cruiser (3), Submarine (3), and Destroyer (2).\n"
            "🎮 Board Size: 10x10 (0-9 coordinates)\n"
            "🚧 Occupied Positions: {occupied_positions}\n"
            "⚡ Strategy Required:\n"
            "  - Ensure ships are **not too easy to find**.\n"
            "  - Consider **defensive positioning**.\n"
            "  - Choose **directions that maximize unpredictability**.\n"
            "  - **No overlapping** between ships.\n"
            "\n"
            "🎯 Return a JSON list of ship placements.\n"
        )
    ])

from langchain_core.prompts import ChatPromptTemplate

def generate_move_prompt(player: str) -> ChatPromptTemplate:
    """
    Generate a prompt for move selection.
    
    Args:
        player: Player name/identifier
        
    Returns:
        ChatPromptTemplate for move selection
    """
    return ChatPromptTemplate.from_messages([
        (
            'system', 
            f"You are {player} in a game of Battleship. Your goal is to find and sink all enemy ships.\n\n"
            "# BOARD INFORMATION\n"
            "- 10x10 board with coordinates from (0,0) to (9,9)\n"
            "- Ships are: Carrier (5), Battleship (4), Cruiser (3), Submarine (3), Destroyer (2)\n\n"
            
            "# TARGETING RULES\n"
            "1. NEVER target a position you've already attacked (check your hits and misses lists)\n"
            "2. If you have hits that might be part of a ship, prioritize adjacent squares\n"
            "3. Use probability to find likely ship locations\n"
            "4. When you find a hit, explore horizontally and vertically from that position\n\n"
            
            "# RESPONSE FORMAT\n"
            "Return a JSON with row and col coordinates:\n"
            "```json\n"
            "{{ \n"
            "  \"row\": 3,  // Integer between 0-9\n"
            "  \"col\": 5   // Integer between 0-9\n"
            "}}\n"
            "```"
        ),
        (
            'human',
            "# CURRENT GAME STATE\n\n"
            "## Your Attack History\n"
            "- Your Hits: {your_hits}\n"
            "- Your Misses: {your_misses}\n"
            "- Enemy Ships You've Sunk: {your_sunk_ships}\n\n"
            
            "## Enemy's Attacks Against You\n"
            "- Hits on Your Ships: {opponent_hits}\n"
            "- Misses on Your Board: {opponent_misses}\n"
            "- Your Ships That Are Sunk: {opponent_sunk_ships}\n\n"
            
            "## Strategic Information\n"
            "- Previous Analysis: {strategic_thoughts}\n\n"
            
            "# YOUR TASK\n"
            "Choose your next attack coordinate. Remember to avoid previously targeted positions.\n"
        )
    ])

def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
    """
    Generate a prompt for strategic analysis.
    
    Args:
        player: Player name/identifier
        
    Returns:
        ChatPromptTemplate for strategic analysis
    """
    return ChatPromptTemplate.from_messages([
        (
            'system', 
            f"You are a Battleship strategist analyzing the game for {player}.\n\n"
            "# YOUR ROLE\n"
            "Analyze the current board state and provide actionable strategic advice.\n\n"
            
            "# FOCUS AREAS\n"
            "1. PATTERN ANALYSIS: Identify patterns in hits and misses\n"
            "2. SHIP LOCATION: Determine likely locations of remaining enemy ships\n"
            "3. TARGETING ADVICE: Suggest specific coordinates for next attacks\n"
            "4. PROBABILITY ASSESSMENT: Evaluate which board areas likely contain ships\n\n"
            
            "# RESPONSE FORMAT\n"
            "Provide a clear, concise strategic analysis in 3-4 paragraphs. Focus on actionable insights."
        ),
        (
            'human',
            "# GAME ANALYSIS REQUEST\n\n"
            
            "## Your Attack History\n"
            "- Your Hits: {your_hits}\n"
            "- Your Misses: {your_misses}\n"
            "- Enemy Ships You've Sunk: {opponent_sunk_ships}\n\n"
            
            "## Enemy's Attacks Against You\n"
            "- Hits on Your Ships: {opponent_hits}\n"
            "- Misses on Your Board: {opponent_misses}\n"
            "- Your Ships That Are Sunk: {your_sunk_ships}\n\n"
            
            "## Previous Analysis\n"
            "{strategic_thoughts}\n\n"
            
            "# YOUR TASK\n"
            "Analyze the game state and provide strategic targeting advice."
        )
    ])