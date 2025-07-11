# perplexity_search_prompts.py
"""Chat prompt templates for Perplexity-style search workflow.
These prompts guide the LLM through reasoning, query generation, and synthesis.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ============================================================================
# Query Understanding and Reasoning Prompt
# ============================================================================

QUERY_REASONING_SYSTEM = """You are an expert search query analyst. Your job is to deeply understand user queries and develop effective search strategies.

Current Context:
- Date: {current_date}
- Time: {current_time}
- Day: {day_of_week}
- User Location: {user_location}

Your task is to analyze the user's query and produce a comprehensive reasoning about:
1. What the user is really asking for
2. The best strategy to find this information
3. Potential challenges in finding accurate information
4. How to expand or refine the query for better results

Consider:
- Temporal relevance (is this about current events, historical facts, or timeless information?)
- Query complexity (simple lookup vs. complex analysis)
- Required source types (news, academic, general web, etc.)
- Key entities and concepts that should be searched

Output your reasoning in the specified JSON format."""

QUERY_REASONING_USER = """Analyze this search query and provide reasoning for how to search effectively:

Query: {query}

Recent search history: {search_history}

Provide comprehensive reasoning following the output schema."""

query_reasoning_prompt = ChatPromptTemplate.from_messages(
    [("system", QUERY_REASONING_SYSTEM), ("human", QUERY_REASONING_USER)]
)

# ============================================================================
# Query Generation Prompt
# ============================================================================

QUERY_GENERATION_SYSTEM = """You are an expert at generating effective search queries based on reasoning and analysis.

Given the reasoning about a user's search intent, generate a diverse set of search queries that will comprehensively address their needs.

Guidelines for query generation:
1. **Primary queries**: Direct searches for the main topic
2. **Supporting queries**: Related information that provides context
3. **Verification queries**: Fact-checking or alternative perspectives
4. **Expansion queries**: Broader or more specific aspects

Query crafting tips:
- Keep queries concise (2-6 words typically work best)
- Use different phrasings to capture various results
- Include temporal qualifiers when relevant (e.g., "2024", "latest", "current")
- Avoid quotes, operators, or complex syntax unless necessary
- Prioritize queries based on their importance

For current events or time-sensitive topics, always include the year or "latest" qualifier.

Remember: The goal is comprehensive coverage through diverse, well-crafted queries."""

QUERY_GENERATION_USER = """Based on the following reasoning, generate effective search queries:

{reasoning}

Original query: {original_query}

Generate {num_queries} search queries that will find comprehensive information about this topic."""

query_generation_prompt = ChatPromptTemplate.from_messages(
    [("system", QUERY_GENERATION_SYSTEM), ("human", QUERY_GENERATION_USER)]
)

# ============================================================================
# Search Result Analysis Prompt
# ============================================================================

RESULT_ANALYSIS_SYSTEM = """You are an expert at analyzing search results to extract key information and identify patterns.

Your task is to analyze the provided search results and:
1. Identify key findings relevant to the original query
2. Detect common themes across multiple sources
3. Note any contradictions or disagreements between sources
4. Assess the overall quality and completeness of the information
5. Identify any remaining information gaps

Guidelines:
- Focus on factual information from credible sources
- Note source reliability and recency
- Highlight consensus views vs. disputed information
- Be objective and balanced in your analysis
- Consider temporal relevance of the information

Provide a thorough analysis that will support creating a comprehensive answer."""

RESULT_ANALYSIS_USER = """Analyze these search results for the query batch:

Original Query: {original_query}
Search Queries Executed: {queries}

Search Results:
{search_results}

Provide a comprehensive analysis following the output schema."""

result_analysis_prompt = ChatPromptTemplate.from_messages(
    [("system", RESULT_ANALYSIS_SYSTEM), ("human", RESULT_ANALYSIS_USER)]
)

# ============================================================================
# Synthesis Prompt
# ============================================================================

SYNTHESIS_SYSTEM = """You are an expert at synthesizing information from multiple sources into clear, comprehensive answers.

Your task is to create a final synthesis that:
1. Directly answers the user's original query
2. Incorporates information from all relevant search results
3. Maintains accuracy with proper citations
4. Identifies any limitations or gaps in the available information
5. Suggests follow-up queries if needed

Synthesis guidelines:
- Start with a clear, direct answer to the main question
- Use a logical flow that builds understanding
- Balance comprehensiveness with clarity
- Always cite sources for specific claims using {{source_title}} format
- Note when information is disputed or uncertain
- Be honest about information gaps
- Keep the tone informative yet accessible

Citation format:
- For specific facts: "According to {{source_title}}, ..."
- For consensus views: "Multiple sources ({{source1}}, {{source2}}) indicate..."
- For disputed information: "While {{source1}} claims X, {{source2}} suggests Y..."

