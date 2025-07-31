"""Enhanced HyDE RAG Agent v2 with Advanced Prompt Selection and Multi-Document Generation.

from typing import Any
This version integrates the new enhanced prompt system with:
- Automatic prompt type selection based on query analysis
- Multi-document generation from different perspectives
- Improved separation of generation from parsing
- Domain-specific prompt templates
- Ensemble retrieval using multiple hypothetical documents
"""

from enum import Enum
from typing import Any

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, model_validator

from haive.agents.base.agent import Agent
from haive.agents.common.utils.pydantic_prompt_utils import (
    PromptStyle,
    PydanticPromptConfig,
    create_generation_and_parsing_prompts,
)
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.common.query_constructors.hyde.enhanced_prompts import (
    HYDE_ANALYSIS_PROMPT,
    HyDEPerspective,
    HyDEPromptType,
    get_ensemble_prompt,
    get_generation_prompt,
    get_perspective_prompt,
    select_prompt_automatically,
)
from haive.agents.rag.models import HyDEResult
from haive.agents.simple.agent import SimpleAgent


class HyDEGenerationMode(str, Enum):
    """Different modes for HyDE document generation."""

    SINGLE = "single"  # Generate one hypothetical document
    MULTI_PERSPECTIVE = "multi_perspective"  # Generate from different perspectives
    MULTI_DOMAIN = "multi_domain"  # Generate different document types
    ENSEMBLE = "ensemble"  # Generate multiple documents for ensemble retrieval


class HyDEAgentConfig(BaseModel):
    """Configuration for Enhanced HyDE RAG Agent."""

    generation_mode: HyDEGenerationMode = Field(
        default=HyDEGenerationMode.SINGLE, description="Mode for document generation"
    )
    auto_select_prompt: bool = Field(
        default=True, description="Automatically select prompt type based on query"
    )
    prompt_type: HyDEPromptType = Field(
        default=HyDEPromptType.GENERAL,
        description="Specific prompt type to use (if not auto-selecting)",
    )
    perspectives: list[HyDEPerspective] = Field(
        default_factory=lambda: [HyDEPerspective.EXPERT, HyDEPerspective.PRACTITIONER],
        description="Perspectives for multi-perspective generation",
    )
    target_length: int = Field(
        default=1000, description="Target character length for generated documents"
    )
    num_ensemble_docs: int = Field(
        default=3, description="Number of documents for ensemble generation"
    )
    use_structured_analysis: bool = Field(
        default=True,
        description="Whether to use structured analysis of generated documents",
    )
    enable_query_rewriting: bool = Field(
        default=True, description="Whether to enable query rewriting based on analysis"
    )


