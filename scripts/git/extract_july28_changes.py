#!/usr/bin/env python3
"""Extract and analyze the July 28 dangling commit and its changes."""

import subprocess


def analyze_july28_commit():
    """Analyze the July 28 commit in detail."""
    commit_sha = "e9c6cbb9ce883514f8e60c01827d540e9c93ed03"
    tree_sha = "81ce3aaca674b093e8305573c01d874bf2067df9"

    print("🔍 Analyzing July 28 Dangling Commit")
    print("=" * 60)

    # Get commit details
    print(f"\n📌 Commit: {commit_sha}")
    print("📅 Date: 2025-07-28T04:10:14")
    print("📝 Subject: On (no branch): temporary changes from import fixes")
    print(f"🌳 Tree: {tree_sha}")

    # Show the commit changes
    print("\n\n=== COMMIT CHANGES ===\n")

    try:
        # Get the diff
        diff_output = subprocess.check_output(
            ["git", "show", commit_sha],
            cwd="/home/will/Projects/haive/backend/haive/packages/haive-agents",
            text=True,
        )

        print(diff_output)
    except Exception as e:
        print(f"Error showing commit: {e}")

    # Extract specific files that might be recoverable
    print("\n\n=== KEY FILES IN TREE ===\n")

    interesting_files = [
        "src/haive/agents/reasoning_and_critique/__init__.py",
        "src/haive/agents/reasoning_and_critique/lats/agent.py",
        "docs/react_agent_v3_comprehensive.py",
        "src/haive/agents/react/README.md",
    ]

    for file_path in interesting_files:
        print(f"\n📄 {file_path}:")
        try:
            # Get the blob SHA for this file
            ls_tree_output = subprocess.check_output(
                ["git", "ls-tree", tree_sha, file_path],
                cwd="/home/will/Projects/haive/backend/haive/packages/haive-agents",
                text=True,
            ).strip()

            if ls_tree_output:
                parts = ls_tree_output.split()
                blob_sha = parts[2]

                # Get file content
                content = subprocess.check_output(
                    ["git", "cat-file", "blob", blob_sha],
                    cwd="/home/will/Projects/haive/backend/haive/packages/haive-agents",
                    text=True,
                )

                # Show first 50 lines
                lines = content.split("\n")
                for i, line in enumerate(lines[:50]):
                    print(f"   {i+1:3}: {line}")

                if len(lines) > 50:
                    print(f"   ... ({len(lines) - 50} more lines)")
        except Exception as e:
            print(f"   Error extracting file: {e}")

    # Compare with current state
    print("\n\n=== COMPARISON WITH CURRENT STATE ===\n")

    # Check if the import fixes are needed
    print("Checking current import issues in reasoning_and_critique module...")

    try:
        current_init = subprocess.check_output(
            ["cat", "src/haive/agents/reasoning_and_critique/__init__.py"],
            cwd="/home/will/Projects/haive/backend/haive/packages/haive-agents",
            stderr=subprocess.DEVNULL,
            text=True,
        )

        print("\nCurrent __init__.py content (first 30 lines):")
        for i, line in enumerate(current_init.split("\n")[:30]):
            print(f"   {i+1:3}: {line}")

        # Check if MCTS imports are commented out
        if "# from haive.agents.reasoning_and_critique.mcts import" in current_init:
            print("\n⚠️  MCTS imports are currently commented out!")
        elif "from haive.agents.reasoning_and_critique.mcts import" in current_init:
            print("\n✅ MCTS imports are active")

    except Exception as e:
        print(f"Error checking current state: {e}")

    # Recovery recommendations
    print("\n\n=== RECOVERY OPTIONS ===\n")

    print("1. Extract the import fixes from the dangling commit:")
    print("   ```bash")
    print("   cd packages/haive-agents")
    print(f"   git show {commit_sha} > july28_import_fixes.patch")
    print("   # Review the patch")
    print("   git apply july28_import_fixes.patch")
    print("   ```")

    print("\n2. Extract specific files:")
    print("   ```bash")
    print("   # Extract the fixed __init__.py")
    print(
        f"   git checkout {commit_sha} -- src/haive/agents/reasoning_and_critique/__init__.py"
    )
    print("   # Extract the fixed lats/agent.py")
    print(
        f"   git checkout {commit_sha} -- src/haive/agents/reasoning_and_critique/lats/agent.py"
    )
    print("   ```")

    print("\n3. View the complete react_agent_v3_comprehensive.py:")
    print("   ```bash")
    print(
        f"   git show {tree_sha}:docs/react_agent_v3_comprehensive.py > react_agent_v3_recovered.py"
    )
    print("   ```")

    print("\n4. Create a recovery branch:")
    print("   ```bash")
    print(f"   git checkout -b recover-july28-imports {commit_sha}")
    print("   git diff feature/fix_everything2")
    print("   ```")


if __name__ == "__main__":
    analyze_july28_commit()
