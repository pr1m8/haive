#https://claude.ai/chat/bf8fa48a-f8d4-4acd-ba1f-7e42843c9386
from typing import Dict, Any, List
from langgraph.types import Command
from src.haive.games.framework.base import GameAgent
from .models import MastermindState, MastermindGuess, MastermindFeedback
from .state import MastermindStateManager
from src.haive.core.engine.agent.agent import register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import time
import random

class MastermindAnalysis(BaseModel):
    """Analysis for Mastermind gameplay."""
    possible_solutions: List[List[str]] = Field(..., description="List of possible solutions that match all feedback so far")
    confidence: int = Field(..., ge=0, le=100, description="Confidence level in next guess (0-100)")
    elimination_strategy: str = Field(..., description="Strategy for eliminating possibilities")
    next_guess_reasoning: str = Field(..., description="Reasoning for the next guess")

def generate_guess_prompt() -> ChatPromptTemplate:
    """Generate a prompt for making a guess in Mastermind."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are the codebreaker in a game of Mastermind. Your goal is to guess the secret code.\n\n"
            "Rules:\n"
            "1. The code consists of 4 colors chosen from: red, green, blue, yellow, purple, orange.\n"
            "2. The same color can appear multiple times.\n"
            "3. After each guess, you receive feedback:\n"
            "   - Exact matches: Correct color in correct position\n"
            "   - Color matches: Correct color in wrong position\n"
            "4. You must deduce the code in as few guesses as possible."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            "Guesses remaining: {guesses_remaining}\n\n"
            "Previous Guesses and Feedback:\n{guess_history}\n\n"
            "Make your next guess. Use logical deduction based on the feedback received so far.\n"
            "Return a list of exactly 4 colors from: red, green, blue, yellow, purple, orange."
        )
    ])

def generate_code_prompt() -> ChatPromptTemplate:
    """Generate a prompt for creating a secret code in Mastermind."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are the codemaker in a game of Mastermind. Your task is to create a challenging secret code.\n\n"
            "Rules:\n"
            "1. The code must consist of exactly 4 colors.\n"
            "2. Choose from: red, green, blue, yellow, purple, orange.\n"
            "3. The same color can appear multiple times.\n"
            "4. Try to create a code that will be difficult to guess but still fair."
        ),
        ('human', 
            "Create a secret code for a Mastermind game.\n"
            "Return a list of exactly 4 colors from: red, green, blue, yellow, purple, orange."
        )
    ])

