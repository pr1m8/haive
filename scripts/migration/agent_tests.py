# agent_analyzer.py
import json
import os
import sys
from collections import defaultdict


def analyze_agent_structure(agent_dir):
    """Analyze the structure of an agent directory."""
    result = {"files": [], "imports": defaultdict(list), "classes": [], "functions": []}

    for root, _, files in os.walk(agent_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, agent_dir)

                result["files"].append(rel_path)

                # Simple parsing to extract imports, classes, and functions
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    # Extract imports
                    for line in content.split("\n"):
                        line = line.strip()
                        if line.startswith(("import ", "from ")):
                            line.split()[1]
                            result["imports"][rel_path].append(line)

                    # Very simple class detection
                    for line in content.split("\n"):
                        line = line.strip()
                        if line.startswith("class "):
                            class_name = line.split("class ")[1].split("(")[0].strip()
                            result["classes"].append(f"{rel_path}: {class_name}")

                    # Simple function detection
                    for line in content.split("\n"):
                        line = line.strip()
                        if line.startswith("def ") and not line.startswith("    def"):
                            func_name = line.split("def ")[1].split("(")[0].strip()
                            result["functions"].append(f"{rel_path}: {func_name}")

    return result


def analyze_all_agents(base_dir):
    """Analyze all agents in the given directory."""
    results = {}

    # Find all potential agent directories
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            # Check if it has agent.py, config.py or similar structure
            agent_markers = ["agent.py", "config.py", "state.py"]
            if any(
                os.path.exists(os.path.join(item_path, marker))
                for marker in agent_markers
            ):
                results[item] = analyze_agent_structure(item_path)

    return results


def find_common_patterns(results):
    """Find common patterns across different agents."""
    common_files = set()
    first = True

    for _agent, data in results.items():
        if first:
            common_files = set(data["files"])
            first = False
        else:
            common_files = common_files.intersection(set(data["files"]))

    return {
        "common_files": sorted(common_files),
        "file_frequencies": get_file_frequencies(results),
    }


def get_file_frequencies(results):
    """Count how often each file appears across agents."""
    frequencies = defaultdict(int)

    for _agent, data in results.items():
        for file in data["files"]:
            frequencies[file] += 1

    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    agents_dir = sys.argv[1]
    if not os.path.exists(agents_dir):
        sys.exit(1)

    results = analyze_all_agents(agents_dir)

    # Output summary
    for agent, data in results.items():

    # Output common patterns
    patterns = find_common_patterns(results)
    for file in patterns["common_files"]:
        pass

    for file, count in list(patterns["file_frequencies"].items())[:10]:
        pass

    # Output detailed results to JSON
    with open("agent_analysis.json", "w") as f:
        json.dump(results, f, indent=2)

