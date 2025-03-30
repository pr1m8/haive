from typing import Dict, Optional, List, Type, Any, Union
from pydantic import BaseModel, Field

from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig, LLMConfig, OpenAILLMConfig, AnthropicLLMConfig

from src.haive.games.monopoly.prompts import (
    generate_move_decision_prompt,
    generate_property_decision_prompt,
    generate_strategy_analysis_prompt,
    generate_turn_decision_prompt
)
from src.haive.games.monopoly.models import (
    MoveAction,
    PropertyAction,
    StrategyAnalysis,
    TurnDecision
)
from src.haive.games.monopoly.state import MonopolyState

class EngineConfig(BaseModel):
    """Configuration for a specific engine."""
    model: str = Field(..., description="Model name")
    provider: str = Field(default="azure", description="Provider: azure, openai, anthropic")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")
    top_p: Optional[float] = Field(default=None, description="Nucleus sampling parameter")
    top_k: Optional[int] = Field(default=None, description="Top-k sampling parameter")
    api_key: Optional[str] = Field(default=None, description="API key override")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters")

class MonopolyAgentConfig(AgentConfig):
    """Configuration for the Monopoly agent."""
    
    # Game configuration
    debug: bool = Field(default=False, description="Enable debug output")
    max_history: int = Field(default=5, description="Maximum number of history events to track")
    state_schema: Type[BaseModel] = Field(default=MonopolyState, description="The state schema for the Monopoly game")
    
    # LLM engines configuration
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=dict, 
        description="Map of engine name to AugLLMConfig"
    )
    
    # Multi-model configuration
    engine_configs: Dict[str, EngineConfig] = Field(
        default_factory=dict,
        description="Configuration for different engines by name"
    )
    
    # Engine assignments
    strategy_engine: str = Field(
        default="primary", 
        description="Engine to use for strategy analysis"
    )
    move_engine: str = Field(
        default="primary", 
        description="Engine to use for move decisions"
    )
    property_engine: str = Field(
        default="primary", 
        description="Engine to use for property decisions"
    )
    turn_engine: str = Field(
        default="primary", 
        description="Engine to use for overall turn decisions"
    )
    
    @classmethod
    def create_default(
        cls,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        name: Optional[str] = None,
        debug: bool = False,
        max_history: int = 5,
        **kwargs
    ) -> "MonopolyAgentConfig":
        """Create a default configuration for the Monopoly agent."""
        
        # Set up LLM config
        llm_config = AzureLLMConfig(
            model=model,
            parameters={"temperature": temperature}
        )
        
        # Create engines for different decision types
        engines = {
            # Move decision engine
            "move_decision": AugLLMConfig(
                name="move_decision",
                llm_config=llm_config,
                prompt_template=generate_move_decision_prompt(),
                structured_output_model=MoveAction
            ),
            
            # Property decision engine
            "property_decision": AugLLMConfig(
                name="property_decision",
                llm_config=llm_config,
                prompt_template=generate_property_decision_prompt(),
                structured_output_model=PropertyAction
            ),
            
            # Strategy analysis engine
            "strategy": AugLLMConfig(
                name="strategy_analysis",
                llm_config=llm_config,
                prompt_template=generate_strategy_analysis_prompt(),
                structured_output_model=StrategyAnalysis
            ),
            
            # Turn decision engine (main engine)
            "turn_decision": AugLLMConfig(
                name="turn_decision",
                llm_config=llm_config,
                prompt_template=generate_turn_decision_prompt(),
                structured_output_model=TurnDecision
            )
        }
        
        # Create config
        agent_name = name or "monopoly_agent"
        return cls(
            name=agent_name,
            engine=engines["turn_decision"],  # Default engine
            engines=engines,
            debug=debug,
            max_history=max_history,
            state_schema=MonopolyState,
            **kwargs
        )

    @classmethod
    def create_multi_model(
        cls,
        name: Optional[str] = None,
        debug: bool = False,
        max_history: int = 5,
        primary_engine: EngineConfig = None,
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
        for name, config in engine_configs.items():
            # Create the appropriate LLM config
            if config.provider.lower() == "azure":
                llm_configs[name] = AzureLLMConfig(
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
                llm_configs[name] = OpenAILLMConfig(
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
                llm_configs[name] = AnthropicLLMConfig(
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
                llm_configs[name] = AzureLLMConfig(
                    model=config.model,
                    parameters={
                        "temperature": config.temperature,
                        **config.parameters
                    }
                )
        
        # Create AugLLM configs
        aug_llm_configs = {
            # Move decision engine
            "move_decision": AugLLMConfig(
                name="move_decision",
                llm_config=llm_configs["move"],
                prompt_template=generate_move_decision_prompt(),
                structured_output_model=MoveAction
            ),
            
            # Property decision engine
            "property_decision": AugLLMConfig(
                name="property_decision",
                llm_config=llm_configs["property"],
                prompt_template=generate_property_decision_prompt(),
                structured_output_model=PropertyAction
            ),
            
            # Strategy analysis engine
            "strategy": AugLLMConfig(
                name="strategy_analysis",
                llm_config=llm_configs["strategy"],
                prompt_template=generate_strategy_analysis_prompt(),
                structured_output_model=StrategyAnalysis
            ),
            
            # Turn decision engine (main engine)
            "turn_decision": AugLLMConfig(
                name="turn_decision",
                llm_config=llm_configs["turn"],
                prompt_template=generate_turn_decision_prompt(),
                structured_output_model=TurnDecision
            )
        }
        
        # Create config
        agent_name = name or "monopoly_agent_multi"
        return cls(
            name=agent_name,
            engine=aug_llm_configs["turn_decision"],  # Default engine
            engines=aug_llm_configs,
            engine_configs=engine_configs,
            strategy_engine="strategy",
            move_engine="move",
            property_engine="property",
            turn_engine="turn",
            debug=debug,
            max_history=max_history,
            state_schema=MonopolyState,
            **kwargs
        )