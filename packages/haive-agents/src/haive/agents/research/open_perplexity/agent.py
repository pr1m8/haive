import importlib
import inspect
import json
import logging

# Import document loader utilities
import pkgutil
from datetime import datetime
from pathlib import Path
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.retriever import create_retriever_from_vectorstore
from haive.core.graph.branches import Branch
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START
from langgraph.types import Command

# Import custom modules
from haive.agents.research.open_perplexity.config import ResearchAgentConfig
from haive.agents.research.open_perplexity.state import (
    ReportSection,
    ResearchState,
)

logger = logging.getLogger(__name__)


@register_agent(ResearchAgentConfig)
class ResearchAgent(Agent[ResearchAgentConfig]):
    """Agent for performing deep research on any topic with dynamic document loader selection."""

    def __init__(self, config: ResearchAgentConfig):
        """Initialize the research agent."""
        super().__init__(config)
        self.config = config
        self.document_loaders = {}
        self.loaded_documents = []

        # Initialize vector store
        self.vectorstore_config = config.vectorstore_config

        # Dictionary to track available document loaders
        self._available_loaders = self._discover_document_loaders()

    @property
    def react_agent(self):
        """Get the ReAct agent for research tasks."""
        if not hasattr(self, "_react_agent"):
            if not self.config.react_agent_name:
                raise ValueError("ReAct agent name not configured")
            self._react_agent = self.load_agent(self.config.react_agent_name)
        return self._react_agent

    @property
    def rag_agent(self):
        """Get the RAG agent for retrieval tasks."""
        if not hasattr(self, "_rag_agent"):
            if not self.config.rag_agent_name:
                logger.warning("RAG agent not configured, will be set up as needed")
                return None
            self._rag_agent = self.load_agent(self.config.rag_agent_name)
        return self._rag_agent

    @property
    def vectorstore(self):
        """Get or create the vector store."""
        if not hasattr(self, "_vectorstore"):
            if not self.vectorstore_config:
                logger.warning("Vector store not configured")
                return None
            self._vectorstore = self.vectorstore_config.build()
        return self._vectorstore

    @property
    def retriever(self):
        """Get or create the retriever from the vector store."""
        if not hasattr(self, "_retriever"):
            if not self.vectorstore:
                logger.warning(
                    "Vector store not available, retriever cannot be created"
                )
                return None
            self._retriever = create_retriever_from_vectorstore(
                self.vectorstore, search_type="similarity", search_kwargs={"k": 5}
            )
        return self._retriever

    def _discover_document_loaders(self) -> dict[str, Any]:
        """Discover available document loaders."""
        import langchain_community.document_loaders as base_loader_pkg

        loader_classes = {}
        for _, module_name, _ in pkgutil.walk_packages(
            base_loader_pkg.__path__, base_loader_pkg.__name__ + "."
        ):
            try:
                module = importlib.import_module(module_name)
            except Exception as e:
                logger.debug(f"Failed to import module {module_name}: {e}")
                continue

            for name, cls in inspect.getmembers(module, inspect.isclass):
                if hasattr(cls, "load") and callable(cls.load):
                    loader_classes[name] = {"class": cls, "module": module_name}

        return loader_classes

    def _create_document_loader(self, loader_name: str, **kwargs) -> Any:
        """Create a document loader instance by name."""
        if loader_name not in self._available_loaders:
            raise ValueError(f"Document loader {loader_name} not found")

        loader_class = self._available_loaders[loader_name]["class"]
        return loader_class(**kwargs)

    def setup_workflow(self) -> None:
        """Set up the research workflow graph."""
        graph_builder = DynamicGraph(ResearchState)

        # Define nodes
        graph_builder.add_node("process_input", self.process_input)
        graph_builder.add_node("extract_topic", self.extract_topic)
        graph_builder.add_node("generate_report_plan", self.generate_report_plan)
        graph_builder.add_node("generate_search_queries", self.generate_search_queries)
        graph_builder.add_node(
            "recommend_document_loaders", self.recommend_document_loaders
        )
        graph_builder.add_node("execute_searches", self.execute_searches)
        graph_builder.add_node("evaluate_sources", self.evaluate_sources)
        graph_builder.add_node("write_section", self.write_section)
        graph_builder.add_node(
            "check_section_completion", self.check_section_completion
        )
        graph_builder.add_node("consolidate_findings", self.consolidate_findings)
        graph_builder.add_node("assess_confidence", self.assess_confidence)
        graph_builder.add_node("compile_final_report", self.compile_final_report)

        # Define edges
        graph_builder.add_edge(START, "process_input")
        graph_builder.add_edge("process_input", "extract_topic")
        graph_builder.add_edge("extract_topic", "generate_report_plan")
        graph_builder.add_edge("generate_report_plan", "generate_search_queries")
        graph_builder.add_edge("generate_search_queries", "recommend_document_loaders")
        graph_builder.add_edge("recommend_document_loaders", "execute_searches")
        graph_builder.add_edge("execute_searches", "evaluate_sources")
        graph_builder.add_edge("evaluate_sources", "write_section")
        graph_builder.add_edge("write_section", "check_section_completion")

        # Branch based on section completion
        with graph_builder.branch("check_section_completion") as branch:
            branch.add(Branch.EQUALS("continue_research", "generate_search_queries"))
            branch.add(Branch.EQUALS("next_section", "generate_search_queries"))
            branch.add(Branch.EQUALS("all_sections_completed", "consolidate_findings"))

        graph_builder.add_edge("consolidate_findings", "assess_confidence")
        graph_builder.add_edge("assess_confidence", "compile_final_report")
        graph_builder.add_edge("compile_final_report", END)

        # Finalize graph
        self.graph = graph_builder.compile()

    def process_input(self, state: ResearchState) -> Command:
        """Process the initial input and set up the research state."""
        self.get_engine("main")

        # Extract the first message if available
        if state.messages:
            message = state.messages[-1]
            state.input_context = message.content

        # Initialize research state
        state.current_step = "process_input"

        return {"next": "extract_topic"}

    def extract_topic(self, state: ResearchState) -> Command:
        """Extract the research topic and question from user input."""
        engine = self.get_engine("topic_extraction")

        input_text = state.input_context or ""

        # Use the topic extraction engine to identify research topic and question
        response = engine.invoke({"input_text": input_text})

        # Update state with extracted information
        if isinstance(response, dict):
            state.research_topic = response.get("research_topic")
            state.research_question = response.get("research_question")
            state.search_parameters = response.get("search_parameters", {})

            # Add additional context if available
            additional_context = response.get("additional_context")
            if additional_context:
                state.input_context = f"{state.input_context or ''}\n\nAdditional context: {additional_context}"

        state.current_step = "extract_topic"

        return {"next": "generate_report_plan"}

    def generate_report_plan(self, state: ResearchState) -> Command:
        """Generate a research report plan with appropriate sections."""
        engine = self.get_engine("report_planning")

        # Start with default sections from config
        initial_sections = self.config.default_report_sections

        # Use the report planning engine to customize sections
        response = engine.invoke(
            {
                "research_topic": state.research_topic,
                "research_question": state.research_question,
                "additional_context": state.input_context,
                "initial_sections": initial_sections,
            }
        )

        # Update state with planned sections
        if isinstance(response, list):
            state.report_sections = []
            for section_data in response:
                section = ReportSection(
                    name=section_data.get("name", "Untitled Section"),
                    description=section_data.get("description", ""),
                    requires_research=section_data.get("requires_research", True),
                    status="pending",
                )
                state.report_sections.append(section)

        # Set first research section as active
        state.current_section_index = 0
        for i, section in enumerate(state.report_sections):
            if section.requires_research:
                state.current_section_index = i
                break

        state.current_step = "generate_report_plan"

        return {"next": "generate_search_queries"}

    def generate_search_queries(self, state: ResearchState) -> Command:
        """Generate search queries for the current section."""
        engine = self.get_engine("query_generation")

        if state.current_section_index is None or state.current_section_index >= len(
            state.report_sections
        ):
            return {"next": "consolidate_findings"}

        current_section = state.report_sections[state.current_section_index]
        current_section.status = "in_progress"

        # Use the query generation engine to create search queries
        response = engine.invoke(
            {
                "research_topic": state.research_topic,
                "research_question": state.research_question,
                "section_name": current_section.name,
                "section_description": current_section.description,
                "num_queries": self.config.concurrent_searches,
            }
        )

        # Update state with generated queries
        if isinstance(response, list):
            current_section.queries = []
            for query_data in response:
                query = {
                    "query": query_data.get("query", ""),
                    "purpose": query_data.get("purpose", ""),
                    "data_source": query_data.get("data_source", "web"),
                    "completed": False,
                    "results": [],
                }
                current_section.queries.append(query)

            # Also store in state for easy access
            state.search_queries = current_section.queries

        state.current_step = "generate_search_queries"

        return {"next": "recommend_document_loaders"}

    def recommend_document_loaders(self, state: ResearchState) -> Command:
        """Recommend document loaders based on queries and data sources."""
        # Get data source types from queries
        data_sources = set()
        for query in state.search_queries:
            data_sources.add(query.get("data_source", "web"))

        # Map data sources to appropriate document loaders
        loader_mapping = {
            "web": ["WebBaseLoader", "RecursiveUrlLoader", "UnstructuredURLLoader"],
            "academic": ["ArxivLoader", "YouTubeLoader"],
            "github": ["GitHubLoader", "GitLoader"],
            "news": ["HNLoader", "NewsURLLoader", "RSSFeedLoader"],
            "pdf": ["PyPDFLoader", "PDFMinerLoader"],
            "document": ["DocxLoader", "TextLoader"],
        }

        # Recommend loaders for each data source
        recommended_loaders = {}
        for source in data_sources:
            source_loaders = loader_mapping.get(source, ["WebBaseLoader"])
            for loader_name in source_loaders:
                if loader_name in self._available_loaders:
                    recommended_loaders[loader_name] = self._available_loaders[
                        loader_name
                    ]

        # Store recommended loaders in state
        state.data_sources = [
            {
                "type": source,
                "recommended_loaders": [
                    loader
                    for loader in loader_mapping.get(source, [])
                    if loader in self._available_loaders
                ],
            }
            for source in data_sources
        ]

        state.current_step = "recommend_document_loaders"

        return {"next": "execute_searches"}

    def execute_searches(self, state: ResearchState) -> Command:
        """Execute searches using appropriate document loaders."""
        if not state.search_queries:
            return {"next": "check_section_completion"}

        # Get current section
        state.report_sections[state.current_section_index]

        # Execute each search query
        for i, query in enumerate(state.search_queries):
            if query.get("completed"):
                continue

            # Select appropriate loader based on data source
            data_source = query.get("data_source", "web")
            query_text = query.get("query", "")

            results = []
            documents = []

            try:
                # Load documents using the appropriate loader
                if data_source == "web":
                    loader = self._create_document_loader(
                        "WebBaseLoader", web_path=query_text
                    )
                    documents = loader.load()

                elif data_source == "academic" and "arxiv" in query_text.lower():
                    loader = self._create_document_loader(
                        "ArxivLoader", query=query_text, load_max_docs=3
                    )
                    documents = loader.load()

                elif data_source == "github" and "/" in query_text:
                    # Assuming format "owner/repo"
                    loader = self._create_document_loader(
                        "GitHubIssuesLoader", repo=query_text
                    )
                    documents = loader.load()

                elif data_source == "news" and query_text.isdigit():
                    # Assuming HN story ID
                    loader = self._create_document_loader(
                        "HNLoader", story_id=int(query_text)
                    )
                    documents = loader.load()

                # Process results
                for doc in documents:
                    # Add to results for this query
                    results.append(
                        {
                            "content": (
                                doc.page_content[:1000] + "..."
                                if len(doc.page_content) > 1000
                                else doc.page_content
                            ),
                            "metadata": doc.metadata,
                        }
                    )

                    # Add to global documents collection
                    state.retrieved_documents.append(doc)
                    self.loaded_documents.append(doc)

                # Add documents to vector store if available
                if self.vectorstore and documents:
                    self.vectorstore.add_documents(documents)
                    state.vectorstore_documents.extend(documents)

            except Exception as e:
                logger.exception(
                    f"Error executing search for query '{query_text}': {e}"
                )
                results.append({"error": str(e), "query": query_text})

            # Update query with results
            query["results"] = results
            query["completed"] = True
            state.search_queries[i] = query

        state.current_step = "execute_searches"

        return {"next": "evaluate_sources"}

    def evaluate_sources(self, state: ResearchState) -> Command:
        """Evaluate and rate the reliability of retrieved sources."""
        engine = self.get_engine("source_evaluation")

        # Get sources from current search queries
        sources = []
        for query in state.search_queries:
            for result in query.get("results", []):
                if "error" in result:
                    continue

                # Extract source info
                content = result.get("content", "")
                metadata = result.get("metadata", {})
                url = metadata.get("source", metadata.get("url", "Unknown"))
                title = metadata.get("title", "Untitled Source")

                # Evaluate each source
                try:
                    evaluation = engine.invoke(
                        {
                            "source_title": title,
                            "source_url": url,
                            "source_content": content,
                            "research_topic": state.research_topic,
                            "research_question": state.research_question,
                        }
                    )

                    if isinstance(evaluation, dict):
                        source = {
                            "url": url,
                            "title": title,
                            "content_snippet": (
                                content[:200] + "..." if len(content) > 200 else content
                            ),
                            "source_type": query.get("data_source", "web"),
                            "reliability": evaluation.get("reliability", "UNKNOWN"),
                            "freshness": evaluation.get("freshness", "UNKNOWN"),
                            "relevance_score": evaluation.get("relevance", 0.5),
                            "query": query.get("query"),
                            "access_timestamp": datetime.now().isoformat(),
                        }
                        sources.append(source)

                except Exception as e:
                    logger.exception(f"Error evaluating source {url}: {e}")

        # Add to sources list
        state.sources.extend(sources)

        # Get current section and update sources
        if (
            state.current_section_index is not None
            and state.current_section_index < len(state.report_sections)
        ):
            current_section = state.report_sections[state.current_section_index]
            current_section.sources.extend(sources)

        state.current_step = "evaluate_sources"

        return {"next": "write_section"}

    def write_section(self, state: ResearchState) -> Command:
        """Write the current section of the report."""
        engine = self.get_engine("section_writing")

        if state.current_section_index is None or state.current_section_index >= len(
            state.report_sections
        ):
            return {"next": "check_section_completion"}

        current_section = state.report_sections[state.current_section_index]

        # Prepare research context with retrieved information
        research_context = ""
        for source in current_section.sources:
            url = source.get("url", "Unknown")
            title = source.get("title", "Untitled")
            reliability = source.get("reliability", "UNKNOWN")
            snippet = source.get("content_snippet", "")

            research_context += f"Source: {title}\n"
            research_context += f"URL: {url}\n"
            research_context += f"Reliability: {reliability}\n"
            research_context += f"Content: {snippet}\n\n"

        # Use RAG if we have documents and a vector store
        if self.retriever and state.vectorstore_documents:
            try:
                query = f"Information about {current_section.name} related to {state.research_topic}"
                relevant_docs = self.retriever.invoke(query)

                research_context += (
                    "Additional relevant information from vector store:\n\n"
                )
                for i, doc in enumerate(relevant_docs[:3]):  # Limit to top 3
                    research_context += f"--- Document {i+1} ---\n"
                    research_context += doc.page_content[:500] + "...\n\n"
            except Exception as e:
                logger.exception(f"Error retrieving documents from vector store: {e}")

        # Use the section writing engine to create content
        response = engine.invoke(
            {
                "section_name": current_section.name,
                "section_description": current_section.description,
                "research_topic": state.research_topic,
                "research_question": state.research_question,
                "research_context": research_context,
            }
        )

        # Update section content
        current_section.content = response
        current_section.status = "completed"

        state.current_step = "write_section"

        return {"next": "check_section_completion"}

    def check_section_completion(self, state: ResearchState) -> str:
        """Check if all sections are completed or if more research is needed."""
        if state.current_section_index is None:
            return "all_sections_completed"

        current_section = state.report_sections[state.current_section_index]

        # Check if we need to do more research for the current section
        if current_section.status != "completed" or not current_section.content:
            return "continue_research"

        # Find the next section that requires research
        next_index = None
        for i, section in enumerate(state.report_sections):
            if (
                i > state.current_section_index
                and section.requires_research
                and section.status != "completed"
            ):
                next_index = i
                break

        if next_index is not None:
            state.current_section_index = next_index
            return "next_section"
        return "all_sections_completed"

    def consolidate_findings(self, state: ResearchState) -> Command:
        """Consolidate findings from all sections."""
        engine = self.get_engine("research_finding")

        # Extract key findings from each section
        findings = []
        for section in state.report_sections:
            if not section.content:
                continue

            # Create a message to the research finding engine
            message = HumanMessage(
                content=f"""
            Research topic: {state.research_topic}
            Research question: {state.research_question}
            Section: {section.name}

            Content:
            {section.content}

            Please extract the key findings from this section.
            """
            )

            try:
                response = engine.invoke({"messages": [message]})
                if isinstance(response, dict):
                    findings.append(response)
            except Exception as e:
                logger.exception(
                    f"Error extracting findings from section {section.name}: {e}"
                )

        # Update state with findings
        state.research_findings = {
            "topic": state.research_topic,
            "question": state.research_question,
            "findings": findings,
        }

        state.current_step = "consolidate_findings"

        return {"next": "assess_confidence"}

    def assess_confidence(self, state: ResearchState) -> Command:
        """Assess confidence in research findings."""
        engine = self.get_engine("confidence_assessment")

        # Count source statistics
        sources_count = len(state.sources)
        high_reliability_sources = sum(
            1 for source in state.sources if source.get("reliability") == "HIGH"
        )
        recent_sources = sum(
            1
            for source in state.sources
            if source.get("freshness") in ["VERY_RECENT", "RECENT"]
        )

        # Format key findings
        key_findings = []
        for finding in state.research_findings.get("findings", []):
            key_findings.append(f"- {finding.get('finding', '')}")

        # Use the confidence assessment engine
        response = engine.invoke(
            {
                "research_topic": state.research_topic,
                "research_question": state.research_question,
                "research_summary": json.dumps(state.research_findings),
                "sources_count": sources_count,
                "high_reliability_sources": high_reliability_sources,
                "recent_sources": recent_sources,
                "key_findings": "\n".join(key_findings),
            }
        )

        # Update state with confidence assessment
        if isinstance(response, dict):
            state.confidence_level = response.get("confidence_level")
            state.confidence_explanation = response.get("explanation")

        state.current_step = "assess_confidence"

        return {"next": "compile_final_report"}

    def compile_final_report(self, state: ResearchState) -> Command:
        """Compile the final research report."""
        engine = self.get_engine("final_report_compilation")

        # Format section content
        section_content = ""
        for section in state.report_sections:
            if section.content:
                section_content += f"## {section.name}\n\n{section.content}\n\n"

        # Format confidence assessment
        confidence_assessment = f"""
        Confidence Level: {state.confidence_level or 'Not assessed'}

        Explanation: {state.confidence_explanation or 'No explanation provided'}
        """

        # Use the report compilation engine
        response = engine.invoke(
            {
                "research_topic": state.research_topic,
                "research_question": state.research_question,
                "confidence_assessment": confidence_assessment,
                "section_content": section_content,
            }
        )

        # Create final report
        state.final_report = response

        # Create output message
        output_message = AIMessage(
            content=f"""
        Research on "{state.research_topic}" completed with {state.confidence_level or 'UNKNOWN'} confidence.

        A comprehensive report has been generated. The report includes:
        - {len(state.report_sections)} sections
        - {len(state.sources)} sources
        - {len(state.research_findings.get('findings', []))} key findings

        You can view or save the full report for detailed information.
        """
        )

        state.messages.append(output_message)

        state.current_step = "compile_final_report"

        return {"next": END}

    def generate_markdown_report(self, state: dict[str, Any]) -> str:
        """Generate a markdown report from the final state."""
        if (
            isinstance(state, dict)
            and "final_report" in state
            and state["final_report"]
        ):
            return state["final_report"]

        # If no final report, create a basic one from sections
        report = (
            f"# Research Report: {state.get('research_topic', 'Untitled Research')}\n\n"
        )

        if state.get("research_question"):
            report += f"**Research Question:** {state['research_question']}\n\n"

        # Add confidence assessment
        if state.get("confidence_level"):
            report += "## Confidence Assessment\n\n"
            report += f"**Confidence Level:** {state['confidence_level']}\n\n"
            if state.get("confidence_explanation"):
                report += f"{state['confidence_explanation']}\n\n"

        # Add sections
        for section in state.get("report_sections", []):
            if section.get("content"):
                report += f"## {section['name']}\n\n"
                report += f"{section['content']}\n\n"

        # Add sources
        if state.get("sources"):
            report += "## Sources\n\n"
            for i, source in enumerate(state["sources"]):
                url = source.get("url", "No URL")
                title = source.get("title", "Untitled")
                report += f"{i+1}. [{title}]({url})\n"

        return report

    def visualize_state(self, state: dict[str, Any]) -> None:
        """Visualize the research state."""
        # Print basic info

        # Print sections
        for _i, section in enumerate(state.get("report_sections", [])):
            "✅" if section.get("status") == "completed" else "⬜"

        # Print source statistics
        sources = state.get("sources", [])
        source_types = {}
        for source in sources:
            source_type = source.get("source_type", "unknown")
            source_types[source_type] = source_types.get(source_type, 0) + 1

        for source_type, _count in source_types.items():
            pass

        # Print findings
        state.get("research_findings", {}).get("findings", [])

        # Print current step

    def save_state_history(self, file_path: str | None = None) -> str:
        """Save the state history to a file."""
        if not hasattr(self, "state_history"):
            logger.warning("No state history to save")
            return None

        # Create default file path if not provided
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"research_state_history_{timestamp}.json"

        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Save state history
        try:
            with open(file_path, "w") as f:
                json.dump(self.state_history, f, default=str, indent=2)
            logger.info(f"State history saved to {file_path}")
            return file_path
        except Exception as e:
            logger.exception(f"Error saving state history: {e}")
            return None
