# src/haive/agents/task_analysis/context/prompts.py

from langchain_core.prompts import ChatPromptTemplate

CONTEXT_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a context requirements analyst specializing in information flow and knowledge dependencies.

Your expertise covers:
- Information requirement analysis
- Knowledge domain identification
- Context size estimation
- Data freshness requirements
- Integration point mapping

Context Sizes:
- **minimal**: < 500 tokens (quick lookups, simple facts)
- **small**: 500-2k tokens (short documents, API responses)
- **medium**: 2k-10k tokens (research papers, documentation)
- **large**: 10k-50k tokens (books, large codebases)
- **massive**: 50k+ tokens (entire knowledge domains)

Freshness Requirements:
- **realtime**: Live data required (stock prices, sensor data)
- **recent**: Hours to days old (news, weather)
- **current**: Weeks to months old (documentation, research)
- **historical**: Any age acceptable (facts, historical data)

Domain Expertise Levels:
- **basic**: General knowledge
- **intermediate**: Some domain familiarity
- **advanced**: Deep domain knowledge
- **expert**: Cutting-edge expertise""",
        ),
        (
            "human",
            """Analyze context requirements for:

**Task Description**: {task_description}
**Task Type**: {task_type}
**Domain**: {domain}

**Subtasks Identified**:
{subtask_list}

**Task Dependencies**:
{dependencies}

Analyze:

1. **Input Context Requirements**:
   - What information is needed to start?
   - How much context (size estimate)?
   - Which knowledge domains?
   - How fresh must data be?
   - What are trusted sources?

2. **Working Context**:
   - What context accumulates during execution?
   - How does context flow between tasks?
   - What must be maintained in memory?
   - Are there size constraints?

3. **Output Context**:
   - What information is produced?
   - How should it be structured?
   - What's the expected size?
   - Who will consume it?

4. **Domain Requirements**:
   - List all knowledge domains needed
   - Specify expertise level for each
   - Identify specific topics
   - Note preferred sources

5. **Integration Points**:
   - Where do contexts merge?
   - What transformations are needed?
   - How to handle conflicts?
   - What's the integration complexity?

6. **Quality Requirements**:
   - Accuracy needs
   - Completeness requirements
   - Validation criteria
   - Source reliability

Return a ContextRequirement object with all fields populated.""",
        ),
    ]
)

CONTEXT_FLOW_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are analyzing how context flows between tasks, identifying transformations and integration points.""",
        ),
        (
            "human",
            """Map context flow for:

**Task Tree**: {task_tree}
**Task Dependencies**: {dependencies}

For each task connection:
1. What data flows between tasks?
2. What transformations occur?
3. Is the flow required or optional?
4. What's the data volume?
5. Are there timing constraints?

Return list of ContextFlow objects.""",
        ),
    ]
)

CONTEXT_OPTIMIZATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are optimizing context loading and caching strategies for efficient execution.""",
        ),
        (
            "human",
            """Optimize context strategy for:

**Context Requirements**: {context_requirements}
**Memory Constraints**: {memory_limits}
**Performance Goals**: {performance_goals}

Design:
1. Loading strategy (eager/lazy/streaming)
2. Caching approach
3. Memory management
4. Prefetching opportunities
5. Context compression

Return optimized context management plan.""",
        ),
    ]
)

DOMAIN_EXPERTISE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are identifying and categorizing knowledge domain requirements for task execution.""",
        ),
        (
            "human",
            """Analyze domain expertise for:

**Task**: {task_description}
**Subtasks**: {subtask_list}

For each identified domain:
1. Domain name and scope
2. Required expertise level
3. Specific topics/skills
4. Learning resources
5. Expert availability

Return list of ContextDomain objects.""",
        ),
    ]
)
