from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any, Union, Literal
from enum import Enum, auto
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import SystemMessage

class ProhibitedActivity(str, Enum):
    """Comprehensive list of prohibited activities based on Corpay's risk appetite"""
    # Illegal Activities
    ARMS_MUNITIONS = "arms_and_munitions_trade"
    UNLAWFUL_DRUGS = "unlawful_drug_trade"
    ADULT_ENTERTAINMENT = "adult_entertainment"
    HUMAN_TRAFFICKING = "human_trafficking"
    HUMAN_EXPLOITATION = "human_exploitation"
    UNLICENSED_GAMBLING = "unlicensed_gambling"
    
    # Financial Crimes
    MONEY_LAUNDERING = "money_laundering"
    TERRORISM_FINANCING = "terrorism_financing"
    TAX_EVASION = "tax_evasion"
    
    # Regulatory Violations
    UNAUTHORIZED_CRYPTO = "unauthorized_cryptocurrency"
    UNREGISTERED_MSB = "unregistered_money_services"
    ANONYMOUS_ACCOUNTS = "anonymous_numbered_accounts"
    SHELL_BANKING = "shell_banking"
    
    # Suspicious Business Types
    CASH_INTENSIVE = "cash_intensive_business"
    HIGH_VALUE_GOODS = "high_value_luxury_goods"
    OFFSHORE_BANKING = "offshore_banking"
    MULTI_LEVEL_MARKETING = "multi_level_marketing"

class RestrictedIndustry(str, Enum):
    """Industries requiring enhanced due diligence"""
    ARMS_DEFENSE = "arms_and_defense"
    CHARITY_NPO = "charities_non_profit"
    FINANCIAL_SERVICES = "financial_services"
    GAMBLING = "gambling"
    GENERAL_TRADING = "general_trading"
    CANNABIS = "cannabis_related"
    PAYMENT_PROCESSING = "third_party_payment_processors"
    VEHICLE_DEALERS = "used_vehicle_dealers"
    VIRTUAL_ASSETS = "virtual_asset_services"
    TRAVEL_TOURISM = "travel_and_tourism"
    POLITICALLY_EXPOSED = "politically_exposed_persons"

class ComplianceRiskFactor(str, Enum):
    """Detailed compliance risk factors"""
    OWNERSHIP_TRANSPARENCY = "lack_of_beneficial_ownership_transparency"
    COMPLEX_CORPORATE_STRUCTURE = "complex_corporate_structure"
    INTERNATIONAL_PRESENCE = "high_risk_international_operations"
    CASH_TRANSACTIONS = "high_volume_cash_transactions"
    REGULATORY_HISTORY = "previous_regulatory_violations"
    SANCTIONS_EXPOSURE = "sanctions_list_exposure"
    UNUSUAL_TRANSACTION_PATTERNS = "unusual_transaction_patterns"

class IdentityVerificationLevel(str, Enum):
    """Levels of identity verification"""
    NONE = "no_verification"
    BASIC = "basic_verification"
    STANDARD = "standard_verification"
    ENHANCED = "enhanced_verification"
    COMPREHENSIVE = "comprehensive_verification"

class GeographicRiskProfile(str, Enum):
    """Geographic risk assessment categories"""
    LOW_RISK = "low_risk_jurisdiction"
    MEDIUM_RISK = "medium_risk_jurisdiction"
    HIGH_RISK = "high_risk_jurisdiction"
    SANCTIONED = "sanctioned_jurisdiction"

class EnhancedDueDiligenceRequirement(str, Enum):
    """Triggers for Enhanced Due Diligence"""
    PEP_ASSOCIATION = "politically_exposed_person"
    HIGH_RISK_INDUSTRY = "high_risk_industry"
    COMPLEX_OWNERSHIP = "complex_ownership_structure"
    UNUSUAL_ACTIVITY = "unusual_transaction_activity"
    INTERNATIONAL_OPERATIONS = "cross_border_operations"
    PREVIOUS_ISSUES = "history_of_compliance_issues"

class CustomerRiskProfile(BaseModel):
    """Comprehensive customer risk profile"""
    # Prohibited Activities
    prohibited_activities: List[ProhibitedActivity] = Field(
        default_factory=list,
        description="List of identified prohibited activities"
    )
    
    # Restricted Industries
    restricted_industries: List[RestrictedIndustry] = Field(
        default_factory=list,
        description="Industries requiring additional scrutiny"
    )
    
    # Detailed Risk Factors
    compliance_risk_factors: List[ComplianceRiskFactor] = Field(
        default_factory=list,
        description="Specific compliance risk indicators"
    )
    
    # Geographic Risks
    geographic_risks: Dict[str, GeographicRiskProfile] = Field(
        default_factory=dict,
        description="Risk profile for jurisdictions of operation"
    )
    
    # Enhanced Due Diligence Triggers
    edd_requirements: List[EnhancedDueDiligenceRequirement] = Field(
        default_factory=list,
        description="Triggers for Enhanced Due Diligence"
    )
    
    # Risk Scoring
    overall_risk_score: float = Field(
        default=0.0, 
        ge=0.0, 
        le=100.0,
        description="Comprehensive risk score (0-100)"
    )
    
    @field_validator('overall_risk_score', mode='before')
    def calculate_risk_score(cls, v, values):
        """
        Dynamically calculate risk score based on identified risk factors
        """
        base_score = 0.0
        
        # Prohibited activities are highest risk
        if 'prohibited_activities' in values:
            base_score += len(values['prohibited_activities']) * 20
        
        # Restricted industries add moderate risk
        if 'restricted_industries' in values:
            base_score += len(values['restricted_industries']) * 10
        
        # Compliance risk factors
        if 'compliance_risk_factors' in values:
            risk_factor_scores = {
                ComplianceRiskFactor.OWNERSHIP_TRANSPARENCY: 15,
                ComplianceRiskFactor.COMPLEX_CORPORATE_STRUCTURE: 15,
                ComplianceRiskFactor.INTERNATIONAL_PRESENCE: 10,
                ComplianceRiskFactor.CASH_TRANSACTIONS: 15,
                ComplianceRiskFactor.REGULATORY_HISTORY: 20,
                ComplianceRiskFactor.SANCTIONS_EXPOSURE: 25,
                ComplianceRiskFactor.UNUSUAL_TRANSACTION_PATTERNS: 20
            }
            base_score += sum(
                risk_factor_scores.get(factor, 10) 
                for factor in values['compliance_risk_factors']
            )
        
        # Geographic risks
        if 'geographic_risks' in values:
            geo_risk_scores = {
                GeographicRiskProfile.LOW_RISK: 0,
                GeographicRiskProfile.MEDIUM_RISK: 10,
                GeographicRiskProfile.HIGH_RISK: 20,
                GeographicRiskProfile.SANCTIONED: 50
            }
            base_score += sum(
                geo_risk_scores.get(risk, 10) 
                for risk in values['geographic_risks'].values()
            )
        
        # Ensure score is between 0 and 100
        return min(max(base_score, 0), 100)

