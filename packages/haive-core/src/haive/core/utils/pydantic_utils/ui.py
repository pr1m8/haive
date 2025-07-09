"""
Pydantic model utilities for serialization, visualization, and code generation.

This module provides standalone functions for visualizing, comparing, and
generating code from Pydantic BaseModel classes and instances, without
requiring inheritance from specialized base classes.
"""

import inspect
import json
from typing import Any, Optional, Type, Union, get_args, get_origin

from pydantic import BaseModel


def display_model(
    model: Union[Type[BaseModel], BaseModel], title: Optional[str] = None
) -> None:
    """
    Display a Pydantic model or instance with clear formatting.

    Args:
        model: Model class or instance to display
        title: Optional title for the display
    """
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.tree import Tree

        console = Console()

        # Determine if it's a class or instance
        is_class = isinstance(model, type)
        model_class = model if is_class else model.__class__

        # Create title
        display_title = (
            title or f"{model_class.__name__} {'Schema' if is_class else 'Instance'}"
        )

        # Create main tree
        tree = Tree(f"{'class' if is_class else 'instance of'} {model_class.__name__}:")

        # Add fields
        fields_node = tree.add("Fields:")

        # Get fields based on version
        if hasattr(model_class, "model_fields"):  # Pydantic v2
            for field_name, field_info in model_class.model_fields.items():
                # Skip internal fields
                if field_name.startswith("__"):
                    continue

                # Format field type (safer implementation)
                type_str = format_type_annotation(field_info.annotation)

                # Format default value
                default_str = format_default_value(field_info)

                # For instances, show actual value
                if not is_class and hasattr(model, field_name):
                    value = getattr(model, field_name)
                    value_str = format_value(value)
                    field_str = (
                        f"{field_name}: {type_str} = {default_str} → {value_str}"
                    )
                else:
                    # Get description if available
                    if hasattr(field_info, "description") and field_info.description:
                        field_str = f"{field_name}: {type_str} = {default_str} # {field_info.description}"
                    else:
                        field_str = f"{field_name}: {type_str} = {default_str}"

                fields_node.add(field_str)

        # Create and display panel
        panel = Panel(tree, title=display_title, border_style="blue")
        console.print(panel)

    except ImportError:
        # Fall back to simple print if rich is not available
        print_model_simple(model, title)


def print_model_simple(
    model: Union[Type[BaseModel], BaseModel], title: Optional[str] = None
) -> None:
    """
    Simple print fallback when rich is not available.

    Args:
        model: Model class or instance to display
        title: Optional title for the display
    """
    is_class = isinstance(model, type)
    model_class = model if is_class else model.__class__

    print(
        f"--- {title or model_class.__name__} {'Schema' if is_class else 'Instance'} ---"
    )
    print(f"{'class' if is_class else 'instance of'} {model_class.__name__}:")
    print("  Fields:")

    if hasattr(model_class, "model_fields"):  # Pydantic v2
        for field_name, field_info in model_class.model_fields.items():
            if field_name.startswith("__"):
                continue

            type_str = format_type_annotation(field_info.annotation)
            default_str = format_default_value(field_info)

            if not is_class and hasattr(model, field_name):
                value = getattr(model, field_name)
                value_str = format_value(value)
                print(f"    {field_name}: {type_str} = {default_str} → {value_str}")
            else:
                if hasattr(field_info, "description") and field_info.description:
                    print(
                        f"    {field_name}: {type_str} = {default_str} # {field_info.description}"
                    )
                else:
                    print(f"    {field_name}: {type_str} = {default_str}")


def model_to_code(model_class: Type[BaseModel]) -> str:
    """
    Generate Python code representation of a Pydantic model.

    Args:
        model_class: Model class to convert to code

    Returns:
        String containing Python code representation
    """
    lines = [f"class {model_class.__name__}(BaseModel):"]

    # Add docstring if available
    doc = inspect.getdoc(model_class)
    if doc:
        lines.append('    """')
        for line in doc.split("\n"):
            lines.append(f"    {line}")
        lines.append('    """')
    else:
        lines.append('    """')
        lines.append(f"    {model_class.__name__} model")
        lines.append('    """')

    lines.append("")

    # Add fields
    if hasattr(model_class, "model_fields"):  # Pydantic v2
        for field_name, field_info in model_class.model_fields.items():
            if field_name.startswith("__"):
                continue

            # Format field type
            type_str = format_type_annotation(field_info.annotation)

            # Format field definition with default
            if field_info.default_factory is not None:
                factory_name = getattr(
                    field_info.default_factory, "__name__", "factory"
                )
                field_str = (
                    f"{field_name}: {type_str} = Field(default_factory={factory_name}"
                )
            else:
                default = field_info.default
                if default is ...:
                    field_str = f"{field_name}: {type_str} = Field(...)"
                else:
                    field_str = (
                        f"{field_name}: {type_str} = Field(default={repr(default)}"
                    )

            # Add description if available
            if hasattr(field_info, "description") and field_info.description:
                if not field_str.endswith(")"):
                    field_str += ", "
                field_str += f'description="{field_info.description}")'
            elif not field_str.endswith(")"):
                field_str += ")"

            lines.append(f"    {field_str}")

    return "\n".join(lines)


