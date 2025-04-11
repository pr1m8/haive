from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.agents.flstaesr.fetch.state import SourceFinderSchema
#from src.haive.agents.flstaesr.fetch.agent import SearchTool
from src.haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel, Field
from typing import Optional, Type, List
from langchain_core.tools import BaseTool

# ===========================================
# Source Finder Config
# ===========================================

class SourceFinderConfig(AgentConfig):
    """Configuration for a source finder agent."""
    # System prompt
    system_prompt: str = Field(
        default="You are a helpful assistant that identifies the most relevant sources of information for a given query.",
        description="System prompt for the source finder agent"
    )
    
    # Search configuration
    search_tools: List[BaseTool] = Field(
        default_factory=list,
        description="Tools for searching various sources"
    )
    
    max_sources_to_load: int = Field(
        default=3,
        description="Maximum number of sources to load"
    )
    
    # Source selection criteria
    min_relevance_score: float = Field(
        default=0.6,
        description="Minimum relevance score for sources (0-1)"
    )
    
    # Override state schema with source finder schema
    state_schema: Type[BaseModel] = Field(
        default=SourceFinderSchema,
        description="Schema for the agent state"
    )
    
    # Chain configuration
    analyze_query_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for query analysis"
    )
    
    search_analysis_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for search result analysis"
    )
    
    source_selection_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for source selection"
    )
    
    source_to_doc_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for source to document conversion"
    )

    # Workflow
    skip_analysis: bool = Field(
        default=False,
        description="Skip detailed analysis and just use web search"
    )
