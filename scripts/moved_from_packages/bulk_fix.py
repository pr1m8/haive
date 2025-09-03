#!/usr/bin/env python3
"""Bulk fix unterminated string literals."""

import os

# All the files with errors from black output
error_fixes = [
    (
        "src/haive/agents/memory_v2/long_term_memory_agent.py",
        579,
        'print("\\n📊 Memory Summary:"y: ")',
        'print("\\n📊 Memory Summary:")',
    ),
    (
        "src/haive/agents/memory_v2/react_memory_coordinator.py",
        484,
        'print("\\n📊 Comprehensive Summary:"y: ")',
        'print("\\n📊 Comprehensive Summary:")',
    ),
    (
        "src/haive/agents/memory_v2/test_graph_memory_simple.py",
        156,
        'print("✅ Configuration: PASSED"D")',
        'print("✅ Configuration: PASSED")',
    ),
    (
        "src/haive/agents/memory_v2/test_multi_memory_agent.py",
        23,
        'print("✅ Default config created:": ")',
        'print("✅ Default config created:")',
    ),
    (
        "src/haive/agents/memory_v2/test_simple_memory_agent_fixed.py",
        51,
        'print("\\n✅ Memory status retrieved!"!")',
        'print("\\n✅ Memory status retrieved!")',
    ),
    (
        "src/haive/agents/memory_v2/test_simple_memory_with_deepseek.py",
        36,
        'print("   ✅ Created AugLLMConfig"g")',
        'print("   ✅ Created AugLLMConfig")',
    ),
    (
        "src/haive/agents/memory_v2/test_with_deepseek.py",
        30,
        'print("✅ Created AugLLMConfig with DeepSeek"k")',
        'print("✅ Created AugLLMConfig with DeepSeek")',
    ),
    (
        "src/haive/agents/memory_v2/test_react_memory_coordinator.py",
        322,
        'print("\\n📊 Final Summary:"y: ")',
        'print("\\n📊 Final Summary:")',
    ),
    (
        "src/haive/agents/patterns/sequential_with_structured_output.py",
        177,
        'print("   ✅ First agent completed"d")',
        'print("   ✅ First agent completed")',
    ),
    (
        "src/haive/agents/rag/simple/enhanced_v3/agent.py",
        527,
        'logger.info("📊 Performance Summary:"y:")',
        'logger.info("📊 Performance Summary:")',
    ),
]

for filepath, _line_num, old_str, new_str in error_fixes:
    if os.path.exists(filepath):
        with open(filepath) as f:
            content = f.read()

        if old_str in content:
            content = content.replace(old_str, new_str)
            with open(filepath, "w") as f:
                f.write(content)
        else:
            pass
