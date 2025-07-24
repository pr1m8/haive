#!/usr/bin/env python3
"""Clean up documentation structure and build docs properly."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def cleanup_docs_structure():
    """Clean up the messy docs structure."""
    docs_dir = Path(__file__).parent

    # Create archive directory for old files
    archive_dir = docs_dir / "archive_old_docs"
    archive_dir.mkdir(exist_ok=True)

    # Files and directories to archive (move out of main docs)
    to_archive = [
        "SESSION_MEMORY_COMPLETE_2025_07_18.md",
        "comprehensive_import_analysis.md",
        "remaining_issues_status.md",
        "DOCUMENTATION_ISSUES_AUDIT.md",
        "implementation_plan.md",
        "ORGANIZATION_OVERVIEW.md",
        "DOCUMENTATION_IMPROVEMENTS_SUMMARY.md",
        "project_docs",
        "css_cleanup_plan.md",
        "DOCUMENTATION_REQUIREMENTS_SPEC.md",
        "modernization_comparison.md",
        "import_warnings_summary.md",
        "documentation-guide.md",
        "documentation_memory_structure.md",
        "error_reports",
        "build_reports",
        "import_analysis",
        "logs",  # Keep build logs but archive old ones
        "nohup.out",
        "poker_debug.log",
        "dynamic_graph.log",
        "docs_build.log",
        "docs_debug.log",
        "docs_server.log",
        "docs_server.pid",
        "developer-guides",
    ]

    # Move files to archive
    for item in to_archive:
        item_path = docs_dir / item
        if item_path.exists():
            try:
                if item_path.is_dir():
                    shutil.move(str(item_path), str(archive_dir / item))
                else:
                    shutil.move(str(item_path), str(archive_dir / item))
            except Exception as e:
                passe}")

    # Clean up old build artifacts
    build_dir = docs_dir / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir, ignore_errors=True)

    # Clean up test directories
    test_build = docs_dir / "test_build"
    if test_build.exists():
        shutil.rmtree(test_build, ignore_errors=True)



def update_sphinx_config():
    """Update the Sphinx configuration to include our new content."""
    docs_dir = Path(__file__).parent
    conf_py = docs_dir / "source" / "conf.py"

    if not conf_py.exists():
        return False


    # Read current config
    with open(conf_py) as f:
        config_content = f.read()

    # Add our new content to toctree if not already there
    additions_needed = []

    if "conversation_showcase" not in config_content:
        additions_needed.append("conversation_showcase")
    if "simple_agent_guide" not in config_content:
        additions_needed.append("simple_agent_guide")
    if "real_examples" not in config_content:
        additions_needed.append("real_examples")

    if additions_needed:
        pass}")
        # We'll handle this in the main index.rst instead

    return True


def update_main_index():
    """Update the main index.rst to include our new documentation."""
    docs_dir = Path(__file__).parent
    index_rst = docs_dir / "source" / "index.rst"

    if not index_rst.exists():
        return False


    # Read current index
    with open(index_rst) as f:
        index_content = f.read()

    # Check if we need to add our content
    additions = []
    if "conversation_showcase" not in index_content:
        additions.append("   conversation_showcase")
    if "simple_agent_guide" not in index_content:
        additions.append("   simple_agent_guide")
    if "real_examples" not in index_content:
        additions.append("   real_examples")

    if additions:
        # Find a good place to insert - look for existing toctree
        if ".. toctree::" in index_content:
            # Add after existing toctree items
            lines = index_content.split("\n")
            new_lines = []
            in_toctree = False
            added = False

            for line in lines:
                new_lines.append(line)

                if ".. toctree::" in line:
                    in_toctree = True
                elif in_toctree and line.strip() and not line.startswith(" "):
                    # End of toctree, add our items before this line
                    if not added:
                        new_lines.pop()  # Remove the line we just added
                        for addition in additions:
                            new_lines.append(addition)
                        new_lines.append("")  # Add blank line
                        new_lines.append(line)  # Add the line back
                        added = True
                    in_toctree = False

            # If we're still in a toctree at the end, add items
            if in_toctree and not added:
                for addition in additions:
                    new_lines.append(addition)

            updated_content = "\n".join(new_lines)

            # Write updated index
            with open(index_rst, "w") as f:
                f.write(updated_content)


    return True


def build_sphinx_docs():
    """Build the Sphinx documentation."""
    docs_dir = Path(__file__).parent


    # Change to docs directory
    original_cwd = os.getcwd()
    os.chdir(docs_dir)

    try:
        # Clean any existing build
        subprocess.run(["make", "clean"], check=False, capture_output=True)

        # Build HTML docs
        result = subprocess.run(
            ["make", "html"], capture_output=True, text=True, check=False
        )

        if result.returncode == 0:

            # Show any warnings
            if result.stderr:

            return True
        print("❌ Documentation build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False

    except Exception as e:
        return False

    finally:
        os.chdir(original_cwd)


def serve_docs():
    """Start serving the documentation locally."""
    docs_dir = Path(__file__).parent
    build_dir = docs_dir / "build" / "html"

    if not build_dir.exists():
        return False


    try:
        os.chdir(build_dir)
        subprocess.run([sys.executable, "-m", "http.server", "8000"], check=False)
    except KeyboardInterrupt:
        passd")
    except Exception as e:
        pass")


def main():
    """Main function."""
    command = sys.argv[1] if len(sys.argv) > 1 else "all"

    if command in ["clean", "all"]:
        cleanup_docs_structure()

    if command in ["config", "all"]:
        update_sphinx_config()
        update_main_index()

    if command in ["build", "all"]:
        if build_sphinx_docs():
            pass!")
        else:
            return 1

    if command == "serve":
        serve_docs()

    if command == "all":

    return 0


if __name__ == "__main__":
    exit(main())
