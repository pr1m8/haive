#!/usr/bin/env python3
"""REPRODUCE THE EXACT ERROR.
=========================

User said the error message is: "Failed to convert BaseGraph to LangGraph: name 'AugLLMConfig' is not defined"
This suggests it's happening during graph compilation/conversion, not during agent creation.
"""

import logging
import os
import sys


# Suppress the noisy supabase logging
logging.getLogger("hpack").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

from rich.console import Console


console = Console()


def test_exact_reproduction():
    """Try to reproduce the exact error from the user's message."""
    try:
        console.print("[bold blue]Step 1: Import modules[/bold blue]")
        from haive.agents.simple.agent_v2 import SimpleAgentV2
        from haive.core.engine.aug_llm import AugLLMConfig

        console.print("✅ Imports successful")

        console.print("[bold blue]Step 2: Create agent[/bold blue]")
        engine = AugLLMConfig(name="test_engine")
        agent = SimpleAgentV2(name="test_agent", engine=engine)
        console.print("✅ Agent created")

        console.print("[bold blue]Step 3: Build graph[/bold blue]")
        graph = agent.build_graph()
        console.print("✅ Graph built")

        console.print(
            "[bold blue]Step 4: Try to compile graph (LIKELY ERROR POINT)[/bold blue]"
        )
        # This is where "Failed to convert BaseGraph to LangGraph" likely happens
        graph.compile()
        console.print("✅ Graph compiled")

        console.print("[bold blue]Step 5: Create runnable[/bold blue]")
        agent.create_runnable()
        console.print("✅ Runnable created")

        console.print(
            "[bold blue]Step 6: Try query input (where user expects it to work)[/bold blue]"
        )
        agent.invoke({"query": "test message"})
        console.print("✅ Query input worked!")

    except Exception as e:
        error_msg = str(e)
        console.print(f"[bold red]ERROR: {error_msg}[/bold red]")

        if "AugLLMConfig" in error_msg and "not defined" in error_msg:
            console.print("[bold red]🎯 FOUND THE AugLLMConfig ERROR![/bold red]")

            # Print the full traceback to see where it's happening
            import traceback

            console.print("\n[bold yellow]FULL TRACEBACK:[/bold yellow]")
            traceback.print_exc()

            # Check specific frames for the error location
            tb = sys.exc_info()[2]
            frame = tb.tb_frame
            while frame:
                filename = frame.f_code.co_filename
                lineno = frame.f_lineno
                function = frame.f_code.co_name

                if any(
                    keyword in filename
                    for keyword in ["state_schema", "agent", "schema_composer"]
                ):
                    console.print(
                        f"[yellow]Frame in suspect file: {filename}:{lineno} in {function}[/yellow]"
                    )

                frame = frame.f_back

        else:
            console.print(f"[red]Different error: {error_msg}[/red]")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    console.print(
        "[bold magenta]REPRODUCING: 'Failed to convert BaseGraph to LangGraph: name AugLLMConfig is not defined'[/bold magenta]"
    )
    test_exact_reproduction()
