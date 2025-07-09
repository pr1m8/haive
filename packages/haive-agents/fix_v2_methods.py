#!/usr/bin/env python3
"""Add missing build_custom_graph methods to V2 classes"""

import re

# Read the file
with open("src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py", "r") as f:
    content = f.read()

# Find all classes
class_pattern = r"class (\w+Agent(?:V2)?)\(MultiAgent"
classes = re.findall(class_pattern, content)

print(f"Found classes: {classes}")

# Check which classes are missing build_custom_graph
missing = []
for class_name in classes:
    # Check if this class has build_custom_graph
    pattern = f"class {class_name}.*?(?=class|\\Z)"
    class_section = re.search(pattern, content, re.DOTALL)
    if class_section:
        if "def build_custom_graph" not in class_section.group():
            missing.append(class_name)

print(f"Missing build_custom_graph: {missing}")

# Add the method to each missing class
for class_name in missing:
    # Find the end of __init__ method for this class
    pattern = f"(class {class_name}.*?return await super\\(\\)\\.ainvoke\\(inputs\\))"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Add build_custom_graph after ainvoke
        replacement = (
            match.group(1)
            + '''
    
    def build_custom_graph(self):
        """Build the custom graph for this workflow"""
        return None  # Use default graph structure'''
        )

        content = content.replace(match.group(1), replacement)
        print(f"Added build_custom_graph to {class_name}")

# Write back
with open("src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py", "w") as f:
    f.write(content)

print("Done!")
