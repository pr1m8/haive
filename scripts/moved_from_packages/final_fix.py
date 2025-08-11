#!/usr/bin/env python3
import os

# Pattern to fix various string literal issues
files_to_check = [
    "src/haive/agents/memory_v2/test_simple_memory_with_deepseek.py",
    "src/haive/agents/memory_v2/test_graph_memory_simple.py",
    "src/haive/agents/memory_v2/test_simple_memory_agent_fixed.py",
    "src/haive/agents/memory_v2/test_multi_memory_agent.py",
    "src/haive/agents/memory_v2/test_with_deepseek.py",
]

# Common patterns to fix
patterns = [
    ('"4j")', '")'),  # Neo4j reference
    ('""g")', '")'),  # Extra g
    ('""!")', '")'),  # Extra !
    ('":"")', '")'),  # Extra colon and quotes
    ('""d")', '")'),  # Extra d
    ('""k")', '")'),  # Extra k
    ('""s:")', '")'),  # Extra s and colon
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath) as f:
            content = f.read()

        original_content = content
        for old, new in patterns:
            content = content.replace(old, new)

        if content != original_content:
            with open(filepath, "w") as f:
                f.write(content)
        else:
            # Check for syntax errors manually
            lines = content.split("\n")
            for _i, line in enumerate(lines, 1):
                if '"' in line and line.count('"') % 2 != 0:
                    pass
