"""LLM prompt templates for the Battleship game.

This module provides prompt templates for various game actions in Battleship,
including ship placement, move selection, and strategic analysis. The prompts
are designed to elicit optimal decision-making from LLM agents.

Key Components:
    - Ship Placement: Strategic positioning of ships
    - Move Selection: Target coordinate choice
    - Strategic Analysis: Pattern recognition and planning

Example:
    >>> from langchain_core.prompts import ChatPromptTemplate
    >>> placement_prompt = generate_ship_placement_prompt("Player 1")
    >>> move_prompt = generate_move_prompt("Player 1")
    >>> analysis_prompt = generate_analysis_prompt("Player 1")
"""

from langchain_core.prompts import ChatPromptTemplate

def generate_ship_placement_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for strategic ship placement.
    
    Creates a prompt template that guides the LLM in placing ships
    optimally on the game board. The prompt emphasizes:
    - Strategic positioning
    - Ship survivability
    - Unpredictability
    - Valid placement rules
    
    Args:
        player (str): Name/identifier of the player placing ships
        
    Returns:
        ChatPromptTemplate: Template for ship placement decisions
        
    Example:
        >>> prompt = generate_ship_placement_prompt("Player 1")
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
            "YOU CANNOT DO anything with coordinates outside the range 0-9.\n"
            "🚀 **Strategic Guidelines:**\n"
            "1️⃣ **Avoid the edges too much** – it's easy for opponents to scan row 0/9 or col 0/9.\n"
            "2️⃣ **Do not cluster ships together** – spread them across the board.\n"
            "3️⃣ **Use a mix of horizontal & vertical ships** – avoid making it too predictable.\n"
            "4️⃣ **Avoid placing ships perfectly aligned next to each other.**\n"
            "5️⃣ **Ensure all ships fit without overlapping existing ones.**\n"
            "\n"
            "📌 **Ship Placement Format:**\n"
            "You must return a JSON for `ShipPlacement` with:\n"
            "  - `ship_name`: The ship being placed.\n"
            "  - `coordinates`: A list of `(row, col)` positions in a straight line.\n"
            "\n"
            "🚨 **Constraints:**\n"
            "✅ Ships must be placed **in a straight line** (horizontal or vertical).\n"
            "✅ Ships **must not overlap with**: {occupied_positions}\n"
            "✅ Ensure **strategic positioning** based on the game board.\n"
            "✅ The ship size must match its standard length: Carrier (5), Battleship (4), Cruiser (3), Submarine (3), Destroyer (2).\n"
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
            "🎯 **Respond with ShipPlacement JSON.**\n"
        )
    ])

def generate_move_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for move selection.
    
    Creates a prompt template that guides the LLM in choosing
    optimal attack coordinates based on:
    - Current board state
    - Hit/miss patterns
    - Ship locations
    - Strategic analysis
    
    Args:
        player (str): Name/identifier of the player making the move
        
    Returns:
        ChatPromptTemplate: Template for move selection
        
    Example:
        >>> prompt = generate_move_prompt("Player 1")
        >>> messages = prompt.format_messages(
        ...     board_size=10,
        ...     your_hits=[(0, 0)],
        ...     your_misses=[(1, 1)],
        ...     opponent_hits=[],
        ...     opponent_misses=[],
        ...     your_sunken_ships=[],
        ...     opponent_sunken_ships=[],
        ...     strategic_thoughts=[]
        ... )
    """
    return ChatPromptTemplate.from_messages([
        (
            'system', 
            f"You are {player} in a game of Battleship. Your goal is to select the best move.\n"
            "The board is 10x10 and 0-indexed (0-9). The first row and column are 0,0 and the last row and column are 9,9.\n"
            "YOU CANNOT choose coordinates outside the range of 0-9.\n"
            "YOU MUST analyze the board state carefully to select your next attack coordinate.\n"
            "\n"
            "RULES FOR CHOOSING A TARGET:\n"
            "1. Never target a position you've already attacked (in your hits or misses)\n"
            "2. If you have hits that might be part of a ship, target adjacent squares to try to sink it\n"
            "3. Focus on likely ship locations based on pattern recognition\n"
            "4. Respond with a valid JSON for a PlayerMove with the 'move' field containing row and col coordinates\n"
            "\n"
            "RESPOND with a JSON for the coordinate you want to attack next."
        ),
        (
            'human',
            "📌 **Game Context:**\n"
            "🔲 **Board Size:** {board_size}x{board_size}\n"
            "💥 **Your Hits:** {your_hits}\n"
            "❌ **Your Misses:** {your_misses}\n"
            "🚨 **Opponent's Hits (on your board):** {opponent_hits}\n"
            "📉 **Opponent's Misses (on your board):** {opponent_misses}\n"
            "⚓ **Your Sunken Ships:** {your_sunken_ships}\n"
            "🔥 **Opponent's Sunken Ships:** {opponent_sunken_ships}\n"
            "💭 **Strategic Thoughts:** {strategic_thoughts}\n\n"
            "🎯 **Your Turn! Choose an attack coordinate (row, col).**"
        )
    ])

def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for strategic analysis.
    
    Creates a prompt template that guides the LLM in analyzing
    the current game state and providing strategic advice based on:
    - Hit/miss patterns
    - Ship positions
    - Probability analysis
    - Historical moves
    
    Args:
        player (str): Name/identifier of the player requesting analysis
        
    Returns:
        ChatPromptTemplate: Template for strategic analysis
        
    Example:
        >>> prompt = generate_analysis_prompt("Player 1")
        >>> messages = prompt.format_messages(
        ...     your_hits=[(0, 0)],
        ...     your_misses=[(1, 1)],
        ...     opponent_hits=[],
        ...     opponent_misses=[],
        ...     your_sunken_ships=[],
        ...     opponent_sunken_ships=[],
        ...     move_history=[]
        ... )
    """
    return ChatPromptTemplate.from_messages([
        (
            'system', 
            f"You are analyzing {player}'s position in Battleship.\n"
            "It is a 10x10 board 0-indexed (0-9), so coordinates range from (0,0) to (9,9).\n"
            "YOUR TASK is to analyze the current board state and provide strategic advice.\n"
            "FOCUS on:\n"
            "1. Identifying patterns in hits and misses\n"
            "2. Determining likely locations of remaining enemy ships\n"
            "3. Suggesting optimal attack coordinates for next moves\n"
            "4. Evaluating which parts of the board have highest probability of containing ships\n"
            "\n"
            "Your analysis should be clear, concise, and actionable. Remember that opponent's hits and misses are on YOUR board, not the opponent's board."
        ),
        (
            'human',
            "📌 **Analysis Required:**\n"
            "✅ **Your Hits:** {your_hits}\n"
            "❌ **Your Misses:** {your_misses}\n"
            "🚨 **Opponent's Hits (ON YOUR BOARD):** {opponent_hits}\n"
            "📉 **Opponent's Misses (ON YOUR BOARD):** {opponent_misses}\n"
            "⚓ **Your Sunken Ships:** {your_sunken_ships}\n"
            "🔥 **Opponent's Sunken Ships:** {opponent_sunken_ships}\n"
            "📜 **Recent Move History:** {move_history}\n\n"
            "🎯 **Based on probability and pattern recognition, provide strategic analysis.**"
        )
    ])