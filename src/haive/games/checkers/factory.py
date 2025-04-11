from src.haive.games.checkers.state import CheckersState

print(CheckersState.initialize().model_dump())

from src.haive.games.checkers.agent import CheckersAgent, CheckersAgentConfig

a = CheckersAgent(CheckersAgentConfig())
a.run()