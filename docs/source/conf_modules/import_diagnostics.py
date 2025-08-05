"""Import diagnostics for Sphinx documentation build.

This module provides functionality to diagnose import issues ahead of
time and generate appropriate mock configurations for Sphinx
autosummary.
"""

from __future__ import annotations

from datetime import datetime
import importlib
import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def find_all_python_modules(
    search_paths: list[str],
    base_dir: str | None = None,
) -> set[str]:
    """Find all Python modules in the given search paths."""
    modules = set()

    for search_path in search_paths:
        path = Path(search_path)
        if base_dir and not path.is_absolute():
            # Resolve relative paths from base directory
            path = Path(base_dir) / path
        path = path.resolve()

        if not path.exists():
            logger.warning(f"Path does not exist: {path}")
            continue

        # Find all Python files
        for py_file in path.rglob("*.py"):
            if py_file.name == "__init__.py":
                # Package
                relative_path = py_file.parent.relative_to(path)
                module_name = str(relative_path).replace("/", ".")
                if module_name != ".":
                    modules.add(module_name)
            else:
                # Module
                relative_path = py_file.relative_to(path)
                module_name = str(relative_path.with_suffix("")).replace(
                    "/",
                    ".",
                )
                modules.add(module_name)

    return modules


def test_module_import(module_name: str) -> dict[str, str]:
    """Test if a module can be imported and return details about any issues."""
    result = {
        "module": module_name,
        "status": "unknown",
        "error": None,
        "error_type": None,
    }

    try:
        importlib.import_module(module_name)
        result["status"] = "success"
    except ModuleNotFoundError as e:
        result["status"] = "missing_module"
        result["error"] = str(e)
        result["error_type"] = "ModuleNotFoundError"
    except ImportError as e:
        result["status"] = "import_error"
        result["error"] = str(e)
        result["error_type"] = "ImportError"
    except Exception as e:
        result["status"] = "other_error"
        result["error"] = str(e)
        result["error_type"] = type(e).__name__

    return result


def diagnose_imports(
    autoapi_dirs: list[str],
    base_dir: str | None = None,
    fast_mode: bool = False,
    sample_limit: int = 500,
) -> tuple[dict, set[str]]:
    """Diagnose import issues for Sphinx documentation build."""
    logger.info("🔍 Diagnosing import issues for Sphinx documentation...")

    # Find all modules
    all_modules = set()
    for autoapi_dir in autoapi_dirs:
        modules = find_all_python_modules([autoapi_dir], base_dir)
        all_modules.update(modules)

    logger.info(f"🔍 Found {len(all_modules)} modules to test...")

    # Apply fast mode optimization if enabled
    if fast_mode or len(all_modules) > sample_limit:
        # Sample key modules for faster diagnostics
        sample_modules = set()
        for module in all_modules:
            # Include all top-level packages
            if (
                "." not in module
                or module.count(".") <= 2
                or any(x in module for x in ["examples", "test", "demo", "archive"])
            ):
                sample_modules.add(module)

        if len(sample_modules) < len(all_modules):
            mode_reason = (
                "fast mode enabled" if fast_mode else f"module count exceeds {sample_limit}"
            )
            logger.info(
                f"🚀 Optimizing: Testing {len(sample_modules)} key modules instead of all {
                    len(all_modules)
                } ({mode_reason})",
            )
            all_modules = sample_modules

    # Test each module
    results = {
        "success": [],
        "missing_module": [],
        "import_error": [],
        "other_error": [],
        "timestamp": datetime.now().isoformat(),
        "total_modules": len(all_modules),
    }

    success_count = 0
    for module in sorted(all_modules):
        if module.startswith("_"):  # Skip private modules
            continue

        # Skip modules that cause warnings during import
        if any(
            skip in module
            for skip in [
                "tools.google",
                "tools.tools.google",  # Google tools with API requirements
                "tools.search",  # Search tools with external deps
                "tools.tools.toolkits",  # Toolkits with API requirements
            ]
        ):
            logger.debug(f"⏭️  Skipping {module} (known import issues)")
            continue

        result = test_module_import(module)
        results[result["status"]].append(result)

        if result["status"] == "success":
            success_count += 1
        else:
            logger.warning(
                f"❌ {module}: {result['error_type']} - {result['error']}",
            )

    logger.info("📊 IMPORT DIAGNOSIS COMPLETE")
    logger.info(f"✅ Successful imports: {len(results['success'])}")

    if results["missing_module"]:
        logger.error(f"❌ Missing modules: {len(results['missing_module'])}")
    if results["import_error"]:
        logger.warning(f"⚠️  Import errors: {len(results['import_error'])}")
    if results["other_error"]:
        logger.error(f"🚨 Other errors: {len(results['other_error'])}")

    # Generate mock imports list
    mock_imports = set()

    for result in results["missing_module"] + results["import_error"]:
        # Extract the missing dependency from error message
        error_msg = result["error"]
        if "No module named" in error_msg:
            # Extract module name from "No module named 'module_name'"
            missing_module = error_msg.split("'")[1] if "'" in error_msg else error_msg.split()[-1]
            mock_imports.add(missing_module)

    logger.info(
        f"🎯 Found {len(mock_imports)} modules to mock in Sphinx configuration",
    )

    return results, mock_imports


