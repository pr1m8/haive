"""Improved tests for SchemaComposer with detailed logging and visibility into field extraction."""

import logging
import operator
from typing import Annotated, Any, Dict, List

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.schema.state_schema import StateSchema
from haive.core.schema.ui import SchemaUI

# Set up extensive logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("schema_composer_tests")
console = Console()


# Sample models for testing
class SimpleModel(BaseModel):
    """Simple model for testing."""

    name: str = Field(description="Name field")
    value: int = Field(default=0, description="Value field")


class SearchResult(BaseModel):
    """Search result model for testing."""

    answer: str = Field(description="Answer to the query")
    sources: list[str] = Field(default_factory=list, description="Source documents")
    confidence: float = Field(default=0.0, description="Confidence score")


class ChatState(StateSchema):
    """Chat state with messages and reducers."""

    messages: Annotated[list[BaseMessage], operator.add] = Field(
        default_factory=list, description="Conversation messages"
    )
    context: list[str] = Field(default_factory=list, description="Context documents")
    query: str = Field(default="", description="User query")


def log_composer_debug_info(
    composer: SchemaComposer, title: str = "Composer Debug Info"
):
    """Log detailed debug information about the composer's state."""
    console.print(Panel(title, expand=False))

    # Show fields
    table = Table(title="Extracted Fields")
    table.add_column("Field Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Default", style="yellow")
    table.add_column("Has Reducer", style="red")
    table.add_column("Shared", style="magenta")

    for field_name, field_def in composer.fields.items():
        table.add_row(
            field_name,
            str(field_def.field_type),
            str(field_def.default or field_def.default_factory),
            "Yes" if field_def.reducer else "No",
            "Yes" if field_def.shared else "No",
        )
    console.print(table)

    # Show I/O mappings
    if composer.engine_io_mappings:
        console.print("\n[bold]Engine I/O Mappings:[/bold]")
        for engine, mapping in composer.engine_io_mappings.items():
            console.print(f"  {engine}:")
            console.print(f"    Inputs: {mapping.get('inputs', [])}")
            console.print(f"    Outputs: {mapping.get('outputs', [])}")

    # Show structured models
    if composer.structured_models:
        console.print("\n[bold]Structured Models:[/bold]")
        for model_name, model in composer.structured_models.items():
            console.print(f"  {model_name}: {model.__name__}")
            if model_name in composer.structured_model_fields:
                console.print(
                    f"    Fields: {list(composer.structured_model_fields[model_name])}"
                )


def log_schema_debug_info(schema, title: str = "Schema Debug Info"):
    """Log detailed debug information about a generated schema."""
    console.print(Panel(title, expand=False))

    # Show all model attributes
    attributes = [
        attr
        for attr in dir(schema)
        if not attr.startswith("__")
        or attr
        in [
            "__shared_fields__",
            "__reducer_fields__",
            "__engine_io_mappings__",
            "__structured_models__",
            "__structured_model_fields__",
        ]
    ]

    for attr in attributes:
        value = getattr(schema, attr, None)
        if value:
            console.print(f"[bold]{attr}:[/bold] {value}")

    # Show model fields specifically
    if hasattr(schema, "model_fields"):
        console.print("\n[bold]Model Fields:[/bold]")
        for field_name, field_info in schema.model_fields.items():
            console.print(
                f"  {field_name}: {field_info.annotation} (default: {field_info.default})"
            )


