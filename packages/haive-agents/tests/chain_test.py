# complex_chain_example.py

import json
import logging
from typing import Any

from agents.simple.agent import SimpleAgent
from agents.simple.chain_agent import ChainAgentSchema
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# =============================================
# Custom Output Models
# =============================================


class DocumentClassification(BaseModel):
    """Model for document classification."""

    document_type: str = Field(
        description="Type of document (legal, financial, technical, creative, academic, news)"
    )
    confidence: float = Field(description="Confidence score (0.0-1.0)")
    languages: list[str] = Field(description="Languages detected in the document")
    primary_topic: str = Field(description="Primary topic or subject of the document")
    subtopics: list[str] = Field(description="List of subtopics in the document")
    complexity_level: str = Field(
        description="Complexity level (simple, moderate, complex, technical)"
    )
    target_audience: str = Field(description="Intended audience for the document")
    sensitive_content: bool = Field(
        description="Whether document contains sensitive/confidential info"
    )


class LegalAnalysis(BaseModel):
    """Model for legal document analysis."""

    document_type: str = Field(description="Specific type of legal document")
    jurisdiction: str = Field(description="Relevant legal jurisdiction")
    parties: list[str] = Field(description="Parties involved in the legal document")
    key_clauses: list[str] = Field(description="Important clauses or provisions")
    obligations: list[str] = Field(description="Legal obligations specified")
    risks: list[str] = Field(description="Potential legal risks identified")
    deadlines: list[str] = Field(description="Important dates or deadlines")
    governing_law: str = Field(description="Governing law of the document")


class FinancialAnalysis(BaseModel):
    """Model for financial document analysis."""

    document_type: str = Field(description="Specific type of financial document")
    entities: list[str] = Field(description="Financial entities mentioned")
    key_metrics: dict[str, Any] = Field(description="Important financial metrics")
    time_period: str = Field(description="Time period covered")
    financial_trends: list[str] = Field(description="Identified financial trends")
    risks: list[str] = Field(description="Financial risks mentioned")
    opportunities: list[str] = Field(description="Financial opportunities identified")
    recommendations: list[str] = Field(description="Financial recommendations")


class TechnicalAnalysis(BaseModel):
    """Model for technical document analysis."""

    document_type: str = Field(description="Specific type of technical document")
    technologies: list[str] = Field(description="Technologies or systems mentioned")
    methodologies: list[str] = Field(description="Technical methodologies described")
    requirements: list[str] = Field(description="Technical requirements")
    specifications: dict[str, Any] = Field(description="Technical specifications")
    limitations: list[str] = Field(description="Technical limitations mentioned")
    dependencies: list[str] = Field(description="Dependencies identified")
    security_considerations: list[str] = Field(description="Security aspects mentioned")


class AcademicAnalysis(BaseModel):
    """Model for academic document analysis."""

    document_type: str = Field(description="Specific type of academic document")
    research_field: str = Field(description="Primary research field")
    methodologies: list[str] = Field(description="Research methodologies used")
    key_findings: list[str] = Field(description="Key research findings")
    sources: int = Field(description="Number of sources/references")
    limitations: list[str] = Field(description="Research limitations mentioned")
    future_work: list[str] = Field(description="Suggested future research")
    contribution: str = Field(description="Main contribution to the field")


# =============================================
# Executive Summary Template - Fixed to avoid template issues
# =============================================

EXEC_SUMMARY_TEMPLATE = """
Create an executive summary of the document analysis results:

# DOCUMENT ANALYSIS EXECUTIVE SUMMARY

## Document Information
- Type: {document_type}
- Topic: {primary_topic}

## Specialized Analysis Results
{specialized_analysis}

## Key Findings

## Recommendations

## Next Steps

Format the summary with clear sections, bullet points, and actionable insights.
"""

# =============================================
# Specialized Document Analysis Chain
# =============================================


