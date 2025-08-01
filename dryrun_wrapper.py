#!/usr/bin/env python3
"""Universal dry-run wrapper for any command.

This wrapper can be used to add dry-run capabilities to any command,
making it safe to test operations before actually running them.

Examples:
    # Wrap any command with dry-run
    DRY_RUN=1 python dryrun_wrapper.py -- python my_script.py --arg value

    # Use in taskipy
    my-task-dry = "DRY_RUN=1 python scripts/maintenance/dryrun_wrapper.py -- python my_script.py"
    my-task = "python scripts/maintenance/dryrun_wrapper.py -- python my_script.py"

    # Complex commands
    DRY_RUN=1 python dryrun_wrapper.py -- poetry run python -m package.module --deploy
"""

import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class UniversalDryRunWrapper:
    """Universal wrapper that adds dry-run capabilities to any command."""

    def __init__(self):
        self.dry_run = self._check_dry_run_mode()
        self.verbose = self._check_verbose_mode()

    def _check_dry_run_mode(self) -> bool:
        """Check if dry-run mode is enabled via environment."""
        return os.getenv("DRY_RUN", "").lower() in ("1", "true", "yes", "on")

    def _check_verbose_mode(self) -> bool:
        """Check if verbose mode is enabled."""
        return os.getenv("VERBOSE", "").lower() in ("1", "true", "yes", "on")

    def _show_banner(self, command: List[str]):
        """Show banner with command info."""
        if self.dry_run:
            print("🔍" * 20)
            print("🔍  DRY RUN MODE ACTIVE  🔍")
            print("🔍" * 20)
        else:
            print("🚀" * 20)
            print("🚀  EXECUTING COMMAND   🚀")
            print("🚀" * 20)

        print(f"Command: {' '.join(command)}")
        print(f"Working Directory: {Path.cwd()}")
        print(f"Environment: DRY_RUN={self.dry_run}, VERBOSE={self.verbose}")
        print("=" * 60)

    def _analyze_command(self, command: List[str]) -> dict:
        """Analyze the command to understand what it might do."""
        analysis = {
            "potentially_destructive": False,
            "file_operations": False,
            "network_operations": False,
            "system_changes": False,
            "git_operations": False,
            "package_operations": False,
        }

        command_str = " ".join(command).lower()

        # Check for potentially destructive operations
        destructive_patterns = [
            "rm ",
            "del ",
            "delete",
            "remove",
            "drop",
            "truncate",
            "format",
            "wipe",
            "destroy",
            "purge",
            "--force",
            "-f",
        ]
        if any(pattern in command_str for pattern in destructive_patterns):
            analysis["potentially_destructive"] = True

        # Check for file operations
        file_patterns = [
            "cp ",
            "copy",
            "mv ",
            "move",
            "mkdir",
            "touch",
            "write",
            "create",
            "edit",
            "modify",
            "update",
            "backup",
        ]
        if any(pattern in command_str for pattern in file_patterns):
            analysis["file_operations"] = True

        # Check for network operations
        network_patterns = [
            "curl",
            "wget",
            "http",
            "https",
            "ftp",
            "ssh",
            "scp",
            "download",
            "upload",
            "push",
            "pull",
            "clone",
        ]
        if any(pattern in command_str for pattern in network_patterns):
            analysis["network_operations"] = True

        # Check for system changes
        system_patterns = [
            "install",
            "uninstall",
            "upgrade",
            "update",
            "configure",
            "systemctl",
            "service",
            "daemon",
            "crontab",
        ]
        if any(pattern in command_str for pattern in system_patterns):
            analysis["system_changes"] = True

        # Check for git operations
        git_patterns = [
            "git add",
            "git commit",
            "git push",
            "git merge",
            "git rebase",
            "git reset",
            "git checkout",
            "git branch",
            "git tag",
        ]
        if any(pattern in command_str for pattern in git_patterns):
            analysis["git_operations"] = True

        # Check for package operations
        package_patterns = [
            "poetry add",
            "poetry remove",
            "pip install",
            "pip uninstall",
            "npm install",
            "npm uninstall",
            "apt install",
            "yum install",
        ]
        if any(pattern in command_str for pattern in package_patterns):
            analysis["package_operations"] = True

        return analysis

    def _show_analysis(self, analysis: dict):
        """Show command analysis."""
        print("\n📊 Command Analysis:")

        risk_level = "🟢 LOW"
        if analysis["potentially_destructive"]:
            risk_level = "🔴 HIGH"
        elif analysis["system_changes"] or analysis["git_operations"]:
            risk_level = "🟡 MEDIUM"
        elif analysis["file_operations"] or analysis["package_operations"]:
            risk_level = "🟡 MEDIUM"

        print(f"   Risk Level: {risk_level}")

        operations = []
        if analysis["file_operations"]:
            operations.append("📁 File Operations")
        if analysis["network_operations"]:
            operations.append("🌐 Network Operations")
        if analysis["system_changes"]:
            operations.append("⚙️  System Changes")
        if analysis["git_operations"]:
            operations.append("🔀 Git Operations")
        if analysis["package_operations"]:
            operations.append("📦 Package Operations")
        if analysis["potentially_destructive"]:
            operations.append("⚠️  Potentially Destructive")

        if operations:
            print(f"   Detected: {', '.join(operations)}")
        else:
            print("   Detected: 🔍 Analysis/Read Operations")

    def _execute_command(self, command: List[str]) -> int:
        """Execute the command (real or dry-run)."""
        if self.dry_run:
            print(f"\n[DRY RUN] Would execute: {' '.join(command)}")

            # Try to provide more specific dry-run feedback
            if "python" in command[0]:
                print("[DRY RUN] Python script would be executed")
                if "--help" not in command and "-h" not in command:
                    # Try to run with --help to show what it would do
                    try:
                        help_cmd = command + ["--help"]
                        print(f"[DRY RUN] Trying: {' '.join(help_cmd)}")
                        result = subprocess.run(
                            help_cmd, capture_output=True, text=True, timeout=10
                        )
                        if result.returncode == 0 and result.stdout:
                            print("[DRY RUN] Available options:")
                            print(
                                result.stdout[:500] + "..."
                                if len(result.stdout) > 500
                                else result.stdout
                            )
                    except:
                        pass

            print("[DRY RUN] Command execution skipped")
            return 0
        else:
            print(f"\n🚀 Executing: {' '.join(command)}")
            try:
                result = subprocess.run(command, cwd=Path.cwd(), env=os.environ.copy())
                return result.returncode
            except KeyboardInterrupt:
                print("\n⚠️  Command interrupted by user")
                return 130
            except Exception as e:
                print(f"\n❌ Command failed: {e}")
                return 1

    def run(self, command: List[str]) -> int:
        """Run the command with dry-run wrapper."""
        self._show_banner(command)

        analysis = self._analyze_command(command)
        self._show_analysis(analysis)

        if self.dry_run and analysis["potentially_destructive"]:
            print("\n⚠️  WARNING: Command appears potentially destructive!")
            print("   This is why dry-run mode is valuable.")

        if self.verbose:
            print(f"\n🔍 Verbose Info:")
            print(f"   Command length: {len(command)} arguments")
            print(f"   Working directory: {Path.cwd()}")
            print(f"   Environment variables: DRY_RUN={os.getenv('DRY_RUN')}")

        return self._execute_command(command)


