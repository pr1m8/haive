from typing import Dict, List, Any, Optional, Union, Callable, Type
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command, Send

from src.haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.graph.GraphBuilder import DynamicGraph
from src.haive.core.graph.NodeFactory import create_node_function
from src.haive.games.framework.base.agent import GameAgent
from src.haive.games.framework.base.config import GameConfig

from src.haive.games.debate.state import DebateState, DebateParticipant, DebateMove, VoteResult
from src.haive.games.debate.state_manager import DebateStateManager
from src.haive.games.debate.config import DebateConfig

@register_agent(DebateConfig)
class DebateAgent(GameAgent[DebateConfig]):
    """Agent for multi-agent debates and conversations.
    
    This agent handles multi-party debates with different roles,
    automatic turn determination, and voting mechanisms.
    """
    
    def __init__(self, config: DebateConfig):
        """Initialize the debate agent.
        
        Args:
            config: Configuration for the debate
        """
        super().__init__(config)
        
        # Set state manager
        self.state_manager = DebateStateManager
        
        # Initialize engines
        self.participant_generator = config.participant_generator_llm.create_runnable()
        
        # Initialize engine registry
        self.engines = {}
        
        # Add default engines
        self.engines["debater"] = config.debater_llm.create_runnable()
        self.engines["judge"] = config.judge_llm.create_runnable()
        
        # Add specific participant engines
        for participant_id, llm_config in config.participant_llms.items():
            self.engines[participant_id] = llm_config.create_runnable()
    
    def setup_workflow(self):
        """Set up the debate workflow using DynamicGraph and NodeFactory."""
        # Create a dynamic graph builder
        graph_builder = DynamicGraph(
            components=[self.config.debater_llm, self.config.judge_llm],
            state_schema=self.config.state_schema
        )
        
        # Add core nodes for debate flow
        graph_builder.add_node("initialize_debate", self.initialize_debate)
        graph_builder.add_node("generate_participants", self.generate_participants)
        
        # Add moderator node to handle turns
        graph_builder.add_node("moderator", self.moderator_node)
        
        # Add participant action nodes
        graph_builder.add_node("debater_action", self.debater_action)
        graph_builder.add_node("judge_action", self.judge_action)
        
        # Add results node
        graph_builder.add_node("calculate_results", self.calculate_results)
        
        # Set up the flow
        # 1. Initialize debate and generate participants
        graph_builder.add_edge(START, "initialize_debate")
        graph_builder.add_edge("initialize_debate", "generate_participants")
        graph_builder.add_edge("generate_participants", "moderator")
        
        # 2. Moderator routes to appropriate action, which returns to moderator
        graph_builder.add_conditional_edges(
            "moderator",
            self.determine_next_action,
            {
                "debater_action": "debater_action",
                "judge_action": "judge_action",
                "calculate_results": "calculate_results",
                "finished": END
            }
        )
        
        graph_builder.add_edge("debater_action", "moderator")
        graph_builder.add_edge("judge_action", "moderator")
        
        # 3. Results calculation leads to end
        graph_builder.add_edge("calculate_results", END)
        
        # Build the graph
        self.graph = graph_builder.build()
    
    # Node functions
    def initialize_debate(self, state: Dict[str, Any]) -> Command:
        """Initialize the debate with basic settings.
        
        Args:
            state: Input state
            
        Returns:
            Command with initialized debate state
        """
        # Create dictionary representation
        state_dict = state if isinstance(state, dict) else state.dict() if hasattr(state, "dict") else state.model_dump()
        
        # Initialize a fresh debate state
        debate_state = self.state_manager.initialize(
            topic=state_dict.get("topic", self.config.topic),
            description=state_dict.get("description", self.config.description),
            max_rounds=state_dict.get("max_rounds", self.config.max_rounds),
            phase_sequence=self.config.phases
        )
        
        # Add initial message
        messages = [
            SystemMessage(content=f"Debate on the topic: {debate_state.topic}"),
            HumanMessage(content=f"Welcome to the debate on: {debate_state.topic}\n\n{debate_state.description}")
        ]
        
        # Update the state
        debate_dict = debate_state.model_dump() if hasattr(debate_state, "model_dump") else debate_state.dict()
        debate_dict["messages"] = messages
        
        # Print debug info
        print(f"Initialized debate on: {debate_state.topic}")
        print(f"Phase sequence: {debate_state.phase_sequence}")
        
        return Command(update=debate_dict)
    
    def generate_participants(self, state: Dict[str, Any]) -> Command:
        """Generate debate participants using the participant generator.
        
        Args:
            state: Current state
            
        Returns:
            Command with generated participants
        """
        # Create a copy of the state dict
        state_dict = state.copy() if isinstance(state, dict) else state.dict() if hasattr(state, "dict") else state.model_dump()
        
        # Only generate if we don't already have participants
        if state_dict.get("participants"):
            return Command(update=state_dict)
        
        # Use the participant generator
        try:
            # Create dummy participants for testing
            print("Generating participants...")
            participants = []
            
            # Add debaters
            for i in range(self.config.num_debaters):
                role = "debater"
                name = f"Debater {i+1}"
                position = "Prosecution" if i == 0 else "Defense" if i == 1 else f"Position {i+1}"
                participant = DebateParticipant(
                    id=f"debater_{i+1}",
                    name=name,
                    role=role,
                    position=position,
                    personality=f"Focused on {position}",
                    system_prompt=f"You are {name}, representing the {position}."
                )
                participants.append(participant)
            
            # Add judges
            for i in range(self.config.num_judges):
                role = "judge"
                name = f"Judge {i+1}"
                participant = DebateParticipant(
                    id=f"judge_{i+1}",
                    name=name,
                    role=role,
                    personality=f"Fair and impartial judge {i+1}",
                    system_prompt=f"You are {name}, a fair and impartial judge."
                )
                participants.append(participant)
            
            # Update state
            print(f"Generated {len(participants)} participants")
            state_dict["participants"] = participants
            state_dict["judge_participants"] = [p.id for p in participants if p.role == "judge"]
            state_dict["current_phase"] = "opening_statements"
            state_dict["game_status"] = "ongoing"
            
            # Set initial turn to first debater
            for participant in participants:
                if participant.role == "debater":
                    state_dict["turn"] = participant.id
                    break
            
            # Add message announcing participants
            messages = state_dict.get("messages", [])
            
            participant_announcement = "# Debate Participants\n\n"
            
            for participant in participants:
                if participant.role == "debater":
                    participant_announcement += f"## {participant.name} (Debater)\n"
                    if participant.position:
                        participant_announcement += f"Position: {participant.position}\n\n"
                else:
                    participant_announcement += f"## {participant.name} (Judge)\n"
                    if participant.personality:
                        participant_announcement += f"{participant.personality}\n\n"
            
            messages.append(AIMessage(content=participant_announcement))
            messages.append(HumanMessage(content=f"The debate will begin with opening statements. {participants[0].name} will go first."))
            
            state_dict["messages"] = messages
            
            print("Participants generated successfully!")
            print(f"Transitioning to phase: {state_dict['current_phase']}")
            print(f"Current turn: {state_dict['turn']}")
            
            return Command(update=state_dict)
            
        except Exception as e:
            print(f"Error generating participants: {str(e)}")
            return Command(update=state_dict)
    
    def moderator_node(self, state: Dict[str, Any]) -> Command:
        """Moderator node to guide the debate flow.
        
        Args:
            state: Current state
            
        Returns:
            Command with moderator actions
        """
        print("MODERATOR NODE CALLED")
        # Create a copy of the state dict
        state_dict = state.copy() if isinstance(state, dict) else state.dict() if hasattr(state, "dict") else state.model_dump()
        
        # Get current phase and participant
        current_phase = state_dict.get("current_phase", "setup")
        participants = state_dict.get("participants", [])
        turn = state_dict.get("turn", "")
        
        # Find current participant
        current_participant = None
        for p in participants:
            if p.get("id", "") == turn:
                current_participant = p
                break
                
        if not current_participant:
            print("No current participant found")
            return Command(update=state_dict)
        
        # Create moderator message
        moderator_message = ""
        
        print(f"Moderating: Phase={current_phase}, Participant={current_participant.get('name', 'Unknown')}")
        
        if current_phase == "opening_statements":
            move_history = state_dict.get("move_history", [])
            if move_history and move_history[-1].get("move_type") == "opening_statement":
                # Transition to next opening statement
                moderator_message = f"Next, {current_participant.get('name')} will present their opening statement."
            else:
                # First opening statement
                moderator_message = f"We'll begin with opening statements. {current_participant.get('name')} will present their opening statement first."
        
        elif current_phase == "arguments":
            moderator_message = f"Round {state_dict.get('current_round', 0)}: {current_participant.get('name')} will now present their argument."
        
        elif current_phase == "closing_statements":
            moderator_message = f"{current_participant.get('name')} will now present their closing statement."
        
        elif current_phase == "voting":
            moderator_message = f"Judge {current_participant.get('name')} will now cast their vote."
        
        elif current_phase == "results":
            moderator_message = "All judges have voted. Let's tally the results."
        
        # Only add message if we have content
        if moderator_message:
            messages = state_dict.get("messages", [])
            messages.append(HumanMessage(content=moderator_message))
            state_dict["messages"] = messages
            print(f"Added moderator message: {moderator_message}")
        else:
            print("No moderator message to add")
        
        return Command(update=state_dict)
    
    def determine_next_action(self, state: Dict[str, Any]) -> str:
        """Determine the next action based on current state.
        
        Args:
            state: Current state
            
        Returns:
            Next action to route to
        """
        print("DETERMINING NEXT ACTION")
        # Create a copy of the state dict
        state_dict = state.copy() if isinstance(state, dict) else state.dict() if hasattr(state, "dict") else state.model_dump()
        
        # Check current phase
        current_phase = state_dict.get("current_phase", "setup")
        
        print(f"Current phase: {current_phase}")
        
        if current_phase == "completed":
            print("Phase is completed, finishing")
            return "finished"
        
        if current_phase == "results":
            print("Phase is results, calculating results")
            return "calculate_results"
        
        # Get current participant
        turn = state_dict.get("turn", "")
        participants = state_dict.get("participants", [])
        
        current_participant = None
        for p in participants:
            if p.get("id", "") == turn:
                current_participant = p
                break
        
        if not current_participant:
            print("No current participant found, finishing")
            return "finished"
        
        # Route based on participant role
        participant_role = current_participant.get("role", "")
        print(f"Current participant role: {participant_role}")
        
        if participant_role == "debater":
            print("Routing to debater_action")
            return "debater_action"
        elif participant_role == "judge":
            print("Routing to judge_action")
            return "judge_action"
        
        print("No valid action found, finishing")
        return "finished"
    
    def debater_action(self, state: Dict[str, Any]) -> Command:
        """Generate a debater's action (opening, argument, closing).
        
        Args:
            state: Current state
            
        Returns:
            Command with debater's move
        """
        print("DEBATER ACTION CALLED")
        # Create a copy of the state dict
        state_dict = state.copy() if isinstance(state, dict) else state.dict() if hasattr(state, "dict") else state.model_dump()
        
        # Get current debater
        debater_id = state_dict.get("turn", "")
        participants = state_dict.get("participants", [])
        
        debater = None
        for p in participants:
            if p.get("id", "") == debater_id:
                debater = p
                break
        
        if not debater:
            print("No current debater found")
            return Command(update=state_dict)
        
        try:
            # Get the right engine
            engine = self.engines.get(debater_id, self.engines.get("debater"))
            
            # Determine move type based on phase
            move_type = "argument"
            current_phase = state_dict.get("current_phase", "arguments")
            
            if current_phase == "opening_statements":
                move_type = "opening_statement"
            elif current_phase == "closing_statements":
                move_type = "closing_statement"
            
            # Create a fake debate content for testing
            print(f"Creating {move_type} for {debater.get('name')}")
            content = f"{debater.get('name')} presents their {move_type}. "
            
            if move_type == "opening_statement":
                content += f"As representative for the {debater.get('position')}, I will demonstrate why our position is correct."
            elif move_type == "argument":
                content += f"The evidence clearly shows that our position ({debater.get('position')}) is supported by facts."
            elif move_type == "closing_statement":
                content += f"In conclusion, the {debater.get('position')} position is the only reasonable conclusion."
            
            # Create debate move
            move = {
                "participant_id": debater_id,
                "content": content,
                "move_type": move_type,
                "round_number": state_dict.get("current_round", 0) if move_type == "argument" else None
            }
            
            # Apply move to state
            move_history = state_dict.get("move_history", [])
            move_history.append(move)
            state_dict["move_history"] = move_history
            
            # Advance to next turn/phase if needed
            state_dict = self._advance_turn(state_dict)
            
            # Add to messages
            messages = state_dict.get("messages", [])
            messages.append(AIMessage(content=f"{debater.get('name')}: {content}"))
            state_dict["messages"] = messages
            
            print(f"Added {move_type} for {debater.get('name')}")
            print(f"New turn: {state_dict.get('turn')}")
            print(f"New phase: {state_dict.get('current_phase')}")
            
            return Command(update=state_dict)
            
        except Exception as e:
            print(f"Error in debater action: {str(e)}")
            return Command(update=state_dict)
    
    def judge_action(self, state: Dict[str, Any]) -> Command:
        """Generate a judge's vote.
        
        Args:
            state: Current state
            
        Returns:
            Command with judge's vote
        """
        print("JUDGE ACTION CALLED")
        # Create a copy of the state dict
        state_dict = state.copy() if isinstance(state, dict) else state.dict() if hasattr(state, "dict") else state.model_dump()
        
        # Get current judge
        judge_id = state_dict.get("turn", "")
        participants = state_dict.get("participants", [])
        
        judge = None
        for p in participants:
            if p.get("id", "") == judge_id:
                judge = p
                break
        
        if not judge:
            print("No current judge found")
            return Command(update=state_dict)
        
        try:
            # Create a fake vote for testing
            debaters = [p for p in participants if p.get("role") == "debater"]
            if not debaters:
                print("No debaters found")
                return Command(update=state_dict)
            
            # Fake vote for the first debater
            vote_for = debaters[0].get("name", "Unknown")
            reasoning = f"As {judge.get('name')}, I find the arguments of {vote_for} more compelling."
            
            # Create vote object
            vote = {
                "voter_id": judge_id,
                "personality": judge.get("personality", ""),
                "vote": vote_for,
                "reasoning": reasoning
            }
            
            # Add vote to state
            votes = state_dict.get("votes", [])
            votes.append(vote)
            state_dict["votes"] = votes
            
            # Add to messages
            messages = state_dict.get("messages", [])
            messages.append(AIMessage(content=f"Judge {judge.get('name')} votes for: {vote_for}\n\nReasoning: {reasoning}"))
            state_dict["messages"] = messages
            
            # Advance to next turn/phase if needed
            state_dict = self._advance_turn(state_dict)
            
            print(f"Added vote from {judge.get('name')} for {vote_for}")
            print(f"New turn: {state_dict.get('turn')}")
            print(f"New phase: {state_dict.get('current_phase')}")
            
            return Command(update=state_dict)
            
        except Exception as e:
            print(f"Error in judge action: {str(e)}")
            return Command(update=state_dict)
    
    def calculate_results(self, state: Dict[str, Any]) -> Command:
        """Calculate and announce the final results.
        
        Args:
            state: Current state
            
        Returns:
            Command with final results
        """
        print("CALCULATING RESULTS")
        # Create a copy of the state dict
        state_dict = state.copy() if isinstance(state, dict) else state.dict() if hasattr(state, "dict") else state.model_dump()
        
        try:
            # Calculate fake results for testing
            votes = state_dict.get("votes", [])
            participants = state_dict.get("participants", [])
            
            # Count votes by debater
            vote_counts = {}
            for vote in votes:
                vote_name = vote.get("vote", "")
                if vote_name in vote_counts:
                    vote_counts[vote_name] += 1
                else:
                    vote_counts[vote_name] = 1
            
            # Find winner
            winner_name = max(vote_counts.items(), key=lambda x: x[1])[0] if vote_counts else None
            
            # Find winner's ID
            winner_id = None
            for p in participants:
                if p.get("name") == winner_name:
                    winner_id = p.get("id")
                    break
            
            # Create result text
            result_text = f"# Final Vote Results\n\n"
            result_text += f"Total votes cast: {len(votes)}\n\n"
            
            for debater_name, count in vote_counts.items():
                result_text += f"{debater_name}: {count} votes\n"
            
            if winner_name:
                result_text += f"\n## Winner: {winner_name}"
            else:
                result_text += "\n## No clear winner"
            
            # Add result to state
            state_dict["result"] = result_text
            state_dict["winner"] = winner_name
            state_dict["current_phase"] = "completed"
            state_dict["game_status"] = "completed"
            
            # Add to messages
            messages = state_dict.get("messages", [])
            messages.append(HumanMessage(content="The judges have reached their decision."))
            messages.append(AIMessage(content=f"# FINAL RESULT\n\n{result_text}"))
            state_dict["messages"] = messages
            
            print(f"Calculated results: Winner={winner_name}")
            print("Debate completed!")
            
            return Command(update=state_dict)
            
        except Exception as e:
            print(f"Error calculating results: {str(e)}")
            return Command(update=state_dict)
    
    # Helper methods
    def _advance_turn(self, state_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Advance to the next turn or phase based on current state.
        
        Args:
            state_dict: Current state dictionary
            
        Returns:
            Updated state dictionary
        """
        current_phase = state_dict.get("current_phase", "setup")
        participants = state_dict.get("participants", [])
        current_turn = state_dict.get("turn", "")
        
        print(f"Advancing from phase={current_phase}, turn={current_turn}")
        
        # Get participants for the current phase
        if current_phase == "opening_statements" or current_phase == "arguments" or current_phase == "closing_statements":
            phase_participants = [p for p in participants if p.get("role") == "debater"]
        elif current_phase == "voting":
            phase_participants = [p for p in participants if p.get("role") == "judge"]
        else:
            phase_participants = []
        
        # Find the index of the current participant
        current_index = -1
        for i, p in enumerate(phase_participants):
            if p.get("id") == current_turn:
                current_index = i
                break
        
        # Check if we're at the end of the current phase
        if current_index == len(phase_participants) - 1 or current_index == -1:
            # Move to the next phase
            phase_sequence = state_dict.get("phase_sequence", ["setup", "opening_statements", "arguments", "closing_statements", "voting", "results", "completed"])
            
            try:
                current_phase_index = phase_sequence.index(current_phase)
                next_phase = phase_sequence[current_phase_index + 1] if current_phase_index + 1 < len(phase_sequence) else "completed"
                
                # Handle phase transitions
                if next_phase == "arguments":
                    state_dict["current_round"] = 1
                elif current_phase == "arguments" and next_phase == "arguments":
                    state_dict["current_round"] = state_dict.get("current_round", 1) + 1
                    if state_dict["current_round"] > state_dict.get("max_rounds", 3):
                        next_phase = phase_sequence[current_phase_index + 1]
                
                state_dict["current_phase"] = next_phase
                print(f"Advanced to next phase: {next_phase}")
                
                # Set the turn to the first participant of the next phase
                if next_phase == "opening_statements" or next_phase == "arguments" or next_phase == "closing_statements":
                    debaters = [p for p in participants if p.get("role") == "debater"]
                    if debaters:
                        state_dict["turn"] = debaters[0].get("id", "")
                
                elif next_phase == "voting":
                    judges = [p for p in participants if p.get("role") == "judge"]
                    if judges:
                        state_dict["turn"] = judges[0].get("id", "")
                
                else:
                    # For phases without turns
                    state_dict["turn"] = ""
                    
            except (ValueError, IndexError):
                # If the current phase is not found or no next phase
                state_dict["current_phase"] = "completed"
                state_dict["turn"] = ""
                
        else:
            # Move to the next participant in the current phase
            state_dict["turn"] = phase_participants[current_index + 1].get("id", "")
            print(f"Advanced to next participant: {state_dict['turn']}")
            
        return state_dict


class DebateConfig(GameConfig):
    """Configuration for multi-agent debate framework.
    
    This configuration extends GameConfig to add debate-specific settings.
    """
    # Debate structure
    topic: str = Field(default="Discuss the benefits and drawbacks of AI", description="Topic of the debate")
    description: str = Field(default="", description="Description of the debate scenario")
    max_rounds: int = Field(default=3, description="Maximum number of argument rounds")
    
    # Phase configuration
    phases: List[str] = Field(
        default=[
            "setup",
            "opening_statements",
            "arguments",
            "closing_statements",
            "voting",
            "results",
            "completed"
        ],
        description="Sequence of phases in the debate"
    )
    
    # Participant configuration
    num_debaters: int = Field(default=2, description="Number of debaters")
    num_judges: int = Field(default=3, description="Number of judges")
    
    # LLM configurations
    participant_generator_llm: AugLLMConfig = Field(
        default=AugLLMConfig(
            name="participant_generator_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.9})
        ),
        description="LLM for generating debate participants"
    )
    
    debater_llm: AugLLMConfig = Field(
        default=AugLLMConfig(
            name="debater_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7})
        ),
        description="Default LLM for debaters"
    )
    
    judge_llm: AugLLMConfig = Field(
        default=AugLLMConfig(
            name="judge_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.4})
        ),
        description="Default LLM for judges"
    )
    
    # Specific participant LLMs (optional)
    participant_llms: Dict[str, AugLLMConfig] = Field(
        default_factory=dict,
        description="LLM configurations for specific participants (by ID)"
    )
    
    # State schema - will use DebateState by default
    state_schema: Type[BaseModel] = Field(default=DebateState, description="State schema for the debate")
    
    @classmethod
    def create_default(cls, topic: str, max_rounds: int = 3):
        """Create a default debate configuration.
        
        Args:
            topic: Topic of the debate
            max_rounds: Maximum number of rounds
            
        Returns:
            Default DebateConfig
        """
        return cls(
            topic=topic,
            max_rounds=max_rounds
        )