class BranchingDocumentAnalyzer:
    """An advanced document analysis system with specialized branches
    for different document types and dynamic routing.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.engines = {}
        self.step_names = []
        self.dynamic_graph = None
        self._setup_engines()

    def _setup_engines(self):
        """Set up all the specialized engines for the analysis chain."""
        # 1. Document Classification Engine
        document_classifier_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a document classification expert. Analyze the provided text to determine document type and characteristics.",
                ),
                (
                    "human",
                    "Analyze the following document and classify its type, subject, complexity, and other characteristics:\n\n{text}",
                ),
            ]
        )

        document_classifier = AugLLMConfig(
            name="document_classifier",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
            prompt_template=document_classifier_prompt,
            structured_output_model=DocumentClassification,
        )

        # 2. Route Determination (decides which specialized branch to use)
        router_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a document routing specialist. Based on document classification, determine the appropriate analysis path.",
                ),
                (
                    "human",
                    "Based on this document classification, determine which specialized analysis path should be used.\nClassification: {classification}\n\nRespond with ONLY ONE of these exact words: legal, financial, technical, academic, general",
                ),
            ]
        )

        document_router = AugLLMConfig(
            name="document_router",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.1}),
            prompt_template=router_prompt,
            output_parser=StrOutputParser(),
        )

        # 3. BRANCH: Legal Document Analysis
        legal_analyzer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a legal document analysis expert."),
                (
                    "human",
                    "Perform a detailed legal analysis of this document, identifying parties, clauses, obligations, risks, and other legal aspects:\n\n{text}",
                ),
            ]
        )

        legal_analyzer = AugLLMConfig(
            name="legal_analyzer",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
            prompt_template=legal_analyzer_prompt,
            structured_output_model=LegalAnalysis,
        )

        # 4. BRANCH: Financial Document Analysis
        financial_analyzer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a financial document analysis expert."),
                (
                    "human",
                    "Perform a detailed financial analysis of this document, identifying entities, metrics, trends, risks, and opportunities:\n\n{text}",
                ),
            ]
        )

        financial_analyzer = AugLLMConfig(
            name="financial_analyzer",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
            prompt_template=financial_analyzer_prompt,
            structured_output_model=FinancialAnalysis,
        )

        # 5. BRANCH: Technical Document Analysis
        technical_analyzer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a technical document analysis expert."),
                (
                    "human",
                    "Perform a detailed technical analysis of this document, identifying technologies, methodologies, requirements, specifications, and limitations:\n\n{text}",
                ),
            ]
        )

        technical_analyzer = AugLLMConfig(
            name="technical_analyzer",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
            prompt_template=technical_analyzer_prompt,
            structured_output_model=TechnicalAnalysis,
        )

        # 6. BRANCH: Academic Document Analysis
        academic_analyzer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an academic document analysis expert."),
                (
                    "human",
                    "Perform a detailed academic analysis of this document, identifying research field, methodologies, findings, and scholarly contribution:\n\n{text}",
                ),
            ]
        )

        academic_analyzer = AugLLMConfig(
            name="academic_analyzer",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
            prompt_template=academic_analyzer_prompt,
            structured_output_model=AcademicAnalysis,
        )

        # 7. BRANCH: General Document Analysis (fallback)
        general_analyzer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a general document analysis expert."),
                (
                    "human",
                    "Provide a comprehensive analysis of this document, covering its main points, structure, and significance:\n\n{text}",
                ),
            ]
        )

        general_analyzer = AugLLMConfig(
            name="general_analyzer",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.4}),
            prompt_template=general_analyzer_prompt,
            output_parser=StrOutputParser(),
        )

        # 8. Executive Summary Generator (final step in all branches)
        # Using a fixed template approach instead of a ChatPromptTemplate to avoid variable issues
        summary_prompt = ChatPromptTemplate.from_template(EXEC_SUMMARY_TEMPLATE)

        executive_summary = AugLLMConfig(
            name="executive_summary",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.4}),
            prompt_template=summary_prompt,
            output_parser=StrOutputParser(),
        )

        # Store engines in a dictionary for easy access
        self.engines = {
            "document_classifier": document_classifier,
            "document_router": document_router,
            "legal_analyzer": legal_analyzer,
            "financial_analyzer": financial_analyzer,
            "technical_analyzer": technical_analyzer,
            "academic_analyzer": academic_analyzer,
            "general_analyzer": general_analyzer,
            "executive_summary": executive_summary,
        }

    def build_chain(self):
        """Build the document analysis chain with branching logic
        based on document classification.
        """

        # Create an extended schema that includes branch information
        class BranchingChainSchema(ChainAgentSchema):
            branch_path: str = Field(
                default="", description="The branch path chosen for analysis"
            )
            document_type: str = Field(
                default="", description="Classified document type"
            )
            primary_topic: str = Field(default="", description="Primary document topic")
            specialized_analysis: str = Field(
                default="", description="Results from specialized analysis"
            )
            chain_data: dict[str, Any] = Field(
                default_factory=dict, description="Data passed between chain steps"
            )

        # Create a dynamic graph
        dg = DynamicGraph(
            components=list(self.engines.values()), state_schema=BranchingChainSchema
        )

        # Add initialization node
        def init_node(state):
            """Initialize the chain state."""
            # Extract text from messages
            messages_text = ""
            if hasattr(state, "messages") and state.messages:
                messages_text = "\n".join(
                    [
                        m.content if hasattr(m, "content") else str(m)
                        for m in state.messages
                    ]
                )

            # Initialize chain_data with input text
            return {"current_step": 0, "chain_data": {"input_text": messages_text}}

        dg.add_node("init", init_node, command_goto="document_classifier")

        # Add document classifier node
        def classifier_node(state):
            """Classify the document to determine analysis path."""
            try:
                # Get input text
                input_text = ""
                if (
                    hasattr(state, "chain_data")
                    and isinstance(state.chain_data, dict)
                    and "input_text" in state.chain_data
                ):
                    input_text = state.chain_data["input_text"]
                elif hasattr(state, "messages") and state.messages:
                    input_text = "\n".join(
                        [
                            m.content if hasattr(m, "content") else str(m)
                            for m in state.messages
                        ]
                    )

                logger.debug(
                    f"Classifying document - input length: {len(input_text)} chars"
                )

                # Create classifier runnable
                classifier = compose_runnable(self.engines["document_classifier"])

                # Classify document
                result = classifier.invoke({"text": input_text})

                # Convert to string for storage
                if hasattr(result, "model_dump"):
                    result_dict = result.model_dump()
                elif hasattr(result, "dict"):
                    result_dict = result.dict()
                else:
                    result_dict = {"error": "Could not convert result to dict"}

                result_str = json.dumps(result_dict)
                logger.debug(f"Classification result: {result_str[:100]}...")

                # Update chain data
                chain_data = {}
                if hasattr(state, "chain_data") and isinstance(state.chain_data, dict):
                    chain_data = dict(state.chain_data)
                chain_data["document_classifier"] = result_str
                chain_data["input_text"] = input_text  # Ensure input text is preserved

                # Store specific fields for later use
                document_type = (
                    result.document_type if hasattr(result, "document_type") else ""
                )
                primary_topic = (
                    result.primary_topic if hasattr(result, "primary_topic") else ""
                )

                # Update state
                return {
                    "chain_data": chain_data,
                    "document_type": document_type,
                    "primary_topic": primary_topic,
                    "intermediate_results": {"document_classifier": result_str},
                }

            except Exception as e:
                logger.error(f"Error in document classifier: {e!s}")
                return {"error": f"Error in document classifier: {e!s}"}

        dg.add_node(
            "document_classifier", classifier_node, command_goto="document_router"
        )

        # Add document router node
        def router_node(state):
            """Route the document to the appropriate specialized analyzer."""
            try:
                # Get classification result
                classification = "{}"
                if (
                    hasattr(state, "chain_data")
                    and isinstance(state.chain_data, dict)
                    and "document_classifier" in state.chain_data
                ):
                    classification = state.chain_data["document_classifier"]

                logger.debug(
                    f"Routing document with classification: {classification[:100]}..."
                )

                # Create router runnable
                router = compose_runnable(self.engines["document_router"])

                # Get routing decision
                result = router.invoke({"classification": classification})

                # Clean up result (ensure it's just one of the expected values)
                branch_path = result.strip().lower()
                valid_paths = ["legal", "financial", "technical", "academic", "general"]

                if branch_path not in valid_paths:
                    # Try to extract from text
                    for path in valid_paths:
                        if path in branch_path:
                            branch_path = path
                            break
                    else:
                        # Default to general if no match
                        branch_path = "general"

                logger.debug(f"Selected branch path: {branch_path}")

                # Update chain data
                chain_data = {}
                if hasattr(state, "chain_data") and isinstance(state.chain_data, dict):
                    chain_data = dict(state.chain_data)
                chain_data["document_router"] = branch_path

                # Update intermediate results
                intermediate_results = {}
                if hasattr(state, "intermediate_results") and isinstance(
                    state.intermediate_results, dict
                ):
                    intermediate_results = dict(state.intermediate_results)
                intermediate_results["document_router"] = branch_path

                # Create the next node name based on branch path
                next_node = f"{branch_path}_analyzer"
                logger.debug(f"Next node: {next_node}")

                # Return updated state with command to route to next node
                return {
                    "chain_data": chain_data,
                    "branch_path": branch_path,
                    "intermediate_results": intermediate_results,
                    "__command__": {"goto": next_node},
                }

            except Exception as e:
                logger.error(f"Error in document router: {e!s}")
                return {
                    "error": f"Error in document router: {e!s}",
                    "branch_path": "general",
                    "__command__": {"goto": "general_analyzer"},
                }

        dg.add_node("document_router", router_node)

        # Add specialized analyzer nodes
        def create_analyzer_node(analyzer_name):
            def analyzer_node(state):
                """Run the specialized analyzer."""
                try:
                    # Get input text
                    input_text = ""
                    if (
                        hasattr(state, "chain_data")
                        and isinstance(state.chain_data, dict)
                        and "input_text" in state.chain_data
                    ):
                        input_text = state.chain_data["input_text"]
                    elif hasattr(state, "messages") and state.messages:
                        input_text = "\n".join(
                            [
                                m.content if hasattr(m, "content") else str(m)
                                for m in state.messages
                            ]
                        )

                    logger.debug(
                        f"Running {analyzer_name} - input length: {len(input_text)} chars"
                    )

                    # Create analyzer runnable
                    analyzer = compose_runnable(self.engines[analyzer_name])

                    # Run analysis
                    result = analyzer.invoke({"text": input_text})

                    # Convert to string for storage
                    if hasattr(result, "model_dump"):
                        result_dict = result.model_dump()
                    elif hasattr(result, "dict"):
                        result_dict = result.dict()
                    else:
                        result_dict = {"result": str(result)}

                    result_str = json.dumps(result_dict)
                    logger.debug(f"{analyzer_name} result: {result_str[:100]}...")

                    # Update chain data
                    chain_data = {}
                    if hasattr(state, "chain_data") and isinstance(
                        state.chain_data, dict
                    ):
                        chain_data = dict(state.chain_data)
                    chain_data[analyzer_name] = result_str

                    # Update intermediate results
                    intermediate_results = {}
                    if hasattr(state, "intermediate_results") and isinstance(
                        state.intermediate_results, dict
                    ):
                        intermediate_results = dict(state.intermediate_results)
                    intermediate_results[analyzer_name] = result_str

                    # Return updated state with command to go to executive summary
                    return {
                        "chain_data": chain_data,
                        "specialized_analysis": result_str,
                        "intermediate_results": intermediate_results,
                        "__command__": {"goto": "executive_summary"},
                    }

                except Exception as e:
                    logger.error(f"Error in {analyzer_name}: {e!s}")
                    error_msg = f"Error in {analyzer_name}: {e!s}"
                    return {
                        "error": error_msg,
                        "specialized_analysis": f"Analysis failed with error: {e!s}",
                        "__command__": {"goto": "executive_summary"},
                    }

            return analyzer_node

        # Add specialized analyzer nodes
        for analyzer_type in ["legal", "financial", "technical", "academic", "general"]:
            analyzer_name = f"{analyzer_type}_analyzer"
            dg.add_node(analyzer_name, create_analyzer_node(analyzer_name))

        # Add executive summary node
        def summary_node(state):
            """Generate executive summary."""
            try:
                # Get required fields
                document_type = (
                    state.document_type
                    if hasattr(state, "document_type")
                    else "Unknown"
                )
                primary_topic = (
                    state.primary_topic
                    if hasattr(state, "primary_topic")
                    else "Unknown"
                )
                specialized_analysis = (
                    state.specialized_analysis
                    if hasattr(state, "specialized_analysis")
                    else "{}"
                )

                logger.debug(
                    f"Generating executive summary for {document_type} document"
                )

                # Create summary runnable
                summary_gen = compose_runnable(self.engines["executive_summary"])

                # Fix any JSON string issues in specialized_analysis
                if isinstance(
                    specialized_analysis, str
                ) and specialized_analysis.startswith("{"):
                    try:
                        # Parse and re-stringify to ensure proper escaping
                        specialized_analysis_obj = json.loads(specialized_analysis)
                        specialized_analysis = json.dumps(
                            specialized_analysis_obj, indent=2
                        )
                    except:
                        # If not valid JSON, leave as is
                        pass

                # Generate summary with fixed inputs to avoid template issues
                summary = summary_gen.invoke(
                    {
                        "document_type": document_type,
                        "primary_topic": primary_topic,
                        "specialized_analysis": specialized_analysis,
                    }
                )

                logger.debug(f"Generated summary: {summary[:100]}...")

                # Update chain data
                chain_data = {}
                if hasattr(state, "chain_data") and isinstance(state.chain_data, dict):
                    chain_data = dict(state.chain_data)
                chain_data["executive_summary"] = summary

                # Update intermediate results
                intermediate_results = {}
                if hasattr(state, "intermediate_results") and isinstance(
                    state.intermediate_results, dict
                ):
                    intermediate_results = dict(state.intermediate_results)
                intermediate_results["executive_summary"] = summary

                # Add as AI message
                messages = []
                if hasattr(state, "messages") and state.messages:
                    messages = list(state.messages)
                messages.append(AIMessage(content=summary))

                # Return final state
                return {
                    "chain_data": chain_data,
                    "output": summary,
                    "intermediate_results": intermediate_results,
                    "messages": messages,
                }

            except Exception as e:
                logger.error(f"Error in executive summary: {e!s}")
                error_msg = f"Error generating executive summary: {e!s}"

                # Add error as message
                messages = []
                if hasattr(state, "messages") and state.messages:
                    messages = list(state.messages)
                messages.append(AIMessage(content=f"Error: {error_msg}"))

                return {"error": error_msg, "messages": messages}

        dg.add_node("executive_summary", summary_node, command_goto=END)

        # Build the graph
        self.dynamic_graph = dg
        return dg.build()

    def analyze_document(self, document_text):
        """Run the document analysis chain on the provided text.

        Args:
            document_text: The document text to analyze

        Returns:
            Dict with analysis results
        """
        # Build the chain
        graph = self.build_chain()

        # Create a custom agent to run the graph
        class BranchingDocumentAnalysisAgent(SimpleAgent):
            def setup_workflow(self):
                self.graph = graph
                self.app = self.graph.compile(checkpointer=self.memory)

        # Create agent config
        from agents.simple.chain_agent import ChainAgentConfig

        # Create agent config
        config = ChainAgentConfig(
            name="branching_document_analyzer",
            engine=self.engines["document_classifier"],  # Placeholder, not used
            engines=list(self.engines.values()),
            visualize=True,
        )

        # Create agent
        agent = BranchingDocumentAnalysisAgent(config=config)

        # Run the agent
        result = agent.run(document_text)

        # Process results
        output = {}
        if hasattr(result, "model_dump"):
            output = result.model_dump()
        elif hasattr(result, "dict"):
            output = result.dict()
        else:
            output = {
                "output": result.get("output", ""),
                "branch_path": result.get("branch_path", ""),
                "document_type": result.get("document_type", ""),
                "primary_topic": result.get("primary_topic", ""),
                "error": result.get("error", None),
                "intermediate_results": result.get("intermediate_results", {}),
            }

        return output


# Example usage
if __name__ == "__main__":
    # Sample financial document for testing
    financial_doc = """QUARTERLY FINANCIAL REPORT - Q2 2023
