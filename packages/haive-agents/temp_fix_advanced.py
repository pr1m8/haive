#!/usr/bin/env python3

import re

# Read the file
with open("src/haive/agents/rag/multi_agent_rag/advanced_workflows.py", "r") as f:
    content = f.read()

# Pattern to match super().__init__ blocks and add build_custom_graph method after them
pattern = r"(        super\(\).__init__\(\s*.*?\s*        \))"


def replacement(match):
    init_block = match.group(1)
    return (
        init_block
        + '\n    \n    def build_custom_graph(self):\n        """Build the custom graph for this multi-agent workflow"""\n        return None  # Use default graph structure'
    )


# Apply the replacement
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open("src/haive/agents/rag/multi_agent_rag/advanced_workflows.py", "w") as f:
    f.write(new_content)

print("Added build_custom_graph methods to advanced_workflows.py")
