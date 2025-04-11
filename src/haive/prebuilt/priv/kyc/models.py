from enum import Enum
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, field_validator

class RiskCategory(str, Enum):
    """Enumeration of risk categories based on Corpay's risk appetite"""
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"
    PROHIBITED = "prohibited"

class BusinessActivity(str, Enum):
    """Enumeration of business activities with associated risk"""
    ARMS_DEFENSE = "arms_defense"
    CALL_INS = "call_ins"
    CHARITIES = "charities"
    CASH_INTENSIVE = "cash_intensive"
    LUXURY_GOODS = "luxury_goods"
    EMBASSIES = "embassies"
    OFFSHORE_BANKING = "offshore_banking"
    FINANCIAL_SERVICES = "financial_services"
    GAMBLING = "gambling"
    GENERAL_TRADING = "general_trading"
    CANNABIS = "cannabis"
    MULTI_LEVEL_MARKETING = "multi_level_marketing"
    POLITICALLY_EXPOSED = "politically_exposed"
    TRAVEL_TOURS = "travel_tours"
    THIRD_PARTY_PROCESSORS = "third_party_processors"
    USED_VEHICLE_DEALERS = "used_vehicle_dealers"
    VIRTUAL_ASSET_PROVIDERS = "virtual_asset_providers"
    OTHER = "other"

class ProhibitedActivity(str, Enum):
    """Enumeration of explicitly prohibited activities"""
    ARMS_DISTRIBUTION = "arms_distribution"
    UNLAWFUL_DRUGS = "unlawful_drugs"
    ADULT_ENTERTAINMENT = "adult_entertainment"
    HUMAN_TRAFFICKING = "human_trafficking"
    HUMAN_EXPLOITATION = "human_exploitation"
    UNLAWFUL_GAMBLING = "unlawful_gambling"
    UNAUTHORIZED_VIRTUAL_CURRENCIES = "unauthorized_virtual_currencies"
    UNLICENSED_MSB = "unlicensed_msb"
    ANONYMOUS_ACCOUNTS = "anonymous_accounts"
    SHELL_BANKS = "shell_banks"

class CustomerRiskAssessmentModel(BaseModel):
    """Comprehensive KYC risk assessment model"""
    
    # Basic customer identification
    customer_name: str = Field(description="Name of the customer or business")
    customer_type: str = Field(description="Type of customer (individual/business)")
    
    # Risk categorization
    overall_risk_category: RiskCategory = Field(
        default=RiskCategory.LOW_RISK, 
        description="Overall risk category based on business activities and compliance"
    )
    
    # Business activity assessment
    primary_business_activity: Optional[BusinessActivity] = Field(
        default=None, 
        description="Primary business activity of the customer"
    )
    
    # Prohibited activities check
    prohibited_activities: List[ProhibitedActivity] = Field(
        default_factory=list, 
        description="List of prohibited activities associated with the customer"
    )
    
    # Compliance flags
    is_politically_exposed: bool = Field(
        default=False, 
        description="Whether the customer is a Politically Exposed Person (PEP)"
    )
    
    beneficial_ownership_confirmed: bool = Field(
        default=False, 
        description="Whether beneficial ownership information has been confirmed"
    )
    
    # Detailed risk factors
    risk_factors: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional risk factors and their details"
    )
    
    # Compliance assessment
    compliance_score: float = Field(
        default=0.0, 
        ge=0.0, 
        le=1.0, 
        description="Compliance score (0.0 - 1.0)"
    )
    
    # Additional assessment details
    additional_notes: Optional[str] = Field(
        default=None, 
        description="Additional notes or comments about the assessment"
    )
    
    @field_validator('compliance_score')
    def validate_compliance_score(cls, v):
        """Ensure compliance score is between 0 and 1"""
        return max(0.0, min(1.0, v))
    
    @field_validator('prohibited_activities', mode='after')
    def check_prohibited_activities(cls, v):
        """Validate and process prohibited activities"""
        if v:
            # Remove duplicates
            return list(set(v))
        return v
    
    def assess_risk(self) -> RiskCategory:
        """
        Assess overall risk based on various factors
        
        Returns:
            RiskCategory: Determined risk category
        """
        # Immediate prohibition if any prohibited activities exist
        if self.prohibited_activities:
            return RiskCategory.PROHIBITED
        
        # High-risk activities
        high_risk_activities = [
            BusinessActivity.ARMS_DEFENSE,
            BusinessActivity.GAMBLING,
            BusinessActivity.OFFSHORE_BANKING,
            BusinessActivity.POLITICALLY_EXPOSED,
            BusinessActivity.VIRTUAL_ASSET_PROVIDERS
        ]
        
        # Check various risk factors
        if self.primary_business_activity in high_risk_activities:
            return RiskCategory.HIGH_RISK
        
        if not self.beneficial_ownership_confirmed:
            return RiskCategory.HIGH_RISK
        
        if self.is_politically_exposed:
            return RiskCategory.HIGH_RISK
        
        # Default to low risk if no red flags
        return RiskCategory.LOW_RISK

class KYCDecisionModel(BaseModel):
    """Decision model for KYC process"""
    
    # Assessment results
    risk_assessment: CustomerRiskAssessmentModel
    
    # Decision outcome
    proceed: bool = Field(description="Whether to proceed with the customer")
    
    # Required actions
    required_actions: List[str] = Field(
        default_factory=list, 
        description="Additional actions required for this customer"
    )
    
    # Reason for decision
    decision_reason: Optional[str] = Field(
        default=None, 
        description="Detailed reason for the proceed/no proceed decision"
    )
    
    def generate_decision(self) -> None:
        """
        Generate a decision based on the risk assessment
        """
        risk_category = self.risk_assessment.assess_risk()
        
        if risk_category == RiskCategory.PROHIBITED:
            self.proceed = False
            self.decision_reason = "Customer involves prohibited activities"
            self.required_actions = ["Immediate rejection", "Escalate to compliance"]
        
        elif risk_category == RiskCategory.HIGH_RISK:
            self.proceed = False
            self.decision_reason = "High-risk customer requiring enhanced due diligence"
            self.required_actions = [
                "Conduct enhanced due diligence", 
                "Request additional documentation", 
                "Senior management review"
            ]
        
        elif risk_category == RiskCategory.MEDIUM_RISK:
            self.proceed = True
            self.decision_reason = "Medium-risk customer requires additional monitoring"
            self.required_actions = [
                "Implement enhanced monitoring", 
                "Periodic review recommended"
            ]
        
        else:  # Low risk
            self.proceed = True
            self.decision_reason = "Low-risk customer meets initial compliance requirements"
            self.required_actions = ["Standard monitoring"]