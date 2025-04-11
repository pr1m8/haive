# kyc_agent_config.py

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.engine.aug_llm import AzureLLMConfig
from src.haive.core.engine.aug_llm import AugLLMConfig

from enum import Enum
class ComplianceCategory(str, Enum):
    PROHIBITED = "PROHIBITED"
    RESTRICTED = "RESTRICTED"
    ACCEPTABLE = "ACCEPTABLE"

class ClientAnalysisSchema(BaseModel):
    """Schema for detailed client analysis against risk appetite statement"""
    client_name: str = Field(description="Official name of the client company")
    business_description: str = Field(description="Description of client's business activities")
    prohibited_activities_detected: List[str] = Field(
        default_factory=list, 
        description="List of prohibited activities detected"
    )
    restricted_activities_detected: List[str] = Field(
        default_factory=list, 
        description="List of restricted activities requiring enhanced due diligence"
    )
    compliance_category: ComplianceCategory = Field(
        default=ComplianceCategory.ACCEPTABLE,
        description="Overall compliance categorization"
    )
    reasoning: str = Field(description="Detailed reasoning for the compliance determination")
    confidence_score: float = Field(
        default=0.0, 
        ge=0.0, 
        le=1.0,
        description="Confidence in the assessment (0.0 to 1.0)"
    )

class KYCAgentConfiguration(BaseModel):
    """Configuration parameters for KYC agent"""
    max_search_queries: int = Field(default=5, description="Maximum search queries per client")
    max_search_results: int = Field(default=5, description="Maximum search results per query")
    max_reflection_steps: int = Field(default=2, description="Maximum reflection steps")
    minimum_confidence_threshold: float = Field(
        default=0.7, 
        description="Minimum confidence required for final determination"
    )
    include_search_results: bool = Field(
        default=True, 
        description="Whether to include raw search results in output"
    )

class KYCAgentConfig(AgentConfig):
    """Configuration for KYC agent architecture"""
    name: str = Field(default="kyc_compliance_agent")
    
    # System prompt for the agent
    system_prompt: str = Field(
        default="You are a KYC compliance agent tasked with analyzing potential clients against risk appetite statements."
    )
    
    # LLM Configuration
    llm_config: Optional[AzureLLMConfig] = Field(
        default=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        description="Configuration for the LLM"
    )
    
    # Agent-specific configuration
    agent_configuration: KYCAgentConfiguration = Field(
        default=KYCAgentConfiguration(),
        description="KYC agent specific configuration"
    )
    
    @classmethod
    def create_default(cls, name: Optional[str] = None) -> "KYCAgentConfig":
        """Create a default KYC agent configuration"""
        return cls(
            name=name or f"kyc_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            visualize=True
        )