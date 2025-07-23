"""Business Multi-Agent Workflows - Real-World Applications

This example demonstrates practical business workflows using complex multi-agent patterns:
- Customer support escalation
- Content creation pipeline
- Data analysis workflow
- Risk assessment system
- Sales qualification process
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

from haive.agents.simple import SimpleAgent
from haive.agents.react import ReactAgent
from haive.agents.multi.base import MultiAgent, SequentialAgent, ParallelAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool


# === 1. CUSTOMER SUPPORT ESCALATION SYSTEM ===

class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    GENERAL = "general"


class TicketClassification(BaseModel):
    """Initial ticket classification."""
    category: TicketCategory
    priority: int = Field(..., ge=1, le=5)
    sentiment: str = Field(..., description="positive/neutral/negative")
    requires_human: bool
    suggested_tags: List[str]


class TicketResolution(BaseModel):
    """Support ticket resolution."""
    resolved: bool
    solution: str
    next_steps: List[str]
    escalation_needed: bool
    escalation_reason: Optional[str] = None


class CustomerSupportEscalation(MultiAgent):
    """Multi-tier customer support with smart escalation."""
    
    def __init__(self):
        # Level 1: AI Classifier
        classifier = SimpleAgent(
            name="ticket_classifier",
            engine=AugLLMConfig(temperature=0.2),
            structured_output_model=TicketClassification,
            system_message="Classify support tickets by type, priority, and sentiment."
        )
        
        # Level 2: Specialized Support Agents
        billing_agent = SimpleAgent(
            name="billing_support",
            engine=AugLLMConfig(temperature=0.4),
            structured_output_model=TicketResolution,
            system_message="You are a billing specialist. Resolve billing inquiries professionally."
        )
        
        @tool
        def check_account_status(account_id: str) -> str:
            """Check customer account status."""
            return f"Account {account_id}: Active, Good standing, Premium tier"
        
        @tool
        def technical_diagnostics(error_code: str) -> str:
            """Run technical diagnostics."""
            return f"Diagnostic for {error_code}: Connection timeout, suggested fix: restart router"
        
        technical_agent = ReactAgent(
            name="technical_support",
            engine=AugLLMConfig(temperature=0.4),
            tools=[technical_diagnostics],
            structured_output_model=TicketResolution,
            system_message="You are a technical support expert. Diagnose and resolve technical issues."
        )
        
        account_agent = ReactAgent(
            name="account_support",
            engine=AugLLMConfig(temperature=0.4),
            tools=[check_account_status],
            structured_output_model=TicketResolution,
            system_message="You are an account specialist. Help with account-related issues."
        )
        
        # Level 3: Senior Support
        senior_agent = SimpleAgent(
            name="senior_support",
            engine=AugLLMConfig(temperature=0.5),
            structured_output_model=TicketResolution,
            system_message="You are a senior support specialist. Handle complex and escalated issues."
        )
        
        # Quality Assurance
        qa_agent = SimpleAgent(
            name="quality_assurance",
            engine=AugLLMConfig(temperature=0.3),
            system_message="Review support interactions for quality and completeness."
        )
        
        agents = {
            "classifier": classifier,
            "billing_support": billing_agent,
            "technical_support": technical_agent,
            "account_support": account_agent,
            "senior_support": senior_agent,
            "qa_review": qa_agent
        }
        
        super().__init__(
            name="support_escalation",
            agents=agents,
            entry_point="classifier"
        )
        
        self._setup_escalation_flow()
    
    def _setup_escalation_flow(self):
        """Setup smart escalation routing."""
        
        def route_by_category(state: Dict[str, Any]) -> str:
            """Route to appropriate specialist."""
            classification = state.get("ticket_classification", {})
            category = classification.get("category", "general")
            priority = classification.get("priority", 3)
            
            # High priority goes to senior
            if priority >= 4 or classification.get("requires_human", False):
                return "senior_support"
            
            # Route by category
            routing = {
                "billing": "billing_support",
                "technical": "technical_support",
                "account": "account_support",
                "general": "billing_support"  # Default
            }
            
            return routing.get(category, "billing_support")
        
        def check_escalation(state: Dict[str, Any]) -> str:
            """Check if escalation is needed."""
            resolution = state.get("ticket_resolution", {})
            
            if resolution.get("escalation_needed", False):
                return "senior_support"
            elif resolution.get("resolved", False):
                return "qa_review"
            else:
                return "senior_support"  # Unresolved goes to senior
        
        # Initial routing
        self.add_conditional_edges(
            source="classifier",
            path=route_by_category
        )
        
        # Escalation check for each specialist
        for specialist in ["billing_support", "technical_support", "account_support"]:
            self.add_conditional_edges(
                source=specialist,
                path=check_escalation
            )
        
        # Senior always goes to QA
        self.add_edge("senior_support", "qa_review")


# === 2. CONTENT CREATION PIPELINE ===

class ContentBrief(BaseModel):
    """Content creation brief."""
    content_type: str  # blog/social/email/whitepaper
    topic: str
    target_audience: str
    key_points: List[str]
    tone: str  # professional/casual/technical
    word_count: int


class ContentOutline(BaseModel):
    """Detailed content outline."""
    title: str
    sections: List[Dict[str, str]]
    keywords: List[str]
    references: List[str]


class ContentDraft(BaseModel):
    """Content draft."""
    title: str
    content: str
    meta_description: str
    tags: List[str]


class ContentReview(BaseModel):
    """Content review results."""
    approved: bool
    score: float
    feedback: List[str]
    required_changes: List[str]


class SEOOptimization(BaseModel):
    """SEO optimization suggestions."""
    optimized_title: str
    optimized_meta: str
    keyword_density: Dict[str, float]
    suggestions: List[str]


async def content_creation_pipeline():
    """Multi-stage content creation with parallel optimization."""
    
    # Research phase
    researcher = SimpleAgent(
        name="content_researcher",
        engine=AugLLMConfig(temperature=0.5),
        structured_output_model=ContentOutline,
        system_message="Research topics and create detailed content outlines."
    )
    
    # Writing phase
    writer = SimpleAgent(
        name="content_writer",
        engine=AugLLMConfig(temperature=0.7),
        structured_output_model=ContentDraft,
        system_message="Write engaging content based on outlines and briefs."
    )
    
    # Parallel optimization phase
    seo_optimizer = SimpleAgent(
        name="seo_optimizer",
        engine=AugLLMConfig(temperature=0.3),
        structured_output_model=SEOOptimization,
        system_message="Optimize content for search engines."
    )
    
    grammar_checker = SimpleAgent(
        name="grammar_checker",
        engine=AugLLMConfig(temperature=0.1),
        system_message="Check grammar, spelling, and readability."
    )
    
    fact_checker = SimpleAgent(
        name="fact_checker",
        engine=AugLLMConfig(temperature=0.2),
        system_message="Verify facts and check sources."
    )
    
    # Review phase
    editor = SimpleAgent(
        name="content_editor",
        engine=AugLLMConfig(temperature=0.4),
        structured_output_model=ContentReview,
        system_message="Review and approve content for publication."
    )
    
    # Parallel optimization
    optimization_team = ParallelAgent(
        name="optimization_team",
        agents=[seo_optimizer, grammar_checker, fact_checker]
    )
    
    # Full pipeline
    pipeline = SequentialAgent(
        name="content_pipeline",
        agents=[researcher, writer, optimization_team, editor]
    )
    
    # Execute with a brief
    brief = ContentBrief(
        content_type="blog",
        topic="AI in Healthcare",
        target_audience="Healthcare professionals",
        key_points=["Diagnosis assistance", "Treatment planning", "Patient monitoring"],
        tone="professional",
        word_count=1500
    )
    
    result = await pipeline.arun(brief.model_dump())
    return result


# === 3. DATA ANALYSIS WORKFLOW ===

class DataAnalysisRequest(BaseModel):
    """Data analysis request."""
    dataset_description: str
    analysis_goals: List[str]
    specific_questions: List[str]
    output_format: str  # report/dashboard/presentation


class DataQualityReport(BaseModel):
    """Data quality assessment."""
    completeness_score: float
    accuracy_indicators: Dict[str, float]
    issues_found: List[str]
    cleaning_recommendations: List[str]


class StatisticalAnalysis(BaseModel):
    """Statistical analysis results."""
    summary_statistics: Dict[str, Any]
    correlations: Dict[str, float]
    significant_findings: List[str]
    visualizations_needed: List[str]


class BusinessInsights(BaseModel):
    """Business insights from data."""
    key_insights: List[str]
    actionable_recommendations: List[str]
    risks_identified: List[str]
    opportunities: List[str]


class DataAnalysisWorkflow(MultiAgent):
    """Comprehensive data analysis workflow."""
    
    def __init__(self):
        # Data quality checker
        quality_analyst = SimpleAgent(
            name="data_quality_analyst",
            engine=AugLLMConfig(temperature=0.2),
            structured_output_model=DataQualityReport,
            system_message="Assess data quality and recommend cleaning steps."
        )
        
        # Statistical analyst
        @tool
        def calculate_correlation(var1: str, var2: str) -> str:
            """Calculate correlation between variables."""
            return f"Correlation between {var1} and {var2}: 0.73 (strong positive)"
        
        statistician = ReactAgent(
            name="statistical_analyst",
            engine=AugLLMConfig(temperature=0.3),
            tools=[calculate_correlation],
            structured_output_model=StatisticalAnalysis,
            system_message="Perform statistical analysis and identify patterns."
        )
        
        # Business analyst
        business_analyst = SimpleAgent(
            name="business_analyst",
            engine=AugLLMConfig(temperature=0.5),
            structured_output_model=BusinessInsights,
            system_message="Extract business insights and actionable recommendations."
        )
        
        # Visualization specialist
        viz_specialist = SimpleAgent(
            name="visualization_specialist",
            engine=AugLLMConfig(temperature=0.6),
            system_message="Design effective data visualizations and dashboards."
        )
        
        # Report generator
        report_writer = SimpleAgent(
            name="report_generator",
            engine=AugLLMConfig(temperature=0.4),
            system_message="Create comprehensive analysis reports."
        )
        
        agents = {
            "quality": quality_analyst,
            "stats": statistician,
            "business": business_analyst,
            "viz": viz_specialist,
            "report": report_writer
        }
        
        super().__init__(
            name="data_analysis_workflow",
            agents=agents,
            entry_point="quality"
        )
        
        self._setup_analysis_flow()
    
    def _setup_analysis_flow(self):
        """Setup analysis workflow."""
        
        def route_after_quality(state: Dict[str, Any]) -> str:
            """Route based on data quality."""
            quality_report = state.get("data_quality_report", {})
            completeness = quality_report.get("completeness_score", 0)
            
            if completeness < 0.7:
                # Poor quality - need business insights on partial data
                return "business"
            else:
                # Good quality - full statistical analysis
                return "stats"
        
        # Quality check routing
        self.add_conditional_edges(
            source="quality",
            path=route_after_quality
        )
        
        # Statistical analysis → Business insights
        self.add_edge("stats", "business")
        
        # Business insights → Visualization
        self.add_edge("business", "viz")
        
        # Visualization → Report
        self.add_edge("viz", "report")


# === 4. RISK ASSESSMENT SYSTEM ===

class RiskFactors(BaseModel):
    """Identified risk factors."""
    category: str  # financial/operational/strategic/compliance
    factors: List[Dict[str, Any]]
    data_sources: List[str]


class RiskScore(BaseModel):
    """Calculated risk score."""
    overall_score: float = Field(..., ge=0, le=10)
    category_scores: Dict[str, float]
    confidence_level: float
    calculation_method: str


class MitigationPlan(BaseModel):
    """Risk mitigation strategies."""
    high_priority_actions: List[str]
    medium_priority_actions: List[str]
    preventive_measures: List[str]
    contingency_plans: Dict[str, List[str]]


async def risk_assessment_system():
    """Multi-dimensional risk assessment."""
    
    # Risk identifiers (parallel)
    financial_analyst = SimpleAgent(
        name="financial_risk_analyst",
        engine=AugLLMConfig(temperature=0.3),
        structured_output_model=RiskFactors,
        system_message="Identify financial risks and vulnerabilities."
    )
    
    operational_analyst = SimpleAgent(
        name="operational_risk_analyst",
        engine=AugLLMConfig(temperature=0.3),
        structured_output_model=RiskFactors,
        system_message="Identify operational risks and process vulnerabilities."
    )
    
    compliance_analyst = SimpleAgent(
        name="compliance_risk_analyst",
        engine=AugLLMConfig(temperature=0.2),
        structured_output_model=RiskFactors,
        system_message="Identify compliance and regulatory risks."
    )
    
    # Risk scoring
    risk_scorer = SimpleAgent(
        name="risk_scoring_engine",
        engine=AugLLMConfig(temperature=0.1),
        structured_output_model=RiskScore,
        system_message="Calculate comprehensive risk scores using multiple factors."
    )
    
    # Mitigation planning
    mitigation_planner = SimpleAgent(
        name="mitigation_strategist",
        engine=AugLLMConfig(temperature=0.5),
        structured_output_model=MitigationPlan,
        system_message="Develop risk mitigation strategies and contingency plans."
    )
    
    # Parallel risk identification
    risk_identifiers = ParallelAgent(
        name="risk_identification_team",
        agents=[financial_analyst, operational_analyst, compliance_analyst]
    )
    
    # Full risk assessment pipeline
    risk_pipeline = SequentialAgent(
        name="risk_assessment_pipeline",
        agents=[risk_identifiers, risk_scorer, mitigation_planner]
    )
    
    # Execute assessment
    result = await risk_pipeline.arun({
        "company": "TechCorp",
        "industry": "Software",
        "size": "Mid-market",
        "recent_events": ["New product launch", "Market expansion", "Leadership change"]
    })
    
    return result


# === 5. SALES QUALIFICATION PROCESS ===

class LeadProfile(BaseModel):
    """Lead qualification profile."""
    lead_score: int = Field(..., ge=0, le=100)
    fit_score: int = Field(..., ge=0, le=100)
    intent_signals: List[str]
    qualification_status: str  # qualified/nurture/disqualified
    recommended_next_steps: List[str]


class CompetitiveIntel(BaseModel):
    """Competitive intelligence."""
    current_vendor: Optional[str]
    satisfaction_level: Optional[str]
    switching_barriers: List[str]
    opportunities: List[str]


async def sales_qualification_workflow():
    """Intelligent sales lead qualification."""
    
    # Lead scorer
    @tool
    def check_company_size(company: str) -> str:
        """Check company size and revenue."""
        return f"{company}: 500 employees, $50M revenue, growing 20% YoY"
    
    @tool
    def check_tech_stack(company: str) -> str:
        """Check company's current tech stack."""
        return f"{company} uses: Salesforce, AWS, Slack, custom ERP"
    
    lead_scorer = ReactAgent(
        name="lead_scoring_agent",
        engine=AugLLMConfig(temperature=0.3),
        tools=[check_company_size, check_tech_stack],
        structured_output_model=LeadProfile,
        system_message="Score and qualify sales leads based on fit and intent."
    )
    
    # Competitive intelligence
    competitive_analyst = SimpleAgent(
        name="competitive_intel",
        engine=AugLLMConfig(temperature=0.4),
        structured_output_model=CompetitiveIntel,
        system_message="Analyze competitive landscape and switching opportunities."
    )
    
    # Personalization engine
    personalizer = SimpleAgent(
        name="message_personalizer",
        engine=AugLLMConfig(temperature=0.7),
        system_message="Create personalized outreach messages based on lead profile."
    )
    
    # Parallel analysis
    analysis_team = ParallelAgent(
        name="qualification_team",
        agents=[lead_scorer, competitive_analyst]
    )
    
    # Full qualification process
    qualification_pipeline = SequentialAgent(
        name="sales_qualification",
        agents=[analysis_team, personalizer]
    )
    
    # Execute qualification
    result = await qualification_pipeline.arun({
        "company": "InnovateCorp",
        "contact": "Jane Smith, VP of Engineering",
        "source": "Webinar attendance",
        "interactions": ["Downloaded whitepaper", "Visited pricing page", "Attended demo"]
    })
    
    return result


