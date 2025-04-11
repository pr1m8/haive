from typing import Optional, List, Dict, Any, Union, Type
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.models.vectorstore.base import VectorStoreConfig
from src.haive.core.models.retriever.base import RetrieverConfig, RetrieverType

# Import KYC-specific modules
from src.haive.prebuilt.priv.kyc.state import KYCReportState, KYCInputState, KYCOutputState
from src.haive.prebuilt.priv.kyc.prompts import (
    MAIN_SYSTEM_PROMPT, 
    CORPAY_RISK_APPETITE_STATEMENT
)
from src.haive.prebuilt.priv.kyc.structured_tools import KYC_TOOLS
from src.haive.prebuilt.priv.kyc.engines import create_kyc_engines
from src.haive.prebuilt.priv.kyc.react_agent_config import (
    create_kyc_react_agent_config,
    create_kyc_rag_agent_config,
    create_kyc_rag_engine
)

class KYCReportConfig(AgentConfig):
    """Configuration for KYC report generation agent"""
    
    # Override state schema to use our custom state
    state_schema: Type[BaseModel] = Field(
        default=KYCReportState,
        description="Schema for the agent state"
    )
    
    # Input and output schemas
    input_schema: Type[BaseModel] = Field(
        default=KYCInputState,
        description="Schema for input to the agent"
    )
    
    output_schema: Type[BaseModel] = Field(
        default=KYCOutputState,
        description="Schema for agent output"
    )
    
    # Company risk profile (preset in our case)
    risk_appetite_statement: str = Field(
        default=CORPAY_RISK_APPETITE_STATEMENT,
        description="Company risk appetite statement"
    )
    
    # Engines dictionary
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=dict,
        description="Dictionary of AugLLM engines for different tasks"
    )
    
    # Tool configurations
    tools: List[BaseTool] = Field(
        default_factory=lambda: KYC_TOOLS,
        description="Tools for KYC research and analysis"
    )
    
    # Vector store configuration
    vectorstore_config: Optional[VectorStoreConfig] = Field(
        default=None,
        description="Vector store configuration for document storage"
    )
    
    # Agent configurations
    react_agent_name: Optional[str] = Field(
        default=None,
        description="Name of the configured ReAct agent"
    )
    
    rag_agent_name: Optional[str] = Field(
        default=None,
        description="Name of the configured RAG agent"
    )
    
    # Report generation settings
    report_format: str = Field(
        default="markdown",
        description="Format for the final report (markdown, html, etc.)"
    )
    
    default_report_sections: List[Dict[str, Any]] = Field(
        default_factory=lambda: [
            {
                "name": "Executive Summary",
                "description": "Brief overview of customer and risk assessment",
                "requires_research": False
            },
            {
                "name": "Company Information",
                "description": "General details about the company, its business model, and operations",
                "requires_research": True
            },
            {
                "name": "Business Activities Analysis",
                "description": "Detailed analysis of the company's business activities and risk factors",
                "requires_research": True
            },
            {
                "name": "Regulatory Compliance",
                "description": "Assessment of regulatory compliance and licensing",
                "requires_research": True
            },
            {
                "name": "Negative News Screening",
                "description": "Analysis of any negative news or regulatory actions",
                "requires_research": True
            },
            {
                "name": "Risk Assessment",
                "description": "Overall risk assessment and categorization",
                "requires_research": False
            },
            {
                "name": "Recommendations",
                "description": "Recommendations for customer onboarding or enhanced due diligence",
                "requires_research": False
            }
        ],
        description="Default report sections"
    )
    
    @classmethod
    def from_scratch(cls, name: Optional[str] = None, llm_model: str = "gpt-4o", **kwargs):
        """Create a KYC report agent configuration from scratch"""
        
        # Create a name if not provided
        if not name:
            name = f"kyc_report_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create LLM configuration
        llm_config = AzureLLMConfig(
            model=llm_model,
            parameters={"temperature": 0.2}  # Lower temperature for more predictable outputs
        )
        
        # Create main AugLLM engine
        main_engine = AugLLMConfig(
            name="kyc_report_main",
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages([
                SystemMessage(content=MAIN_SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="messages")
            ])
        )
        
        # Get all specialized engines
        engines = create_kyc_engines(llm_model)
        
        # Add main engine to engines dictionary
        engines["main"] = main_engine
        
        # Create ReAct agent config for research
        react_agent_config = create_kyc_react_agent_config(
            name=f"{name}_research",
            llm_model=llm_model,
            temperature=0.2
        )
        
        # Create RAG engine (but not the full config yet since we need loaded documents)
        rag_engine_name = f"{name}_retrieval_engine"
        rag_engine = create_kyc_rag_engine(
            name=rag_engine_name,
            llm_model=llm_model,
            temperature=0.2
        )
        
        # Store the engine in the engines dictionary
        engines["rag_engine"] = rag_engine
        
        # No rag_agent_name yet - will be set up after vector store is populated
        rag_agent_name = None
        
        # Create the KYC report agent config
        return cls(
            name=name,
            engine=main_engine,  # Set main engine as primary
            engines=engines,     # Set all engines in dictionary
            react_agent_name=react_agent_config.name,
            rag_agent_name=rag_agent_name,  # This will be set later after documents are loaded
            tools=KYC_TOOLS,
            **kwargs
        )