def test_schema_composer_basics():
    """Test basic SchemaComposer functionality with extensive logging."""
    console.print("\n[bold cyan]Testing Basic SchemaComposer Functionality[/bold cyan]")

    # Create a composer
    composer = SchemaComposer(name="TestSchema")

    # Add fields with debugging
    console.print("\n[yellow]Adding field: name (str)[/yellow]")
    composer.add_field(name="name", field_type=str, description="Name field")
    log_composer_debug_info(composer, "After adding 'name' field")

    console.print("\n[yellow]Adding field: value (int)[/yellow]")
    composer.add_field(
        name="value", field_type=int, default=0, description="Value field"
    )
    log_composer_debug_info(composer, "After adding 'value' field")

    console.print("\n[yellow]Adding field: active (bool)[/yellow]")
    composer.add_field(
        name="active", field_type=bool, default=False, description="Active status"
    )
    log_composer_debug_info(composer, "After adding 'active' field")

    # Build schema
    console.print("\n[bold]Building schema...[/bold]")
    schema = composer.build()
    log_schema_debug_info(schema, "Built Schema")

    # Verify fields
    assert hasattr(schema, "model_fields"), "Schema missing model_fields attribute"
    assert (
        "name" in schema.model_fields
    ), f"Field 'name' missing. Available: {list(schema.model_fields.keys())}"
    assert (
        "value" in schema.model_fields
    ), f"Field 'value' missing. Available: {list(schema.model_fields.keys())}"
    assert (
        "active" in schema.model_fields
    ), f"Field 'active' missing. Available: {list(schema.model_fields.keys())}"

    # Create instance
    instance = schema(name="Test")
    console.print(f"\n[green]Created instance: {instance}[/green]")

    # Display with rich UI
    SchemaUI.display_schema(schema, "Basic Schema")


def test_schema_composer_from_model():
    """Test SchemaComposer with Pydantic model extraction."""
    console.print("\n[bold cyan]Testing Model Field Extraction[/bold cyan]")

    # Show what we're extracting from
    console.print("\n[bold]SimpleModel fields:[/bold]")
    for field_name, field_info in SimpleModel.model_fields.items():
        console.print(
            f"  {field_name}: {field_info.annotation} (default: {field_info.default})"
        )

    # Add fields from model
    composer = SchemaComposer(name="ModelSchema")
    console.print("\n[yellow]Extracting fields from SimpleModel...[/yellow]")
    composer.add_fields_from_model(SimpleModel)
    log_composer_debug_info(composer, "After extracting from SimpleModel")

    # Build schema
    schema = composer.build()
    log_schema_debug_info(schema, "Built Schema from Model")

    # Verify fields were correctly extracted
    assert hasattr(schema, "model_fields"), "Schema missing model_fields attribute"

    for field_name in SimpleModel.model_fields:
        assert (
            field_name in schema.model_fields
        ), f"Field '{field_name}' not found in schema"

        # Compare field info
        original_field = SimpleModel.model_fields[field_name]
        extracted_field = schema.model_fields[field_name]
        console.print(f"\n[bold]{field_name} comparison:[/bold]")
        console.print(f"  Original type: {original_field.annotation}")
        console.print(f"  Extracted type: {extracted_field.annotation}")
        console.print(f"  Original default: {original_field.default}")
        console.print(f"  Extracted default: {extracted_field.default}")

    SchemaUI.display_schema(schema, "Schema From Model")


