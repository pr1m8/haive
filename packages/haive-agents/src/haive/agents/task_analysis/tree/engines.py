# src/haive/agents/task_analysis/tree/engine.py

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.task_analysis.tree.prompts import (
    CRITICAL_PATH_ANALYSIS_PROMPT,
    TREE_PATTERN_RECOGNITION_PROMPT,
    TREE_STRUCTURE_ANALYSIS_PROMPT,
)

# Tree structure analyzer
TreeStructureAnalyzerEngine = AugLLMConfig(
    name="tree_structure_analyzer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=TREE_STRUCTURE_ANALYSIS_PROMPT,
    structured_output_model=None,  # Returns analysis text
    system_message="You specialize in hierarchical task tree analysis and optimization.",
)

# Critical path analyzer
CriticalPathAnalyzerEngine = AugLLMConfig(
    name="critical_path_analyzer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=CRITICAL_PATH_ANALYSIS_PROMPT,
    structured_output_model=None,  # Returns critical path analysis
    system_message="You analyze critical paths through task trees.",
)

# Pattern recognition engine
TreePatternRecognizerEngine = AugLLMConfig(
    name="tree_pattern_recognizer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=TREE_PATTERN_RECOGNITION_PROMPT,
    structured_output_model=None,  # Returns pattern analysis
    system_message="You recognize patterns in task tree structures.",
)