class EnhancedHyDERAGAgentV2(SequentialAgent, ToolRouteMixin):
    """Enhanced HyDE RAG Agent with advanced prompt selection and multi-document generation.

    Key Features:
    - Automatic prompt type selection based on query analysis
    - Multi-document generation from different perspectives/domains
    - Ensemble retrieval using multiple hypothetical documents
    - Proper separation of generation from parsing
    - Configurable generation strategies
    - Enhanced error handling and fallback mechanisms
    """

    config: HyDEAgentConfig = Field(
        default_factory=HyDEAgentConfig, description="Configuration for HyDE agent"
    )

    @model_validator(mode="after")
    @classmethod
    def setup_hyde_agent(cls) -> "EnhancedHyDERAGAgentV2":
        """Setup HyDE agent with enhanced prompts."""
        # Set up tool routing for any additional tools
        if hasattr(self, "tools") and self.tools:
            self.sync_tool_routes_from_tools(self.tools)
        return self

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        embedding_model: str | None = None,
        config: HyDEAgentConfig | None = None,
        **kwargs,
    ) -> "EnhancedHyDERAGAgentV2":
        """Create Enhanced HyDE RAG Agent v2 from documents.

        Args:
            documents: Documents to index for retrieval
            llm_config: LLM configuration
            embedding_model: Optional embedding model
            config: HyDE agent configuration
            **kwargs: Additional arguments

        Returns:
            Configured Enhanced HyDE RAG Agent v2
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        if not config:
            config = HyDEAgentConfig()

        # Create agents based on generation mode
        if config.generation_mode == HyDEGenerationMode.SINGLE:
            agents = cls._create_single_document_pipeline(
                documents, llm_config, embedding_model, config
            )
        elif config.generation_mode == HyDEGenerationMode.MULTI_PERSPECTIVE:
            agents = cls._create_multi_perspective_pipeline(
                documents, llm_config, embedding_model, config
            )
        elif config.generation_mode == HyDEGenerationMode.MULTI_DOMAIN:
            agents = cls._create_multi_domain_pipeline(
                documents, llm_config, embedding_model, config
            )
        elif config.generation_mode == HyDEGenerationMode.ENSEMBLE:
            agents = cls._create_ensemble_pipeline(
                documents, llm_config, embedding_model, config
            )
        else:
            # Fallback to single document
            agents = cls._create_single_document_pipeline(
                documents, llm_config, embedding_model, config
            )

        return cls(
            agents=agents,
            config=config,
            name=kwargs.get(
                "name", f"Enhanced HyDE RAG v2 ({config.generation_mode.value})"
            ),
            **kwargs,
        )

    @classmethod
    def _create_single_document_pipeline(
        cls,
        documents: list[Document],
        llm_config: LLMConfig,
        embedding_model: str | None,
        config: HyDEAgentConfig,
    ) -> list[Agent]:
        """Create pipeline for single document generation."""
        # Step 1: Query analysis and prompt selection
        query_analyzer = QueryAnalysisAgent(
            llm_config=llm_config,
            auto_select=config.auto_select_prompt,
            default_prompt_type=config.prompt_type,
            name="Query Analyzer",
        )

        # Step 2: Document generation using selected prompt
        doc_generator = AdaptiveHyDEGenerator(
            llm_config=llm_config,
            target_length=config.target_length,
            name="Adaptive HyDE Generator",
        )

        # Step 3: Optional structured analysis
        agents = [query_analyzer, doc_generator]

        if config.use_structured_analysis:
            analyzer = HyDEDocumentAnalyzer(
                llm_config=llm_config,
                enable_query_rewriting=config.enable_query_rewriting,
                name="HyDE Document Analyzer",
            )
            agents.append(analyzer)

        # Step 4: Enhanced retrieval
        retriever = EnhancedHyDERetrieverV2(
            documents=documents,
            embedding_model=embedding_model,
            name="Enhanced HyDE Retriever v2",
        )
        agents.append(retriever)

        # Step 5: Answer generation
        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )
        agents.append(answer_agent)

        return agents

    @classmethod
    def _create_multi_perspective_pipeline(
        cls,
        documents: list[Document],
        llm_config: LLMConfig,
        embedding_model: str | None,
        config: HyDEAgentConfig,
    ) -> list[Agent]:
        """Create pipeline for multi-perspective document generation."""
        agents = []

        # Generate documents from different perspectives
        for _i, perspective in enumerate(config.perspectives):
            generator = SimpleAgent(
                engine=AugLLMConfig(
                    llm_config=llm_config,
                    prompt_template=get_perspective_prompt(
                        perspective, config.target_length
                    ),
                    output_key=f"hypothetical_doc_{perspective.value}",
                ),
                name=f"HyDE Generator ({perspective.value})",
            )
            agents.append(generator)

        # Ensemble retrieval using all generated documents
        retriever = EnsembleHyDERetriever(
            documents=documents,
            embedding_model=embedding_model,
            perspectives=[p.value for p in config.perspectives],
            name="Multi-Perspective Retriever",
        )
        agents.append(retriever)

        # Answer generation
        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )
        agents.append(answer_agent)

        return agents

    @classmethod
    def _create_multi_domain_pipeline(
        cls,
        documents: list[Document],
        llm_config: LLMConfig,
        embedding_model: str | None,
        config: HyDEAgentConfig,
    ) -> list[Agent]:
        """Create pipeline for multi-domain document generation."""
        agents = []

        # Query analysis to determine relevant domain types
        domain_analyzer = DomainAnalysisAgent(
            llm_config=llm_config, name="Domain Analyzer"
        )
        agents.append(domain_analyzer)

        # Generate documents for multiple domains
        domain_types = [
            HyDEPromptType.TECHNICAL,
            HyDEPromptType.ACADEMIC,
            HyDEPromptType.GENERAL,
        ]

        for domain_type in domain_types:
            generator = SimpleAgent(
                engine=AugLLMConfig(
                    llm_config=llm_config,
                    prompt_template=get_generation_prompt(
                        domain_type, config.target_length
                    ),
                    output_key=f"hypothetical_doc_{domain_type.value}",
                ),
                name=f"HyDE Generator ({domain_type.value})",
            )
            agents.append(generator)

        # Multi-domain retrieval
        retriever = MultiDomainHyDERetriever(
            documents=documents,
            embedding_model=embedding_model,
            domain_types=[dt.value for dt in domain_types],
            name="Multi-Domain Retriever",
        )
        agents.append(retriever)

        # Answer generation
        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )
        agents.append(answer_agent)

        return agents

    @classmethod
    def _create_ensemble_pipeline(
        cls,
        documents: list[Document],
        llm_config: LLMConfig,
        embedding_model: str | None,
        config: HyDEAgentConfig,
    ) -> list[Agent]:
        """Create pipeline for ensemble document generation."""
        # Single agent that generates multiple documents
        ensemble_generator = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=get_ensemble_prompt(
                    config.num_ensemble_docs, config.target_length
                ),
                output_key="ensemble_documents",
            ),
            name="Ensemble HyDE Generator",
        )

        # Parse ensemble output
        ensemble_parser = EnsembleDocumentParser(
            llm_config=llm_config, name="Ensemble Document Parser"
        )

        # Ensemble retrieval
        retriever = EnsembleHyDERetriever(
            documents=documents,
            embedding_model=embedding_model,
            ensemble_mode=True,
            name="Ensemble Retriever",
        )

        # Answer generation
        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )

        return [ensemble_generator, ensemble_parser, retriever, answer_agent]


# ==============================================================================
# SPECIALIZED AGENTS FOR ENHANCED FUNCTIONALITY
# ==============================================================================


class QueryAnalysisAgent(SimpleAgent):
    """Agent that analyzes queries and selects appropriate prompt types."""

    auto_select: bool = Field(
        default=True, description="Whether to auto-select prompt type"
    )
    default_prompt_type: HyDEPromptType = Field(
        default=HyDEPromptType.GENERAL,
        description="Default prompt type if not auto-selecting",
    )

    def __init__(self, llm_config: LLMConfig, **kwargs):
        analysis_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Analyze the query to determine the best approach for HyDE document generation.

            Consider:
            - Domain (technical, academic, news, business, tutorial, etc.)
            - Question type (factual, procedural, analytical, comparative)
            - Complexity level (beginner, intermediate, expert)
            - Expected document format

            Provide analysis that will guide document generation strategy.""",
                ),
                ("human", "Analyze this query for HyDE generation: {query}"),
            ]
        )

        super().__init__(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=analysis_prompt,
                output_key="query_analysis",
            ),
            **kwargs,
        )

    def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Run query analysis and add prompt type selection."""
        result = super().run(input_data)

        # Auto-select prompt type if enabled
        if self.auto_select:
            query = input_data.get("query", "")
            selected_type = select_prompt_automatically(query)
            result["selected_prompt_type"] = selected_type.value
        else:
            result["selected_prompt_type"] = self.default_prompt_type.value

        return result


class AdaptiveHyDEGenerator(SimpleAgent):
    """Generator that adapts its prompt based on query analysis."""

    target_length: int = Field(default=1000, description="Target document length")

    def __init__(self, llm_config: LLMConfig, **kwargs):
        # Default prompt - will be replaced based on analysis
        default_prompt = get_generation_prompt(
            HyDEPromptType.GENERAL, kwargs.get("target_length", 1000)
        )

        super().__init__(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=default_prompt,
                output_key="hypothetical_document",
            ),
            **kwargs,
        )

    def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate document using adaptively selected prompt."""
        # Get selected prompt type from previous analysis
        prompt_type_str = input_data.get("selected_prompt_type", "general")
        try:
            prompt_type = HyDEPromptType(prompt_type_str)
        except ValueError:
            prompt_type = HyDEPromptType.GENERAL

        # Update engine with appropriate prompt
        new_prompt = get_generation_prompt(prompt_type, self.target_length)
        self.engine.prompt_template = new_prompt

        # Generate document
        result = super().run(input_data)
        result["prompt_type_used"] = prompt_type.value

        return result


