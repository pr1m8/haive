from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.games.reversi.models import ReversiMove, ReversiAnalysis

def generate_move_prompt(player_symbol: str) -> ChatPromptTemplate:
    """Generate a prompt for making a move in Reversi/Othello."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are playing as {player_symbol} in a game of Reversi (also known as Othello). "
            f"{'Black' if player_symbol == 'B' else 'White'} discs are represented as '{player_symbol}'.\n\n"
            f"Rules:\n"
            f"1. Players take turns placing discs on the board.\n"
            f"2. A valid move must capture at least one opponent's disc by flanking it between your new disc and an existing disc of your color.\n"
            f"3. Captured discs are flipped to your color.\n"
            f"4. If a player cannot make a valid move, they must pass their turn.\n"
            f"5. The game ends when neither player can make a valid move or the board is full.\n"
            f"6. The player with the most discs of their color wins."
        ),
        ('human', 
            "Current Board:\n"
            "{board_string}\n\n"
            "It's your turn ({current_player}).\n\n"
            "Legal moves (row, col):\n{legal_moves}\n\n"
            "Previous analysis (if available):\n{player_analysis}\n\n"
            "Choose one of the legal moves. Explain your reasoning and return a ReversiMove object with your row, col, and player."
        )
    ])

def generate_analysis_prompt(player_symbol: str) -> ChatPromptTemplate:
    """Generate a prompt for analyzing a Reversi/Othello position."""
    player_color = "Black" if player_symbol == "B" else "White"
    opponent_symbol = "W" if player_symbol == "B" else "B"
    opponent_color = "White" if player_symbol == "B" else "Black"

    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a Reversi/Othello strategy expert. Analyze the position from the perspective of player {player_symbol} ({player_color}).\n\n"
            f"Key Reversi concepts:\n"
            f"- Mobility: Having more legal moves gives you flexibility\n"
            f"- Corner control: Corners are strategically valuable as they can never be flipped\n"
            f"- Edge control: Edge discs are harder to flip than center discs\n"
            f"- Stability: Stable discs are those that cannot be flipped for the remainder of the game\n"
            f"- Parity: Having the last move in a region is advantageous\n"
            f"- Frontier discs: Discs adjacent to empty spaces are vulnerable"
        ),
        ('human', 
            "Current Board:\n"
            "{board_string}\n\n"
            "Player: {player_symbol} ({player_color})\n"
            "Opponent: {opponent_symbol} ({opponent_color})\n\n"
            "Legal moves (row, col):\n{legal_moves}\n\n"
            "Disc count: Black: {black_count}, White: {white_count}\n\n"
            "Analyze this position. Consider:\n"
            "1. Mobility (number of legal moves)\n"
            "2. Corner and edge control\n"
            "3. Disc stability and frontier discs\n"
            "4. Positional advantages and disadvantages\n"
            "5. Short-term vs. long-term strategy\n\n"
            "Provide a detailed analysis and specific move recommendations by coordinates (row, col)."
        )
    ])


# Define the AugLLM configurations
reversi_engines = {
    "B_player": AugLLMConfig(
        name="B_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
        prompt_template=generate_move_prompt("B"),
        structured_output_model=ReversiMove
    ),
    "W_player": AugLLMConfig(
        name="W_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
        prompt_template=generate_move_prompt("W"),
        structured_output_model=ReversiMove
    ),
    "B_analyzer": AugLLMConfig(
        name="B_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("B"),
        structured_output_model=ReversiAnalysis
    ),
    "W_analyzer": AugLLMConfig(
        name="W_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("W"),
        structured_output_model=ReversiAnalysis
    )
}