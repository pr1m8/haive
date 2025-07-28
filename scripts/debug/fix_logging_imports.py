#!/usr/bin/env python3
"""Fix logging imports in conversation agents."""

import re
from pathlib import Path


def fix_logging_imports():
    """Replace rich_logger imports with standard logging."""
    # Files that need fixing
    files_to_fix = [
        "packages/haive-agents/tests/multi/test_recompile_mixin.py",
        "packages/haive-agents/src/haive/agents/conversation/collaberative/agent.py",
        "packages/haive-agents/src/haive/agents/conversation/base/state.py",
        "packages/haive-agents/src/haive/agents/conversation/base/agent.py",
        "packages/haive-agents/src/haive/agents/conversation/round_robin/agent.py",
        "packages/haive-agents/src/haive/agents/conversation/debate/agent.py",
        "packages/haive-agents/src/haive/agents/conversation/directed/state.py",
        "packages/haive-agents/src/haive/agents/conversation/directed/agent.py",
        "packages/haive-agents/src/haive/agents/conversation/social_media/state.py",
        "packages/haive-agents/src/haive/agents/conversation/social_media/agent.py",
    ]

    fixed_count = 0

    for file_path in files_to_fix:
        path = Path(file_path)
        if not path.exists():
            continue


        # Read the file
        with open(path, encoding="utf-8") as f:
            content = f.read()

        # Replace the import
        old_import = "from haive.core.logging.rich_logger import LogLevel, get_logger"
        new_import = "import logging"

        if old_import in content:
            content = content.replace(old_import, new_import)

            # Replace get_logger() calls with logging.getLogger()
            content = re.sub(r"get_logger\(\)", "logging.getLogger(__name__)", content)
            content = re.sub(
                r'get_logger\("([^"]+)"\)', r'logging.getLogger("\1")', content
            )

            # Replace LogLevel references with logging levels
            content = content.replace("LogLevel.DEBUG", "logging.DEBUG")
            content = content.replace("LogLevel.INFO", "logging.INFO")
            content = content.replace("LogLevel.WARNING", "logging.WARNING")
            content = content.replace("LogLevel.ERROR", "logging.ERROR")

            # Write back
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            fixed_count += 1
        else:
            pass
if __name__ == "__main__":
    fix_logging_imports()
