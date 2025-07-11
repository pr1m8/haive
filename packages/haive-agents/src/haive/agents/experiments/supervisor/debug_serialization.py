"""Debug what exactly is not serializable in the agent objects."""

import ormsgpack
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.react.agent import ReactAgent


def test_serialization(obj, name):
    """Test if an object can be serialized with msgpack."""
    try:
        ormsgpack.packb(obj)
        return True
    except Exception as e:
        return False


def analyze_agent_serialization():
    """Analyze what parts of an agent are not serializable."""

    # Create a ReactAgent
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    test_serialization("simple string", "string")
    test_serialization(123, "int")
    test_serialization({"key": "value"}, "dict")
    test_serialization(["item"], "list")

    test_serialization(search_agent, "full agent")
    test_serialization(search_agent.name, "agent.name")
    test_serialization(search_agent.description, "agent.description")

    if hasattr(search_agent, "state_schema"):
        test_serialization(search_agent.state_schema, "agent.state_schema")

    if hasattr(search_agent, "input_schema"):
        test_serialization(search_agent.input_schema, "agent.input_schema")

    if hasattr(search_agent, "output_schema"):
        test_serialization(search_agent.output_schema, "agent.output_schema")

    test_serialization(search_agent.engine, "agent.engine")
    test_serialization(search_agent.engine.name, "agent.engine.name")

    if hasattr(search_agent.engine, "tools"):
        test_serialization(search_agent.engine.tools, "agent.engine.tools")
        if search_agent.engine.tools:
            test_serialization(search_agent.engine.tools[0], "first tool")
            tool = search_agent.engine.tools[0]

            # Test tool components
            if hasattr(tool, "args_schema"):
                test_serialization(tool.args_schema, "tool.args_schema")

    agent_info = AgentInfo(
        agent=search_agent,
        name="search_agent",
        description="Web search specialist",
        active=True,
    )

    test_serialization(agent_info, "AgentInfo")
    test_serialization(agent_info.name, "AgentInfo.name")
    test_serialization(agent_info.description, "AgentInfo.description")
    test_serialization(agent_info.active, "AgentInfo.active")
    test_serialization(agent_info.agent, "AgentInfo.agent")

    try:
        agent_dict = search_agent.model_dump()
        test_serialization(agent_dict, "agent.model_dump()")
    except Exception as e:
        pass")

    try:
        agent_info_dict = agent_info.model_dump()
        test_serialization(agent_info_dict, "agent_info.model_dump()")
    except Exception as e:
        pass")


if __name__ == "__main__":
    analyze_agent_serialization()
