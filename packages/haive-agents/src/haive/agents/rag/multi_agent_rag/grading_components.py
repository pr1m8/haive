"""
Grading Components for RAG Workflows

This module provides reusable grading agents for document relevance,
answer quality, and hallucination detection.
"""

from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent

# ===== MODELS =====


class DocumentGrade(BaseModel):
    """Grade for a retrieved document"""

    document_id: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    is_relevant: bool
    reasoning: str
    key_information: List[str] = []


class AnswerGrade(BaseModel):
    """Grade for generated answer quality"""

    completeness_score: float = Field(ge=0.0, le=1.0)
    accuracy_score: float = Field(ge=0.0, le=1.0)
    clarity_score: float = Field(ge=0.0, le=1.0)
    overall_score: float = Field(ge=0.0, le=1.0)
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []


class HallucinationGrade(BaseModel):
    """Grade for hallucination detection"""

    has_hallucination: bool
    hallucination_score: float = Field(ge=0.0, le=1.0)
    hallucination_types: List[str] = []
    specific_issues: List[str] = []
    supported_claims: List[str] = []
    unsupported_claims: List[str] = []


# ===== PROMPT TEMPLATES =====

DOCUMENT_RELEVANCE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert document relevance evaluator. Assess each document's relevance to the query.

**Scoring Guidelines:**
- 0.9-1.0: Directly answers the query with specific, comprehensive information
- 0.7-0.8: Contains substantial relevant information that helps answer the query
- 0.5-0.6: Has some relevant information but may be partially off-topic
- 0.3-0.4: Marginally relevant, contains tangential information
- 0.0-0.2: Not relevant or completely off-topic

**Consider:**
- Direct relevance to query intent
- Quality and specificity of information
- Completeness of coverage
- Usefulness for answering the query""",
        ),
        (
            "human",
            """Query: {query}

Document to evaluate:
{document}

Provide a detailed relevance assessment with:
1. Relevance score (0.0-1.0)
2. Is relevant (true/false - use 0.5 as threshold)
3. Reasoning for your assessment
4. Key information extracted (if relevant)""",
        ),
    ]
)

ANSWER_QUALITY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert answer quality evaluator. Assess the generated answer across multiple dimensions.

**Evaluation Criteria:**

1. **Completeness (0.0-1.0)**:
   - Does it fully address all aspects of the query?
   - Are there important missing elements?
   - Is the depth of coverage appropriate?

2. **Accuracy (0.0-1.0)**:
   - Is the information factually correct?
   - Are claims properly supported by sources?
   - Are there any errors or misrepresentations?

3. **Clarity (0.0-1.0)**:
   - Is the answer well-organized and easy to understand?
   - Is technical language used appropriately?
   - Is the flow logical and coherent?

4. **Overall Quality (0.0-1.0)**:
   - Holistic assessment of the answer
   - Balance of all factors
   - Usefulness to the user""",
        ),
        (
            "human",
            """Query: {query}

Generated Answer:
{answer}

Source Documents Used:
{source_documents}

Provide a comprehensive quality assessment including:
1. Individual scores for completeness, accuracy, clarity
2. Overall quality score
3. Specific strengths
4. Identified weaknesses
5. Concrete suggestions for improvement""",
        ),
    ]
)

HALLUCINATION_DETECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert hallucination detector. Rigorously verify that all claims in the answer are grounded in source documents.

**Types of Hallucinations to Detect:**
1. **Factual**: Claims contradicting or not present in sources
2. **Inferential**: Conclusions beyond reasonable inference
3. **Attributional**: Misattributing information to wrong sources
4. **Temporal**: Adding time information not in sources
5. **Quantitative**: Introducing unsupported numbers/statistics
6. **Causal**: Unsupported cause-effect relationships

**Scoring:**
- 0.0: No hallucination detected
- 0.1-0.3: Minor inferential leaps
- 0.4-0.6: Some unsupported claims
- 0.7-0.9: Major hallucinations
- 1.0: Severe fabrication

