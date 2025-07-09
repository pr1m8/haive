#!/usr/bin/env python3
"""View checkpoint metadata to understand prepared statement errors."""

import json
import os
from datetime import datetime

import psycopg


def view_checkpoint_metadata(thread_id: str = None):
    """View checkpoint metadata for debugging."""
    print("🔍 Viewing Checkpoint Metadata")
    print("=" * 70)

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        print("❌ No connection string")
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

                print(f"\n📊 Found {len(checkpoints)} checkpoints with metadata")

                for thread, cp_id, metadata in checkpoints:
                    print(f"\n📋 Thread: {thread}")
                    print(f"   Checkpoint: {cp_id}")

                    try:
                        meta_dict = (
                            json.loads(metadata)
                            if isinstance(metadata, str)
                            else metadata
                        )

                        # Show key fields
                        if "step" in meta_dict:
                            print(f"   Step: {meta_dict['step']}")

                        if "langgraph_node" in meta_dict:
                            print(f"   Node: {meta_dict['langgraph_node']}")

                        if "error" in meta_dict:
                            print(f"   ❌ Error: {meta_dict['error']}")

                        # Check writes for errors
                        if "writes" in meta_dict:
                            writes = meta_dict["writes"]
                            if isinstance(writes, dict):
                                for node, data in writes.items():
                                    if isinstance(data, dict):
                                        if "error" in data:
                                            print(
                                                f"   ❌ Error in {node}: {data['error']}"
                                            )
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
                                                            print(
                                                                f"   ❌ Error from {contrib[0]}: {content[:100]}..."
                                                            )

                    except Exception as e:
                        print(f"   ⚠️  Error parsing metadata: {e}")

    except Exception as e:
        print(f"❌ Database error: {e}")


def organize_test_files():
    """Organize test files into proper structure."""
    print("\n\n🗂️  Organizing Test Files")
    print("=" * 70)

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
        print(f"📁 {subdir}/: {description}")

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
                        print(f"   ✅ Moved {file} -> {category}/")
                        moved += 1
                    break

    print(f"\n✅ Moved {moved} files")

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

    print("\n✅ Updated README.md")


def main():
    """Run metadata viewing and file organization."""
    import sys

    # View metadata
    if len(sys.argv) > 1:
        thread_id = sys.argv[1]
        print(f"Viewing metadata for thread: {thread_id}")
        view_checkpoint_metadata(thread_id)
    else:
        print("Viewing checkpoints with errors in metadata")
        view_checkpoint_metadata()

    # Organize files
    organize_test_files()


if __name__ == "__main__":
    main()
