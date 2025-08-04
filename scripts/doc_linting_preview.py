#!/usr/bin/env python3
"""Preview documentation issues using proper linting tools."""

import argparse
import json
from pathlib import Path
import subprocess


class DocLinter:
    """Documentation linting and preview system."""

    def __init__(self, docs_dir: Path, dry_run: bool = True):
        self.docs_dir = docs_dir
        self.dry_run = dry_run
        self.results = {}

    def run_rstcheck(self) -> dict[str, list[str]]:
        """Run rstcheck on RST files."""
        print("\n🔍 Running rstcheck...")
        issues = {}

        rst_files = list(self.docs_dir.rglob("*.rst"))

        for rst_file in rst_files:
            try:
                result = subprocess.run(
                    [
                        "poetry", "run", "rstcheck",
                        str(rst_file), "--report", "warning"
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode != 0 or result.stderr:
                    issues[str(rst_file)] = result.stderr.strip().split("\n")

            except Exception as e:
                issues[str(rst_file)] = [f"Error: {e!s}"]

        return issues

    def run_sphinx_lint(self) -> dict[str, list[str]]:
        """Run sphinx-lint on documentation."""
        print("\n🔍 Running sphinx-lint...")
        issues = {}

        try:
            result = subprocess.run(
                ["poetry", "run", "sphinx-lint",
                 str(self.docs_dir)],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.stdout:
                for line in result.stdout.strip().split("\n"):
                    if ":" in line:
                        file_path, issue = line.split(":", 1)
                        if file_path not in issues:
                            issues[file_path] = []
                        issues[file_path].append(issue.strip())

        except Exception as e:
            issues["sphinx-lint"] = [f"Error: {e!s}"]

        return issues

    def run_pydocstyle(self) -> dict[str, list[str]]:
        """Run pydocstyle on Python files."""
        print("\n🔍 Running pydocstyle...")
        issues = {}

        # Find Python files that likely have documentation issues
        py_files = list(Path("packages").rglob("*.py"))

        for py_file in py_files[:50]:  # Limit to first 50 for preview
            try:
                result = subprocess.run(
                    ["poetry", "run", "pydocstyle",
                     str(py_file)],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.stdout:
                    issues[str(py_file)] = result.stdout.strip().split("\n")

            except Exception as e:
                issues[str(py_file)] = [f"Error: {e!s}"]

        return issues

    def preview_rstfmt(self, sample_file: Path) -> tuple[str, str]:
        """Preview rstfmt formatting on a sample file."""
        print(f"\n🔍 Preview rstfmt on {sample_file.name}...")

        try:
            # Read original
            with open(sample_file) as f:
                original = f.read()

            # Run rstfmt
            result = subprocess.run(
                ["poetry", "run", "rstfmt",
                 str(sample_file)],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                return original, result.stdout
            return original, f"Error: {result.stderr}"

        except Exception as e:
            return "", f"Error: {e!s}"

    def test_sphinx_build(self) -> bool:
        """Test if Sphinx can build with current state."""
        print("\n🔨 Testing Sphinx build...")

        try:
            result = subprocess.run(
                [
                    "poetry",
                    "run",
                    "sphinx-build",
                    "-b",
                    "html",
                    "-W",
                    "--keep-going",
                    str(self.docs_dir),
                    "docs/test_build",
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,  # 1 minute timeout for test
            )

            success = result.returncode == 0

            # Clean up test build
            subprocess.run(["rm", "-rf", "docs/test_build"],
                           capture_output=True,
                           check=False)

            return success, result.stderr

        except subprocess.TimeoutExpired:
            return False, "Build timed out after 60 seconds"
        except Exception as e:
            return False, str(e)

    def summarize_issues(self):
        """Summarize all found issues."""
        print("\n" + "=" * 80)
        print("DOCUMENTATION ISSUES SUMMARY")
        print("=" * 80)

        total_issues = 0

        # RST issues
        if "rstcheck" in self.results:
            rst_issues = self.results["rstcheck"]
            issue_count = sum(len(issues) for issues in rst_issues.values())
            print(
                f"\n📄 RST Issues (rstcheck): {issue_count} issues in {
                    len(rst_issues)} files", )

            # Show first 5 files as examples
            for file, issues in list(rst_issues.items())[:5]:
                print(f"\n  {Path(file).name}:")
                for issue in issues[:3]:  # First 3 issues per file
                    print(f"    - {issue}")

            total_issues += issue_count

        # Sphinx-lint issues
        if "sphinx-lint" in self.results:
            sphinx_issues = self.results["sphinx-lint"]
            issue_count = sum(len(issues) for issues in sphinx_issues.values())
            print(f"\n📚 Sphinx Issues (sphinx-lint): {issue_count} issues")
            total_issues += issue_count

        # Docstring issues
        if "pydocstyle" in self.results:
            py_issues = self.results["pydocstyle"]
            issue_count = sum(len(issues) for issues in py_issues.values())
            print(
                f"\n🐍 Python Docstring Issues (pydocstyle): {issue_count} issues in {
                    len(py_issues)} files", )
            total_issues += issue_count

        print(f"\n📊 Total Issues Found: {total_issues}")

        return total_issues

    def suggest_fixes(self):
        """Suggest automated fixes based on issues found."""
        print("\n" + "=" * 80)
        print("SUGGESTED FIXES")
        print("=" * 80)

        print("\n1. For RST formatting issues:")
        print("   poetry run rstfmt --write docs/source/**/*.rst")

        print("\n2. For Python docstring issues:")
        print("   poetry run docformatter --in-place --recursive packages/")

        print("\n3. For Sphinx-specific issues:")
        print("   poetry run sphinx-lint --fix docs/source/")

        print("\n4. For comprehensive docstring linting:")
        print("   poetry run pydoclint --style=google packages/")

        print("\n5. To validate all changes:")
        print("   poetry run rstcheck docs/source/ --recursive")
        print(
            "   poetry run sphinx-build -b html -W docs/source docs/test_build"
        )


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Preview documentation issues")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply fixes (not just preview)",
    )
    parser.add_argument("--test-build",
                        action="store_true",
                        help="Test Sphinx build")
    args = parser.parse_args()

    docs_dir = Path("docs/source")
    linter = DocLinter(docs_dir, dry_run=not args.fix)

    # Run various linters
    print("🚀 Starting documentation linting preview...")

    # Check which tools are available
    available_tools = []
    for tool in ["rstcheck", "sphinx-lint", "pydocstyle", "rstfmt"]:
        try:
            subprocess.run(
                ["poetry", "run", tool, "--help"],
                capture_output=True,
                check=True,
            )
            available_tools.append(tool)
        except BaseException:
            print(f"⚠️  {tool} not available - skipping")

    print(f"\n✅ Available tools: {', '.join(available_tools)}")

    # Run available tools
    if "rstcheck" in available_tools:
        linter.results["rstcheck"] = linter.run_rstcheck()

    if "sphinx-lint" in available_tools:
        linter.results["sphinx-lint"] = linter.run_sphinx_lint()

    if "pydocstyle" in available_tools:
        linter.results["pydocstyle"] = linter.run_pydocstyle()

    # Preview rstfmt on a sample file
    if "rstfmt" in available_tools:
        sample_files = list(docs_dir.glob("*.rst"))[:1]
        if sample_files:
            original, formatted = linter.preview_rstfmt(sample_files[0])
            if formatted and not formatted.startswith("Error"):
                print("\n📝 rstfmt preview (first 20 lines):")
                print("BEFORE:")
                print("\n".join(original.split("\n")[:20]))
                print("\nAFTER:")
                print("\n".join(formatted.split("\n")[:20]))

    # Test build if requested
    if args.test_build:
        success, error = linter.test_sphinx_build()
        print(f"\n🏗️  Test build: {'✅ SUCCESS' if success else '❌ FAILED'}")
        if not success:
            print(f"   Error: {error[:200]}...")

    # Summarize
    total_issues = linter.summarize_issues()

    if total_issues > 0:
        linter.suggest_fixes()
    else:
        print("\n✨ No issues found!")

    # Save results
    with open("docs/linting_results.json", "w") as f:
        json.dump(linter.results, f, indent=2)
    print("\n💾 Detailed results saved to docs/linting_results.json")


if __name__ == "__main__":
    main()
