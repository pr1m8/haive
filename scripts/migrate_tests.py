#!/usr/bin/env python3
"""Script to migrate test files to the correct package structure.

This script helps reorganize test files from scattered locations to the proper
packages/haive-*/tests/ structure.
"""

from pathlib import Path
import shutil


# Define test file patterns
TEST_PATTERNS = ["test_*.py", "*_test.py", "tests.py"]

# Root directory
ROOT_DIR = Path(__file__).parent.parent

# Mapping of test files to their target locations
TEST_MIGRATIONS = {
    # Root tests directory -> package tests
    "tests/test_agent_interactions.py": "packages/haive-agents/tests/integration/test_agent_interactions.py",
    "tests/test_schema_message_passing.py": "packages/haive-core/tests/unit/test_schema_message_passing.py",
    "tests/test_semantic_scholar_loader.py": "packages/haive-core/tests/unit/engine/document/test_semantic_scholar_loader.py",
    "tests/test_storm_wiki_runner.py": "packages/haive-agents/tests/integration/research/test_storm_wiki_runner.py",
    "tests/test_tokenization.py": "packages/haive-core/tests/unit/test_tokenization.py",

    # Source directory tests -> package tests
    "packages/haive-games/src/haive/games/poker/test_poker_actions.py": "packages/haive-games/tests/unit/poker/test_poker_actions.py",
    "packages/haive-games/src/haive/games/mafia/test.py": "packages/haive-games/tests/unit/mafia/test_mafia.py",
    "packages/haive-dataflow/src/haive/dataflow/db/api/test_api.py": "packages/haive-dataflow/tests/unit/db/api/test_api.py",

    # Scattered test files
    "test_improved_subgraph_visualization.py": "packages/haive-core/tests/unit/visualization/test_improved_subgraph_visualization.py",
    "test_schema_optional.py": "packages/haive-core/tests/unit/test_schema_optional.py",
    "test_subgraph_visualization.py": "packages/haive-core/tests/unit/visualization/test_subgraph_visualization.py",
}


def find_test_files() -> list[Path]:
    """Find all test files in the project."""
    test_files = []

    # Only look in specific directories
    search_dirs = [
        ROOT_DIR / "tests",
        ROOT_DIR / "packages" / "haive-core" / "src",
        ROOT_DIR / "packages" / "haive-agents" / "src",
        ROOT_DIR / "packages" / "haive-tools" / "src",
        ROOT_DIR / "packages" / "haive-games" / "src",
        ROOT_DIR / "packages" / "haive-dataflow" / "src",
        ROOT_DIR / "packages" / "haive-prebuilt" / "src",
        ROOT_DIR / "packages" / "haive-mcp" / "src",
        ROOT_DIR,  # Root level test files
    ]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for pattern in TEST_PATTERNS:
            if search_dir == ROOT_DIR:
                # Only check root level, not recursive
                test_files.extend(search_dir.glob(pattern))
            else:
                test_files.extend(search_dir.rglob(pattern))

    # Filter out already correct locations and unwanted directories
    filtered_files = []
    for file in test_files:
        try:
            relative_path = file.relative_to(ROOT_DIR)
            path_str = str(relative_path)

            # Skip if already in correct location
            if path_str.startswith("packages/") and "/tests/" in path_str and "/src/" not in path_str:
                continue

            # Skip unwanted directories
            skip_patterns = [
                "build/", "__pycache__", ".tox", ".pytest_cache",
                ".venv/", "venv/", ".git/", "node_modules/",
                ".history/", "temp/", "tmp/", ".eggs/"
            ]
            if any(skip in path_str for skip in skip_patterns):
                continue

            filtered_files.append(file)
        except ValueError:
            # Skip files not under ROOT_DIR
            continue

    return filtered_files


