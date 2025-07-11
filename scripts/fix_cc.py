#!/usr/bin/env python3
"""clean_and_export.py.

1. Cleans all JSONL files under ~/.claude/projects/ by removing invalid JSON lines.
2. Optionally filters messages from today.
3. Outputs cleaned files to a temporary directory.
4. Runs 'uvx claude-code-log' on the cleaned directory to generate HTML.
"""

import json
import os
import shutil
import subprocess
import tempfile
from datetime import date, datetime
from pathlib import Path

# Configuration: adjust as needed
PROJECTS_DIR = Path.home() / ".claude" / "projects"
TODAY_ONLY = False  # Set False to include all dates


def is_today_timestamp(ts_str):
    """Return True if ISO8601 timestamp is from today."""
    try:
        ts = datetime.fromisoformat(ts_str.rstrip("Z"))
        return ts.date() == date.today()
    except Exception:
        return False


def clean_file(src_path, dst_path):
    with open(src_path, encoding="utf-8", errors="ignore") as fin, open(
        dst_path, "w", encoding="utf-8"
    ) as fout:
        for raw in fin:
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue
            # Only include today's entries (if desired)...
            text = json.dumps(obj, ensure_ascii=False)
            # Normalize surrogates: pass them through, then replace any lone halves
            safe = text.encode("utf-8", "surrogatepass").decode("utf-8", "replace")
            fout.write(safe + "\n")


def main():
    if not PROJECTS_DIR.exists():
        return

    # Create a temporary clean workspace
    temp_dir = Path(tempfile.mkdtemp(prefix="claude_clean_"))

    # Mirror directory structure and clean each JSONL
    for root, _dirs, files in os.walk(PROJECTS_DIR):
        rel = Path(root).relative_to(PROJECTS_DIR)
        dst_root = temp_dir / rel
        dst_root.mkdir(parents=True, exist_ok=True)
        for fn in files:
            if fn.endswith(".jsonl"):
                src = Path(root) / fn
                dst = dst_root / fn
                clean_file(src, dst)

    # Invoke claude-code-log on cleaned data
    cmd = ["uvx", "claude-code-log", str(temp_dir), "--open-browser"]
    subprocess.run(cmd, check=False)

    # Note: temporary directory remains for inspection if needed


if __name__ == "__main__":
    main()