class HyDEDocumentAnalyzer(SimpleAgent):
    """Analyzes generated hypothetical documents and extracts structured information."""

    enable_query_rewriting: bool = Field(
        default=True, description="Enable query rewriting"
    )

    def __init__(self, llm_config: LLMConfig, **kwargs):
        # Create both generation and parsing prompts
        generation_prompt, parsing_prompt = create_generation_and_parsing_prompts(
            model_class=HyDEResult,
            generation_instruction="Analyze the hypothetical document and extract structured information.",
            config=PydanticPromptConfig(style=PromptStyle.DESCRIPTIVE),
        )

        super().__init__(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=HYDE_ANALYSIS_PROMPT,
                structured_output_model=HyDEResult,
                output_key="hyde_analysis",
            ),
            **kwargs,
        )


class DomainAnalysisAgent(SimpleAgent):
    """Analyzes queries to determine relevant domains for multi-domain generation."""

    def __init__(self, llm_config: LLMConfig, **kwargs):
        domain_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Analyze the query to determine which document domains would be most valuable.

            Available domains:
            - Technical: Programming, engineering, technical documentation
            - Academic: Research papers, scholarly articles, theoretical content
            - News: Current events, reports, journalistic content
            - Business: Market analysis, corporate documentation, strategy
            - Tutorial: How-to guides, instructional content
            - Reference: Encyclopedia entries, definitions, comprehensive overviews

            Rank the top 3 domains that would provide the best hypothetical documents for this query.""",
                ),
                ("human", "Analyze query for domain relevance: {query}"),
            ]
        )

        super().__init__(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=domain_prompt,
                output_key="domain_analysis",
            ),
            **kwargs,
        )


class EnsembleDocumentParser(SimpleAgent):
    """Parses ensemble document output into individual documents."""

    def __init__(self, llm_config: LLMConfig, **kwargs):
        parser_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Parse the ensemble document output into individual hypothetical documents.

            Extract each document and provide:
            - Document content
            - Document type/style
            - Key topics covered
            - Retrieval keywords

            Structure the output so each document can be used independently for retrieval.""",
                ),
                ("human", "Parse this ensemble output: {ensemble_documents}"),
            ]
        )

        super().__init__(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=parser_prompt,
                output_key="parsed_documents",
            ),
            **kwargs,
        )


