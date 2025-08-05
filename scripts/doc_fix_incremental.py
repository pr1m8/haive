#!/usr/bin/env python3
"""Apply documentation fixes incrementally with validation."""

import argparse
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path


class IncrementalDocFixer:
    """Apply documentation fixes step by step with validation."""

    def __init__(self, backup: bool = True, validate_each: bool = True):
        self.backup = backup
        self.validate_each = validate_each
        self.backup_dir = Path(
            f"docs/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        )
        self.fixes_applied = []
        self.validation_results = {}

    def create_backup(self):
        """Create backup of docs directory."""
        if self.backup:
            print(f"📦 Creating backup in {self.backup_dir}...")
            shutil.copytree("docs/source", self.backup_dir)
            print("✅ Backup created")

    def validate_current_state(self, step_name: str = "initial") -> dict[str, int]:
        """Validate current documentation state."""
        print(f"\n🔍 Validating {step_name} state...")

        results = {"rst_errors": 0, "rst_warnings": 0, "build_success": False}

        # Quick RST check on sample files
        sample_files = list(Path("docs/source").rglob("*.rst"))[:20]

        for rst_file in sample_files:
            try:
                result = subprocess.run(
                    ["poetry", "run", "rstcheck", str(rst_file)],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.stderr:
                    for line in result.stderr.split("\n"):
                        if "ERROR" in line:
                            results["rst_errors"] += 1
                        elif "WARNING" in line:
                            results["rst_warnings"] += 1
            except BaseException:
                pass

        # Try a quick build
        try:
            result = subprocess.run(
                [
                    "poetry",
                    "run",
                    "sphinx-build",
                    "-b",
                    "html",
                    "-q",
                    "docs/source",
                    "docs/test_build_validate",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            results["build_success"] = result.returncode == 0

            # Clean up
            if Path("docs/test_build_validate").exists():
                shutil.rmtree("docs/test_build_validate")
        except BaseException:
            results["build_success"] = False

        self.validation_results[step_name] = results

        print(f"  RST Errors: {results['rst_errors']}")
        print(f"  RST Warnings: {results['rst_warnings']}")
        print(f"  Build Success: {'✅' if results['build_success'] else '❌'}")

        return results

    def apply_rstfmt(self, dry_run: bool = False) -> bool:
        """Apply RST formatting fixes."""
        print("\n🔧 STEP 1: Applying rstfmt (RST formatting)...")

        if dry_run:
            print("  [DRY RUN - not applying changes]")
            return True

        try:
            # Find all RST files
            rst_files = list(Path("docs/source").rglob("*.rst"))

            # Apply rstfmt in batches
            batch_size = 10
            fixed_count = 0

            for i in range(0, len(rst_files), batch_size):
                batch = rst_files[i : i + batch_size]

                for rst_file in batch:
                    result = subprocess.run(
                        ["poetry", "run", "rstfmt", "--write", str(rst_file)],
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    if result.returncode == 0:
                        fixed_count += 1

                print(
                    f"  Progress: {min(i + batch_size, len(rst_files))}/{len(rst_files)} files",
                )

            print(f"✅ Applied rstfmt to {fixed_count} files")
            self.fixes_applied.append("rstfmt")

            if self.validate_each:
                self.validate_current_state("after_rstfmt")

            return True

        except Exception as e:
            print(f"❌ Error applying rstfmt: {e}")
            return False

    def apply_docformatter(self, dry_run: bool = False) -> bool:
        """Apply Python docstring formatting fixes."""
        print("\n🔧 STEP 2: Applying docformatter (Python docstrings)...")

        if dry_run:
            print("  [DRY RUN - not applying changes]")
            return True

        try:
            # Apply to packages directory
            result = subprocess.run(
                [
                    "poetry",
                    "run",
                    "docformatter",
                    "--in-place",
                    "--recursive",
                    "--wrap-summaries",
                    "79",
                    "--wrap-descriptions",
                    "79",
                    "packages/",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                print("✅ Applied docformatter to Python files")
                self.fixes_applied.append("docformatter")

                if self.validate_each:
                    self.validate_current_state("after_docformatter")

                return True
            print(f"⚠️  docformatter had issues: {result.stderr}")
            return False

        except Exception as e:
            print(f"❌ Error applying docformatter: {e}")
            return False

    def apply_blacken_docs(self, dry_run: bool = False) -> bool:
        """Apply code block formatting in documentation."""
        print("\n🔧 STEP 3: Applying blacken-docs (code blocks)...")

        if dry_run:
            print("  [DRY RUN - not applying changes]")
            return True

        try:
            # Find RST files with code blocks
            rst_files_with_code = []

            for rst_file in Path("docs/source").rglob("*.rst"):
                with open(rst_file) as f:
                    if ".. code-block::" in f.read():
                        rst_files_with_code.append(rst_file)

            print(f"  Found {len(rst_files_with_code)} files with code blocks")

            # Apply blacken-docs
            fixed_count = 0
            for rst_file in rst_files_with_code:
                result = subprocess.run(
                    [
                        "poetry",
                        "run",
                        "blacken-docs",
                        "--line-length",
                        "79",
                        str(rst_file),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    fixed_count += 1

            print(f"✅ Applied blacken-docs to {fixed_count} files")
            self.fixes_applied.append("blacken-docs")

            if self.validate_each:
                self.validate_current_state("after_blacken_docs")

            return True

        except Exception as e:
            print(f"❌ Error applying blacken-docs: {e}")
            return False

    def apply_codespell(self, dry_run: bool = False) -> bool:
        """Apply spelling corrections."""
        print("\n🔧 STEP 4: Applying codespell (spelling corrections)...")

        if dry_run:
            # Show what would be fixed
            result = subprocess.run(
                ["poetry", "run", "codespell", "docs/"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.stdout:
                print("  Would fix these spelling issues:")
                for line in result.stdout.split("\n")[:10]:
                    if line:
                        print(f"    {line}")
            return True

        try:
            # Apply spelling fixes
            result = subprocess.run(
                ["poetry", "run", "codespell", "-w", "docs/"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                print("✅ Applied spelling corrections")
                self.fixes_applied.append("codespell")

                if self.validate_each:
                    self.validate_current_state("after_codespell")

                return True
            print(f"⚠️  codespell had issues: {result.stderr}")
            return False

        except Exception as e:
            print(f"❌ Error applying codespell: {e}")
            return False

    def apply_custom_fixes(self, dry_run: bool = False) -> bool:
        """Apply custom fixes for known issues."""
        print("\n🔧 STEP 5: Applying custom fixes (directives, references)...")

        if dry_run:
            print("  [DRY RUN - not applying changes]")
            return True

        try:
            fixed_count = 0

            for rst_file in Path("docs/source").rglob("*.rst"):
                with open(rst_file) as f:
                    content = f.read()

                original = content

                # Fix exec_code directives
                if ".. exec_code::" in content:
                    content = content.replace(
                        ".. exec_code::",
                        ".. code-block:: python",
                    )
                    # Remove exec_code specific options
                    lines = content.split("\n")
                    fixed_lines = []
                    skip_next = False
                    for line in lines:
                        if skip_next and line.strip().startswith(":"):
                            continue
                        if ".. code-block:: python" in line:
                            skip_next = True
                        else:
                            skip_next = False
                        fixed_lines.append(line)
                    content = "\n".join(fixed_lines)

                # Fix unclosed references
                import re

                # Fix :role:`text without closing backtick
                content = re.sub(r":(\w+):`([^`\n]+)(?!`)", r":\1:`\2`", content)

                if content != original:
                    with open(rst_file, "w") as f:
                        f.write(content)
                    fixed_count += 1

            print(f"✅ Applied custom fixes to {fixed_count} files")
            self.fixes_applied.append("custom_fixes")

            if self.validate_each:
                self.validate_current_state("after_custom_fixes")

            return True

        except Exception as e:
            print(f"❌ Error applying custom fixes: {e}")
            return False

    def final_validation(self) -> bool:
        """Perform final comprehensive validation."""
        print("\n🏁 FINAL VALIDATION")
        print("=" * 60)

        # Full rstcheck validation
        print("Running comprehensive rstcheck...")
        try:
            result = subprocess.run(
                ["poetry", "run", "rstcheck", "docs/source", "--recursive"],
                capture_output=True,
                text=True,
                check=False,
            )

            errors = result.stderr.count("ERROR")
            warnings = result.stderr.count("WARNING")

            print(f"  Total Errors: {errors}")
            print(f"  Total Warnings: {warnings}")

        except Exception as e:
            print(f"  Error running rstcheck: {e}")

        # Test build
        print("\nTesting Sphinx build...")
        try:
            start_time = time.time()
            result = subprocess.run(
                [
                    "poetry",
                    "run",
                    "sphinx-build",
                    "-b",
                    "html",
                    "-W",
                    "--keep-going",
                    "docs/source",
                    "docs/test_final_build",
                ],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )

            build_time = time.time() - start_time
            build_success = result.returncode == 0

            print(
                f"  Build {'✅ PASSED' if build_success else '❌ FAILED'} in {build_time:.1f}s",
            )

            if not build_success and result.stderr:
                # Show first few errors
                errors = result.stderr.split("\n")
                print("\n  First few errors:")
                for error in errors[:5]:
                    if error.strip():
                        print(f"    {error}")

            # Clean up
            if Path("docs/test_final_build").exists():
                shutil.rmtree("docs/test_final_build")

            return build_success

        except subprocess.TimeoutExpired:
            print("  Build timed out after 120s")
            return False
        except Exception as e:
            print(f"  Error during build: {e}")
            return False

    def summarize(self):
        """Summarize all fixes applied and validation results."""
        print("\n" + "=" * 80)
        print("INCREMENTAL FIX SUMMARY")
        print("=" * 80)

        print(f"\n✅ Fixes Applied: {', '.join(self.fixes_applied)}")

        if self.validation_results:
            print("\n📊 Validation Results:")
            print(f"{'Step':<20} {'Errors':<10} {'Warnings':<10} {'Build':<10}")
            print("-" * 50)

            for step, results in self.validation_results.items():
                build_status = "✅" if results.get("build_success", False) else "❌"
                print(
                    f"{step:<20} {results.get('rst_errors', 0):<10} "
                    f"{results.get('rst_warnings', 0):<10} {build_status:<10}",
                )

        if self.backup:
            print(f"\n📦 Backup saved to: {self.backup_dir}")
            print(
                f"   To restore: rm -rf docs/source && cp -r {self.backup_dir} docs/source",
            )


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Apply documentation fixes incrementally",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without applying",
    )
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup")
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation after each step",
    )
    parser.add_argument(
        "--steps",
        nargs="+",
        choices=["rstfmt", "docformatter", "blacken-docs", "codespell", "custom"],
        help="Apply only specific steps",
    )
    args = parser.parse_args()

    fixer = IncrementalDocFixer(
        backup=not args.no_backup and not args.dry_run,
        validate_each=not args.no_validate,
    )

    print("🚀 Incremental Documentation Fixer")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'APPLYING FIXES'}")
    print(f"   Validation: {'After each step' if fixer.validate_each else 'Disabled'}")

    # Create backup
    if not args.dry_run and fixer.backup:
        fixer.create_backup()

    # Initial validation
    if fixer.validate_each:
        fixer.validate_current_state("initial")

    # Apply fixes
    steps = args.steps or [
        "rstfmt",
        "docformatter",
        "blacken-docs",
        "codespell",
        "custom",
    ]

    for step in steps:
        if step == "rstfmt":
            if not fixer.apply_rstfmt(dry_run=args.dry_run):
                print("⚠️  Stopping due to error")
                break
        elif step == "docformatter":
            if not fixer.apply_docformatter(dry_run=args.dry_run):
                print("⚠️  Stopping due to error")
                break
        elif step == "blacken-docs":
            if not fixer.apply_blacken_docs(dry_run=args.dry_run):
                print("⚠️  Stopping due to error")
                break
        elif step == "codespell":
            if not fixer.apply_codespell(dry_run=args.dry_run):
                print("⚠️  Stopping due to error")
                break
        elif step == "custom":
            if not fixer.apply_custom_fixes(dry_run=args.dry_run):
                print("⚠️  Stopping due to error")
                break

    # Final validation
    if not args.dry_run:
        fixer.final_validation()

    # Summary
    fixer.summarize()

    if args.dry_run:
        print("\n💡 To apply these fixes, run without --dry-run")
        print("   python scripts/doc_fix_incremental.py")


if __name__ == "__main__":
    main()
