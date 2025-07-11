from haive.core.engine.agent.agent import register_agent
from haive.core.graph import DynamicGraph
from langgraph.graph import END, START

from haive.agents.rag.multi_strategy.config import MultiStrategyRAGConfig
from haive.agents.rag.multi_strategy.query_types import QueryType
from haive.agents.rag.self_corr.agent import SelfCorrectiveRAGAgent


@register_agent(MultiStrategyRAGConfig)
class MultiStrategyRAGAgent(SelfCorrectiveRAGAgent):
    """RAG agent with multiple retrieval strategies."""

    def _init_components(self):
        """Initialize components for multiple strategies."""
        super()._init_components()
        self.query_analyzer = self._create_query_analyzer()
        self.query_rewriter = self._create_query_rewriter()
        self.retriever_strategies = self._create_retriever_strategies()

    def _create_query_analyzer(self):
        """Create a query analyzer from the configuration."""
        if self.config.query_analyzer_config:
            return self.config.query_analyzer_config.create_runnable()
        return None

    def _create_query_rewriter(self):
        """Create a query rewriter from the configuration."""
        if self.config.query_rewriter_config:
            return self.config.query_rewriter_config.create_runnable()
        return None

    def _create_retriever_strategies(self):
        """Create specialized retrievers from the configuration."""
        strategies = {}
        for name, config in self.config.retriever_strategies.items():
            strategies[name] = config.create_retriever()
        return strategies

    def analyze_query(self, state):
        """Analyze the query to determine the appropriate strategy."""
        query = state.query

        if not self.query_analyzer:
            return {"query_type": QueryType.FACTUAL.value, "strategy_name": "default"}

        analysis = self.query_analyzer.invoke({"query": query})

        if isinstance(analysis, dict):
            query_type = analysis.get("query_type", QueryType.FACTUAL.value)
        else:
            # Try to extract query type from text response
            text = analysis.lower()
            if "temporal" in text or "time" in text or "when" in text:
                query_type = QueryType.TEMPORAL.value
            elif "relation" in text or "connection" in text or "between" in text:
                query_type = QueryType.RELATIONAL.value
            elif "analytical" in text or "analyze" in text or "why" in text:
                query_type = QueryType.ANALYTICAL.value
            else:
                query_type = QueryType.FACTUAL.value

        # Map query type to strategy
        strategy_mapping = {
            QueryType.FACTUAL.value: "default",
            QueryType.ANALYTICAL.value: "analytical",
            QueryType.TEMPORAL.value: "temporal",
            QueryType.RELATIONAL.value: "relational",
        }

        strategy_name = strategy_mapping.get(query_type, "default")

        return {"query_type": query_type, "strategy_name": strategy_name}

    def rewrite_query(self, state):
        """Generate variations of the query for better retrieval."""
        query = state.query

        if not self.query_rewriter:
            return {"query_variations": [], "rewritten_query": None}

        rewrite_result = self.query_rewriter.invoke({"query": query})

        if isinstance(rewrite_result, dict):
            variations = rewrite_result.get("variations", [])
        elif isinstance(rewrite_result, list):
            variations = rewrite_result
        else:
            # Try to parse variations from text
            try:
                variations = [
                    q.strip() for q in rewrite_result.split("\n") if q.strip()
                ]
            except:
                variations = []

        rewritten_query = variations[0] if variations else None

        return {"query_variations": variations, "rewritten_query": rewritten_query}

    def retrieve_with_strategy(self, state):
        """Retrieve documents using the selected strategy."""
        query = state.query
        rewritten_query = state.rewritten_query
        strategy_name = state.strategy_name

        # Use the appropriate retriever for the strategy
        retriever = self.retriever_strategies.get(strategy_name, self.retriever)

        # Use rewritten query if available
        effective_query = rewritten_query if rewritten_query else query

        documents = retriever.invoke(effective_query)

        metrics = {
            "strategy_used": strategy_name,
            "query_used": effective_query,
            "document_count": len(documents),
        }

        return {"retrieved_documents": documents, "strategy_metrics": metrics}

    def setup_workflow(self):
        """Set up the multi-strategy RAG workflow."""
        from haive.core.graph.branches import Branch

        gb = DynamicGraph(state_schema=self.state_schema)

        # Add nodes
        gb.add_node("analyze_query", self.analyze_query)
        gb.add_node("rewrite_query", self.rewrite_query)
        gb.add_node("retrieve_with_strategy", self.retrieve_with_strategy)
        gb.add_node("filter_documents", self.filter_documents)
        gb.add_node("generate_answer", self.generate_answer)
        gb.add_node("evaluate_answer", self.evaluate_answer)
        gb.add_node("correct_answer", self.correct_answer)
        gb.add_node("finalize_answer", self.finalize_answer)

        # Connect nodes
        gb.add_edge(START, "analyze_query")
        gb.add_edge("analyze_query", "rewrite_query")
        gb.add_edge("rewrite_query", "retrieve_with_strategy")
        gb.add_edge("retrieve_with_strategy", "filter_documents")
        gb.add_edge("filter_documents", "generate_answer")
        gb.add_edge("generate_answer", "evaluate_answer")

        # Add conditional branch for correction
        correction_branch = Branch(
            function=self.decide_correction,
            destinations={"correct": "correct_answer", "finalize": "finalize_answer"},
        )
        gb.add_conditional_edges("evaluate_answer", correction_branch)

        # Connect correction back to evaluation
        gb.add_edge("correct_answer", "evaluate_answer")
        gb.add_edge("finalize_answer", END)

        # Build the graph
        self.graph = gb.build()
