#!/usr/bin/env python3
"""Automatically fix documentation issues using proper tools."""

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class DocAutoFixer:
    """Automated documentation fixing with proper tools."""

    def __init__(self, backup: bool = True):
        self.backup = backup
        self.backup_dir = Path(
            f"docs/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        self.fixed_files = []
        self.errors = []

    def create_backup(self):
        """Create backup of docs directory."""
        if self.backup:
            print(f"📦 Creating backup in {self.backup_dir}")
            shutil.copytree("docs/source", self.backup_dir)
            print("✅ Backup created")

    def run_rstfmt(self, dry_run: bool = True):
        """Format RST files with rstfmt."""
        print("\n🔧 Running rstfmt formatter...")

        rst_files = list(Path("docs/source").rglob("*.rst"))

        cmd = ["poetry", "run", "rstfmt"]
        if not dry_run:
            cmd.append("--write")

        fixed_count = 0
        for rst_file in rst_files:
            try:
                result = subprocess.run(
                    cmd + [str(rst_file)], capture_output=True, text=True
                )

                if result.returncode == 0:
                    if dry_run:
                        # Check if output differs from input
                        with open(rst_file, "r") as f:
                            original = f.read()
                        if result.stdout != original:
                            print(f"  Would fix: {rst_file.name}")
                            fixed_count += 1
                    else:
                        print(f"  ✅ Fixed: {rst_file.name}")
                        self.fixed_files.append(str(rst_file))
                        fixed_count += 1

            except Exception as e:
                self.errors.append(f"rstfmt error on {rst_file}: {e}")

        print(f"  {'Would fix' if dry_run else 'Fixed'} {fixed_count} files")
        return fixed_count

    def run_docformatter(self, dry_run: bool = True):
        """Format Python docstrings with docformatter."""
        print("\n🔧 Running docformatter...")

        cmd = ["poetry", "run", "docformatter", "--recursive"]
        if not dry_run:
            cmd.append("--in-place")
        else:
            cmd.append("--diff")

        # Add options for better formatting
        cmd.extend(["--wrap-summaries", "79", "--wrap-descriptions", "79", "--blank"])

        cmd.append("packages/")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if dry_run and result.stdout:
                # Count files that would be changed
                changed_files = result.stdout.count("---")
                print(f"  Would fix {changed_files} Python files")

                # Show first few examples
                lines = result.stdout.split("\n")
                for i, line in enumerate(lines[:50]):
                    if line.startswith("---"):
                        print(f"  Example: {line}")
            elif not dry_run:
                print("  ✅ Fixed Python docstrings")

        except Exception as e:
            self.errors.append(f"docformatter error: {e}")

    def run_blacken_docs(self, dry_run: bool = True):
        """Format code blocks in documentation with blacken-docs."""
        print("\n🔧 Running blacken-docs on code blocks...")

        rst_files = list(Path("docs/source").rglob("*.rst"))

        cmd = ["poetry", "run", "blacken-docs"]
        if not dry_run:
            cmd.append("--write")

        fixed_count = 0
        for rst_file in rst_files:
            try:
                if dry_run:
                    # Check mode
                    result = subprocess.run(
                        cmd + ["--diff", str(rst_file)], capture_output=True, text=True
                    )
                    if result.stdout:  # Has differences
                        print(f"  Would fix code blocks in: {rst_file.name}")
                        fixed_count += 1
                else:
                    # Fix mode
                    result = subprocess.run(
                        cmd + [str(rst_file)], capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        fixed_count += 1

            except Exception as e:
                self.errors.append(f"blacken-docs error on {rst_file}: {e}")

        print(f"  {'Would fix' if dry_run else 'Fixed'} {fixed_count} files")
        return fixed_count

    def fix_sphinx_directives(self, dry_run: bool = True):
        """Fix common Sphinx directive issues."""
        print("\n🔧 Fixing Sphinx directive issues...")

        fixes_applied = 0

        for rst_file in Path("docs/source").rglob("*.rst"):
            try:
                with open(rst_file, "r") as f:
                    content = f.read()

                original = content

                # Fix exec_code -> code-block
                if ".. exec_code::" in content:
                    content = content.replace(".. exec_code::", ".. code-block::")
                    content = content.replace("   :language: python", "")
                    content = content.replace("   :hide_output:", "")

                # Fix jinja directives
                if ".. jinja::" in content:
                    lines = content.split("\n")
                    fixed_lines = []
                    for line in lines:
                        if line.strip() == ".. jinja::":
                            fixed_lines.append(".. .. jinja:: (commented out)")
                        else:
                            fixed_lines.append(line)
                    content = "\n".join(fixed_lines)

                # Fix common role issues
                # :doc:`missing_close -> :doc:`missing_close`
                import re

                content = re.sub(r":(\w+):`([^`]+)(?!`)", r":\1:`\2`", content)

                if content != original:
                    if not dry_run:
                        with open(rst_file, "w") as f:
                            f.write(content)
                        self.fixed_files.append(str(rst_file))
                    print(f"  {'Would fix' if dry_run else 'Fixed'}: {rst_file.name}")
                    fixes_applied += 1

            except Exception as e:
                self.errors.append(f"Directive fix error on {rst_file}: {e}")

        print(f"  {'Would fix' if dry_run else 'Fixed'} {fixes_applied} files")
        return fixes_applied

    def validate_fixes(self):
        """Validate fixes with rstcheck."""
        print("\n✔️  Validating fixes with rstcheck...")

        issues_found = 0
        for rst_file in Path("docs/source").rglob("*.rst")[:10]:  # Check first 10
            try:
                result = subprocess.run(
                    ["poetry", "run", "rstcheck", str(rst_file)],
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    issues_found += 1
                    print(f"  ⚠️  Issues remain in: {rst_file.name}")

            except Exception as e:
                self.errors.append(f"Validation error: {e}")

        if issues_found == 0:
            print("  ✅ All checked files are valid!")
        else:
            print(f"  ⚠️  {issues_found} files still have issues")

    def summarize(self):
        """Summarize fixes applied."""
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        print(f"\n✅ Fixed {len(self.fixed_files)} files")

        if self.errors:
            print(f"\n❌ Encountered {len(self.errors)} errors:")
            for error in self.errors[:5]:
                print(f"  - {error}")

        if self.backup:
            print(f"\n📦 Backup saved to: {self.backup_dir}")
            print(
                "   To restore: rm -rf docs/source && mv {self.backup_dir} docs/source"
            )


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Auto-fix documentation issues")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Preview changes without applying (default)",
    )
    parser.add_argument("--fix", action="store_true", help="Actually apply fixes")
    parser.add_argument(
        "--no-backup", action="store_true", help="Don't create backup (not recommended)"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate fixes after applying"
    )
    args = parser.parse_args()

    if args.fix and args.dry_run:
        args.dry_run = False

    fixer = DocAutoFixer(backup=not args.no_backup and not args.dry_run)

    print("🚀 Documentation Auto-Fixer")
    print(
        f"   Mode: {'DRY RUN - Preview Only' if args.dry_run else '⚠️  APPLYING FIXES'}"
    )

    # Create backup if fixing
    if not args.dry_run:
        fixer.create_backup()

    # Run fixes
    fixer.run_rstfmt(dry_run=args.dry_run)
    fixer.run_docformatter(dry_run=args.dry_run)
    fixer.run_blacken_docs(dry_run=args.dry_run)
    fixer.fix_sphinx_directives(dry_run=args.dry_run)

    # Validate if requested
    if args.validate and not args.dry_run:
        fixer.validate_fixes()

    # Summarize
    fixer.summarize()

    if args.dry_run:
        print("\n💡 To apply these fixes, run:")
        print("   python scripts/doc_auto_fix.py --fix")
        print("\n⚠️  Always review changes before committing!")


if __name__ == "__main__":
    main()