ACME HOLDINGS, INC.

INCOME STATEMENT (in millions USD)
                        Q2 2023   Q1 2023   Q2 2022   YoY Change
Revenue                 857.4     792.1     731.5     +17.2%
Cost of Goods Sold      423.8     401.7     372.1     +13.9%
Gross Profit            433.6     390.4     359.4     +20.6%
Operating Expenses      289.2     271.5     263.7     +9.7%
Operating Income        144.4     118.9     95.7      +50.9%
Interest Expense        18.3      18.7      19.4      -5.7%
Income Tax              31.5      25.1      19.1      +64.9%
Net Income              94.6      75.1      57.2      +65.4%

BALANCE SHEET HIGHLIGHTS
- Total Assets increased to $4.92 billion, up 7.8% from Q2 2022
- Cash and Cash Equivalents at $783 million
- Total Debt reduced to $1.13 billion, down 5.3% year-over-year
- Shareholders' Equity increased to $2.87 billion

KEY FINANCIAL METRICS
- Gross Margin: 50.6% (up from 49.1% in Q2 2022)
- Operating Margin: 16.8% (up from 13.1% in Q2 2022)
- Return on Equity (TTM): 13.2% (up from 10.7% in Q2 2022)
- Debt-to-Equity Ratio: 0.39 (improved from 0.45 in Q2 2022)
- Earnings Per Share (EPS): $1.58 (up from $0.94 in Q2 2022)

