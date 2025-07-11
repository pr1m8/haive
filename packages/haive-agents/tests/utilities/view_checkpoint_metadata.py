#!/usr/bin/env python3
"""View checkpoint metadata to understand prepared statement errors."""

import json
import os
from datetime import datetime

import psycopg


def view_checkpoint_metadata(thread_id: str | None = None):
    """View checkpoint metadata for debugging."""

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # Build query
                query = """
                    SELECT
                        thread_id,
                        checkpoint_id,
                        metadata
                    FROM public.checkpoints
                    WHERE metadata IS NOT NULL
                """
                params = []

                if thread_id:
                    query += " AND thread_id = %s"
                    params.append(thread_id)
                else:
                    query += " AND metadata::text LIKE '%error%'"

                query += " ORDER BY checkpoint_id DESC LIMIT 10"

                cur.execute(query, params)
                checkpoints = cur.fetchall()


                for thread, cp_id, metadata in checkpoints:

                    try:
                        meta_dict = (
                            json.loads(metadata)
                            if isinstance(metadata, str)
                            else metadata
                        )

                        # Show key fields
                        if "step" in meta_dict:
                            pass

                        if "langgraph_node" in meta_dict:
                            pass

                        if "error" in meta_dict:
                            pass")

                        # Check writes for errors
                        if "writes" in meta_dict:
                            writes = meta_dict["writes"]
                            if isinstance(writes, dict):
                                for node, data in writes.items():
                                    if isinstance(data, dict):
                                        if "error" in data:
                                            pass
                                        if "process_response" in data:
                                            pr = data["process_response"]
                                            if (
                                                isinstance(pr, dict)
                                                and "contributions" in pr
                                            ):
                                                # Check for errors in contributions
                                                for contrib in pr["contributions"]:
                                                    if (
                                                        isinstance(contrib, list)
                                                        and len(contrib) >= 3
                                                    ):
                                                        content = str(contrib[2])
                                                        if (
                                                            "error" in content.lower()
                                                            or "prepared statement"
                                                            in content.lower()
                                                        ):
                                                            pass

                    except Exception as e:
                        passe}")

    except Exception as e:
        pass")


def organize_test_files():
    """Organize test files into proper structure."""

    test_dir = "/home/will/Projects/haive/backend/haive/tests/persistence_debugging"

    # Create subdirectories
    subdirs = {
        "utilities": "Utility scripts for viewing data",
        "tests": "Test scripts",
        "analysis": "Analysis and debugging scripts",
    }

    for subdir, description in subdirs.items():
        path = os.path.join(test_dir, subdir)
        os.makedirs(path, exist_ok=True)

    # Categorize files
    file_categories = {
        "utilities": ["view_", "check_", "decode_", "supabase_"],
        "tests": ["test_", "verify_"],
        "analysis": ["conversation_status", "extract_"],
    }

    # Move files
    moved = 0
    for file in os.listdir(test_dir):
        if file.endswith(".py") and file != "organize_files.py":
            file_path = os.path.join(test_dir, file)

            # Skip if already in subdirectory
            if os.path.isdir(file_path):
                continue

            # Determine category
            for category, prefixes in file_categories.items():
                if any(file.startswith(prefix) for prefix in prefixes):
                    new_path = os.path.join(test_dir, category, file)
                    if not os.path.exists(new_path):
                        os.rename(file_path, new_path)
                        moved += 1
                    break


    # Update README
    readme_content = """# PostgreSQL Persistence Debugging

## Directory Structure

### utilities/
Utility scripts for viewing database content and debugging:
- `view_*.py` - View various database tables and content
- `check_*.py` - Check system status and configuration
- `decode_*.py` - Decode binary data (msgpack, etc)

### tests/
Test scripts for verifying functionality:
- `test_*.py` - Various test scenarios
- `verify_*.py` - Verification scripts

### analysis/
Analysis and data extraction scripts:
- `conversation_status_summary.py` - Analyze conversation status
- `extract_conversation_outputs.py` - Extract conversation data

### results/
Test results and output files (JSON, logs)

### state_history/
Agent state history files

## Key Fixes Applied

1. **Prepared Statement Conflicts**: Fixed by setting `prepare_threshold=None`
2. **Connection Manager**: Updated to disable prepared statements
3. **Persistence Mixin**: Fixed to handle `persistence=True`
4. **Unique App Names**: Each agent gets unique PostgreSQL app name

## Usage

```bash
# Run a test
python tests/test_all_agents_comprehensive.py

# View errors
python utilities/view_conversation_errors.py

# Check system status
python utilities/check_db.py
```
"""

    with open(os.path.join(test_dir, "README.md"), "w") as f:
        f.write(readme_content)



def main():
    """Run metadata viewing and file organization."""
    import sys

    # View metadata
    if len(sys.argv) > 1:
        thread_id = sys.argv[1]
        view_checkpoint_metadata(thread_id)
    else:
        view_checkpoint_metadata()

    # Organize files
    organize_test_files()


if __name__ == "__main__":
    main()
