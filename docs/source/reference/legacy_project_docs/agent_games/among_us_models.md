# Among Us Game Models

This document outlines the core data models for the improved Among Us game implementation.

## Core Models

### Player Model

```python
from enum import Enum
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

class PlayerRole(str, Enum):
    CREWMATE = "crewmate"
    IMPOSTOR = "impostor"

class PlayerColor(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    PURPLE = "purple"
    WHITE = "white"
    BLACK = "black"
    PINK = "pink"
    BROWN = "brown"
    CYAN = "cyan"
    LIME = "lime"

class PlayerStatus(str, Enum):
    ALIVE = "alive"
    DEAD = "dead"
    DISCONNECTED = "disconnected"

class PlayerVisibility(BaseModel):
    visible_players: Set[str] = Field(default_factory=set)
    last_seen_locations: Dict[str, str] = Field(default_factory=dict)
    known_roles: Dict[str, PlayerRole] = Field(default_factory=dict)
    suspicious_players: Dict[str, float] = Field(default_factory=dict)  # Player ID -> suspicion level (0-1)

class PlayerMemory(BaseModel):
    observations: List[Dict] = Field(default_factory=list)  # Timestamped observations
    alibis: Dict[int, str] = Field(default_factory=dict)  # Round -> location
    meeting_notes: List[Dict] = Field(default_factory=list)  # Notes from meetings
    player_history: Dict[str, List[Dict]] = Field(default_factory=dict)  # Player -> history of interactions

class Player(BaseModel):
    id: str
    name: str
    color: PlayerColor
    role: PlayerRole
    status: PlayerStatus = PlayerStatus.ALIVE
    location: str
    previous_location: Optional[str] = None
    tasks: List[str] = Field(default_factory=list)  # Task IDs
    completed_tasks: List[str] = Field(default_factory=list)
    fake_tasks: List[str] = Field(default_factory=list)  # For impostors
    kill_cooldown: int = 0  # Seconds until next kill is available
    emergency_meetings: int = 1  # Number of emergency meetings available
    last_action: Optional[str] = None
    in_vent: bool = False
    current_vent: Optional[str] = None
    visibility: PlayerVisibility = Field(default_factory=PlayerVisibility)
    memory: PlayerMemory = Field(default_factory=PlayerMemory)

    def is_impostor(self) -> bool:
        return self.role == PlayerRole.IMPOSTOR

    def is_alive(self) -> bool:
        return self.status == PlayerStatus.ALIVE

    def can_kill(self) -> bool:
        return self.is_impostor() and self.is_alive() and self.kill_cooldown <= 0 and not self.in_vent

    def can_call_meeting(self) -> bool:
        return self.is_alive() and self.emergency_meetings > 0

    def can_complete_task(self, task_id: str) -> bool:
        return (
            self.is_alive() and
            not self.is_impostor() and
            task_id in self.tasks and
            task_id not in self.completed_tasks
        )
```

### Map and Room Models

```python
from enum import Enum
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

class RoomType(str, Enum):
    STANDARD = "standard"  # Normal room
    COMMON = "common"      # High-traffic areas like Cafeteria
    CRITICAL = "critical"  # Critical systems (O2, Reactor)
    SECURITY = "security"  # Areas with monitoring capabilities

class RoomConnection(BaseModel):
    target_room: str
    distance: int = 1  # Travel time in seconds
    is_blocked: bool = False  # Can be blocked by sabotage

class VentConnection(BaseModel):
    target_vent: str
    travel_time: int = 2  # Time to travel between vents

class SecurityCamera(BaseModel):
    id: str
    visible_rooms: List[str]
    is_functional: bool = True

class Vent(BaseModel):
    id: str
    location: str  # Room ID
    connections: List[VentConnection] = Field(default_factory=list)

class Room(BaseModel):
    id: str
    name: str
    type: RoomType
    connections: List[RoomConnection] = Field(default_factory=list)
    tasks: List[str] = Field(default_factory=list)  # Task IDs available in this room
    vents: List[str] = Field(default_factory=list)  # Vent IDs in this room
    cameras: List[str] = Field(default_factory=list)  # Camera IDs in this room
    door_locked: bool = False
    lights_on: bool = True

    def is_connected_to(self, room_id: str) -> bool:
        return any(conn.target_room == room_id for conn in self.connections)

    def get_connection(self, room_id: str) -> Optional[RoomConnection]:
        for conn in self.connections:
            if conn.target_room == room_id:
                return conn
        return None

class GameMap(BaseModel):
    id: str
    name: str
    rooms: Dict[str, Room] = Field(default_factory=dict)
    vents: Dict[str, Vent] = Field(default_factory=dict)
    cameras: Dict[str, SecurityCamera] = Field(default_factory=dict)

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)

    def get_connected_rooms(self, room_id: str) -> List[str]:
        room = self.get_room(room_id)
        if not room:
            return []
        return [conn.target_room for conn in room.connections if not conn.is_blocked]

    def get_vent(self, vent_id: str) -> Optional[Vent]:
        return self.vents.get(vent_id)

    def get_vents_in_room(self, room_id: str) -> List[Vent]:
        return [vent for vent_id, vent in self.vents.items() if vent.location == room_id]

    def get_connected_vents(self, vent_id: str) -> List[str]:
        vent = self.get_vent(vent_id)
        if not vent:
            return []
        return [conn.target_vent for conn in vent.connections]
```

