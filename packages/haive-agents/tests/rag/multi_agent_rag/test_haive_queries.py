"""Tests for Haive Query Processing and RAG Integration.

Run with: poetry run pytest packages/haive-agents/tests/rag/multi_agent_rag/test_haive_queries.py -v
"""

from langchain_core.documents import Document
import pytest

from haive.agents.rag.multi_agent_rag import (
    BaseRAGMultiAgent,
    ConditionalRAGMultiAgent,
    DocumentGradingAgent,
    MultiAgentRAGState,
    SimpleRAGAgent,
    SimpleRAGAnswerAgent,
)
from haive.core.fixtures.documents import (
    news_documents,
    technical_documents,
)


class TestHaiveSpecificQueries:
    """Test RAG system with Haive-specific queries and content."""

    def test_haive_framework_query(self):
        """Test querying about Haive framework."""
        # Create Haive-specific documents
        haive_docs = [
            Document(
                page_content="Haive is a multi-agent framework for building complex AI systems. It supports agent composition, state management, and workflow orchestration.",
                metadata={"source": "haive_docs", "category": "framework"},
            ),
            Document(
                page_content="The StateSchema in Haive provides structured state management with reducer fields and shared fields for multi-agent coordination.",
                metadata={"source": "haive_docs", "category": "state_management"},
            ),
            Document(
                page_content="Haive agents can be composed using SequentialAgent, ParallelAgent, and ConditionalAgent for different execution patterns.",
                metadata={"source": "haive_docs", "category": "agent_composition"},
            ),
            Document(
                page_content="LangGraph integration in Haive allows for building complex stateful workflows with proper message handling.",
                metadata={"source": "haive_docs", "category": "langgraph"},
            ),
        ]

        # Create RAG agent with Haive documents
        rag_agent = SimpleRAGAgent.from_documents(
            documents=haive_docs, name="Haive RAG Agent"
        )

        # Test retrieval for Haive-specific query
        retrieved = rag_agent.retrieve_documents(
            "How does Haive handle agent composition?"
        )

        assert len(retrieved) > 0

        # Should retrieve agent composition related documents
        composition_docs = [
            doc
            for doc in retrieved
            if "composition" in doc.page_content.lower()
            or "SequentialAgent" in doc.page_content
        ]
        assert len(composition_docs) > 0

    def test_haive_state_management_query(self):
        """Test querying about Haive state management."""
        state_docs = [
            Document(
                page_content="StateSchema in Haive defines the structure of agent state with typed fields, shared fields, and reducer functions.",
                metadata={"topic": "state_schema"},
            ),
            Document(
                page_content="Shared fields in Haive state are accessible across all agents in a multi-agent system, enabling coordination.",
                metadata={"topic": "shared_fields"},
            ),
            Document(
                page_content="Reducer fields in Haive automatically merge state updates using functions like operator.add for lists.",
                metadata={"topic": "reducer_fields"},
            ),
            Document(
                page_content="Message handling in Haive preserves tool_call_id and other important fields across agent boundaries.",
                metadata={"topic": "message_handling"},
            ),
        ]

        # Create complete RAG system
        system = BaseRAGMultiAgent(
            retrieval_agent=SimpleRAGAgent.from_documents(
                state_docs, name="State Docs Agent"
            ),
            grading_agent=DocumentGradingAgent(name="State Grader"),
            answer_agent=SimpleRAGAnswerAgent(name="State Answer Agent"),
        )

        # Test with state management query
        initial_state = MultiAgentRAGState(
            query="How do shared fields work in Haive StateSchema?"
        )

        # Run retrieval
        retrieval_result = system.agents[0].run_retrieval(initial_state)
        initial_state.retrieved_documents = retrieval_result["retrieved_documents"]

        # Should retrieve documents about shared fields
        shared_field_docs = [
            doc
            for doc in initial_state.retrieved_documents
            if "shared" in doc.page_content.lower()
        ]
        assert len(shared_field_docs) > 0

        # Run grading
        grading_result = system.agents[1].run_grading(initial_state)
        initial_state.graded_documents = grading_result["graded_documents"]
        initial_state.filtered_documents = grading_result["filtered_documents"]

        # Should have relevant documents after grading
        assert len(initial_state.filtered_documents) > 0

    def test_multi_agent_workflow_query(self):
        """Test query about multi-agent workflows."""
        workflow_docs = [
            Document(
                page_content="SequentialAgent in Haive executes agents one after another, with state flowing between them for pipeline processing.",
                metadata={"workflow_type": "sequential"},
            ),
            Document(
                page_content="ParallelAgent runs multiple agents simultaneously on the same input, useful for consensus building or independent analysis.",
                metadata={"workflow_type": "parallel"},
            ),
            Document(
                page_content="ConditionalAgent uses dynamic routing based on conditions to decide which agent should execute next in the workflow.",
                metadata={"workflow_type": "conditional"},
            ),
            Document(
                page_content="Multi-agent systems in Haive support automatic schema composition with intelligent field separation and message preservation.",
                metadata={"workflow_type": "general"},
            ),
        ]

        # Test conditional RAG system
        conditional_system = ConditionalRAGMultiAgent(
            retrieval_agent=SimpleRAGAgent.from_documents(
                workflow_docs, name="Workflow Agent"
            ),
            name="Workflow RAG System",
        )

        assert len(conditional_system.agents) >= 3
        assert conditional_system.state_schema == MultiAgentRAGState

    def test_haive_engine_integration_query(self):
        """Test querying about Haive engine integration."""
        engine_docs = [
            Document(
                page_content="AugLLMConfig in Haive provides configuration for augmented language models with tool support and structured outputs.",
                metadata={"component": "engine", "type": "aug_llm"},
            ),
            Document(
                page_content="Engine nodes in Haive graphs wrap engines and handle input/output schema validation and transformation.",
                metadata={"component": "graph", "type": "engine_node"},
            ),
            Document(
                page_content="Tool integration in Haive engines supports both LangChain tools and custom Pydantic-based tools.",
                metadata={"component": "tools", "type": "integration"},
            ),
            Document(
                page_content="Structured output models in Haive engines ensure type-safe responses and automatic parsing.",
                metadata={"component": "output", "type": "structured"},
            ),
        ]

        # Create agent and test complex query
        engine_agent = SimpleRAGAgent.from_documents(
            documents=engine_docs, name="Engine Integration Agent"
        )

        # Test retrieval with technical query
        retrieved = engine_agent.retrieve_documents(
            "How do AugLLMConfig and engine nodes work together in Haive?"
        )

        assert len(retrieved) > 0

        # Should find documents about both AugLLMConfig and engine nodes
        aug_llm_docs = [doc for doc in retrieved if "AugLLMConfig" in doc.page_content]
        engine_node_docs = [
            doc for doc in retrieved if "engine node" in doc.page_content.lower()
        ]

        # Should find relevant documents for the query
        assert len(aug_llm_docs) > 0 or len(engine_node_docs) > 0


