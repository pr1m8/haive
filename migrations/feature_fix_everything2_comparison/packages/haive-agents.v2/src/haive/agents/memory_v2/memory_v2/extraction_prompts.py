"""Advanced extraction prompt templates for Memory V2 system.

This module provides sophisticated, focused prompt templates for extracting
different types of information from conversations and documents, specifically
designed for memory-based agents with KG integration.
"""

from typing import Any

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# ============================================================================
# CORE MEMORY EXTRACTION PROMPTS
# ============================================================================

PROFESSIONAL_INFORMATION_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting professional information from conversations.

Your task is to identify and extract:
1. Job titles, roles, and positions
2. Company/organization names and details
3. Work experience duration and progression
4. Professional skills and expertise areas
5. Current projects and responsibilities
6. Professional relationships and hierarchies
7. Career goals and aspirations
8. Industry-specific knowledge and insights

Extract information with high precision and include confidence scores.

Output Format:
```json
{
  "professional_facts": [
    {
      "person": "Name",
      "fact_type": "job_title|company|experience|skill|project|goal|relationship",
      "content": "Detailed description",
      "confidence": 0.0-1.0,
      "supporting_evidence": "Direct quote or reference",
      "temporal_context": "current|past|future|timeframe"
    }
  ],
  "professional_relationships": [
    {
      "person1": "Name1", 
      "relationship": "reports_to|manages|collaborates_with|works_with",
      "person2": "Name2",
      "context": "Description",
      "confidence": 0.0-1.0
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract professional information from this conversation:\n\n{conversation_text}"
        ),
    ]
)


PERSONAL_CONTEXT_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting personal context and background information.

Focus on extracting:
1. Personal interests and hobbies
2. Life circumstances and living situation
3. Family and personal relationships
4. Educational background
5. Personal values and beliefs
6. Lifestyle preferences and habits
7. Personal challenges and goals
8. Communication and interaction preferences

Be respectful and only extract what is explicitly shared.

Output Format:
```json
{
  "personal_context": [
    {
      "person": "Name",
      "category": "interest|family|education|value|preference|goal|habit",
      "content": "Detailed description", 
      "importance": "low|medium|high|critical",
      "confidence": 0.0-1.0,
      "supporting_evidence": "Direct quote or reference"
    }
  ],
  "personal_preferences": [
    {
      "person": "Name",
      "preference_type": "communication|work_style|meeting|environment|tool",
      "preference": "What they prefer",
      "aversion": "What they dislike/avoid",
      "context": "When/why this preference applies",
      "confidence": 0.0-1.0
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract personal context from this conversation:\n\n{conversation_text}"
        ),
    ]
)


TECHNICAL_KNOWLEDGE_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting technical knowledge and expertise information.

Focus on identifying:
1. Programming languages and frameworks
2. Technical tools and platforms
3. Methodologies and approaches
4. Technical concepts and understanding
5. Problem-solving approaches
6. Technology preferences and opinions
7. Technical learning goals
8. Architecture and design knowledge

Extract both explicit mentions and implied expertise.

