import logging
import time
import json
import re
from typing import Any, Dict, Union, List, Optional, Tuple
from datetime import datetime
import os
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.documents import Document
from langgraph.graph import END, START
from langgraph.types import Command
from langgraph.pregel import RetryPolicy

from src.haive.core.engine.agent.agent import Agent, register_agent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from src.haive.core.graph.branches import Branch
from src.haive.core.engine.vectorstore import VectorStoreConfig
from src.haive.core.engine.aug_llm import compose_runnable
from src.haive.core.engine.retriever import create_retriever_from_vectorstore
from src.haive.agents.v2.config import ReactAgentConfig
from src.haive.agents.rag.base.config import BaseRAGConfig

# Import custom modules
from src.haive.prebuilt.priv.kyc.config import KYCReportConfig
from src.haive.prebuilt.priv.kyc.state import (
    KYCReportState, 
    CustomerInfo, 
    ReportSection, 
    WebSearchQuery
)
from src.haive.prebuilt.priv.kyc.models import (
    RiskCategory, 
    BusinessActivity, 
    ProhibitedActivity,
    CustomerRiskAssessmentModel, 
    KYCDecisionModel
)
from src.haive.prebuilt.priv.kyc.react_agent_config import create_kyc_rag_agent_config

logger = logging.getLogger(__name__)

