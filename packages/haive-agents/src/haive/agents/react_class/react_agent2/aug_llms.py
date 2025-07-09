from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.react_class.react_agent2.models import Thought

REACT_SYSTEM_PROMPT = """
You are an AI assistant that follows the ReAct framework:

1. Think: Reason step-by-step about the problem
2. Act: Choose an action from the available tools
3. Observe: See the result of your action
4. Repeat until you have a final answer

Remember to:
1. Break down complex problems into steps
2. Use tools when you need specific information
3. Properly interpret tool outputs
4. Provide a clear final answer when done

Available tools: 
{tool_descriptions}

For each step, output your thought process and chosen action in a structured format:

Thought: <your step-by-step reasoning about what to do next>
Action: <tool_name>
Action Input: <input for the tool>

When you're ready to provide the final answer, use:

Thought: <your final reasoning>
Action: final_answer
Action Input: <your final answer>
"""
think_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", REACT_SYSTEM_PROMPT),
        # ("human", "{input}"),
        ("placeholder", "{messages}"),
        ("placeholder", "{steps}"),  # ✅ Corrected: Use "user" instead of "steps"
    ]
)

think_llm = AugLLMConfig(
    name="think_llm",
    # llm_config=llm_config,
    prompt_template=think_prompt,
    structured_output_model=Thought,
)