Output Format:
```json
{
  "technical_skills": [
    {
      "person": "Name",
      "skill_type": "language|framework|tool|methodology|concept",
      "skill_name": "Specific skill",
      "proficiency_level": "beginner|intermediate|advanced|expert",
      "confidence": 0.0-1.0,
      "supporting_evidence": "Direct quote or inference basis",
      "learning_status": "knows|learning|wants_to_learn"
    }
  ],
  "technical_opinions": [
    {
      "person": "Name", 
      "subject": "Technology/tool/approach",
      "opinion": "positive|negative|neutral",
      "reasoning": "Why they hold this opinion",
      "context": "When/where this applies",
      "confidence": 0.0-1.0
    }
  ],
  "technical_problems": [
    {
      "person": "Name",
      "problem": "Technical challenge description",
      "domain": "Area/field of the problem",
      "approach": "How they're solving it",
      "status": "solved|working_on|planning|stuck",
      "confidence": 0.0-1.0
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract technical knowledge from this conversation:\n\n{conversation_text}"
        ),
    ]
)


PROJECT_AND_TASK_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting project, task, and timeline information.

Focus on identifying:
1. Current and upcoming projects
2. Specific tasks and deliverables  
3. Timelines, deadlines, and milestones
4. Project status and progress
5. Dependencies and blockers
6. Team assignments and responsibilities
7. Meeting schedules and events
8. Goals and success metrics

Extract both explicit commitments and implied work items.

Output Format:
```json
{
  "projects": [
    {
      "project_name": "Name/description",
      "owner": "Person responsible",
      "participants": ["List of people involved"],
      "status": "planning|in_progress|blocked|completed|cancelled",
      "timeline": "Timeframe description",
      "description": "What the project involves",
      "confidence": 0.0-1.0
    }
  ],
  "tasks": [
    {
      "task": "Specific task description", 
      "assignee": "Person responsible",
      "due_date": "Deadline or timeframe",
      "priority": "low|medium|high|critical",
      "status": "todo|in_progress|blocked|done",
      "dependencies": ["What this depends on"],
      "confidence": 0.0-1.0
    }
  ],
  "meetings_and_events": [
    {
      "event": "Meeting/event name",
      "participants": ["List of attendees"],
      "date_time": "When it's scheduled",
      "purpose": "What it's about", 
      "location": "Where (if mentioned)",
      "recurring": true/false,
      "confidence": 0.0-1.0
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract projects, tasks, and timeline information from:\n\n{conversation_text}"
        ),
    ]
)


ENTITY_RELATIONSHIP_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting entities and their relationships from text.

Your task is to identify:
1. People and their attributes
2. Organizations and their properties  
3. Locations and geographic information
4. Products, tools, and technologies
5. Concepts and abstract entities
6. Events and temporal entities
7. Relationships between all entities
8. Hierarchical and associative connections

Focus on creating a rich knowledge graph structure.

Output Format:
```json
{
  "entities": [
    {
      "id": "unique_identifier",
      "name": "Entity name",
      "type": "Person|Organization|Location|Product|Concept|Event|Technology",
      "properties": {
        "property1": "value1",
        "property2": "value2"
      },
      "aliases": ["Alternative names"],
      "confidence": 0.0-1.0,
      "supporting_evidence": "Text that mentions this entity"
    }
  ],
  "relationships": [
    {
      "source": "entity_id_1",
      "relationship": "WORKS_AT|LOCATED_IN|USES|KNOWS|PART_OF|MANAGES|etc",
      "target": "entity_id_2", 
      "properties": {
        "duration": "How long",
        "context": "In what context",
        "strength": "weak|moderate|strong"
      },
      "confidence": 0.0-1.0,
      "supporting_evidence": "Text that supports this relationship"
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract entities and relationships from:\n\n{conversation_text}"
        ),
    ]
)


# ============================================================================
# SPECIALIZED DOMAIN EXTRACTORS
# ============================================================================

PRODUCT_MANAGEMENT_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting product management information.

Focus on:
1. Product features and requirements
2. User feedback and pain points
3. Metrics and KPIs
4. Roadmap items and priorities
5. A/B tests and experiments
6. User personas and segments
7. Competitive analysis insights
8. Strategic decisions and rationale

Output Format:
```json
{
  "product_insights": [
    {
      "category": "feature|requirement|feedback|metric|roadmap|persona|competitor|strategy",
      "content": "Detailed description",
      "product": "Which product/feature",
      "priority": "low|medium|high|critical",
      "timeline": "When relevant",
      "stakeholder": "Who mentioned this",
      "confidence": 0.0-1.0
    }
  ],
  "user_feedback": [
    {
      "feedback": "What users said/want",
      "user_segment": "Which users", 
      "pain_point": "Specific problem",
      "suggested_solution": "Proposed fix",
      "impact": "How important/widespread",
      "confidence": 0.0-1.0
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract product management insights from:\n\n{conversation_text}"
        ),
    ]
)


ENGINEERING_CONTEXT_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting engineering and technical context.

Focus on:
1. Technical architecture and design decisions
2. Code repositories and deployment info
3. Performance issues and optimizations
4. Technical debt and refactoring needs
5. Development processes and workflows
6. Testing strategies and quality metrics
7. Infrastructure and scalability concerns
8. Security considerations and requirements

