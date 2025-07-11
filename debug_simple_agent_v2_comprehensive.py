#!/usr/bin/env python3
"""COMPREHENSIVE DEBUG TEST FOR SIMPLE AGENT V2.
============================================

This file recreates the notebook Untitled83 issue with extensive tracing
to find the exact point where 'AugLLMConfig' is not defined.
"""

import logging
import sys
import traceback

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

# Install rich tracebacks
install()

# Set up rich logging
console = Console()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger(__name__)


def trace_step(step_name, func):
    """Trace a step with comprehensive error handling."""
    try:
        console.print(f"\n[bold blue]{'='*60}[/bold blue]")
        console.print(f"[bold green]STEP: {step_name}[/bold green]")
        console.print(f"[bold blue]{'='*60}[/bold blue]")

        result = func()

        console.print(f"[bold green]✅ {step_name} - SUCCESS[/bold green]")
        return result

    except Exception as e:
        console.print(f"[bold red]❌ {step_name} - FAILED[/bold red]")
        console.print(f"[bold red]Error: {e}[/bold red]")
        console.print(f"[bold red]Error type: {type(e).__name__}[/bold red]")

        # Print full traceback
        console.print("\n[bold yellow]FULL TRACEBACK:[/bold yellow]")
        traceback.print_exc()

        # Print locals and globals at error point
        frame = sys.exc_info()[2].tb_frame
        console.print("\n[bold yellow]LOCALS at error:[/bold yellow]")
        for k, v in frame.f_locals.items():
            console.print(f"  {k}: {type(v)} = {str(v)[:100]}")

        console.print("\n[bold yellow]GLOBALS at error (relevant):[/bold yellow]")
        for k, v in frame.f_globals.items():
            if "AugLLM" in k or "Engine" in k or "Agent" in k:
                console.print(f"  {k}: {type(v)} = {str(v)[:100]}")

        raise


def test_imports():
    """Test all imports step by step."""
    console.print("[bold yellow]Testing imports...[/bold yellow]")

    # Test core imports
    from haive.core.engine.aug_llm import AugLLMConfig

    console.print("✅ AugLLMConfig imported successfully")

    from haive.agents.simple.agent_v2 import SimpleAgentV2

    console.print("✅ SimpleAgentV2 imported successfully")

    return AugLLMConfig, SimpleAgentV2


def test_agent_creation(AugLLMConfig, SimpleAgentV2):
    """Test agent creation."""
    console.print("[bold yellow]Testing agent creation...[/bold yellow]")

    # Create engine with CORRECT parameters
    engine = AugLLMConfig(name="debug_engine", temperature=0.7)
    console.print(f"✅ Engine created: {engine.name}")

    # Create agent
    agent = SimpleAgentV2(name="debug_agent", engine=engine)
    console.print(f"✅ Agent created: {agent.name}")
    console.print(f"✅ Agent state schema: {agent.state_schema.__name__}")

    return agent


def test_state_creation(agent):
    """Test state creation."""
    console.print("[bold yellow]Testing state creation...[/bold yellow]")

    # Try to create state directly
    state = agent.state_schema(engine=agent.engine)
    console.print(f"✅ State created: {type(state).__name__}")

    return state


def test_input_schema_derivation(agent):
    """Test input schema derivation."""
    console.print("[bold yellow]Testing input schema derivation...[/bold yellow]")

    input_schema = agent.derive_input_schema()
    console.print(f"✅ Input schema derived: {input_schema.__name__}")

    # Test input schema fields
    console.print(f"Input schema fields: {list(input_schema.model_fields.keys())}")

    return input_schema


def test_graph_building(agent):
    """Test graph building."""
    console.print("[bold yellow]Testing graph building...[/bold yellow]")

    graph = agent.build_graph()
    console.print(f"✅ Graph built: {graph.name}")

    return graph


def test_runnable_creation(agent):
    """Test runnable creation - THIS IS WHERE THE ERROR LIKELY OCCURS."""
    console.print("[bold yellow]Testing runnable creation...[/bold yellow]")

    # This is likely where the error happens
    runnable = agent.create_runnable()
    console.print(f"✅ Runnable created: {type(runnable).__name__}")

    return runnable


def test_agent_execution(agent):
    """Test actual agent execution."""
    console.print("[bold yellow]Testing agent execution...[/bold yellow]")

    # Test with proper input that includes messages
    from langchain_core.messages import HumanMessage

    result = agent.invoke({"messages": [HumanMessage(content="Hello, test message")]})
    console.print("✅ Agent execution successful"l")
    console.print(f"Result type: {type(result)}")

    return result


def main():
    """Main test function."""
    console.print(
        "[bold magenta]STARTING COMPREHENSIVE SIMPLE AGENT V2 DEBUG[/bold magenta]"
    )

    try:
        # Step 1: Test imports
        AugLLMConfig, SimpleAgentV2 = trace_step("Import modules", test_imports)

        # Step 2: Test agent creation
        agent = trace_step(
            "Create agent", lambda: test_agent_creation(AugLLMConfig, SimpleAgentV2)
        )

        # Step 3: Test state creation
        trace_step("Create state", lambda: test_state_creation(agent))

        # Step 4: Test input schema derivation
        trace_step(
            "Derive input schema", lambda: test_input_schema_derivation(agent)
        )

        # Step 5: Test graph building
        trace_step("Build graph", lambda: test_graph_building(agent))

        # Step 6: Test runnable creation (LIKELY ERROR POINT)
        trace_step("Create runnable", lambda: test_runnable_creation(agent))

        # Step 7: Test agent execution
        trace_step("Execute agent", lambda: test_agent_execution(agent))

        console.print("\n[bold green]🎉 ALL TESTS PASSED! 🎉[/bold green]")

    except Exception as e:
        console.print(f"\n[bold red]💥 CRITICAL ERROR: {e}[/bold red]")
        console.print("[bold red]Full error trace printed above[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
