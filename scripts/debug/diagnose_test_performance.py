#!/usr/bin/env python3
"""Diagnostic script to identify why tests are running slowly.

This script checks common issues that cause slow test execution:
- Missing API keys
- Configuration problems
- Import issues
- Environment setup
"""

import os
import sys
import time
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages/haive-core/src"))
sys.path.insert(
    0, str(Path(__file__).parent.parent.parent / "packages/haive-agents/src")
)


def check_environment():
    """Check environment configuration."""

    # Check Python version

    # Check environment variables
    env_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "AZURE_OPENAI_API_KEY",
        "LANGCHAIN_TRACING_V2",
        "LANGCHAIN_VERBOSE",
        "HAIVE_DEBUG",
    ]

    for var in env_vars:
        value = os.environ.get(var, "Not Set")
        if "API_KEY" in var and value != "Not Set":
            value = f"{value[:8]}..." if len(value) > 8 else "***"


def check_imports():
    """Check if all required modules can be imported."""

    imports_to_test = [
        ("haive.core.engine.aug_llm", "AugLLMConfig"),
        ("haive.agents.simple.agent_v3", "SimpleAgentV3"),
        ("haive.agents.multi.enhanced_multi_agent_v4", "EnhancedMultiAgentV4"),
        ("haive.core.utils.debugkit", "debugkit"),
        ("langchain_core.messages", "HumanMessage"),
        ("pydantic", "BaseModel"),
    ]

    for module_name, class_name in imports_to_test:
        try:
            start = time.time()
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            duration = time.time() - start
        except Exception as e:
            pass")


def test_simple_agent():
    """Test creating a simple agent quickly."""

    try:
        from haive.agents.simple.agent_v3 import SimpleAgentV3
        from haive.core.engine.aug_llm import AugLLMConfig

        start = time.time()
        config = AugLLMConfig(
            temperature=0.1, max_tokens=10, timeout=5  # Short timeout
        )
        config_time = time.time() - start

        start = time.time()
        agent = SimpleAgentV3(
            name="diagnostic_agent",
            engine=config,
            system_message="You are a test agent.",
        )
        agent_time = time.time() - start

        # Don't actually run it - just test creation

    except Exception as e:
        import traceback

        traceback.print_exc()


def test_multi_agent_creation():
    """Test creating multi-agent without execution."""

    try:
        from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
        from haive.agents.simple.agent_v3 import SimpleAgentV3
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create config
        config = AugLLMConfig(temperature=0.1, max_tokens=10, timeout=5)

        # Create agents
        start = time.time()
        agents = [
            SimpleAgentV3(name="agent1", engine=config),
            SimpleAgentV3(name="agent2", engine=config),
        ]
        agents_time = time.time() - start

        # Create multi-agent
        start = time.time()
        multi = EnhancedMultiAgentV4(
            name="diagnostic_multi", agents=agents, execution_mode="sequential"
        )
        multi_time = time.time() - start


    except Exception as e:
        import traceback

        traceback.print_exc()


def test_graph_compilation():
    """Test graph compilation timing."""

    try:
        from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
        from haive.agents.simple.agent_v3 import SimpleAgentV3
        from haive.core.engine.aug_llm import AugLLMConfig

        # Quick setup
        config = AugLLMConfig(temperature=0.1, max_tokens=10, timeout=5)
        agents = [
            SimpleAgentV3(name="agent1", engine=config),
            SimpleAgentV3(name="agent2", engine=config),
        ]
        multi = EnhancedMultiAgentV4(
            name="compilation_test", agents=agents, execution_mode="sequential"
        )

        # Test compilation
        start = time.time()
        compiled = multi.compile()
        compile_time = time.time() - start


        # This is often where it hangs - if compilation takes >5s, that's the issue
        if compile_time > 2.0:
            pass

    except Exception as e:
        import traceback

        traceback.print_exc()


def check_debugkit():
    """Check if debugkit is available and working."""

    try:
        from haive.core.utils.debugkit import debugkit


        # Test basic functionality
        debugkit.ice("Debugkit test", value=42)

        with debugkit.log_context("test"):
            debugkit.log.info("Test message")

    except Exception as e:


def main():
    """Run all diagnostics."""

    start_time = time.time()

    # Run diagnostics
    check_environment()
    check_imports()
    test_simple_agent()
    test_multi_agent_creation()
    test_graph_compilation()
    check_debugkit()

    total_time = time.time() - start_time





if __name__ == "__main__":
    main()