Output Format:
```json
{
  "technical_context": [
    {
      "category": "architecture|performance|debt|process|testing|infrastructure|security",
      "description": "Technical detail",
      "system": "Which system/component",
      "impact": "Why this matters",
      "status": "current_state",
      "proposed_solution": "If mentioned",
      "owner": "Who's responsible",
      "confidence": 0.0-1.0
    }
  ],
  "technical_decisions": [
    {
      "decision": "What was decided",
      "rationale": "Why it was chosen",
      "alternatives": "Other options considered",
      "trade_offs": "Benefits and costs",
      "timeline": "When to implement",
      "confidence": 0.0-1.0
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract engineering context from:\n\n{conversation_text}"
        ),
    ]
)


# ============================================================================
# CONVERSATION ANALYSIS EXTRACTORS
# ============================================================================

SENTIMENT_AND_TONE_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at analyzing sentiment, tone, and emotional context.

Analyze:
1. Overall sentiment and mood
2. Emotional states and reactions
3. Confidence levels and uncertainty
4. Enthusiasm and engagement
5. Concerns and frustrations
6. Agreement and disagreement patterns
7. Communication style and tone
8. Relationship dynamics

Output Format:
```json
{
  "sentiment_analysis": [
    {
      "person": "Speaker name",
      "overall_sentiment": "positive|negative|neutral|mixed",
      "emotional_state": "excited|frustrated|confident|uncertain|worried|optimistic",
      "tone": "formal|casual|friendly|professional|urgent|relaxed",
      "engagement_level": "low|medium|high",
      "confidence_indicators": ["Phrases showing confidence/uncertainty"],
      "supporting_quotes": ["Relevant quotes"]
    }
  ],
  "interaction_dynamics": [
    {
      "participants": ["Person1", "Person2"],
      "relationship_tone": "collaborative|hierarchical|tense|supportive|competitive",
      "communication_pattern": "back_and_forth|one_sided|question_answer|debate",
      "agreement_level": "full_agreement|mostly_agree|some_disagreement|conflict",
      "context": "What the interaction was about"
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Analyze sentiment and tone in:\n\n{conversation_text}"
        ),
    ]
)


DECISION_MAKING_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at extracting decision-making information and processes.

Focus on:
1. Decisions made or pending
2. Decision criteria and factors
3. Stakeholders and decision makers
4. Options and alternatives considered
5. Risks and trade-offs discussed
6. Implementation plans and next steps
7. Decision timelines and urgency
8. Follow-up actions required