# ==============================================================================
# ENHANCED RETRIEVERS
# ==============================================================================


class EnhancedHyDERetrieverV2(Agent):
    """Enhanced retriever with better state handling and fallback mechanisms."""

    documents: list[Document] = Field(default_factory=list)
    embedding_model: str | None = Field(default=None)

    def build_graph(self) -> Any:
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from langgraph.graph import END, START

        graph = BaseGraph(name="EnhancedHyDERetrieverV2")

        def smart_retrieval(state: dict[str, Any]) -> dict[str, Any]:
            """Smart retrieval that handles multiple input formats."""
            # Priority order for retrieval queries
            retrieval_candidates = [
                state.get("hypothetical_document"),  # From adaptive generator
                state.get("refined_query"),  # From structured analysis
                state.get("hypothetical_doc"),  # From analysis result
                state.get("query"),  # Original query as fallback
            ]

            # Find first non-empty candidate
            retrieval_query = None
            for candidate in retrieval_candidates:
                if candidate and isinstance(candidate, str) and candidate.strip():
                    retrieval_query = candidate.strip()
                    break

            if not retrieval_query:
                retrieval_query = state.get("query", "")

            # Perform retrieval
            base_retriever = BaseRAGAgent.from_documents(
                documents=self.documents,
                embedding_model=self.embedding_model,
                name="Base Retrievef",
            )

            try:
                result = base_retriever.run({"query": retrieval_query})
                docs = []

                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents
                elif isinstance(result, dict) and "retrieved_documents" in result:
                    docs = result["retrieved_documents"]

                return {
                    "retrieved_documents": docs,
                    "retrieval_query_used": retrieval_query,
                    "retrieval_method": "hyde_enhanced_v2",
                    "num_retrieved": len(docs),
                }

            except Exception as e:
                return {
                    "retrieved_documents": [],
                    "retrieval_query_used": retrieval_query,
                    "retrieval_method": "error_fallback",
                    "num_retrieved": 0,
                    "error": str(e),
                }

        graph.add_node("smart_retrieve", smart_retrieval)
        graph.add_edge(START, "smart_retrieve")
        graph.add_edge("smart_retrieve", END)

        return graph


