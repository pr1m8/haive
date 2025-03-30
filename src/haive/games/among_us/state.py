# Updated AmongUsState model

from typing import Dict, List, Optional, Literal, Any
from pydantic import BaseModel, Field
from src.haive.games.framework.multi_player.state import MultiPlayerGameState
from src.haive.games.among_us.models import PlayerState, SabotageEvent, AmongUsGamePhase, Task, TaskStatus, PlayerRole

class AmongUsState(MultiPlayerGameState):
    map_locations: List[str] = Field(default_factory=list)
    player_states: Dict[str, PlayerState] = Field(default_factory=dict)
    tasks: Dict[str, Task] = Field(default_factory=dict)
    sabotages: List[SabotageEvent] = Field(default_factory=list)
    eliminated_players: List[str] = Field(default_factory=list)
    meeting_active: bool = Field(default=False)
    meeting_caller: Optional[str] = Field(default=None)
    reported_body: Optional[str] = Field(default=None)
    votes: Dict[str, str] = Field(default_factory=dict)
    game_phase: AmongUsGamePhase = Field(default=AmongUsGamePhase.TASKS)
    impostor_count: int = Field(default=0)
    crewmate_count: int = Field(default=0)
    discussion_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    def get_alive_players(self) -> List[str]:
        """Get list of alive player IDs."""
        return [pid for pid, pstate in self.player_states.items() 
                if pstate.is_alive]
    
    def get_task_completion_percentage(self) -> float:
        """Calculate task completion percentage."""
        total = len(self.tasks)
        if total == 0:
            return 100.0
        
        completed = sum(1 for task in self.tasks.values() 
                       if task.status == TaskStatus.COMPLETED)
        return (completed / total) * 100
        
    def check_win_condition(self) -> Optional[Literal["crewmates", "impostors"]]:
        """Check if either side has won."""
        if self.get_task_completion_percentage() >= 100:
            return "crewmates"
        
        alive_impostors = sum(1 for pid, pstate in self.player_states.items()
                             if pstate.is_alive and pstate.role == PlayerRole.IMPOSTOR)
        alive_crewmates = sum(1 for pid, pstate in self.player_states.items()
                             if pstate.is_alive and pstate.role == PlayerRole.CREWMATE)
        
        if alive_impostors == 0:
            return "crewmates"
        if alive_impostors >= alive_crewmates:
            return "impostors"
        
        return None