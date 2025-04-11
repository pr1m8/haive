from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.engine.aug_llm import AugLLMConfig

from src.haive.prebuilt.priv.kyc.prompts import (
    MAIN_SYSTEM_PROMPT,
    RESEARCH_SYSTEM_PROMPT,
    CUSTOMER_INFO_EXTRACTION_PROMPT,
    REPORT_PLANNING_PROMPT,
    QUERY_GENERATION_PROMPT,
    SECTION_WRITING_PROMPT,
    RISK_ASSESSMENT_PROMPT,
    FINAL_REPORT_COMPILATION_PROMPT
)

from src.haive.prebuilt.priv.kyc.models import CustomerRiskAssessmentModel, KYCDecisionModel

def create_base_llm_config(model_name: str = "gpt-4o", temperature: float = 0.2) -> AzureLLMConfig:
    """Create a base LLM configuration with the specified parameters"""
    return AzureLLMConfig(
        model=model_name,
        parameters={
            "temperature": temperature,
            "max_tokens": 4000
        }
    )

def create_kyc_engines(model_name: str = "gpt-4o") -> Dict[str, AugLLMConfig]:
    """Create all engines needed for KYC report generation"""
    
    engines = {}
    
    # Customer info extraction engine
    customer_info_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are an information extraction assistant that extracts structured data from unstructured text."),
        HumanMessage(content=CUSTOMER_INFO_EXTRACTION_PROMPT)
    ])
    
    engines["customer_info_extraction"] = AugLLMConfig(
        name="customer_info_extraction",
        llm_config=create_base_llm_config(model_name, 0.1),
        prompt_template=customer_info_template
    )
    
    # Report planning engine
    report_planning_template = ChatPromptTemplate.from_template(REPORT_PLANNING_PROMPT)
    
    engines["report_planning"] = AugLLMConfig(
        name="report_planning",
        llm_config=create_base_llm_config(model_name, 0.2),
        prompt_template=report_planning_template
    )
    
    # Query generation engine
    query_generation_template = ChatPromptTemplate.from_template(QUERY_GENERATION_PROMPT)
    
    engines["query_generation"] = AugLLMConfig(
        name="query_generation",
        llm_config=create_base_llm_config(model_name, 0.3),
        prompt_template=query_generation_template
    )
    
    # Section writing engine
    section_writing_template = ChatPromptTemplate.from_template(SECTION_WRITING_PROMPT)
    
    engines["section_writing"] = AugLLMConfig(
        name="section_writing",
        llm_config=create_base_llm_config(model_name, 0.2),
        prompt_template=section_writing_template
    )
    
    # Risk assessment engine
    risk_assessment_template = ChatPromptTemplate.from_template(RISK_ASSESSMENT_PROMPT)
    
    engines["risk_assessment"] = AugLLMConfig(
        name="risk_assessment",
        llm_config=create_base_llm_config(model_name, 0.1),
        prompt_template=risk_assessment_template,
        structured_output_model=CustomerRiskAssessmentModel
    )
    
    # KYC decision engine
    kyc_decision_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are a KYC compliance officer making decisions based on risk assessments.
        Your task is to determine whether to proceed with a customer based on their risk profile.
        You will be provided with a risk assessment and need to generate a decision with reasoning and required actions.
        """),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    engines["kyc_decision"] = AugLLMConfig(
        name="kyc_decision",
        llm_config=create_base_llm_config(model_name, 0.1),
        prompt_template=kyc_decision_template,
        structured_output_model=KYCDecisionModel
    )
    
    # Final report compilation engine
    final_report_template = ChatPromptTemplate.from_template(FINAL_REPORT_COMPILATION_PROMPT)
    
    engines["final_report_compilation"] = AugLLMConfig(
        name="final_report_compilation",
        llm_config=create_base_llm_config(model_name, 0.2),
        prompt_template=final_report_template
    )
    
    # Main engine
    main_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=MAIN_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    engines["main"] = AugLLMConfig(
        name="main",
        llm_config=create_base_llm_config(model_name, 0.2),
        prompt_template=main_template
    )
    
    return engines