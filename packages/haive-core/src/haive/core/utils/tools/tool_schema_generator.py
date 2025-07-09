"""Tool schema extraction utilities for the Haive framework.

This module provides utilities to extract Pydantic input schemas from various
callable types including regular functions, LangChain tools, and other tool types.
Also includes utilities for creating StructuredTool instances and ToolNode configurations.
"""

import inspect
import logging
import re
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field, create_model

logger = logging.getLogger(__name__)

# Type definitions for different tool types
try:
    from langchain_core.tools import BaseTool, StructuredTool
    from langchain_core.tools.base import BaseToolkit
    from langgraph.prebuilt import ToolNode

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseTool = None
    StructuredTool = None
    BaseToolkit = None
    ToolNode = None


def extract_input_schema(
    tool_or_callable: Union[Callable, Any],
    schema_name: Optional[str] = None,
    include_docstring: bool = True,
    strict_typing: bool = False,
    include_signature: bool = True,
) -> Type[BaseModel]:
    """
    Extract a Pydantic input schema from a callable or tool.

    This function can handle:
    - Regular Python functions with type hints
    - LangChain BaseTool instances
    - LangChain StructuredTool instances
    - Any callable with proper type annotations

    Args:
        tool_or_callable: The callable or tool to extract schema from
        schema_name: Optional name for the generated schema class
        include_docstring: Whether to extract descriptions from docstrings
        strict_typing: Whether to be strict about type annotations
        include_signature: Whether to store the original function signature

    Returns:
        Pydantic BaseModel class representing the input schema

    Example:
        ```python
        def my_function(name: str, age: int = 25, active: bool = True):
            '''Process user information.

            Args:
                name: User's full name
                age: User's age in years
                active: Whether the user is active
            '''
            return f"User {name} is {age} years old"

        Schema = extract_input_schema(my_function)
        # Creates a Pydantic model with name, age, active fields
        # and stores the original signature for dynamic invocation
        ```
    """
    # Determine schema name
    if schema_name is None:
        if hasattr(tool_or_callable, "name"):
            schema_name = f"{tool_or_callable.name}Input"
        elif hasattr(tool_or_callable, "__name__"):
            schema_name = f"{tool_or_callable.__name__}Input"
        else:
            schema_name = "ToolInput"

    # Handle different tool types
    if LANGCHAIN_AVAILABLE and isinstance(tool_or_callable, Type[BaseTool]):
        return _extract_from_langchain_tool(tool_or_callable, schema_name)
    elif callable(tool_or_callable):
        return _extract_from_callable(
            tool_or_callable,
            schema_name,
            include_docstring,
            strict_typing,
            include_signature,
        )
    else:
        raise ValueError(f"Unsupported tool type: {type(tool_or_callable)}")


def _extract_from_langchain_tool(tool: Any, schema_name: str) -> Type[BaseModel]:
    """Extract schema from a LangChain tool."""

    # Check if tool already has an input schema
    if hasattr(tool, "args_schema") and tool.args_schema is not None:
        # Return existing schema or create a copy with new name
        if tool.args_schema.__name__ == schema_name:
            return tool.args_schema

        # Create a copy with the desired name
        fields = {}
        for field_name, field_info in tool.args_schema.model_fields.items():
            fields[field_name] = (field_info.annotation, field_info)

        return create_model(schema_name, **fields)

    # If tool has a _run method, extract from that
    if hasattr(tool, "_run"):
        return _extract_from_callable(tool._run, schema_name, True, False, True)

    # If tool has a run method, extract from that
    if hasattr(tool, "run"):
        return _extract_from_callable(tool.run, schema_name, True, False, True)

    # Fallback: create a generic schema
    logger.warning(
        f"Could not extract specific schema from tool {tool.name if hasattr(tool, 'name') else 'unknown'}"
    )
    return create_model(schema_name, input=(str, Field(description="Tool input")))


