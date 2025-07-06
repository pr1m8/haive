#!/usr/bin/env python3
"""Extract and organize conversation agent outputs for easy access.

This script creates consolidated output files in each conversation type's root folder,
making it easy to review the actual conversation results and state data.
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def find_conversation_outputs(base_path: str) -> dict[str, list[str]]:
    """Find all conversation output files organized by type."""
    conversation_types = {}

    # Define conversation type directories
    conv_base = Path(base_path) / "packages/haive-agents/src/haive/agents/conversation"

    for conv_type_dir in conv_base.iterdir():
        if conv_type_dir.is_dir() and conv_type_dir.name != "base":
            conv_type = conv_type_dir.name
            conversation_types[conv_type] = []

            # Find outputs directory
            outputs_dir = conv_type_dir / "outputs"
            if outputs_dir.exists():
                for output_file in outputs_dir.iterdir():
                    if output_file.suffix in [".md", ".json", ".txt"]:
                        conversation_types[conv_type].append(str(output_file))

            # Find state history in resources
            resources_dir = conv_type_dir / "resources/state_history"
            if resources_dir.exists():
                for state_file in resources_dir.iterdir():
                    if state_file.suffix == ".json":
                        conversation_types[conv_type].append(str(state_file))

    return conversation_types


def find_global_state_history(base_path: str) -> list[str]:
    """Find conversation-related state history in global resources."""
    global_resources = Path(base_path) / "packages/haive-agents/resources/state_history"
    conversation_files = []

    if global_resources.exists():
        for state_file in global_resources.iterdir():
            if state_file.suffix == ".json":
                # Check if it's a conversation-related file
                filename = state_file.name.lower()
                if any(
                    keyword in filename
                    for keyword in [
                        "productmanager",
                        "designer",
                        "engineer",
                        "marketer",
                        "conversation",
                        "debate",
                        "collaborative",
                        "round_robin",
                    ]
                ):
                    conversation_files.append(str(state_file))

    return conversation_files


def extract_key_content(file_path: str) -> dict:
    """Extract key content from output files."""
    file_path = Path(file_path)

    if file_path.suffix == ".json":
        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            # Extract key information
            if isinstance(data, list) and len(data) > 0:
                # State history format
                first_entry = data[0]
                if "messages" in first_entry:
                    messages = first_entry["messages"]
                    return {
                        "type": "state_history",
                        "file": str(file_path),
                        "message_count": len(messages),
                        "sample_messages": messages[:3] if len(messages) > 0 else [],
                        "last_modified": datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat(),
                    }

            return {
                "type": "json_data",
                "file": str(file_path),
                "content_keys": (
                    list(data.keys()) if isinstance(data, dict) else "list_format"
                ),
                "last_modified": datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).isoformat(),
            }

        except Exception as e:
            return {"type": "error", "file": str(file_path), "error": str(e)}

    elif file_path.suffix == ".md":
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Extract key information
            lines = content.split("\n")
            return {
                "type": "markdown",
                "file": str(file_path),
                "line_count": len(lines),
                "title": lines[0] if lines else "No title",
                "preview": "\n".join(lines[:10]),
                "last_modified": datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).isoformat(),
            }

        except Exception as e:
            return {"type": "error", "file": str(file_path), "error": str(e)}

    return {"type": "unknown", "file": str(file_path)}


def create_conversation_summary(conv_type: str, files: list[str], base_path: str):
    """Create a summary file for each conversation type."""
    conv_dir = (
        Path(base_path)
        / f"packages/haive-agents/src/haive/agents/conversation/{conv_type}"
    )
    summary_file = conv_dir / "CONVERSATION_OUTPUTS.md"

    # Extract content from all files
    file_contents = []
    for file_path in files:
        content = extract_key_content(file_path)
        file_contents.append(content)

    # Sort by last modified (newest first)
    file_contents.sort(key=lambda x: x.get("last_modified", ""), reverse=True)

    # Create summary
    summary = f"""# {conv_type.title()} Conversation Outputs

Generated: {datetime.now().isoformat()}

## Overview
This file provides easy access to all outputs from {conv_type} conversation agents.

## Recent Outputs ({len(file_contents)} files found)

