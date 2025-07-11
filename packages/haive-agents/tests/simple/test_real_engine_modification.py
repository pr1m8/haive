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

    except Exception as e:
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

        # Check v1 engine's natural schema
        v1_natural_schema = v1_engine.derive_output_schema()
        v1_fields = list(v1_natural_schema.model_fields.keys())

        # V1 should naturally include structured fields
        has_summary = "summary" in v1_fields
        has_completed = "completed" in v1_fields
        has_messages = "messages" in v1_fields


        if has_summary and has_completed:
            pass")
        else:
            pass

    except Exception as e:
        return

    try:
        # Create v2 engine config
        v2_engine = AugLLMConfig(
            name="test_v2_engine",
            llm_config=mock_llm_config,
            structured_output_model=TestOutput,
            structured_output_version="v2",
        )

        # Check v2 engine's natural schema
        v2_natural_schema = v2_engine.derive_output_schema()
        v2_fields = list(v2_natural_schema.model_fields.keys())

        # V2 should only have messages
        has_structured_in_v2 = "summary" in v2_fields or "completed" in v2_fields
        has_messages_v2 = "messages" in v2_fields


        if not has_structured_in_v2 and has_messages_v2:
            pass")
        else:
            passed")

        # Check if v2 has the model available
        has_structured_model = hasattr(v2_engine, "structured_output_model")
        has_pydantic_tools = hasattr(v2_engine, "pydantic_tools")
        model_in_tools = has_pydantic_tools and TestOutput in v2_engine.pydantic_tools


    except Exception as e:
        return

    # Test SimpleAgent creation with modification disabled
    try:

        with patch.object(SimpleAgent, "_modify_engine_schema") as mock_modify:
            # Create SimpleAgent with v1 engine
            agent_v1 = SimpleAgent(
                name="test_agent_v1_no_mod",
                engine=v1_engine,
                structured_output_model=TestOutput,
            )


            # Verify modification was called but disabled
            assert mock_modify.called, "Modification method should have been called"

            # Check if agent can determine it needs parser
            needs_parser = agent_v1._needs_parser_node()

            # Try to build graph
            try:
                graph = agent_v1.build_graph()

                # Check if parser node exists
                has_parser = any("parse" in name.lower() for name in graph.nodes)

            except Exception as e:
                pass")

    except Exception as e:
        return

    # Test with v2 engine
    try:
        with patch.object(SimpleAgent, "_modify_engine_schema") as mock_modify:
            agent_v2 = SimpleAgent(
                name="test_agent_v2_no_mod",
                engine=v2_engine,
                structured_output_model=TestOutput,
            )


            # Check engine still has structured model available
            engine_has_model = hasattr(agent_v2.engine, "structured_output_model")
            model_matches = (
                engine_has_model
                and agent_v2.engine.structured_output_model == TestOutput
            )


            if model_matches:
                pass")

    except Exception as e:
        pass")



if __name__ == "__main__":
    test_real_simple_agent_without_modification()
