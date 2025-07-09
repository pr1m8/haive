"""
Simple test to verify SchemaComposer fixes work.
"""

from rich.console import Console

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.schema.schema_composer import SchemaComposer

console = Console()


def test_schema_composer_diagnostics():
    """Diagnostic test to see what's happening with field extraction."""
    console.print(
        "\n[bold cyan]Diagnosing Schema Composer Field Extraction...[/bold cyan]"
    )

    # Create engines
    llm_engine = AugLLMConfig(name="test_llm", model="gpt-4")
    retriever_engine = BaseRetrieverConfig(
        name="test_retriever", retriever_type="VectorStoreRetriever", k=5
    )

    # Step 1: Check engine field definitions
    console.print("\n[bold yellow]Step 1: Engine Field Definitions[/bold yellow]")

    # Check LLM engine
    console.print("\n[green]LLM Engine:[/green]")
    if hasattr(llm_engine, "get_input_fields"):
        input_fields = llm_engine.get_input_fields()
        console.print("  Input fields:")
        for field_name, (field_type, field_info) in input_fields.items():
            console.print(f"    {field_name}: {field_type}")

    if hasattr(llm_engine, "get_output_fields"):
        output_fields = llm_engine.get_output_fields()
        console.print("  Output fields:")
        for field_name, (field_type, field_info) in output_fields.items():
            console.print(f"    {field_name}: {field_type}")

    # Check Retriever engine
    console.print("\n[green]Retriever Engine:[/green]")
    if hasattr(retriever_engine, "get_input_fields"):
        input_fields = retriever_engine.get_input_fields()
        console.print("  Input fields:")
        for field_name, (field_type, field_info) in input_fields.items():
            console.print(f"    {field_name}: {field_type}")

    if hasattr(retriever_engine, "get_output_fields"):
        output_fields = retriever_engine.get_output_fields()
        console.print("  Output fields:")
        for field_name, (field_type, field_info) in output_fields.items():
            console.print(f"    {field_name}: {field_type}")

    # Step 2: Create composer and extract fields
    console.print(
        "\n[bold yellow]Step 2: Create Composer and Extract Fields[/bold yellow]"
    )

    composer = SchemaComposer(name="SimpleState")
    composer.add_fields_from_components([llm_engine, retriever_engine])

    # Display extracted fields
    console.print("\n[green]Extracted Fields:[/green]")
    for field_name, field_def in composer.fields.items():
        console.print(f"  {field_name}: {field_def.field_type}")
        console.print(f"    Input for: {field_def.input_for}")
        console.print(f"    Output from: {field_def.output_from}")
        console.print(f"    Default: {field_def.default}")
        console.print(f"    Default factory: {field_def.default_factory}")

    # Step 3: Create schema and inspect fields
    console.print(
        "\n[bold yellow]Step 3: Create Schema and Inspect Fields[/bold yellow]"
    )

    schema = composer.build(create_io_schemas=False)

    console.print("\n[green]Schema Model Fields:[/green]")
    for field_name, field_info in schema.model_fields.items():
        console.print(f"  {field_name}: {field_info.annotation}")
        if hasattr(field_info, "default"):
            console.print(f"    Default: {field_info.default}")
        if hasattr(field_info, "is_required"):
            console.print(f"    Required: {field_info.is_required()}")

    # Step 4: Test instance creation with different data
    console.print("\n[bold yellow]Step 4: Test Instance Creation[/bold yellow]")

    # Try minimal instance creation
    try:
        minimal_instance = schema(messages=[HumanMessage(content="Test")])
        console.print("[green]✓ Minimal instance created![/green]")
        console.print(f"  Has 'query': {hasattr(minimal_instance, 'query')}")
        console.print(f"  Has 'content': {hasattr(minimal_instance, 'content')}")
    except Exception as e:
        console.print(f"[red]✗ Minimal instance failed: {e}[/red]")

    # Try with query field
    try:
        full_instance = schema(
            messages=[HumanMessage(content="Test")], query="Test query"
        )
        console.print("[green]✓ Full instance created![/green]")
        console.print(f"  Has 'query': {hasattr(full_instance, 'query')}")
        console.print(f"  Query value: {getattr(full_instance, 'query', 'N/A')}")
        console.print(f"  Has 'content': {hasattr(full_instance, 'content')}")
    except Exception as e:
        console.print(f"[red]✗ Full instance failed: {e}[/red]")


if __name__ == "__main__":
    test_schema_composer_diagnostics()
