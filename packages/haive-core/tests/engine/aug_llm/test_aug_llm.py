import json
import logging

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig, RunnableLambda
from pydantic import BaseModel

from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from haive.core.models.llm.base import AzureLLMConfig

# Setup logger with more visible formatting
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="\n%(asctime)s [%(levelname)s] %(name)s:\n%(message)s"
)


def log_test_result(test_name, result):
    """Format and log test results for better visibility."""
    separator = "=" * 70
    log_msg = f"\n{separator}\n✅ TEST: {test_name}\n{separator}\n"

    # Pretty format the result based on type
    if hasattr(result, "model_dump"):
        try:
            log_msg += f"RESULT:\n{json.dumps(result.model_dump(), indent=2)}\n"
        except:
            log_msg += f"RESULT:\n{result}\n"
    elif isinstance(result, dict):
        try:
            log_msg += f"RESULT:\n{json.dumps(result, indent=2)}\n"
        except:
            log_msg += f"RESULT:\n{result}\n"
    else:
        log_msg += f"RESULT:\n{result}\n"

    log_msg += f"{separator}\n"
    logger.info(log_msg)
    return result


class DummyOutput(BaseModel):
    answer: str


def test_basic_init():
    config = AugLLMConfig(llm_config=AzureLLMConfig(model="gpt-4o"))
    result = {
        "llm_config": str(config.llm_config),
        "engine_type": config.engine_type.value,
    }
    log_test_result("test_basic_init", result)
    assert config.llm_config.model == "gpt-4o"
    assert config.engine_type.value == "llm"


def test_prompt_template_input_schema():
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are helpful"),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    config = AugLLMConfig.from_prompt(prompt)
    schema = config.derive_input_schema()
    result = {"schema_fields": list(schema.model_fields.keys())}
    log_test_result("test_prompt_template_input_schema", result)
    assert "messages" in schema.model_fields


def test_output_schema_with_structured_output():
    config = AugLLMConfig(
        llm_config=AzureLLMConfig(model="gpt-4o"), structured_output_model=DummyOutput
    )
    schema = config.derive_output_schema()
    result = {"schema_fields": list(schema.model_fields.keys())}
    log_test_result("test_output_schema_with_structured_output", result)
    assert "answer" in schema.model_fields or "dummyoutput" in schema.model_fields


def test_process_input_string():
    config = AugLLMConfig(llm_config=AzureLLMConfig(model="gpt-4o"))
    processed = config._process_input("Hello!")
    result = {
        "message_type": type(processed["messages"][0]).__name__,
        "content": processed["messages"][0].content,
    }
    log_test_result("test_process_input_string", result)
    assert isinstance(processed["messages"][0], HumanMessage)
    assert processed["messages"][0].content == "Hello!"


def test_invoke_runs(monkeypatch):
    def mock_llm(input):
        # Create a proper AIMessage as the return value
        from langchain_core.messages import AIMessage

        # Return an AIMessage object directly to match the expected return type
        return AIMessage(content="This is a mock response")

    # Fix the monkeypatch path to use the correct import path
    monkeypatch.setattr(
        "haive.core.models.llm.base.AzureLLMConfig.instantiate",
        lambda self: RunnableLambda(mock_llm),
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful assistant."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    config = AugLLMConfig(
        llm_config=AzureLLMConfig(model="gpt-4o"), prompt_template=prompt
    )

    result = config.invoke("What's the weather like?")
    log_result = {
        "type": type(result).__name__,
        "content": result.content if hasattr(result, "content") else str(result),
    }
    log_test_result("test_invoke_runs", log_result)

    assert isinstance(result, AIMessage)
    assert hasattr(result, "content")
    assert "mock response" in result.content


def test_compose_runnable_creates_chain(monkeypatch):
    # Fix the monkeypatch path to use the correct import path
    monkeypatch.setattr(
        "haive.core.models.llm.base.AzureLLMConfig.instantiate",
        lambda self: RunnableLambda(lambda x: x),
    )
    config = AugLLMConfig(llm_config=AzureLLMConfig(model="gpt-4o"))
    chain = compose_runnable(config)
    result = {
        "has_invoke": hasattr(chain, "invoke"),
        "chain_type": type(chain).__name__,
    }
    log_test_result("test_compose_runnable_creates_chain", result)
    assert hasattr(chain, "invoke")


def test_apply_runnable_config_overrides(monkeypatch):
    # Fix the monkeypatch path to use the correct import path
    monkeypatch.setattr(
        "haive.core.models.llm.base.AzureLLMConfig.instantiate",
        lambda self: RunnableLambda(lambda x: x),
    )
    config = AugLLMConfig(llm_config=AzureLLMConfig(model="gpt-4o"))
    rcfg = RunnableConfig(configurable={"temperature": 0.1})
    resolved = config.apply_runnable_config(rcfg)
    log_test_result("test_apply_runnable_config_overrides", resolved)
    assert resolved.get("temperature") == 0.1


@pytest.mark.skip(reason="Requires actual API keys - for manual testing only")
def test_invoke_runs_real_llm():
    from haive.core.models.llm.base import AzureLLMConfig

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful assistant."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    config = AugLLMConfig(
        llm_config=AzureLLMConfig(model="gpt-4o"), prompt_template=prompt
    )

    # Actually invoke the real LLM
    result = config.invoke("What is the capital of France?")

    log_result = {
        "type": type(result).__name__,
        "content": result.content if hasattr(result, "content") else str(result),
    }
    log_test_result("test_invoke_runs_real_llm", log_result)

    # Show the content based on actual return type
    if hasattr(result, "content"):
        assert "Paris" in result.content
    elif isinstance(result, dict) and "messages" in result:
        for m in result["messages"]:
            assert any("Paris" in m.content for m in result["messages"])
    else:
        raise TypeError(f"Unexpected result format: {type(result)}")
