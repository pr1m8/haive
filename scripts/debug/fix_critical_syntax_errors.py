#!/usr/bin/env python3
"""Fix critical syntax errors that prevent documentation build."""

import re
import sys
from pathlib import Path


def fix_chess_example():
    """Fix unterminated string literal in chess example."""
    file_path = Path(
        "packages/haive-games/src/haive/games/chess/example_configurable_players.py"
    )
    if not file_path.exists():
        return False

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Fix the double exclamation mark causing unterminated string
        fixed_content = re.sub(
            r'print\("✅ Game completed successfully!"!"\)',
            r'print("✅ Game completed successfully!")',
            content,
        )

        if fixed_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
    except Exception as e:
        pass
    return False


def fix_graph_db_example():
    """Fix unterminated string literal in graph DB example."""
    file_path = Path(
        "packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py"
    )
    if not file_path.exists():
        return False

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Fix unterminated string literal with pass
        fixed_content = re.sub(r'pass"\)', r'pass")', content)

        if fixed_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
    except Exception as e:
        pass
    return False


def fix_kg_base_example():
    """Fix unterminated string literal in KG base example."""
    file_path = Path(
        "packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/example.py"
    )
    if not file_path.exists():
        return False

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Fix unterminated string literal with pass
        fixed_content = re.sub(r'pass"\)', r'pass")', content)

        if fixed_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
    except Exception as e:
        pass
    return False


def fix_social_media_example():
    """Fix unmatched brace in social media example."""
    file_path = Path(
        "packages/haive-agents/src/haive/agents/conversation/social_media/example.py"
    )
    if not file_path.exists():
        return False

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Fix unmatched brace
        fixed_content = re.sub(r'pass"\}', r'pass"}', content)

        if fixed_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
    except Exception as e:
        pass
    return False


def fix_basic_state_management():
    """Fix unterminated string literal in basic state management."""
    file_path = Path(
        "packages/haive-agents/src/haive/agents/conversation/base/examples/basic_state_management.py"
    )
    if not file_path.exists():
        return False

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Fix unterminated string literal with pass
        fixed_content = re.sub(r'pass"\)', r'pass")', content)

        if fixed_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
    except Exception as e:
        pass
    return False


def fix_additional_syntax_errors():
    """Fix additional syntax errors found in the pre-build checker."""
    fixes = []

    # Fix test_rewoo.py - missing indented block after 'for' statement
    file_path = Path(
        "packages/haive-agents/src/haive/agents/planning/rewoo/test_rewoo.py"
    )
    if file_path.exists():
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Fix missing indented block after 'for' statement followed by 'else'
            fixed_content = re.sub(
                r"(\s+for [^:]+:)\s*\n(\s+else:)", r"\1\n\2    pass\n\3", content
            )

            if fixed_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(fixed_content)
                fixes.append("Fixed test_rewoo.py missing indented block")
        except Exception as e:
            pass

    # Fix test_planner.py - missing indented block after 'for' statement
    file_path = Path(
        "packages/haive-agents/src/haive/agents/planning/rewoo/test_planner.py"
    )
    if file_path.exists():
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Fix missing indented block after 'for' statement
            fixed_content = re.sub(
                r"(\s+for [^:]+:)\s*\n(\s+return)", r"\1\n        pass\n\2", content
            )

            if fixed_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(fixed_content)
                fixes.append("Fixed test_planner.py missing indented block")
        except Exception as e:
            pass

    return fixes


def main():
    """Main function to run critical syntax fixes."""

    fixes = []

    # Fix the most critical syntax errors that block documentation build
    if fix_chess_example():
        fixes.append("Fixed chess example unterminated string")

    if fix_graph_db_example():
        fixes.append("Fixed graph DB example unterminated string")

    if fix_kg_base_example():
        fixes.append("Fixed KG base example unterminated string")

    if fix_social_media_example():
        fixes.append("Fixed social media example unmatched brace")

    if fix_basic_state_management():
        fixes.append("Fixed basic state management unterminated string")

    # Fix additional syntax errors
    additional_fixes = fix_additional_syntax_errors()
    fixes.extend(additional_fixes)

    if fixes:
        for fix in fixes:
            pass
    else:
        print("pass")

    return 0


if __name__ == "__main__":
    sys.exit(main())