"""Enhanced HyDE prompts based on LangChain best practices.

This module provides improved HyDE prompt templates that follow the principle
of separating document generation from structured output parsing.

Key improvements:
- Simplified generation prompts focused on content creation
- Domain-specific prompt templates
- Separate analysis/parsing prompts for structured output
- Multi-perspective generation support
- Controlled document length
"""

from enum import Enum
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class HyDEPromptType(str, Enum):
    """Types of HyDE prompts for different domains."""

    GENERAL = "general"
    TECHNICAL = "technical"
    ACADEMIC = "academic"
    NEWS = "news"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    BUSINESS = "business"


class HyDEPerspective(str, Enum):
    """Different perspectives for multi-angle document generation."""

    EXPERT = "expert"
    BEGINNER = "beginner"
    PRACTITIONER = "practitioner"
    RESEARCHER = "researcher"
    CRITIC = "critic"


# ==============================================================================
# SIMPLIFIED GENERATION PROMPTS (Focus on content creation only)
# ==============================================================================

HYDE_GENERATION_PROMPTS: Dict[HyDEPromptType, ChatPromptTemplate] = {
    HyDEPromptType.GENERAL: ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert writer creating comprehensive documents that directly answer questions.
            
            Write a detailed, informative document that fully addresses the user's question.
            
            Guidelines:
            - Write as if creating an authoritative reference document
            - Include specific details, examples, and factual information
            - Use clear, professional language
            - Write approximately {target_length} characters
            - Focus on density of relevant information
            - Do not mention this is hypothetical - write as if it's real content""",
            ),
            ("human", "Write a comprehensive document that answers: {query}"),
        ]
    ),
    HyDEPromptType.TECHNICAL: ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a technical writer creating detailed technical documentation.
            
            Write comprehensive technical documentation that answers the user's question.
            
            Guidelines:
            - Include implementation details and code examples where relevant
            - Use precise technical terminology
            - Provide step-by-step explanations
            - Include best practices and common pitfalls
            - Write approximately {target_length} characters
            - Structure as technical reference material""",
            ),
            ("human", "Write technical documentation that covers: {query}"),
        ]
    ),
    HyDEPromptType.ACADEMIC: ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are writing an academic research paper section.
            
            Create a detailed, well-researched academic passage that addresses the research question.
            
            Guidelines:
            - Use formal academic writing style
            - Include theoretical background and methodology
            - Reference key concepts and principles
            - Provide detailed analysis and conclusions
            - Write approximately {target_length} characters
            - Structure as academic literature""",
            ),
            ("human", "Write an academic passage addressing: {query}"),
        ]
    ),
    HyDEPromptType.NEWS: ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a news reporter writing a comprehensive news article.
            
            Write a detailed news article that covers the topic thoroughly.
            
            Guidelines:
            - Use journalistic writing style (who, what, when, where, why)
            - Include quotes and specific details
            - Provide context and background information
            - Use clear, accessible language
            - Write approximately {target_length} characters
            - Structure as news reporting""",
            ),
            ("human", "Write a news article covering: {query}"),
        ]
    ),
    HyDEPromptType.TUTORIAL: ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert instructor writing a comprehensive tutorial.
            
            Create a detailed tutorial that teaches the user about the topic.
            
            Guidelines:
            - Use instructional writing style
            - Include step-by-step explanations
            - Provide examples and exercises
            - Anticipate common questions and mistakes
            - Write approximately {target_length} characters
            - Structure as educational content""",
            ),
            ("human", "Write a tutorial explaining: {query}"),
        ]
    ),
    HyDEPromptType.REFERENCE: ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are writing an encyclopedia or reference entry.
            
            Create a comprehensive reference document that definitively covers the topic.
            
            Guidelines:
            - Use formal, encyclopedic writing style
            - Include definitions, classifications, and detailed descriptions
            - Provide historical context and significance
            - Use objective, authoritative tone
            - Write approximately {target_length} characters
            - Structure as reference material""",
            ),
            ("human", "Write a reference entry for: {query}"),
        ]
    ),
    HyDEPromptType.BUSINESS: ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are writing business documentation or analysis.
            
            Create professional business content that addresses the topic comprehensively.
            
            Guidelines:
            - Use business writing style and terminology
            - Include market analysis, strategies, and outcomes
            - Provide data-driven insights and recommendations
            - Use professional, results-oriented language
            - Write approximately {target_length} characters
            - Structure as business documentation""",
            ),
            ("human", "Write business content addressing: {query}"),
        ]
    ),
}


