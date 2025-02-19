from src.haive.core.aug_llm.base import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.agents.agent_games.chess.models import ChessPlayerDecision, ChessAnalysis,SegmentedAnalysis
white_prompt = ChatPromptTemplate.from_messages([
    ('system', "You are the white chess player. Focus on aggressive opening play..."),
    ('human', "Current position: {board_fen}\nMove history: {move_history}\nMake your move.")
])

black_prompt = ChatPromptTemplate.from_messages([
    ('system', "You are the black chess player. Focus on solid defensive play..."),
    ('human', "Current position: {board_fen}\nMove history: {move_history}\nMake your move.")
])
white_analyzer_prompt = ChatPromptTemplate.from_messages([
    ('system', "You are analyzing from White's perspective. Focus on attacking chances..."),
    ('human', "Position: {board_fen}\nMove history: {move_history}\nAnalyze White's position.")
])

black_analyzer_prompt = ChatPromptTemplate.from_messages([
    ('system', "You are analyzing from Black's perspective. Focus on defensive resources..."),
    ('human', "Position: {board_fen}\nMove history: {move_history}\nAnalyze Black's position.")
])

aug_llm_configs = {
    "white_player": AugLLMConfig(
        name="white_player",
        prompt_template=white_prompt,
        structured_output_model=ChessPlayerDecision
    ),
    "black_player": AugLLMConfig(
        name="black_player",
        prompt_template=black_prompt,
        structured_output_model=ChessPlayerDecision
    ),
    "white_analyzer": AugLLMConfig(
        name="white_analyzer",
        prompt_template=white_analyzer_prompt,
        structured_output_model=SegmentedAnalysis
    ),
    "black_analyzer": AugLLMConfig(
        name="black_analyzer",
        prompt_template=black_analyzer_prompt,
        structured_output_model=SegmentedAnalysis
    )
}