@register_agent(KYCReportConfig)
class KYCReportAgent(Agent[KYCReportConfig]):
    """
    KYC Report Agent for comprehensive customer due diligence
    
    This agent implements a workflow to:
    1. Plan a KYC report based on customer information
    2. Research the company using web search and website scraping
    3. Analyze business activities and risk factors
    4. Generate a comprehensive KYC report with risk assessment
    """
    
    def __init__(self, config: KYCReportConfig):
        self._react_agent = None
        self._rag_agent = None
        self._vectorstore = None
        self._retriever = None
        super().__init__(config)
    
    @property
    def react_agent(self):
        """Lazy initialization of ReAct agent for research"""
        if self._react_agent is None and self.config.react_agent_name:
            try:
                # Import ReactAgent and ReactAgentConfig to ensure proper registration
                from src.haive.agents.v2.config import ReactAgentConfig
                from src.haive.agents.v2.agent import ReactAgent
                from src.haive.core.engine.agent.agent import AGENT_REGISTRY
                
                # Check if ReactAgentConfig is registered
                logger.info(f"Checking ReactAgentConfig registration, found: {ReactAgentConfig in AGENT_REGISTRY}")
                
                # Create a ReactAgent configuration with minimal required components
                # Avoid using components that may have compatibility issues
                react_config = ReactAgentConfig(
                    tools=[],  # Empty tools to avoid initialization errors
                    max_retries=3,  # Set max_retries in config instead of in RetryPolicy
                    retry_delay=1.0
                )
                
                # Register ReactAgent with ReactAgentConfig if not already registered
                if ReactAgentConfig not in AGENT_REGISTRY:
                    logger.warning("ReactAgentConfig not found in registry, registering ReactAgent manually")
                    AGENT_REGISTRY[ReactAgentConfig] = ReactAgent
                
                # Build the agent
                # Use a try-except block to handle potential RetryPolicy issues
                try:
                    self._react_agent = react_config.build_agent()
                    logger.info(f"Successfully built ReactAgent")
                except TypeError as e:
                    if "RetryPolicy.__new__() got an unexpected keyword argument" in str(e):
                        # Fix for RetryPolicy parameter mismatch
                        # Import the correct RetryPolicy
                        from src.haive.core.graph.retry import RetryPolicy
                        
                        # Create a compatible version of the agent
                        self._react_agent = ReactAgent(config=react_config)
                        
                        # If necessary, manually set up retry policy
                        self._react_agent.retry_policy = RetryPolicy(
                            max_retries=3,
                            delay=1.0,
                            errors_to_retry=["Exception"]
                        )
                        
                        logger.info(f"Successfully built ReactAgent with compatible RetryPolicy")
                    else:
                        raise
            except Exception as e:
                logger.error(f"Error initializing ReactAgent: {str(e)}")
                logger.error(f"Fallback to standard search without ReactAgent")
        
        return self._react_agent
    
    @property
    def rag_agent(self):
        """Lazy initialization of RAG agent for context retrieval"""
        if self._rag_agent is None:
            # Check if we have a vector store already set up
            if self.vectorstore:
                # Create RAG config with the existing vector store
                
                # Get the RAG engine name from config
                rag_engine = self.config.engines.get("rag_engine")
                if not rag_engine:
                    logger.warning("RAG engine not found in config")
                    return None
                
                # Create RAG agent config using the vectorstore
                rag_config = create_kyc_rag_agent_config(
                    vectorstore_config=self.config.vectorstore_config,
                    name=f"{self.config.name}_retrieval",
                    llm_model=rag_engine.llm_config.model if rag_engine.llm_config else "gpt-4o"
                )
                
                # Set the RAG agent name in the config
                self.config.rag_agent_name = rag_config.name
                
                # Build the RAG agent
                self._rag_agent = rag_config.build_agent()
            elif self.config.rag_agent_name:
                # If rag_agent_name is already set, try to get the config from registry
                from src.haive.agents.rag.llm_rag.config import LLMRAGConfig
                rag_config = LLMRAGConfig()
                
                if rag_config and isinstance(rag_config, LLMRAGConfig):
                    self._rag_agent = rag_config.build_agent()
                else:
                    logger.warning(f"RAG agent config '{self.config.rag_agent_name}' not found or not a LLMRAGConfig")
        
        return self._rag_agent
    
    @property
    def vectorstore(self):
        """Lazy initialization of vector store"""
        if self._vectorstore is None and self.config.vectorstore_config:
            self._vectorstore = self.config.vectorstore_config.create_vectorstore()
        return self._vectorstore
    
    @property
    def retriever(self):
        """Lazy initialization of retriever"""
        if self._retriever is None:
            if self.vectorstore:
                self._retriever = create_retriever_from_vectorstore(self.vectorstore)
            elif hasattr(self.config, 'retriever_config') and self.config.retriever_config:
                self._retriever = self.config.retriever_config.create_runnable()
        return self._retriever
    
    def setup_workflow(self) -> None:
        """Set up the KYC report generation workflow graph"""
        logger.info(f"Setting up workflow for KYCReportAgent {self.config.name}")
        
        # Create DynamicGraph with our engines
        engines = list(self.config.engines.values())
        gb = DynamicGraph(
            components=engines,
            state_schema=self.state_schema
        )
        
        # Add nodes for each step in the workflow
        gb.add_node("process_input", self.process_input)
        gb.add_node("initial_business_check", self.initial_business_check)
        gb.add_node("generate_report_plan", self.generate_report_plan)
        gb.add_node("human_feedback", self.process_human_feedback)
        gb.add_node("generate_queries", self.generate_search_queries)
        gb.add_node("search_web", self.search_web)
        gb.add_node("write_section", self.write_section)
        gb.add_node("gather_completed_sections", self.gather_completed_sections)
        gb.add_node("analyze_risk", self.analyze_risk)
        gb.add_node("write_final_sections", self.write_final_sections)
        gb.add_node("compile_final_report", self.compile_final_report)
        
        # Set up main flow with initial business check
        gb.add_edge("process_input", "initial_business_check")
        
        # Add conditional edge from initial business check
        gb.add_conditional_edges(
            "initial_business_check",
            self.check_early_rejection,
            {
                "immediate_rejection": "compile_final_report",
                "continue_assessment": "generate_report_plan"
            }
        )
        
        gb.add_edge("generate_report_plan", "human_feedback")
        
        # Define branch for section building
        gb.add_conditional_edges(
            "human_feedback",
            self.should_start_research,
            {
                "continue_research": "generate_queries",
                "skip_research": "gather_completed_sections"
            }
        )
        
        # Research flow
        gb.add_edge("generate_queries", "search_web")
        gb.add_edge("search_web", "write_section")
        
        # Define branch for more search or section completion
        gb.add_conditional_edges(
            "write_section",
            self.check_section_completion,
            {
                "need_more_search": "search_web",
                "section_complete": "generate_queries",
                "all_sections_complete": "gather_completed_sections" 
            }
        )
        
        # Final report generation
        gb.add_edge("gather_completed_sections", "analyze_risk")
        gb.add_edge("analyze_risk", "write_final_sections")
        gb.add_edge("write_final_sections", "compile_final_report")
        gb.add_edge("compile_final_report", END)
        
        # Set entry point
        gb.set_entry_point("process_input")
        
        # Build the graph
        self.graph = gb.build()
        
        logger.info(f"Workflow setup complete for {self.config.name}")
    
    def initial_business_check(self, state: KYCReportState) -> Command:
        """
        Perform an initial search to identify the business and check for immediate red flags
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with initial business information
        """
        try:
            # Get customer info
            customer_info = state.customer_info
            
            # Prepare immediate check message
            check_message = f"""
I'll conduct a quick initial verification for {customer_info.name} to check for any immediate concerns.
            """
            
            # Use a direct search for quick background check
            query = f"{customer_info.name} business activities regulatory issues compliance"
            
            logger.info(f"Performing initial business check for: {customer_info.name}")
            
            # Import search tool directly
            search_content = ""
            try:
                from src.haive.prebuilt.priv.kyc.structured_tools import tavily_search_context_func
                search_content = tavily_search_context_func(
                    query=query,
                    search_depth="basic",  # Use basic for faster results
                    max_results=3
                )
                logger.info(f"Initial search returned {len(search_content)} chars")
            except Exception as search_err:
                logger.error(f"Error in initial search: {str(search_err)}")
                search_content = f"Unable to perform initial verification search: {str(search_err)}"
            
            # Check for immediate red flags in the content
            is_prohibited = False
            prohibited_activities = []
            business_category = None
            
            # Check for prohibited activities in search results
            lower_content = search_content.lower()
            
            # Detect prohibited activities based on keywords
            prohibited_activities_map = {
                "arms_distribution": ["arms dealer", "weapons manufacturer", "military equipment supplier", "defense contractor"],
                "unlawful_drugs": ["illegal drugs", "narcotics trade", "drug trafficking", "illicit substances"],
                "adult_entertainment": ["adult entertainment", "pornography", "adult content provider"],
                "human_trafficking": ["human trafficking", "smuggling people"],
                "human_exploitation": ["exploitation", "forced labor", "child labor"],
                "unlawful_gambling": ["illegal gambling", "unlicensed betting", "gambling violations"],
                "unauthorized_virtual_currencies": ["unregulated crypto", "unlicensed virtual currency", "unauthorized crypto"],
                "unlicensed_msb": ["unlicensed money service", "unlicensed money transmitter", "unregistered msb"],
                "anonymous_accounts": ["anonymous accounts", "no kyc", "bypass verification"],
                "sanctioned_countries": ["sanctioned country", "Iran", "North Korea", "Cuba", "Syria", "economic sanctions"],
                "shell_banks": ["shell bank", "shell company", "no physical presence"]
            }
            
            # Check for prohibited activities in search content
            for activity, keywords in prohibited_activities_map.items():
                if any(keyword in lower_content for keyword in keywords):
                    prohibited_activities.append(activity)
                    is_prohibited = True
                    logger.info(f"Detected potential prohibited activity: {activity}")
            
            # Check for business type
            business_types = {
                "cryptocurrency_exchange": ["cryptocurrency exchange", "crypto exchange", "digital currency exchange", "bitcoin exchange"],
                "online_gambling": ["online gambling", "betting platform", "online casino", "sports betting"],
                "offshore_banking": ["offshore banking", "offshore financial", "tax haven"],
                "money_services_business": ["money service business", "money transmitter", "currency exchange"],
                "payment_processor": ["payment processor", "payment service provider", "payment gateway"],
                "crypto_mixer": ["crypto mixer", "bitcoin mixer", "cryptocurrency tumbler", "mixing service"]
            }
            
            for business_type, keywords in business_types.items():
                if any(keyword in lower_content for keyword in keywords):
                    business_category = business_type
                    logger.info(f"Detected business type: {business_type}")
                    break
            
            # Update customer info with findings
            if business_category and not customer_info.business_description:
                customer_info.business_description = business_category
            
            # For cryptocurrency exchanges, payment processors, and MSBs, check for regulatory compliance
            if business_category in ["cryptocurrency_exchange", "money_services_business", "payment_processor"]:
                # Check for regulatory issues in these high-risk businesses
                regulatory_issues = [
                    "regulatory action", "fined", "penalized", "investigation", 
                    "regulatory violation", "compliance failure", "unlicensed operation", 
                    "unregistered", "illegal operation", "sanctions violation"
                ]
                
                has_regulatory_issues = any(issue in lower_content for issue in regulatory_issues)
                if has_regulatory_issues:
                    detected_issues = [issue for issue in regulatory_issues if issue in lower_content]
                    logger.info(f"Detected regulatory issues: {', '.join(detected_issues)}")
            
            # If prohibited activities were found, create a risk assessment and decision to reject immediately
            if is_prohibited:
                from src.haive.prebuilt.priv.kyc.models import (
                    RiskCategory, 
                    BusinessActivity, 
                    ProhibitedActivity,
                    CustomerRiskAssessmentModel, 
                    KYCDecisionModel
                )
                
                # Create risk assessment for prohibited activities
                risk_assessment = CustomerRiskAssessmentModel(
                    customer_name=customer_info.name,
                    customer_type=customer_info.customer_type,
                    overall_risk_category=RiskCategory.HIGH_RISK,
                    primary_business_activity=business_category,
                    prohibited_activities=[ProhibitedActivity(p) for p in prohibited_activities],
                    is_politically_exposed=False,
                    additional_notes=f"Initial check detected prohibited activities: {', '.join(prohibited_activities)}"
                )
                
                # Create KYC decision
                kyc_decision = KYCDecisionModel(
                    risk_assessment=risk_assessment,
                    proceed=False
                )
                kyc_decision.required_actions = [
                    "Report to compliance officer immediately",
                    "Document all detected prohibited activities",
                    "Consider filing suspicious activity report",
                    "Document decision rationale in compliance system"
                ]
                kyc_decision.decision_reason = f"Initial verification detected prohibited activities: {', '.join(prohibited_activities)}"
                
                # Create message about immediate rejection
                rejection_message = f"""
Based on my initial verification, I've detected prohibited activities for {customer_info.name} that require immediate attention:

**Prohibited Activities Detected:** {', '.join(prohibited_activities)}

This customer appears to be involved in activities that are prohibited by our policies and regulations. A full KYC report is not recommended, and the customer should be rejected immediately.

**Risk Category:** HIGH RISK
**Decision:** DO NOT PROCEED
**Reason:** {kyc_decision.decision_reason}

**Required Actions:**
{chr(10).join(['- ' + action for action in kyc_decision.required_actions])}

This assessment requires immediate escalation according to our risk policies.
                """
                
                return Command(
                    update={
                        "customer_info": customer_info,
                        "risk_assessment": risk_assessment,
                        "kyc_decision": kyc_decision,
                        "risk_category": risk_assessment.overall_risk_category,
                        "business_activities": [business_category] if business_category else [],
                        "prohibited_activities": prohibited_activities,
                        "initial_verification_result": "prohibited_activities_detected",
                        "messages": list(state.messages) + [AIMessage(content=rejection_message)]
                    }
                )
            
            # If no prohibited activities, continue with summary of findings
            verification_message = f"""
Initial verification completed for {customer_info.name}.

**Business Category:** {business_category or "Not immediately identified"}
**Prohibited Activities:** None detected in initial check
**Next Steps:** Proceeding with full KYC assessment

I'll now create a detailed plan for the KYC report.
            """
            
            return Command(
                update={
                    "customer_info": customer_info,
                    "business_category": business_category,
                    "initial_verification_result": "no_immediate_concerns",
                    "messages": list(state.messages) + [AIMessage(content=verification_message)]
                }
            )
        
        except Exception as e:
            logger.error(f"Error in initial business check: {str(e)}")
            return Command(
                update={
                    "error": f"Error in initial business check: {str(e)}",
                    "messages": list(state.messages) + [
                        AIMessage(content=f"I encountered an error during initial verification: {str(e)}. I'll proceed with caution and conduct a full assessment.")
                    ]
                }
            )
    
    def check_early_rejection(self, state: KYCReportState) -> str:
        """
        Check if customer should be immediately rejected based on initial verification
        
        Args:
            state: Current agent state
            
        Returns:
            Routing decision: "immediate_rejection" or "continue_assessment"
        """
        # Check if we already have a KYC decision from initial verification
        if hasattr(state, "kyc_decision") and state.kyc_decision is not None:
            if not state.kyc_decision.proceed:
                logger.info("Early rejection detected, skipping full assessment")
                return "immediate_rejection"
        
        # Check if prohibited activities were detected
        if hasattr(state, "initial_verification_result") and state.initial_verification_result == "prohibited_activities_detected":
            return "immediate_rejection"
        
        # Continue with full assessment
        return "continue_assessment"
    
    def process_input(self, state: KYCReportState) -> Command:
        """
        Process the initial input and set up the customer information
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with customer info
        """
        logger.info("Processing input for KYC report")
        
        try:
            # Extract customer information from input
            messages = state.messages if hasattr(state, "messages") else []
            input_text = ""
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    input_text = msg.content
                    break
            
            if not input_text:
                raise ValueError("No input message found")
            
            # Get input context
            input_context = state.input_context if hasattr(state, "input_context") else None
            logger.info(f"Input context: {input_context}")
            
            # Use customer info extraction engine
            extraction_engine = self.config.engines.get("customer_info_extraction")
            if not extraction_engine:
                logger.warning("Customer info extraction engine not found, using main engine")
                extraction_engine = self.config.engine
                
            extraction_runnable = compose_runnable(extraction_engine)
            
            # Invoke the extraction with additional context if available
            extraction_prompt = {
                "input_text": input_text
            }
            
            if input_context:
                extraction_prompt["input_text"] += f"\n\nAdditional context: {input_context}"
                
            extraction_result = extraction_runnable.invoke(extraction_prompt)
            
            # Extract JSON from response
            if isinstance(extraction_result, str):
                customer_info_text = extraction_result
            elif isinstance(extraction_result, dict) and "content" in extraction_result:
                customer_info_text = extraction_result["content"]
            elif hasattr(extraction_result, "content"):
                customer_info_text = extraction_result.content
            else:
                customer_info_text = str(extraction_result)
            
            # Parse JSON from response text
            customer_info_dict = self._extract_json_from_text(customer_info_text)
            
            # Fallback if parsing fails
            if not customer_info_dict:
                logger.warning("Failed to parse JSON from extraction result, using fallback")
                
                # Try to find the company name using better parsing logic
                import re
                first_few_lines = "\n".join(input_text.split("\n")[:5])
                
                # Try to extract name using patterns:
                # 1. "KYC risk assessment for X"
                # 2. "X is a company/business"
                name_match = re.search(r'KYC (?:risk assessment|report) for ([^.\n]+)', first_few_lines, re.IGNORECASE)
                if not name_match:
                    name_match = re.search(r'([^.\n]+) is a (?:company|business|cryptocurrency|corporation|entity)', first_few_lines, re.IGNORECASE)
                
                if name_match:
                    customer_name = name_match.group(1).strip()
                else:
                    # Fallback to first line with simple cleanup
                    customer_name = input_text.split("\n")[0].replace("I need to do a KYC risk assessment for", "").strip()
                    if not customer_name:
                        customer_name = "Unknown Company"
                
                logger.info(f"Extracted customer name using fallback: {customer_name}")
                
                customer_info_dict = {
                    "name": customer_name,
                    "customer_type": "business" if "company" in input_text.lower() or "business" in input_text.lower() else "individual",
                    "website": re.search(r'(?:website|url)[^\n]*?(https?://[^\s,\n]+)', input_text, re.IGNORECASE).group(1) if re.search(r'(?:website|url)[^\n]*?(https?://[^\s,\n]+)', input_text, re.IGNORECASE) else None,
                    "business_description": re.search(r'is a ([^.]+)', input_text).group(1) if re.search(r'is a ([^.]+)', input_text) else None,
                    "additional_context": input_text
                }
            
            # Create CustomerInfo object
            customer_info = CustomerInfo(**customer_info_dict)
            
            # Generate report topic
            report_topic = f"KYC Risk Assessment Report for {customer_info.name}"
            logger.info(f"Generated report topic: {report_topic}")
            
            # Set up initial state with customer info
            return Command(
                update={
                    "customer_info": customer_info,
                    "report_topic": report_topic,
                    "input_context": input_context,
                    "current_step": "plan_report"
                }
            )
        
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            return Command(
                update={
                    "error": f"Error processing input: {str(e)}"
                }
            )
    
    def generate_report_plan(self, state: KYCReportState) -> Command:
        """
        Generate a plan for the KYC report with sections
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with report plan
        """
        logger.info(f"Generating report plan for {state.report_topic}")
        
        try:
            # Get customer info
            customer_info = state.customer_info
            
            # Start with default sections
            report_sections = []
            for section_info in self.config.default_report_sections:
                report_sections.append(ReportSection(**section_info))
            
            # Convert to JSON for the template
            initial_sections_json = json.dumps([{
                "name": s.name,
                "description": s.description,
                "requires_research": s.requires_research
            } for s in report_sections], indent=2)
            
            # Use report planning engine
            planning_engine = self.config.engines.get("report_planning")
            if not planning_engine:
                logger.warning("Report planning engine not found, using main engine")
                planning_engine = self.config.engine
                
            planning_runnable = compose_runnable(planning_engine)
            
            # Invoke the planning
            planning_result = planning_runnable.invoke({
                "customer_name": customer_info.name,
                "customer_type": customer_info.customer_type,
                "business_description": customer_info.business_description or "Not provided",
                "location": customer_info.location or "Not provided",
                "additional_context": state.input_context or "None provided",
                "initial_sections": initial_sections_json
            })
            
            # Extract plan from response
            if isinstance(planning_result, str):
                plan_text = planning_result
            elif isinstance(planning_result, dict) and "content" in planning_result:
                plan_text = planning_result["content"]
            elif hasattr(planning_result, "content"):
                plan_text = planning_result.content
            else:
                plan_text = str(planning_result)
            
            # Parse JSON from response
            sections_list = self._extract_json_from_text(plan_text)
            
            # Use original sections if parsing fails
            if not sections_list:
                logger.warning("Failed to parse JSON from planning result, using default sections")
                sections_list = [{
                    "name": s.name,
                    "description": s.description,
                    "requires_research": s.requires_research
                } for s in report_sections]
            
            # Create report sections
            updated_sections = []
            for section_data in sections_list:
                # Ensure required fields are present
                if "name" not in section_data or "description" not in section_data:
                    continue
                
                # Add requires_research if missing
                if "requires_research" not in section_data:
                    section_data["requires_research"] = True
                
                # Create section
                updated_sections.append(ReportSection(**section_data))
            
            # Generate AI message explaining the plan
            plan_explanation = f"""
I've created a plan for the KYC report on {customer_info.name}. The report will include the following sections:

{chr(10).join([f"- **{s.name}**: {s.description}" for s in updated_sections])}

We'll start by researching the company and gathering information for each section that requires research. Then we'll analyze the risk factors and generate a final risk assessment.
            """
            
            # Update messages to include the plan explanation
            messages = list(state.messages) if hasattr(state, "messages") else []
            messages.append(AIMessage(content=plan_explanation))
            
            # Update state with report sections and plan
            return Command(
                update={
                    "report_sections": updated_sections,
                    "messages": messages,
                    "current_step": "human_feedback"
                }
            )
        
        except Exception as e:
            logger.error(f"Error generating report plan: {str(e)}")
            return Command(
                update={
                    "error": f"Error generating report plan: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=f"Error generating report plan: {str(e)}")]
                }
            )
    
    def process_human_feedback(self, state: KYCReportState) -> Command:
        """
        Process feedback from the human on the report plan
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state based on feedback
        """
        logger.info("Processing human feedback on report plan")
        
        try:
            # Check for human feedback in the last message
            messages = state.messages if hasattr(state, "messages") else []
            if messages and isinstance(messages[-1], HumanMessage):
                feedback = messages[-1].content
                
                # Check if the feedback indicates changes to the plan
                if any(keyword in feedback.lower() for keyword in ["change", "modify", "update", "add", "remove"]):
                    # Use the main engine to process the feedback
                    feedback_processing = self.config.engine.create_runnable().invoke({
                        "messages": [
                            HumanMessage(content=f"""
                            The user has provided feedback on the KYC report plan: {feedback}
                            
                            Current report sections:
                            {json.dumps([s.dict() for s in state.report_sections], indent=2)}
                            
                            Please update the report sections based on this feedback. 
                            Respond with a JSON array of updated sections, each with 'name', 'description', and 'requires_research' fields.
                            """)
                        ]
                    })
                    
                    # Extract response
                    if isinstance(feedback_processing, AIMessage):
                        response_text = feedback_processing.content
                    elif isinstance(feedback_processing, str):
                        response_text = feedback_processing
                    elif isinstance(feedback_processing, dict) and "content" in feedback_processing:
                        response_text = feedback_processing["content"]
                    else:
                        response_text = str(feedback_processing)
                    
                    # Parse JSON from response
                    updated_sections_data = self._extract_json_from_text(response_text)
                    
                    # Update sections if parsing succeeded
                    if updated_sections_data:
                        updated_sections = []
                        for section_data in updated_sections_data:
                            if "name" not in section_data or "description" not in section_data:
                                continue
                                
                            if "requires_research" not in section_data:
                                section_data["requires_research"] = True
                                
                            updated_sections.append(ReportSection(**section_data))
                        
                        # Generate confirmation message
                        confirmation = f"""
I've updated the report plan based on your feedback. The report will now include these sections:

{chr(10).join([f"- **{s.name}**: {s.description}" for s in updated_sections])}

Let's proceed with the research for this report.
                        """
                        
                        return Command(
                            update={
                                "report_sections": updated_sections,
                                "messages": list(state.messages) + [AIMessage(content=confirmation)]
                            }
                        )
            
            # No changes needed or no feedback, proceed with research
            return Command(
                update={"current_step": "start_research"}
            )
        
        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            return Command(
                update={
                    "error": f"Error processing feedback: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=f"Error processing feedback: {str(e)}")]
                }
            )
    
    def should_start_research(self, state: KYCReportState) -> str:
        """
        Determine whether to start research or skip to final sections
        
        Args:
            state: Current agent state
            
        Returns:
            Routing decision: "continue_research" or "skip_research"
        """
        # Check if any sections require research
        research_sections = [s for s in state.report_sections if s.requires_research]
        
        if research_sections:
            # Set the first research section as current
            current_section_index = state.report_sections.index(research_sections[0])
            
            # Return routing decision with state update
            return "continue_research"
        else:
            # No sections require research, skip to gathering sections
            return "skip_research"
    
    def generate_search_queries(self, state: KYCReportState) -> Command:
        """
        Generate search queries for the current section
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with search queries
        """
        try:
            # Find next section that requires research
            research_sections = [
                (i, s) for i, s in enumerate(state.report_sections) 
                if s.requires_research and s.status != "completed"
            ]
            
            if not research_sections:
                # All research sections are complete
                return Command(
                    update={
                        "current_section_index": None,
                        "current_step": "gather_sections"
                    }
                )
            
            # Get the first incomplete section
            current_section_index, current_section = research_sections[0]
            
            # If section is already in progress, skip query generation
            if current_section.status == "in_progress" and current_section.queries:
                return Command(
                    update={
                        "current_section_index": current_section_index,
                        "query": current_section.queries[0].query
                    }
                )
            
            # Use query generation engine
            query_engine = self.config.engines.get("query_generation")
            if not query_engine:
                logger.warning("Query generation engine not found, using main engine")
                query_engine = self.config.engine
                
            query_runnable = compose_runnable(query_engine)
            
            # Get customer info
            customer_info = state.customer_info
            
            # Invoke the query generation
            result = query_runnable.invoke({
                "customer_name": customer_info.name,
                "business_description": customer_info.business_description or "Not provided",
                "location": customer_info.location or "Not provided",
                "section_name": current_section.name,
                "section_description": current_section.description,
                "num_queries": 3  # Generate 3 queries
            })
            
            # Extract queries from response
            if isinstance(result, str):
                query_text = result
            elif isinstance(result, dict) and "content" in result:
                query_text = result["content"]
            elif hasattr(result, "content"):
                query_text = result.content
            else:
                query_text = str(result)
            
            # Parse JSON from response
            queries_data = self._extract_json_from_text(query_text)
            
            # Create default queries if parsing fails
            if not queries_data:
                logger.warning("Failed to parse JSON from query generation result, using default queries")
                queries_data = [
                    {
                        "query": f"{customer_info.name} company information",
                        "purpose": "Get basic information about the company"
                    },
                    {
                        "query": f"{customer_info.name} business activities {current_section.name.lower()}",
                        "purpose": f"Research {current_section.name.lower()} information"
                    },
                    {
                        "query": f"{customer_info.name} risk factors {current_section.name.lower()}",
                        "purpose": f"Identify potential risk factors related to {current_section.name.lower()}"
                    }
                ]
            
            # Create WebSearchQuery objects
            search_queries = []
            for query_data in queries_data:
                if "query" not in query_data:
                    continue
                    
                if "purpose" not in query_data:
                    query_data["purpose"] = f"Research for {current_section.name}"
                    
                search_queries.append(WebSearchQuery(**query_data))
            
            # Update section
            current_section.status = "in_progress"
            current_section.queries = search_queries
            state.report_sections[current_section_index] = current_section
            
            # Select first query
            first_query = search_queries[0].query if search_queries else f"{customer_info.name} {current_section.name}"
            
            # Generate message about starting research
            research_message = f"""
I'll now research information for the "{current_section.name}" section. 

I've generated these search queries:
{chr(10).join([f"- {q.query} ({q.purpose})" for q in search_queries])}

Let me start searching for information...
            """
            
            return Command(
                update={
                    "report_sections": state.report_sections,
                    "current_section_index": current_section_index,
                    "query": first_query,
                    "messages": list(state.messages) + [AIMessage(content=research_message)],
                    "current_step": "search_web"
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating search queries: {str(e)}")
            return Command(
                update={
                    "error": f"Error generating search queries: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=f"Error generating search queries: {str(e)}")]
                }
            )
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """
        Extract JSON from a text string
        
        Args:
            text: Text containing JSON
            
        Returns:
            Parsed JSON as dict/list or None if extraction fails
        """
        # Try to find JSON using regex patterns
        # Pattern 1: ```json ... ```
        json_match = re.search(r'```(?:json)?\n(.*?)\n```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Pattern 2: Any JSON object/array
            json_match = re.search(r'({[\s\S]*}|\[[\s\S]*\])', text)
            if json_match:
                json_str = json_match.group(0)
            else:
                # No JSON found
                return None
        
        # Try to parse the JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Clean up the string and try again
            json_str = json_str.replace("'", '"')
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
    
    def search_web(self, state: KYCReportState) -> Command:
        """
        Search the web for information using ReactAgent
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with search results
        """
        try:
            # Get current section and query
            if state.current_section_index is None:
                raise ValueError("No current section index specified")
                
            current_section = state.report_sections[state.current_section_index]
            query = state.query
            
            if not query:
                # If no query is set, use a default query
                query = f"{state.customer_info.name} {current_section.name}"
            
            logger.info(f"Searching web for: {query}")
            
            # Initialize research_content variable
            research_content = ""
            
            # Use ReactAgent for research if available
            if self.react_agent:
                try:
                    # Run the ReactAgent with the query
                    logger.info(f"Running ReactAgent with query: {query}")
                    
                    # Get the customer website for deeper crawling if available
                    customer_website = state.customer_info.website if state.customer_info and state.customer_info.website else None
                    
                    # Prepare research instructions with website crawling if a website is available
                    research_instructions = f"Research the following information for a KYC report: {query}. Focus on accurate, factual information from reliable sources. Include any business activities, regulatory information, or risk factors that you find."
                    
                    if customer_website:
                        research_instructions += f" Additionally, use the recursive_url_loader tool to thoroughly crawl the company website at {customer_website} to extract detailed business information, activities, and any regulatory or compliance mentions."
                    
                    logger.info(f"Sending research instructions to ReactAgent: {research_instructions[:100]}...")
                    react_result = self.react_agent.run(research_instructions)
                    
                    # Extract search results from ReactAgent
                    if isinstance(react_result, dict) and "messages" in react_result:
                        # Get the last AI message from the result
                        react_messages = react_result["messages"]
                        last_ai_message = next((m for m in reversed(react_messages) if isinstance(m, AIMessage)), None)
                        
                        if last_ai_message:
                            research_content = last_ai_message.content
                        else:
                            research_content = str(react_result)
                    else:
                        research_content = str(react_result)
                        
                    logger.info(f"Successfully got research content from ReactAgent ({len(research_content)} chars)")
                except Exception as react_error:
                    # Log the error and fall back to direct tool use
                    logger.error(f"Error using ReactAgent: {str(react_error)}")
                    logger.info("Falling back to direct tool use")
                    research_content = self._fallback_search(query, state.customer_info)
            else:
                # Fallback to using search tools directly if ReactAgent not available
                logger.warning("ReactAgent not available, falling back to direct tool use")
                research_content = self._fallback_search(query, state.customer_info)
            
            # Create document from research content
            research_doc = Document(
                page_content=research_content,
                metadata={
                    "query": query,
                    "section": current_section.name,
                    "timestamp": time.time()
                }
            )
            
            # Update the retrieved documents
            retrieved_documents = list(state.retrieved_documents) if state.retrieved_documents else []
            retrieved_documents.append(research_doc)
            
            # Mark the query as completed in the current section
            for i, q in enumerate(current_section.queries):
                if q.query == query:
                    current_section.queries[i].completed = True
                    current_section.queries[i].results = [{"content": research_content}]
                    break
            
            # Update the section in the report_sections list
            updated_sections = list(state.report_sections)
            updated_sections[state.current_section_index] = current_section
            
            # Get the next query if any remain
            next_query = None
            for q in current_section.queries:
                if not q.completed:
                    next_query = q.query
                    break
            
            return Command(
                update={
                    "report_sections": updated_sections,
                    "retrieved_documents": retrieved_documents,
                    "query": next_query,  # Set next query or None if all done
                    "current_step": "write_section" if next_query is None else "search_web"
                }
            )
        
        except Exception as e:
            logger.error(f"Error searching web: {str(e)}")
            return Command(
                update={
                    "error": f"Error searching web: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=f"Error searching web: {str(e)}")]
                }
            )
    
    def _fallback_search(self, query: str, customer_info: CustomerInfo) -> str:
        """
        Fallback search implementation using direct tool calls
        
        Args:
            query: Search query
            customer_info: Customer information
            
        Returns:
            Research content as string
        """
        try:
            logger.info(f"Using fallback search for query: {query}")
            
            # Import tools directly
            from src.haive.prebuilt.priv.kyc.structured_tools import tavily_search_context_func, recursive_url_loader_func
            
            # First get general search results
            search_content = tavily_search_context_func(
                query=query,
                search_depth="advanced",
                topic="general",
                days=30,  # Look back 30 days for KYC research
                max_results=5
            )
            
            # Add website crawling if a website is available
            website_content = ""
            customer_website = customer_info.website if customer_info and customer_info.website else None
            
            if customer_website:
                try:
                    logger.info(f"Crawling customer website: {customer_website}")
                    
                    website_content = recursive_url_loader_func(
                        url=customer_website,
                        max_depth=2,
                        prevent_outside=True,
                        continue_on_failure=True
                    )
                    
                    # Combine web search and website content
                    research_content = f"Web Search Results:\n\n{search_content}\n\n" + \
                                       f"Company Website Analysis:\n\n{website_content}"
                except Exception as web_error:
                    logger.error(f"Error crawling website: {str(web_error)}")
                    research_content = search_content  # Fallback to search results only
            else:
                research_content = search_content
                
            logger.info(f"Fallback search complete, got {len(research_content)} chars")
            return research_content
            
        except Exception as fallback_error:
            logger.error(f"Error in fallback search: {str(fallback_error)}")
            # Return minimal content in case of complete failure
            return f"Failed to retrieve search results for: {query}. Please try a different search query."
    
    def write_section(self, state: KYCReportState) -> Command:
        """
        Write a section of the report based on research results
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with the written section
        """
        try:
            # Get current section
            if state.current_section_index is None:
                raise ValueError("No current section index specified")
                
            current_section = state.report_sections[state.current_section_index]
            
            # Collect research for this section
            research_content = []
            
            # Get all documents for this section
            for doc in state.retrieved_documents:
                if doc.metadata.get("section") == current_section.name:
                    research_content.append(doc.page_content)
            
            # Join research content
            research_context = "\n\n".join(research_content)
            
            # Use section writing engine
            section_engine = self.config.engines.get("section_writing")
            if not section_engine:
                logger.warning("Section writing engine not found, using main engine")
                section_engine = self.config.engine
                
            section_runnable = compose_runnable(section_engine)
            
            # Get customer info
            customer_info = state.customer_info
            
            # Invoke the section writing
            result = section_runnable.invoke({
                "section_name": current_section.name,
                "section_description": current_section.description,
                "customer_name": customer_info.name,
                "business_description": customer_info.business_description or "Not provided",
                "research_context": research_context,
                "risk_appetite_statement": self.config.risk_appetite_statement
            })
            
            # Extract section content from response
            if isinstance(result, str):
                section_content = result
            elif isinstance(result, dict) and "content" in result:
                section_content = result["content"]
            elif hasattr(result, "content"):
                section_content = result.content
            else:
                section_content = str(result)
            
            # Extract sources from content if possible
            sources = []
            sources_match = re.search(r'### Sources\s+([\s\S]+)', section_content)
            if sources_match:
                sources_text = sources_match.group(1)
                source_lines = sources_text.strip().split('\n')
                
                for line in source_lines:
                    source_match = re.search(r'\[(\d+)\]\s*([\w\s]+):\s*([\w\s]+),\s*line', line)
                    if source_match:
                        source_num = source_match.group(1)
                        source_title = source_match.group(2).strip()
                        source_url = source_match.group(3).strip()
                        sources.append({
                            "number": source_num,
                            "title": source_title,
                            "url": source_url
                        })
            
            # Update the section
            current_section.content = section_content
            current_section.sources = sources
            current_section.status = "completed"
            
            # Update the section in the report_sections list
            updated_sections = list(state.report_sections)
            updated_sections[state.current_section_index] = current_section
            
            # Generate message about completed section
            section_message = f"""
I've completed the research and writing for the "{current_section.name}" section.

Key findings:
{section_content[:300]}...

{len(sources)} sources were used in this research.
            """
            
            return Command(
                update={
                    "report_sections": updated_sections,
                    "messages": list(state.messages) + [AIMessage(content=section_message)],
                    "current_step": "check_completion"
                }
            )
            
        except Exception as e:
            logger.error(f"Error writing section: {str(e)}")
            return Command(
                update={
                    "error": f"Error writing section: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=f"Error writing section: {str(e)}")]
                }
            )
    
    def check_section_completion(self, state: KYCReportState) -> str:
        """
        Check if the current section is complete and determine next steps
        
        Args:
            state: Current agent state
            
        Returns:
            Routing decision: "need_more_search", "section_complete", or "all_sections_complete"
        """
        # Get current section
        if state.current_section_index is None:
            return "all_sections_complete"
            
        current_section = state.report_sections[state.current_section_index]
        
        # Check if current section needs more research
        if current_section.status != "completed":
            # Check if there are unfinished queries
            if any(not q.completed for q in current_section.queries):
                return "need_more_search"
            else:
                # All queries complete but section not marked complete
                return "section_complete"
        
        # Section is complete, check if there are more sections to research
        research_sections = [
            s for s in state.report_sections 
            if s.requires_research and s.status != "completed"
        ]
        
        if research_sections:
            return "section_complete"
        else:
            return "all_sections_complete"
    
    def gather_completed_sections(self, state: KYCReportState) -> Command:
        """
        Gather all completed sections and prepare for risk analysis
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with gathered sections
        """
        try:
            # Verify all research sections are complete
            incomplete_sections = [
                s.name for s in state.report_sections 
                if s.requires_research and s.status != "completed"
            ]
            
            if incomplete_sections:
                logger.warning(f"Some sections are still incomplete: {incomplete_sections}")
                
                # Send incomplete sections to research
                first_incomplete = next(
                    (i for i, s in enumerate(state.report_sections) 
                     if s.requires_research and s.status != "completed"), 
                    None
                )
                
                if first_incomplete is not None:
                    return Command(
                        update={
                            "current_section_index": first_incomplete,
                            "messages": list(state.messages) + [
                                AIMessage(content=f"I need to complete research for the '{state.report_sections[first_incomplete].name}' section.")
                            ]
                        },
                        goto="generate_queries"
                    )
            
            # All research sections complete, gather information for risk assessment
            completed_content = "\n\n".join([
                f"## {s.name}\n{s.content}" for s in state.report_sections if s.content
            ])
            
            # Prepare message about gathering sections
            gather_message = """
All sections of the report have been researched and drafted. Now I'll analyze the risk factors and generate a risk assessment for this customer.
            """
            
            return Command(
                update={
                    "messages": list(state.messages) + [AIMessage(content=gather_message)],
                    "current_step": "analyze_risk"
                }
            )
            
        except Exception as e:
            logger.error(f"Error gathering sections: {str(e)}")
            return Command(
                update={
                    "error": f"Error gathering sections: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=f"Error gathering sections: {str(e)}")]
                }
            )
    
    def analyze_risk(self, state: KYCReportState) -> Command:
        """
        Analyze risk factors and generate risk assessment
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with risk assessment
        """
        try:
            # Get completed sections content
            sections_content = "\n\n".join([
                f"## {s.name}\n{s.content}" for s in state.report_sections if s.content
            ])
            
            # Early detection of prohibited activities and high-risk indicators
            prohibited_activities = []
            is_high_risk = False
            business_activity = None
            
            # Check for immediate red flags in content
            lower_content = sections_content.lower()
            
            # Detect prohibited activities based on keywords
            prohibited_activities_map = {
                "arms_distribution": ["weapons", "arms dealer", "military equipment", "defense contractor"],
                "unlawful_drugs": ["illegal drugs", "narcotics", "drug trade", "illicit substances"],
                "adult_entertainment": ["adult entertainment", "adult content", "pornography"],
                "human_trafficking": ["human trafficking", "smuggling people"],
                "human_exploitation": ["exploitation", "forced labor", "child labor"],
                "unlawful_gambling": ["illegal gambling", "unlicensed gambling", "gambling violation"],
                "unauthorized_virtual_currencies": ["unregulated crypto", "unlicensed virtual currency", "unauthorized crypto"],
                "unlicensed_msb": ["unlicensed money service", "unlicensed money transmitter", "unregistered msb"],
                "anonymous_accounts": ["anonymous accounts", "no kyc", "bypass verification"],
                "shell_banks": ["shell bank", "shell company", "no physical presence"]
            }
            
            # Check for prohibited activities
            for activity, keywords in prohibited_activities_map.items():
                if any(keyword in lower_content for keyword in keywords):
                    prohibited_activities.append(activity)
                    is_high_risk = True
                    logger.info(f"Detected prohibited activity: {activity}")
            
            # Check for specific high-risk business types
            high_risk_businesses = {
                "cryptocurrency_exchange": ["cryptocurrency exchange", "crypto exchange", "digital currency exchange"],
                "online_gambling": ["online gambling", "betting platform", "casino"],
                "offshore_banking": ["offshore banking", "offshore financial", "tax haven"],
                "money_services_business": ["money service business", "money transmitter", "currency exchange"]
            }
            
            for business_type, keywords in high_risk_businesses.items():
                if any(keyword in lower_content for keyword in keywords):
                    business_activity = business_type
                    logger.info(f"Detected high-risk business type: {business_type}")
            
            # Check for regulatory issues
            regulatory_issues = ["regulatory action", "fined", "penalized", "investigation", "regulatory violation", 
                               "compliance failure", "unlicensed", "unregistered", "illegal operation"]
            
            has_regulatory_issues = any(issue in lower_content for issue in regulatory_issues)
            if has_regulatory_issues:
                logger.info("Detected regulatory issues in content")
                is_high_risk = True
            
            # If high risk detected, we can create a default risk assessment without calling the engine
            if is_high_risk and prohibited_activities:
                from src.haive.prebuilt.priv.kyc.models import (
                    RiskCategory, 
                    BusinessActivity, 
                    ProhibitedActivity,
                    CustomerRiskAssessmentModel, 
                    KYCDecisionModel
                )
                
                # Get customer info
                customer_info = state.customer_info
                
                # Create a default high-risk assessment
                risk_assessment = CustomerRiskAssessmentModel(
                    customer_name=customer_info.name,
                    customer_type=customer_info.customer_type,
                    overall_risk_category=RiskCategory.HIGH_RISK,
                    business_activities=[business_activity or "other"],
                    prohibited_activities=[ProhibitedActivity(p) for p in prohibited_activities],
                    is_politically_exposed=False,
                    additional_notes=f"High-risk assessment due to detected prohibited activities: {', '.join(prohibited_activities)}"
                )
                
                # Generate KYC decision based on risk assessment
                kyc_decision = KYCDecisionModel(
                    risk_assessment=risk_assessment,
                    proceed=False  # Default to not proceeding for high-risk with prohibited activities
                )
                kyc_decision.required_actions = [
                    "Report to compliance officer immediately",
                    "Document all detected prohibited activities",
                    "Consider filing suspicious activity report",
                    "Document decision rationale in compliance system"
                ]
                kyc_decision.decision_reason = f"Customer engages in prohibited activities: {', '.join(prohibited_activities)}"
                
                # Create message about immediate risk assessment
                risk_message = f"""
Based on my research, I've detected prohibited activities for {customer_info.name} that require immediate attention:

**Risk Category:** {risk_assessment.overall_risk_category}

**Key Risk Factors:**
- {"Business Activity: " + str(business_activity) if business_activity else "Business activities were analyzed"}
- **Prohibited Activities:** {', '.join([str(a) for a in prohibited_activities])}
- {f"Regulatory issues detected: {', '.join(issue for issue in regulatory_issues if issue in lower_content)}" if has_regulatory_issues else "No specific regulatory issues identified"}

**Decision:** DO NOT PROCEED

**Reason:** {kyc_decision.decision_reason}

**Required Actions:**
{chr(10).join(['- ' + action for action in kyc_decision.required_actions])}

This assessment requires immediate escalation according to our risk policies.
                """
                
                return Command(
                    update={
                        "risk_assessment": risk_assessment,
                        "kyc_decision": kyc_decision,
                        "risk_category": risk_assessment.overall_risk_category,
                        "business_activities": [business_activity] if business_activity else [],
                        "prohibited_activities": prohibited_activities,
                        "messages": list(state.messages) + [AIMessage(content=risk_message)],
                        "current_step": "write_final"
                    }
                )
            
            # Use risk assessment engine
            risk_engine = self.config.engines.get("risk_assessment")
            if not risk_engine:
                logger.warning("Risk assessment engine not found, using main engine")
                risk_engine = self.config.engine
                
            risk_runnable = compose_runnable(risk_engine)
            
            # Get customer info
            customer_info = state.customer_info
            
            # Invoke the risk assessment
            result = risk_runnable.invoke({
                "customer_name": customer_info.name,
                "customer_type": customer_info.customer_type,
                "business_description": customer_info.business_description or "Not provided",
                "report_findings": sections_content,
                "risk_appetite_statement": self.config.risk_appetite_statement
            })
            
            # Process result based on whether we got a structured output
            from src.haive.prebuilt.priv.kyc.models import (
                RiskCategory, 
                BusinessActivity, 
                ProhibitedActivity,
                CustomerRiskAssessmentModel, 
                KYCDecisionModel
            )
            
            if isinstance(result, CustomerRiskAssessmentModel):
                risk_assessment = result
            elif isinstance(result, dict) and all(hasattr(CustomerRiskAssessmentModel, k) for k in result.keys()):
                risk_assessment = CustomerRiskAssessmentModel(**result)
            else:
                # Try to extract JSON from text result
                if isinstance(result, str):
                    result_text = result
                elif isinstance(result, dict) and "content" in result:
                    result_text = result["content"]
                elif hasattr(result, "content"):
                    result_text = result.content
                else:
                    result_text = str(result)
                
                # Extract JSON
                risk_data = self._extract_json_from_text(result_text)
                
                if risk_data:
                    # Convert string values to enum values for prohibited activities
                    if "prohibited_activities" in risk_data and risk_data["prohibited_activities"]:
                        processed_activities = []
                        for activity in risk_data["prohibited_activities"]:
                            try:
                                # Attempt to convert to the correct enum value
                                if isinstance(activity, str):
                                    # Map similar terms to valid enum values
                                    activity_mapping = {
                                        "unregulated_virtual_currencies": "unauthorized_virtual_currencies",
                                        "illegal_drugs": "unlawful_drugs",
                                        "illegal_gambling": "unlawful_gambling"
                                    }
                                    if activity in activity_mapping:
                                        activity = activity_mapping[activity]
                                    
                                    # Verify it's a valid enum value
                                    if activity in [p.value for p in ProhibitedActivity]:
                                        processed_activities.append(activity)
                                    else:
                                        logger.warning(f"Invalid prohibited activity value: {activity}, skipping")
                                else:
                                    # Already a valid enum or other object
                                    processed_activities.append(activity)
                            except Exception as enum_err:
                                logger.error(f"Error processing prohibited activity: {str(enum_err)}")
                                
                        risk_data["prohibited_activities"] = processed_activities
                        
                    # Create the risk assessment model
                    try:
                        risk_assessment = CustomerRiskAssessmentModel(**risk_data)
                    except Exception as model_err:
                        logger.error(f"Error creating risk assessment model: {str(model_err)}")
                        # Fallback to default
                        risk_assessment = self._create_default_risk_assessment(customer_info, business_activity)
                else:
                    # Create a minimal risk assessment
                    risk_assessment = self._create_default_risk_assessment(customer_info, business_activity)
            
            # Generate KYC decision based on risk assessment
            kyc_decision = KYCDecisionModel(
                risk_assessment=risk_assessment,
                proceed=True  # Set a default value that will be updated by generate_decision
            )
            kyc_decision.generate_decision()
            
            # Create message about risk assessment
            risk_message = f"""
Based on my research, I've completed a risk assessment for {customer_info.name}:

**Risk Category:** {risk_assessment.overall_risk_category}

**Key Risk Factors:**
- {"Primary Business Activity: " + str(risk_assessment.primary_business_activity) if risk_assessment.primary_business_activity else "Business activities were analyzed"}
- {"Prohibited Activities: " + ", ".join([str(a) for a in risk_assessment.prohibited_activities]) if risk_assessment.prohibited_activities else "No prohibited activities identified"}
- {"PEP Status: The customer is a politically exposed person" if risk_assessment.is_politically_exposed else "No PEP concerns identified"}

**Decision:** {"Proceed" if kyc_decision.proceed else "Do Not Proceed"}

**Reason:** {kyc_decision.decision_reason}

**Required Actions:**
{chr(10).join(['- ' + action for action in kyc_decision.required_actions])}
            """
            
            return Command(
                update={
                    "risk_assessment": risk_assessment,
                    "kyc_decision": kyc_decision,
                    "risk_category": risk_assessment.overall_risk_category,
                    "business_activities": [risk_assessment.primary_business_activity] if risk_assessment.primary_business_activity else [],
                    "prohibited_activities": risk_assessment.prohibited_activities,
                    "messages": list(state.messages) + [AIMessage(content=risk_message)],
                    "current_step": "write_final"
                }
            )
            
        except Exception as e:
            logger.error(f"Error analyzing risk: {str(e)}")
            
            # Create fallback risk assessment in case of error
            from src.haive.prebuilt.priv.kyc.models import (
                RiskCategory, 
                CustomerRiskAssessmentModel, 
                KYCDecisionModel
            )
            
            # Get customer info
            customer_info = state.customer_info
            
            # Create default risk assessment
            risk_assessment = self._create_default_risk_assessment(customer_info)
            
            # Create default decision
            kyc_decision = KYCDecisionModel(
                risk_assessment=risk_assessment,
                proceed=False
            )
            kyc_decision.required_actions = [
                "Additional enhanced due diligence required",
                "Manual review by compliance team",
                "Verification of business activities"
            ]
            kyc_decision.decision_reason = "Error in risk assessment process. Manual review required."
            
            error_message = f"""
An error occurred during risk assessment: {str(e)}

As a precaution, I've assigned a high-risk rating to {customer_info.name}.

**Risk Category:** {risk_assessment.overall_risk_category}

**Decision:** DO NOT PROCEED until manual review

**Required Actions:**
{chr(10).join(['- ' + action for action in kyc_decision.required_actions])}
            """
            
            return Command(
                update={
                    "risk_assessment": risk_assessment,
                    "kyc_decision": kyc_decision,
                    "risk_category": risk_assessment.overall_risk_category,
                    "business_activities": [],
                    "prohibited_activities": [],
                    "error": f"Error analyzing risk: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=error_message)],
                    "current_step": "write_final"
                }
            )
    
    def _create_default_risk_assessment(self, customer_info, business_activity=None):
        """Create a default risk assessment when normal processing fails"""
        from src.haive.prebuilt.priv.kyc.models import (
            RiskCategory, 
            BusinessActivity, 
            CustomerRiskAssessmentModel
        )
        
        # Always default to high risk when uncertain
        return CustomerRiskAssessmentModel(
            customer_name=customer_info.name,
            customer_type=customer_info.customer_type,
            overall_risk_category=RiskCategory.HIGH_RISK,
            primary_business_activity=business_activity,
            prohibited_activities=[],
            is_politically_exposed=False,
            additional_notes="Risk assessment was created with default values due to processing errors. Manual review recommended."
        )
    
    def write_final_sections(self, state: KYCReportState) -> Command:
        """
        Write the executive summary and recommendations sections
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with final sections
        """
        try:
            # Get all section content
            sections_content = {}
            for section in state.report_sections:
                sections_content[section.name] = section.content
            
            # Get risk assessment and decision
            risk_assessment = state.risk_assessment
            kyc_decision = state.kyc_decision
            
            # Find executive summary and recommendations sections
            exec_summary_section = next((s for s in state.report_sections if s.name == "Executive Summary"), None)
            recommendations_section = next((s for s in state.report_sections if s.name == "Recommendations"), None)
            
            # Use main engine for final sections
            engine = self.config.engine
                
            # Get customer info
            customer_info = state.customer_info
            
            # For the executive summary
            if exec_summary_section:
                # Create a custom prompt for executive summary
                summary_prompt = f"""
                Write an executive summary for a KYC risk assessment report.
                
                Customer: {customer_info.name}
                Customer Type: {customer_info.customer_type}
                Business Description: {customer_info.business_description or "Not provided"}
                Risk Category: {risk_assessment.overall_risk_category}
                Decision: {"Proceed" if kyc_decision.proceed else "Do Not Proceed"}
                
                The summary should be concise (150-200 words) and highlight:
                1. Key business information
                2. Main risk factors identified
                3. Overall risk determination
                4. Decision rationale
                
                Format as professional business writing with a ## Executive Summary heading.
                """
                
                # Invoke for executive summary
                summary_result = engine.create_runnable().invoke({
                    "messages": [HumanMessage(content=summary_prompt)]
                })
                
                # Extract content
                if isinstance(summary_result, AIMessage):
                    summary_content = summary_result.content
                elif isinstance(summary_result, str):
                    summary_content = summary_result
                elif isinstance(summary_result, dict) and "content" in summary_result:
                    summary_content = summary_result["content"]
                else:
                    summary_content = str(summary_result)
                
                # Update section
                exec_summary_section.content = summary_content
                exec_summary_section.status = "completed"
                
                # Update in sections list
                for i, s in enumerate(state.report_sections):
                    if s.name == "Executive Summary":
                        state.report_sections[i] = exec_summary_section
                        break
            
            # For the recommendations section
            if recommendations_section:
                # Create a custom prompt for recommendations
                recommendations_prompt = f"""
                Write a recommendations section for a KYC risk assessment report.
                
                Customer: {customer_info.name}
                Risk Category: {risk_assessment.overall_risk_category}
                Required Actions: {", ".join(kyc_decision.required_actions)}
                Decision: {"Proceed" if kyc_decision.proceed else "Do Not Proceed"}
                Decision Reason: {kyc_decision.decision_reason}
                
                The recommendations should:
                1. List specific actions required based on the risk assessment
                2. Provide clear guidance for compliance staff
                3. Reference company risk appetite where relevant
                
                Format with a ## Recommendations heading and use bullet points for key actions.
                """
                
                # Invoke for recommendations
                recommendations_result = engine.create_runnable().invoke({
                    "messages": [HumanMessage(content=recommendations_prompt)]
                })
                
                # Extract content
                if isinstance(recommendations_result, AIMessage):
                    recommendations_content = recommendations_result.content
                elif isinstance(recommendations_result, str):
                    recommendations_content = recommendations_result
                elif isinstance(recommendations_result, dict) and "content" in recommendations_result:
                    recommendations_content = recommendations_result["content"]
                else:
                    recommendations_content = str(recommendations_result)
                
                # Update section
                recommendations_section.content = recommendations_content
                recommendations_section.status = "completed"
                
                # Update in sections list
                for i, s in enumerate(state.report_sections):
                    if s.name == "Recommendations":
                        state.report_sections[i] = recommendations_section
                        break
            
            # Message about final sections
            final_sections_message = """
I've completed the Executive Summary and Recommendations sections based on the risk assessment.
Now I'll compile the complete report.
            """
            
            return Command(
                update={
                    "report_sections": state.report_sections,
                    "messages": list(state.messages) + [AIMessage(content=final_sections_message)],
                    "current_step": "compile_report"
                }
            )
            
        except Exception as e:
            logger.error(f"Error writing final sections: {str(e)}")
            return Command(
                update={
                    "error": f"Error writing final sections: {str(e)}",
                    "messages": list(state.messages) + [AIMessage(content=f"Error writing final sections: {str(e)}")]
                }
            )
    
    def compile_final_report(self, state: KYCReportState) -> Command:
        """
        Compile the final KYC report and save it to a markdown file
        
        Args:
            state: Current agent state
            
        Returns:
            Command for updating state with final report
        """
        try:
            # Get all completed sections
            section_contents = []
            
            # Order sections logically
            ordered_section_names = [
                "Executive Summary",
                "Company Information", 
                "Business Activities Analysis",
                "Corporate Structure",  # Optional
                "Regulatory Compliance",
                "Industry Risk Assessment",  # Optional
                "Negative News Screening",
                "Risk Assessment",
                "Recommendations"
            ]
            
            # Add sections in proper order
            for section_name in ordered_section_names:
                section = next((s for s in state.report_sections if s.name == section_name), None)
                if section and section.content:
                    section_contents.append(section.content)
            
            # Add any remaining sections not in the ordered list
            for section in state.report_sections:
                if section.name not in ordered_section_names and section.content:
                    section_contents.append(section.content)
            
            # Create the complete report content
            customer_info = state.customer_info
            
            # Handle potentially missing risk_assessment and kyc_decision
            if not hasattr(state, "risk_assessment") or state.risk_assessment is None:
                from src.haive.prebuilt.priv.kyc.models import (
                    RiskCategory, 
                    CustomerRiskAssessmentModel, 
                    KYCDecisionModel
                )
                # Create default risk assessment
                risk_assessment = self._create_default_risk_assessment(customer_info)
                kyc_decision = KYCDecisionModel(
                    risk_assessment=risk_assessment,
                    proceed=False
                )
                kyc_decision.required_actions = [
                    "Additional enhanced due diligence required",
                    "Manual review by compliance team"
                ]
                kyc_decision.decision_reason = "No proper risk assessment completed. Manual review required."
                
                # Update state with the created values
                state.risk_assessment = risk_assessment
                state.kyc_decision = kyc_decision
                state.risk_category = risk_assessment.overall_risk_category
            else:
                risk_assessment = state.risk_assessment
                kyc_decision = state.kyc_decision
            
            # Create a title and metadata section
            report_title = f"# KYC Risk Assessment Report: {customer_info.name}"
            
            metadata_section = f"""
**Report Date:** {time.strftime("%Y-%m-%d")}
**Customer Type:** {customer_info.customer_type}
**Risk Category:** {risk_assessment.overall_risk_category}
**KYC Decision:** {"Proceed" if kyc_decision.proceed else "Do Not Proceed"}
            """
            
            # Join all content
            report_content = "\n\n".join([
                report_title,
                metadata_section,
                *section_contents
            ])
            
            # Save the report to a markdown file
            try:
                import os
                from pathlib import Path
                
                # Create reports directory if it doesn't exist
                reports_dir = Path("reports")
                reports_dir.mkdir(exist_ok=True)
                
                # Create a safe filename
                safe_name = customer_info.name.replace(" ", "_").replace("/", "_").replace("\\", "_")
                filename = f"reports/kyc_report_{safe_name}_{time.strftime('%Y%m%d_%H%M%S')}.md"
                
                # Write the report to file
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(report_content)
                
                logger.info(f"KYC report saved to {filename}")
                
                # Add to the message
                report_saved_message = f"The KYC report has been saved to {filename}"
            except Exception as file_error:
                logger.error(f"Error saving report to file: {str(file_error)}")
                report_saved_message = f"Error saving report to file: {str(file_error)}"
            
            # Generate message with final report
            final_report_message = f"""
I've completed the KYC Risk Assessment Report for {customer_info.name}.

**Risk Category:** {risk_assessment.overall_risk_category}
**KYC Decision:** {"Proceed" if kyc_decision.proceed else "Do Not Proceed"}

{report_saved_message}
            """
            
            # Return command with all required output fields
            updated_messages = list(state.messages) + [AIMessage(content=final_report_message)]
            return Command(
                update={
                    # Required output fields 
                    "final_report": report_content,
                    "risk_assessment": risk_assessment,
                    "kyc_decision": kyc_decision,
                    "risk_category": risk_assessment.overall_risk_category,
                    "business_activities": getattr(state, "business_activities", []),
                    "prohibited_activities": getattr(state, "prohibited_activities", []),
                    "messages": updated_messages,
                    
                    # State management field
                    "current_step": "completed"
                }
            )
            
        except Exception as e:
            logger.error(f"Error compiling final report: {str(e)}")
            
            # Create an emergency fallback report with minimal information
            try:
                from src.haive.prebuilt.priv.kyc.models import (
                    RiskCategory, 
                    CustomerRiskAssessmentModel, 
                    KYCDecisionModel
                )
                
                # Get customer info
                customer_info = state.customer_info
                
                # Create default risk assessment
                risk_assessment = CustomerRiskAssessmentModel(
                    customer_name=customer_info.name,
                    customer_type=customer_info.customer_type,
                    overall_risk_category=RiskCategory.HIGH_RISK,
                    prohibited_activities=[],
                    is_politically_exposed=False,
                    additional_notes="Error occurred during report generation. Manual review required."
                )
                
                # Create KYC decision
                kyc_decision = KYCDecisionModel(
                    risk_assessment=risk_assessment,
                    proceed=False
                )
                kyc_decision.required_actions = [
                    "Manual review required due to error in report generation",
                    "Verify customer information manually",
                    "Document decision rationale in compliance system"
                ]
                kyc_decision.decision_reason = "Error in report generation process. Manual review required."
                
                # Create minimal report content
                minimal_report = f"""
# Emergency KYC Risk Assessment Report: {customer_info.name}

**Report Date:** {time.strftime("%Y-%m-%d")}
**Customer Type:** {customer_info.customer_type}
**Risk Category:** {risk_assessment.overall_risk_category}
**KYC Decision:** Do Not Proceed

## Error Information
An error occurred during the report generation process: {str(e)}

## Recommendations
- Manual review required
- Verify customer information manually
- Document decision rationale in compliance system
                """
                
                # Save the emergency report
                import os
                from pathlib import Path
                
                # Create reports directory if it doesn't exist
                reports_dir = Path("reports")
                reports_dir.mkdir(exist_ok=True)
                
                # Create a safe filename
                safe_name = customer_info.name.replace(" ", "_").replace("/", "_").replace("\\", "_")
                filename = f"reports/EMERGENCY_kyc_report_{safe_name}_{time.strftime('%Y%m%d_%H%M%S')}.md"
                
                # Write the report to file
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(minimal_report)
                
                emergency_msg = f"An emergency minimal report has been saved to {filename}"
                logger.info(emergency_msg)
                
                error_message = f"""
Error compiling final report: {str(e)}

As a precaution, I've created an emergency minimal report with HIGH RISK rating.
{emergency_msg}
                """
                
                return Command(
                    update={
                        "risk_assessment": risk_assessment,
                        "kyc_decision": kyc_decision,
                        "risk_category": risk_assessment.overall_risk_category,
                        "final_report": minimal_report,
                        "error": f"Error compiling final report: {str(e)}",
                        "messages": list(state.messages) + [AIMessage(content=error_message)]
                    }
                )
                
            except Exception as emergency_error:
                # If even the emergency report creation fails
                error_message = f"Critical error: Failed to create even an emergency report: {str(emergency_error)}"
                logger.critical(error_message)
                
                return Command(
                    update={
                        "error": error_message,
                        "messages": list(state.messages) + [AIMessage(content=error_message)]
                    }
                )
                
    def generate_markdown_report(self, state: Dict[str, Any]) -> str:
        """Generate a markdown report from the final state."""
        # If we already have a final report, return it
        if state.get("final_report"):
            return state["final_report"]
        
        # Otherwise, generate a report from the state
        report = []
        report.append("# KYC Report\n")
        
        # Add customer info
        if state.get("customer_info"):
            report.append("## Customer Information\n")
            customer = state["customer_info"]
            report.append(f"**Name:** {customer.get('name', 'Unknown')}\n")
            report.append(f"**Type:** {customer.get('customer_type', 'Unknown')}\n")
            if customer.get("website"):
                report.append(f"**Website:** {customer.get('website')}\n")
            if customer.get("location"):
                report.append(f"**Location:** {customer.get('location')}\n")
            if customer.get("business_description"):
                report.append(f"**Business Description:** {customer.get('business_description')}\n")
            report.append("\n")
        
        # Add report sections
        if state.get("report_sections"):
            for section in state["report_sections"]:
                report.append(f"## {section.get('name')}\n")
                report.append(f"{section.get('content', 'No content available.')}\n\n")
        
        # Add risk assessment
        if state.get("risk_assessment"):
            report.append("## Risk Assessment\n")
            risk = state["risk_assessment"]
            report.append(f"**Overall Risk Category:** {state.get('risk_category', 'Unknown')}\n")
            
            if risk.get("assessment_factors"):
                report.append("\n### Assessment Factors\n")
                for factor, details in risk.get("assessment_factors", {}).items():
                    report.append(f"**{factor}**: {details.get('rating', 'Unknown')} - {details.get('justification', 'No justification provided.')}\n")
            
            report.append("\n")
        
        # Add business activities
        if state.get("business_activities"):
            report.append("## Business Activities\n")
            for activity in state["business_activities"]:
                report.append(f"- **{activity.get('activity')}**: {activity.get('description')}\n")
            report.append("\n")
        
        # Add prohibited activities
        if state.get("prohibited_activities"):
            report.append("## Prohibited Activities\n")
            for activity in state["prohibited_activities"]:
                report.append(f"- **{activity.get('activity')}**: {activity.get('description')}\n")
            report.append("\n")
        
        # Add decision
        if state.get("kyc_decision"):
            report.append("## KYC Decision\n")
            decision = state["kyc_decision"]
            report.append(f"**Decision:** {decision.get('decision', 'No decision')}\n")
            report.append(f"**Justification:** {decision.get('justification', 'No justification provided.')}\n")
            if decision.get("conditions"):
                report.append("\n### Conditions\n")
                for condition in decision.get("conditions", []):
                    report.append(f"- {condition}\n")
            report.append("\n")
        
        return "".join(report)

    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current KYC report state in a readable format.

        Args:
            state (Dict[str, Any]): Current KYC report state.
        """
        print("\n" + "=" * 50)
        print("KYC REPORT STATE VISUALIZATION")
        print("=" * 50)

        # Display current step in the workflow
        print(f"\n🔄 Current Step: {state.get('current_step', 'Unknown')}")
        
        # Display customer information
        if state.get("customer_info"):
            customer = state["customer_info"]
            print("\n📋 Customer Information:")
            print(f"   Name: {customer.get('name', 'Unknown')}")
            print(f"   Type: {customer.get('customer_type', 'Unknown')}")
            if customer.get("website"):
                print(f"   Website: {customer.get('website')}")
            if customer.get("location"):
                print(f"   Location: {customer.get('location')}")

        # Display report progress
        if state.get("report_sections"):
            print("\n📊 Report Progress:")
            sections_completed = sum(1 for section in state["report_sections"] if section.get("status") == "completed")
            sections_total = len(state["report_sections"])
            print(f"   Sections: {sections_completed}/{sections_total} completed")
            
            print("   Section Status:")
            for section in state["report_sections"]:
                status_emoji = "✅" if section.get("status") == "completed" else "🔄" if section.get("status") == "in_progress" else "⏳"
                print(f"   {status_emoji} {section.get('name')}: {section.get('status')}")

        # Display risk assessment if available
        if state.get("risk_assessment"):
            print("\n⚠️ Risk Assessment:")
            risk_category = state.get("risk_category", "Not determined")
            risk_emoji = "🟢" if risk_category == "LOW_RISK" else "🟡" if risk_category == "MEDIUM_RISK" else "🔴" if risk_category == "HIGH_RISK" else "⛔" if risk_category == "PROHIBITED" else "❓"
            print(f"   {risk_emoji} Overall Risk Category: {risk_category}")
            
            if state.get("business_activities"):
                print("\n   Business Activities:")
                for i, activity in enumerate(state["business_activities"], 1):
                    print(f"   {i}. {activity.get('activity')}")
            
            if state.get("prohibited_activities"):
                print("\n   ⛔ Prohibited Activities:")
                for i, activity in enumerate(state["prohibited_activities"], 1):
                    print(f"   {i}. {activity.get('activity')}")

        # Display decision if available
        if state.get("kyc_decision"):
            decision = state["kyc_decision"]
            print("\n🏁 KYC Decision:")
            decision_status = decision.get("decision", "Pending")
            decision_emoji = "✅" if decision_status == "APPROVE" else "⛔" if decision_status == "REJECT" else "⚠️" if decision_status == "APPROVE_WITH_CONDITIONS" else "❓"
            print(f"   {decision_emoji} Decision: {decision_status}")

        # Display error if present
        if state.get("error"):
            print(f"\n❌ Error: {state.get('error')}")

        print("\n" + "=" * 50)

    def save_state_history(self, file_path: str = None) -> str:
        """
        Save the state history to a JSON file
        
        Args:
            file_path: Path to save the state history (optional)
            
        Returns:
            The path to the saved file
        """
        # Create a default file path if none provided
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("kyc_states", exist_ok=True)
            file_path = f"kyc_states/kyc_state_history_{timestamp}.json"
            
        # Get the state history from the agent
        if hasattr(self, 'app') and hasattr(self.app, 'get_state_history'):
            # Create a config object to pass to get_state_history
            config = {"configurable": {}}
            state_history = self.app.get_state_history(config)
        else:
            # Fallback to empty history if not available
            state_history = []
            
        # Convert state history to JSON-serializable format if needed
        serializable_history = []
        for state in state_history:
            # If state is a custom class, convert to dict
            if hasattr(state, '__dict__'):
                serializable_history.append(state.__dict__)
            elif hasattr(state, 'to_dict'):
                serializable_history.append(state.to_dict())
            else:
                serializable_history.append(state)
        
        # Save to JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_history, f, indent=2, default=str)
            
        return file_path