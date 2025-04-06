from typing import Any, Dict, List, Optional, Type, Union
import uuid
import logging
from pydantic import BaseModel, Field

from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.language_models import BaseChatModel

from src.haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from src.haive.core.graph.retry import RetryPolicy, create_exponential_backoff_policy

#from src.haive.agents.rec_plan.models import RecursiveTreePlannerState, ReasoningModule
from src.haive.agents.rec_plan.engines import create_engine_registry
from src.haive.agents.rec_plan.state import RecursiveTreePlannerState
from src.haive.agents.rec_plan.models import ReasoningModule
# Configure logging
logger = logging.getLogger(__name__)

class RecursiveTreePlannerConfig(AgentConfig):
    """Configuration for a recursive tree planner agent."""
    # Schema
    state_schema: Type[BaseModel] = Field(
        default=RecursiveTreePlannerState,
        description="Schema for the agent state"
    )
    
    # Engines configuration
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=dict,
        description="Engines used by the agent"
    )
    
    # Tools
    tools: List[Union[BaseTool, StructuredTool]] = Field(
        default_factory=list,
        description="Tools available to the agent"
    )
    
    # Execution configuration
    max_parallel_steps: int = Field(
        default=3,
        description="Maximum number of steps to execute in parallel"
    )
    execution_timeout: float = Field(
        default=60.0,
        description="Timeout for step execution in seconds"
    )
    retry_policy: Optional[RetryPolicy] = Field(
        default=None,
        description="Retry policy for step execution"
    )
    
    # Reasoning modules
    available_reasoning_modules: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Available reasoning modules"
    )
    
    # Iteration control
    max_iterations: int = Field(
        default=2,
        description="Maximum number of planning iterations"
    )
    replan_threshold: float = Field(
        default=0.7,
        description="Threshold for replanning (0-1)"
    )
    
    @classmethod
    def create_default(cls, 
                    name: Optional[str] = None, 
                    llm_config: Optional[LLMConfig] = None,
                    tools: Optional[List[Union[BaseTool, StructuredTool]]] = None,
                    **kwargs) -> 'RecursiveTreePlannerConfig':
        """Create a default configuration for the recursive tree planner agent."""

        # Set up default LLM if none provided
        if llm_config is None:
            llm_config = AzureLLMConfig(
                model="gpt-4o", 
                parameters={"temperature": 0.7}
            )

        # Create engines
        engines = create_engine_registry(llm_config)

        # Set up default tools
        tools = tools or []

        # Set up default retry policy
        retry_policy = kwargs.pop("retry_policy", create_exponential_backoff_policy(
            max_retries=3,
            base_delay=1.0,
            max_delay=10.0
        ))

        # Set up default reasoning modules
        default_reasoning_modules = [
            {"name": "Problem Decomposition", "description": "Break down complex problems."},
            {"name": "Structured Analysis", "description": "Create structured frameworks for problem analysis."},
            {"name": "Critical Thinking", "description": "Analyze assumptions and evaluate evidence."},
            {"name": "Creative Solution Generation", "description": "Generate innovative solutions."},
            {"name": "Step-by-Step Planning", "description": "Create organized step-by-step plans."},
            {"name": "Logical Reasoning", "description": "Apply deductive, inductive, and abductive reasoning."},
            {"name": "Numerical Analysis", "description": "Use mathematical concepts to analyze quantitative problems."},
            {"name": "Information Synthesis", "description": "Combine information from multiple sources."},
            {"name": "Evaluation & Comparison", "description": "Assess solutions against criteria."},
            {"name": "Systems Thinking", "description": "Analyze how parts of a system interact."},
            {"name": "Counterfactual Reasoning", "description": "Consider alternative conditions."},
            {"name": "Algorithmic Thinking", "description": "Develop step-by-step problem-solving procedures."}
        ]

        # Ensure that kwargs do not contain conflicting keys
        return cls(
            name=name or f"recursive_tree_planner_{uuid.uuid4().hex[:8]}",
            engine=engines["planning"],  # Primary engine
            engines=engines,
            state_schema=RecursiveTreePlannerState,
            tools=tools,
            max_parallel_steps=kwargs.pop("max_parallel_steps", 3),  # ✅ Fix
            execution_timeout=kwargs.pop("execution_timeout", 60.0),  # ✅ Fix
            retry_policy=retry_policy,
            max_iterations=kwargs.pop("max_iterations", 2),  # ✅ Fix
            replan_threshold=kwargs.pop("replan_threshold", 0.7),  # ✅ Fix
            available_reasoning_modules=kwargs.pop("available_reasoning_modules", default_reasoning_modules),  # ✅ Fix
            **kwargs  # ✅ This now only contains extra keys
        )

    
    def register_tool(self, tool: Union[BaseTool, StructuredTool]) -> 'RecursiveTreePlannerConfig':
        """Register a tool with the agent."""
        self.tools.append(tool)
        return self
    
    def register_reasoning_module(self, name: str, description: str) -> 'RecursiveTreePlannerConfig':
        """Register a reasoning module with the agent."""
        self.available_reasoning_modules.append({
            "name": name,
            "description": description
        })
        return self