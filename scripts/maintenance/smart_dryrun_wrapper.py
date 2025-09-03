#!/usr/bin/env python3
"""Universal smart dry-run wrapper for any command.

This wrapper intelligently adds --dry-run capabilities to any command,
making it safe to test operations before actually running them.

Features:
- Automatically detects if command supports --dry-run, --preview, etc.
- Falls back to environment variable DRY_RUN=1 if needed
- Interactive mode with confirmation prompts
- Supports adding target paths/directories to commands
- Works with any command line tool

Examples:
    # Test what absolufy-imports would do
    DRY_RUN=1 python scripts/smart_dryrun_wrapper.py --target packages/haive-dataflow -- poetry run absolufy-imports

    # Interactive confirmation
    INTERACTIVE=1 python scripts/smart_dryrun_wrapper.py --target haive-core -- poetry run ruff check --fix

    # Direct dry-run flag injection
    python scripts/smart_dryrun_wrapper.py --dry-run -- rm -rf logs/
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


class SmartDryRunWrapper:
    """Smart wrapper that adds dry-run capabilities to any command."""

    # Known dry-run flags for common tools
    DRY_RUN_FLAGS = {
        'absolufy-imports': ['--diff'],  # Shows what would change
        'ruff': ['--diff'],  # Shows what would be fixed
        'black': ['--diff'],  # Shows what would be formatted
        'isort': ['--diff'],  # Shows what would be sorted
        'autoflake': ['--check'],  # Check mode
        'autopep8': ['--diff'],  # Shows changes
        'yapf': ['--diff'],  # Shows changes
        'git': ['--dry-run'],  # Git operations
        'rm': ['-i'],  # Interactive mode as fallback
        'mv': ['-i'],  # Interactive mode as fallback
        'cp': ['-i'],  # Interactive mode as fallback
        'rsync': ['--dry-run'],  # rsync dry run
        'pip': ['--dry-run'],  # pip operations
        'poetry': ['--dry-run'],  # poetry operations (some commands)
    }

    # Tools that support preview/check modes
    PREVIEW_FLAGS = {
        'pre-commit': ['--dry-run'],
        'mypy': ['--no-incremental'],  # Forces full check
        'pylint': ['--help-msg'],  # Help mode as fallback
    }

    def __init__(self):
        self.dry_run = os.getenv('DRY_RUN', '').lower() in ('1', 'true', 'yes')
        self.interactive = os.getenv('INTERACTIVE', '').lower() in ('1', 'true', 'yes')
        self.target_path = None

    def detect_tool_name(self, command: list[str]) -> str | None:
        """Detect the main tool from command."""
        if not command:
            return None

        # Handle poetry run commands
        if len(command) >= 3 and command[0] == 'poetry' and command[1] == 'run':
            return command[2]

        # Handle direct commands
        return Path(command[0]).name

    def get_dry_run_flags(self, tool_name: str) -> list[str]:
        """Get appropriate dry-run flags for a tool."""
        flags = []

        # Check known dry-run flags
        if tool_name in self.DRY_RUN_FLAGS:
            flags.extend(self.DRY_RUN_FLAGS[tool_name])
        elif tool_name in self.PREVIEW_FLAGS:
            flags.extend(self.PREVIEW_FLAGS[tool_name])
        else:
            # Try common dry-run flags
            # Just return the most common one
            flags.append('--dry-run')

        return flags

    def check_flag_support(self, command: list[str], flag: str) -> bool:
        """Check if command supports a specific flag."""
        try:
            # Try running with --help to see available options
            help_cmd = [*command, '--help']
            result = subprocess.run(
                help_cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return flag.replace('--', '') in result.stdout.lower()
        except (
            subprocess.TimeoutExpired,
            subprocess.SubprocessError,
            FileNotFoundError,
        ):
            return False

    def add_target_to_command(self, command: list[str]) -> list[str]:
        """Add target path to command if specified."""
        if not self.target_path:
            return command

        # For absolufy-imports, add as positional argument
        tool_name = self.detect_tool_name(command)
        if tool_name == 'absolufy-imports':
            # Add target as positional argument
            return [*command, str(self.target_path)]

        # For other tools, add at the end
        return [*command, str(self.target_path)]

    def build_dry_run_command(self, command: list[str]) -> tuple[list[str], bool]:
        """Build command with dry-run flags if possible."""
        if not command:
            return command, False

        tool_name = self.detect_tool_name(command)
        if not tool_name:
            return command, False

        # Add target path if specified
        command = self.add_target_to_command(command)

        # If not in dry-run mode, return original
        if not self.dry_run:
            return command, False

        # Try to add dry-run flags
        dry_run_flags = self.get_dry_run_flags(tool_name)

        for flag in dry_run_flags:
            if self.check_flag_support(command, flag):
                return [*command, flag], True

        # If no dry-run flag works, we'll use environment variable
        return command, False

    def confirm_execution(self, command: list[str]) -> bool:
        """Ask user for confirmation in interactive mode."""
        if not self.interactive:
            return True

        while True:
            response = input('\n❓ Continue? [y/N]: ').strip().lower()
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no', ''):
                return False

    def execute_command(self, command: list[str]) -> int:
        """Execute the command with appropriate handling."""
        modified_command, has_dry_run_flag = self.build_dry_run_command(command)

        # Show what we're about to do
        if self.dry_run and not has_dry_run_flag:
            return 0
        if self.dry_run and has_dry_run_flag:
            pass  # Command already has dry-run flag

        # Interactive confirmation
        if not self.confirm_execution(modified_command):
            return 1

        # Execute the command
        try:
            env = os.environ.copy()
            if self.dry_run and not has_dry_run_flag:
                env['DRY_RUN'] = '1'

            result = subprocess.run(modified_command, check=False, env=env)
            return result.returncode
        except FileNotFoundError:
            return 127
        except KeyboardInterrupt:
            return 130
        except Exception:
            return 1


def main():
    """Main entry point."""
    wrapper = SmartDryRunWrapper()

    # Parse arguments
    args = sys.argv[1:]
    command = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '--':
            # Everything after -- is the command
            command = args[i + 1:]
            break
        if arg == '--dry-run':
            wrapper.dry_run = True
        elif arg == '--interactive':
            wrapper.interactive = True
        elif arg == '--target' and i + 1 < len(args):
            wrapper.target_path = Path(args[i + 1])
            i += 1
        elif arg in ('--help', '-h'):
            return 1
        else:
            return 1
        i += 1

    if not command:
        return 1

    return wrapper.execute_command(command)


if __name__ == '__main__':
    sys.exit(main())
