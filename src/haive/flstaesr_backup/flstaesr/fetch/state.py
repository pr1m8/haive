from pydantic import BaseModel, Field
from typing import Optional, List
from typing import Annotated, Sequence, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from src.haive.agents.flstaesr.fetch.models import (
    SourceQueryState, DocumentSource
)


class SourceFindingState(BaseModel):
    """State for the source finding step."""
    search_results: List[Dict[str, Any]] = Field(default_factory=list, description="Search results")
    selected_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Selected sources")
    rejected_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Rejected sources")
    reasoning: Optional[str] = Field(default=None, description="Reasoning for source selection")

class DocumentLoadingState(BaseModel):
    """State for the document loading step."""
    loaded_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Successfully loaded sources")
    failed_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Failed to load sources")
    loaded_documents_count: int = Field(default=0, description="Count of loaded documents")
    document_summaries: List[str] = Field(default_factory=list, description="Brief summaries of loaded documents")

class SourceFinderSchema(BaseModel):
    """Schema for source finder agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default=[],
        description="Messages in the conversation"
    )
    
    # Query analysis
    query_state: Optional[SourceQueryState] = Field(default=None, description="State of query analysis")
    
    # Source finding
    finding_state: Optional[SourceFindingState] = Field(default=None, description="State of source finding")
    
    # Document loading
    loading_state: Optional[DocumentLoadingState] = Field(default=None, description="State of document loading")
    
    # Sources and documents
    potential_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Potential sources identified")
    discovered_sources: List[DocumentSource] = Field(default_factory=list, description="Sources discovered")
    loaded_documents: List[Dict[str, Any]] = Field(default_factory=list, description="Loaded documents")
    
    # Tracking
    current_step: str = Field(default="initialize", description="Current step in the process")
    current_substep: int = Field(default=0, description="Current substep")
    total_steps: int = Field(default=4, description="Total steps in the process")
    step_history: List[str] = Field(default_factory=list, description="History of steps taken")
    
    # Error handling
    error: Optional[str] = Field(default=None, description="Error message if any step fails")