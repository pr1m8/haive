"""Query Rewriting Agent for Agentic RAG.

This agent rewrites queries to improve retrieval using existing models from common.
"""

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.rag.common.query_refinement.models import QueryRefinementResponse
from haive.agents.simple import SimpleAgent


def create_query_rewriter_agent(
    name: str = "query_rewriter", temperature: float = 0.7, **kwargs
) -> SimpleAgent:
    """Create a query rewriter agent using direct SimpleAgent instantiation.

    Args:
        name: Agent name (default: "query_rewriter")
        temperature: LLM temperature (default: 0.7 for creativity)
        **kwargs: Additional configuration options

    Returns:
        SimpleAgent configured for query refinement

    Example:
        .. code-block:: python

            # Create query rewriter agent
            rewriter = create_query_rewriter_agent(
            name="query_rewritef",
            temperature=0.7
            )

            # Rewrite a query
            result = await rewriter.arun({
            "query": "quantum computing basics"
            })

            # Access results
            print(f"Original: {result.original_query}")
            print(f"Best rewrite: {result.best_refined_query}")
            for suggestion in result.refinement_suggestions:
            print(f"- {suggestion.refined_query} ({suggestion.improvement_type})")

    """
    prompt_template = (
        "You are a query optimization specialist for RAG systems. "
        "Your role is to analyze queries and suggest improvements for better retrieval.\n\n"
        "Guidelines:\n"
        "1. Make queries more specific and clear\n"
        "2. Add relevant context or constraints\n"
        "3. Use appropriate technical terminology\n"
        "4. Consider different phrasings that might yield better results\n"
        "5. Break down complex queries if needed\n\n"
        "Provide multiple suggestions with clear rationales and select the best one.\n\n"
        "Query to rewrite: {query}\n\n"
        "Context: {context}"
    )

    return SimpleAgent(
        name=name,
        engine=AugLLMConfig(
            temperature=temperature,
            prompt_template=prompt_template,
            structured_output_model=QueryRefinementResponse,
            structured_output_version="v2",
        ),
        **kwargs
    )


async def rewrite_query(
    agent: SimpleAgent, query: str, context: str = ""
) -> QueryRefinementResponse:
    """Rewrite a query to improve retrieval.

    Args:
        agent: The query rewriter agent
        query: The original query to rewrite
        context: Optional context to help with rewriting

    Returns:
        QueryRefinementResponse with refinement suggestions
    """
    # Format the input for the agent
    input_data = {
        "query": query,
        "context": context or "No additional context provided",
    }

    # Run the agent
    result = await agent.arun(input_data)

    # Return the structured result
    return result