class EnsembleHyDERetriever(Agent):
    """Retriever that handles multiple documents for ensemble retrieval."""

    documents: list[Document] = Field(default_factory=list)
    embedding_model: str | None = Field(default=None)
    perspectives: list[str] = Field(default_factory=list)
    ensemble_mode: bool = Field(default=False)

    def build_graph(self) -> Any:
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from langgraph.graph import END, START

        graph = BaseGraph(name="EnsembleHyDERetriever")

        def ensemble_retrieval(state: dict[str, Any]) -> dict[str, Any]:
            """Retrieve using multiple hypothetical documents and combine results."""
            all_docs = []
            queries_used = []

            if self.ensemble_mode:
                # Parse ensemble documents
                parsed_docs = state.get("parsed_documents", [])
                if isinstance(parsed_docs, str):
                    # If it's a string, try to split into individual documents
                    queries_used = [parsed_docs]
                elif isinstance(parsed_docs, list):
                    queries_used = parsed_docs
            else:
                # Multi-perspective mode
                for perspective in self.perspectives:
                    doc_key = f"hypothetical_doc_{perspective}"
                    if state.get(doc_key):
                        queries_used.append(state[doc_key])

            # Fallback to single document if no ensemble/perspective docs
            if not queries_used:
                single_doc = state.get("hypothetical_document") or state.get(
                    "query", ""
                )
                if single_doc:
                    queries_used = [single_doc]

            # Retrieve for each query
            base_retriever = BaseRAGAgent.from_documents(
                documents=self.documents,
                embedding_model=self.embedding_model,
                name="Ensemble Base Retrievef",
            )

            for query in queries_used:
                try:
                    result = base_retriever.run({"query": query})
                    docs = []

                    if hasattr(result, "retrieved_documents"):
                        docs = result.retrieved_documents
                    elif isinstance(result, dict) and "retrieved_documents" in result:
                        docs = result["retrieved_documents"]

                    all_docs.extend(docs)

                except Exception:
                    continue

            # Remove duplicates while preserving order
            seen = set()
            unique_docs = []
            for doc in all_docs:
                doc_id = (
                    hash(doc.page_content)
                    if hasattr(doc, "page_content")
                    else hash(str(doc))
                )
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_docs.append(doc)

            return {
                "retrieved_documents": unique_docs,
                "queries_used": queries_used,
                "retrieval_method": "ensemble_hyde",
                "num_retrieved": len(unique_docs),
                "num_queries": len(queries_used),
            }

        graph.add_node("ensemble_retrieve", ensemble_retrieval)
        graph.add_edge(START, "ensemble_retrieve")
        graph.add_edge("ensemble_retrieve", END)

        return graph