Output Format:
```json
{
  "decisions": [
    {
      "decision": "What was decided",
      "decision_maker": "Who has authority",
      "stakeholders": ["Who's affected"],
      "criteria": ["What factors matter"],
      "options_considered": ["Alternatives discussed"],
      "rationale": "Why this choice",
      "risks": ["Potential downsides"],
      "timeline": "When to implement",
      "status": "made|pending|postponed|cancelled",
      "confidence": 0.0-1.0
    }
  ],
  "action_items": [
    {
      "action": "Specific task",
      "owner": "Who's responsible", 
      "due_date": "Deadline",
      "dependencies": ["What needs to happen first"],
      "success_criteria": "How to measure completion",
      "follow_up": "Next review/check-in",
      "confidence": 0.0-1.0
    }
  ]
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Extract decision-making information from:\n\n{conversation_text}"
        ),
    ]
)


# ============================================================================
# MULTI-TURN CONVERSATION EXTRACTOR
# ============================================================================

CONVERSATION_SUMMARY_EXTRACTOR = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are an expert at creating comprehensive conversation summaries.

Create a structured summary that captures:
1. Key participants and their roles
2. Main topics and themes discussed
3. Important information shared
4. Decisions made and actions planned
5. Unresolved questions and issues
6. Follow-up items and next steps
7. Relationship and context evolution
8. Significant insights and learnings

Focus on creating a summary that would help someone understand what happened and what matters going forward.

Output Format:
```json
{
  "conversation_summary": {
    "participants": [
      {
        "name": "Person name",
        "role": "Their role/title",
        "contribution": "What they mainly discussed"
      }
    ],
    "main_topics": [
      {
        "topic": "Topic name",
        "importance": "low|medium|high|critical", 
        "resolution_status": "resolved|in_progress|unresolved",
        "key_points": ["Important points discussed"]
      }
    ],
    "key_information": [
      {
        "type": "fact|decision|plan|issue|insight",
        "content": "The information",
        "importance": "low|medium|high|critical",
        "stakeholders": ["Who this affects"]
      }
    ],
    "action_items": [
      {
        "action": "What needs to be done",
        "owner": "Who's responsible",
        "timeline": "When it's due",
        "priority": "low|medium|high|critical"
      }
    ],
    "next_steps": "What should happen next",
    "open_questions": ["Unresolved issues"],
    "overall_outcome": "Summary of what was accomplished"
  }
}
```"""
        ),
        HumanMessagePromptTemplate.from_template(
            "Create a comprehensive summary of this conversation:\n\n{conversation_text}"
        ),
    ]
)


# ============================================================================
# PROMPT TEMPLATE REGISTRY
# ============================================================================

EXTRACTION_PROMPTS = {
    "professional": PROFESSIONAL_INFORMATION_EXTRACTOR,
    "personal": PERSONAL_CONTEXT_EXTRACTOR,
    "technical": TECHNICAL_KNOWLEDGE_EXTRACTOR,
    "projects": PROJECT_AND_TASK_EXTRACTOR,
    "entities": ENTITY_RELATIONSHIP_EXTRACTOR,
    "product": PRODUCT_MANAGEMENT_EXTRACTOR,
    "engineering": ENGINEERING_CONTEXT_EXTRACTOR,
    "sentiment": SENTIMENT_AND_TONE_EXTRACTOR,
    "decisions": DECISION_MAKING_EXTRACTOR,
    "summary": CONVERSATION_SUMMARY_EXTRACTOR,
}


def get_extraction_prompt(prompt_type: str) -> ChatPromptTemplate:
    """Get extraction prompt by type.

    Args:
        prompt_type: One of the available prompt types

    Returns:
        ChatPromptTemplate for the specified extraction type

    Raises:
        ValueError: If prompt_type is not available
    """
    if prompt_type not in EXTRACTION_PROMPTS:
        available = ", ".join(EXTRACTION_PROMPTS.keys())
        raise ValueError(f"Unknown prompt type '{prompt_type}'. Available: {available}")

    return EXTRACTION_PROMPTS[prompt_type]


def get_all_extraction_types() -> list[str]:
    """Get list of all available extraction types."""
    return list(EXTRACTION_PROMPTS.keys())


# ============================================================================
# EXTRACTION ORCHESTRATOR
# ============================================================================


class ExtractionOrchestrator:
    """Orchestrates multiple extraction types on the same content."""

    def __init__(self, llm_config=None):
        """Initialize with LLM configuration."""
        self.llm_config = llm_config
        if llm_config:
            self.llm = llm_config.instantiate()

    async def extract_all(
        self, conversation_text: str, extraction_types: list[str] = None
    ) -> dict[str, Any]:
        """Run multiple extractors on the same conversation.

        Args:
            conversation_text: The conversation to analyze
            extraction_types: Which extractors to run (default: all)

        Returns:
            Dictionary with results from each extractor
        """
        if extraction_types is None:
            extraction_types = get_all_extraction_types()

        results = {}

        for extraction_type in extraction_types:
            try:
                prompt = get_extraction_prompt(extraction_type)

                if self.llm:
                    # Use configured LLM
                    chain = prompt | self.llm
                    result = await chain.ainvoke(
                        {"conversation_text": conversation_text}
                    )
                    results[extraction_type] = (
                        result.content if hasattr(result, "content") else str(result)
                    )
                else:
                    # Return prompt for external processing
                    formatted_prompt = prompt.format(
                        conversation_text=conversation_text
                    )
                    results[extraction_type] = {"prompt": formatted_prompt}

            except Exception as e:
                results[extraction_type] = {"error": str(e)}

        return results

    def get_focused_extractors(self, domain: str) -> list[str]:
        """Get recommended extractors for a specific domain.

        Args:
            domain: Domain type (e.g., 'product', 'engineering', 'general')

        Returns:
            List of recommended extraction types
        """
        domain_mappings = {
            "product": ["professional", "projects", "product", "decisions", "summary"],
            "engineering": [
                "professional",
                "technical",
                "engineering",
                "projects",
                "summary",
            ],
            "general": ["professional", "personal", "entities", "summary"],
            "analysis": ["sentiment", "decisions", "entities", "summary"],
            "comprehensive": get_all_extraction_types(),
        }

        return domain_mappings.get(domain, ["professional", "entities", "summary"])
