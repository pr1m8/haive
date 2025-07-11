from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from haive.agents.research.open_perplexity.models import (
    ResearchFinding,
    ResearchSource,
    ResearchSummary,
)
from haive.agents.research.open_perplexity.prompts import (
    CONFIDENCE_ASSESSMENT_PROMPT,
    DATA_SOURCE_SELECTION_PROMPT,
    FINAL_REPORT_COMPILATION_PROMPT,
    MAIN_SYSTEM_PROMPT,
    QUERY_GENERATION_PROMPT,
    REPORT_PLANNING_PROMPT,
    SECTION_WRITING_PROMPT,
    SOURCE_EVALUATION_PROMPT,
    TOPIC_EXTRACTION_PROMPT,
)

engines = {}

# Topic extraction engine
topic_extraction_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are an information extraction assistant that identifies research topics and questions from user input."
        ),
        HumanMessage(content=TOPIC_EXTRACTION_PROMPT),
    ]
)

engines["topic_extraction"] = AugLLMConfig(
    name="topic_extraction",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2),
    prompt_template=topic_extraction_template,
)

# Report planning engine
report_planning_template = ChatPromptTemplate.from_template(REPORT_PLANNING_PROMPT)

engines["report_planning"] = AugLLMConfig(
    name="report_planning",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2),
    prompt_template=report_planning_template,
)

# Query generation engine
query_generation_template = ChatPromptTemplate.from_template(QUERY_GENERATION_PROMPT)

engines["query_generation"] = AugLLMConfig(
    name="query_generation",
    llm_config=AzureLLMConfig(
        model="gpt-4o", temperature=0.3
    ),  # Higher temp for creative queries
    prompt_template=query_generation_template,
)

# Section writing engine
section_writing_template = ChatPromptTemplate.from_template(SECTION_WRITING_PROMPT)

engines["section_writing"] = AugLLMConfig(
    name="section_writing",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2),
    prompt_template=section_writing_template,
)

# Source evaluation engine
source_evaluation_template = ChatPromptTemplate.from_template(SOURCE_EVALUATION_PROMPT)

engines["source_evaluation"] = AugLLMConfig(
    name="source_evaluation",
    llm_config=AzureLLMConfig(
        model="gpt-4o", temperature=0.1
    ),  # Lower temp for objective evaluation
    prompt_template=source_evaluation_template,
    structured_output_model=ResearchSource,
)

# Research finding engine
research_finding_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
    You are a research analyst who synthesizes information into clear findings.
    For each finding, you will assess confidence based on the quality and consistency of sources.
    """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

engines["research_finding"] = AugLLMConfig(
    name="research_finding",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.1),
    prompt_template=research_finding_template,
    structured_output_model=ResearchFinding,
)

# Confidence assessment engine
confidence_assessment_template = ChatPromptTemplate.from_template(
    CONFIDENCE_ASSESSMENT_PROMPT
)

engines["confidence_assessment"] = AugLLMConfig(
    name="confidence_assessment",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.1),
    prompt_template=confidence_assessment_template,
)

# Research summary engine
research_summary_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""
    You are a research analyst who summarizes research findings.
    Your task is to assess the overall quality, depth, and confidence of the research.
    """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

engines["research_summary"] = AugLLMConfig(
    name="research_summary",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.1),
    prompt_template=research_summary_template,
    structured_output_model=ResearchSummary,
)

# Data source selection engine
data_source_selection_template = ChatPromptTemplate.from_template(
    DATA_SOURCE_SELECTION_PROMPT
)

engines["data_source_selection"] = AugLLMConfig(
    name="data_source_selection",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2),
    prompt_template=data_source_selection_template,
)

# Final report compilation engine
final_report_template = ChatPromptTemplate.from_template(
    FINAL_REPORT_COMPILATION_PROMPT
)

engines["final_report_compilation"] = AugLLMConfig(
    name="final_report_compilation",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2),
    prompt_template=final_report_template,
)

# Main engine
main_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=MAIN_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

engines["main"] = AugLLMConfig(
    name="main",
    llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.2),
    prompt_template=main_template,
)


def create_research_engines():
    """Create and return the dictionary of research engines.

    Returns:
        dict: Dictionary mapping engine names to their configurations
    """
    return engines
