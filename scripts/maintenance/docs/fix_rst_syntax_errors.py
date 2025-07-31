#!/usr/bin/env python3
"""Fix critical RST syntax errors in documentation files."""

from pathlib import Path
import re


def fix_triple_quotes(content):
    """Fix unterminated triple-quoted strings in code blocks."""
    # Pattern to find code blocks with unterminated triple quotes
    pattern = r'(\.\. code-block:: python\n\n(?:   [^\n]*\n)*?   """[^"]*?)\n\n"""""""""""'

    def replace_func(match):
        code_block = match.group(1)
        # Close the triple quote properly
        return code_block + '   """'

    content = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
    return content


def fix_grid_directives(content):
    """Replace grid directives with standard RST."""
    # Replace grid directive with table or list
    content = re.sub(r"\.\. grid::[^\n]*\n(?:   :[^\n]*\n)*", "", content)
    content = re.sub(r"\.\. grid-item-card::[^\n]*\n(?:   :[^\n]*\n)*", ".. card::\n", content)

    return content


def fix_agent_run_capture(content):
    """Fix agent-run-capture directive."""
    # Replace with code-block for now
    pattern = r"\.\. agent-run-capture:: ([^\n]+)\n(?:   :[^\n]*\n)*"
    replacement = r".. note::\n\n   Agent execution capture available at: \1"
    content = re.sub(pattern, replacement, content)

    return content


def fix_todo_directives(content):
    """Replace todo directives with admonitions."""
    content = re.sub(r"\.\. todo::", ".. admonition:: TODO", content)

    return content


def fix_rst_file(file_path):
    """Fix RST syntax errors in a file."""
    content = file_path.read_text()
    original = content

    # Apply fixes
    content = fix_triple_quotes(content)
    content = fix_grid_directives(content)
    content = fix_agent_run_capture(content)
    content = fix_todo_directives(content)

    # Fix title underlines
    lines = content.split("\n")
    fixed_lines = []

    for i in range(len(lines)):
        if i > 0 and i < len(lines) - 1:
            # Check if current line is a potential underline
            if lines[i].strip() and all(c in "=-~`" for c in lines[i].strip()):
                # Check if previous line is a title
                prev_line = lines[i - 1].strip()
                if prev_line and len(lines[i].strip()) < len(prev_line):
                    # Fix underline length
                    char = lines[i].strip()[0]
                    fixed_lines.append(char * len(prev_line))
                    continue

        fixed_lines.append(lines[i])

    content = "\n".join(fixed_lines)

    if content != original:
        file_path.write_text(content)
        print(f"Fixed: {file_path}")
        return True
    return False


def main():
    """Fix all RST files with syntax errors."""
    docs_dir = Path("docs/source")
    rst_files = list(docs_dir.rglob("*.rst"))

    fixed_count = 0
    for file_path in rst_files:
        try:
            if fix_rst_file(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")

    print(f"\nFixed {fixed_count} RST files")


if __name__ == "__main__":
    main()