"""

    for i, content in enumerate(file_contents, 1):
        summary += f"\n### {i}. {Path(content['file']).name}\n"
        summary += f"**Type:** {content['type']}\n"
        summary += f"**File:** `{content['file']}`\n"
        summary += f"**Last Modified:** {content.get('last_modified', 'Unknown')}\n"

        if content["type"] == "state_history":
            summary += f"**Messages:** {content.get('message_count', 0)}\n"
            if content.get("sample_messages"):
                summary += "\n**Sample Messages:**\n"
                for msg in content["sample_messages"][:2]:
                    msg_type = msg.get("type", "unknown")
                    msg_content = msg.get("content", "")[:100]
                    summary += f"- {msg_type}: {msg_content}...\n"

        elif content["type"] == "markdown":
            summary += f"**Lines:** {content.get('line_count', 0)}\n"
            summary += f"**Title:** {content.get('title', 'No title')}\n"
            if content.get("preview"):
                summary += "\n**Preview:**\n```\n"
                summary += content["preview"][:200] + "...\n```\n"

        elif content["type"] == "json_data":
            summary += (
                f"**Content:** {content.get('content_keys', 'Unknown structure')}\n"
            )

        elif content["type"] == "error":
            summary += f"**Error:** {content.get('error', 'Unknown error')}\n"

        summary += "\n---\n"

    # Add access instructions
    summary += f"""
## Quick Access

### View State History (JSON)
```bash
# View recent state history files
find {conv_dir} -name "*.json" -exec ls -la {{}} \\;

# Pretty print JSON
cat path/to/file.json | jq '.[0].messages | length'
```

### View Conversation Outputs (Markdown)
```bash
# View markdown outputs
find {conv_dir}/outputs -name "*.md" -exec cat {{}} \\;
```

### Copy Files for Analysis
```bash
# Copy all outputs to a temporary directory for analysis
mkdir -p /tmp/{conv_type}_analysis
find {conv_dir} -name "*.json" -o -name "*.md" | xargs -I {{}} cp {{}} /tmp/{conv_type}_analysis/
```

## File Structure
```
{conv_type}/
├── outputs/           # Conversation result files (.md)
├── resources/         # State history files (.json)
│   └── state_history/
└── CONVERSATION_OUTPUTS.md  # This summary file
```
"""

    # Write summary file
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)

    return summary_file


def main():
    """Main function to extract and organize conversation outputs."""
    base_path = "/home/will/Projects/haive/backend/haive"


    # Find conversation outputs
    conversation_outputs = find_conversation_outputs(base_path)
    global_state_files = find_global_state_history(base_path)


    # Add global state files to relevant conversation types
    for state_file in global_state_files:
        filename = Path(state_file).name.lower()

        # Try to match to conversation type
        for conv_type in conversation_outputs:
            if conv_type in filename or any(
                keyword in filename
                for keyword in ["productmanager", "designer", "engineer", "marketer"]
            ):
                conversation_outputs[conv_type].append(state_file)
                break

    # Create summaries for each conversation type
    summary_files = []
    for conv_type, files in conversation_outputs.items():
        if files:  # Only create summary if files exist
            summary_file = create_conversation_summary(conv_type, files, base_path)
            summary_files.append(summary_file)
        else:
            passe}")

    # Create master index
    master_index = (
        Path(base_path)
        / "packages/haive-agents/src/haive/agents/conversation/CONVERSATION_INDEX.md"
    )

    index_content = f"""# Conversation Agent Outputs Index

Generated: {datetime.now().isoformat()}

## Available Conversation Types

"""

    for conv_type, files in conversation_outputs.items():
        file_count = len(files)
        summary_path = f"{conv_type}/CONVERSATION_OUTPUTS.md"

        index_content += f"### [{conv_type.title()}](./{summary_path})\n"
        index_content += f"**Files:** {file_count}\n"
        index_content += f"**Summary:** `./{summary_path}`\n\n"

    index_content += f"""
## Global State History
**Location:** `packages/haive-agents/resources/state_history/`
**Conversation files:** {len(global_state_files)}

## Quick Commands

```bash
# View all conversation summaries
find packages/haive-agents/src/haive/agents/conversation -name "CONVERSATION_OUTPUTS.md" -exec cat {{}} \\;

# Copy all conversation outputs to analysis directory
mkdir -p /tmp/conversation_analysis
find packages/haive-agents/src/haive/agents/conversation -name "*.json" -o -name "*.md" | xargs -I {{}} cp {{}} /tmp/conversation_analysis/
```
"""

    with open(master_index, "w", encoding="utf-8") as f:
        f.write(index_content)


    # Show what was created
    for summary_file in summary_files:
        pass


if __name__ == "__main__":
    main()
