#!/usr/bin/env python3
"""EXACT REPRODUCTION OF UNTITLED83 NOTEBOOK.
==========================================

Converting the notebook exactly to catch the real error with comprehensive debugging.
"""

import logging
import sys
import traceback

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

# Install rich tracebacks
install()

# Set up rich logging with MAXIMUM detail
console = Console()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s:%(lineno)d - %(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True, markup=True)],
)


def add_comprehensive_debugging():
    """Add debugging to ALL critical modules."""
    console.print("[bold blue]Adding comprehensive debugging...[/bold blue]")

    # 1. STATE SCHEMA DEBUGGING
    try:
        import haive.core.schema.state_schema as state_schema_mod

        original_derive = state_schema_mod.StateSchema.derive_input_schema

        def debug_derive_input_schema(self, *args, **kwargs):
            console.print(
                f"[yellow]🔍 derive_input_schema called on {type(self).__name__}[/yellow]"
            )
            try:
                result = original_derive(self, *args, **kwargs)
                console.print(
                    f"[green]✅ derive_input_schema success: {result.__name__}[/green]"
                )
                return result
            except Exception as e:
                console.print(
                    f"[bold red]💥 derive_input_schema FAILED: {e}[/bold red]"
                )
                if "AugLLMConfig" in str(e):
                    console.print(
                        "[bold red]🎯 FOUND AugLLMConfig ERROR in derive_input_schema![/bold red]"d]"
                    )
                raise

        state_schema_mod.StateSchema.derive_input_schema = debug_derive_input_schema
        console.print("✅ Added debugging to StateSchema.derive_input_schema")

    except Exception as e:
        console.print(f"[red]Failed to debug state_schema: {e}[/red]")

    # 2. SCHEMA COMPOSER DEBUGGING
    try:
        import haive.core.schema.schema_composer as composer_mod

        original_build = composer_mod.SchemaComposer.build

        def debug_build(self, *args, **kwargs):
            console.print("[yellow]🔍 SchemaComposer.build called[/yellow]"w]")
            try:
                result = original_build(self, *args, **kwargs)
                console.print("[green]✅ SchemaComposer.build success[/green]"]")
                return result
            except Exception as e:
                console.print(
                    f"[bold red]💥 SchemaComposer.build FAILED: {e}[/bold red]"
                )
                if "AugLLMConfig" in str(e):
                    console.print(
                        "[bold red]🎯 FOUND AugLLMConfig ERROR in SchemaComposer![/bold red]"d]"
                    )
                raise

        composer_mod.SchemaComposer.build = debug_build
        console.print("✅ Added debugging to SchemaComposer.build")

    except Exception as e:
        console.print(f"[red]Failed to debug schema_composer: {e}[/red]")

    # 3. AGENT BASE DEBUGGING
    try:
        import haive.agents.base.agent as agent_mod

        original_compile = agent_mod.Agent.compile

        def debug_compile(self, *args, **kwargs):
            console.print(
                f"[yellow]🔍 Agent.compile called on {type(self).__name__}[/yellow]"
            )
            try:
                result = original_compile(self, *args, **kwargs)
                console.print("[green]✅ Agent.compile success[/green]"]")
                return result
            except Exception as e:
                console.print(f"[bold red]💥 Agent.compile FAILED: {e}[/bold red]")
                if "AugLLMConfig" in str(e):
                    console.print(
                        "[bold red]🎯 FOUND AugLLMConfig ERROR in Agent.compile![/bold red]"d]"
                    )
                raise

        agent_mod.Agent.compile = debug_compile
        console.print("✅ Added debugging to Agent.compile")

    except Exception as e:
        console.print(f"[red]Failed to debug agent base: {e}[/red]")

    # 4. GRAPH CONVERSION DEBUGGING (CRITICAL!)
    try:
        import haive.core.graph.base as graph_mod

        original_to_langgraph = graph_mod.BaseGraph.to_langgraph

        def debug_to_langgraph(self, *args, **kwargs):
            console.print("[yellow]🔍 BaseGraph.to_langgraph called[/yellow]"w]")
            try:
                result = original_to_langgraph(self, *args, **kwargs)
                console.print("[green]✅ BaseGraph.to_langgraph success[/green]"]")
                return result
            except Exception as e:
                console.print(
                    f"[bold red]💥 BaseGraph.to_langgraph FAILED: {e}[/bold red]"
                )
                if "AugLLMConfig" in str(e):
                    console.print(
                        "[bold red]🎯 FOUND AugLLMConfig ERROR in BaseGraph.to_langgraph![/bold red]"d]"
                    )
                    console.print(
                        "[bold red]THIS IS LIKELY THE MAIN ERROR LOCATION![/bold red]"
                    )
                raise

        graph_mod.BaseGraph.to_langgraph = debug_to_langgraph
        console.print("✅ Added debugging to BaseGraph.to_langgraph")

    except Exception as e:
        console.print(f"[red]Failed to debug graph base: {e}[/red]")


def test_notebook_exact_reproduction():
    """Test the exact notebook code step by step."""
    console.print(
        "[bold green]🧪 TESTING NOTEBOOK CODE EXACT REPRODUCTION[/bold green]"
    )

    try:
        # Cell 1: Import types

        console.print("✅ Cell 1: Basic imports successful")

        # Cell 2: Chat prompt template (the complex one from notebook)
        from langchain_core.prompts import ChatPromptTemplate

        RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert query optimization specialist for RAG systems...""",
                ),
                (
                    "human",
                    """Analyze and refine the following user query: {query}

