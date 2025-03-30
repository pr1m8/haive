from src.haive.games.framework.base.config import GameConfig
from src.haive.games.debate.state import DebateState
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from pydantic import BaseModel, Field
from typing import Dict, Type, List

class DebateConfig(GameConfig):
    """Configuration for multi-agent debate framework.
    
    This configuration extends GameConfig to add debate-specific settings.
    """
    # Debate structure
    topic: str = Field(default="Discuss the benefits and drawbacks of AI", description="Topic of the debate")
    description: str = Field(default="", description="Description of the debate scenario")
    max_rounds: int = Field(default=3, description="Maximum number of argument rounds")
    state_schema: Type[BaseModel] = Field(default_factory=DebateState, description="State schema for the debate")
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
            max_rounds=max_rounds,
            #state_schema=DebateState
        )