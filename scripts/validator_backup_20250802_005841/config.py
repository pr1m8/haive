from datetime import datetime

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive_prebuilt.misc.company_researcher.models import (
    EnhancedKYCCustomerProfile,
)
from haive_prebuilt.misc.company_researcher.state import (
    KYCWorkflowState,
)
from haive_prebuilt.priv.prompts import (
    create_enhanced_due_diligence_prompt,
    create_initial_screening_prompt,
)
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, field_validator

# Import models and state


class KYCComplianceEngines(BaseModel):
    """Configuration for different KYC compliance engines"""

    initial_screening: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="kyc_initial_screening",
            prompt_template=create_initial_screening_prompt(),
            structured_output_model=EnhancedKYCCustomerProfile,
        ),
        description="Engine for initial customer screening",
    )

    enhanced_due_diligence: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="kyc_enhanced_due_diligence",
            prompt_template=create_enhanced_due_diligence_prompt(),
            structured_output_model=EnhancedKYCCustomerProfile,
        ),
        description="Engine for enhanced due diligence",
    )

    final_risk_assessment: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="kyc_final_risk_assessment",
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    SystemMessage(
                        content="""You are the final compliance reviewer conducting comprehensive risk assessment.

                Review Process:
                1. Synthesize all previous screening and investigation findings
                2. Evaluate cumulative risk factors
                3. Make definitive compliance recommendation
                4. Provide detailed rationale for final decision"""
                    ),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            ),
            structured_output_model=EnhancedKYCCustomerProfile,
        ),
        description="Engine for final risk assessment",
    )


class KYCAgentConfiguration(AgentConfig):
    """Advanced configuration for KYC Agent with granular control"""

    # Screening Thresholds
    risk_score_thresholds: dict[str, float] = Field(
        default_factory=lambda: {
            "low_risk": 25.0,
            "medium_risk": 50.0,
            "high_risk": 75.0,
            "prohibited": 90.0,
        },
        description="Risk score thresholds for different risk categories",
    )

    # Compliance Configuration
    compliance_checks: dict[str, bool] = Field(
        default_factory=lambda: {
            "politically_exposed_persons": True,
            "sanctions_screening": True,
            "adverse_media_check": True,
            "document_verification": True,
        },
        description="Toggle for specific compliance checks",
    )

    # Enhanced Due Diligence Triggers
    edd_triggers: dict[str, float] = Field(
        default_factory=lambda: {
            "risk_score_threshold": 50.0,
            "prohibited_activities_multiplier": 2.0,
            "restricted_industry_threshold": 40.0,
        },
        description="Triggers for Enhanced Due Diligence",
    )

    # KYC Workflow Configuration
    max_screening_iterations: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum number of screening iterations before final decision",
    )

    # Compliance Engines
    compliance_engines: KYCComplianceEngines = Field(
        default_factory=KYCComplianceEngines,
        description="Configurable engines for KYC compliance stages",
    )

    # State Schema Derivation
    def derive_schema(self) -> type[BaseModel]:
        """Create a custom state schema specifically for KYC workflow

        Returns:
            Pydantic model representing the KYC agent state
        """
        # Use the predefined KYCWorkflowState as the state schema
        return KYCWorkflowState

    @field_validator("edd_triggers")
    def validate_edd_triggers(cls, v):
        """Validate Enhanced Due Diligence triggers

        Ensures trigger values are within reasonable ranges
        """
        # Validate risk score threshold
        if (
            v.get("risk_score_threshold", 0) < 0
            or v.get("risk_score_threshold", 0) > 100
        ):
            raise ValueError("Risk score threshold must be between 0 and 100")

        # Validate prohibited activities multiplier
        if v.get("prohibited_activities_multiplier", 1) < 1:
            raise ValueError("Prohibited activities multiplier must be at least 1")

        return v

    @classmethod
    def create_config(
        cls, name: str | None = None, **kwargs
    ) -> "KYCAgentConfiguration":
        """Factory method to create a KYC agent configuration

        Args:
            name: Optional name for the agent
            **kwargs: Additional configuration parameters

        Returns:
            Configured KYC agent configuration
        """
        # Generate a default name if not provided
        config_name = name or f"kyc_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create configuration
        config = cls(name=config_name, **kwargs)

        return config


"""
# Demonstration
def main():
    # Create a basic KYC agent configuration
    kyc_config = KYCAgentConfiguration.create_config(
        max_screening_iterations=4,
        compliance_checks={
            "politically_exposed_persons": True,
            "sanctions_screening": True,
            "adverse_media_check": True,
            "document_verification": True
        }
    )

    # Print configuration details
    print("KYC Agent Configuration:")
    print(kyc_config.model_dump_json(indent=2))

    # Derive the state schema
    state_schema = kyc_config.derive_schema()
    print("\nDerived State Schema:")
    print(state_schema)

if __name__ == "__main__":
    main()
"""
