"""Haive — meta-package that installs the full Haive AI agent framework.

Installing `haive` pulls in all 8 sub-packages:
    haive-core, haive-agents, haive-games, haive-tools,
    haive-mcp, haive-hap, haive-dataflow, haive-prebuilt.

Use the sub-packages directly:
    >>> from haive.agents.simple.agent import SimpleAgent
    >>> from haive.core.engine.aug_llm import AugLLMConfig

See https://github.com/pr1m8/haive for full documentation.
"""

__version__ = "1.0.0"