Be thorough and evidence-based.""",
        ),
        (
            "human",
            """Query: {query}

Source Documents:
{source_documents}

Generated Answer:
{answer}

Analyze for hallucinations:
1. Has hallucination (true/false)
2. Hallucination score (0.0-1.0)
3. Types of hallucinations found
4. Specific problematic claims
5. List of supported vs unsupported claims""",
        ),
    ]
)


# ===== GRADING AGENTS =====


def create_document_grader(name: str = "document_grader") -> SimpleAgent:
    """Create a document relevance grading agent"""
    return SimpleAgent(
        name=name,
        instructions="""Evaluate document relevance to queries using systematic criteria.
        Provide detailed assessments with scores, reasoning, and extracted key information.""",
        prompt_template=DOCUMENT_RELEVANCE_PROMPT,
        output_schema={
            "document_id": "str",
            "relevance_score": "float",
            "is_relevant": "bool",
            "reasoning": "str",
            "key_information": "List[str]",
        },
    )


def create_answer_grader(name: str = "answer_grader") -> SimpleAgent:
    """Create an answer quality grading agent"""
    return SimpleAgent(
        name=name,
        instructions="""Evaluate generated answers across multiple quality dimensions.
        Assess completeness, accuracy, clarity, and overall quality with specific feedback.""",
        prompt_template=ANSWER_QUALITY_PROMPT,
        output_schema={
            "completeness_score": "float",
            "accuracy_score": "float",
            "clarity_score": "float",
            "overall_score": "float",
            "strengths": "List[str]",
            "weaknesses": "List[str]",
            "suggestions": "List[str]",
        },
    )


def create_hallucination_grader(name: str = "hallucination_grader") -> SimpleAgent:
    """Create a hallucination detection agent"""
    return SimpleAgent(
        name=name,
        instructions="""Detect hallucinations by comparing generated answers against source documents.
        Identify unsupported claims, fabrications, and misrepresentations.""",
        prompt_template=HALLUCINATION_DETECTION_PROMPT,
        output_schema={
            "has_hallucination": "bool",
            "hallucination_score": "float",
            "hallucination_types": "List[str]",
            "specific_issues": "List[str]",
            "supported_claims": "List[str]",
            "unsupported_claims": "List[str]",
        },
    )


# ===== PRIORITY GRADING =====

PRIORITY_RANKING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at prioritizing retrieved documents based on their relevance and usefulness.

**Prioritization Criteria:**
1. **Direct Relevance**: How directly does it answer the query?
2. **Information Quality**: Depth, specificity, and accuracy
3. **Completeness**: Coverage of query aspects
4. **Recency**: More recent information when relevant
5. **Authority**: Source credibility and expertise
6. **Uniqueness**: Novel information not in other documents

Rank documents from most to least important for answering the query.""",
        ),
        (
            "human",
            """Query: {query}

Documents to prioritize:
{documents}

Provide:
1. Ranked list of document IDs (most to least important)
2. Priority score for each (0.0-1.0)
3. Reasoning for top 3 documents
4. Documents to potentially exclude (if any)""",
        ),
    ]
)


def create_priority_ranker(name: str = "priority_ranker") -> SimpleAgent:
    """Create a document priority ranking agent"""
    return SimpleAgent(
        name=name,
        instructions="""Prioritize retrieved documents based on relevance, quality, and usefulness.
        Create ranked lists to optimize document usage in answer generation.""",
        prompt_template=PRIORITY_RANKING_PROMPT,
        output_schema={
            "ranked_document_ids": "List[str]",
            "priority_scores": "Dict[str, float]",
            "top_3_reasoning": "Dict[str, str]",
            "exclude_document_ids": "List[str]",
            "exclusion_reasons": "Dict[str, str]",
        },
    )


# ===== QUERY UNDERSTANDING =====