def display_code(model_class: Type[BaseModel], title: Optional[str] = None) -> None:
    """
    Display Python code representation of a Pydantic model.

    Args:
        model_class: Model class to display
        title: Optional title for the display
    """
    code = model_to_code(model_class)

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.syntax import Syntax

        console = Console()
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
        panel = Panel(
            syntax, title=title or f"{model_class.__name__} Code", border_style="green"
        )
        console.print(panel)
    except ImportError:
        # Fall back to simple print
        print(f"--- {title or model_class.__name__} Code ---")
        print(code)


def compare_models(
    model1: Type[BaseModel],
    model2: Type[BaseModel],
    title1: Optional[str] = None,
    title2: Optional[str] = None,
) -> None:
    """
    Compare two Pydantic models side by side.

    Args:
        model1: First model to compare
        model2: Second model to compare
        title1: Optional title for first model
        title2: Optional title for second model
    """
    title1 = title1 or model1.__name__
    title2 = title2 or model2.__name__

    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title=f"Model Comparison: {title1} vs {title2}")

        # Add columns
        table.add_column("Field", style="cyan")
        table.add_column(title1, style="green")
        table.add_column(title2, style="blue")

        # Get fields
        fields1 = getattr(model1, "model_fields", {})
        fields2 = getattr(model2, "model_fields", {})

        # Combine fields
        all_fields = set(fields1.keys()) | set(fields2.keys())
        all_fields = {field for field in all_fields if not field.startswith("__")}

        # Add rows
        for field_name in sorted(all_fields):
            field1 = fields1.get(field_name)
            field2 = fields2.get(field_name)

            # Format fields
            field1_str = format_field_info(field1) if field1 else "Not present"
            field2_str = format_field_info(field2) if field2 else "Not present"

            table.add_row(field_name, field1_str, field2_str)

        console.print(table)
    except ImportError:
        # Fall back to simple print
        print(f"--- Model Comparison: {title1} vs {title2} ---")
        fields1 = getattr(model1, "model_fields", {})
        fields2 = getattr(model2, "model_fields", {})

        print("Fields in both:")
        for field in set(fields1.keys()) & set(fields2.keys()):
            if not field.startswith("__"):
                print(f"  {field}")

        print(f"Fields only in {title1}:")
        for field in set(fields1.keys()) - set(fields2.keys()):
            if not field.startswith("__"):
                print(f"  {field}")

        print(f"Fields only in {title2}:")
        for field in set(fields2.keys()) - set(fields1.keys()):
            if not field.startswith("__"):
                print(f"  {field}")


def pretty_print(model_instance: BaseModel, title: Optional[str] = None) -> None:
    """
    Pretty print a Pydantic model instance.

    Args:
        model_instance: Model instance to print
        title: Optional title for the display
    """
    display_model(model_instance, title)


