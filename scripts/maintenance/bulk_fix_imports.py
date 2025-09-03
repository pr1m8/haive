#!/usr/bin/env python3
"""Bulk fix common import errors."""

import re
from collections import defaultdict
from pathlib import Path


def fix_relative_imports(file_path, content):
    """Fix relative imports to absolute imports."""
    fixes = 0
    lines = content.split("\n")
    new_lines = []

    # Determine package context
    package_match = re.search(r"/haive-(\w+)/src/haive/(\w+)", str(file_path))
    if not package_match:
        return content, 0

    package_name = package_match.group(2)

    for line in lines:
        new_line = line

        # Fix relative imports
        if re.match(r"^from \w+[\.\w]* import", line):
            # Extract module name
            match = re.match(r"^from (\w+(?:\.\w+)*) import", line)
            if match:
                module = match.group(1)
                # Check if it's not already an absolute import
                if not module.startswith("haive") and not module.startswith(
                    ("langchain", "pydantic", "typing")
                ):
                    # Try to guess the correct absolute path
                    if module in [
                        "types",
                        "base",
                        "config",
                        "models",
                        "state",
                        "utils",
                    ]:
                        # Common module names - check current directory structure
                        current_dir = file_path.parent
                        if (current_dir / f"{module}.py").exists():
                            # Same directory
                            abs_path = (
                                str(file_path.parent)
                                .replace("/src/", ".")
                                .replace("/", ".")
                            )
                            abs_path = abs_path.split(".haive.")[-1]
                            new_module = f"haive.{abs_path}.{module}"
                            new_line = line.replace(
                                f"from {module} import", f"from {new_module} import"
                            )
                            fixes += 1

        new_lines.append(new_line)

    return "\n".join(new_lines), fixes


def fix_missing_loader_imports(file_path, content):
    """Fix missing loader source imports."""
    fixes = 0

    # Common missing imports
    replacements = {
        "from haive.core.engine.loaders.sources.types import SourceType": "from haive.core.engine.loaders.sources.source_types import SourceType",
        "from haive.core.engine.loaders.sources.local.types import LocalSourceFileType": "from haive.core.engine.loaders.sources.source_types import LocalSourceFileType",
        "from haive.core.engine.loaders.sources.local.base import FileSource": "from haive.core.engine.loaders.sources.source_types import LocalFileSource as FileSource",
        "from haive.core.engine.loaders.sources.remote.base import URLSource": "from haive.core.engine.loaders.sources.source_types import RemoteSource as URLSource",
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            fixes += 1

    return content, fixes


def fix_enhanced_registry_imports(file_path, content):
    """Fix enhanced_registry imports."""
    fixes = 0

    # Fix enhanced_registry imports
    if "from enhanced_registry import" in content:
        content = content.replace(
            "from enhanced_registry import",
            "from haive.core.engine.loaders.sources.enhanced_registry import",
        )
        fixes += 1

    return content, fixes


def fix_source_types_imports(file_path, content):
    """Fix source_types imports."""
    fixes = 0

    # Fix source_types relative imports
    patterns = [
        (
            r"from source_types import (\w+)",
            r"from haive.core.engine.loaders.sources.source_types import \1",
        ),
        (
            r"from sources\.source_types import (\w+)",
            r"from haive.core.engine.loaders.sources.source_types import \1",
        ),
    ]

    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            fixes += 1

    return content, fixes


def process_file(file_path):
    """Process a single file and apply fixes."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        total_fixes = 0

        # Apply fixes
        content, fixes = fix_relative_imports(file_path, content)
        total_fixes += fixes

        content, fixes = fix_missing_loader_imports(file_path, content)
        total_fixes += fixes

        content, fixes = fix_enhanced_registry_imports(file_path, content)
        total_fixes += fixes

        content, fixes = fix_source_types_imports(file_path, content)
        total_fixes += fixes

        # Write back if changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return total_fixes

        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0


def main():
    """Apply bulk fixes to all Python files."""
    print("🔧 Applying bulk import fixes...\n")

    packages_dir = Path(__file__).parent / "packages"
    files_fixed = 0
    total_fixes = 0

    # Process all Python files
    for package in [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
        "haive-prebuilt",
    ]:
        package_src = packages_dir / package / "src"
        if package_src.exists():
            for py_file in package_src.rglob("*.py"):
                fixes = process_file(py_file)
                if fixes > 0:
                    files_fixed += 1
                    total_fixes += fixes
                    print(
                        f"  Fixed {fixes} imports in {py_file.relative_to(packages_dir)}"
                    )

    print(f"\n✅ Summary:")
    print(f"  Files modified: {files_fixed}")
    print(f"  Total fixes applied: {total_fixes}")


if __name__ == "__main__":
    main()