OUTLOOK
ACME Holdings is raising its full-year 2023 guidance:
- Revenue growth now expected at 14-16% (previously 12-14%)
- Operating margin projected at 16-17% (previously 14-15%)
- EPS guidance increased to $5.90-$6.20 (previously $5.40-$5.70)

RISK FACTORS
- Continued inflationary pressures may impact cost structure
- Foreign exchange volatility expected to continue
- Supply chain challenges in APAC region partially mitigated but ongoing

The company will host an investor call on August 15, 2023, at 2:00 PM EST to discuss these results in detail.

John Reynolds
Chief Financial Officer
ACME Holdings, Inc.
"""

    # Create and run the analyzer
    print("Initializing document analyzer...")
    analyzer = BranchingDocumentAnalyzer()

    print("\nAnalyzing financial document...")
    results = analyzer.analyze_document(financial_doc)

    print("\n=== ANALYSIS RESULTS ===\n")
    print(f"Document Type: {results.get('document_type', 'Unknown')}")
    print(f"Primary Topic: {results.get('primary_topic', 'Unknown')}")
    print(f"Selected Branch: {results.get('branch_path', 'Unknown')}")

    if results.get("error"):
        print(f"\nERROR: {results['error']}")

    print("\n=== EXECUTIVE SUMMARY ===\n")
    print(results.get("output", "No summary generated"))