def get_package_for_test(test_file: Path) -> str:
    """Determine which package a test file belongs to."""
    try:
        content = test_file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        try:
            content = test_file.read_text(encoding="latin-1")
        except:
            # If we can't read the file, guess from path
            path_str = str(test_file)
            if "agents" in path_str:
                return "haive-agents"
            if "games" in path_str:
                return "haive-games"
            if "tools" in path_str:
                return "haive-tools"
            if "dataflow" in path_str:
                return "haive-dataflow"
            if "prebuilt" in path_str:
                return "haive-prebuilt"
            if "mcp" in path_str:
                return "haive-mcp"
            return "haive-core"

    # Check imports and path to determine package
    path_str = str(test_file)

    # Check path first for better accuracy
    if "/agents/" in path_str or "test_react" in path_str or "test_simple_agent" in path_str:
        return "haive-agents"
    if "/tools/" in path_str or "test_corporate_bs" in path_str or "/toolkits/" in path_str:
        return "haive-tools"
    if "/games/" in path_str:
        return "haive-games"

    # Then check imports
    if "from haive.agents" in content or "import haive.agents" in content:
        return "haive-agents"
    if "from haive.games" in content or "import haive.games" in content:
        return "haive-games"
    if "from haive.tools" in content or "import haive.tools" in content:
        return "haive-tools"
    if "from haive.dataflow" in content or "import haive.dataflow" in content:
        return "haive-dataflow"
    if "from haive.prebuilt" in content or "import haive.prebuilt" in content:
        return "haive-prebuilt"
    if "from haive.mcp" in content or "import haive.mcp" in content:
        return "haive-mcp"
    # Default to core
    return "haive-core"


def create_test_directories():
    """Create necessary test directory structure."""
    packages = ["haive-core", "haive-agents", "haive-tools", "haive-games",
                "haive-dataflow", "haive-prebuilt", "haive-mcp"]

    subdirs = ["unit", "integration", "fixtures", "conftest.py"]

    for package in packages:
        package_test_dir = ROOT_DIR / "packages" / package / "tests"
        package_test_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        for subdir in subdirs[:-1]:  # Skip conftest.py
            (package_test_dir / subdir).mkdir(exist_ok=True)

        # Create conftest.py if it doesn't exist
        conftest_file = package_test_dir / "conftest.py"
        if not conftest_file.exists():
            conftest_file.write_text(f'"""Pytest configuration for {package} tests."""\n')

        # Create __init__.py files
        (package_test_dir / "__init__.py").touch(exist_ok=True)
        (package_test_dir / "unit" / "__init__.py").touch(exist_ok=True)
        (package_test_dir / "integration" / "__init__.py").touch(exist_ok=True)


def migrate_test_file(source: Path, target: Path, dry_run: bool = True):
    """Migrate a single test file."""
    if dry_run:
        print(f"Would move: {source} -> {target}")
    else:
        # Create target directory
        target.parent.mkdir(parents=True, exist_ok=True)

        # Move file
        shutil.move(str(source), str(target))
        print(f"Moved: {source} -> {target}")


def main(dry_run: bool = True):
    """Main migration function."""
    print("Haive Test Migration Script")
    print("=" * 50)

    if dry_run:
        print("DRY RUN MODE - No files will be moved")
    else:
        print("LIVE MODE - Files will be moved")

    print("\n1. Creating test directory structure...")
    create_test_directories()

    print("\n2. Finding test files to migrate...")
    test_files = find_test_files()
    print(f"Found {len(test_files)} test files to analyze")

    print("\n3. Processing predefined migrations...")
    for source_str, target_str in TEST_MIGRATIONS.items():
        source = ROOT_DIR / source_str
        target = ROOT_DIR / target_str

        if source.exists():
            migrate_test_file(source, target, dry_run)

    print("\n4. Processing remaining test files...")
    for test_file in test_files:
        relative_path = test_file.relative_to(ROOT_DIR)

        # Skip if already in migrations
        if str(relative_path) in TEST_MIGRATIONS:
            continue

        # Determine package
        package = get_package_for_test(test_file)

        # Determine if unit or integration test
        test_type = "integration" if "integration" in test_file.name else "unit"

        # Create target path
        target = ROOT_DIR / "packages" / package / "tests" / test_type / test_file.name

        migrate_test_file(test_file, target, dry_run)

    print("\n5. Cleanup empty directories...")
    if not dry_run:
        # Remove empty test directories
        for empty_dir in ["tests", "test", "testing"]:
            dir_path = ROOT_DIR / empty_dir
            if dir_path.exists() and not any(dir_path.iterdir()):
                dir_path.rmdir()
                print(f"Removed empty directory: {dir_path}")

    print("\nMigration complete!")

    if dry_run:
        print("\nTo perform the actual migration, run:")
        print("python scripts/migrate_tests.py --no-dry-run")


if __name__ == "__main__":
    import sys
    dry_run = "--no-dry-run" not in sys.argv
    main(dry_run)
