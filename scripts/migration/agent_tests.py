# agent_analyzer.py
import os
import sys
from pathlib import Path
import json
from collections import defaultdict

def analyze_agent_structure(agent_dir):
    """Analyze the structure of an agent directory."""
    result = {
        "files": [],
        "imports": defaultdict(list),
        "classes": [],
        "functions": []
    }
    
    for root, _, files in os.walk(agent_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, agent_dir)
                
                result["files"].append(rel_path)
                
                # Simple parsing to extract imports, classes, and functions
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Extract imports
                    for line in content.split('\n'):
                        line = line.strip()
                        if line.startswith('import ') or line.startswith('from '):
                            module = line.split()[1]
                            result["imports"][rel_path].append(line)
                    
                    # Very simple class detection
                    for line in content.split('\n'):
                        line = line.strip()
                        if line.startswith('class '):
                            class_name = line.split('class ')[1].split('(')[0].strip()
                            result["classes"].append(f"{rel_path}: {class_name}")
                    
                    # Simple function detection
                    for line in content.split('\n'):
                        line = line.strip()
                        if line.startswith('def ') and not line.startswith('    def'):
                            func_name = line.split('def ')[1].split('(')[0].strip()
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
            if any(os.path.exists(os.path.join(item_path, marker)) for marker in agent_markers):
                results[item] = analyze_agent_structure(item_path)
    
    return results

def find_common_patterns(results):
    """Find common patterns across different agents."""
    common_files = set()
    first = True
    
    for agent, data in results.items():
        if first:
            common_files = set(data["files"])
            first = False
        else:
            common_files = common_files.intersection(set(data["files"]))
    
    return {
        "common_files": sorted(list(common_files)),
        "file_frequencies": get_file_frequencies(results)
    }

def get_file_frequencies(results):
    """Count how often each file appears across agents."""
    frequencies = defaultdict(int)
    
    for agent, data in results.items():
        for file in data["files"]:
            frequencies[file] += 1
    
    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent_analyzer.py <agents_directory>")
        sys.exit(1)
    
    agents_dir = sys.argv[1]
    if not os.path.exists(agents_dir):
        print(f"Directory not found: {agents_dir}")
        sys.exit(1)
    
    results = analyze_all_agents(agents_dir)
    
    # Output summary
    print(f"Found {len(results)} agent directories")
    for agent, data in results.items():
        print(f"\n{agent}:")
        print(f"  Files: {len(data['files'])}")
        print(f"  Classes: {len(data['classes'])}")
        print(f"  Functions: {len(data['functions'])}")
    
    # Output common patterns
    patterns = find_common_patterns(results)
    print("\nCommon files found in all agents:")
    for file in patterns["common_files"]:
        print(f"  {file}")
    
    print("\nMost frequent files:")
    for file, count in list(patterns["file_frequencies"].items())[:10]:
        print(f"  {file}: found in {count} agents")
    
    # Output detailed results to JSON
    with open('agent_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed analysis written to agent_analysis.json")