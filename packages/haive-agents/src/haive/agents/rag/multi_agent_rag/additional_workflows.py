"""Additional RAG Workflows - Extended Multi-Agent RAG Implementations.

This module implements additional RAG architectures beyond the simple enhanced workflows,
including memory-based, multi-query, fusion, and advanced reasoning patterns.
"""

from typing import Dict, List

from haive.agents.multi.base import ExecutionMode, MultiAgent
from haive.agents.simple import SimpleAgent
from haive.core.schema.prebuilt.rag_state import RAGState


class MemoryRAGState(RAGState):
    """Extended RAG state with conversation memory."""

    conversation_history: list[dict[str, str]] = []
    previous_queries: list[str] = []
    memory_context: str = ""


class MultiQueryRAGState(RAGState):
    """RAG state for multi-query approaches."""

    generated_queries: list[str] = []
    query_results: dict[str, list[str]] = {}


class SelfRAGState(RAGState):
    """RAG state with self-reflection capabilities."""

    reflection_tokens: list[str] = []
    needs_retrieval: bool = True
    retrieval_confidence: float = 0.0
    answer_confidence: float = 0.0


class SimpleRAGWithMemoryAgent(MultiAgent):
    """Simple RAG with Memory - incorporates conversation history and previous queries
    to provide contextually aware responses.
    """

    def __init__(self, **kwargs):
        # Memory context agent
        memory_agent = SimpleAgent(
            name="memory_context_agent",
            instructions="""
            You analyze conversation history and previous queries to build relevant context.
            Extract key topics, themes, and context from the conversation history that would
            be relevant for the current query. Focus on:
            - Related previous questions and their context
            - Key topics and entities mentioned
            - User preferences or patterns
            - Contextual information that would enhance retrieval

            Provide a concise memory context summary.
            """,
            output_schema={"memory_context": "str", "relevant_history": "List[str]"},
        )

        # Standard retrieval agent
        retrieval_agent = SimpleAgent(
            name="retrieval_agent",
            instructions="""
            Retrieve relevant documents for the query, considering both the current query
            and the memory context provided. Use the memory context to enhance your
            retrieval strategy and find more relevant documents.
            """,
            output_schema={"documents": "List[str]", "retrieval_strategy": "str"},
        )

        # Answer generation with memory
        answer_agent = SimpleAgent(
            name="answer_agent",
            instructions="""
            Generate a comprehensive answer using the retrieved documents and memory context.
            Incorporate relevant information from conversation history where appropriate.
            Reference previous discussions when relevant but focus on the current query.
            """,
            output_schema={
                "answer": "str",
                "used_memory": "bool",
                "confidence": "float",
            },
        )

        agents = [memory_agent, retrieval_agent, answer_agent]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=MemoryRAGState,
            **kwargs
        )

    def build_custom_graph(self):
        """Build the custom graph for this multi-agent workflow."""
        # Simple sequential execution for memory RAG
        return  # Use default graph structure


class SelfRAGAgent(MultiAgent):
    """Self-RAG with reflection tokens - determines whether retrieval is needed
    and reflects on the quality of generated answers.
    """

    def __init__(self, **kwargs):
        # Retrieval necessity checker
        retrieval_checker = SimpleAgent(
            name="retrieval_checker",
            instructions="""
            Analyze the query to determine if retrieval is necessary. Consider:
            - Is this a factual question requiring external knowledge?
            - Can this be answered with general knowledge?
            - Does this require recent or specific information?

            Output reflection tokens: [Retrieval], [No Retrieval], [Continue], [Utility]
            """,
            output_schema={
                "needs_retrieval": "bool",
                "reflection_token": "str",
                "confidence": "float",
                "reasoning": "str",
            },
        )

        # Conditional retrieval agent
        retrieval_agent = SimpleAgent(
            name="conditional_retrieval_agent",
            instructions="""
            Only retrieve documents if needs_retrieval is True.
            Use the reflection reasoning to guide retrieval strategy.
            """,
            output_schema={"documents": "List[str]", "retrieval_quality": "str"},
        )

        # Self-reflective answer generator
        answer_agent = SimpleAgent(
            name="self_reflective_answer_agent",
            instructions="""
            Generate an answer and reflect on its quality. Consider:
            - Is the answer supported by evidence?
            - Are there any hallucinations or unsupported claims?
            - Is the answer complete and accurate?

            Output reflection tokens: [Relevant], [Partially Relevant], [Irrelevant],
            [No support], [Utility], [Isrel], [Issup]
            """,
            output_schema={
                "answer": "str",
                "reflection_tokens": "List[str]",
                "answer_confidence": "float",
                "needs_revision": "bool",
            },
        )

        agents = [retrieval_checker, retrieval_agent, answer_agent]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=SelfRAGState,
            **kwargs
        )

    def build_custom_graph(self):
        """Build the custom graph for this multi-agent workflow."""
        return  # Use default graph structure


