#!/usr/bin/env python3
"""Prioritized Import Fix Script for Haive Framework.

Based on the comprehensive analysis, this script applies fixes in order of impact:
1. HIGH: Missing __init__.py files
2. HIGH: Relative import fixes
3. MEDIUM: Missing function/class implementations
4. MEDIUM: Pydantic v2 validator fixes

Usage:
    poetry run python scripts/debug/prioritized_import_fixes.py
"""

import re
from pathlib import Path

# Project root
project_root = Path(__file__).parent.parent.parent
packages_root = project_root / "packages"


class ImportFixer:

    def __init__(self):
        self.fixes_applied = []
        self.errors_encountered = []

    def apply_all_fixes(self):
        """Apply all import fixes in priority order."""
        print("🔧 Applying Prioritized Import Fixes")
        print("=" * 50)

        # Priority 1: Missing __init__.py files
        self.fix_missing_init_files()

        # Priority 2: Fix relative import issues
        self.fix_relative_imports()

        # Priority 3: Fix missing function exports
        self.fix_missing_exports()

        # Priority 4: Fix Pydantic v2 validators
        self.fix_pydantic_validators()

        # Priority 5: Create stub implementations for missing modules
        self.create_missing_stubs()

        # Generate report
        self.generate_report()

    def fix_missing_init_files(self):
        """Find and create missing __init__.py files."""
        print("\n1. 🗂️  FIXING MISSING __init__.py FILES")
        print("-" * 40)

        missing_init_dirs = []

        # Find directories without __init__.py that should have them
        for package_dir in packages_root.glob("haive-*"):
            if not package_dir.is_dir():
                continue

            src_dir = package_dir / "src"
            if not src_dir.exists():
                continue

            # Walk all directories in src
            for dirpath in src_dir.rglob("*"):
                if not dirpath.is_dir():
                    continue

                # Skip if it's a __pycache__ directory
                if "__pycache__" in str(dirpath):
                    continue

                # Check if directory has Python files but no __init__.py
                python_files = list(dirpath.glob("*.py"))
                init_file = dirpath / "__init__.py"

                if python_files and not init_file.exists():
                    missing_init_dirs.append(dirpath)

        # Create missing __init__.py files
        for directory in missing_init_dirs[:20]:  # Limit to first 20
            init_file = directory / "__init__.py"
            try:
                # Create basic __init__.py with module docstring
                module_name = directory.name
                relative_path = directory.relative_to(packages_root)

                content = f'''"""
{module_name.replace("_", " ").title()} module.

This module is part of the Haive framework.
Location: {relative_path}
"""

# This __init__.py was auto-generated to fix import issues
'''

                with open(init_file, "w") as f:
                    f.write(content)

                self.fixes_applied.append(
                    f"Created {init_file.relative_to(project_root)}", )
                print(f"✅ Created {init_file.relative_to(project_root)}")

            except Exception as e:
                self.errors_encountered.append(
                    f"Failed to create {init_file}: {e}")
                print(f"❌ Failed to create {init_file}: {e}")

    def fix_relative_imports(self):
        """Fix common relative import patterns."""
        print("\n2. 🔗 FIXING RELATIVE IMPORT ISSUES")
        print("-" * 40)

        # Common problematic patterns from our analysis
        relative_import_fixes = [
            # Multi-agent RAG module
            {
                "file":
                "packages/haive-agents/src/haive/agents/rag/multi_agent_rag/__init__.py",
                "patterns": [
                    (r"from multi_agent_rag",
                     "from haive.agents.rag.multi_agent_rag"),
                ],
            },
            # React agent2 module
            {
                "file":
                "packages/haive-agents/src/haive/agents/react_class/react_agent2/__init__.py",
                "patterns": [
                    (
                        r"from react_agent2",
                        "from haive.agents.react_class.react_agent2",
                    ),
                ],
            },
            # Task analysis module
            {
                "file":
                "packages/haive-agents/src/haive/agents/task_analysis/agent.py",
                "patterns": [
                    (r"from task_analysis", "from haive.agents.task_analysis"),
                ],
            },
        ]

        for fix_info in relative_import_fixes:
            file_path = project_root / fix_info["file"]
            if not file_path.exists():
                continue

            try:
                with open(file_path) as f:
                    content = f.read()

                original_content = content

                # Apply patterns
                for pattern, replacement in fix_info["patterns"]:
                    content = re.sub(pattern, replacement, content)

                # Write back if changed
                if content != original_content:
                    with open(file_path, "w") as f:
                        f.write(content)

                    self.fixes_applied.append(
                        f"Fixed relative imports in {
                            file_path.relative_to(project_root)}", )
                    print(
                        f"✅ Fixed relative imports in {
                            file_path.relative_to(project_root)}", )

            except Exception as e:
                self.errors_encountered.append(
                    f"Failed to fix {file_path}: {e}")
                print(f"❌ Failed to fix {file_path}: {e}")

    def fix_missing_exports(self):
        """Fix missing function/class exports in __init__.py files."""
        print("\n3. 📤 FIXING MISSING EXPORTS")
        print("-" * 40)

        # Based on our analysis, these are commonly missing exports
        missing_exports = [
            # MCTS module missing exports
            {
                "file":
                "packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/models.py",
                "missing_functions": [
                    "as_message",
                    "backpropagate",
                    "best_child_score",
                ],
            },
            # LATS module missing exports
            {
                "file":
                "packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/node.py",
                "missing_functions": ["add_child", "get", "get_path"],
            },
        ]

        for export_info in missing_exports:
            file_path = project_root / export_info["file"]
            if not file_path.exists():
                continue

            try:
                with open(file_path) as f:
                    content = f.read()

                # Add stub implementations for missing functions
                missing_funcs = export_info["missing_functions"]
                stub_implementations = []

                for func_name in missing_funcs:
                    # Check if function already exists
                    if f"def {func_name}" not in content:
                        stub_impl = f'''

def {func_name}(*args, **kwargs):
    """
    Stub implementation for {func_name}.

    This function was auto-generated to fix import issues.
    Please implement the actual functionality.
    """
    raise NotImplementedError(f"{func_name} is not yet implemented")
'''
                        stub_implementations.append(stub_impl)

                if stub_implementations:
                    # Add stubs to end of file
                    content += "\n\n# Auto-generated stub implementations"
                    content += "".join(stub_implementations)

                    with open(file_path, "w") as f:
                        f.write(content)

                    self.fixes_applied.append(
                        f"Added {
                            len(stub_implementations)} stub functions to {
                            file_path.relative_to(project_root)}", )
                    print(
                        f"✅ Added {
                            len(stub_implementations)} stub functions to {
                            file_path.relative_to(project_root)}", )

            except Exception as e:
                self.errors_encountered.append(
                    f"Failed to add stubs to {file_path}: {e}", )
                print(f"❌ Failed to add stubs to {file_path}: {e}")

    def fix_pydantic_validators(self):
        """Fix remaining Pydantic v2 validator issues."""
        print("\n4. 🔍 FIXING PYDANTIC V2 VALIDATORS")
        print("-" * 40)

        # Find files with old Pydantic validator patterns
        for package_dir in packages_root.glob("haive-*"):
            if not package_dir.is_dir():
                continue

            src_dir = package_dir / "src"
            if not src_dir.exists():
                continue

            # Look for Python files with @validator decorators
            for py_file in src_dir.rglob("*.py"):
                try:
                    with open(py_file) as f:
                        content = f.read()

                    # Check for old Pydantic v1 patterns
                    if "@validator(" in content:
                        original_content = content

                        # Replace @validator with @field_validator
                        content = re.sub(r"@validator\(", "@field_validator(",
                                         content)

                        # Add @classmethod decorator if missing
                        lines = content.split("\n")
                        new_lines = []

                        for i, line in enumerate(lines):
                            new_lines.append(line)
                            # If we find @field_validator, ensure next function has
                            # @classmethod
                            if "@field_validator(" in line:
                                # Look ahead to find the function definition
                                for j in range(i + 1, min(i + 3, len(lines))):
                                    if "def " in lines[
                                            j] and "@classmethod" not in lines[
                                                j - 1]:
                                        new_lines.insert(
                                            -1, "    @classmethod")
                                        break

                        content = "\n".join(new_lines)

                        # Add necessary imports
                        if ("from pydantic import field_validator"
                                not in content
                                and "@field_validator" in content):
                            # Find existing pydantic imports
                            if "from pydantic import" in content:
                                content = re.sub(
                                    r"from pydantic import ([^\\n]+)",
                                    r"from pydantic import \1, field_validator",
                                    content,
                                )
                            else:
                                # Add new import
                                content = "from pydantic import field_validator\n" + content

                        # Write back if changed
                        if content != original_content:
                            with open(py_file, "w") as f:
                                f.write(content)

                            self.fixes_applied.append(
                                f"Fixed Pydantic validators in {
                                    py_file.relative_to(project_root)}", )
                            print(
                                f"✅ Fixed Pydantic validators in {
                                    py_file.relative_to(project_root)}", )

                except Exception as e:
                    self.errors_encountered.append(
                        f"Failed to fix Pydantic validators in {py_file}: {e}",
                    )
                    # Don't print every error, too noisy

    def create_missing_stubs(self):
        """Create stub files for commonly missing modules."""
        print("\n5. 📝 CREATING MISSING MODULE STUBS")
        print("-" * 40)

        # Based on our analysis, these modules are frequently missing
        missing_modules = [
            {
                "path":
                "packages/haive-agents/src/haive/agents/chain/declarative_chain.py",
                "content":
                '''"""
Declarative chain module stub.

This module was auto-generated to fix import issues.
"""

class DeclarativeChain:
    """Stub implementation of DeclarativeChain."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("DeclarativeChain not yet implemented")

def complex_rag(*args, **kwargs):
    """Stub implementation of complex_rag function."""
    raise NotImplementedError("complex_rag not yet implemented")
''',
            },
            {
                "path":
                "packages/haive-core/src/haive/core/graph/state_graph/compiled_state_graph.py",
                "content":
                '''"""
Compiled state graph module stub.

This module was auto-generated to fix import issues.
"""

class CompiledStateGraph:
    """Stub implementation of CompiledStateGraph."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("CompiledStateGraph not yet implemented")
''',
            },
            {
                "path":
                "packages/haive-core/src/haive/core/engine/base/agent_types.py",
                "content":
                '''"""
Agent types module stub.

This module was auto-generated to fix import issues.
"""

from enum import Enum

class AgentType(Enum):
    """Stub enum for agent types."""
    SIMPLE = "simple"
    REACT = "react"
    MULTI = "multi"
''',
            },
        ]

        for stub_info in missing_modules:
            file_path = project_root / stub_info["path"]

            # Only create if file doesn't exist
            if not file_path.exists():
                try:
                    # Ensure parent directory exists
                    file_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(file_path, "w") as f:
                        f.write(stub_info["content"])

                    self.fixes_applied.append(
                        f"Created stub module {file_path.relative_to(project_root)}",
                    )
                    print(
                        f"✅ Created stub module {file_path.relative_to(project_root)}",
                    )

                except Exception as e:
                    self.errors_encountered.append(
                        f"Failed to create stub {file_path}: {e}", )
                    print(f"❌ Failed to create stub {file_path}: {e}")

    def generate_report(self):
        """Generate final report of all fixes applied."""
        print("\n📊 IMPORT FIX SUMMARY")
        print("=" * 50)
        print(f"✅ Fixes applied: {len(self.fixes_applied)}")
        print(f"❌ Errors encountered: {len(self.errors_encountered)}")

        if self.fixes_applied:
            print("\n🎯 SUCCESSFUL FIXES:")
            for fix in self.fixes_applied:
                print(f"   ✅ {fix}")

        if self.errors_encountered:
            print("\n⚠️  ERRORS (first 10):")
            for error in self.errors_encountered[:10]:
                print(f"   ❌ {error}")

        print("\n🚀 NEXT STEPS:")
        print("1. Test documentation build:")
        print("   nox -s docs_fast")
        print("\n2. Run import analysis again:")
        print("   poetry run python scripts/debug/find_all_import_issues.py")
        print("\n3. Check specific modules:")
        print(
            "   poetry run python -c 'import haive.agents.chain.declarative_chain'"
        )


def main():
    """Main function to apply all fixes."""
    fixer = ImportFixer()
    fixer.apply_all_fixes()


if __name__ == "__main__":
    main()