class TestComplexHaiveQueries:
    """Test complex, multi-faceted queries about Haive."""

    def test_multi_step_haive_query(self):
        """Test complex query requiring multiple retrieval steps."""
        # Comprehensive Haive documentation
        haive_comprehensive_docs = [
            Document(
                page_content="Haive framework architecture consists of agents, engines, graphs, and state management components working together.",
                metadata={"section": "architecture", "level": "overview"},
            ),
            Document(
                page_content="Agent composition in Haive allows building complex workflows by combining SimpleAgent, ReactAgent, and multi-agent systems.",
                metadata={"section": "agents", "level": "composition"},
            ),
            Document(
                page_content="State schemas in Haive use Pydantic models with special annotations for shared fields, reducer fields, and engine mappings.",
                metadata={"section": "state", "level": "schema"},
            ),
            Document(
                page_content="Graph building in Haive automatically handles node creation, edge configuration, and state flow validation.",
                metadata={"section": "graphs", "level": "building"},
            ),
            Document(
                page_content="Engine integration supports multiple LLM providers, tool systems, and output formats through unified interfaces.",
                metadata={"section": "engines", "level": "integration"},
            ),
            Document(
                page_content="Debugging and monitoring in Haive provides detailed logging, state inspection, and execution tracing capabilities.",
                metadata={"section": "debugging", "level": "monitoring"},
            ),
        ]

        # Create sophisticated RAG system
        system = BaseRAGMultiAgent(
            retrieval_agent=SimpleRAGAgent.from_documents(
                haive_comprehensive_docs, name="Comprehensive Haive Agent"
            ),
            grading_agent=DocumentGradingAgent(
                min_relevance_threshold=0.3, name="Haive Grader"
            ),
            answer_agent=SimpleRAGAnswerAgent(
                use_citations=True, name="Haive Answer Agent"
            ),
        )

        # Complex query about Haive architecture
        complex_query = "How do agents, engines, and state schemas work together in Haive to create multi-agent systems?"

        state = MultiAgentRAGState(query=complex_query)

        # Simulate full workflow
        # Step 1: Retrieval
        retrieval_result = system.agents[0].run_retrieval(state)
        state.retrieved_documents = retrieval_result["retrieved_documents"]

        # Should retrieve multiple relevant documents
        assert len(state.retrieved_documents) >= 2

        # Step 2: Grading
        grading_result = system.agents[1].run_grading(state)
        state.graded_documents = grading_result["graded_documents"]
        state.filtered_documents = grading_result["filtered_documents"]

        # Should have some relevant documents after grading
        relevant_docs = [doc for doc in state.graded_documents if doc.is_relevant]
        assert len(relevant_docs) > 0

        # Step 3: Answer generation
        answer_result = system.agents[2].run_generation(state)

        assert "generated_answer" in answer_result
        assert (
            len(answer_result["generated_answer"]) > 50
        )  # Should be substantial answer

    def test_haive_troubleshooting_query(self):
        """Test troubleshooting-style queries about Haive."""
        troubleshooting_docs = [
            Document(
                page_content="Common Haive error: 'Schema validation failed' - usually caused by mismatched input/output schemas between agents.",
                metadata={"type": "error", "category": "schema"},
            ),
            Document(
                page_content="Tool execution failures in Haive often result from missing tool registrations or incorrect tool routing configurations.",
                metadata={"type": "error", "category": "tools"},
            ),
            Document(
                page_content="State serialization issues in Haive can be resolved by ensuring all state fields are JSON-serializable or using custom serializers.",
                metadata={"type": "error", "category": "serialization"},
            ),
            Document(
                page_content="Memory issues in large Haive workflows can be addressed by using checkpointing, state pruning, or streaming processing.",
                metadata={"type": "solution", "category": "performance"},
            ),
            Document(
                page_content="Debug mode in Haive enables detailed logging, state snapshots, and execution tracing for workflow analysis.",
                metadata={"type": "solution", "category": "debugging"},
            ),
        ]

        troubleshooting_agent = SimpleRAGAgent.from_documents(
            troubleshooting_docs, name="Haive Troubleshooting Agent"
        )

        # Test troubleshooting query
        error_query = "My Haive agents are failing with schema validation errors, how do I fix this?"

        retrieved = troubleshooting_agent.retrieve_documents(error_query)

        # Should find schema-related troubleshooting docs
        schema_docs = [
            doc
            for doc in retrieved
            if "schema" in doc.page_content.lower()
            and "error" in doc.page_content.lower()
        ]
        assert len(schema_docs) > 0

    def test_haive_performance_optimization_query(self):
        """Test performance optimization queries."""
        performance_docs = [
            Document(
                page_content="Haive performance can be optimized by using parallel agent execution for independent tasks and sequential for dependent workflows.",
                metadata={"topic": "optimization", "aspect": "execution"},
            ),
            Document(
                page_content="Memory optimization in Haive involves strategic use of shared fields, efficient state schemas, and periodic state cleanup.",
                metadata={"topic": "optimization", "aspect": "memory"},
            ),
            Document(
                page_content="LLM call optimization in Haive includes batching requests, caching responses, and using structured outputs to reduce token usage.",
                metadata={"topic": "optimization", "aspect": "llm"},
            ),
            Document(
                page_content="Graph compilation optimization in Haive reduces runtime overhead through static analysis and pre-computation of execution paths.",
                metadata={"topic": "optimization", "aspect": "compilation"},
            ),
        ]

        # Test with grading for relevance
        grading_agent = DocumentGradingAgent(
            min_relevance_threshold=0.4, name="Performance Grader"
        )

        state = MultiAgentRAGState(
            query="How can I optimize the performance of my Haive multi-agent system?",
            retrieved_documents=performance_docs,
        )

        grading_result = grading_agent.run_grading(state)

        # All documents should be relevant to performance optimization
        relevant_docs = [
            doc for doc in grading_result["graded_documents"] if doc.is_relevant
        ]
        assert len(relevant_docs) >= 2  # Most should be relevant


