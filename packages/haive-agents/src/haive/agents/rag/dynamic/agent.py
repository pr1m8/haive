import logging
import time

from haive.core.engine.agent.agent import register_agent
from haive.core.graph import DynamicGraph
from langgraph.graph import END, START

from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.dynamic.config import DynamicRAGConfig

logger = logging.getLogger(__name__)


@register_agent(DynamicRAGConfig)
class DynamicRAGAgent(BaseRAGAgent):
    """Implements a dynamic RAG pipeline that routes queries to appropriate data sources."""

    def __init__(self, config: DynamicRAGConfig):
        super().__init__(config)
        self._init_data_sources()
        self._init_router()
        self._init_merger()

    def _init_data_sources(self):
        """Initialize all configured data sources."""
        self.retrievers = {}
        for name, source_config in self.config.data_sources.items():
            try:
                self.retrievers[name] = source_config.create_retriever()
                logger.info(f"Initialized data source: {name}")
            except Exception as e:
                logger.exception(f"Failed to initialize data source {name}: {e}")

    def _init_router(self):
        """Initialize the query router."""
        if self.config.query_router_config:
            self.router = self.config.query_router_config.create_runnable()
        else:
            self.router = None

    def _init_merger(self):
        """Initialize the result merger."""
        if self.config.result_merger_config:
            self.merger = self.config.result_merger_config.create_runnable()
        else:
            self.merger = None

    def route_query(self, state):
        """Route the query to appropriate data sources."""
        query = state.query

        if not self.router:
            # Use default source or all sources if no router
            if (
                self.config.default_source
                and self.config.default_source in self.retrievers
            ):
                selected_sources = [self.config.default_source]
            else:
                selected_sources = list(self.retrievers.keys())

            return {"selected_sources": selected_sources}

        # Use router to select data sources
        try:
            # Prepare input for router with available sources
            source_descriptions = {
                name: config.description
                for name, config in self.config.data_sources.items()
            }

            router_result = self.router.invoke(
                {"query": query, "available_sources": source_descriptions}
            )

            if isinstance(router_result, dict):
                selected_sources = router_result.get("selected_sources", [])
                explanation = router_result.get("explanation", "")
            elif isinstance(router_result, list):
                selected_sources = router_result
                explanation = ""
            else:
                # Try to parse from string
                try:
                    import json

                    selected_sources = json.loads(router_result)
                    if not isinstance(selected_sources, list):
                        selected_sources = [router_result]
                    explanation = ""
                except:
                    selected_sources = [router_result]
                    explanation = ""

            # Validate that sources exist
            validated_sources = [s for s in selected_sources if s in self.retrievers]

            # Limit number of sources if needed
            if len(validated_sources) > self.config.max_sources_per_query:
                validated_sources = validated_sources[
                    : self.config.max_sources_per_query
                ]

            if not validated_sources and self.config.default_source:
                validated_sources = [self.config.default_source]

            return {
                "selected_sources": validated_sources,
                "routing_explanation": explanation,
            }

        except Exception as e:
            logger.exception(f"Error in query routing: {e}")

            # Fall back to default source
            if (
                self.config.default_source
                and self.config.default_source in self.retrievers
            ):
                return {"selected_sources": [self.config.default_source]}

            # Or use all sources as last resort
            return {"selected_sources": list(self.retrievers.keys())}

    def retrieve_from_sources(self, state):
        """Retrieve documents from selected sources."""
        query = state.query
        selected_sources = state.selected_sources

        source_documents = {}
        source_metrics = {}

        if self.config.enable_parallel_retrieval:
            # Implement parallel retrieval with concurrent.futures or asyncio
            import concurrent.futures

            def retrieve_from_source(source_name):
                try:
                    retriever = self.retrievers.get(source_name)
                    if retriever:
                        start_time = time.time()
                        docs = retriever.invoke(query)
                        retrieve_time = time.time() - start_time

                        return (
                            source_name,
                            docs,
                            {
                                "retrieve_time": retrieve_time,
                                "document_count": len(docs),
                            },
                        )
                    return source_name, [], {"error": "Retriever not found"}
                except Exception as e:
                    return source_name, [], {"error": str(e)}

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(retrieve_from_source, source)
                    for source in selected_sources
                ]

                for future in concurrent.futures.as_completed(futures):
                    try:
                        source_name, docs, metrics = future.result()
                        source_documents[source_name] = docs
                        source_metrics[source_name] = metrics
                    except Exception as e:
                        logger.exception(f"Error in parallel retrieval: {e}")

        else:
            # Sequential retrieval
            for source_name in selected_sources:
                retriever = self.retrievers.get(source_name)
                if retriever:
                    try:
                        start_time = time.time()
                        docs = retriever.invoke(query)
                        retrieve_time = time.time() - start_time

                        source_documents[source_name] = docs
                        source_metrics[source_name] = {
                            "retrieve_time": retrieve_time,
                            "document_count": len(docs),
                        }
                    except Exception as e:
                        logger.exception(f"Error retrieving from {source_name}: {e}")
                        source_documents[source_name] = []
                        source_metrics[source_name] = {"error": str(e)}

        return {"source_documents": source_documents, "source_metrics": source_metrics}

    def merge_results(self, state):
        """Merge results from multiple sources."""
        source_documents = state.source_documents

        if not source_documents:
            return {"retrieved_documents": []}

        # If only one source has results, use them directly
        if len(source_documents) == 1:
            source_name = next(iter(source_documents.keys()))
            return {"retrieved_documents": source_documents[source_name]}

        # Flatten all documents
        all_docs = []
        for source_name, docs in source_documents.items():
            # Add source to metadata
            for doc in docs:
                doc.metadata["source"] = source_name
            all_docs.extend(docs)

        if not self.merger:
            # Simple deduplication and selection
            unique_docs = {}
            for doc in all_docs:
                doc_id = doc.metadata.get("id", hash(doc.page_content))
                if doc_id not in unique_docs:
                    unique_docs[doc_id] = doc

            # Sort by "relevance" if available in metadata
            sorted_docs = sorted(
                unique_docs.values(),
                key=lambda d: d.metadata.get("relevance", 0),
                reverse=True,
            )

            # Limit to a reasonable number
            return {"retrieved_documents": sorted_docs[:10]}

        # Use merger for more sophisticated merging
        try:
            # Group documents by source for the merger
            docs_by_source = {
                source: docs for source, docs in source_documents.items() if docs
            }

            merged_docs = self.merger.invoke(
                {"query": state.query, "docs_by_source": docs_by_source}
            )

            if isinstance(merged_docs, list):
                return {"retrieved_documents": merged_docs}
            if isinstance(merged_docs, dict) and "documents" in merged_docs:
                return {"retrieved_documents": merged_docs["documents"]}
            logger.error(f"Unexpected merger output format: {type(merged_docs)}")
            # Fall back to simple deduplication
            unique_docs = {}
            for doc in all_docs:
                doc_id = doc.metadata.get("id", hash(doc.page_content))
                if doc_id not in unique_docs:
                    unique_docs[doc_id] = doc

            return {"retrieved_documents": list(unique_docs.values())}

        except Exception as e:
            logger.exception(f"Error in result merging: {e}")
            # Fall back to all documents
            return {"retrieved_documents": all_docs}

    def setup_workflow(self):
        """Set up the Dynamic RAG workflow."""
        gb = DynamicGraph(state_schema=self.state_schema)

        # Add nodes
        gb.add_node("route_query", self.route_query)
        gb.add_node("retrieve_from_sources", self.retrieve_from_sources)
        gb.add_node("merge_results", self.merge_results)
        gb.add_node("filter_documents", self.filter_documents)
        gb.add_node("generate_answer", self.generate_answer)

        # Connect nodes
        gb.add_edge(START, "route_query")
        gb.add_edge("route_query", "retrieve_from_sources")
        gb.add_edge("retrieve_from_sources", "merge_results")
        gb.add_edge("merge_results", "filter_documents")
        gb.add_edge("filter_documents", "generate_answer")
        gb.add_edge("generate_answer", END)

        # Build the graph
        self.graph = gb.build()
