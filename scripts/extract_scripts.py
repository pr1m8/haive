#!/usr/bin/env python3
"""Extract individual dev-tools scripts from stash patch."""

import os
from pathlib import Path
import re


def extract_script_from_patch(patch_content, script_name):
    """Extract a single script file from the patch content."""
    # Find the start of this script in the patch
    pattern = (
        rf"\+\+\+ b/dev-tools/scripts/{re.escape(script_name)}\n(.*?)(?=\n\+\+\+ b/|\n--- a/|\Z)"
    )
    match = re.search(pattern, patch_content, re.DOTALL)

    if not match:
        return None

    # Extract the script content (lines starting with +)
    script_lines = []
    lines = match.group(1).split("\n")

    for line in lines:
        if line.startswith("+"):
            # Remove the + prefix and add to script
            script_lines.append(line[1:])
        elif line.startswith("@@"):
            # Skip hunk headers
            continue
        elif line.startswith("-"):
            # Skip deleted lines
            continue
        elif line.startswith(" "):
            # Context line - remove space prefix
            script_lines.append(line[1:])

    return "\n".join(script_lines)


def main():
    # Read the patch file
    patch_file = "git_fsck_repair_20250729_213007/stashes/stash_1_content_20250729_213007.patch"

    with open(patch_file) as f:
        patch_content = f.read()

    # List of important scripts to extract
    priority_scripts = [
        "fix-rich-dependency-permanently.sh",
        "intelligent-error-analyzer.sh",
        "comprehensive-import-manager.sh",
        "debug-and-fix-syntax.sh",
        "systematic-code-fixer.sh",
        "safe-refactor.sh",
        "sync-package-configs.sh",
        "bulk_package_fix.sh",
        "dependency-conflict-checker.sh",
    ]

    # Create scripts directory if it doesn't exist
    scripts_dir = Path("dev-tools/scripts")
    scripts_dir.mkdir(parents=True, exist_ok=True)

    successful_extractions = 0

    for script_name in priority_scripts:
        script_path = scripts_dir / script_name

        # Skip if file already exists
        if script_path.exists():
            continue

        script_content = extract_script_from_patch(patch_content, script_name)

        if script_content:
            # Write the script file
            with open(script_path, "w") as f:
                f.write(script_content)

            # Make it executable
            os.chmod(script_path, 0o755)

            successful_extractions += 1
        else:
            pass


if __name__ == "__main__":
    main()
