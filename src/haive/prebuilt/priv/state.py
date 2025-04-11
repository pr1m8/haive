# kyc_agent_schema.py

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from src.haive.prebuilt.priv.config import ClientAnalysisSchema
# Input state for KYC agent
class KYCAgentInput(BaseModel):
    """Input state for the KYC agent"""
    client_name: str = Field(description="Name of the client to analyze")
    initial_information: Optional[str] = Field(
        default=None, 
        description="Any initial information about the client"
    )
    risk_appetite_statement: str = Field(
        description="Current risk appetite statement defining prohibited and restricted activities"
    )

# Complete state for KYC agent
class KYCAgentState(BaseModel):
    """Complete state for the KYC agent during execution"""
    client_name: str = Field(description="Name of the client to analyze")
    initial_information: Optional[str] = Field(
        default=None, 
        description="Any initial information about the client"
    )
    risk_appetite_statement: str = Field(
        description="Current risk appetite statement defining prohibited and restricted activities"
    )
    search_queries: Optional[List[str]] = Field(
        default=None, 
        description="Generated search queries for client research"
    )
    search_results: Optional[List[Dict[str, Any]]] = Field(
        default=None, 
        description="Results from web searches about client"
    )
    research_notes: List[str] = Field(
        default_factory=list, 
        description="Compiled research notes about the client"
    )
    analysis: Optional[ClientAnalysisSchema] = Field(
        default=None, 
        description="Complete analysis of client against risk appetite statement"
    )
    reflection_complete: Optional[bool] = Field(
        default=None, 
        description="Whether reflection determines we have sufficient information"
    )
    reflection_steps_taken: int = Field(
        default=0, 
        description="Number of reflection steps completed"
    )
    
# Output state for KYC agent
class KYCAgentOutput(BaseModel):
    """Output state for the KYC agent"""
    analysis: ClientAnalysisSchema = Field(
        description="Complete analysis of client against risk appetite statement"
    )
    search_results: Optional[List[Dict[str, Any]]] = Field(
        default=None, 
        description="Results from web searches about client"
    )