class TestHaiveQueryIntegration:
    """Integration tests for Haive queries with real document collections."""

    def test_mixed_content_haive_query(self):
        """Test Haive queries against mixed content types."""
        # Mix technical docs with Haive-specific content
        mixed_haive_docs = [
            *technical_documents[:2],  # Some general technical content
            Document(
                page_content="Haive SimpleAgent provides streamlined agent creation with automatic schema management and tool integration.",
                metadata={"source": "haive", "component": "simple_agent"},
            ),
            Document(
                page_content="ReactAgent in Haive implements reasoning and acting patterns with tool use and iterative problem solving.",
                metadata={"source": "haive", "component": "react_agent"},
            ),
            *news_documents[:1],  # Some news content
        ]

        # Create system with mixed content
        mixed_system = BaseRAGMultiAgent(
            retrieval_agent=SimpleRAGAgent.from_documents(
                mixed_haive_docs, name="Mixed Content Agent"
            ),
            grading_agent=DocumentGradingAgent(
                min_relevance_threshold=0.3, name="Mixed Grader"
            ),
        )

        # Query specifically about Haive
        haive_query = (
            "What are the differences between SimpleAgent and ReactAgent in Haive?"
        )

        state = MultiAgentRAGState(query=haive_query)

        # Run retrieval
        retrieval_result = mixed_system.agents[0].run_retrieval(state)
        state.retrieved_documents = retrieval_result["retrieved_documents"]

        # Run grading
        grading_result = mixed_system.agents[1].run_grading(state)

        # Should preferentially select Haive-specific documents
        haive_docs_in_graded = [
            doc
            for doc in grading_result["graded_documents"]
            if "haive" in doc.document.page_content.lower() and doc.is_relevant
        ]

        assert len(haive_docs_in_graded) > 0

    def test_educational_haive_content(self):
        """Test educational queries about Haive concepts."""
        educational_haive_docs = [
            Document(
                page_content="Tutorial: Getting started with Haive involves installing the framework, creating your first agent, and running a simple workflow.",
                metadata={"type": "tutorial", "level": "beginner"},
            ),
            Document(
                page_content="Advanced Haive patterns include custom engine development, complex state schemas, and multi-agent orchestration strategies.",
                metadata={"type": "tutorial", "level": "advanced"},
            ),
            Document(
                page_content="Common mistakes in Haive development include improper schema design, missing tool registrations, and inefficient state management.",
                metadata={"type": "tutorial", "level": "intermediate"},
            ),
            Document(
                page_content="Best practices for Haive include using type hints, proper error handling, comprehensive testing, and clear documentation.",
                metadata={"type": "best_practices", "level": "intermediate"},
            ),
        ]

        # Test with educational query
        educational_agent = SimpleRAGAgent.from_documents(
            educational_haive_docs, name="Haive Education Agent"
        )

        learning_query = "What are the best practices for developing with Haive?"

        retrieved = educational_agent.retrieve_documents(learning_query)

        # Should find best practices documents
        best_practice_docs = [
            doc
            for doc in retrieved
            if "best practices" in doc.page_content.lower()
            or "practices" in doc.metadata.get("type", "")
        ]

        assert len(best_practice_docs) > 0

    def test_comparative_haive_query(self):
        """Test comparative queries about Haive vs other frameworks."""
        comparative_docs = [
            Document(
                page_content="Haive differs from LangGraph by providing higher-level abstractions for agent composition and automatic schema management.",
                metadata={"comparison": "langgraph", "aspect": "abstraction"},
            ),
            Document(
                page_content="Unlike CrewAI, Haive focuses on stateful workflows with strong typing and comprehensive state management capabilities.",
                metadata={"comparison": "crewai", "aspect": "state_management"},
            ),
            Document(
                page_content="Haive provides more structured agent orchestration compared to AutoGen, with explicit state schemas and execution patterns.",
                metadata={"comparison": "autogen", "aspect": "orchestration"},
            ),
            Document(
                page_content="LangChain integration in Haive allows leveraging existing tools while providing better multi-agent coordination.",
                metadata={"comparison": "langchain", "aspect": "integration"},
            ),
        ]

        # Test comparative query
        comparative_agent = SimpleRAGAgent.from_documents(
            comparative_docs, name="Comparative Analysis Agent"
        )

        comparison_query = (
            "How does Haive compare to LangGraph for building multi-agent systems?"
        )

        retrieved = comparative_agent.retrieve_documents(comparison_query)

        # Should find LangGraph comparison docs
        langgraph_docs = [
            doc for doc in retrieved if "langgraph" in doc.page_content.lower()
        ]

        assert len(langgraph_docs) > 0


