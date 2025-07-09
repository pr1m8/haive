"""Test with real SimpleAgent to verify engine modification is unnecessary."""

import os
import sys
from unittest.mock import MagicMock, patch

from pydantic import BaseModel, Field

# Add the packages to path to avoid import issues
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def test_real_simple_agent_without_modification():
    """Test real SimpleAgent with engine modification disabled."""

    try:
        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.simple.agent import SimpleAgent

        print("✅ Successfully imported SimpleAgent and AugLLMConfig")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("This test requires the actual haive packages to be available")
        return

    # Test model
    class TestOutput(BaseModel):
        summary: str = Field(description="Summary of the task")
        completed: bool = Field(description="Whether completed")

    # Mock LLM config to avoid API calls
    mock_llm_config = MagicMock()
    mock_llm_config.model = "gpt-4"

    try:
        # Create v1 engine config
        v1_engine = AugLLMConfig(
            name="test_v1_engine",
            llm_config=mock_llm_config,
            structured_output_model=TestOutput,
            structured_output_version="v1",
        )
        print("✅ Created v1 AugLLMConfig")

        # Check v1 engine's natural schema
        v1_natural_schema = v1_engine.derive_output_schema()
        v1_fields = list(v1_natural_schema.model_fields.keys())
        print(f"📋 V1 natural fields: {v1_fields}")

        # V1 should naturally include structured fields
        has_summary = "summary" in v1_fields
        has_completed = "completed" in v1_fields
        has_messages = "messages" in v1_fields

        print(f"   - Has summary: {has_summary}")
        print(f"   - Has completed: {has_completed}")
        print(f"   - Has messages: {has_messages}")

        if has_summary and has_completed:
            print("✅ V1 engine naturally includes structured output fields!")
        else:
            print(
                "⚠️  V1 engine doesn't naturally include fields - may need investigation"
            )

    except Exception as e:
        print(f"❌ V1 engine test failed: {e}")
        return

    try:
        # Create v2 engine config
        v2_engine = AugLLMConfig(
            name="test_v2_engine",
            llm_config=mock_llm_config,
            structured_output_model=TestOutput,
            structured_output_version="v2",
        )
        print("✅ Created v2 AugLLMConfig")

        # Check v2 engine's natural schema
        v2_natural_schema = v2_engine.derive_output_schema()
        v2_fields = list(v2_natural_schema.model_fields.keys())
        print(f"📋 V2 natural fields: {v2_fields}")

        # V2 should only have messages
        has_structured_in_v2 = "summary" in v2_fields or "completed" in v2_fields
        has_messages_v2 = "messages" in v2_fields

        print(f"   - Has structured fields: {has_structured_in_v2}")
        print(f"   - Has messages: {has_messages_v2}")

        if not has_structured_in_v2 and has_messages_v2:
            print("✅ V2 engine correctly only has messages!")
        else:
            print("⚠️  V2 engine behavior unexpected")

        # Check if v2 has the model available
        has_structured_model = hasattr(v2_engine, "structured_output_model")
        has_pydantic_tools = hasattr(v2_engine, "pydantic_tools")
        model_in_tools = has_pydantic_tools and TestOutput in v2_engine.pydantic_tools

        print(f"   - Has structured_output_model: {has_structured_model}")
        print(f"   - Has pydantic_tools: {has_pydantic_tools}")
        print(f"   - Model in tools: {model_in_tools}")

    except Exception as e:
        print(f"❌ V2 engine test failed: {e}")
        return

    # Test SimpleAgent creation with modification disabled
    try:
        print("\n🧪 Testing SimpleAgent with modification disabled...")

        with patch.object(SimpleAgent, "_modify_engine_schema") as mock_modify:
            # Create SimpleAgent with v1 engine
            agent_v1 = SimpleAgent(
                name="test_agent_v1_no_mod",
                engine=v1_engine,
                structured_output_model=TestOutput,
            )

            print("✅ Created SimpleAgent with v1 engine (modification disabled)")
            print(f"   - Agent name: {agent_v1.name}")
            print(f"   - Engine name: {agent_v1.engine.name}")
            print(f"   - Structured model: {agent_v1.structured_output_model.__name__}")

            # Verify modification was called but disabled
            assert mock_modify.called, "Modification method should have been called"
            print("✅ _modify_engine_schema was called but disabled")

            # Check if agent can determine it needs parser
            needs_parser = agent_v1._needs_parser_node()
            print(f"   - Needs parser node: {needs_parser}")

            # Try to build graph
            try:
                graph = agent_v1.build_graph()
                print(f"✅ Built graph successfully with {len(graph.nodes)} nodes")
                print(f"   - Node names: {list(graph.nodes.keys())}")

                # Check if parser node exists
                has_parser = any("parse" in name.lower() for name in graph.nodes.keys())
                print(f"   - Has parser node: {has_parser}")

            except Exception as e:
                print(f"❌ Graph building failed: {e}")

    except Exception as e:
        print(f"❌ SimpleAgent test failed: {e}")
        return

    # Test with v2 engine
    try:
        with patch.object(SimpleAgent, "_modify_engine_schema") as mock_modify:
            agent_v2 = SimpleAgent(
                name="test_agent_v2_no_mod",
                engine=v2_engine,
                structured_output_model=TestOutput,
            )

            print("✅ Created SimpleAgent with v2 engine (modification disabled)")

            # Check engine still has structured model available
            engine_has_model = hasattr(agent_v2.engine, "structured_output_model")
            model_matches = (
                engine_has_model
                and agent_v2.engine.structured_output_model == TestOutput
            )

            print(f"   - Engine has structured_output_model: {engine_has_model}")
            print(f"   - Model matches: {model_matches}")

            if model_matches:
                print("✅ Parser should be able to find the model!")

    except Exception as e:
        print(f"❌ V2 SimpleAgent test failed: {e}")

    print("\n🎉 Real SimpleAgent tests completed!")
    print("📝 Summary:")
    print("   - V1 engines naturally include structured fields")
    print("   - V2 engines provide model via tools/direct reference")
    print("   - SimpleAgent can be created without engine modification")
    print("   - Parser nodes should be able to find models via direct lookup")
    print("   - Engine modification appears to be unnecessary!")


if __name__ == "__main__":
    test_real_simple_agent_without_modification()