def generate_analysis_prompt() -> ChatPromptTemplate:
    """Generate a prompt for analyzing Mastermind gameplay."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a Mastermind strategy expert. Analyze the current game state and provide insights."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            "Previous Guesses and Feedback:\n{guess_history}\n\n"
            "Analyze the current game state. Consider:\n"
            "1. What possible codes remain based on the feedback?\n"
            "2. What would be an optimal next guess?\n"
            "3. What elimination strategy should be used?\n"
            "Provide a detailed analysis with possible solutions that match all feedback."
        )
    ])

# Define the AugLLM configurations
aug_llm_configs = {
    "codebreaker": AugLLMConfig(
        name="codebreaker",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_guess_prompt(),
        structured_output_model=MastermindGuess
    ),
    "codemaker": AugLLMConfig(
        name="codemaker",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_code_prompt(),
        structured_output_model=List[str]
    ),
    "analyzer": AugLLMConfig(
        name="analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt(),
        structured_output_model=MastermindAnalysis
    ),
}

class MastermindConfig(GameConfig):
    """Configuration for the Mastermind agent."""
    state_schema: Type[MastermindState] = Field(default=MastermindState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs, description="Config for the Mastermind agent."
    )
    enable_analysis: bool = Field(
        default=True, description="Whether to enable analysis."
    )
    visualize: bool = Field(
        default=True, description="Whether to visualize the game."
    )
    max_guesses: int = Field(
        default=10, description="Maximum number of guesses allowed."
    )
    use_ai_codemaker: bool = Field(
        default=False, description="Whether to use AI to create the secret code."
    )

    @classmethod
    def default_config(cls):
        """Create a default configuration."""
        return cls(
            state_schema=MastermindState,
            aug_llm_configs=aug_llm_configs,
            enable_analysis=True,
            visualize=True,
            max_guesses=10,
            use_ai_codemaker=False
        )

@register_agent(MastermindConfig)
class MastermindAgent(GameAgent[MastermindConfig]):
    """Agent for playing Mastermind."""
    
    def __init__(self, config: MastermindConfig = MastermindConfig()):
        """Initialize the Mastermind agent."""
        super().__init__(config)
        self.state_manager = MastermindStateManager
        self.engines = config.aug_llm_configs
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new Mastermind game with secret code."""
        # Generate secret code
        secret_code = None
        if self.config.use_ai_codemaker:
            # Use AI to generate code
            try:
                codemaker = self.engines.get("codemaker")
                if codemaker:
                    secret_code = codemaker.invoke({})
            except Exception as e:
                print(f"Error generating code with AI: {e}")
                # Fall back to random code
                secret_code = None
        
        if secret_code is None:
            # Generate random code
            colors = ["red", "green", "blue", "yellow", "purple", "orange"]
            secret_code = random.choices(colors, k=4)
        
        # Initialize game state
        game_state = self.state_manager.initialize(
            secret_code=secret_code,
            max_guesses=self.config.max_guesses
        )
        
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def prepare_move_context(self, state: MastermindState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation."""
        # Format guess history
        guess_history = []
        for i, (guess, feedback) in enumerate(zip(state.guesses, state.feedback)):
            guess_history.append(f"Guess {i+1}: {', '.join(guess.colors)} → {feedback.exact_matches} exact, {feedback.color_matches} color")
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "guesses_remaining": state.max_guesses - len(state.guesses),
            "guess_history": "\n".join(guess_history)
        }
    
    def extract_move(self, response: Any) -> MastermindGuess:
        """Extract move from engine response."""
        # The response should already be a MastermindGuess object
        return response
    
    def make_player1_move(self, state: MastermindState) -> Command:
        """Make a move for codebreaker."""
        return self.make_move(state, "codebreaker")
    
    def make_player2_move(self, state: MastermindState) -> Command:
        """In Mastermind, there's no player2 move during the game."""
        # Just return the current state since codemaker doesn't make moves during the game
        return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
    
    def prepare_analysis_context(self, state: MastermindState, player: str) -> Dict[str, Any]:
        """Prepare context for analysis."""
        # Format guess history
        guess_history = []
        for i, (guess, feedback) in enumerate(zip(state.guesses, state.feedback)):
            guess_history.append(f"Guess {i+1}: {', '.join(guess.colors)} → {feedback.exact_matches} exact, {feedback.color_matches} color")
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "guess_history": "\n".join(guess_history)
        }
    
    def analyze_player1(self, state: MastermindState) -> Command:
        """Analyze game for codebreaker."""
        return self.analyze_position(state, "codebreaker")
    
    def analyze_player2(self, state: MastermindState) -> Command:
        """In Mastermind, we don't analyze for the codemaker."""
        # Just return the current state since we don't analyze for codemaker
        return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state."""
        # Create a MastermindState from the dict
        game_state = MastermindState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Mastermind - Guesses remaining: {game_state.max_guesses - len(game_state.guesses)}")
        print(f"📌 Game Status: {game_state.game_status}")
        print("=" * 50)
        
        # Print the board
        print("\n" + game_state.board_string)
        
        # Print secret code if game is over
        if game_state.game_status != "ongoing":
            print(f"\n🔑 Secret Code: {', '.join(game_state.secret_code)}")
        
        # Print last guess if available
        if game_state.guesses:
            last_guess = game_state.guesses[-1]
            last_feedback = game_state.feedback[-1]
            print(f"\n📝 Last Guess: {', '.join(last_guess.colors)}")
            print(f"   Feedback: {last_feedback.exact_matches} exact matches, {last_feedback.color_matches} color matches")
        
        # Print analysis if available
        if hasattr(game_state, "codebreaker_analysis") and game_state.codebreaker_analysis:
            last_analysis = game_state.codebreaker_analysis[-1]
            print(f"\n🔍 Analysis:")
            print(f"Confidence: {last_analysis.get('confidence', 'N/A')}%")
            print(f"Strategy: {last_analysis.get('elimination_strategy', 'N/A')}")
            print(f"Reasoning: {last_analysis.get('next_guess_reasoning', 'N/A')}")
            
            # Print a few possible solutions
            possible_solutions = last_analysis.get('possible_solutions', [])
            if possible_solutions:
                print(f"Possible solutions remaining: {len(possible_solutions)}")
                # Show up to 5 possible solutions
                if len(possible_solutions) <= 5:
                    for i, solution in enumerate(possible_solutions[:5]):
                        print(f"  {i+1}. {', '.join(solution)}")
                else:
                    print("  Too many possibilities to display")
        
        # Add a short delay for readability
        time.sleep(0.5)