class TestQueryComplexity:
    """Test handling of varying query complexity levels."""

    def test_simple_haive_query(self):
        """Test simple, single-concept queries."""
        simple_docs = [
            Document(
                page_content="Haive agents are the basic building blocks of the framework.",
                metadata={},
            ),
            Document(
                page_content="StateSchema defines the structure of agent state.",
                metadata={},
            ),
            Document(
                page_content="Engines power the execution of agent logic.", metadata={}
            ),
        ]

        agent = SimpleRAGAgent.from_documents(simple_docs, name="Simple Query Agent")

        simple_query = "What are Haive agents?"
        retrieved = agent.retrieve_documents(simple_query)

        assert len(retrieved) > 0
        agents_docs = [doc for doc in retrieved if "agents" in doc.page_content.lower()]
        assert len(agents_docs) > 0

    def test_complex_multi_concept_query(self):
        """Test complex queries involving multiple concepts."""
        complex_docs = [
            Document(
                page_content="Haive StateSchema with shared fields enables coordination between SequentialAgent and ParallelAgent execution patterns.",
                metadata={
                    "concepts": [
                        "state_schema",
                        "shared_fields",
                        "sequential",
                        "parallel",
                    ]
                },
            ),
            Document(
                page_content="Engine configuration in multi-agent systems requires careful schema alignment and tool routing considerations.",
                metadata={"concepts": ["engines", "multi_agent", "schemas", "tools"]},
            ),
            Document(
                page_content="Conditional routing in Haive allows dynamic workflow adaptation based on agent outputs and state conditions.",
                metadata={
                    "concepts": ["conditional", "routing", "dynamic", "workflow"]
                },
            ),
        ]

        complex_agent = SimpleRAGAgent.from_documents(
            complex_docs, name="Complex Query Agent"
        )

        # Multi-concept query
        complex_query = "How do StateSchema shared fields work with SequentialAgent execution patterns in multi-agent systems?"

        retrieved = complex_agent.retrieve_documents(complex_query)

        # Should retrieve documents covering multiple concepts
        assert len(retrieved) > 0

        # Check for coverage of key concepts
        key_concepts = ["stateschema", "shared", "sequential", "multi"]
        covered_concepts = set()

        for doc in retrieved:
            content_lower = doc.page_content.lower()
            for concept in key_concepts:
                if concept in content_lower:
                    covered_concepts.add(concept)

        # Should cover multiple concepts from the query
        assert len(covered_concepts) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
