# tests/test_simple_agent.py

from haive.core.engine.agent.agent import SimpleAgent, SimpleAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel


# Test creating simple agent
def test_create_simple_agent():
    # Create config
    config = SimpleAgentConfig(
        name="test_simple_agent", engine=AugLLMConfig(name="test_llm", model="gpt-4")
    )

    # Build agent
    agent = config.build_agent()

    # Check agent properties
    assert isinstance(agent, SimpleAgent)
    assert agent.config.name == "test_simple_agent"
    assert agent.engine is not None
    assert hasattr(agent, "graph")
    assert hasattr(agent, "app")

    # Check single node setup
    assert "process" in agent.graph.nodes


# Test with structured output
def test_simple_agent_structured_output():
    # Define a structured output model
    class TestOutput(BaseModel):
        answer: str
        reasoning: str = ""

    # Create config with structured output
    config = SimpleAgentConfig(
        name="structured_agent",
        engine=AugLLMConfig(
            name="structured_llm", model="gpt-4", structured_output_model=TestOutput
        ),
    )

    # Build agent
    agent = config.build_agent()

    # Check schema has the structured fields
    assert hasattr(agent.state_schema, "model_fields")
    assert "answer" in agent.state_schema.model_fields
    assert "reasoning" in agent.state_schema.model_fields


# Test running simple agent with basic input
def test_simple_agent_run():
    # Create config
    config = SimpleAgentConfig(
        name="runnable_agent",
        engine=AugLLMConfig(
            name="test_llm",
            model="gpt-4",
            temperature=0,  # For deterministic testing
            max_tokens=50,  # Limit output size for tests
        ),
    )

    # Mock the engine's invoke method to avoid actual API calls
    def mock_invoke(self, input_data, runnable_config=None):
        messages = input_data.get("messages", [])
        if messages and len(messages) > 0:
            content = messages[-1].content
            return {"response": f"Processed: {content}", "messages": messages}
        return {"response": "No input", "messages": messages}

    # Apply the mock
    import types

    config.engine.invoke = types.MethodType(mock_invoke, config.engine)

    # Build agent
    agent = config.build_agent()

    # Run with string input
    result = agent.run("Test input")

    # Check result
    assert "response" in result
    assert result["response"] == "Processed: Test input"
    assert "messages" in result
    assert len(result["messages"]) > 0


# Test agent with custom node name
def test_custom_node_name():
    # Create config with custom node name
    config = SimpleAgentConfig(name="custom_node_agent", node_name="custom_process")

    # Build agent
    agent = config.build_agent()

    # Check node exists
    assert "custom_process" in agent.graph.nodes