def _extract_from_callable(
    func: Callable,
    schema_name: str,
    include_docstring: bool = True,
    strict_typing: bool = False,
    include_signature: bool = True,
) -> Type[BaseModel]:
    """Extract schema from a regular callable."""

    # Get function signature
    signature = None
    try:
        signature = inspect.signature(func)
    except (ValueError, TypeError) as e:
        logger.warning(f"Could not inspect signature of {func}: {e}")
        schema = create_model(
            schema_name, input=(str, Field(description="Function input"))
        )
        if include_signature:
            schema.__signature_info__ = {"error": str(e), "callable": func}
        return schema

    # Get type hints
    try:
        type_hints = get_type_hints(func)
    except (NameError, AttributeError, TypeError) as e:
        logger.warning(f"Could not get type hints for {func}: {e}")
        type_hints = {}

    # Extract parameter descriptions from docstring
    param_descriptions = {}
    if include_docstring and func.__doc__:
        param_descriptions = _extract_param_descriptions(func.__doc__)

    # Build field definitions
    fields = {}

    for param_name, param in signature.parameters.items():
        # Skip 'self' and 'cls' parameters
        if param_name in ("self", "cls"):
            continue

        # Skip **kwargs and *args
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue

        # Get type annotation
        param_type = type_hints.get(param_name, param.annotation)

        # Handle missing type annotations
        if param_type == inspect.Parameter.empty:
            if strict_typing:
                raise ValueError(f"Parameter {param_name} has no type annotation")
            param_type = Any

        # Handle default values
        default_value = param.default
        field_kwargs = {}

        if default_value != inspect.Parameter.empty:
            field_kwargs["default"] = default_value
        else:
            # No default means required field
            field_kwargs["default"] = ...

        # Add description from docstring
        if param_name in param_descriptions:
            field_kwargs["description"] = param_descriptions[param_name]

        # Create field
        if field_kwargs.get("default") == ...:
            # Required field
            fields[param_name] = (
                param_type,
                Field(**{k: v for k, v in field_kwargs.items() if k != "default"}),
            )
        else:
            # Optional field with default
            fields[param_name] = (param_type, Field(**field_kwargs))

    # Handle case where function has no parameters
    if not fields:
        logger.warning(
            f"Function {func.__name__ if hasattr(func, '__name__') else 'unknown'} has no extractable parameters"
        )
        schema = create_model(schema_name)
        if include_signature:
            schema.__signature_info__ = {
                "signature": signature,
                "callable": func,
                "has_parameters": False,
            }
        return schema

    # Create and return the model
    try:
        schema = create_model(schema_name, **fields)

        # Store signature information for dynamic invocation
        if include_signature:
            schema.__signature_info__ = {
                "signature": signature,
                "callable": func,
                "parameter_count": len(signature.parameters),
                "required_params": [
                    name
                    for name, field in schema.model_fields.items()
                    if field.default == ... or field.default is None
                ],
                "optional_params": [
                    name
                    for name, field in schema.model_fields.items()
                    if field.default != ... and field.default is not None
                ],
                "type_hints": type_hints,
                "docstring": func.__doc__,
            }

        return schema
    except Exception as e:
        logger.error(f"Failed to create model {schema_name}: {e}")
        # Fallback to a simple model
        fallback_schema = create_model(
            schema_name, input=(str, Field(description="Function input"))
        )
        if include_signature:
            fallback_schema.__signature_info__ = {
                "signature": signature,
                "callable": func,
                "error": str(e),
            }
        return fallback_schema


