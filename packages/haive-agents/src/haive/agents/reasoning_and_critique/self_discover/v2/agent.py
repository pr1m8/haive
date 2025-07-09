# src/haive/agents/self_discovery/agents.py
"""
Self-Discovery agent implementation using SimpleAgent and SequentialAgent.
"""

from typing import List

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.multi.base import SequentialAgent
from haive.agents.reasoning_and_critique.self_discover.v2.models import (
    AdaptedModules,
    FinalAnswer,
    ReasoningStructure,
    SelectedModules,
)
from haive.agents.reasoning_and_critique.self_discover.v2.prompts import (
    adapt_prompt,
    reasoning_prompt,
    select_prompt,
    structured_prompt,
)
from haive.agents.reasoning_and_critique.self_discover.v2.state import (
    SelfDiscoveryState,
)
from haive.agents.simple.agent import SimpleAgent

# Create AugLLM configs for each step
select_engine = AugLLMConfig(
    name="select_modules",
    structured_output_model=SelectedModules,
    structured_output_version="v2",
    prompt_template=select_prompt,
    temperature=0.7,
)

adapt_engine = AugLLMConfig(
    name="adapt_modules",
    structured_output_model=AdaptedModules,
    structured_output_version="v2",
    prompt_template=adapt_prompt,
    temperature=0.7,
)

structure_engine = AugLLMConfig(
    name="create_structure",
    structured_output_model=ReasoningStructure,
    structured_output_version="v2",
    prompt_template=structured_prompt,
    temperature=0.3,
)

reason_engine = AugLLMConfig(
    name="final_reasoning",
    structured_output_model=FinalAnswer,
    structured_output_version="v2",
    prompt_template=reasoning_prompt,
    temperature=0.1,
)


# Create SimpleAgent for each step
select_agent = SimpleAgent(engine=select_engine)
adapt_agent = SimpleAgent(engine=adapt_engine)
structure_agent = SimpleAgent(engine=structure_engine)
reason_agent = SimpleAgent(engine=reason_engine)


# Create the SequentialAgent
self_discovery = SequentialAgent(
    agents=[select_agent, adapt_agent, structure_agent, reason_agent],
    # state_schema=SelfDiscoveryState
)


# Default reasoning modules
DEFAULT_REASONING_MODULES = [
    "1. How could I devise an experiment to help solve that problem?",
    "2. Make a list of ideas for solving this problem, and apply them one by one to the problem to see if any progress can be made.",
    "4. How can I simplify the problem so that it is easier to solve?",
    "5. What are the key assumptions underlying this problem?",
    "6. What are the potential risks and drawbacks of each solution?",
    "7. What are the alternative perspectives or viewpoints on this problem?",
    "8. What are the long-term implications of this problem and its solutions?",
    "9. How can I break down this problem into smaller, more manageable parts?",
    "10. Critical Thinking: This style involves analyzing the problem from different perspectives, questioning assumptions, and evaluating the evidence or information available.",
    "11. Try creative thinking, generate innovative and out-of-the-box ideas to solve the problem.",
    "13. Use systems thinking: Consider the problem as part of a larger system and understanding the interconnectedness of various elements.",
    "14. Use Risk Analysis: Evaluate potential risks, uncertainties, and tradeoffs associated with different solutions.",
    "16. What is the core issue or problem that needs to be addressed?",
    "17. What are the underlying causes or factors contributing to the problem?",
    "18. Are there any potential solutions or strategies that have been tried before?",
    "19. What are the potential obstacles or challenges that might arise in solving this problem?",
    "20. Are there any relevant data or information that can provide insights into the problem?",
    "21. Are there any stakeholders or individuals who are directly affected by the problem?",
    "22. What resources (financial, human, technological, etc.) are needed to tackle the problem effectively?",
    "23. How can progress or success in solving the problem be measured or evaluated?",
    "24. What indicators or metrics can be used?",
    "25. Is the problem a technical or practical one that requires specific expertise?",
    "26. Does the problem involve a physical constraint, such as limited resources?",
    "27. Is the problem related to human behavior, such as a social or psychological issue?",
    "28. Does the problem involve decision-making under uncertainty?",
    "29. Is the problem an analytical one that requires data analysis or optimization?",
    "30. Is the problem a design challenge that requires creative solutions?",
    "31. Does the problem require addressing systemic or structural issues?",
    "32. Is the problem time-sensitive or urgent?",
    "33. What kinds of solution typically are produced for this kind of problem?",
    "34. Given the problem specification, have a guess about other possible solutions.",
    "35. Let's imagine the current best solution is totally wrong, what other ways are there?",
    "36. What is the best way to modify this current best solution?",
    "37. Ignoring the current best solution, create an entirely new solution.",
    "39. Let's make a step by step plan and implement it with good notation and explanation.",
]