class OwnershipStructure(BaseModel):
    """Detailed ownership and control information"""
    ultimate_beneficial_owners: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of ultimate beneficial owners"
    )
    ownership_percentage: Dict[str, float] = Field(
        default_factory=dict,
        description="Ownership percentages for key stakeholders"
    )
    corporate_hierarchy: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Detailed corporate ownership hierarchy"
    )
    control_mechanisms: List[str] = Field(
        default_factory=list,
        description="Mechanisms of corporate control"
    )

class ComplianceDocumentation(BaseModel):
    """Comprehensive compliance documentation tracking"""
    verified_documents: Dict[str, bool] = Field(
        default_factory=dict,
        description="Status of required compliance documents"
    )
    document_expiration_dates: Dict[str, datetime] = Field(
        default_factory=dict,
        description="Expiration dates for compliance documents"
    )
    verification_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Historical record of document verifications"
    )
    missing_documents: List[str] = Field(
        default_factory=list,
        description="List of documents still required"
    )

class EnhancedKYCCustomerProfile(BaseModel):
    """
    Comprehensive and enhanced KYC customer profile
    Combines multiple aspects of customer risk assessment
    """
    # Basic Identification
    customer_id: str = Field(
        default_factory=lambda: f"CUS-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}",
        description="Unique customer identifier"
    )
    
    # Personal/Business Information
    full_name: str = Field(..., description="Full legal name")
    date_of_birth: Optional[datetime] = Field(None, description="Date of birth")
    nationality: Optional[str] = Field(None, description="Nationality")
    business_name: Optional[str] = Field(None, description="Registered business name")
    
    # Comprehensive Risk Assessment
    risk_profile: CustomerRiskProfile = Field(
        default_factory=CustomerRiskProfile,
        description="Detailed customer risk profile"
    )
    
    # Ownership and Control
    ownership: Optional[OwnershipStructure] = Field(
        default=None,
        description="Detailed ownership and control information"
    )
    
    # Compliance Documentation
    compliance_docs: ComplianceDocumentation = Field(
        default_factory=ComplianceDocumentation,
        description="Comprehensive compliance documentation"
    )
    
    # Identity Verification
    identity_verification_level: IdentityVerificationLevel = Field(
        default=IdentityVerificationLevel.BASIC,
        description="Level of identity verification completed"
    )
    
    # Temporal Tracking
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    # Additional Metadata
    additional_notes: Optional[str] = Field(None, description="Additional compliance notes")
    
    # Configuration for extra flexibility
    model_config = ConfigDict(
        extra='allow',  # Allow extra fields
        validate_assignment=True  # Validate on assignment
    )
    
    @model_validator(mode='before')
    def validate_customer_profile(cls, values):
        """
        Perform comprehensive validation of the customer profile
        """
        # Ensure either personal or business name is provided
        if not values.get('full_name') and not values.get('business_name'):
            raise ValueError("Either full name or business name must be provided")
        
        return values
    
    @field_validator('last_updated')
    def update_last_updated(cls, v):
        """Always update last_updated when the model is modified"""
        return datetime.now()
"""
# Demonstration
def main():
    # Create a sample enhanced KYC customer profile
    customer = EnhancedKYCCustomerProfile(
        full_name="John Michael Doe",
        date_of_birth=datetime(1985, 5, 15),
        nationality="United States",
        business_name="Global Financial Solutions LLC"
    )
    
    # Add some risk factors
    customer.risk_profile.prohibited_activities.append(
        ProhibitedActivity.MONEY_LAUNDERING
    )
    customer.risk_profile.restricted_industries.append(
        RestrictedIndustry.FINANCIAL_SERVICES
    )
    customer.risk_profile.compliance_risk_factors.extend([
        ComplianceRiskFactor.COMPLEX_CORPORATE_STRUCTURE,
        ComplianceRiskFactor.UNUSUAL_TRANSACTION_PATTERNS
    ])
    
    # Print the customer profile with detailed risk assessment
    print("Enhanced KYC Customer Profile:")
    print(customer.model_dump_json(indent=2))
    
    # Demonstrate risk score calculation
    print(f"\nOverall Risk Score: {customer.risk_profile.overall_risk_score}")

if __name__ == "__main__":
    main()
"""

