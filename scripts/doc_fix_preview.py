#!/usr/bin/env python3
"""Preview documentation fixes before applying them."""

from __future__ import annotations

import difflib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


class DocFixPreviewer:
    """Preview documentation fixes with before/after comparison."""

    def __init__(self):
        self.preview_results = {}
        self.temp_dir = tempfile.mkdtemp(prefix="doc_preview_")
        print(f"📁 Created temp directory: {self.temp_dir}")

    def preview_rstfmt(self, sample_files: int = 3) -> dict[str, str]:
        """Preview rstfmt formatting changes on sample RST files."""
        print("\n🔍 PREVIEWING: rstfmt (RST formatting)")
        print("=" * 60)

        rst_files = list(Path("docs/source").rglob("*.rst"))[:sample_files]
        previews = {}

        for rst_file in rst_files:
            print(f"\n📄 File: {rst_file}")

            # Read original
            with open(rst_file) as f:
                original = f.read()

            # Get formatted version
            try:
                result = subprocess.run(
                    ["poetry", "run", "rstfmt", str(rst_file)],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    formatted = result.stdout

                    # Show diff
                    if original != formatted:
                        diff = self._create_diff(original, formatted, str(rst_file))
                        print(diff)
                        previews[str(rst_file)] = diff
                    else:
                        print("  ✅ Already properly formatted")
                else:
                    print(f"  ❌ Error: {result.stderr}")

            except Exception as e:
                print(f"  ❌ Error: {e!s}")

        return previews

    def preview_docformatter(self, sample_files: int = 3) -> dict[str, str]:
        """Preview docformatter changes on Python files."""
        print("\n🔍 PREVIEWING: docformatter (Python docstrings)")
        print("=" * 60)

        # Find Python files with docstrings
        py_files = []
        for py_file in Path("packages").rglob("*.py"):
            if py_file.stat().st_size > 100:  # Skip empty files
                with open(py_file) as f:
                    content = f.read()
                    if '"""' in content or "'''" in content:
                        py_files.append(py_file)
                        if len(py_files) >= sample_files:
                            break

        previews = {}

        for py_file in py_files:
            print(f"\n📄 File: {py_file}")

            try:
                # Get diff from docformatter
                result = subprocess.run(
                    ["poetry", "run", "docformatter", "--diff", str(py_file)],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.stdout:
                    print(result.stdout)
                    previews[str(py_file)] = result.stdout
                else:
                    print("  ✅ Docstrings already properly formatted")

            except Exception as e:
                print(f"  ❌ Error: {e!s}")

        return previews

    def preview_blacken_docs(self, sample_files: int = 3) -> dict[str, str]:
        """Preview blacken-docs changes on RST files with code blocks."""
        print("\n🔍 PREVIEWING: blacken-docs (code blocks in docs)")
        print("=" * 60)

        # Find RST files with code blocks
        rst_files = []
        for rst_file in Path("docs/source").rglob("*.rst"):
            with open(rst_file) as f:
                content = f.read()
                if ".. code-block::" in content or ".. code::" in content:
                    rst_files.append(rst_file)
                    if len(rst_files) >= sample_files:
                        break

        previews = {}

        for rst_file in rst_files:
            print(f"\n📄 File: {rst_file}")

            try:
                # Copy file to temp location
                temp_file = Path(self.temp_dir) / rst_file.name
                shutil.copy2(rst_file, temp_file)

                # Run blacken-docs on temp file
                result = subprocess.run(
                    [
                        "poetry",
                        "run",
                        "blacken-docs",
                        "--line-length",
                        "79",
                        str(temp_file),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                # Compare original and modified
                with open(rst_file) as f:
                    original = f.read()
                with open(temp_file) as f:
                    modified = f.read()

                if original != modified:
                    diff = self._create_diff(original, modified, str(rst_file))
                    print(diff)
                    previews[str(rst_file)] = diff
                else:
                    print("  ✅ Code blocks already properly formatted")

            except Exception as e:
                print(f"  ❌ Error: {e!s}")

        return previews

    def preview_codespell(self, sample_issues: int = 10) -> dict[str, list[str]]:
        """Preview spelling corrections from codespell."""
        print("\n🔍 PREVIEWING: codespell (spelling corrections)")
        print("=" * 60)

        try:
            # Run codespell on docs
            result = subprocess.run(
                ["poetry", "run", "codespell", "docs/", "--count"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.stdout:
                lines = result.stdout.strip().split("\n")
                issues = []

                for i, line in enumerate(lines[:sample_issues]):
                    if ": " in line:
                        print(f"  {line}")
                        issues.append(line)

                if len(lines) > sample_issues:
                    print(f"  ... and {len(lines) - sample_issues} more")

                return {"spelling": issues}
            print("  ✅ No spelling issues found")
            return {}

        except Exception as e:
            print(f"  ❌ Error: {e!s}")
            return {}

    def preview_rstcheck_issues(self) -> dict[str, int]:
        """Preview issues that rstcheck would find."""
        print("\n🔍 CHECKING: rstcheck validation")
        print("=" * 60)

        issue_counts = {"errors": 0, "warnings": 0, "info": 0}

        try:
            # Run rstcheck on a sample of files
            rst_files = list(Path("docs/source").rglob("*.rst"))[:10]

            for rst_file in rst_files:
                result = subprocess.run(
                    ["poetry", "run", "rstcheck", str(rst_file), "--report", "warning"],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.stderr:
                    for line in result.stderr.strip().split("\n"):
                        if "ERROR" in line:
                            issue_counts["errors"] += 1
                        elif "WARNING" in line:
                            issue_counts["warnings"] += 1
                        else:
                            issue_counts["info"] += 1

            print(f"  Errors: {issue_counts['errors']}")
            print(f"  Warnings: {issue_counts['warnings']}")
            print(f"  Info: {issue_counts['info']}")

            return issue_counts

        except Exception as e:
            print(f"  ❌ Error: {e!s}")
            return issue_counts

    def test_fixes_on_sample(self) -> bool:
        """Test if applying fixes to a sample file allows it to build."""
        print("\n🧪 TESTING: Apply fixes to sample file and validate")
        print("=" * 60)

        # Find a problematic RST file
        sample_file = None
        for rst_file in Path("docs/source/agents/demos").rglob("*.rst"):
            # Check if file has issues
            result = subprocess.run(
                ["poetry", "run", "rstcheck", str(rst_file)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                sample_file = rst_file
                break

        if not sample_file:
            print("  ✅ No problematic files found")
            return True

        print(f"  Testing on: {sample_file}")

        # Copy to temp
        temp_file = Path(self.temp_dir) / sample_file.name
        shutil.copy2(sample_file, temp_file)

        # Apply fixes
        print("  Applying fixes...")

        # 1. Format with rstfmt
        subprocess.run(
            ["poetry", "run", "rstfmt", "--write", str(temp_file)],
            capture_output=True,
            check=False,
        )

        # 2. Fix code blocks
        subprocess.run(
            ["poetry", "run", "blacken-docs", str(temp_file)],
            capture_output=True,
            check=False,
        )

        # 3. Validate fixed file
        print("  Validating fixed file...")
        result = subprocess.run(
            ["poetry", "run", "rstcheck", str(temp_file)],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print("  ✅ File validates successfully after fixes!")

            # Show what was fixed
            with open(sample_file) as f:
                original = f.read()
            with open(temp_file) as f:
                fixed = f.read()

            if original != fixed:
                print("\n  Changes made:")
                diff = self._create_diff(original, fixed, str(sample_file), context=3)
                print(diff)

            return True
        print("  ⚠️  File still has issues after fixes:")
        print(result.stderr)
        return False

    def _create_diff(
        self,
        original: str,
        modified: str,
        filename: str,
        context: int = 5,
    ) -> str:
        """Create a unified diff between original and modified content."""
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"{filename} (original)",
            tofile=f"{filename} (fixed)",
            n=context,
        )

        # Colorize diff if terminal supports it
        diff_text = ""
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                diff_text += f"\033[32m{line}\033[0m"  # Green for additions
            elif line.startswith("-") and not line.startswith("---"):
                diff_text += f"\033[31m{line}\033[0m"  # Red for deletions
            elif line.startswith("@"):
                diff_text += f"\033[36m{line}\033[0m"  # Cyan for headers
            else:
                diff_text += line

        return diff_text

    def cleanup(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)
        print("\n🧹 Cleaned up temp directory")

    def save_preview_results(self):
        """Save preview results to file."""
        output_file = Path("docs/fix_preview_results.json")

        # Convert preview results to serializable format
        serializable_results = {
            "rstfmt_changes": len(self.preview_results.get("rstfmt", {})),
            "docformatter_changes": len(self.preview_results.get("docformatter", {})),
            "blacken_docs_changes": len(self.preview_results.get("blacken_docs", {})),
            "spelling_issues": len(
                self.preview_results.get("codespell", {}).get("spelling", []),
            ),
            "rstcheck_issues": self.preview_results.get("rstcheck", {}),
        }

        with open(output_file, "w") as f:
            json.dump(serializable_results, f, indent=2)

        print(f"\n💾 Preview results saved to: {output_file}")


def main():
    """Main function."""
    print("🚀 Documentation Fix Preview Tool")
    print("This tool shows you what would be fixed BEFORE applying changes\n")

    previewer = DocFixPreviewer()

    try:
        # Preview each type of fix
        previewer.preview_results["rstfmt"] = previewer.preview_rstfmt(sample_files=3)
        previewer.preview_results["docformatter"] = previewer.preview_docformatter(
            sample_files=3,
        )
        previewer.preview_results["blacken_docs"] = previewer.preview_blacken_docs(
            sample_files=3,
        )
        previewer.preview_results["codespell"] = previewer.preview_codespell(
            sample_issues=10,
        )
        previewer.preview_results["rstcheck"] = previewer.preview_rstcheck_issues()

        # Test fixes on a sample file
        success = previewer.test_fixes_on_sample()

        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        total_changes = 0
        total_changes += len(previewer.preview_results.get("rstfmt", {}))
        total_changes += len(previewer.preview_results.get("docformatter", {}))
        total_changes += len(previewer.preview_results.get("blacken_docs", {}))

        print(f"\n📊 Total files that would be changed: {total_changes}")
        print(
            f"   - RST formatting: {len(previewer.preview_results.get('rstfmt', {}))}",
        )
        print(
            f"   - Python docstrings: {len(previewer.preview_results.get('docformatter', {}))}",
        )
        print(
            f"   - Code blocks: {len(previewer.preview_results.get('blacken_docs', {}))}",
        )

        spelling_issues = len(
            previewer.preview_results.get("codespell", {}).get("spelling", []),
        )
        if spelling_issues > 0:
            print(f"   - Spelling corrections: {spelling_issues}")

        rstcheck = previewer.preview_results.get("rstcheck", {})
        if rstcheck:
            print("\n⚠️  Current validation issues:")
            print(f"   - Errors: {rstcheck.get('errors', 0)}")
            print(f"   - Warnings: {rstcheck.get('warnings', 0)}")

        if success:
            print("\n✅ Test fixes validated successfully!")
        else:
            print("\n⚠️  Some issues may remain after automatic fixes")

        # Save results
        previewer.save_preview_results()

        print("\n💡 To apply these fixes, run:")
        print("   python scripts/doc_auto_fix.py --fix")
        print("\n⚠️  Always review changes before committing!")

    finally:
        previewer.cleanup()


if __name__ == "__main__":
    main()
