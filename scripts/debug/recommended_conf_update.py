#!/usr/bin/env python3
"""Generate recommended conf.py update for nitpick_ignore."""

# Recommended high-impact additions to your current nitpick_ignore list
from __future__ import annotations

RECOMMENDED_ADDITIONS = [
    # === HIGH PRIORITY: LangChain Core Types ===
    ("py:class", "langchain_core.documents.Document"),
    ("py:class", "langchain_core.messages.BaseMessage"),
    ("py:class", "langchain_core.messages.HumanMessage"),
    ("py:class", "langchain_core.messages.AIMessage"),
    ("py:class", "langchain_core.messages.SystemMessage"),
    ("py:class", "langchain_core.messages.ToolMessage"),
    ("py:class", "langchain_core.messages.ChatMessage"),
    ("py:class", "langchain_core.messages.FunctionMessage"),
    ("py:class", "langchain_core.tools.BaseTool"),
    ("py:class", "langchain_core.tools.Tool"),
    ("py:class", "langchain_core.tools.StructuredTool"),
    ("py:class", "langchain_core.language_models.BaseLanguageModel"),
    ("py:class", "langchain_core.language_models.llms.BaseLLM"),
    ("py:class", "langchain_core.language_models.chat_models.BaseChatModel"),
    ("py:class", "langchain_core.retrievers.BaseRetriever"),
    ("py:class", "langchain_core.vectorstores.VectorStore"),
    ("py:class", "langchain_core.embeddings.Embeddings"),
    ("py:class", "langchain_core.prompts.BasePromptTemplate"),
    ("py:class", "langchain_core.prompts.PromptTemplate"),
    ("py:class", "langchain_core.prompts.ChatPromptTemplate"),
    ("py:class", "langchain_core.output_parsers.BaseOutputParser"),
    ("py:class", "langchain_core.runnables.Runnable"),
    ("py:class", "langchain_core.runnables.RunnableConfig"),
    ("py:class", "langchain_core.callbacks.BaseCallbackHandler"),
    ("py:class", "langchain_core.exceptions.OutputParserException"),
    # === HIGH PRIORITY: LangGraph Types ===
    ("py:class", "StateGraph"),
    ("py:class", "langgraph.graph.StateGraph"),
    ("py:class", "langgraph.graph.MessageGraph"),
    ("py:class", "langgraph.graph.CompiledGraph"),
    ("py:class", "langgraph.checkpoint.base.BaseCheckpointSaver"),
    ("py:class", "langgraph.checkpoint.memory.MemorySaver"),
    ("py:class", "langgraph.constants.START"),
    ("py:class", "langgraph.constants.END"),
    # === HIGH PRIORITY: Enhanced Pydantic Types ===
    ("py:class", "pydantic.ValidationError"),
    ("py:class", "pydantic.BaseSettings"),
    ("py:class", "pydantic_settings.BaseSettings"),
    ("py:class", "pydantic.field_validator"),
    ("py:class", "pydantic.model_validator"),
    ("py:class", "pydantic.EmailStr"),
    ("py:class", "pydantic.HttpUrl"),
    ("py:class", "pydantic.PositiveInt"),
    ("py:class", "pydantic.StrictStr"),
    ("py:class", "pydantic.UUID4"),
    # === MEDIUM PRIORITY: Advanced Typing ===
    ("py:class", "ClassVar"),
    ("py:class", "Final"),
    ("py:class", "Annotated"),
    ("py:class", "Iterator"),
    ("py:class", "Iterable"),
    ("py:class", "AsyncIterator"),
    ("py:class", "AsyncIterable"),
    ("py:class", "Awaitable"),
    ("py:class", "Coroutine"),
    ("py:class", "Sequence"),
    ("py:class", "MutableSequence"),
    ("py:class", "Mapping"),
    ("py:class", "MutableMapping"),
    ("py:class", "typing_extensions.Self"),
    ("py:class", "typing_extensions.Annotated"),
    ("py:class", "typing_extensions.Literal"),
    # === MEDIUM PRIORITY: Collections & Async ===
    ("py:class", "collections.abc.Mapping"),
    ("py:class", "collections.abc.MutableMapping"),
    ("py:class", "collections.abc.Sequence"),
    ("py:class", "collections.abc.Iterator"),
    ("py:class", "collections.OrderedDict"),
    ("py:class", "collections.defaultdict"),
    ("py:class", "asyncio.Future"),
    ("py:class", "asyncio.Task"),
    ("py:class", "asyncio.Event"),
    ("py:class", "asyncio.Queue"),
    ("py:class", "pathlib.Path"),
    # === HAIVE-SPECIFIC TYPES (add based on your usage) ===
    ("py:class", "BaseAgent"),
    ("py:class", "MultiAgent"),
    ("py:class", "ReactAgent"),
    ("py:class", "SimpleAgent"),
    ("py:class", "StateSchema"),
    ("py:class", "MetaStateSchema"),
    ("py:class", "AugLLMConfig"),
    ("py:class", "BaseEngineConfig"),
    ("py:class", "VectorStoreConfig"),
    ("py:class", "EmbeddingConfig"),
    ("py:class", "HuggingFaceEmbeddingConfig"),
    ("py:class", "RecompileMixin"),
    ("py:class", "RetrieverMixin"),
    # === GENERIC TYPE VARIABLES ===
    ("py:class", "K"),
    ("py:class", "V"),
    ("py:class", "P"),
    ("py:class", "R"),
    ("py:class", "S"),
    ("py:class", "U"),
    ("py:class", "TState"),
    ("py:class", "TConfig"),
    ("py:class", "TModel"),
    ("py:class", "TEngine"),
    ("py:class", "_T"),
    ("py:class", "_K"),
    ("py:class", "_V"),
    ("py:class", "~T"),
    ("py:class", "~K"),
    ("py:class", "~V"),
    # === FUNCTION REFERENCES ===
    ("py:func", "tool"),
    ("py:func", "langchain_core.tools.tool"),
    # === METHOD REFERENCES ===
    ("py:meth", "BaseModel.model_validate"),
    ("py:meth", "BaseModel.model_dump"),
    ("py:meth", "BaseModel.model_copy"),
    ("py:meth", "Agent.run"),
    ("py:meth", "Agent.arun"),
    ("py:meth", "Agent.invoke"),
    ("py:meth", "Agent.ainvoke"),
    # === EXCEPTION REFERENCES ===
    ("py:exc", "ValidationError"),
    ("py:exc", "pydantic.ValidationError"),
    ("py:exc", "NotImplementedError"),
    ("py:exc", "FileNotFoundError"),
    ("py:exc", "ImportError"),
    ("py:exc", "ModuleNotFoundError"),
]