class MultiQueryRAGAgent(MultiAgent):
    """Multi-Query RAG - generates multiple diverse queries and retrieves documents
    for each, then synthesizes results.
    """

    def __init__(self, **kwargs):
        # Query expansion agent
        query_expander = SimpleAgent(
            name="query_expander",
            instructions="""
            Generate 3-5 diverse queries related to the original question.
            Create queries that:
            - Approach the topic from different angles
            - Use different keywords and terminology
            - Include broader and narrower scopes
            - Consider different aspects of the question
            """,
            output_schema={
                "generated_queries": "List[str]",
                "expansion_strategy": "str",
            },
        )

        # Multi-retrieval agent
        multi_retrieval_agent = SimpleAgent(
            name="multi_retrieval_agent",
            instructions="""
            Retrieve documents for each generated query separately.
            Maintain query-document mappings and identify overlapping documents.
            """,
            output_schema={
                "query_results": "Dict[str, List[str]]",
                "unique_documents": "List[str]",
                "overlap_analysis": "str",
            },
        )

        # Synthesis agent
        synthesis_agent = SimpleAgent(
            name="synthesis_agent",
            instructions="""
            Synthesize information from all retrieved documents across different queries.
            Prioritize information that appears across multiple query results.
            Generate a comprehensive answer that leverages the diverse perspectives.
            """,
            output_schema={
                "answer": "str",
                "source_queries": "List[str]",
                "synthesis_confidence": "float",
            },
        )

        agents = [query_expander, multi_retrieval_agent, synthesis_agent]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=MultiQueryRAGState,
            **kwargs
        )

    def build_custom_graph(self):
        """Build the custom graph for this multi-agent workflow."""
        return  # Use default graph structure


class RAGFusionAgent(MultiAgent):
    """RAG Fusion - combines multiple retrieval strategies and fuses results
    using reciprocal rank fusion and other techniques.
    """

    def __init__(self, **kwargs):
        # Multiple strategy retrieval
        fusion_retrieval_agent = SimpleAgent(
            name="fusion_retrieval_agent",
            instructions="""
            Apply multiple retrieval strategies:
            1. Semantic similarity search
            2. Keyword-based search
            3. Question-based retrieval
            4. Context-aware retrieval

            Retrieve documents using each strategy and rank them.
            """,
            output_schema={
                "semantic_results": "List[str]",
                "keyword_results": "List[str]",
                "question_results": "List[str]",
                "context_results": "List[str]",
                "strategy_scores": "Dict[str, float]",
            },
        )

        # Fusion ranking agent
        fusion_ranker = SimpleAgent(
            name="fusion_ranker",
            instructions="""
            Apply Reciprocal Rank Fusion (RRF) to combine results from different strategies.
            RRF formula: score(d) = Î£(1/(k + rank_i(d))) for all strategies i

            Create a unified ranking of the most relevant documents.
            """,
            output_schema={
                "fused_documents": "List[str]",
                "fusion_scores": "Dict[str, float]",
                "ranking_explanation": "str",
            },
        )

        # Fusion answer agent
        fusion_answer_agent = SimpleAgent(
            name="fusion_answer_agent",
            instructions="""
            Generate an answer using the fusion-ranked documents.
            Give higher weight to documents with better fusion scores.
            Explain how different retrieval strategies contributed to the answer.
            """,
            output_schema={
                "answer": "str",
                "strategy_contributions": "Dict[str, str]",
                "fusion_confidence": "float",
            },
        )

        agents = [fusion_retrieval_agent, fusion_ranker, fusion_answer_agent]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=MultiQueryRAGState,  # Reuse for similar structure
            **kwargs
        )

    def build_custom_graph(self):
        """Build the custom graph for this multi-agent workflow."""
        return  # Use default graph structure