# ==============================================================================
# MULTI-PERSPECTIVE GENERATION
# ==============================================================================

HYDE_PERSPECTIVE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are writing a document from the perspective of a {perspective}.
        
        Perspective characteristics:
        - Expert: Deep technical knowledge, comprehensive understanding
        - Beginner: Learning-focused, asks clarifying questions, seeks fundamentals
        - Practitioner: Hands-on experience, practical applications, real-world examples
        - Researcher: Evidence-based, methodology-focused, theoretical depth
        - Critic: Analytical, evaluates pros/cons, identifies limitations
        
        Write a document that a {perspective} would create to address the topic.
        Use language, examples, and focus appropriate for this perspective.
        Write approximately {target_length} characters.""",
        ),
        ("human", "From the perspective of a {perspective}, write about: {query}"),
    ]
)


# ==============================================================================
# ANALYSIS AND PARSING PROMPTS (Separate from generation)
# ==============================================================================

HYDE_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are analyzing a hypothetical document to extract structured information.
        
        Analyze the document and extract:
        - Document type and style
        - Key concepts and topics covered
        - Target audience and expertise level
        - Retrieval strategy recommendations
        - Quality assessment
        
        Provide structured analysis that will help with document retrieval and ranking.""",
        ),
        (
            "human",
            """Analyze this hypothetical document:

Document:
{document}

Original Query: {query}

Provide structured analysis including document type, key concepts, target audience, and retrieval strategy.""",
        ),
    ]
)


HYDE_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Extract key information from the hypothetical document for retrieval purposes.
        
        Focus on:
        - Main topics and subtopics
        - Important keywords and terminology
        - Factual claims and data points
        - Relationships between concepts
        - Document structure and organization""",
        ),
        (
            "human",
            """Extract key information from this document:

{document}

Provide a structured extraction suitable for semantic search and retrieval.""",
        ),
    ]
)


# ==============================================================================
# CONTROLLED LENGTH GENERATION
# ==============================================================================

HYDE_LENGTH_CONTROLLED_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Generate a hypothetical document that answers the question.
        
        The document should be exactly {target_length} characters.
        Focus on information density - pack as much relevant information as possible
        into the specified length while maintaining readability and coherence.
        
        Length targets:
        - Short (500 chars): Key facts and direct answer
        - Medium (1000 chars): Detailed explanation with examples  
        - Long (2000 chars): Comprehensive coverage with context""",
        ),
        ("human", "Question: {query}"),
    ]
)


# ==============================================================================
# ENSEMBLE GENERATION (Multiple documents)
# ==============================================================================

