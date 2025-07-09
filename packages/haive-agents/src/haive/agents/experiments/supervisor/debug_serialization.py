"""Debug what exactly is not serializable in the agent objects."""

import ormsgpack
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.react.agent import ReactAgent


def test_serialization(obj, name="object"):
    """Test if an object can be serialized with msgpack."""
    try:
        ormsgpack.packb(obj)
        print(f"✅ {name}: SERIALIZABLE")
        return True
    except Exception as e:
        print(f"❌ {name}: NOT SERIALIZABLE - {e}")
        return False


def analyze_agent_serialization():
    """Analyze what parts of an agent are not serializable."""
    print("🔍 Analyzing agent serialization issues...\n")

    # Create a ReactAgent
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    print("1. Testing basic types:")
    test_serialization("simple string", "string")
    test_serialization(123, "int")
    test_serialization({"key": "value"}, "dict")
    test_serialization(["item"], "list")

    print("\n2. Testing agent components:")
    test_serialization(search_agent, "full agent")
    test_serialization(search_agent.name, "agent.name")
    test_serialization(search_agent.description, "agent.description")

    print("\n3. Testing agent schemas:")
    if hasattr(search_agent, "state_schema"):
        test_serialization(search_agent.state_schema, "agent.state_schema")
        print(f"   state_schema type: {type(search_agent.state_schema)}")
        print(f"   state_schema __class__: {search_agent.state_schema.__class__}")
        print(f"   state_schema metaclass: {type(search_agent.state_schema.__class__)}")

    if hasattr(search_agent, "input_schema"):
        test_serialization(search_agent.input_schema, "agent.input_schema")

    if hasattr(search_agent, "output_schema"):
        test_serialization(search_agent.output_schema, "agent.output_schema")

    print("\n4. Testing engine:")
    test_serialization(search_agent.engine, "agent.engine")
    test_serialization(search_agent.engine.name, "agent.engine.name")

    print("\n5. Testing engine components:")
    if hasattr(search_agent.engine, "tools"):
        test_serialization(search_agent.engine.tools, "agent.engine.tools")
        if search_agent.engine.tools:
            test_serialization(search_agent.engine.tools[0], "first tool")
            tool = search_agent.engine.tools[0]
            print(f"   tool type: {type(tool)}")
            print(f"   tool __class__: {tool.__class__}")
            print(f"   tool metaclass: {type(tool.__class__)}")

            # Test tool components
            if hasattr(tool, "args_schema"):
                test_serialization(tool.args_schema, "tool.args_schema")
                print(f"   args_schema type: {type(tool.args_schema)}")
                print(f"   args_schema metaclass: {type(tool.args_schema.__class__)}")

    print("\n6. Testing AgentInfo:")
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

    print("\n7. Testing state dict representation:")
    try:
        agent_dict = search_agent.model_dump()
        test_serialization(agent_dict, "agent.model_dump()")
    except Exception as e:
        print(f"❌ agent.model_dump() failed: {e}")

    try:
        agent_info_dict = agent_info.model_dump()
        test_serialization(agent_info_dict, "agent_info.model_dump()")
    except Exception as e:
        print(f"❌ agent_info.model_dump() failed: {e}")


if __name__ == "__main__":
    analyze_agent_serialization()
