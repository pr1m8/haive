"""UI utilities for displaying and visualizing schemas in a user-friendly way.

This module provides the SchemaUI class, which offers rich-formatted visualization
of schemas in the Haive Schema System. It allows for displaying schema structures,
generating equivalent Python code representations, and comparing schemas side by side
to identify differences.

The SchemaUI is designed to work with the Rich library to provide colorized,
structured terminal output for both schema classes and instances. This makes
it invaluable for debugging, development, and educational purposes when working
with the Haive Schema System.

Key features include:
- Rich terminal visualization of schema structure
- Python code generation for schema definitions
- Side-by-side schema comparison
- Specialized handling for StateSchema features
- Support for both class and instance visualization
- Highlight of important schema features like shared fields and reducers

Example:
    ```python
    from haive.core.schema import SchemaUI
    from haive.core.schema import SchemaComposer
    from typing import List

    # Create a schema
    composer = SchemaComposer(name="MyState")
    composer.add_field(
        name="messages",
        field_type=List[str],
        default_factory=list
    )
    MyState = composer.build()

    # Display schema structure
    SchemaUI.display_schema(MyState)

    # Generate Python code representation
    code = SchemaUI.schema_to_code(MyState)
    print(code)

    # Create an instance and display it
    state = MyState(messages=["Hello"])
    SchemaUI.display_schema(state, title="State Instance")
    ```
"""

import logging
from typing import Any, Type, Union

from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)