HYDE_ENSEMBLE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Generate multiple hypothetical documents that would answer the question from different angles.
        
        Create {num_documents} documents with different:
        - Document types (academic, news, technical, etc.)
        - Perspectives (expert, beginner, practitioner)
        - Focuses (theoretical, practical, historical)
        
        Each document should be approximately {target_length} characters.
        Vary the approach while maintaining quality and relevance.""",
        ),
        ("human", "Generate {num_documents} different documents answering: {query}"),
    ]
)


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================


def get_generation_prompt(
    prompt_type: HyDEPromptType = HyDEPromptType.GENERAL, target_length: int = 1000
) -> ChatPromptTemplate:
    """Get a generation prompt for the specified type and length.

    Args:
        prompt_type: Type of prompt to use
        target_length: Target character length for generated document

    Returns:
        Configured ChatPromptTemplate
    """
    base_prompt = HYDE_GENERATION_PROMPTS[prompt_type]
    return base_prompt.partial(target_length=target_length)


def get_perspective_prompt(
    perspective: HyDEPerspective, target_length: int = 1000
) -> ChatPromptTemplate:
    """Get a perspective-based generation prompt.

    Args:
        perspective: Perspective to use for generation
        target_length: Target character length for generated document

    Returns:
        Configured ChatPromptTemplate
    """
    return HYDE_PERSPECTIVE_PROMPT.partial(
        perspective=perspective.value, target_length=target_length
    )


def get_ensemble_prompt(
    num_documents: int = 3, target_length: int = 1000
) -> ChatPromptTemplate:
    """Get an ensemble generation prompt for multiple documents.

    Args:
        num_documents: Number of documents to generate
        target_length: Target character length per document

    Returns:
        Configured ChatPromptTemplate
    """
    return HYDE_ENSEMBLE_PROMPT.partial(
        num_documents=num_documents, target_length=target_length
    )


# ==============================================================================
# PROMPT SELECTION LOGIC
# ==============================================================================


class HyDEPromptConfig(BaseModel):
    """Configuration for HyDE prompt selection."""

    prompt_type: HyDEPromptType = Field(
        default=HyDEPromptType.GENERAL, description="Type of prompt to use"
    )
    perspective: HyDEPerspective | None = Field(
        default=None, description="Optional perspective for generation"
    )
    target_length: int = Field(
        default=1000, description="Target character length for generated documents"
    )
    use_ensemble: bool = Field(
        default=False, description="Whether to generate multiple documents"
    )
    num_documents: int = Field(
        default=3, description="Number of documents for ensemble generation"
    )


def select_prompt_automatically(query: str) -> HyDEPromptType:
    """Automatically select appropriate prompt type based on query analysis.

    Args:
        query: User query to analyze

    Returns:
        Recommended prompt type
    """
    query_lower = query.lower()

    # Technical keywords
    if any(
        word in query_lower
        for word in [
            "code",
            "programming",
            "algorithm",
            "implementation",
            "api",
            "software",
            "system",
            "architecture",
            "framework",
            "library",
        ]
    ):
        return HyDEPromptType.TECHNICAL

    # Academic keywords
    elif any(
        word in query_lower
        for word in [
            "research",
            "study",
            "analysis",
            "theory",
            "hypothesis",
            "methodology",
            "literature",
            "empirical",
            "statistical",
        ]
    ):
        return HyDEPromptType.ACADEMIC

    # News/current events keywords
    elif any(
        word in query_lower
        for word in [
            "news",
            "current",
            "recent",
            "latest",
            "update",
            "report",
            "announcement",
            "event",
            "happening",
            "today",
        ]
    ):
        return HyDEPromptType.NEWS

    # Tutorial/how-to keywords
    elif any(
        word in query_lower
        for word in [
            "how to",
            "tutorial",
            "guide",
            "learn",
            "teach",
            "explain",
            "step by step",
            "instructions",
            "walkthrough",
        ]
    ):
        return HyDEPromptType.TUTORIAL

    # Business keywords
    elif any(
        word in query_lower
        for word in [
            "business",
            "market",
            "strategy",
            "company",
            "revenue",
            "profit",
            "management",
            "enterprise",
            "corporate",
        ]
    ):
        return HyDEPromptType.BUSINESS

    # Default to general
    else:
        return HyDEPromptType.GENERAL


def create_hyde_prompt(config: HyDEPromptConfig, query: str) -> ChatPromptTemplate:
    """Create a HyDE prompt based on configuration.

    Args:
        config: Prompt configuration
        query: User query

    Returns:
        Configured ChatPromptTemplate ready for use
    """
    if config.use_ensemble:
        return get_ensemble_prompt(config.num_documents, config.target_length)
    elif config.perspective:
        return get_perspective_prompt(config.perspective, config.target_length)
    else:
        return get_generation_prompt(config.prompt_type, config.target_length)