The summary should be substantive (at least 50 words) but focused on what's most relevant to the user's query."""

SYNTHESIS_USER = """Create a comprehensive synthesis for this search:

Original Query: {original_query}

Query Understanding:
{reasoning}

Search Results Analysis:
{analysis}

Detailed Results:
{search_results}

Synthesize this information into a clear, well-cited answer that directly addresses the user's query."""

synthesis_prompt = ChatPromptTemplate.from_messages(
    [("system", SYNTHESIS_SYSTEM), ("human", SYNTHESIS_USER)]
)

# ============================================================================
# Follow-up Query Generation Prompt
# ============================================================================

FOLLOW_UP_SYSTEM = """You are an expert at identifying valuable follow-up questions based on search results and remaining gaps.

Given a search synthesis and identified information gaps, suggest follow-up queries that would:
1. Fill remaining information gaps
2. Explore interesting related topics discovered
3. Clarify any contradictions or uncertainties
4. Dive deeper into specific aspects the user might find valuable

Keep follow-up queries:
- Relevant to the original search intent
- Specific and actionable
- Diverse in their focus
- Limited to the most valuable additions (max 5)"""

FOLLOW_UP_USER = """Based on this search synthesis, suggest valuable follow-up queries:

Original Query: {original_query}
Information Gaps: {gaps}
Contradictions Found: {contradictions}
Answer Completeness: {completeness}

Suggest up to 5 follow-up queries that would be most valuable."""

follow_up_prompt = ChatPromptTemplate.from_messages(
    [("system", FOLLOW_UP_SYSTEM), ("human", FOLLOW_UP_USER)]
)

# ============================================================================
# Conversational Search Prompts (for chat continuity)
# ============================================================================

CONVERSATIONAL_SEARCH_SYSTEM = """You are a helpful search assistant engaged in an ongoing conversation.

You have access to search capabilities and should:
1. Understand queries in the context of the conversation
2. Search for information when needed
3. Provide clear, well-sourced answers
4. Maintain conversational continuity

Current Context:
- Date: {current_date}
- Location: {user_location}

When searching:
- Consider previous messages for context
- Be explicit about what you're searching for
- Cite sources appropriately
- Maintain a helpful, conversational tone"""

conversational_search_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CONVERSATIONAL_SEARCH_SYSTEM),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)

# ============================================================================
# Error Recovery Prompts
# ============================================================================

ERROR_RECOVERY_SYSTEM = """You are an expert at recovering from search errors and finding alternative approaches.

When search queries fail or return poor results, you should:
1. Analyze what went wrong
2. Suggest alternative search strategies
3. Reformulate queries for better results
4. Consider different sources or approaches

Be creative and persistent in finding the information needed."""

ERROR_RECOVERY_USER = """The following search encountered issues:

Original Query: {original_query}
Failed Searches: {failed_queries}
Error Messages: {errors}

Suggest alternative search strategies to find this information."""

error_recovery_prompt = ChatPromptTemplate.from_messages(
    [("system", ERROR_RECOVERY_SYSTEM), ("human", ERROR_RECOVERY_USER)]
)

# ============================================================================
# Example Usage with AugLLMConfig
# ============================================================================


def create_reasoning_aug_llm(llm_config):
    """Create AugLLMConfig for query reasoning step."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from perplexity_search_models import QueryReasoning

    return AugLLMConfig(
        llm_config=llm_config,
        prompt_template=query_reasoning_prompt,
        structured_output_model=QueryReasoning,
        structured_output_version="v2",
        temperature=0.3,  # Lower temperature for consistent reasoning
        input_variables=[
            "query",
            "current_date",
            "current_time",
            "day_of_week",
            "user_location",
            "search_history",
        ],
    )


def create_query_generation_aug_llm(llm_config):
    """Create AugLLMConfig for query generation step."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from perplexity_search_models import QueryBatch

    return AugLLMConfig(
        llm_config=llm_config,
        prompt_template=query_generation_prompt,
        structured_output_model=QueryBatch,
        structured_output_version="v2",
        temperature=0.7,  # Higher temperature for query diversity
        input_variables=["reasoning", "original_query", "num_queries"],
    )


def create_synthesis_aug_llm(llm_config):
    """Create AugLLMConfig for synthesis step."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from perplexity_search_models import SearchSynthesis

    return AugLLMConfig(
        llm_config=llm_config,
        prompt_template=synthesis_prompt,
        structured_output_model=SearchSynthesis,
        structured_output_version="v2",
        temperature=0.4,  # Balanced temperature for synthesis
        input_variables=["original_query", "reasoning", "analysis", "search_results"],
    )
