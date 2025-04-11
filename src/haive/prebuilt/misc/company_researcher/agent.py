from typing import Dict, Any, List, Union, Optional
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.haive.core.engine.agent.agent import Agent, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig

# Import the configuration and state
from src.haive.prebuilt.misc.company_researcher.config import KYCAgentConfiguration
from src.haive.prebuilt.misc.company_researcher.state import (
    KYCWorkflowState, 
    KYCWorkflowStage, 
    KYCDecisionStatus
)

# Import models 
from src.haive.prebuilt.misc.company_researcher.models import (
    EnhancedKYCCustomerProfile, 
    ProhibitedActivity, 
    RestrictedIndustry
)

@register_agent(KYCAgentConfiguration)
class EnhancedKYCAgent(Agent[KYCAgentConfiguration]):
    """
    Advanced KYC Agent with comprehensive risk assessment workflow
    
    Implements a sophisticated multi-stage KYC processing pipeline:
    1. Initial Screening
    2. Risk Assessment
    3. Enhanced Due Diligence (if needed)
    4. Final Decision
    """
    
    def setup_workflow(self) -> None:
        """
        Configure the KYC workflow graph
        
        Stages:
        - Initial Screening
        - Risk Assessment
        - Enhanced Due Diligence (conditional)
        - Final Decision
        """
        # Add nodes for each stage of KYC process
        self.graph.add_node("initial_screening", self.initial_screening)
        self.graph.add_node("risk_assessment", self.risk_assessment)
        self.graph.add_node("enhanced_due_diligence", self.enhanced_due_diligence)
        self.graph.add_node("final_decision", self.final_decision)
        
        # Define workflow edges with conditional routing
        # Start with initial screening
        self.graph.add_edge(START, "initial_screening")
        
        # Route from initial screening to risk assessment
        self.graph.add_edge("initial_screening", "risk_assessment")
        
        # Conditional routing based on risk assessment
        self.graph.add_conditional_edges(
            "risk_assessment", 
            self.route_risk_assessment,
            {
                "enhanced_due_diligence": "enhanced_due_diligence",
                "final_decision": "final_decision"
            }
        )
        
        # Route from enhanced due diligence to final decision
        self.graph.add_edge("enhanced_due_diligence", "final_decision")
        
        # Final decision leads to END
        self.graph.add_edge("final_decision", END)
    
    def initial_screening(self, state: KYCWorkflowState) -> KYCWorkflowState:
        """
        Perform initial customer screening
        
        Args:
            state: Current workflow state
        
        Returns:
            Updated state with screening results
        """
        # Use the initial screening engine
        engine = self.config.compliance_engines.initial_screening
        
        # Prepare input messages
        input_messages = state.messages or [
            SystemMessage(content="Perform initial KYC screening"),
            HumanMessage(content="Please screen this customer profile")
        ]
        
        try:
            # Invoke the screening engine
            screening_result = engine.create_runnable().invoke({
                "messages": input_messages
            })
            
            # Update state with screening result
            state.customer_profile = screening_result
            state.messages.append(
                AIMessage(content="Initial Screening Completed")
            )
            state.update_stage(KYCWorkflowStage.RISK_ASSESSMENT)
            
            return state
        
        except Exception as e:
            # Log error if screening fails
            state.log_error({
                "stage": "initial_screening",
                "error_type": "screening_failure",
                "message": str(e)
            })
            return state
    
    def risk_assessment(self, state: KYCWorkflowState) -> KYCWorkflowState:
        """
        Assess customer risk based on initial screening
        
        Args:
            state: Current workflow state
        
        Returns:
            Updated state with risk assessment
        """
        # Extract customer profile
        if not state.customer_profile:
            state.log_error({
                "stage": "risk_assessment",
                "error_type": "no_profile",
                "message": "No customer profile available for risk assessment"
            })
            return state
        
        # Evaluate risk score
        risk_score = state.customer_profile.risk_profile.overall_risk_score
        
        # Determine routing based on risk thresholds
        thresholds = self.config.risk_score_thresholds
        
        # Add risk assessment message
        state.messages.append(
            AIMessage(content=f"Risk Score: {risk_score}")
        )
        
        # Determine next routing and decision status
        if risk_score >= thresholds['prohibited']:
            state.set_decision_status(KYCDecisionStatus.REJECTED)
            state.messages.append(
                AIMessage(content="PROHIBITED: Customer profile exceeds risk threshold")
            )
            state.next_stage = KYCWorkflowStage.FINAL_DECISION
        elif risk_score >= thresholds['high_risk']:
            state.messages.append(
                AIMessage(content="HIGH RISK: Enhanced Due Diligence Required")
            )
            state.next_stage = KYCWorkflowStage.ENHANCED_DUE_DILIGENCE
        else:
            state.set_decision_status(KYCDecisionStatus.APPROVED)
            state.messages.append(
                AIMessage(content="Risk Assessment Complete: Low Risk")
            )
            state.next_stage = KYCWorkflowStage.FINAL_DECISION
        
        # Update current stage
        state.update_stage(KYCWorkflowStage.RISK_ASSESSMENT)
        
        return state
    
    def route_risk_assessment(self, state: KYCWorkflowState) -> str:
        """
        Determine routing based on risk assessment
        
        Args:
            state: Current workflow state
        
        Returns:
            Next node in the workflow
        """
        if state.next_stage == KYCWorkflowStage.ENHANCED_DUE_DILIGENCE:
            return "enhanced_due_diligence"
        return "final_decision"
    
    def enhanced_due_diligence(self, state: KYCWorkflowState) -> KYCWorkflowStage:
        """
        Perform Enhanced Due Diligence for high-risk customers
        
        Args:
            state: Current workflow state
        
        Returns:
            Updated state with EDD results
        """
        # Ensure we haven't exceeded max screening iterations
        if state.screening_iterations >= self.config.max_screening_iterations:
            state.set_decision_status(KYCDecisionStatus.REJECTED)
            state.messages.append(
                AIMessage(content="REJECTED: Maximum screening iterations exceeded")
            )
            state.update_stage(KYCWorkflowStage.FINAL_DECISION)
            return state
        
        # Use the enhanced due diligence engine
        engine = self.config.compliance_engines.enhanced_due_diligence
        
        # Prepare input messages for enhanced due diligence
        edd_messages = state.messages + [
            SystemMessage(content="Initiating Enhanced Due Diligence (EDD)"),
            HumanMessage(content="Conduct comprehensive investigation for high-risk customer")
        ]
        
        try:
            # Invoke the EDD engine
            edd_result = engine.create_runnable().invoke({
                "messages": edd_messages
            })
            
            # Update customer profile with EDD findings
            state.customer_profile = self._merge_edd_results(
                state.customer_profile, 
                edd_result
            )
            
            # Add EDD messages
            state.messages.append(
                AIMessage(content="Enhanced Due Diligence Completed")
            )
            
            # Update stage and prepare for final decision
            state.update_stage(KYCWorkflowStage.ENHANCED_DUE_DILIGENCE)
            state.next_stage = KYCWorkflowStage.FINAL_DECISION
            
            return state
        
        except Exception as e:
            # Log error if EDD fails
            state.log_error({
                "stage": "enhanced_due_diligence",
                "error_type": "edd_failure",
                "message": str(e)
            })
            return state
    
    def final_decision(self, state: KYCWorkflowState) -> KYCWorkflowState:
        """
        Make final KYC decision based on all previous assessments
        
        Args:
            state: Current workflow state
        
        Returns:
            Final KYC decision state
        """
        # If decision already set by previous stages, finalize
        if state.decision_status != KYCDecisionStatus.PENDING:
            state.update_stage(KYCWorkflowStage.FINAL_DECISION)
            return state
        
        # Use the final risk assessment engine
        engine = self.config.compliance_engines.final_risk_assessment
        
        # Prepare final decision messages
        decision_messages = state.messages + [
            SystemMessage(content="Conducting Final Compliance Decision"),
            HumanMessage(content="Make final determination based on all collected information")
        ]
        
        try:
            # Invoke final assessment engine
            final_assessment = engine.create_runnable().invoke({
                "messages": decision_messages
            })
            
            # Merge final assessment with existing profile
            state.customer_profile = self._merge_edd_results(
                state.customer_profile, 
                final_assessment
            )
            
            # Determine final decision
            decision_outcome = self._determine_final_decision(state.customer_profile)
            
            # Update state with final decision
            state.messages.append(
                AIMessage(content="Final Compliance Decision Reached")
            )
            state.update_stage(KYCWorkflowStage.FINAL_DECISION)
            
            return state
        
        except Exception as e:
            # Log error if final decision fails
            state.log_error({
                "stage": "final_decision",
                "error_type": "decision_failure",
                "message": str(e)
            })
            return state
    
    def _merge_edd_results(
        self, 
        original_profile: EnhancedKYCCustomerProfile, 
        new_results: EnhancedKYCCustomerProfile
    ) -> EnhancedKYCCustomerProfile:
        """
        Merge results from different stages of KYC assessment
        
        Args:
            original_profile: Initial customer profile
            new_results: New assessment results
        
        Returns:
            Merged customer profile
        """
        # Create a copy of the original profile to avoid direct mutation
        merged_profile = original_profile.model_copy(deep=True)
        
        # Merge risk profile
        merged_profile.risk_profile.prohibited_activities.extend(
            set(new_results.risk_profile.prohibited_activities) - 
            set(merged_profile.risk_profile.prohibited_activities)
        )
        merged_profile.risk_profile.restricted_industries.extend(
            set(new_results.risk_profile.restricted_industries) - 
            set(merged_profile.risk_profile.restricted_industries)
        )
        merged_profile.risk_profile.compliance_risk_factors.extend(
            set(new_results.risk_profile.compliance_risk_factors) - 
            set(merged_profile.risk_profile.compliance_risk_factors)
        )
        
        # Recalculate risk score
        merged_profile.risk_profile.overall_risk_score = (
            merged_profile.risk_profile.overall_risk_score +
            new_results.risk_profile.overall_risk_score
        ) / 2
        
        # Update other fields
        merged_profile.last_updated = datetime.now()
        
        return merged_profile
    
    def _determine_final_decision(
        self, 
        final_profile: EnhancedKYCCustomerProfile
    ) -> KYCDecisionStatus:
        """
        Determine the final KYC decision based on comprehensive assessment
        
        Args:
            final_profile: Final customer profile after all assessments
        
        Returns:
            Final decision status
        """
        risk_score = final_profile.risk_profile.overall_risk_score
        thresholds = self.config.risk_score_thresholds
        
        # Check for absolute prohibitions
        if (final_profile.risk_profile.prohibited_activities or 
            any(RestrictedIndustry.PROHIBITED == ind for ind in final_profile.risk_profile.restricted_industries)):
            return KYCDecisionStatus.REJECTED
        
        # Determine decision based on risk score
        if risk_score >= thresholds['prohibited']:
            return KYCDecisionStatus.REJECTED
        elif risk_score >= thresholds['high_risk']:
            return KYCDecisionStatus.PENDING_REVIEW
        elif risk_score >= thresholds['medium_risk']:
            return KYCDecisionStatus.CONDITIONAL_APPROVAL
        else:
            return KYCDecisionStatus.APPROVED

# Example demonstration
def main():
    # Create a KYC agent configuration
    config = KYCAgentConfiguration.create_config(
        name="enhanced_kyc_agent",
        max_screening_iterations=3
    )
    
    # Create the agent
    kyc_agent = EnhancedKYCAgent(config=config)
    
    # Sample input data
    sample_input = KYCWorkflowState(
        messages=[
            HumanMessage(content="Bitfinity"),
            #SystemMessage(content="Customer from financial services industry")
        ]
    )
    
    # Run the KYC workflow
    result = kyc_agent.run(sample_input)
    
    # Display the result
    print("KYC Workflow Result:")
    print(result)

if __name__ == "__main__":
    main()