def format_type_annotation(type_annotation: Any) -> str:
    """
    Format type annotation for display.

    Args:
        type_annotation: The type annotation to format

    Returns:
        Formatted string representation of the type annotation
    """
    # Handle None case
    if type_annotation is None:
        return "Any"

    # Handle primitive types
    if type_annotation is str:
        return "str"
    if type_annotation is int:
        return "int"
    if type_annotation is float:
        return "float"
    if type_annotation is bool:
        return "bool"

    # Get module string representation
    type_str = str(type_annotation)

    # Get origin and arguments for complex types
    origin = get_origin(type_annotation)
    args = get_args(type_annotation)

    # Handle non-parameterized types
    if origin is None:
        # Handle classes with names
        if hasattr(type_annotation, "__name__"):
            # For types from typing, use the name directly
            if type_str.startswith("typing."):
                return type_annotation.__name__
            # For other types, return the full name
            return type_annotation.__name__
        # Special case for list and dict types
        if type_str == "typing.List":
            return "List"
        if type_str == "typing.Dict":
            return "Dict"
        # Clean up remaining typing prefixes
        return type_str.replace("typing.", "")

    # Handle parameterized types
    if origin is list or str(origin) == "typing.List":
        if args:
            return f"List[{format_type_annotation(args[0])}]"
        return "List"
    elif origin is dict or str(origin) == "typing.Dict":
        if len(args) == 2:
            return f"Dict[{format_type_annotation(args[0])}, {format_type_annotation(args[1])}]"
        return "Dict"
    elif origin is Union or str(origin) == "typing.Union":
        # Handle Optional (Union with None)
        if len(args) == 2 and (type(None) in args):
            non_none_type = args[0] if args[1] is type(None) else args[1]
            return f"Optional[{format_type_annotation(non_none_type)}]"
        inner_types = [format_type_annotation(arg) for arg in args]
        return f"Union[{', '.join(inner_types)}]"

    # For other generic types
    formatted_args = [format_type_annotation(arg) for arg in args]
    type_name = str(origin).replace("typing.", "")
    if "." in type_name:
        type_name = type_name.split(".")[-1]
    if formatted_args:
        return f"{type_name}[{', '.join(formatted_args)}]"
    return type_name


def format_default_value(field_info: Any) -> str:
    """
    Format default value for display.

    Args:
        field_info: The field info to format

    Returns:
        Formatted string representation of the default value
    """
    try:
        if (
            hasattr(field_info, "default_factory")
            and field_info.default_factory is not None
        ):
            factory_name = getattr(field_info.default_factory, "__name__", "factory")
            return f"default_factory={factory_name}"
        else:
            default = field_info.default
            if default is ...:
                return "required"
            return f"default={repr(default)}"
    except Exception as e:
        return f"<error formatting default: {str(e)}>"


def format_value(value: Any) -> str:
    """
    Format a value for display.

    Args:
        value: The value to format

    Returns:
        Formatted string representation of the value
    """
    try:
        if value is None:
            return "None"
        elif isinstance(value, str):
            if len(value) > 50:
                return f'"{value[:47]}..."'
            return f'"{value}"'
        elif isinstance(value, (int, float, bool)):
            return str(value)
        elif isinstance(value, list):
            if not value:
                return "[]"
            if len(value) > 3:
                return f"[{', '.join(format_value(v) for v in value[:2])}, ... ({len(value)} items)]"
            return f"[{', '.join(format_value(v) for v in value)}]"
        elif isinstance(value, dict):
            if not value:
                return "{}"
            if len(value) > 3:
                items = list(value.items())[:2]
                return f"{{{', '.join(f'{k}: {format_value(v)}' for k, v in items)}, ... ({len(value)} items)}}"
            return (
                f"{{{', '.join(f'{k}: {format_value(v)}' for k, v in value.items())}}}"
            )
        elif hasattr(value, "model_dump"):  # Pydantic v2
            class_name = value.__class__.__name__
            return f"{class_name}(...)"
        return str(value)
    except Exception as e:
        return f"<error formatting value: {str(e)}>"


def format_field_info(field_info: Any) -> str:
    """
    Format field info for comparison display.

    Args:
        field_info: The field info to format

    Returns:
        Formatted string representation of the field info
    """
    if field_info is None:
        return "None"

    try:
        # Extract type
        type_str = format_type_annotation(field_info.annotation)

        # Extract default
        default_str = format_default_value(field_info)

        # Add description if available
        description = getattr(field_info, "description", None)
        if description:
            return f"{type_str} ({default_str}, description: {description})"

        return f"{type_str} ({default_str})"
    except Exception as e:
        return f"<error formatting field: {str(e)}>"


def schema_to_code(schema: Any) -> str:
    """
    Generate Python code for a schema (possibly ComposedSchema).

    Args:
        schema: The schema to convert to code

    Returns:
        String containing Python code representation
    """
    if not schema:
        return "# No schema provided"

    # Handle the case where schema is a class
    if isinstance(schema, type):
        if hasattr(schema, "to_python_code") and callable(schema.to_python_code):
            return schema.to_python_code()
        return model_to_code(schema)

    # Handle case where schema is a class instance with to_python_code method
    if hasattr(schema, "to_python_code") and callable(schema.to_python_code):
        return schema.to_python_code()

    # Handle the case where schema is a BaseModel instance
    if isinstance(schema, BaseModel):
        return model_to_code(schema.__class__)

    # Default case
    return f"# Unable to generate code for schema of type {type(schema)}"