### Task Models

```python
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class TaskType(str, Enum):
    VISUAL = "visual"      # Tasks that show visual confirmation to other players
    COMMON = "common"      # Tasks assigned to all crewmates
    SHORT = "short"        # Quick tasks
    LONG = "long"          # Time-consuming tasks
    CRITICAL = "critical"  # Tasks related to critical systems

class TaskDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskStep(BaseModel):
    id: str
    description: str
    completed: bool = False
    time_required: int = 0  # Time in seconds to complete this step

class Task(BaseModel):
    id: str
    name: str
    description: str
    type: TaskType
    difficulty: TaskDifficulty
    location: str  # Room ID
    status: TaskStatus = TaskStatus.NOT_STARTED
    steps: List[TaskStep] = Field(default_factory=list)
    visual_indicator: bool = False  # Whether this task shows visual confirmation
    completion_time: int = 0  # Time in seconds to complete the task
    prerequisite_tasks: List[str] = Field(default_factory=list)  # Task IDs that must be completed first

    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    def is_visual(self) -> bool:
        return self.type == TaskType.VISUAL or self.visual_indicator

    def get_progress(self) -> float:
        """Returns the completion percentage (0.0 - 1.0)"""
        if not self.steps:
            return 1.0 if self.is_completed() else 0.0

        completed_steps = sum(1 for step in self.steps if step.completed)
        return completed_steps / len(self.steps)

    def get_next_step(self) -> Optional[TaskStep]:
        """Returns the next uncompleted step"""
        for step in self.steps:
            if not step.completed:
                return step
        return None
```

### Sabotage Models

```python
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class SabotageType(str, Enum):
    LIGHTS = "lights"           # Reduces visibility
    COMMUNICATIONS = "comms"    # Disables task list
    OXYGEN = "o2"               # Time-critical, requires two-point fix
    REACTOR = "reactor"         # Time-critical, requires two-point fix
    DOORS = "doors"             # Locks doors to a room

class SabotageStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    FAILED = "failed"   # Timer ran out on critical sabotages

class SabotageResolutionPoint(BaseModel):
    id: str
    location: str  # Room ID
    description: str
    resolved: bool = False
    resolver_id: Optional[str] = None  # Player ID who resolved this point

class Sabotage(BaseModel):
    id: str
    type: SabotageType
    status: SabotageStatus = SabotageStatus.ACTIVE
    initiator_id: Optional[str] = None  # Player ID who initiated the sabotage
    start_time: float  # System time when sabotage started
    duration: int  # Duration in seconds before critical sabotages cause game over
    resolution_points: List[SabotageResolutionPoint] = Field(default_factory=list)
    affected_rooms: List[str] = Field(default_factory=list)  # Room IDs affected by this sabotage

    def is_critical(self) -> bool:
        return self.type in [SabotageType.OXYGEN, SabotageType.REACTOR]

    def is_resolved(self) -> bool:
        return self.status == SabotageStatus.RESOLVED

    def is_failed(self) -> bool:
        return self.status == SabotageStatus.FAILED

    def time_remaining(self, current_time: float) -> float:
        """Returns time remaining in seconds before critical sabotage causes game over"""
        if not self.is_critical() or self.is_resolved() or self.is_failed():
            return 0

        elapsed = current_time - self.start_time
        remaining = max(0, self.duration - elapsed)
        return remaining

    def get_resolution_progress(self) -> float:
        """Returns the resolution progress (0.0 - 1.0)"""
        if not self.resolution_points:
            return 1.0 if self.is_resolved() else 0.0

        resolved_points = sum(1 for point in self.resolution_points if point.resolved)
        return resolved_points / len(self.resolution_points)
```

### Meeting and Voting Models