class StepBackPromptingRAGAgent(MultiAgent):
    """Step-Back Prompting RAG - asks broader conceptual questions before
    specific retrieval to get better context.
    """

    def __init__(self, **kwargs):
        # Step-back question generator
        step_back_agent = SimpleAgent(
            name="step_back_agent",
            instructions="""
            Generate a broader, more conceptual "step-back" question based on the original query.
            The step-back question should:
            - Be more general and conceptual
            - Help establish broader context
            - Lead to foundational knowledge retrieval

            Example: "What is the best treatment for pneumonia?" â’ 
            "What are the principles of treating bacterial infections?"
            """,
            output_schema={
                "step_back_question": "str",
                "conceptual_focus": "str",
                "reasoning": "str",
            },
        )

        # Dual retrieval agent
        dual_retrieval_agent = SimpleAgent(
            name="dual_retrieval_agent",
            instructions="""
            Retrieve documents for both:
            1. The original specific question
            2. The step-back conceptual question

            The step-back retrieval provides foundational context.
            """,
            output_schema={
                "original_documents": "List[str]",
                "stepback_documents": "List[str]",
                "context_coverage": "str",
            },
        )

        # Contextual answer agent
        contextual_answer_agent = SimpleAgent(
            name="contextual_answer_agent",
            instructions="""
            Generate an answer using both specific and conceptual documents.
            Use the step-back documents to provide foundational context,
            then address the specific question using targeted documents.
            """,
            output_schema={
                "answer": "str",
                "conceptual_foundation": "str",
                "specific_details": "str",
                "integration_quality": "float",
            },
        )

        agents = [step_back_agent, dual_retrieval_agent, contextual_answer_agent]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=RAGState,
            **kwargs
        )

    def build_custom_graph(self):
        """Build the custom graph for this multi-agent workflow."""
        return  # Use default graph structure


class QueryDecompositionRAGAgent(MultiAgent):
    """Query Decomposition RAG - breaks complex queries into simpler sub-questions,
    retrieves for each, then composes the final answer.
    """

    def __init__(self, **kwargs):
        # Query decomposer
        decomposition_agent = SimpleAgent(
            name="decomposition_agent",
            instructions="""
            Break down complex queries into 2-4 simpler, focused sub-questions.
            Each sub-question should:
            - Address a specific aspect of the main question
            - Be answerable independently
            - Contribute to the overall answer
            - Be clear and specific
            """,
            output_schema={
                "sub_questions": "List[str]",
                "decomposition_strategy": "str",
                "question_dependencies": "List[str]",
            },
        )

        # Sub-question retrieval agent
        subq_retrieval_agent = SimpleAgent(
            name="subquestion_retrieval_agent",
            instructions="""
            Retrieve relevant documents for each sub-question separately.
            Maintain sub-question to document mappings for composition.
            """,
            output_schema={
                "subquestion_results": "Dict[str, List[str]]",
                "retrieval_coverage": "Dict[str, float]",
                "cross_references": "List[str]",
            },
        )

        # Answer composition agent
        composition_agent = SimpleAgent(
            name="composition_agent",
            instructions="""
            Compose a comprehensive answer by integrating responses to all sub-questions.
            Ensure logical flow and coherence in the final answer.
            Address any dependencies between sub-questions.
            """,
            output_schema={
                "sub_answers": "Dict[str, str]",
                "composed_answer": "str",
                "integration_notes": "str",
                "completeness_score": "float",
            },
        )

        agents = [decomposition_agent, subq_retrieval_agent, composition_agent]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=MultiQueryRAGState,  # Reuse for similar structure
            **kwargs
        )

    def build_custom_graph(self):
        """Build the custom graph for this multi-agent workflow."""
        return  # Use default graph structure
