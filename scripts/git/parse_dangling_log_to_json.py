#!/usr/bin/env python3
"""Parse the dangling objects log file and create a JSON file for analysis."""

from datetime import datetime
import json
from pathlib import Path
import re
import subprocess


def parse_dangling_log(log_file: str, repo_path: str = "packages/haive-agents"):
    """Parse dangling objects from git fsck log and create JSON."""
    print(f"Parsing {log_file}...")

    # Read log file
    with open(log_file) as f:
        lines = f.readlines()

    # Parse objects
    dangling_objects = {"commits": [], "trees": [], "blobs": [], "tags": []}

    # Extract object SHAs and types
    for line in lines:
        match = re.match(
            f"(dangling )?(commit|tree|blob|tag)\s+([0-9a-f]{40})", line.strip()
        )
        if match:
            obj_type = match.group(2)
            obj_sha = match.group(3)

            if obj_type == "commit":
                # Get detailed commit info
                commit_info = get_commit_info(obj_sha, repo_path)
                if commit_info:
                    dangling_objects["commits"].append(commit_info)
            elif obj_type == "tree":
                tree_info = {"sha": obj_sha, "type": "tree"}
                # Try to get tree info
                try:
                    tree_data = subprocess.check_output(
                        ["git", "ls-tree", obj_sha],
                        cwd=repo_path,
                        stderr=subprocess.DEVNULL,
                        text=True,
                    )
                    entries = tree_data.strip().split("\n") if tree_data.strip() else []
                    tree_info["entry_count"] = len(entries)
                    tree_info["entries"] = []
                    for entry in entries[:10]:  # First 10 entries
                        parts = entry.split(None, 3)
                        if len(parts) >= 4:
                            tree_info["entries"].append(
                                {
                                    "mode": parts[0],
                                    "type": parts[1],
                                    "sha": parts[2],
                                    "path": parts[3],
                                }
                            )
                except:
                    tree_info["entry_count"] = 0

                dangling_objects["trees"].append(tree_info)
            elif obj_type == "blob":
                blob_info = {"sha": obj_sha, "type": "blob"}
                # Try to get blob size
                try:
                    size_output = subprocess.check_output(
                        ["git", "cat-file", "-s", obj_sha],
                        cwd=repo_path,
                        stderr=subprocess.DEVNULL,
                        text=True,
                    )
                    blob_info["size"] = int(size_output.strip())
                except:
                    blob_info["size"] = 0

                dangling_objects["blobs"].append(blob_info)
            elif obj_type == "tag":
                dangling_objects["tags"].append({"sha": obj_sha, "type": "tag"})

    # Create output structure
    output = {
        "metadata": {
            "repo_path": repo_path,
            "scan_date": datetime.now().isoformat(),
            "summary": {
                "total_dangling_commits": len(dangling_objects["commits"]),
                "total_dangling_trees": len(dangling_objects["trees"]),
                "total_dangling_blobs": len(dangling_objects["blobs"]),
                "total_dangling_tags": len(dangling_objects["tags"]),
            },
        },
        "objects": dangling_objects,
    }

    # Save to JSON
    json_file = "haive-agents-dangling-objects.json"
    with open(json_file, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n✅ Created {json_file}")
    print(f"   Commits: {len(dangling_objects['commits'])}")
    print(f"   Trees: {len(dangling_objects['trees'])}")
    print(f"   Blobs: {len(dangling_objects['blobs'])}")
    print(f"   Tags: {len(dangling_objects['tags'])}")

    return json_file


def get_commit_info(sha: str, repo_path: str):
    """Get detailed information about a commit."""
    try:
        # Get commit details
        commit_data = subprocess.check_output(
            [
                "git",
                "show",
                "--no-patch",
                "--format=format:%H|%P|%T|%an|%ae|%at|%cn|%ce|%ct|%s|%b",
                sha,
            ],
            cwd=repo_path,
            stderr=subprocess.DEVNULL,
            text=True,
        )

        parts = commit_data.strip().split("|", 10)
        if len(parts) >= 10:
            commit_info = {
                "sha": parts[0],
                "parent_shas": parts[1].split() if parts[1] else [],
                "tree_sha": parts[2],
                "author_name": parts[3],
                "author_email": parts[4],
                "author_timestamp": int(parts[5]) * 1000,  # Convert to milliseconds
                "committer_name": parts[6],
                "committer_email": parts[7],
                "committer_timestamp": int(parts[8]) * 1000,
                "subject": parts[9],
                "body": parts[10] if len(parts) > 10 else "",
            }

            # Add formatted dates
            commit_info["author_date"] = datetime.fromtimestamp(
                int(parts[5])
            ).isoformat()
            commit_info["committer_date"] = datetime.fromtimestamp(
                int(parts[8])
            ).isoformat()

            # Get file changes
            try:
                changes = subprocess.check_output(
                    ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", sha],
                    cwd=repo_path,
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                commit_info["changes"] = [f for f in changes.strip().split("\n") if f]
            except:
                commit_info["changes"] = []

            return commit_info
    except:
        return None


if __name__ == "__main__":
    # Find the log file
    log_file = "dangling_objects_haive_agents.log"

    if not Path(log_file).exists():
        print(f"Error: {log_file} not found")
        print("Available log files:")
        for f in Path(".").glob("*dangling*.log"):
            print(f"  - {f}")
        exit(1)

    # Parse and create JSON
    json_file = parse_dangling_log(log_file)
    print("\nNow you can run: python scripts/git/analyze_recent_dangling_objects.py")