```python
from enum import Enum
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

class MeetingType(str, Enum):
    EMERGENCY = "emergency"  # Called by a player
    BODY_REPORT = "body_report"  # Reporting a dead body

class MeetingPhase(str, Enum):
    DISCUSSION = "discussion"  # Initial discussion phase
    VOTING = "voting"  # Voting phase
    RESULTS = "results"  # Showing results

class MeetingStatus(str, Enum):
    ACTIVE = "active"
    ENDED = "ended"

class VoteOption(str, Enum):
    SKIP = "skip"  # Skip voting

class DiscussionMessage(BaseModel):
    player_id: str
    content: str
    timestamp: float

class Vote(BaseModel):
    voter_id: str
    vote_for: str  # Player ID or "skip"
    timestamp: float

class Meeting(BaseModel):
    id: str
    type: MeetingType
    phase: MeetingPhase = MeetingPhase.DISCUSSION
    status: MeetingStatus = MeetingStatus.ACTIVE
    caller_id: str  # Player who called the meeting
    reported_body_id: Optional[str] = None  # Player ID of reported body
    report_location: Optional[str] = None  # Room ID where body was reported
    start_time: float
    discussion_duration: int  # Duration of discussion phase in seconds
    voting_duration: int  # Duration of voting phase in seconds
    discussion_messages: List[DiscussionMessage] = Field(default_factory=list)
    votes: Dict[str, Vote] = Field(default_factory=dict)  # Player ID -> Vote
    ejected_player_id: Optional[str] = None  # Result of the vote

    def is_active(self) -> bool:
        return self.status == MeetingStatus.ACTIVE

    def get_phase_time_remaining(self, current_time: float) -> float:
        """Returns time remaining in the current phase"""
        elapsed = current_time - self.start_time

        if self.phase == MeetingPhase.DISCUSSION:
            return max(0, self.discussion_duration - elapsed)
        elif self.phase == MeetingPhase.VOTING:
            phase_start = self.start_time + self.discussion_duration
            phase_elapsed = current_time - phase_start
            return max(0, self.voting_duration - phase_elapsed)

        return 0

    def get_vote_counts(self) -> Dict[str, int]:
        """Returns a count of votes for each player"""
        counts = {}
        for vote in self.votes.values():
            counts[vote.vote_for] = counts.get(vote.vote_for, 0) + 1
        return counts

    def has_player_voted(self, player_id: str) -> bool:
        return player_id in self.votes

    def get_players_who_voted(self) -> Set[str]:
        return set(self.votes.keys())
```

## Game State Models

### Game State