def main():
    """Main entry point for the dry-run wrapper."""
    if len(sys.argv) < 2:
        print(
            """Universal Dry-Run Wrapper

Usage:
    python dryrun_wrapper.py -- <command> [args...]
    
Examples:
    # Basic usage
    python dryrun_wrapper.py -- ls -la
    
    # With dry-run mode
    DRY_RUN=1 python dryrun_wrapper.py -- rm -rf dangerous_folder
    
    # Complex command
    DRY_RUN=1 python dryrun_wrapper.py -- poetry run python my_script.py --deploy --force
    
    # In taskipy (pyproject.toml):
    [tool.taskipy.tasks]
    my-task = "python scripts/maintenance/dryrun_wrapper.py -- python my_script.py"
    my-task-dry = "DRY_RUN=1 python scripts/maintenance/dryrun_wrapper.py -- python my_script.py"
    
Environment Variables:
    DRY_RUN=1     Enable dry-run mode (safe simulation)
    VERBOSE=1     Enable verbose output
        """
        )
        return 1

    # Find the -- separator
    try:
        separator_index = sys.argv.index("--")
        command = sys.argv[separator_index + 1 :]
    except ValueError:
        # No -- separator, treat everything after script name as command
        command = sys.argv[1:]

    if not command:
        print("❌ No command specified")
        return 1

    wrapper = UniversalDryRunWrapper()
    return wrapper.run(command)


if __name__ == "__main__":
    sys.exit(main())