def save_import_diagnosis(
    results: dict,
    mock_imports: set[str],
    output_dir: str = "docs/logs",
):
    """Save diagnostic results to files for later reference."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save detailed results as JSON
    results_file = output_path / f"import_diagnosis_{timestamp}.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    # Save sphinx configuration snippet
    sphinx_config_file = output_path / f"sphinx_mock_imports_{timestamp}.py"
    with open(sphinx_config_file, "w") as f:
        f.write("# Add this to your conf.py to mock problematic imports\n")
        f.write("autodoc_mock_imports = [\n")
        for module in sorted(mock_imports):
            f.write(f"    '{module}',\n")
        f.write("]\n")

    # Save summary report
    summary_file = output_path / f"import_diagnosis_summary_{timestamp}.md"
    with open(summary_file, "w") as f:
        f.write(f"# Import Diagnosis Report - {timestamp}\n\n")
        f.write("## Summary\n")
        f.write(f"- ✅ Successful imports: {len(results['success'])}\n")
        f.write(f"- ❌ Missing modules: {len(results['missing_module'])}\n")
        f.write(f"- ⚠️  Import errors: {len(results['import_error'])}\n")
        f.write(f"- 🚨 Other errors: {len(results['other_error'])}\n\n")

        f.write("## Modules to Mock\n")
        for module in sorted(mock_imports):
            f.write(f"- `{module}`\n")

        f.write("\n## Failed Imports\n")
        for result in results["missing_module"] + results["import_error"]:
            f.write(
                f"- **{result['module']}**: {result['error_type']} - {result['error']}\n",
            )

    logger.info("📁 Diagnosis results saved to:")
    logger.info(f"  - Detailed results: {results_file}")
    logger.info(f"  - Sphinx config: {sphinx_config_file}")
    logger.info(f"  - Summary report: {summary_file}")

    return results_file, sphinx_config_file, summary_file


def get_autodoc_mock_imports_from_diagnosis(
    autoapi_dirs: list[str],
    base_dir: str | None = None,
    fast_mode: bool = False,
    sample_limit: int = 500,
) -> list[str]:
    """Get autodoc mock imports by diagnosing current import issues."""
    try:
        results, mock_imports = diagnose_imports(
            autoapi_dirs,
            base_dir,
            fast_mode,
            sample_limit,
        )

        # Save results for reference
        save_import_diagnosis(results, mock_imports)

        # Add comprehensive list of known problematic imports based on diagnostics
        comprehensive_mocks = list(mock_imports) + [
            # Missing modules identified in diagnostics
            "agents",
            "pokebase",
            "google-search-results",
            "serpapi",
            "haive.core.exceptions",
            "haive.core.graph.state_graph.compiled_state_graph",
            "haive.core.engine.base.agent_types",
            "haive.agents.chain.chain_agent",
            "haive.agents.archive.meta.agent",
            "haive.agents.web_nav",
            "haive.agents.chain.chain_examples",
            "haive.agents.simple.agent",
            "haive.agents.common.models.task_analysis.solvability_assessment",
            "iterative_refinement",
            "map_branch",
            "haive.core.engine.document_loader",
            "haive.agents.document_loader",
            "graph_db",
            "haive.agents.multi.simple",
            "haive.agents.multi.agent",
            "haive.core.schema.prebuilt.enhanced_multi_agent_state",
            "search",
            "llm_compiler",
            "plan_and_execute",
            # Missing class/function imports that can't be easily resolved
            "build_graph",
            "compare_to",
            "ComplexityType",
            "ComponentMetadata",
            "create_conversation_state",
            "MessagesState",
            "MemoryType",
            "MultiAgentBase",
            "TypeConverter",
            "compiled_state_graph",
            "agent_types",
            "complex_rag",
            "langgraph_supervisor",
            "usage_examples",
            "normalize_contents",
            # Database and connection pool related
            "BaseConnectionPool",
            "psycopg_pool",
            "psycopg",
            "asyncpg",
            # Optional dependencies that may not be installed
            "langchain_community",
            "langchain_experimental",
            "chromadb",
            "faiss",
            "pinecone",
            "weaviate",
            "qdrant_client",
            "redis",
            "numpy",
            "pandas",
            "matplotlib",
            "seaborn",
            "plotly",
            "streamlit",
            "gradio",
            "jupyter",
            "ipython",
            "notebook",
            # Game and environment specific
            "pygame",
            "gym",
            "gymnasium",
            "pettingzoo",
            # Tools and external APIs
            "requests",
            "httpx",
            "aiohttp",
            "websockets",
            "socketio",
            "celery",
            "dramatiq",
            # Machine learning and AI
            "torch",
            "tensorflow",
            "transformers",
            "openai",
            "anthropic",
            "cohere",
            "huggingface_hub",
            "sentence_transformers",
            # Development and testing
            "pytest",
            "hypothesis",
            "factory_boy",
            "faker",
            "mock",
            "unittest.mock",
        ]

        return sorted(set(comprehensive_mocks))
    except Exception as e:
        logger.exception(f"Failed to diagnose imports: {e}")
        # Return comprehensive fallback list
        return [
            "agents",
            "pokebase",
            "google-search-results",
            "serpapi",
            "haive.core.exceptions",
            "haive.core.graph.state_graph.compiled_state_graph",
            "haive.core.engine.base.agent_types",
            "haive.agents.chain.chain_agent",
            "build_graph",
            "compare_to",
            "ComplexityType",
            "ComponentMetadata",
            "create_conversation_state",
            "compiled_state_graph",
            "agent_types",
            "complex_rag",
            "langgraph_supervisor",
            "usage_examples",
            "normalize_contents",
            "BaseConnectionPool",
            "psycopg_pool",
            "psycopg",
            "asyncpg",
            "langchain_community",
            "chromadb",
            "numpy",
            "pandas",
            "torch",
            "tensorflow",
            "openai",
            "requests",
            "pytest",
        ]