```python
from enum import Enum
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

class GamePhase(str, Enum):
    LOBBY = "lobby"  # Game setup phase
    TASKS = "tasks"  # Normal gameplay
    MEETING = "meeting"  # Meeting in progress
    GAME_OVER = "game_over"  # Game has ended

class GameStatus(str, Enum):
    WAITING = "waiting"  # Waiting for players
    ONGOING = "ongoing"  # Game in progress
    ENDED = "ended"  # Game has ended

class WinReason(str, Enum):
    TASKS_COMPLETED = "tasks_completed"  # Crewmates completed all tasks
    IMPOSTORS_ELIMINATED = "impostors_eliminated"  # All impostors were eliminated
    CREWMATES_ELIMINATED = "crewmates_eliminated"  # Impostors eliminated/outnumbered crewmates
    CRITICAL_SABOTAGE = "critical_sabotage"  # Critical sabotage timer ran out

class GameSettings(BaseModel):
    map_id: str
    num_impostors: int
    emergency_cooldown: int = 15  # Seconds between emergency meetings
    kill_cooldown: int = 45  # Seconds between impostor kills
    player_speed: float = 1.0  # Movement speed multiplier
    task_bar_updates: str = "always"  # "always", "meetings", "never"
    visual_tasks: bool = True  # Whether visual tasks are enabled
    anonymous_voting: bool = False  # Whether votes are anonymous
    confirm_ejects: bool = True  # Whether ejected player's role is revealed
    emergency_meetings: int = 1  # Number of emergency meetings per player
    common_tasks: int = 1  # Number of common tasks
    short_tasks: int = 2  # Number of short tasks
    long_tasks: int = 1  # Number of long tasks

class GameState(BaseModel):
    id: str
    phase: GamePhase = GamePhase.LOBBY
    status: GameStatus = GameStatus.WAITING
    settings: GameSettings
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    round_number: int = 0
    players: Dict[str, Player] = Field(default_factory=dict)
    game_map: GameMap
    tasks: Dict[str, Task] = Field(default_factory=dict)
    sabotages: List[Sabotage] = Field(default_factory=list)
    active_sabotage: Optional[str] = None  # ID of active sabotage if any
    meetings: List[Meeting] = Field(default_factory=list)
    current_meeting: Optional[str] = None  # ID of current meeting if any
    eliminated_players: List[str] = Field(default_factory=list)
    winner: Optional[str] = None  # "crewmates" or "impostors"
    win_reason: Optional[WinReason] = None

    def get_active_sabotage(self) -> Optional[Sabotage]:
        if not self.active_sabotage:
            return None
        for sabotage in self.sabotages:
            if sabotage.id == self.active_sabotage:
                return sabotage
        return None

    def get_current_meeting(self) -> Optional[Meeting]:
        if not self.current_meeting:
            return None
        for meeting in self.meetings:
            if meeting.id == self.current_meeting:
                return meeting
        return None

    def get_alive_players(self) -> Dict[str, Player]:
        return {pid: player for pid, player in self.players.items() if player.is_alive()}

    def get_alive_crewmates(self) -> Dict[str, Player]:
        return {
            pid: player
            for pid, player in self.players.items()
            if player.is_alive() and not player.is_impostor()
        }

    def get_alive_impostors(self) -> Dict[str, Player]:
        return {
            pid: player
            for pid, player in self.players.items()
            if player.is_alive() and player.is_impostor()
        }

    def get_task_completion_percentage(self) -> float:
        """Returns overall task completion percentage"""
        # Only count tasks assigned to crewmates
        crewmate_task_ids = set()
        for player in self.players.values():
            if not player.is_impostor():
                crewmate_task_ids.update(player.tasks)

        if not crewmate_task_ids:
            return 100.0

        completed_tasks = sum(
            1 for task_id in crewmate_task_ids
            if task_id in self.tasks and self.tasks[task_id].is_completed()
        )

        return (completed_tasks / len(crewmate_task_ids)) * 100

    def check_win_condition(self) -> Optional[str]:
        """Check if either side has won"""
        # Tasks completed
        if self.get_task_completion_percentage() >= 100:
            return "crewmates"

        # Count alive players by role
        alive_impostors = len(self.get_alive_impostors())
        alive_crewmates = len(self.get_alive_crewmates())

        # No impostors left
        if alive_impostors == 0:
            return "crewmates"

        # Impostors equal or outnumber crewmates
        if alive_impostors >= alive_crewmates:
            return "impostors"

        # Critical sabotage timer ran out
        active_sabotage = self.get_active_sabotage()
        if active_sabotage and active_sabotage.is_critical() and active_sabotage.is_failed():
            return "impostors"

        # Game still ongoing
        return None
```

## Player Action Models

```python
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field

class ActionType(str, Enum):
    MOVE = "move"
    COMPLETE_TASK = "complete_task"
    KILL = "kill"
    REPORT_BODY = "report_body"
    CALL_MEETING = "call_meeting"
    SABOTAGE = "sabotage"
    VENT = "vent"
    EXIT_VENT = "exit_vent"
    USE_CAMERA = "use_camera"
    DISCUSS = "discuss"
    VOTE = "vote"
    RESOLVE_SABOTAGE = "resolve_sabotage"

class MoveAction(BaseModel):
    target_room: str

class CompleteTaskAction(BaseModel):
    task_id: str
    step_id: Optional[str] = None  # For multi-step tasks

class KillAction(BaseModel):
    target_id: str

class ReportBodyAction(BaseModel):
    body_id: Optional[str] = None  # If None, reports any body in the room

class CallMeetingAction(BaseModel):
    pass  # No additional data needed

class SabotageAction(BaseModel):
    sabotage_type: SabotageType
    target_rooms: List[str] = Field(default_factory=list)  # For door sabotages

class VentAction(BaseModel):
    vent_id: str

class ExitVentAction(BaseModel):
    pass  # No additional data needed

class UseCameraAction(BaseModel):
    camera_id: str

class DiscussAction(BaseModel):
    message: str

class VoteAction(BaseModel):
    vote_for: str  # Player ID or "skip"

class ResolveSabotageAction(BaseModel):
    sabotage_id: str
    resolution_point_id: str

class PlayerAction(BaseModel):
    player_id: str
    action_type: ActionType
    timestamp: float
    action_data: Optional[Dict] = None  # Action-specific data

    def get_move_data(self) -> Optional[MoveAction]:
        if self.action_type != ActionType.MOVE or not self.action_data:
            return None
        return MoveAction(**self.action_data)

    def get_complete_task_data(self) -> Optional[CompleteTaskAction]:
        if self.action_type != ActionType.COMPLETE_TASK or not self.action_data:
            return None
        return CompleteTaskAction(**self.action_data)

    # Similar methods for other action types...
```