QUERY_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert query analyzer. Break down queries to understand intent and requirements.

**Analysis Dimensions:**
1. **Query Type**: Factual, analytical, comparative, procedural, etc.
2. **Key Entities**: Important nouns, concepts, and entities
3. **Intent**: What the user really wants to know
4. **Complexity**: Simple, moderate, or complex
5. **Required Information**: What types of information are needed
6. **Potential Ambiguities**: Unclear or multiple interpretations""",
        ),
        (
            "human",
            """Analyze this query in detail:

Query: {query}

Provide comprehensive analysis including:
1. Query type classification
2. Key entities and concepts
3. User intent interpretation
4. Complexity assessment
5. Information requirements
6. Potential ambiguities or clarifications needed""",
        ),
    ]
)


def create_query_analyzer(name: str = "query_analyzer") -> SimpleAgent:
    """Create a query analysis agent"""
    return SimpleAgent(
        name=name,
        instructions="""Analyze queries to understand intent, complexity, and information needs.
        Provide detailed breakdowns to guide retrieval and answer generation.""",
        prompt_template=QUERY_ANALYSIS_PROMPT,
        output_schema={
            "query_type": "str",
            "key_entities": "List[str]",
            "user_intent": "str",
            "complexity": "str",  # simple, moderate, complex
            "information_requirements": "List[str]",
            "ambiguities": "List[str]",
            "suggested_clarifications": "List[str]",
        },
    )


# ===== COMPOSITE GRADING WORKFLOW =====


class CompositeGradingAgent:
    """Combines multiple grading components for comprehensive evaluation"""

    def __init__(self):
        self.document_grader = create_document_grader()
        self.answer_grader = create_answer_grader()
        self.hallucination_grader = create_hallucination_grader()
        self.priority_ranker = create_priority_ranker()
        self.query_analyzer = create_query_analyzer()

    async def grade_rag_pipeline(
        self, query: str, documents: List[Dict[str, Any]], answer: str
    ) -> Dict[str, Any]:
        """Perform comprehensive grading of entire RAG pipeline"""

        # Analyze query
        query_analysis = await self.query_analyzer.ainvoke({"query": query})

        # Grade each document
        document_grades = []
        for doc in documents:
            grade = await self.document_grader.ainvoke(
                {"query": query, "document": doc.get("content", doc)}
            )
            document_grades.append(grade)

        # Prioritize documents
        priority_ranking = await self.priority_ranker.ainvoke(
            {"query": query, "documents": documents}
        )

        # Grade answer quality
        answer_grade = await self.answer_grader.ainvoke(
            {"query": query, "answer": answer, "source_documents": documents}
        )

        # Check for hallucinations
        hallucination_grade = await self.hallucination_grader.ainvoke(
            {"query": query, "answer": answer, "source_documents": documents}
        )

        return {
            "query_analysis": query_analysis,
            "document_grades": document_grades,
            "priority_ranking": priority_ranking,
            "answer_grade": answer_grade,
            "hallucination_grade": hallucination_grade,
            "overall_pipeline_score": self._calculate_overall_score(
                document_grades, answer_grade, hallucination_grade
            ),
        }

    def _calculate_overall_score(
        self, document_grades: List[Dict], answer_grade: Dict, hallucination_grade: Dict
    ) -> float:
        """Calculate overall pipeline score"""
        # Average document relevance
        doc_score = (
            sum(g.get("relevance_score", 0) for g in document_grades)
            / len(document_grades)
            if document_grades
            else 0
        )

        # Answer quality
        answer_score = answer_grade.get("overall_score", 0)

        # Hallucination penalty
        hallucination_penalty = hallucination_grade.get("hallucination_score", 0)

        # Weighted combination
        overall = (0.3 * doc_score + 0.5 * answer_score) * (
            1 - 0.5 * hallucination_penalty
        )

        return min(max(overall, 0.0), 1.0)
