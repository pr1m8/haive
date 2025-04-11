"""
Configuration for the Monopoly agent.

This module provides configuration classes for the Monopoly agent, including:
    - Agent configuration
    - Engine configuration for different LLMs
    - Retry policies
"""

from typing import Dict, Optional, List, Type, Any, Union
from pydantic import BaseModel, Field, model_validator

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.agent.persistence.base import CheckpointerConfig
from haive.core.engine.agent.persistence.memory_config import MemoryCheckpointerConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig, OpenAILLMConfig, AnthropicLLMConfig

from haive.games.monopoly.prompts import (
    generate_move_decision_prompt,
    generate_property_decision_prompt,
    generate_strategy_analysis_prompt,
    generate_turn_decision_prompt
)
from haive.games.monopoly.models import (
    MoveAction,
    PropertyAction,
    StrategyAnalysis,
    TurnDecision
)
from haive.games.monopoly.state import MonopolyState

class EngineConfig(BaseModel):
    """Configuration for a specific LLM engine."""
    model: str = Field(..., description="Model name")
    provider: str = Field(default="azure", description="Provider: azure, openai, anthropic")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")
    top_p: Optional[float] = Field(default=None, description="Nucleus sampling parameter")
    top_k: Optional[int] = Field(default=None, description="Top-k sampling parameter")
    api_key: Optional[str] = Field(default=None, description="API key override")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters")

class RetryPolicyConfig(BaseModel):
    """Configuration for retry policies."""
    max_retries: int = Field(default=3, description="Maximum number of retries")
    initial_delay: float = Field(default=1.0, description="Initial delay in seconds")
    backoff_factor: float = Field(default=2.0, description="Backoff multiplier")
    max_delay: float = Field(default=60.0, description="Maximum delay in seconds")
    jitter: bool = Field(default=True, description="Add jitter to delay")