def generate_conf_py_snippet():
    """Generate the conf.py snippet to replace current nitpick_ignore."""

    lines = [
        "# Enhanced nitpick_ignore list for Haive documentation",
        "# Reduces type reference warnings while maintaining useful error detection",
        "nitpicky = True  # Enable nitpicky mode to catch all reference issues",
        "nitpick_ignore = [",
    ]

    # Add existing entries (from current conf.py)
    current_entries = [
        "    # Basic Python types that don't need cross-references",
        '    ("py:class", "str"),',
        '    ("py:class", "int"),',
        '    ("py:class", "bool"),',
        '    ("py:class", "float"),',
        '    ("py:class", "list"),',
        '    ("py:class", "dict"),',
        '    ("py:class", "tuple"),',
        '    ("py:class", "set"),',
        '    ("py:class", "bytes"),',
        '    ("py:class", "None"),',
        '    ("py:class", "type"),',
        '    ("py:class", "object"),',
        "",
        "    # Common typing module types",
        '    ("py:class", "Any"),',
        '    ("py:class", "List"),',
        '    ("py:class", "Dict"),',
        '    ("py:class", "Tuple"),',
        '    ("py:class", "Set"),',
        '    ("py:class", "Optional"),',
        '    ("py:class", "Union"),',
        '    ("py:class", "Callable"),',
        '    ("py:class", "Type"),',
        '    ("py:class", "TypeVar"),',
        '    ("py:class", "Generic"),',
        '    ("py:class", "Literal"),',
        '    ("py:class", "Protocol"),',
        '    ("py:class", "TypedDict"),',
        "",
        "    # Pydantic types",
        '    ("py:class", "BaseModel"),',
        '    ("py:class", "Field"),',
        '    ("py:class", "SecretStr"),',
        '    ("py:class", "ConfigDict"),',
        "",
        "    # datetime types",
        '    ("py:class", "datetime.datetime"),',
        '    ("py:class", "datetime.date"),',
        '    ("py:class", "datetime.time"),',
        '    ("py:class", "datetime.timedelta"),',
        "",
        "    # Common missing classes",
        '    ("py:class", "Document"),',
        '    ("py:class", "BaseMessage"),',
        '    ("py:class", "HumanMessage"),',
        '    ("py:class", "AIMessage"),',
        '    ("py:class", "SystemMessage"),',
        '    ("py:class", "ToolMessage"),',
        "",
        "    # Ignore some specific references that are causing issues",
        '    ("py:class", "T"),',
        '    ("py:class", "Agent"),',
        '    ("py:class", "TIn"),',
        '    ("py:class", "TOut"),',
        '    ("py:class", "InvokableEngine"),',
        "",
        "    # === ENHANCED ADDITIONS FOR BETTER COVERAGE ===",
        "",
    ]

    lines.extend(current_entries)

    # Group new additions by category
    for ref_type, target in RECOMMENDED_ADDITIONS:
        # Skip if already in current list
        if (ref_type, target) in [
            ("py:class", "Document"),
            ("py:class", "BaseMessage"),
            ("py:class", "HumanMessage"),
            ("py:class", "AIMessage"),
            ("py:class", "SystemMessage"),
            ("py:class", "ToolMessage"),
            ("py:class", "T"),
            ("py:class", "Agent"),
            ("py:class", "TIn"),
            ("py:class", "TOut"),
            ("py:class", "InvokableEngine"),
        ]:
            continue

        lines.append(f'    ("{ref_type}", "{target}"),')

    lines.append("]")

    return "\n".join(lines)