## Filtered State for Players

```python
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

class FilteredPlayer(BaseModel):
    id: str
    name: str
    color: PlayerColor
    status: PlayerStatus
    location: Optional[str] = None  # Only visible if in same room

class VisibleTask(BaseModel):
    id: str
    name: str
    description: str
    location: str
    status: TaskStatus
    progress: float

class FilteredRoom(BaseModel):
    id: str
    name: str
    players: List[str] = Field(default_factory=list)  # IDs of visible players
    has_vent: bool = False
    is_door_locked: bool = False
    has_body: bool = False
    body_ids: List[str] = Field(default_factory=list)  # IDs of visible bodies

class FilteredSabotage(BaseModel):
    type: SabotageType
    time_remaining: float  # For critical sabotages
    resolution_points: List[Dict] = Field(default_factory=list)

class FilteredMeeting(BaseModel):
    type: MeetingType
    phase: MeetingPhase
    caller_id: str
    reported_body_id: Optional[str] = None
    report_location: Optional[str] = None
    discussion_messages: List[Dict] = Field(default_factory=list)
    votes: Dict[str, str] = Field(default_factory=dict)  # Only if not anonymous
    voted_players: Set[str] = Field(default_factory=set)  # Who has voted
    ejected_player_id: Optional[str] = None
    ejected_player_role: Optional[PlayerRole] = None  # Only if confirm_ejects is true

class PlayerFilteredState(BaseModel):
    player_id: str
    role: PlayerRole
    location: str
    in_vent: bool
    current_vent: Optional[str]
    tasks: List[VisibleTask] = Field(default_factory=list)
    task_completion: float  # Overall task completion percentage
    emergency_meetings_remaining: int
    kill_cooldown: int  # Only for impostors
    game_phase: GamePhase
    current_room: FilteredRoom
    visible_rooms: Dict[str, FilteredRoom] = Field(default_factory=dict)
    visible_players: Dict[str, FilteredPlayer] = Field(default_factory=dict)
    active_sabotage: Optional[FilteredSabotage] = None
    current_meeting: Optional[FilteredMeeting] = None
    fellow_impostors: List[str] = Field(default_factory=list)  # Only for impostors
    observations: List[str] = Field(default_factory=list)  # Recent observations
    round_number: int
```

This design provides a comprehensive and flexible model structure for the Among Us game. The models are designed to support all the enhanced game mechanics while maintaining clean separation of concerns.

## State Management

For state management, we'll adopt a more event-driven approach:

```python
class StateManager:
    """Manages game state transitions and enforces game rules."""

    def __init__(self, initial_state: GameState):
        self.state = initial_state
        self.event_handlers = {
            # Register event handlers for different game events
            "player_move": self._handle_player_move,
            "player_complete_task": self._handle_player_complete_task,
            "player_kill": self._handle_player_kill,
            # ... other event handlers ...
        }

    def apply_action(self, action: PlayerAction) -> GameState:
        """Apply a player action to the game state."""
        # Validate the action
        if not self._is_action_valid(action):
            return self.state

        # Apply the action based on its type
        handler = self._get_action_handler(action.action_type)
        if handler:
            new_state = handler(self.state, action)

            # Check for state transitions
            new_state = self._check_state_transitions(new_state)

            # Check win conditions
            new_state = self._check_win_conditions(new_state)

            self.state = new_state

        return self.state

    def _is_action_valid(self, action: PlayerAction) -> bool:
        """Check if an action is valid in the current game state."""
        # Implementation details...

    def _get_action_handler(self, action_type: ActionType):
        """Get the appropriate handler for an action type."""
        # Implementation details...

    def _handle_player_move(self, state: GameState, action: PlayerAction) -> GameState:
        """Handle a player movement action."""
        # Implementation details...

    # Other action handlers...

    def _check_state_transitions(self, state: GameState) -> GameState:
        """Check for state transitions (e.g., meeting phase to voting phase)."""
        # Implementation details...

    def _check_win_conditions(self, state: GameState) -> GameState:
        """Check if either side has won."""
        # Implementation details...

    def filter_state_for_player(self, player_id: str) -> PlayerFilteredState:
        """Create a filtered state view for a specific player."""
        # Implementation details...
```

The state manager provides a clean interface for applying actions to the game state while enforcing game rules and managing state transitions.