def _extract_param_descriptions(docstring: str) -> Dict[str, str]:
    """
    Extract parameter descriptions from a docstring.

    Supports multiple docstring formats:
    - Google style
    - NumPy style
    - Sphinx style
    """
    descriptions = {}

    # Try Google style first: "Args:" section
    google_match = re.search(
        r"Args?:\s*\n(.*?)(?:\n\s*\n|\n[A-Z][a-z]+:|\Z)",
        docstring,
        re.DOTALL | re.IGNORECASE,
    )
    if google_match:
        args_section = google_match.group(1)
        # Match parameter lines: "param_name: description" or "param_name (type): description"
        param_matches = re.findall(
            r"^\s*(\w+)(?:\s*\([^)]+\))?\s*:\s*(.+?)(?=^\s*\w+(?:\s*\([^)]+\))?\s*:|$)",
            args_section,
            re.MULTILINE | re.DOTALL,
        )
        for param_name, description in param_matches:
            descriptions[param_name.strip()] = " ".join(description.strip().split())

    # Try NumPy style: "Parameters" section
    if not descriptions:
        numpy_match = re.search(
            r"Parameters\s*\n\s*-+\s*\n(.*?)(?:\n\s*\n|\n[A-Z][a-z]+\s*\n\s*-+|\Z)",
            docstring,
            re.DOTALL | re.IGNORECASE,
        )
        if numpy_match:
            params_section = numpy_match.group(1)
            # Match parameter blocks
            param_blocks = re.findall(
                r"(\w+)\s*:\s*([^:]+?)(?=\n\w+\s*:|$)", params_section, re.DOTALL
            )
            for param_name, description in param_blocks:
                descriptions[param_name.strip()] = " ".join(description.strip().split())

    # Try Sphinx style: ":param name: description"
    if not descriptions:
        sphinx_matches = re.findall(
            r":param\s+(\w+)\s*:\s*(.+?)(?=:param|\Z)", docstring, re.DOTALL
        )
        for param_name, description in sphinx_matches:
            descriptions[param_name.strip()] = " ".join(description.strip().split())

    return descriptions


def extract_output_schema(
    tool_or_callable: Union[Callable, Any],
    schema_name: Optional[str] = None,
    include_docstring: bool = True,
) -> Optional[Type[BaseModel]]:
    """
    Extract a Pydantic output schema from a callable or tool.

    Args:
        tool_or_callable: The callable or tool to extract schema from
        schema_name: Optional name for the generated schema class
        include_docstring: Whether to extract descriptions from docstrings

    Returns:
        Pydantic BaseModel class representing the output schema, or None if not extractable
    """
    # Determine schema name
    if schema_name is None:
        if hasattr(tool_or_callable, "name"):
            schema_name = f"{tool_or_callable.name}Output"
        elif hasattr(tool_or_callable, "__name__"):
            schema_name = f"{tool_or_callable.__name__}Output"
        else:
            schema_name = "ToolOutput"

    # Handle LangChain tools
    if LANGCHAIN_AVAILABLE and isinstance(tool_or_callable, BaseTool):
        # Most LangChain tools return strings, but check if there's a specific schema
        return create_model(schema_name, output=(str, Field(description="Tool output")))

    # Handle regular callables
    if callable(tool_or_callable):
        try:
            # Get return type annotation
            signature = inspect.signature(tool_or_callable)
            return_annotation = signature.return_annotation

            if return_annotation != inspect.Signature.empty:
                # Try to get full type hints for better resolution
                type_hints = get_type_hints(tool_or_callable)
                return_type = type_hints.get("return", return_annotation)

                # If it's already a BaseModel, return it
                if inspect.isclass(return_type) and issubclass(return_type, BaseModel):
                    return return_type

                # Create a simple schema with the return type
                return create_model(
                    schema_name,
                    output=(return_type, Field(description="Function output")),
                )

        except Exception as e:
            logger.warning(f"Could not extract output schema: {e}")

    return None


def create_tool_schemas(
    tool_or_callable: Union[Callable, Any],
    input_schema_name: Optional[str] = None,
    output_schema_name: Optional[str] = None,
    include_docstring: bool = True,
    strict_typing: bool = False,
    include_signature: bool = True,
) -> Dict[str, Optional[Type[BaseModel]]]:
    """
    Create both input and output schemas for a tool or callable.

    Args:
        tool_or_callable: The callable or tool to extract schemas from
        input_schema_name: Optional name for the input schema class
        output_schema_name: Optional name for the output schema class
        include_docstring: Whether to extract descriptions from docstrings
        strict_typing: Whether to be strict about type annotations
        include_signature: Whether to store the original function signature

    Returns:
        Dictionary with 'input' and 'output' schema classes
    """
    input_schema = extract_input_schema(
        tool_or_callable,
        input_schema_name,
        include_docstring,
        strict_typing,
        include_signature,
    )

    output_schema = extract_output_schema(
        tool_or_callable, output_schema_name, include_docstring
    )

    return {"input": input_schema, "output": output_schema}


