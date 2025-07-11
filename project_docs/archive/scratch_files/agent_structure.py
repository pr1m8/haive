#!/usr/bin/env python3
from collections import Counter
import json
import os


# Patterns to ignore
IGNORED_DIRS = {"__pycache__"}
IGNORED_EXTENSIONS = {".pyc"}


def aggregate_counts(base_dir):
    """Scan the immediate child modules in base_dir, and aggregate counts
    of file names (from the module's top-level) and subdirectory names.
    """
    file_counter = Counter()
    subdir_counter = Counter()

    if not os.path.exists(base_dir):
        return {"error": f"Directory '{base_dir}' does not exist."}

    for module in os.listdir(base_dir):
        module_path = os.path.join(base_dir, module)
        if os.path.isdir(module_path) and module not in IGNORED_DIRS:
            for entry in os.listdir(module_path):
                full_entry = os.path.join(module_path, entry)
                if os.path.isdir(full_entry):
                    if entry in IGNORED_DIRS:
                        continue
                    subdir_counter[entry] += 1
                elif os.path.isfile(full_entry):
                    _, ext = os.path.splitext(entry)
                    if ext in IGNORED_EXTENSIONS:
                        continue
                    file_counter[entry] += 1
    return {
        "common_files": dict(file_counter),
        "common_subdirectories": dict(subdir_counter),
    }


def main():
    targets = {"agents": "src/haive/agents", "games": "src/haive/games"}
    output = {}
    for label, path in targets.items():
        output[label] = aggregate_counts(path)

    # Save the aggregate summary to resources/aggregate_structure.json
    output_dir = "resources"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "aggregate_structure.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()
