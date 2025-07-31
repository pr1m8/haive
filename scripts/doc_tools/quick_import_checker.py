#!/usr/bin/env python3
"""Quick Import Checker for Documentation Issues.

A simplified version that quickly identifies problematic modules for documentation.
"""

import importlib
import json
import sys
from datetime import datetime
from pathlib import Path

# Setup paths
workspace_root = Path(__file__).resolve().parents[2]
packages_dir = workspace_root / "packages"
for package_name in [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-prebuilt",
    "haive-mcp",
]:
    package_path = packages_dir / package_name / "src"
    if package_path.exists():
        sys.path.insert(0, str(package_path))


def test_key_modules():
    """Test import of key modules that are referenced in documentation."""
    # Key modules from the documentation that we know were failing
    key_modules = [
        # Agent modules
        "haive.agents.conversation",
        "haive.agents.conversation.base",
        "haive.agents.conversation.debate",
        "haive.agents.conversation.directed",
        "haive.agents.conversation.round_robin",
        "haive.agents.conversation.social_media",
        "haive.agents.conversation.collaberative",
        # RAG modules
        "haive.agents.rag",
        "haive.agents.rag.base",
        "haive.agents.rag.adaptive_rag",
        "haive.agents.rag.filtered",
        "haive.agents.rag.hyde",
        "haive.agents.rag.self_corr",
        "haive.agents.rag.llm_rag",
        "haive.agents.rag.multi_strategy",
        # Core modules
        "haive.core.engine",
        "haive.core.engine.base",
        "haive.core.registry",
        "haive.core.persistence",
        # Tools modules
        "haive.tools.base",
        "haive.tools.general",
        "haive.tools.google",
        "haive.tools.search",
        "haive.tools.content",
        "haive.tools.utility",
        # Games modules
        "haive.games.base",
        "haive.games.framework",
        "haive.games.poker",
        "haive.games.chess",
        "haive.games.mancala",
        "haive.games.tic_tac_toe",
    ]

    results = {
        "timestamp": datetime.now().isoformat(),
        "successful": [],
        "failed": {},
        "missing_dependencies": [],
        "syntax_errors": [],
        "type_errors": [],
        "other_errors": [],
    }


    for i, module_name in enumerate(key_modules, 1):

        try:
            importlib.import_module(module_name)
            results["successful"].append(module_name)
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)

            results["failed"][module_name] = {
                "error_type": error_type,
                "error_message": error_msg,
            }

            # Categorize errors
            if "no module named" in error_msg.lower():
                results["missing_dependencies"].append(module_name)
                # Extract missing dependency
                if "'" in error_msg:
                    missing = error_msg.split("'")[1]
            elif "syntax" in error_msg.lower():
                results["syntax_errors"].append(module_name)
            elif "type" in error_type.lower() or "pydantic" in error_msg.lower():
                results["type_errors"].append(module_name)
            else:
                results["other_errors"].append(module_name)

    return results


def generate_quick_fixes(results):
    """Generate quick fix suggestions."""

    if results["missing_dependencies"]:

        # Extract unique missing dependencies
        missing_deps = set()
        for module in results["missing_dependencies"]:
            error_msg = results["failed"][module]["error_message"]
            if "'" in error_msg:
                dep = error_msg.split("'")[1]
                missing_deps.add(dep)

        for dep in sorted(missing_deps):
            pass

    if results["type_errors"]:
        for module in results["type_errors"]:
            pass

    if results["syntax_errors"]:
        for module in results["syntax_errors"]:
            pass

    if results["other_errors"]:
        for module in results["other_errors"]:
            error_info = results["failed"][module]

    # Success rate
    total = len(results["successful"]) + len(results["failed"])
    success_rate = len(results["successful"]) / total * 100 if total > 0 else 0


    # Recommendation
    if success_rate < 50:
        pass
    elif success_rate < 80:
        passs")
    else:
        passy")


def generate_autosummary_skip_list(results):
    """Generate a list of modules to skip in autosummary."""
    skip_modules = list(results["failed"].keys())

    for module in sorted(skip_modules):
        pass


def save_results(results):
    """Save results to a file."""
    output_dir = workspace_root / "docs" / "import_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"quick_import_check_{timestamp}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)



def main():
    """Run the quick import checker."""

    results = test_key_modules()
    generate_quick_fixes(results)
    generate_autosummary_skip_list(results)
    save_results(results)



if __name__ == "__main__":
    main()