**Context (if provided):** {context}

Focus on improvements that will lead to better document retrieval.""",
                ),
            ]
        ).partial(context="")
        console.print("✅ Cell 2: RAG_QUERY_REFINEMENT prompt created")

        # Cell 3: Pydantic models
        from pydantic import BaseModel, Field

        class QueryRefinementSuggestion(BaseModel):
            refined_query: str = Field(description="The refined/improved query")
            improvement_type: str = Field(description="Type of improvement made")
            rationale: str = Field(description="Why this refinement improves the query")
            expected_benefit: str = Field(
                description="Expected improvement in retrieval"
            )

        class QueryRefinementResponse(BaseModel):
            original_query: str = Field(description="The original user query")
            query_analysis: str = Field(description="Analysis of the original query")
            query_type: str = Field(description="Classification of query type")
            complexity_level: str = Field(description="simple, moderate, or complex")
            refinement_suggestions: list[QueryRefinementSuggestion] = Field(
                description="List of suggestions"
            )
            best_refined_query: str = Field(
                description="The recommended best refined query"
            )
            search_strategy_recommendations: list[str] = Field(
                description="Search strategy recommendations"
            )

        console.print("✅ Cell 3: Pydantic models created")

        # Cell 4: Import SimpleAgentV2 and AugLLMConfig - CRITICAL IMPORTS
        from haive.agents.simple.agent_v2 import SimpleAgentV2
        from haive.core.engine.aug_llm import AugLLMConfig

        console.print("✅ Cell 4: SimpleAgentV2 and AugLLMConfig imported")

        # Cell 5: Agent tester function (exact from notebook)
        def agent_tester(prompt, model, test_prompt):
            agent = SimpleAgentV2(
                engine=AugLLMConfig(
                    prompt_template=prompt,
                    structured_output_model=model,
                    structured_output_version="v2",
                )
            )
            return agent

        console.print("✅ Cell 5: agent_tester function defined")

        # Cell 6: Create the agent (this is where error likely happens)
        console.print(
            "[bold yellow]🔥 EXECUTING CRITICAL CELL 6: Creating agent...[/bold yellow]"
        )
        result = agent_tester(
            RAG_QUERY_REFINEMENT,
            QueryRefinementResponse,
            {"query": "what is the tallest building in france"},
        )
        console.print("✅ Cell 6: Agent created successfully!")

        # Cell 7: Test input schema (this worked in notebook)
        console.print(
            "[bold yellow]🔥 EXECUTING CELL 7: Testing input schema...[/bold yellow]"
        )
        input_schema_fields = result.input_schema(query="hello").model_fields
        console.print(
            f"✅ Cell 7: Input schema fields: {list(input_schema_fields.keys())}"
        )

        # Cell 8: The actual run call (this is where the error REALLY happens)
        def agent_tester_with_run(prompt, model, test_prompt):
            agent = SimpleAgentV2(
                engine=AugLLMConfig(
                    prompt_template=prompt,
                    structured_output_model=model,
                    structured_output_version="v2",
                )
            )
            return agent.run(test_prompt, debug=True)

        console.print(
            "[bold yellow]🔥 EXECUTING CRITICAL CELL 8: Running agent (WHERE ERROR HAPPENS)...[/bold yellow]"
        )
        agent_tester_with_run(
            RAG_QUERY_REFINEMENT,
            QueryRefinementResponse,
            {"query": "what is the tallest building in france"},
        )
        console.print("✅ Cell 8: Agent run successful!")

        console.print(
            "[bold green]🎉 ALL NOTEBOOK CELLS EXECUTED SUCCESSFULLY![/bold green]"
        )

    except Exception as e:
        console.print(f"[bold red]💥 NOTEBOOK EXECUTION FAILED: {e}[/bold red]")
        console.print(f"[bold red]Error type: {type(e).__name__}[/bold red]")

        # Check if this is the AugLLMConfig error
        if "AugLLMConfig" in str(e) and "not defined" in str(e):
            console.print(
                "[bold red]🎯 FOUND THE EXACT ERROR FROM NOTEBOOK![/bold red]"
            )
        elif "abstract class Engine" in str(e):
            console.print(
                "[bold red]🎯 FOUND ABSTRACT ENGINE ERROR (RELATED ISSUE)![/bold red]"
            )

        # Print full traceback with rich formatting
        console.print("\n[bold yellow]FULL TRACEBACK:[/bold yellow]")
        traceback.print_exc()

        # Print stack trace details
        tb = sys.exc_info()[2]
        while tb:
            frame = tb.tb_frame
            filename = frame.f_code.co_filename
            lineno = tb.tb_lineno
            function = frame.f_code.co_name

            # Check for suspect files
            if any(
                keyword in filename
                for keyword in ["state_schema", "agent", "schema_composer", "graph"]
            ):
                console.print(
                    f"[yellow]📍 Suspect frame: {filename}:{lineno} in {function}[/yellow]"
                )

            tb = tb.tb_next

        raise


def main():
    """Main test function with all debugging enabled."""
    console.print(
        "[bold magenta]EXACT NOTEBOOK REPRODUCTION WITH COMPREHENSIVE DEBUG[/bold magenta]"
    )
    console.print(
        "[bold yellow]USER SAID: Fix this issue using state_schema, agent.base, schema_composer debugging[/bold yellow]"
    )

    # Add all debugging first
    add_comprehensive_debugging()

    # Then run the exact notebook reproduction
    test_notebook_exact_reproduction()


if __name__ == "__main__":
    main()
