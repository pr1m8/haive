# among_us_models.py
from enum import Enum
from typing import List, Dict, Optional, Literal, Tuple
from pydantic import BaseModel

class PlayerRole(str, Enum):
    CREWMATE = "crewmate"
    IMPOSTOR = "impostor"

class TaskType(str, Enum):
    VISUAL = "visual"
    COMMON = "common"
    SHORT = "short"
    LONG = "long"

class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(BaseModel):
    id: str
    type: TaskType
    location: str
    description: str
    status: TaskStatus = TaskStatus.NOT_STARTED

class PlayerState(BaseModel):
    id: str
    role: PlayerRole
    location: str
    tasks: List[Task]
    is_alive: bool = True
    last_action: Optional[str] = None
    observations: List[str] = []

class SabotageEvent(BaseModel):
    type: str
    location: str
    timer: int
    resolved: bool = False

class AmongUsGamePhase(str, Enum):
    TASKS = "tasks"
    MEETING = "meeting"
    VOTING = "voting"
    GAME_OVER = "game_over"