class MonopolyAgentConfig(AgentConfig):
    """Configuration for the Monopoly agent."""
    
    # Game configuration
    debug: bool = Field(default=False, description="Enable debug output")
    max_history: int = Field(default=5, description="Maximum number of history events to track")
    state_schema: Type[BaseModel] = Field(default=MonopolyState, description="The state schema for the Monopoly game")
    num_players: int = Field(default=2, description="Number of players in the game")
    
    # LLM engines configuration
    engines: Dict[str, Union[AugLLMConfig, Dict[str, Any]]] = Field(
        default_factory=dict, 
        description="Map of engine name to AugLLMConfig or engine config dict"
    )
    
    # Multi-model configuration
    engine_configs: Dict[str, EngineConfig] = Field(
        default_factory=dict,
        description="Configuration for different engines by name"
    )
    
    # Engine assignments
    strategy_engine: str = Field(
        default="strategy", 
        description="Engine to use for strategy analysis"
    )
    move_engine: str = Field(
        default="move_decision", 
        description="Engine to use for move decisions"
    )
    property_engine: str = Field(
        default="property_decision", 
        description="Engine to use for property decisions"
    )
    turn_engine: str = Field(
        default="turn_decision", 
        description="Engine to use for overall turn decisions"
    )
    
    # Retry policies
    enable_retries: bool = Field(
        default=True,
        description="Enable retry policies for LLM calls"
    )
    retry_policy: RetryPolicyConfig = Field(
        default_factory=RetryPolicyConfig,
        description="Retry policy configuration"
    )
    
    # Persistence configuration
    persistence: Optional[CheckpointerConfig] = Field(
        default_factory=MemoryCheckpointerConfig,
        description="Persistence configuration for state checkpointing"
    )
    
    # Monopoly specific settings
    properties_to_prioritize: List[str] = Field(
        default_factory=lambda: ["orange", "red", "light_blue"],
        description="Property colors to prioritize (in order of preference)"
    )
    
    mortgage_threshold: int = Field(
        default=300,
        description="Cash threshold below which to consider mortgaging properties"
    )
    
    cash_reserve_target: int = Field(
        default=500,
        description="Target amount of cash to keep in reserve"
    )
    
    target_properties_before_building: int = Field(
        default=5,
        description="Number of properties to acquire before focusing on building"
    )
    
    risky_strategy: bool = Field(
        default=False,
        description="Whether to use a higher-risk strategy (spend more cash, take more risks)"
    )
    
    @model_validator(mode="after")
    def ensure_engines(self):
        """Ensure engines are properly configured."""
        # If no engines are provided, create default ones
        if not self.engines:
            # Create default LLM config
            llm_config = AzureLLMConfig(
                model="gpt-4o", 
                parameters={"temperature": 0.7}
            ).model_dump()
            
            # Create engines for different decision types
            move_decision = AugLLMConfig.from_llm_config(
                name="move_decision",
                llm_config=llm_config,
                prompt_template=generate_move_decision_prompt(),
                structured_output_model=MoveAction
            )
            
            property_decision = AugLLMConfig.from_llm_config(
                name="property_decision",
                llm_config=llm_config,
                prompt_template=generate_property_decision_prompt(),
                structured_output_model=PropertyAction
            )
            
            strategy = AugLLMConfig.from_llm_config(
                name="strategy_analysis",
                llm_config=llm_config,
                prompt_template=generate_strategy_analysis_prompt(),
                structured_output_model=StrategyAnalysis
            )
            
            turn_decision = AugLLMConfig.from_llm_config(
                name="turn_decision",
                llm_config=llm_config,
                prompt_template=generate_turn_decision_prompt(),
                structured_output_model=TurnDecision
            )
            
            # Convert to dictionaries for storage
            self.engines = {
                "move_decision": move_decision.model_dump(),
                "property_decision": property_decision.model_dump(),
                "strategy": strategy.model_dump(),
                "turn_decision": turn_decision.model_dump()
            }
            
            # Set default engine
            if not self.engine:
                self.engine = turn_decision
        
        return self
    
    @classmethod
    def create_default(
        cls,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        name: Optional[str] = None,
        debug: bool = False,
        max_history: int = 5,
        num_players: int = 2,
        **kwargs
    ) -> "MonopolyAgentConfig":
        """
        Create a default configuration for the Monopoly agent.
        
        Args:
            model: LLM model to use
            temperature: Temperature for generation
            name: Optional name for the agent
            debug: Enable debug output
            max_history: Maximum history events to track
            num_players: Number of players in the game
            **kwargs: Additional arguments for configuration
            
        Returns:
            MonopolyAgentConfig instance
        """
        
        # Set up LLM config
        llm_config = AzureLLMConfig(
            model=model,
            parameters={"temperature": temperature}
        ).model_dump()
        
        # Create engines for different decision types
        move_decision = AugLLMConfig.from_llm_config(
            name="move_decision",
            llm_config=llm_config,
            prompt_template=generate_move_decision_prompt(),
            structured_output_model=MoveAction
        )
        
        property_decision = AugLLMConfig.from_llm_config(
            name="property_decision",
            llm_config=llm_config,
            prompt_template=generate_property_decision_prompt(),
            structured_output_model=PropertyAction
        )
        
        strategy = AugLLMConfig.from_llm_config(
            name="strategy_analysis",
            llm_config=llm_config,
            prompt_template=generate_strategy_analysis_prompt(),
            structured_output_model=StrategyAnalysis
        )
        
        turn_decision = AugLLMConfig.from_llm_config(
            name="turn_decision",
            llm_config=llm_config,
            prompt_template=generate_turn_decision_prompt(),
            structured_output_model=TurnDecision
        )
        
        # Convert to dictionaries for storage
        engines = {
            "move_decision": move_decision.model_dump(),
            "property_decision": property_decision.model_dump(),
            "strategy": strategy.model_dump(),
            "turn_decision": turn_decision.model_dump()
        }
        
        # Create config
        agent_name = name or "monopoly_agent"
        return cls(
            name=agent_name,
            engine=turn_decision,  # Default engine
            engines=engines,
            debug=debug,
            max_history=max_history,
            state_schema=MonopolyState,
            num_players=num_players,
            **kwargs
        )

    @classmethod
    def create_multi_model(
        cls,
        name: Optional[str] = None,
        debug: bool = False,
        max_history: int = 5,
        num_players: int = 2,
        primary_engine: Optional[EngineConfig] = None,
        strategy_engine: Optional[EngineConfig] = None,
        move_engine: Optional[EngineConfig] = None,
        property_engine: Optional[EngineConfig] = None,
        turn_engine: Optional[EngineConfig] = None,
        **kwargs
    ) -> "MonopolyAgentConfig":
        """
        Create a configuration with multiple models.
        
        Args:
            name: Optional name for the agent
            debug: Enable debug output
            max_history: Maximum history events to track
            num_players: Number of players in the game
            primary_engine: Primary engine config (fallback for all engines)
            strategy_engine: Engine for strategy analysis
            move_engine: Engine for move decisions
            property_engine: Engine for property decisions
            turn_engine: Engine for turn decisions
            **kwargs: Additional args for configuration
            
        Returns:
            MonopolyAgentConfig instance
        """
        # Ensure we have a primary engine
        if primary_engine is None:
            primary_engine = EngineConfig(
                model="gpt-4o",
                provider="azure",
                temperature=0.7
            )
        
        # Create engine configs
        engine_configs = {
            "primary": primary_engine,
            "strategy": strategy_engine or primary_engine,
            "move": move_engine or primary_engine,
            "property": property_engine or primary_engine,
            "turn": turn_engine or primary_engine
        }
        
        # Create LLM configs
        llm_configs = {}
        for engine_name, config in engine_configs.items():
            # Create the appropriate LLM config
            if config.provider.lower() == "azure":
                llm_configs[engine_name] = AzureLLMConfig(
                    model=config.model,
                    parameters={
                        "temperature": config.temperature,
                        **({"max_tokens": config.max_tokens} if config.max_tokens else {}),
                        **({"top_p": config.top_p} if config.top_p else {}),
                        **({"top_k": config.top_k} if config.top_k else {}),
                        **config.parameters
                    }
                )
            elif config.provider.lower() == "openai":
                llm_configs[engine_name] = OpenAILLMConfig(
                    model=config.model,
                    api_key=config.api_key,
                    extra_params={
                        "temperature": config.temperature,
                        **({"max_tokens": config.max_tokens} if config.max_tokens else {}),
                        **({"top_p": config.top_p} if config.top_p else {}),
                        **config.parameters
                    }
                )
            elif config.provider.lower() == "anthropic":
                llm_configs[engine_name] = AnthropicLLMConfig(
                    model=config.model,
                    api_key=config.api_key,
                    extra_params={
                        "temperature": config.temperature,
                        **({"max_tokens": config.max_tokens} if config.max_tokens else {}),
                        **({"top_p": config.top_p} if config.top_p else {}),
                        **config.parameters
                    }
                )
            else:
                # Default to Azure
                llm_configs[engine_name] = AzureLLMConfig(
                    model=config.model,
                    parameters={
                        "temperature": config.temperature,
                        **config.parameters
                    }
                )
        
        # Create AugLLM configs
        move_decision = AugLLMConfig.from_llm_config(
            name="move_decision",
            llm_config=llm_configs["move"],
            prompt_template=generate_move_decision_prompt(),
            structured_output_model=MoveAction
        )
        
        property_decision = AugLLMConfig.from_llm_config(
            name="property_decision",
            llm_config=llm_configs["property"],
            prompt_template=generate_property_decision_prompt(),
            structured_output_model=PropertyAction
        )
        
        strategy = AugLLMConfig.from_llm_config(
            name="strategy_analysis",
            llm_config=llm_configs["strategy"],
            prompt_template=generate_strategy_analysis_prompt(),
            structured_output_model=StrategyAnalysis
        )
        
        turn_decision = AugLLMConfig.from_llm_config(
            name="turn_decision",
            llm_config=llm_configs["turn"],
            prompt_template=generate_turn_decision_prompt(),
            structured_output_model=TurnDecision
        )
        
        # Convert to dictionaries for storage
        aug_llm_configs = {
            "move_decision": move_decision.model_dump(),
            "property_decision": property_decision.model_dump(),
            "strategy": strategy.model_dump(),
            "turn_decision": turn_decision.model_dump()
        }
        
        # Create config
        agent_name = name or "monopoly_agent_multi"
        return cls(
            name=agent_name,
            engine=turn_decision,  # Default engine
            engines=aug_llm_configs,
            engine_configs=engine_configs,
            strategy_engine="strategy",
            move_engine="move_decision",
            property_engine="property_decision",
            turn_engine="turn_decision",
            debug=debug,
            max_history=max_history,
            state_schema=MonopolyState,
            num_players=num_players,
            **kwargs
        )
    
    @classmethod
    def create_conservative(cls, **kwargs) -> "MonopolyAgentConfig":
        """
        Create a configuration for a conservative player that focuses on cash reserves.
        
        Args:
            **kwargs: Arguments to pass to create_default
            
        Returns:
            MonopolyAgentConfig instance with conservative settings
        """
        # Create base config
        config = cls.create_default(**kwargs)
        
        # Adjust for conservative strategy
        config.mortgage_threshold = 500  # Higher threshold for mortgaging (more cautious)
        config.cash_reserve_target = 800  # Higher cash reserve target
        config.target_properties_before_building = 8  # Acquire more properties before building
        config.risky_strategy = False
        
        # Prioritize safer property groups
        config.properties_to_prioritize = ["light_blue", "orange", "red"]
        
        return config
    
    @classmethod
    def create_aggressive(cls, **kwargs) -> "MonopolyAgentConfig":
        """
        Create a configuration for an aggressive player that focuses on rapid development.
        
        Args:
            **kwargs: Arguments to pass to create_default
            
        Returns:
            MonopolyAgentConfig instance with aggressive settings
        """
        # Create base config
        config = cls.create_default(**kwargs)
        
        # Adjust for aggressive strategy
        config.mortgage_threshold = 200  # Lower threshold for mortgaging (more aggressive)
        config.cash_reserve_target = 300  # Lower cash reserve target
        config.target_properties_before_building = 3  # Build sooner
        config.risky_strategy = True
        
        # Prioritize high-value property groups
        config.properties_to_prioritize = ["orange", "red", "yellow", "green"]
        
        return config