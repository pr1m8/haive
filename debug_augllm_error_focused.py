#!/usr/bin/env python3
"""FOCUSED DEBUG: Find AugLLMConfig not defined error.
==================================================

USER SAYS: The error is in state_schema, agent.base, or schema_composer
Need to add PROPER logging to find exactly where AugLLMConfig is not defined.
"""

import logging
import sys

from rich.console import Console
from rich.logging import RichHandler

console = Console()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s:%(lineno)d - %(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)


def add_debug_to_modules():
    """Add debug logging to the modules where the error likely occurs."""
    # 1. STATE SCHEMA - Add logging to find AugLLMConfig issues
    try:
        console.print("[bold blue]Adding debug to state_schema.py...[/bold blue]")
        import haive.core.schema.state_schema as state_schema_mod

        # Monkey patch key functions to add logging
        original_derive_input_schema = state_schema_mod.StateSchema.derive_input_schema

        def debug_derive_input_schema(self, *args, **kwargs):
            console.print(
                f"[yellow]StateSchema.derive_input_schema called on {type(self).__name__}[/yellow]"
            )
            try:
                # Check for AugLLMConfig in globals
                import inspect

                frame = inspect.currentframe()
                while frame:
                    if "AugLLMConfig" in frame.f_globals:
                        console.print(
                            f"[green]Found AugLLMConfig in frame: {frame.f_code.co_filename}:{frame.f_lineno}[/green]"
                        )
                    frame = frame.f_back

                result = original_derive_input_schema(self, *args, **kwargs)
                console.print(
                    f"[green]derive_input_schema succeeded, result: {result.__name__}[/green]"
                )
                return result
            except NameError as e:
                if "AugLLMConfig" in str(e):
                    console.print(
                        f"[bold red]FOUND AugLLMConfig NameError in derive_input_schema: {e}[/bold red]"
                    )
                    import traceback

                    traceback.print_exc()
                raise
            except Exception as e:
                console.print(f"[red]derive_input_schema error: {e}[/red]")
                raise

        state_schema_mod.StateSchema.derive_input_schema = debug_derive_input_schema
        console.print("✅ Added debug to StateSchema.derive_input_schema")

    except Exception as e:
        console.print(f"[red]Failed to add debug to state_schema: {e}[/red]")

    # 2. SCHEMA COMPOSER - Add logging
    try:
        console.print("[bold blue]Adding debug to schema_composer.py...[/bold blue]")
        import haive.core.schema.schema_composer as composer_mod

        original_build = composer_mod.SchemaComposer.build

        def debug_build(self, *args, **kwargs):
            console.print("[yellow]SchemaComposer.build called[/yellow]")
            try:
                # Check for AugLLMConfig references
                console.print(f"Composer engines: {getattr(self, 'engines', 'None')}")
                console.print(
                    f"Composer input_fields: {getattr(self, 'input_fields', 'None')}"
                )

                result = original_build(self, *args, **kwargs)
                console.print("[green]SchemaComposer.build succeeded[/green]")
                return result
            except NameError as e:
                if "AugLLMConfig" in str(e):
                    console.print(
                        f"[bold red]FOUND AugLLMConfig NameError in SchemaComposer.build: {e}[/bold red]"
                    )
                    import traceback

                    traceback.print_exc()
                raise
            except Exception as e:
                console.print(f"[red]SchemaComposer.build error: {e}[/red]")
                raise

        composer_mod.SchemaComposer.build = debug_build
        console.print("✅ Added debug to SchemaComposer.build")

    except Exception as e:
        console.print(f"[red]Failed to add debug to schema_composer: {e}[/red]")

    # 3. AGENT BASE - Add logging
    try:
        console.print("[bold blue]Adding debug to agent.py base...[/bold blue]")
        import haive.agents.base.agent as agent_mod

        original_model_post_init = agent_mod.Agent.model_post_init

        def debug_model_post_init(self, __context):
            console.print(
                f"[yellow]Agent.model_post_init called on {type(self).__name__}[/yellow]"
            )
            try:
                result = original_model_post_init(self, __context)
                console.print("[green]Agent.model_post_init succeeded[/green]")
                return result
            except NameError as e:
                if "AugLLMConfig" in str(e):
                    console.print(
                        f"[bold red]FOUND AugLLMConfig NameError in Agent.model_post_init: {e}[/bold red]"
                    )
                    import traceback

                    traceback.print_exc()
                raise
            except Exception as e:
                console.print(f"[red]Agent.model_post_init error: {e}[/red]")
                raise

        agent_mod.Agent.model_post_init = debug_model_post_init
        console.print("✅ Added debug to Agent.model_post_init")

    except Exception as e:
        console.print(f"[red]Failed to add debug to agent base: {e}[/red]")


def test_simple_agent_creation():
    """Test SimpleAgent V2 creation with debugging."""
    console.print("[bold green]Testing SimpleAgent V2 creation...[/bold green]")

    try:
        from haive.agents.simple.agent_v2 import SimpleAgentV2
        from haive.core.engine.aug_llm import AugLLMConfig

        console.print("✅ Imports successful")

        # Create engine
        engine = AugLLMConfig(name="debug_engine")
        console.print("✅ Engine created")

        # Create agent - this should trigger the debug logging
        agent = SimpleAgentV2(name="debug_agent", engine=engine)
        console.print("✅ Agent created")

        # Try to test the query input that should work
        console.print("[yellow]Testing query input (should work)...[/yellow]")
        try:
            agent.invoke({"query": "test"})
            console.print("✅ Query input worked!")
        except Exception as e:
            console.print(f"[red]Query input failed: {e}[/red]")
            if "AugLLMConfig" in str(e):
                console.print("[bold red]THIS IS THE AugLLMConfig ERROR![/bold red]")
                import traceback

                traceback.print_exc()

    except Exception as e:
        console.print(f"[red]Creation failed: {e}[/red]")
        if "AugLLMConfig" in str(e):
            console.print("[bold red]AugLLMConfig ERROR DURING CREATION![/bold red]")
            import traceback

            traceback.print_exc()


def main():
    """Main debug function."""
    console.print(
        "[bold magenta]FOCUSED DEBUG: Finding AugLLMConfig not defined error[/bold magenta]"
    )
    console.print(
        "[bold yellow]USER SAID: Check state_schema, agent.base, schema_composer[/bold yellow]"
    )

    # First add debugging to the suspect modules
    add_debug_to_modules()

    # Then test agent creation
    test_simple_agent_creation()


if __name__ == "__main__":
    main()