def generate_incremental_addition():
    """Generate just the new entries to add to existing list."""

    lines = [
        "",
        "    # === ENHANCED ADDITIONS - Add these to your existing nitpick_ignore list ===",
        "",
    ]

    for ref_type, target in RECOMMENDED_ADDITIONS:
        lines.append(f'    ("{ref_type}", "{target}"),')

    return "\n".join(lines)


def main():
    """Generate both full replacement and incremental addition."""

    print("🎯 Recommended nitpick_ignore Configuration Update")
    print("=" * 60)
    print()
    print("📊 Analysis:")
    print("  - Current list: ~45 entries")
    print(f"  - Recommended additions: {len(RECOMMENDED_ADDITIONS)} entries")
    print("  - Focus: High-impact LangChain, Pydantic, and typing references")
    print()

    # Save full replacement
    full_config = generate_conf_py_snippet()
    Path("recommended_full_nitpick_ignore.py").write_text(full_config)

    # Save incremental addition
    incremental = generate_incremental_addition()
    Path("recommended_incremental_additions.txt").write_text(incremental)

    print("📁 Files generated:")
    print("  1. recommended_full_nitpick_ignore.py - Complete replacement")
    print("  2. recommended_incremental_additions.txt - Add to existing list")
    print()

    print("🚀 Implementation Options:")
    print()
    print("  Option A - Full Replacement (Recommended):")
    print(
        "    Replace your entire nitpick_ignore list with recommended_full_nitpick_ignore.py",
    )
    print()
    print("  Option B - Incremental Addition:")
    print(
        "    Add the entries from recommended_incremental_additions.txt to your current list",
    )
    print()
    print("  Option C - Gradual Implementation:")
    print("    Add high-priority LangChain entries first, then test")
    print()

    # Show high priority sample
    print("📝 High Priority Entries (LangChain Core):")
    priority_count = 0
    for ref_type, target in RECOMMENDED_ADDITIONS:
        if "langchain_core" in target and priority_count < 10:
            print(f'    ("{ref_type}", "{target}"),')
            priority_count += 1

    print()
    print("⚡ Quick Test:")
    print("  After updating, run: nox -s docs_fast")
    print("  Look for 'reference target not found' warnings")


if __name__ == "__main__":
    from pathlib import Path

    main()
