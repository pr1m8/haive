# among_us_config.py
from pydantic import Field
from typing import Dict
from src.haive.games.framework.multi_player.config import MultiPlayerGameConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.games.among_us.state import AmongUsState

class AmongUsAgentConfig(MultiPlayerGameConfig):
    state_schema: type = Field(default=AmongUsState)
    engines: Dict[str, Dict[str, AugLLMConfig]] = Field(...)
    map_name: str = Field(default="skeld")
    num_impostors: int = Field(default=1)
    emergency_meetings_per_player: int = Field(default=1)
    discussion_time: int = Field(default=45)  # seconds
    voting_time: int = Field(default=30)  # seconds
    player_movement_speed: float = Field(default=1.0)
    kill_cooldown: int = Field(default=45)  # seconds
    task_bar_updates: str = Field(default="always")  # "always", "meetings", "never"