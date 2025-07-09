"""Tests for SimpleAgent specific use cases and examples."""

from agents.simple.factory import create_simple_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


def test_basic_agent():
    """Test a basic SimpleAgent with default settings."""
    agent = create_simple_agent(
        system_prompt="You are a helpful assistant.", name="test_simple_agent"
    )

    # Verify agent configuration
    assert agent.config.name == "test_simple_agent"
    assert agent.config.system_prompt == "You are a helpful assistant."
    assert agent.config.state_schema is not None

    # Test running the agent
    result = agent.run("What is the capital of France?")
    assert "messages" in result
    assert len(result["messages"]) > 1  # Should have at least the question and response


def test_summarizer_agent():
    """Test creating a simple agent as a summarizer."""
    map_prompt = ChatPromptTemplate.from_messages(
        [("human", "Write a concise summary of the following:\n\n{context}")]
    )

    map_aug_llm_config = AugLLMConfig(
        name="summarizer_map",
        prompt_template=map_prompt,
        output_parser=StrOutputParser(),
    )

    summarizer_agent = create_simple_agent(
        engine=map_aug_llm_config, name="simple_agent_summarizer", visualize=True
    )

    # Verify agent configuration
    assert summarizer_agent.config.name == "simple_agent_summarizer"
    assert summarizer_agent.config.engine.name == "summarizer_map"

    # Test running with context
    result = summarizer_agent.run(
        {
            "context": "Paris is the capital of France. It is known for its art, culture, and the Eiffel Tower."
        }
    )
    assert "messages" in result


class QA(BaseModel):
    """Question and Answer model for structured output."""

    question: str = Field(description="The question that was asked.")
    answer: str = Field(description="The answer to the question.")


class QAs(BaseModel):
    """Container for multiple QA pairs."""

    qas: list[QA] = Field(description="A list of question and answer pairs.")


def test_qa_agent():
    """Test creating a QA agent with structured output."""
    # QA system prompt
    qa_system_prompt = """You are an AI assistant specializing in generating questions and answers from text.
    Extract important facts and create question-answer pairs from the input."""

    # Prompt template
    qa_prompt_template = ChatPromptTemplate.from_messages(
        [("system", qa_system_prompt), ("user", "{contents}")]
    )

    # Create AugLLM config
    qa_aug_llm_config = AugLLMConfig(
        llm_config=AzureLLMConfig(model="gpt-4o"),
        structured_output_model=QAs,
        prompt_template=qa_prompt_template,
    )

    # Create QA agent
    qa_agent = create_simple_agent(
        engine=qa_aug_llm_config,
        name="simple_qa_agent",
        visualize=True,
        mock_response=True,  # Add mock response for testing
    )

    # Verify agent configuration
    assert qa_agent.config.engine.structured_output_model == QAs
    assert qa_agent.config.name == "simple_qa_agent"

    # A short text for testing
    test_text = "Marie Curie was a Polish-born physicist and chemist known for her pioneering research on radioactivity."

    # Run the agent
    result = qa_agent.run({"contents": test_text})

    # Check for messages
    assert "messages" in result

    # Check for qas field directly in result
    assert "qas" in result
    # Alternative: If qas not directly in result but inside a nested field
    if "qas" not in result and "output" in result:
        assert hasattr(result["output"], "qas")


def test_document_structure_agent():
    """Test creating an agent for document structuring."""
    # Document splitting prompt
    split_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Analyze the given document and split it into a structured hierarchy with sections and subsections.",
            ),
            ("user", "{contents}"),
        ]
    )

    # Create AugLLM config
    split_aug_llm = AugLLMConfig(
        name="document_splitter",
        prompt_template=split_prompt,
        structured_output_model=DocumentHierarchy,
    )

    # Create document structure agent
    split_agent = create_simple_agent(
        engine=split_aug_llm,
        name="document_split_agent",
        mock_response=True,  # Add mock response
    )

    # Verify agent configuration
    assert split_agent.config.engine.structured_output_model == DocumentHierarchy
    assert split_agent.config.name == "document_split_agent"

    # A short text for testing
    test_text = """# Introduction to Python
    
    Python is a popular programming language.
    
    ## Basic Syntax
    
    Python has a simple syntax that is easy to learn.
    
    ## Data Types
    
    Python supports various data types including strings, numbers, and lists.
    """

    # Run the agent
    result = split_agent.run({"contents": test_text})

    # Check for messages
    assert "messages" in result

    # Check for documenthierarchy field directly in result (lowercase model name)
    assert "documenthierarchy" in result
    # Alternative check for title inside the object
    if "documenthierarchy" in result:
        assert hasattr(result["documenthierarchy"], "title")
    # Fallback if implemented differently
    elif "output" in result:
        assert hasattr(result["output"], "title")
