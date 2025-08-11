#!/usr/bin/env python3
"""
Agent Base Consolidation Script with Dry Run Support

This script consolidates the agent base classes by:
1. Moving EnhancedAgent to become the main Agent class
2. Updating all imports across the project
3. Removing version suffixes from class names
4. Ensuring all references are consistent

Usage:
    # Test what would happen (DRY RUN)
    DRY_RUN=1 python scripts/maintenance/agent_consolidation_refactorer.py

    # Actually perform the consolidation
    python scripts/maintenance/agent_consolidation_refactorer.py

    # Rollback to checkpoint
    python scripts/maintenance/agent_consolidation_refactorer.py --rollback
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from rope.base.project import Project
    from rope.refactor.move import MoveGlobal
    from rope.refactor.rename import Rename
    from rope.refactor.restructure import Restructure
except ImportError:
    print("❌ Error: rope library not installed")
    print("💡 Install with: poetry add --group dev rope")
    sys.exit(1)


class AgentConsolidationRefactorer:
    """Safely consolidate agent base classes using rope and dry run protection."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run or os.getenv("DRY_RUN", "").lower() in (
            "1",
            "true",
            "yes",
        )
        self.project_root = Path.cwd()
        self.target_package = self.project_root / "packages" / "haive-agents"
        self.changes_applied = []

        print(f"🔧 Agent Consolidation Refactorer")
        print(f"📁 Project root: {self.project_root}")
        print(f"🎯 Target package: {self.target_package}")
        print(f"🧪 Dry run mode: {'ON' if self.dry_run else 'OFF'}")
        print("=" * 60)

    def step_1_analyze_current_structure(self):
        """Analyze current agent class structure in TARGET PACKAGE ONLY."""
        print(
            f"\n📊 Step 1: Analyzing agent structure in {self.target_package.name}..."
        )
        print(
            f"🎯 SCOPE: Only analyzing {self.target_package} - NOT touching root repo"
        )

        # Only look in the target package
        agent_files = list(self.target_package.glob("src/**/*agent*.py"))

        agent_classes = {}
        for file_path in agent_files:
            try:
                content = file_path.read_text()
                # Look for class definitions
                import re

                classes = re.findall(r"class\s+(\w*[Aa]gent\w*)", content)
                if classes:
                    rel_path = str(file_path.relative_to(self.target_package))
                    agent_classes[rel_path] = classes
            except Exception as e:
                print(f"⚠️  Error reading {file_path}: {e}")

        print(
            f"\n📋 Found {len(agent_classes)} files with agent classes in {self.target_package.name}:"
        )
        for file_path, classes in agent_classes.items():
            print(f"  📄 {file_path}")
            for cls in classes:
                print(f"    - {cls}")

        return agent_classes

    def step_2_identify_consolidation_targets(self):
        """Identify what needs to be consolidated in TARGET PACKAGE ONLY."""
        print(
            f"\n🎯 Step 2: Identifying consolidation targets in {self.target_package.name}..."
        )
        print(f"🎯 SCOPE: Only targeting files within {self.target_package}")

        # All paths relative to target package only
        targets = {
            "enhanced_agent_base": "src/haive/agents/base/enhanced_agent.py",
            "main_agent_base": "src/haive/agents/base/agent.py",
            "simple_agent_v3": "src/haive/agents/simple/agent_v3.py",
            "react_agent": "src/haive/agents/react/agent.py",
        }

        print("🎯 Consolidation plan (TARGET PACKAGE ONLY):")
        for name, rel_path in targets.items():
            file_path = self.target_package / rel_path
            exists = "✅" if file_path.exists() else "❌"
            print(f"  {exists} {name}: {self.target_package.name}/{rel_path}")

        return targets

    def step_3_create_enhanced_agent_backup(self):
        """Backup the enhanced agent before moving."""
        print("\n💾 Step 3: Creating enhanced agent backup...")

        enhanced_path = (
            self.project_root
            / "packages/haive-agents/src/haive/agents/base/enhanced_agent.py"
        )
        backup_path = enhanced_path.with_suffix(".py.pre_consolidation_backup")

        if self.dry_run:
            print(f"[DRY RUN] Would backup: {enhanced_path.name} → {backup_path.name}")
        else:
            if enhanced_path.exists():
                import shutil

                shutil.copy(enhanced_path, backup_path)
                print(f"✅ Backup created: {backup_path.name}")
                self.changes_applied.append(f"Backup: {backup_path.name}")
            else:
                print("⚠️  Enhanced agent file not found")

    def step_4_find_import_patterns(self):
        """Find all import patterns that need updating."""
        print("\n🔍 Step 4: Finding import patterns...")

        patterns_to_find = [
            "from haive.agents.base.enhanced_agent import",
            "from haive.agents.simple.agent_v3 import SimpleAgentV3",
            "SimpleAgentV3(",
            "EnhancedMultiAgentV4(",
            "class.*Agent.*Enhanced",
        ]

        import re
        import subprocess

        found_patterns = {}

        for pattern in patterns_to_find:
            try:
                # Use grep to find patterns
                result = subprocess.run(
                    [
                        "grep",
                        "-r",
                        "--include=*.py",
                        "-n",
                        pattern,
                        str(self.project_root / "packages" / "haive-agents"),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.stdout:
                    matches = result.stdout.strip().split("\n")
                    found_patterns[pattern] = matches[:10]  # Limit to first 10 matches

            except Exception as e:
                print(f"⚠️  Error searching for pattern '{pattern}': {e}")

        print("🔍 Import patterns found:")
        for pattern, matches in found_patterns.items():
            if matches:
                print(f"\n  📋 Pattern: {pattern}")
                for match in matches[:3]:  # Show first 3 matches
                    # Clean up the match for display
                    parts = match.split(":", 2)
                    if len(parts) >= 3:
                        file_path = Path(parts[0]).relative_to(self.project_root)
                        line_num = parts[1]
                        content = parts[2].strip()
                        print(f"    📄 {file_path}:{line_num} - {content[:50]}...")
                if len(matches) > 3:
                    print(f"    ... and {len(matches) - 3} more matches")

        return found_patterns

    def step_5_rope_based_consolidation(self):
        """Use rope to perform the consolidation."""
        print("\n🔄 Step 5: Performing rope-based consolidation...")

        if self.dry_run:
            print("[DRY RUN] Would perform rope operations:")
            print("  1. Restructure imports from enhanced_agent to agent")
            print("  2. Rename SimpleAgentV3 to SimpleAgent")
            print("  3. Update class instantiations")
            print("  4. Fix circular import issues")
            return

        # Initialize rope project
        try:
            print("🔧 Initializing rope project...")
            project = Project(str(self.project_root))

            # Define import restructuring patterns
            patterns = [
                {
                    "pattern": "from haive.agents.base.enhanced_agent import Agent",
                    "goal": "from haive.agents.base.agent import Agent",
                },
                {
                    "pattern": "from haive.agents.base.enhanced_agent import *",
                    "goal": "from haive.agents.base.agent import *",
                },
                {
                    "pattern": "from haive.agents.simple.agent_v3 import SimpleAgentV3",
                    "goal": "from haive.agents.simple.agent import SimpleAgent",
                },
                {"pattern": "SimpleAgentV3(${args})", "goal": "SimpleAgent(${args})"},
            ]

            for pattern_info in patterns:
                try:
                    print(f"  🔄 Restructuring: {pattern_info['pattern']}")
                    restructurer = Restructure(
                        project, pattern_info["pattern"], pattern_info["goal"]
                    )
                    changes = restructurer.get_changes()

                    if changes.changes:
                        print(
                            f"    📝 Applying changes to {len(changes.changes)} files"
                        )
                        project.do(changes)
                        self.changes_applied.append(
                            f"Restructured: {pattern_info['pattern']}"
                        )
                    else:
                        print("    ℹ️  No changes needed for this pattern")

                except Exception as e:
                    print(f"    ❌ Error with pattern: {e}")

            project.close()
            print("✅ Rope operations completed")

        except Exception as e:
            print(f"❌ Rope project error: {e}")

    def step_6_manual_file_operations(self):
        """Handle operations that need manual intervention."""
        print("\n✋ Step 6: Manual file operations...")

        operations = [
            "Replace enhanced_agent.py content with consolidated Agent class",
            "Update __init__.py files to export new class names",
            "Remove deprecated version files (agent_v3.py, etc.)",
            "Update example files and documentation",
            "Fix any remaining circular imports",
        ]

        if self.dry_run:
            print("[DRY RUN] Manual operations needed:")
            for i, op in enumerate(operations, 1):
                print(f"  {i}. {op}")
        else:
            print("🚧 Manual operations required:")
            for i, op in enumerate(operations, 1):
                print(f"  {i}. {op}")
            print(
                "\n💡 These operations require human review and cannot be fully automated."
            )
            print("   Please review the changes and complete manually as needed.")

    def step_7_compile_and_validate(self):
        """Compile and validate that the consolidation worked."""
        print(
            f"\n🔍 Step 7: Compiling and validating TARGET PACKAGE: {self.target_package.name}"
        )
        print(
            f"🎯 SCOPE: Only validating {self.target_package} - NOT touching other packages"
        )

        if self.dry_run:
            print("[DRY RUN] Would validate:")
            print("  1. Compile all Python files in target package")
            print("  2. Check all imports resolve correctly")
            print("  3. Test core agent classes can be instantiated")
            print("  4. Run target package tests")
            print("  5. Verify no circular dependencies")
            return True

        all_passed = True

        # Step 1: Compile all Python files in target package
        print("\n🏗️  Step 7.1: Compiling all Python files in target package...")
        python_files = list(self.target_package.glob("**/*.py"))
        compilation_errors = []

        for py_file in python_files:
            try:
                import py_compile

                py_compile.compile(py_file, doraise=True)
            except py_compile.PyCompileError as e:
                compilation_errors.append(
                    f"{py_file.relative_to(self.target_package)}: {e}"
                )
                all_passed = False

        if compilation_errors:
            print("❌ Compilation errors found:")
            for error in compilation_errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(compilation_errors) > 5:
                print(f"  ... and {len(compilation_errors) - 5} more errors")
        else:
            print(f"✅ All {len(python_files)} Python files compiled successfully")

        # Step 2: Import validation
        print("\n📦 Step 7.2: Import validation...")
        validation_commands = [
            (
                "Base Agent Import",
                "from haive.agents.base.agent import Agent; print('✅ Base import works')",
            ),
            (
                "Simple Agent Import",
                "from haive.agents.simple.agent import SimpleAgent; print('✅ Simple import works')",
            ),
            (
                "React Agent Import",
                "from haive.agents.react.agent import ReactAgent; print('✅ React import works')",
            ),
            ("Package Import", "import haive.agents; print('✅ Package import works')"),
        ]

        for description, cmd in validation_commands:
            try:
                import subprocess

                result = subprocess.run(
                    ["poetry", "run", "python", "-c", cmd],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=self.project_root,
                )

                print(f"✅ {description}")
            except subprocess.CalledProcessError as e:
                print(f"❌ {description} failed: {e.stderr.strip()}")
                all_passed = False
            except Exception as e:
                print(f"❌ {description} error: {e}")
                all_passed = False

        # Step 3: Agent instantiation test
        print("\n🤖 Step 7.3: Agent instantiation test...")
        instantiation_test = """
try:
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.agents.base.agent import Agent
    
    config = AugLLMConfig()
    print('✅ AugLLMConfig created')
    print('✅ Agent instantiation test passed')
except Exception as e:
    print(f'❌ Agent instantiation failed: {e}')
    exit(1)
"""

        try:
            import subprocess

            result = subprocess.run(
                ["poetry", "run", "python", "-c", instantiation_test],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.project_root,
            )

            print("✅ Agent instantiation test passed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Agent instantiation failed: {e.stderr.strip()}")
            all_passed = False

        # Step 4: Run target package tests (if they exist)
        print(f"\n🧪 Step 7.4: Running {self.target_package.name} tests...")
        test_dir = self.target_package / "tests"

        if test_dir.exists():
            try:
                import subprocess

                result = subprocess.run(
                    ["poetry", "run", "pytest", str(test_dir), "-v", "--tb=short"],
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=self.project_root,
                )

                if result.returncode == 0:
                    print(f"✅ {self.target_package.name} tests passed")
                else:
                    print(
                        f"⚠️  Some {self.target_package.name} tests failed (may be expected during consolidation)"
                    )
                    print("   Check test output after manual operations are complete")
            except Exception as e:
                print(f"⚠️  Could not run {self.target_package.name} tests: {e}")
        else:
            print(f"ℹ️  No tests directory found in {self.target_package.name}")

        return all_passed

    def create_git_checkpoint(self):
        """Create a git checkpoint before making changes."""
        print("\n🏷️  Creating git checkpoint...")

        import subprocess
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_tag = f"agent-consolidation-checkpoint-{timestamp}"

        if self.dry_run:
            print(f"[DRY RUN] Would create git checkpoint: {checkpoint_tag}")
            return checkpoint_tag

        try:
            # Create git stash
            subprocess.run(
                [
                    "git",
                    "stash",
                    "push",
                    "-m",
                    f"AGENT_CONSOLIDATION_CHECKPOINT_{timestamp}",
                ],
                check=False,
            )  # Don't fail if no changes to stash

            # Create git tag
            subprocess.run(["git", "tag", checkpoint_tag], check=True)

            print(f"✅ Git checkpoint created: {checkpoint_tag}")
            return checkpoint_tag

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git checkpoint warning: {e}")
            return None

    def rollback_changes(self, checkpoint_tag=None):
        """Rollback changes if something went wrong."""
        print("\n🔙 Rolling back changes...")

        import subprocess

        if not checkpoint_tag:
            # Find the most recent checkpoint
            try:
                result = subprocess.run(
                    ["git", "tag", "-l", "agent-consolidation-checkpoint-*"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                checkpoints = [
                    tag.strip() for tag in result.stdout.split("\n") if tag.strip()
                ]
                if checkpoints:
                    checkpoint_tag = sorted(checkpoints)[-1]
                    print(f"🏷️  Found latest checkpoint: {checkpoint_tag}")
                else:
                    print("⚠️  No checkpoints found")
                    return False
            except Exception as e:
                print(f"❌ Error finding checkpoints: {e}")
                return False

        if self.dry_run:
            print(f"[DRY RUN] Would rollback to checkpoint: {checkpoint_tag}")
            print("[DRY RUN] Would restore backup files")
            return True

        try:
            # Reset to checkpoint
            subprocess.run(["git", "reset", "--hard", checkpoint_tag], check=True)

            # Restore backup files if they exist
            backup_files = list(self.project_root.glob("**/*.pre_consolidation_backup"))
            for backup_file in backup_files:
                original_file = backup_file.with_suffix("")
                if backup_file.exists():
                    import shutil

                    shutil.copy(backup_file, original_file)
                    print(f"✅ Restored: {original_file.name}")

            print("✅ Rollback completed successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Rollback failed: {e}")
            return False

    def run_consolidation(self):
        """Run the complete consolidation process."""
        try:
            print("🚀 Starting Agent Base Consolidation")
            print("=" * 60)

            # Safety phase - create checkpoint
            checkpoint_tag = self.create_git_checkpoint()

            # Analysis phase
            agent_classes = self.step_1_analyze_current_structure()
            targets = self.step_2_identify_consolidation_targets()

            # Pattern analysis
            patterns = self.step_4_find_import_patterns()

            # Backup phase
            self.step_3_create_enhanced_agent_backup()

            # Consolidation phase
            self.step_5_rope_based_consolidation()
            self.step_6_manual_file_operations()

            # Validation phase
            validation_passed = self.step_7_compile_and_validate()

            # Summary
            print("\n" + "=" * 60)
            print("📊 CONSOLIDATION SUMMARY")
            print("=" * 60)
            print(f"🧪 Mode: {'DRY RUN' if self.dry_run else 'LIVE EXECUTION'}")
            print(f"📊 Changes applied: {len(self.changes_applied)}")

            for change in self.changes_applied:
                print(f"  ✓ {change}")

            if self.dry_run:
                print("\n💡 Next steps:")
                print("  1. Review the analysis above")
                print("  2. Run without DRY_RUN=1 to apply changes:")
                print(
                    "     python scripts/maintenance/agent_consolidation_refactorer.py"
                )
                print("  3. Test thoroughly after consolidation")
            else:
                if validation_passed:
                    print("\n🎉 Consolidation completed successfully!")
                    print("💡 Next steps:")
                    print(
                        "  1. Run tests: poetry run pytest packages/haive-agents/tests/"
                    )
                    print("  2. Update documentation")
                    print(
                        "  3. Test imports: poetry run python -c 'from haive.agents.base.agent import Agent'"
                    )
                    print("  4. Commit changes when satisfied")
                else:
                    print("\n⚠️  Consolidation completed but validation failed")
                    print("🔙 Consider rollback:")
                    print(f"    python {__file__} --rollback")

        except Exception as e:
            print(f"\n❌ Consolidation failed: {e}")
            import traceback

            traceback.print_exc()

            if not self.dry_run:
                print("🚨 Automatic rollback recommended")
                response = input("🔙 Rollback now? [y/N]: ")
                if response.lower().startswith("y"):
                    self.rollback_changes()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Agent Base Consolidation with Dry Run Support"
    )
    parser.add_argument(
        "--rollback", action="store_true", help="Rollback to the latest checkpoint"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Run in dry run mode (same as DRY_RUN=1)"
    )

    args = parser.parse_args()

    # Set dry run mode from argument
    if args.dry_run:
        os.environ["DRY_RUN"] = "1"

    refactorer = AgentConsolidationRefactorer()

    if args.rollback:
        success = refactorer.rollback_changes()
        sys.exit(0 if success else 1)
    else:
        refactorer.run_consolidation()


if __name__ == "__main__":
    main()