def invoke_from_schema(schema_instance: BaseModel, **extra_kwargs) -> Any:
    """
    Invoke the original callable using a schema instance.

    This function uses the stored signature information to properly
    invoke the original callable with the validated input data.

    Args:
        schema_instance: Instance of a schema created by extract_input_schema
        **extra_kwargs: Additional keyword arguments to pass to the callable

    Returns:
        Result of calling the original function

    Example:
        ```python
        Schema = extract_input_schema(my_function)
        input_data = Schema(name="John", age=30)
        result = invoke_from_schema(input_data)
        ```
    """
    schema_class = type(schema_instance)

    if not hasattr(schema_class, "__signature_info__"):
        raise ValueError(
            "Schema does not contain signature information. "
            "Ensure include_signature=True was used during extraction."
        )

    sig_info = schema_class.__signature_info__
    callable_func = sig_info.get("callable")
    signature = sig_info.get("signature")

    if callable_func is None:
        raise ValueError("No callable function found in signature info")

    # Convert schema instance to dict
    input_dict = schema_instance.model_dump()

    # Merge with extra kwargs
    input_dict.update(extra_kwargs)

    # If we have signature info, use it to call properly
    if signature:
        try:
            # Bind arguments to signature to validate
            bound_args = signature.bind(**input_dict)
            bound_args.apply_defaults()

            # Call the function with bound arguments
            return callable_func(*bound_args.args, **bound_args.kwargs)
        except TypeError as e:
            logger.error(f"Failed to bind arguments to signature: {e}")
            # Fallback to direct call
            return callable_func(**input_dict)
    else:
        # Direct call if no signature available
        return callable_func(**input_dict)


def get_signature_info(schema_class: Type[BaseModel]) -> Optional[Dict[str, Any]]:
    """
    Get stored signature information from a schema class.

    Args:
        schema_class: Schema class created by extract_input_schema

    Returns:
        Dictionary containing signature information, or None if not available
    """
    return getattr(schema_class, "__signature_info__", None)


def create_structured_tool_from_callable(
    callable_func: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
    extract_schema: bool = True,
) -> Optional[Any]:
    """
    Create a LangChain StructuredTool from a callable.

    Args:
        callable_func: The function to wrap
        name: Optional tool name (defaults to function name)
        description: Optional tool description (defaults to docstring)
        extract_schema: Whether to extract and use schema for args_schema

    Returns:
        StructuredTool instance or None if LangChain not available
    """
    if not LANGCHAIN_AVAILABLE or StructuredTool is None:
        logger.warning("LangChain not available, cannot create StructuredTool")
        return None

    # Get name
    tool_name = name or getattr(callable_func, "__name__", "unknown_tool")

    # Get description
    tool_description = description or getattr(
        callable_func, "__doc__", f"Tool: {tool_name}"
    )
    if tool_description:
        tool_description = tool_description.strip()

    # Extract schema if requested
    args_schema = None
    if extract_schema:
        try:
            args_schema = extract_input_schema(callable_func, f"{tool_name}Args")
        except Exception as e:
            logger.warning(f"Could not extract schema for {tool_name}: {e}")

    # Create the tool
    try:
        if args_schema:
            return StructuredTool.from_function(
                func=callable_func,
                name=tool_name,
                description=tool_description,
                args_schema=args_schema,
            )
        else:
            return StructuredTool.from_function(
                func=callable_func, name=tool_name, description=tool_description
            )
    except Exception as e:
        logger.error(f"Failed to create StructuredTool for {tool_name}: {e}")
        return None


