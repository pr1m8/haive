from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document
from langgraph.graph import add_messages

# Import risk assessment models
from src.haive.prebuilt.priv.kyc.models import RiskCategory, BusinessActivity, ProhibitedActivity, CustomerRiskAssessmentModel, KYCDecisionModel

class KYCInputState(BaseModel):
    """
    Input state for the KYC process.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Input messages including user query"
    )
    input_context: Optional[str] = Field(
        default=None,
        description="Additional context provided for the KYC assessment"
    )
    

class KYCOutputState(BaseModel):
    """
    Output state for the KYC process.
    """
    final_report: str = Field(
        description="Complete KYC report in markdown format"
    )
    risk_assessment: CustomerRiskAssessmentModel = Field(
        description="Risk assessment for the customer"
    )
    kyc_decision: KYCDecisionModel = Field(
        description="Decision for the customer"
    )
    risk_category: RiskCategory = Field(
        description="Overall risk category (LOW_RISK, MEDIUM_RISK, HIGH_RISK, PROHIBITED)"
    )
    business_activities: List[BusinessActivity] = Field(
        default_factory=list,
        description="Identified business activities"
    )
    prohibited_activities: List[ProhibitedActivity] = Field(
        default_factory=list,
        description="Identified prohibited activities"
    )
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Conversation history including the assistant's final response"
    )

class WebSearchQuery(BaseModel):
    """Represents a web search query for retrieving information"""
    query: str = Field(description="The search query text")
    purpose: str = Field(description="Purpose of this search query")
    completed: bool = Field(default=False, description="Whether this query has been executed")
    results: List[Dict] = Field(default_factory=list, description="Search results")

class ReportSection(BaseModel):
    """Represents a section in the KYC report"""
    name: str = Field(description="Section name")
    description: str = Field(description="Section description")
    content: str = Field(default="", description="Section content")
    requires_research: bool = Field(default=True, description="Whether this section requires web research")
    queries: List[WebSearchQuery] = Field(default_factory=list, description="Search queries for this section")
    sources: List[Dict] = Field(default_factory=list, description="Sources used in this section")
    status: str = Field(default="pending", description="Section status (pending, in_progress, completed)")

class CustomerInfo(BaseModel):
    """Basic customer information for the KYC report"""
    name: str = Field(description="Name of the customer or business")
    customer_type: str = Field(description="Type of customer (individual/business)")
    website: Optional[str] = Field(default=None, description="Customer website URL")
    business_description: Optional[str] = Field(default=None, description="Brief description of business activities")
    location: Optional[str] = Field(default=None, description="Customer's primary location/country")
    additional_context: Optional[str] = Field(default=None, description="Any additional context provided")

class KYCReportState(BaseModel):
    """State schema for KYC report generation agent"""
    # Conversation messages
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Conversation messages"
    )
    
    # Customer information
    customer_info: Optional[CustomerInfo] = Field(
        default=None,
        description="Basic customer information"
    )
    
    # Input context (optional additional information)
    input_context: Optional[str] = Field(
        default=None,
        description="Optional additional context provided by the user"
    )
    
    # Report planning
    report_topic: Optional[str] = Field(
        default=None,
        description="Main topic of the report"
    )
    
    report_sections: List[ReportSection] = Field(
        default_factory=list,
        description="Sections of the KYC report"
    )
    
    # Research management
    current_section_index: Optional[int] = Field(
        default=None,
        description="Index of the current section being researched"
    )
    
    search_queries: List[WebSearchQuery] = Field(
        default_factory=list,
        description="List of search queries to execute"
    )
    
    # Document storage and retrieval
    query: Optional[str] = Field(
        default=None,
        description="Current search query"
    )
    
    retrieved_documents: List[Document] = Field(
        default_factory=list,
        description="Documents retrieved from search"
    )
    
    scraped_websites: List[Dict] = Field(
        default_factory=list,
        description="List of scraped website contents"
    )
    
    # Risk assessment
    risk_assessment: Optional[CustomerRiskAssessmentModel] = Field(
        default=None,
        description="Risk assessment results"
    )
    
    kyc_decision: Optional[KYCDecisionModel] = Field(
        default=None,
        description="KYC decision model with risk assessment"
    )
    
    business_activities: List[BusinessActivity] = Field(
        default_factory=list,
        description="Identified business activities"
    )
    
    prohibited_activities: List[ProhibitedActivity] = Field(
        default_factory=list,
        description="Identified prohibited activities"
    )
    
    risk_category: Optional[RiskCategory] = Field(
        default=None,
        description="Overall risk category assessment"
    )
    
    # Report generation
    final_report: Optional[str] = Field(
        default=None,
        description="Final KYC report content"
    )
    
    # Process management
    current_step: str = Field(
        default="start",
        description="Current step in the workflow"
    )
    
    error: Optional[str] = Field(
        default=None,
        description="Error message if any step fails"
    )
    
    # Dynamic documents storage for vector search
    vectorstore_documents: List[Document] = Field(
        default_factory=list,
        description="Documents loaded into vector store"
    )