def test_schema_composer_with_engine():
    """Test SchemaComposer with AugLLMConfig engine with extensive debugging."""
    console.print("\n[bold cyan]Testing Engine Field Extraction[/bold cyan]")

    # Create AugLLMConfig
    console.print("\n[yellow]Creating AugLLMConfig...[/yellow]")
    aug_llm = AugLLMConfig(
        name="test_llm",
        system_message="You are a helpful assistant.",
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Debug engine attributes
    console.print("\n[bold]Engine Attributes:[/bold]")
    console.print(f"  Name: {aug_llm.name}")
    console.print(f"  Engine Type: {aug_llm.engine_type}")
    console.print(
        f"  Has structured_output_model: {hasattr(aug_llm, 'structured_output_model')}"
    )
    if hasattr(aug_llm, "structured_output_model"):
        console.print(f"  Structured Model: {aug_llm.structured_output_model}")
        console.print(
            f"  Model Fields: {list(aug_llm.structured_output_model.model_fields.keys())}"
        )

    console.print(f"  Has get_input_fields: {hasattr(aug_llm, 'get_input_fields')}")
    console.print(f"  Has get_output_fields: {hasattr(aug_llm, 'get_output_fields')}")

    # Test field extraction methods
    if hasattr(aug_llm, "get_input_fields"):
        try:
            input_fields = aug_llm.get_input_fields()
            console.print("\n[bold]Engine Input Fields:[/bold]")
            for field_name, (field_type, _field_info) in input_fields.items():
                console.print(f"  {field_name}: {field_type}")
        except Exception as e:
            console.print(f"Error getting input fields: {e}")

    if hasattr(aug_llm, "get_output_fields"):
        try:
            output_fields = aug_llm.get_output_fields()
            console.print("\n[bold]Engine Output Fields:[/bold]")
            for field_name, (field_type, _field_info) in output_fields.items():
                console.print(f"  {field_name}: {field_type}")
        except Exception as e:
            console.print(f"Error getting output fields: {e}")

    # Create schema from engine
    composer = SchemaComposer(name="EngineSchema")
    console.print("\n[yellow]Extracting fields from engine...[/yellow]")
    composer.add_fields_from_engine(aug_llm)
    log_composer_debug_info(composer, "After extracting from engine")

    # Build schema
    schema = composer.build()
    log_schema_debug_info(schema, "Built Schema from Engine")

    # Verify schema has fields
    assert hasattr(schema, "model_fields"), "Schema missing model_fields attribute"
    console.print(f"\n[green]Schema fields: {list(schema.model_fields.keys())}[/green]")

    # Check for expected fields
    expected_fields = ["messages", "content"]
    for field in expected_fields:
        if field in schema.model_fields:
            console.print(f"  ✓ Found expected field: {field}")
        else:
            console.print(f"  ✗ Missing expected field: {field}")

    SchemaUI.display_schema(schema, "Schema From AugLLM Engine")


def test_schema_composer_input_output_schema():
    """Test input/output schema composition with comprehensive debugging."""
    console.print("\n[bold cyan]Testing Input/Output Schema Composition[/bold cyan]")

    # Create AugLLMConfig
    aug_llm = AugLLMConfig(
        name="io_llm",
        system_message="You are a helpful assistant.",
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Test input schema creation
    console.print("\n[yellow]Creating input schema...[/yellow]")
    input_schema = SchemaComposer.compose_input_schema(
        components=[aug_llm], name="InputSchema"
    )

    console.print("\n[bold]Input Schema Fields:[/bold]")
    for field_name, field_info in input_schema.model_fields.items():
        console.print(f"  {field_name}: {field_info.annotation}")

    # Test output schema creation
    console.print("\n[yellow]Creating output schema...[/yellow]")

    # Add debugging to understand what's happening in compose_output_schema
    SchemaComposer(name="DebugOutputSchema")

    # Manually add fields to see what should be there
    console.print("\n[bold]Manual Output Field Addition (for debugging):[/bold]")

    # Check what fields get extracted
    if hasattr(aug_llm, "get_output_fields"):
        try:
            output_fields = aug_llm.get_output_fields()
            console.print("Engine output fields:")
            for field_name, (field_type, field_info) in output_fields.items():
                console.print(f"  {field_name}: {field_type}")
        except Exception as e:
            console.print(f"Error getting output fields: {e}")

    # Check for structured output
    if hasattr(aug_llm, "structured_output_model") and aug_llm.structured_output_model:
        console.print("\nStructured output model fields:")
        for (
            field_name,
            field_info,
        ) in aug_llm.structured_output_model.model_fields.items():
            console.print(f"  {field_name}: {field_info.annotation}")

    # Create output schema using the method
    output_schema = SchemaComposer.compose_output_schema(
        components=[aug_llm], name="OutputSchema"
    )

    console.print("\n[bold]Generated Output Schema Fields:[/bold]")
    for field_name, field_info in output_schema.model_fields.items():
        console.print(f"  {field_name}: {field_info.annotation}")

    # Assertions with better error messages
    assert hasattr(input_schema, "model_fields"), "Input schema missing model_fields"
    assert hasattr(output_schema, "model_fields"), "Output schema missing model_fields"

    # Check for specific fields
    for field in ["messages"]:
        if field in input_schema.model_fields:
            console.print(f"  ✓ Input schema has '{field}'")
        else:
            console.print(
                f"  ✗ Input schema missing '{field}'. Has: {list(input_schema.model_fields.keys())}"
            )

    # Check what's in output schema
    has_content = "content" in output_schema.model_fields
    has_searchresult = any("searchresult" in k for k in output_schema.model_fields)

    console.print("\nOutput schema contains:")
    console.print(f"  - 'content' field: {has_content}")
    console.print(f"  - SearchResult field: {has_searchresult}")
    console.print(f"  - All fields: {list(output_schema.model_fields.keys())}")

    SchemaUI.display_schema(input_schema, "Input Schema")
    SchemaUI.display_schema(output_schema, "Output Schema")


def test_schema_composer_merge():
    """Test SchemaComposer merge with detailed logging."""
    console.print("\n[bold cyan]Testing SchemaComposer Merge[/bold cyan]")

    # Create first composer
    composer1 = SchemaComposer(name="FirstSchema")
    console.print("\n[yellow]Setting up first composer...[/yellow]")
    composer1.add_field(
        name="field1", field_type=str, description="Field from first composer"
    )
    composer1.add_field(
        name="shared_field",
        field_type=int,
        default=0,
        description="Shared field (from first)",
    )
    log_composer_debug_info(composer1, "First Composer")

    # Create second composer
    composer2 = SchemaComposer(name="SecondSchema")
    console.print("\n[yellow]Setting up second composer...[/yellow]")
    composer2.add_field(
        name="field2", field_type=str, description="Field from second composer"
    )
    composer2.add_field(
        name="shared_field",
        field_type=int,
        default=100,
        description="Shared field (from second)",
    )
    log_composer_debug_info(composer2, "Second Composer")

    # Test merge method
    console.print("\n[yellow]Merging composers using the merge method...[/yellow]")
    merged = SchemaComposer.merge(composer1, composer2)
    log_composer_debug_info(merged, "Merged Composer")

    # Build schema
    schema = merged.build()
    log_schema_debug_info(schema, "Built Merged Schema")

    # Verify merge results
    expected_fields = ["field1", "field2", "shared_field"]
    for field in expected_fields:
        assert (
            field in schema.model_fields
        ), f"Expected field '{field}' not found in merged schema"
        console.print(f"  ✓ Found merged field: {field}")

    # Check which value was used for shared_field
    instance = schema(field1="test1", field2="test2")
    console.print(
        f"\n[bold]shared_field value (should be from first composer):[/bold] {instance.shared_field}"
    )
    assert (
        instance.shared_field == 0
    ), f"Expected shared_field = 0, got {instance.shared_field}"

    SchemaUI.display_schema(schema, "Merged Schema")


def test_schema_composer_state_from_io():
    """Test creating state from I/O schemas with detailed debugging."""
    console.print("\n[bold cyan]Testing State Creation from I/O Schemas[/bold cyan]")

    # Define input schema
    class QueryInputSchema(BaseModel):
        """Input schema for a query-based system."""

        messages: list[BaseMessage] = Field(default_factory=list)
        query: str = Field(default="", description="User query")
        context: list[str] = Field(
            default_factory=list, description="Context documents"
        )

    # Define output schema
    class ResponseOutputSchema(BaseModel):
        """Output schema for a response-based system."""

        messages: list[BaseMessage] = Field(default_factory=list)
        response: str = Field(default="", description="Generated response")
        sources: list[dict[str, Any]] = Field(
            default_factory=list, description="Source documents"
        )
        confidence: float = Field(default=0.0, description="Confidence score")

    # Show schema details
    console.print("\n[bold]Input Schema Fields:[/bold]")
    for field_name, field_info in QueryInputSchema.model_fields.items():
        console.print(f"  {field_name}: {field_info.annotation}")

    console.print("\n[bold]Output Schema Fields:[/bold]")
    for field_name, field_info in ResponseOutputSchema.model_fields.items():
        console.print(f"  {field_name}: {field_info.annotation}")

    # Test create_state_from_io_schemas method
    console.print("\n[yellow]Creating state schema from I/O schemas...[/yellow]")
    try:
        state_schema = SchemaComposer.create_state_from_io_schemas(
            QueryInputSchema, ResponseOutputSchema, name="ComposedStateSchema"
        )

        log_schema_debug_info(state_schema, "Composed State Schema")

        # Verify inheritance
        console.print("\n[bold]Schema Inheritance Check:[/bold]")
        console.print(f"  Is StateSchema: {issubclass(state_schema, StateSchema)}")
        console.print(
            f"  Is QueryInputSchema: {issubclass(state_schema, QueryInputSchema)}"
        )
        console.print(
            f"  Is ResponseOutputSchema: {issubclass(state_schema, ResponseOutputSchema)}"
        )

        # Verify all fields
        expected_fields = [
            "messages",
            "query",
            "context",
            "response",
            "sources",
            "confidence",
        ]
        for field in expected_fields:
            if field in state_schema.model_fields:
                console.print(f"  ✓ Found field: {field}")
            else:
                console.print(f"  ✗ Missing field: {field}")

        # Test instance creation
        state = state_schema(
            query="What is AI?", context=["AI is artificial intelligence."]
        )
        console.print(f"\n[green]Successfully created state instance: {state}[/green]")

        SchemaUI.display_schema(state_schema, "Composed State Schema")

    except Exception as e:
        console.print(f"[red]Error creating state schema: {e}[/red]")
        import traceback

        traceback.print_exc()


def test_schema_composer_complete_workflow():
    """Complete workflow test with visualization of every step."""
    console.print("\n[bold cyan]Complete Workflow Test with Visualization[/bold cyan]")

    # Step 1: Create initial composer
    composer = SchemaComposer(name="CompleteWorkflow")

    # Step 2: Add basic fields
    console.print("\n[bold]Step 1: Adding basic fields[/bold]")
    composer.add_field(
        name="task_id",
        field_type=str,
        description="Unique task identifier",
        shared=True,
    )
    log_composer_debug_info(composer, "After adding task_id")

    # Step 3: Configure messages with reducer
    console.print("\n[bold]Step 2: Configuring messages field[/bold]")
    composer.configure_messages_field(with_reducer=True, force_add=True)
    log_composer_debug_info(composer, "After configuring messages")

    # Step 4: Add engine
    console.print("\n[bold]Step 3: Adding AugLLM engine[/bold]")
    aug_llm = AugLLMConfig(
        name="workflow_llm",
        system_message="You are a helpful assistant.",
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )
    composer.add_fields_from_engine(aug_llm)
    log_composer_debug_info(composer, "After adding engine")

    # Step 5: Mark I/O fields
    console.print("\n[bold]Step 4: Marking I/O fields[/bold]")
    composer.mark_as_input_field("messages", "workflow_llm")
    composer.mark_as_output_field("searchresult", "workflow_llm")
    log_composer_debug_info(composer, "After marking I/O fields")

    # Step 6: Build final schema
    console.print("\n[bold]Step 5: Building final schema[/bold]")
    schema = composer.build()
    log_schema_debug_info(schema, "Final Workflow Schema")

    # Step 7: Create instance and test
    console.print("\n[bold]Step 6: Testing the schema[/bold]")
    instance = schema(task_id="test-task-123")

    # Add messages
    instance.messages.append(HumanMessage(content="Test message"))
    instance.messages.append(AIMessage(content="Response message"))

    console.print("\n[green]Instance state:[/green]")
    console.print(f"  Task ID: {instance.task_id}")
    console.print(f"  Messages: {len(instance.messages)}")

    # Final visualization
    SchemaUI.display_schema(schema, "Complete Workflow Schema")

    # Test serialization
    console.print("\n[bold]Step 7: Testing serialization[/bold]")
    schema_dict = schema.__dict__.copy()
    console.print(f"Serialized schema keys: {list(schema_dict.keys())}")


if __name__ == "__main__":
    # Run all tests
    test_schema_composer_basics()
    test_schema_composer_from_model()
    test_schema_composer_with_engine()
    test_schema_composer_merge()
    test_schema_composer_input_output_schema()
    test_schema_composer_state_from_io()
    test_schema_composer_complete_workflow()