class MultiDomainHyDERetriever(Agent):
    """Retriever that handles documents from multiple domains."""

    documents: list[Document] = Field(default_factory=list)
    embedding_model: str | None = Field(default=None)
    domain_types: list[str] = Field(default_factory=list)

    def build_graph(self) -> Any:
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from langgraph.graph import END, START

        graph = BaseGraph(name="MultiDomainHyDERetriever")

        def multi_domain_retrieval(state: dict[str, Any]) -> dict[str, Any]:
            """Retrieve using documents from multiple domains."""
            all_docs = []
            domain_queries = {}

            # Collect documents from each domain
            for domain in self.domain_types:
                doc_key = f"hypothetical_doc_{domain}"
                if state.get(doc_key):
                    domain_queries[domain] = state[doc_key]

            # Retrieve for each domain
            base_retriever = BaseRAGAgent.from_documents(
                documents=self.documents,
                embedding_model=self.embedding_model,
                name="Multi-Domain Base Retrievef",
            )

            domain_results = {}
            for domain, query in domain_queries.items():
                try:
                    result = base_retriever.run({"query": query})
                    docs = []

                    if hasattr(result, "retrieved_documents"):
                        docs = result.retrieved_documents
                    elif isinstance(result, dict) and "retrieved_documents" in result:
                        docs = result["retrieved_documents"]

                    domain_results[domain] = docs
                    all_docs.extend(docs)

                except Exception:
                    domain_results[domain] = []

            # Remove duplicates
            seen = set()
            unique_docs = []
            for doc in all_docs:
                doc_id = (
                    hash(doc.page_content)
                    if hasattr(doc, "page_content")
                    else hash(str(doc))
                )
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_docs.append(doc)

            return {
                "retrieved_documents": unique_docs,
                "domain_results": domain_results,
                "retrieval_method": "multi_domain_hyde",
                "num_retrieved": len(unique_docs),
                "domains_used": list(domain_queries.keys()),
            }

        graph.add_node("multi_domain_retrieve", multi_domain_retrieval)
        graph.add_edge(START, "multi_domain_retrieve")
        graph.add_edge("multi_domain_retrieve", END)

        return graph


# ==============================================================================
# FACTORY FUNCTIONS
# ==============================================================================


def create_enhanced_hyde_v2(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    generation_mode: HyDEGenerationMode = HyDEGenerationMode.SINGLE,
    auto_select_prompt: bool = True,
    **kwargs,
) -> EnhancedHyDERAGAgentV2:
    """Create Enhanced HyDE RAG Agent v2 with specified configuration.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        generation_mode: Mode for document generation
        auto_select_prompt: Whether to auto-select prompt types
        **kwargs: Additional configuration options

    Returns:
        Configured Enhanced HyDE RAG Agent v2
    """
    config = HyDEAgentConfig(
        generation_mode=generation_mode, auto_select_prompt=auto_select_prompt, **kwargs
    )

    return EnhancedHyDERAGAgentV2.from_documents(
        documents=documents, llm_config=llm_config, config=config
    )


def create_multi_perspective_hyde(
    documents: list[Document],
    perspectives: list[HyDEPerspective],
    llm_config: LLMConfig | None = None,
    **kwargs,
) -> EnhancedHyDERAGAgentV2:
    """Create HyDE agent with multi-perspective generation.

    Args:
        documents: Documents for retrieval
        perspectives: List of perspectives to use
        llm_config: LLM configuration
        **kwargs: Additional options

    Returns:
        Multi-perspective HyDE agent
    """
    config = HyDEAgentConfig(
        generation_mode=HyDEGenerationMode.MULTI_PERSPECTIVE, perspectives=perspectives
    )

    return EnhancedHyDERAGAgentV2.from_documents(
        documents=documents, llm_config=llm_config, config=config, **kwargs
    )


def create_ensemble_hyde(
    documents: list[Document],
    num_docs: int = 3,
    llm_config: LLMConfig | None = None,
    **kwargs,
) -> EnhancedHyDERAGAgentV2:
    """Create HyDE agent with ensemble document generation.

    Args:
        documents: Documents for retrieval
        num_docs: Number of documents to generate
        llm_config: LLM configuration
        **kwargs: Additional options

    Returns:
        Ensemble HyDE agent
    """
    config = HyDEAgentConfig(
        generation_mode=HyDEGenerationMode.ENSEMBLE, num_ensemble_docs=num_docs
    )

    return EnhancedHyDERAGAgentV2.from_documents(
        documents=documents, llm_config=llm_config, config=config, **kwargs
    )
