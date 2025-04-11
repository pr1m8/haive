from __future__ import annotations
from typing import Optional, Dict, Any, List, Union, Annotated
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid
from enum import Enum, auto

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

# Import the enhanced models
from src.haive.prebuilt.misc.company_researcher.models import (
    EnhancedKYCCustomerProfile,
    ProhibitedActivity,
    RestrictedIndustry,
    ComplianceRiskFactor
)

class KYCWorkflowStage(str, Enum):
    """Stages in the KYC workflow"""
    INITIAL_SCREENING = "initial_screening"
    RISK_ASSESSMENT = "risk_assessment"
    ENHANCED_DUE_DILIGENCE = "enhanced_due_diligence"
    FINAL_DECISION = "final_decision"
    COMPLETED = "completed"
    ERROR = "error"

class KYCDecisionStatus(str, Enum):
    """Possible decision statuses in KYC workflow"""
    PENDING = "pending"
    APPROVED = "approved"
    CONDITIONAL_APPROVAL = "conditional_approval"
    PENDING_REVIEW = "pending_review"
    REJECTED = "rejected"

class KYCWorkflowState(BaseModel):
    """
    Comprehensive state model for KYC workflow
    
    Captures the entire state of the KYC processing pipeline
    """
    # Workflow Tracking
    current_stage: KYCWorkflowStage = Field(
        default=KYCWorkflowStage.INITIAL_SCREENING,
        description="Current stage in the KYC workflow"
    )
    
    # Customer Profile
    customer_profile: Optional[EnhancedKYCCustomerProfile] = Field(
        default=None,
        description="Comprehensive customer profile"
    )
    
    # Workflow Messaging
    messages: Annotated[List[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Conversation and workflow messages"
    )
    
    # Decision Tracking
    decision_status: KYCDecisionStatus = Field(
        default=KYCDecisionStatus.PENDING,
        description="Current decision status of the KYC process"
    )
    
    # Workflow Metadata
    workflow_id: str = Field(
        default_factory=lambda: f"KYC-{uuid.uuid4().hex[:8]}",
        description="Unique identifier for this KYC workflow instance"
    )
    
    # Screening Iterations
    screening_iterations: int = Field(
        default=0,
        description="Number of screening iterations performed",
        ge=0
    )
    
    # Additional Routing Information
    next_stage: Optional[KYCWorkflowStage] = Field(
        default=None,
        description="Next stage in the workflow"
    )
    
    # Error Handling
    error_details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Details of any errors encountered during processing"
    )
    
    # Temporal Tracking
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of workflow creation"
    )
    
    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of last workflow update"
    )
    
    # Configuration for extra flexibility
    model_config = ConfigDict(
        extra='allow',  # Allow extra fields
        validate_assignment=True  # Validate on assignment
    )
    
    def update_stage(self, new_stage: KYCWorkflowStage) -> None:
        """
        Update the current workflow stage
        
        Args:
            new_stage: New workflow stage
        """
        self.current_stage = new_stage
        self.last_updated = datetime.now()
        
        # Increment screening iterations for certain stages
        if new_stage in [
            KYCWorkflowStage.RISK_ASSESSMENT, 
            KYCWorkflowStage.ENHANCED_DUE_DILIGENCE
        ]:
            self.screening_iterations += 1
    
    def set_decision_status(self, status: KYCDecisionStatus) -> None:
        """
        Set the decision status and update stage
        
        Args:
            status: New decision status
        """
        self.decision_status = status
        
        # Update stage based on decision
        if status in [
            KYCDecisionStatus.APPROVED, 
            KYCDecisionStatus.REJECTED, 
            KYCDecisionStatus.CONDITIONAL_APPROVAL
        ]:
            self.current_stage = KYCWorkflowStage.FINAL_DECISION
        
        self.last_updated = datetime.now()
    
    def log_error(self, error_details: Dict[str, Any]) -> None:
        """
        Log error details and update workflow state
        
        Args:
            error_details: Dictionary of error information
        """
        self.current_stage = KYCWorkflowStage.ERROR
        self.error_details = error_details
        self.decision_status = KYCDecisionStatus.REJECTED
        self.last_updated = datetime.now()

"""
def main():
    # Create a sample KYC workflow state
    kyc_state = KYCWorkflowState(
        customer_profile=EnhancedKYCCustomerProfile(
            basic_info={
                "full_name": "John Doe",
                "date_of_birth": datetime(1985, 5, 15)
            }
        )
    )
    
    # Demonstrate stage update
    print("Initial State:")
    print(kyc_state.model_dump_json(indent=2))
    
    # Update stage
    kyc_state.update_stage(KYCWorkflowStage.RISK_ASSESSMENT)
    
    # Set decision status
    kyc_state.set_decision_status(KYCDecisionStatus.PENDING_REVIEW)
    
    # Log an error (optional)
    kyc_state.log_error({
        "error_type": "compliance_issue",
        "message": "Additional verification required"
    })
    
    print("\nUpdated State:")
    print(kyc_state.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
"""