# === MAIN EXECUTION ===

async def main():
    """Run business workflow demonstrations."""
    
    print("💼 Business Multi-Agent Workflows Demo\n")
    
    # 1. Customer Support
    print("1️⃣ Customer Support Escalation")
    print("-" * 50)
    support_system = CustomerSupportEscalation()
    ticket_result = await support_system.arun({
        "ticket_id": "TICK-12345",
        "customer_id": "CUST-789",
        "issue": "My billing shows duplicate charges for last month. This is the third time this has happened!",
        "previous_interactions": 2
    })
    print(f"Support Result: {ticket_result}\n")
    
    # 2. Content Creation
    print("2️⃣ Content Creation Pipeline")
    print("-" * 50)
    content_result = await content_creation_pipeline()
    print(f"Content Result: {content_result}\n")
    
    # 3. Data Analysis
    print("3️⃣ Data Analysis Workflow")
    print("-" * 50)
    analysis_workflow = DataAnalysisWorkflow()
    analysis_result = await analysis_workflow.arun({
        "dataset_description": "Customer behavior data for Q4 2023",
        "analysis_goals": ["Identify churn patterns", "Segment high-value customers"],
        "specific_questions": ["What drives customer retention?", "Which features correlate with upgrades?"],
        "output_format": "report"
    })
    print(f"Analysis Result: {analysis_result}\n")
    
    # 4. Risk Assessment
    print("4️⃣ Risk Assessment System")
    print("-" * 50)
    risk_result = await risk_assessment_system()
    print(f"Risk Assessment: {risk_result}\n")
    
    # 5. Sales Qualification
    print("5️⃣ Sales Qualification Process")
    print("-" * 50)
    sales_result = await sales_qualification_workflow()
    print(f"Qualification Result: {sales_result}\n")


if __name__ == "__main__":
    asyncio.run(main())