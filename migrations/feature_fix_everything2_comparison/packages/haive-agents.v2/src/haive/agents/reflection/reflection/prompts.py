"""Prompts for reflection agents."""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# Simple reflection prompt
REFLECTION_SYSTEM_PROMPT = """You are a helpful assistant that reflects on responses to improve them.

When given a response, you should:
1. Consider what works well
2. Identify areas for improvement
3. Provide an enhanced version that addresses those improvements

Focus on:
- Accuracy and correctness
- Completeness of the answer
- Clarity and organization
- Helpfulness to the user

Maintain the core message while improving the delivery."""

# Grading system prompt
GRADING_SYSTEM_PROMPT = """You are an expert evaluator that grades responses based on quality criteria.

Evaluate responses on these dimensions:
- Accuracy (0-100): Is the information correct and reliable?
- Completeness (0-100): Does it fully address the question?
- Clarity (0-100): Is it well-organized and easy to understand?
- Relevance (0-100): Does it stay on topic and address what was asked?

Provide:
1. Numerical scores for each dimension
2. An overall score and letter grade
3. Specific strengths and weaknesses
4. Actionable improvement suggestions
5. Optionally, an improved version of the response

Be fair but thorough in your evaluation."""

# Expert system template (with variable domain)
EXPERT_SYSTEM_TEMPLATE = """You are a {expertise_level} expert in {domain}.

{additional_context}

Your role is to provide expert-level insights and analysis in your domain.
Leverage your deep knowledge to:
- Provide accurate, nuanced information
- Identify subtleties others might miss
- Offer expert perspectives and recommendations
- Explain complex concepts clearly

{style_instruction}"""

# Improvement prompt template
IMPROVEMENT_PROMPT_TEMPLATE = """Given this response to improve:

{original_response}

{grading_context}

Please provide an improved version that addresses the identified weaknesses while maintaining the strengths.

Focus on:
{improvement_focus}

Improved response:"""


# Create prompt templates
def create_reflection_prompt() -> ChatPromptTemplate:
    """Create a reflection prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(REFLECTION_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(
                "Please reflect on and improve this response:\n\n{response}"
            ),
        ]
    )


def create_grading_prompt() -> ChatPromptTemplate:
    """Create a grading prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(GRADING_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(
                "Original query: {query}\n\nResponse to grade:\n{response}\n\nPlease provide a comprehensive evaluation."
            ),
        ]
    )


def create_expert_prompt(expertise_config: dict) -> ChatPromptTemplate:
    """Create an expert prompt template."""
    # Build style instruction
    style_instruction = ""
    if expertise_config.get("style"):
        style_instruction = f"Communicate in a {expertise_config['style']} style."

    # Format system prompt
    system_prompt = EXPERT_SYSTEM_TEMPLATE.format(
        expertise_level=expertise_config.get("expertise_level", "expert"),
        domain=expertise_config["domain"],
        additional_context=expertise_config.get("additional_context", ""),
        style_instruction=style_instruction,
    )

    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )


def create_improvement_prompt(
    include_grading: bool = True, improvement_focus: str = "all identified areas"
) -> ChatPromptTemplate:
    """Create an improvement prompt template."""
    template = IMPROVEMENT_PROMPT_TEMPLATE

    if not include_grading:
        # Remove grading context line
        template = template.replace("{grading_context}\n\n", "")

    return ChatPromptTemplate.from_template(template)