def create_goal_tool_node(
    goal_schemas: List[Type[BaseModel]],
    executor_function: Callable,
    executor_name: Optional[str] = None,
) -> Optional[Any]:
    """
    Create a ToolNode for "goal tools" pattern.

    This creates a ToolNode where:
    1. Each goal schema becomes a StructuredTool that calls the executor
    2. The executor receives the structured data and handles the actual work

    Args:
        goal_schemas: List of Pydantic models representing different goals/actions
        executor_function: Function that executes the actual work
        executor_name: Optional name for the executor (defaults to function name)

    Returns:
        ToolNode instance or None if LangChain not available

    Example:
        ```python
        class SearchQueries(BaseModel):
            search_queries: List[str]

        class AnswerQuestion(BaseModel):
            answer: str
            sources: List[str]

        def execute_goal(goal_data, **kwargs):
            if isinstance(goal_data, SearchQueries):
                return search_function(goal_data.search_queries)
            elif isinstance(goal_data, AnswerQuestion):
                return answer_function(goal_data.answer, goal_data.sources)

        tool_node = create_goal_tool_node(
            [SearchQueries, AnswerQuestion],
            execute_goal
        )
        ```
    """
    if not LANGCHAIN_AVAILABLE or ToolNode is None:
        logger.warning("LangChain not available, cannot create ToolNode")
        return None

    executor_name = executor_name or getattr(
        executor_function, "__name__", "execute_goal"
    )
    tools = []

    for schema_class in goal_schemas:
        schema_name = schema_class.__name__

        # Create a wrapper function that converts the schema to the expected format
        def create_wrapper(schema_cls):
            def wrapper(**kwargs):
                # Convert kwargs to schema instance
                try:
                    goal_instance = schema_cls(**kwargs)
                    # Call executor with the goal instance
                    return executor_function(goal_instance, **kwargs)
                except Exception as e:
                    logger.error(f"Error executing goal {schema_cls.__name__}: {e}")
                    return f"Error: {str(e)}"

            # Copy metadata
            wrapper.__name__ = f"execute_{schema_cls.__name__.lower()}"
            wrapper.__doc__ = f"Execute {schema_cls.__name__} goal"

            return wrapper

        # Create wrapper for this schema
        goal_wrapper = create_wrapper(schema_class)

        # Create StructuredTool with the schema as args_schema
        try:
            tool = StructuredTool.from_function(
                func=goal_wrapper,
                name=schema_name,
                description=f"Execute {schema_name} action",
                args_schema=schema_class,
            )
            tools.append(tool)
        except Exception as e:
            logger.error(f"Failed to create tool for {schema_name}: {e}")

    if not tools:
        logger.error("No tools created for goal tool node")
        return None

    # Create and return ToolNode
    try:
        return ToolNode(tools)
    except Exception as e:
        logger.error(f"Failed to create ToolNode: {e}")
        return None


def create_batch_goal_tool_node(
    goal_schemas: List[Type[BaseModel]],
    batch_executor_function: Callable,
    executor_name: Optional[str] = None,
) -> Optional[Any]:
    """
    Create a ToolNode for batch "goal tools" pattern like the tavily example.

    This creates a ToolNode where multiple goal schemas can share the same
    underlying batch executor function.

    Args:
        goal_schemas: List of Pydantic models representing different goals
        batch_executor_function: Function that can handle batch operations
        executor_name: Optional name for the executor

    Returns:
        ToolNode instance or None if LangChain not available

    Example:
        ```python
        class SearchQueries(BaseModel):
            search_queries: List[str]

        class ReviseAnswer(BaseModel):
            search_queries: List[str]

        def run_queries(search_queries: List[str], **kwargs):
            return tavily_tool.batch([{"query": query} for query in search_queries])

        tool_node = create_batch_goal_tool_node(
            [SearchQueries, ReviseAnswer],
            run_queries
        )
        ```
    """
    if not LANGCHAIN_AVAILABLE or ToolNode is None:
        logger.warning("LangChain not available, cannot create ToolNode")
        return None

    tools = []

    for schema_class in goal_schemas:
        schema_name = schema_class.__name__

        # Create StructuredTool that uses the schema name and calls batch executor
        try:
            tool = StructuredTool.from_function(
                func=batch_executor_function,
                name=schema_name,
                description=f"Execute {schema_name} batch operation",
                args_schema=schema_class,
            )
            tools.append(tool)
        except Exception as e:
            logger.error(f"Failed to create batch tool for {schema_name}: {e}")

    if not tools:
        logger.error("No tools created for batch goal tool node")
        return None

    # Create and return ToolNode
    try:
        return ToolNode(tools)
    except Exception as e:
        logger.error(f"Failed to create batch ToolNode: {e}")
        return None