class SchemaUI:
    """UI utilities for visualizing and working with schemas.

    The SchemaUI class provides a collection of static methods for visualizing
    schema structures, generating equivalent Python code, and comparing different
    schemas side by side. It uses the Rich library to create colorized, structured
    terminal output that makes complex schema relationships more accessible.

    This class is particularly useful for:
    - Debugging schema composition and creation
    - Exploring schema structure and relationships
    - Generating code from dynamically created schemas
    - Understanding differences between schema versions
    - Visualizing shared fields and reducer configurations
    - Displaying the structure of StateSchema instances

    All methods in this class are static and focus on visualization rather than
    schema modification. For schema creation and manipulation, use SchemaComposer
    or StateSchemaManager instead.

    Note:
        The visualization capabilities support both Pydantic v1 and v2 models,
        with special handling for StateSchema-specific features like shared fields,
        reducers, and engine I/O mappings.
    """

    @staticmethod
    def display_schema(
        schema: type[BaseModel] | BaseModel, title: str = "Schema"
    ) -> None:
        """Display a schema or schema instance with rich formatting.

        Args:
            schema: Schema class or instance to display
            title: Title for the display
        """
        console = Console()

        # Determine if it's a class or instance
        is_class = isinstance(schema, type)

        # Create main panel
        panel = Panel(
            SchemaUI._create_schema_content(schema, is_class),
            title=title,
            border_style="blue",
            expand=False,
        )

        console.print(panel)

    @staticmethod
    def _create_schema_content(
        schema: type[BaseModel] | BaseModel, is_class: bool = True
    ) -> Any:
        """Create rich content for schema display.

        Args:
            schema: Schema class or instance
            is_class: Whether schema is a class or instance

        Returns:
            Rich content for display
        """
        is_state_schema = issubclass(
            schema.__class__ if not is_class else schema, StateSchema
        )
        schema_class = schema if is_class else schema.__class__
        schema_name = schema_class.__name__

        # Create layout
        tree = Tree(f"class {schema_name}({schema_class.__base__.__name__}):")
        tree.add('"""')
        tree.add(f"Generated {schema_name} schema")
        tree.add('"""')
        tree.add("")  # Empty line

        # Add fields section
        fields_node = tree.add("Fields:")

        # Get fields from class or instance
        if hasattr(schema_class, "model_fields"):  # Pydantic v2
            fields_dict = schema_class.model_fields

            for field_name, field_info in fields_dict.items():
                # Get field type as string
                field_type = field_info.annotation
                type_str = str(field_type).replace("typing.", "")

                # Get default value or factory
                if field_info.default_factory is not None:
                    factory_name = getattr(
                        field_info.default_factory, "__name__", "factory"
                    )
                    default_str = f"Field(default_factory={factory_name})"
                else:
                    default = field_info.default
                    default_str = (
                        "Field(...)"
                        if default is ...
                        else f"Field(default={default!r})"
                    )

                # Add description if available
                if field_info.description:
                    default_str = default_str.replace(
                        ")", f', description="{field_info.description}")'
                    )

                # For instances, show the actual value
                if not is_class and hasattr(schema, field_name):
                    value = getattr(schema, field_name)
                    value_str = SchemaUI._format_value(value)
                    fields_node.add(
                        f"{field_name}: {type_str} = {default_str} -> {value_str}"
                    )
                else:
                    fields_node.add(f"{field_name}: {type_str} = {default_str}")

        # Add StateSchema-specific sections
        if is_state_schema:
            # Add reducers section
            tree.add("")  # Empty line
            reducers_node = tree.add("Reducers:")
            if hasattr(schema_class, "__serializable_reducers__"):
                for (
                    field,
                    reducer_name,
                ) in schema_class.__serializable_reducers__.items():
                    reducers_node.add(f"{field}: {reducer_name}")

            # Add shared fields section
            tree.add("")  # Empty line
            shared_node = tree.add("Shared Fields:")
            if hasattr(schema_class, "__shared_fields__"):
                for field in schema_class.__shared_fields__:
                    shared_node.add(field)

            # Add engine I/O mappings
            tree.add("")  # Empty line
            io_node = tree.add("Engine I/O Mappings:")
            if hasattr(schema_class, "__engine_io_mappings__"):
                for engine_name, mapping in schema_class.__engine_io_mappings__.items():
                    engine_node = io_node.add(f"{engine_name}:")
                    engine_node.add(f"Inputs: {mapping.get('inputs', [])}")
                    engine_node.add(f"Outputs: {mapping.get('outputs', [])}")

        return tree

    @staticmethod
    def _format_value(value: Any) -> str:
        """Format a value for display, handling complex types.

        Args:
            value: Value to format

        Returns:
            Formatted string representation
        """
        if value is None:
            return "None"
        if isinstance(value, str):
            if len(value) > 100:
                return f'"{value[:97]}..."'
            return f'"{value}"'
        if isinstance(value, int | float | bool):
            return str(value)
        if isinstance(value, list):
            if not value:
                return "[]"
            if len(value) > 5:
                return f"[{', '.join(SchemaUI._format_value(v) for v in value[:3])}, ... ({len(value)} items)]"
            return f"[{', '.join(SchemaUI._format_value(v) for v in value)}]"
        if isinstance(value, dict):
            if not value:
                return "{}"
            if len(value) > 3:
                keys = list(value.keys())[:3]
                formatted = ", ".join(
                    f"{k}: {SchemaUI._format_value(value[k])}" for k in keys
                )
                return f"{{{formatted}, ... ({len(value)} items)}}"
            return f"{{{', '.join(f'{k}: {SchemaUI._format_value(v)}' for k, v in value.items())}}}"
        elif hasattr(value, "model_dump"):  # Pydantic v2
            class_name = value.__class__.__name__
            return f"{class_name}(...)"
        else:
            return str(value)

    @staticmethod
    def schema_to_code(schema: type[BaseModel]) -> str:
        """Convert schema to Python code representation.

        Args:
            schema: Schema class to convert

        Returns:
            String containing Python code representation
        """
        is_state_schema = issubclass(schema, StateSchema)
        lines = [f"class {schema.__name__}({schema.__base__.__name__}):"]
        lines.append('    """')
        lines.append(f"    Generated {schema.__name__} schema")
        lines.append('    """')

        # Add fields
        if hasattr(schema, "model_fields"):  # Pydantic v2
            fields_dict = schema.model_fields

            for field_name, field_info in fields_dict.items():
                # Get field type as string
                field_type = field_info.annotation
                type_str = str(field_type).replace("typing.", "")

                # Get default value or factory
                if field_info.default_factory is not None:
                    factory_name = getattr(
                        field_info.default_factory, "__name__", "factory"
                    )
                    default_str = f"Field(default_factory={factory_name})"
                else:
                    default = field_info.default
                    default_str = (
                        "Field(...)"
                        if default is ...
                        else f"Field(default={default!r})"
                    )

                # Add description if available
                if field_info.description:
                    default_str = default_str.replace(
                        ")", f', description="{field_info.description}")'
                    )

                lines.append(f"    {field_name}: {type_str} = {default_str}")

        # Add StateSchema-specific sections
        if is_state_schema:
            # Add shared fields
            if hasattr(schema, "__shared_fields__") and schema.__shared_fields__:
                lines.append("")
                lines.append(f"    __shared_fields__ = {schema.__shared_fields__}")

            # Add serializable reducers
            if (
                hasattr(schema, "__serializable_reducers__")
                and schema.__serializable_reducers__
            ):
                lines.append("")
                lines.append(
                    f"    __serializable_reducers__ = {schema.__serializable_reducers__}"
                )

        return "\n".join(lines)

    @staticmethod
    def display_schema_code(
        schema: type[BaseModel], title: str = "Schema Code"
    ) -> None:
        """Display schema as syntax-highlighted Python code.

        Args:
            schema: Schema class to display
            title: Title for the display
        """
        console = Console()
        code = SchemaUI.schema_to_code(schema)
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)

        panel = Panel(syntax, title=title, border_style="green", expand=False)

        console.print(panel)

    @staticmethod
    def compare_schemas(
        schema1: type[BaseModel],
        schema2: type[BaseModel],
        title1: str = "Schema 1",
        title2: str = "Schema 2",
    ) -> None:
        """Compare two schemas side by side.

        Args:
            schema1: First schema to compare
            schema2: Second schema to compare
            title1: Title for first schema
            title2: Title for second schema
        """
        console = Console()

        # Create table for comparison
        table = Table(title="Schema Comparison")

        # Add columns
        table.add_column("Field", style="cyan")
        table.add_column(title1, style="green")
        table.add_column(title2, style="blue")

        # Get fields from both schemas
        fields1 = getattr(schema1, "model_fields", {})
        fields2 = getattr(schema2, "model_fields", {})

        # Combine all unique field names
        all_fields = set(fields1.keys()) | set(fields2.keys())

        # Add rows for each field
        for field_name in sorted(all_fields):
            field1 = fields1.get(field_name)
            field2 = fields2.get(field_name)

            field1_str = SchemaUI._format_field(field1) if field1 else "Not present"
            field2_str = SchemaUI._format_field(field2) if field2 else "Not present"

            table.add_row(field_name, field1_str, field2_str)

        # Add rows for metadata
        table.add_section()

        # Compare shared fields
        shared1 = getattr(schema1, "__shared_fields__", [])
        shared2 = getattr(schema2, "__shared_fields__", [])
        table.add_row("Shared Fields", str(shared1), str(shared2))

        # Compare reducers
        reducers1 = getattr(schema1, "__serializable_reducers__", {})
        reducers2 = getattr(schema2, "__serializable_reducers__", {})
        table.add_row("Reducers", str(reducers1), str(reducers2))

        console.print(table)

    @staticmethod
    def _format_field(field_info: Any) -> str:
        """Format field info for display.

        Args:
            field_info: Field info to format

        Returns:
            Formatted string representation
        """
        if field_info is None:
            return "None"

        # Extract type
        type_str = str(field_info.annotation).replace("typing.", "")

        # Extract default
        if field_info.default_factory is not None:
            factory_name = getattr(field_info.default_factory, "__name__", "factory")
            default_str = f"default_factory={factory_name}"
        else:
            default = field_info.default
            default_str = "required" if default is ... else f"default={default!r}"

        return f"{type_str} ({default_str})"


# Create convenience function for easy access
def display_schema(schema: type[BaseModel] | BaseModel, title: str = "Schema") -> None:
    """Display a schema or schema instance with rich formatting.

    Args:
        schema: Schema class or instance to display
        title: Title for the display
    """
    SchemaUI.display_schema(schema, title)
