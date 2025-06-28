#!/usr/bin/env python3
"""Quick Import Checker for Documentation Issues

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

    print("🔍 Testing key modules for documentation issues...")
    print("=" * 80)

    for i, module_name in enumerate(key_modules, 1):
        print(f"[{i:2d}/{len(key_modules)}] {module_name}...", end=" ")

        try:
            importlib.import_module(module_name)
            print("✅")
            results["successful"].append(module_name)
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            print(f"❌ {error_type}")

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
                    print(f"    Missing: {missing}")
            elif "syntax" in error_msg.lower():
                results["syntax_errors"].append(module_name)
            elif "type" in error_type.lower() or "pydantic" in error_msg.lower():
                results["type_errors"].append(module_name)
            else:
                results["other_errors"].append(module_name)

    return results


def generate_quick_fixes(results):
    """Generate quick fix suggestions."""
    print("\n" + "=" * 80)
    print("📋 QUICK FIX RECOMMENDATIONS")
    print("=" * 80)

    if results["missing_dependencies"]:
        print(
            f"\n🔧 MISSING DEPENDENCIES ({len(results['missing_dependencies'])} modules)"
        )
        print("Add these to autodoc_mock_imports in conf.py:")

        # Extract unique missing dependencies
        missing_deps = set()
        for module in results["missing_dependencies"]:
            error_msg = results["failed"][module]["error_message"]
            if "'" in error_msg:
                dep = error_msg.split("'")[1]
                missing_deps.add(dep)

        for dep in sorted(missing_deps):
            print(f"    '{dep}',")

    if results["type_errors"]:
        print(f"\n🔧 TYPE/PYDANTIC ERRORS ({len(results['type_errors'])} modules)")
        print("These modules have Pydantic/typing issues:")
        for module in results["type_errors"]:
            print(f"    - {module}")
        print("Consider checking Generic type annotations and BaseModel inheritance")

    if results["syntax_errors"]:
        print(f"\n🔧 SYNTAX ERRORS ({len(results['syntax_errors'])} modules)")
        print("These modules have syntax issues:")
        for module in results["syntax_errors"]:
            print(f"    - {module}")

    if results["other_errors"]:
        print(f"\n🔧 OTHER ERRORS ({len(results['other_errors'])} modules)")
        for module in results["other_errors"]:
            error_info = results["failed"][module]
            print(
                f"    - {module}: {error_info['error_type']} - {error_info['error_message'][:100]}..."
            )

    # Success rate
    total = len(results["successful"]) + len(results["failed"])
    success_rate = len(results["successful"]) / total * 100 if total > 0 else 0

    print("\n📊 SUMMARY:")
    print(f"    ✅ Working: {len(results['successful'])}/{total} ({success_rate:.1f}%)")
    print(f"    ❌ Broken: {len(results['failed'])}/{total} ({100-success_rate:.1f}%)")

    # Recommendation
    if success_rate < 50:
        print(
            "\n💡 RECOMMENDATION: Keep autosummary disabled until more modules are fixed"
        )
    elif success_rate < 80:
        print("\n💡 RECOMMENDATION: Enable autosummary but exclude problematic modules")
    else:
        print("\n💡 RECOMMENDATION: Most modules working - can re-enable autosummary")


def generate_autosummary_skip_list(results):
    """Generate a list of modules to skip in autosummary."""
    skip_modules = list(results["failed"].keys())

    print("\n🚫 AUTOSUMMARY SKIP LIST:")
    print("Add this to your conf.py:")
    print("```python")
    print("# Modules to skip in autosummary due to import issues")
    print("autosummary_skip_modules = [")
    for module in sorted(skip_modules):
        print(f"    '{module}',")
    print("]")
    print("```")


def save_results(results):
    """Save results to a file."""
    output_dir = workspace_root / "docs" / "import_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"quick_import_check_{timestamp}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {output_file}")


def main():
    """Run the quick import checker."""
    print("🚀 Haive Documentation Import Checker")
    print("=" * 80)

    results = test_key_modules()
    generate_quick_fixes(results)
    generate_autosummary_skip_list(results)
    save_results(results)

    print("\n🎯 Next Steps:")
    print("1. Add missing dependencies to autodoc_mock_imports")
    print("2. Fix syntax and type errors in failing modules")
    print("3. Update autosummary configuration to skip problematic modules")
    print("4. Test documentation build: nox -s docs")


if __name__ == "__main__":
    main()