# Example usage and testing
if __name__ == "__main__":
    # Test with a regular function
    def search_documents(
        query: str, limit: int = 10, include_metadata: bool = True
    ) -> List[str]:
        """Search for documents matching a query.

        Args:
            query: The search query string
            limit: Maximum number of results to return
            include_metadata: Whether to include document metadata

        Returns:
            List of matching document titles
        """
        return [f"Document {i}" for i in range(limit)]

    # Extract schema
    SearchSchema = extract_input_schema(search_documents)
    print("Generated schema fields:")
    for name, field_info in SearchSchema.model_fields.items():
        print(f"  {name}: {field_info.annotation} = {field_info.default}")
        if field_info.description:
            print(f"    Description: {field_info.description}")

    # Test creating an instance
    search_input = SearchSchema(query="test query", limit=5)
    print(f"\nExample usage: {search_input}")

    # Test schemas creation with signature
    schemas = create_tool_schemas(search_documents, include_signature=True)
    print(f"\nInput schema: {schemas['input']}")
    print(f"Output schema: {schemas['output']}")

    # Test signature info
    sig_info = get_signature_info(schemas["input"])
    if sig_info:
        print(f"\nSignature info available:")
        print(f"  Parameter count: {sig_info.get('parameter_count', 'N/A')}")
        print(f"  Required params: {sig_info.get('required_params', [])}")
        print(f"  Optional params: {sig_info.get('optional_params', [])}")

    # Test goal tool node creation
    print(f"\n{'='*50}")
    print("Testing Goal Tool Node Creation")
    print(f"{'='*50}")

    # Define some goal schemas
    class SearchQueries(BaseModel):
        search_queries: List[str] = Field(
            description="List of search queries to execute"
        )

    class AnswerQuestion(BaseModel):
        answer: str = Field(description="The answer to provide")
        sources: List[str] = Field(
            default_factory=list, description="Sources for the answer"
        )

    # Define executor function
    def execute_search_goal(goal_data, **kwargs):
        """Execute search-related goals."""
        if isinstance(goal_data, SearchQueries):
            print(f"Executing search queries: {goal_data.search_queries}")
            return f"Search results for: {', '.join(goal_data.search_queries)}"
        elif isinstance(goal_data, AnswerQuestion):
            print(f"Providing answer: {goal_data.answer}")
            return f"Answer: {goal_data.answer} (Sources: {goal_data.sources})"
        return "Unknown goal type"

    # Create goal tool node
    if LANGCHAIN_AVAILABLE:
        goal_tool_node = create_goal_tool_node(
            [SearchQueries, AnswerQuestion], execute_search_goal
        )
        print(f"Goal tool node created: {goal_tool_node is not None}")

        # Test batch version too
        def run_queries(search_queries: List[str], **kwargs):
            """Run the generated queries."""
            print(f"Batch executing queries: {search_queries}")
            return [f"Result for: {query}" for query in search_queries]

        batch_tool_node = create_batch_goal_tool_node(
            [SearchQueries, AnswerQuestion], run_queries
        )
        print(f"Batch goal tool node created: {batch_tool_node is not None}")
    else:
        print("LangChain not available, skipping goal tool node creation")
