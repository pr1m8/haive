"""
Your First Haive Agent in 5 Minutes
===================================

**Level**: Beginner
**Time**: 5 minutes
**Prerequisites**: None

This quickstart example shows you how to create your first AI agent with Haive.
We'll build a simple conversational agent that can answer questions and maintain context.
"""

# %%
# Installation and Setup
# ----------------------
#
# First, make sure Haive is installed:
#
# .. code-block:: bash
#
#     pip install haive-agents
#
# Or with Poetry:
#
# .. code-block:: bash
#
#     poetry add haive-agents

# %%
# Import Required Components
# --------------------------
#
# We need just two imports to get started.

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

print("✅ Imports successful!")

# %%
# Create Your First Agent
# -----------------------
#
# Let's create a simple conversational agent. The AugLLMConfig handles
# all the LLM configuration for you.

# Configure the language model
config = AugLLMConfig(
    temperature=0.7,  # Controls creativity (0.0 = focused, 1.0 = creative)
    system_message="You are a helpful AI assistant named Haive.",
)

# Create the agent
agent = SimpleAgent(name="my_first_agent", engine=config)

print(f"🤖 Agent created: {agent.name}")
print(f"📝 Agent type: {type(agent).__name__}")

# %%
# Have a Conversation
# -------------------
#
# Now let's chat with our agent! SimpleAgent maintains conversation history
# automatically.

# First message
response1 = agent.run("Hello! What's your name?")
print("You: Hello! What's your name?")
print(f"Agent: {response1}")
print()

# %%
# Test Context Memory
# -------------------
#
# The agent remembers previous messages in the conversation.

response2 = agent.run("What did I just ask you?")
print("You: What did I just ask you?")
print(f"Agent: {response2}")
print()

# %%
# Ask Something Useful
# --------------------
#
# Let's ask our agent to help with a real task.

response3 = agent.run(
    "Can you help me write a Python function to calculate fibonacci numbers?"
)
print("You: Can you help me write a Python function to calculate fibonacci numbers?")
print(f"Agent: {response3}")

# %%
# Visualize the Conversation Flow
# --------------------------------
#
# We can visualize how the conversation flows through the agent.

import matplotlib.patches as patches
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

# Draw conversation flow
messages = [
    ("User", "Hello! What's your name?", 0),
    ("Agent", "I'm Haive", 1),
    ("User", "What did I just ask you?", 2),
    ("Agent", "You asked about my name", 3),
    ("User", "Help with Fibonacci", 4),
    ("Agent", "Here's the code...", 5),
]

colors = ["#e3f2fd", "#bbdefb"]  # Light blue alternating
y_position = 5

for sender, msg, idx in messages:
    # Create message box
    box = patches.FancyBboxPatch(
        (0.1 if sender == "User" else 0.5, y_position - idx * 0.8),
        0.4,
        0.6,
        boxstyle="round,pad=0.1",
        facecolor=colors[idx % 2],
        edgecolor="#1976d2",
        linewidth=2,
    )
    ax.add_patch(box)

    # Add text
    ax.text(
        0.3 if sender == "User" else 0.7,
        y_position - idx * 0.8 + 0.3,
        f"{sender}: {msg[:20]}...",
        ha="center",
        va="center",
        fontsize=10,
        weight="bold",
    )

# Add arrows
for i in range(len(messages) - 1):
    ax.arrow(
        0.3 if i % 2 == 0 else 0.7,
        y_position - i * 0.8 - 0.1,
        0.2 if i % 2 == 0 else -0.2,
        -0.6,
        head_width=0.05,
        head_length=0.05,
        fc="#1976d2",
        ec="#1976d2",
    )

ax.set_xlim(0, 1)
ax.set_ylim(-1, 6)
ax.axis("off")
ax.set_title(
    "Conversation Flow with Context Memory", fontsize=16, weight="bold", pad=20
)

plt.tight_layout()
plt.show()

# %%
# Check Conversation History
# --------------------------
#
# SimpleAgent keeps track of the entire conversation history.

print(f"Total messages in history: {len(agent.messages)}")
print("\nConversation summary:")
for i, msg in enumerate(agent.messages):
    role = msg.type if hasattr(msg, "type") else "unknown"
    content_preview = (
        str(msg.content)[:50] + "..."
        if len(str(msg.content)) > 50
        else str(msg.content)
    )
    print(f"{i+1}. {role}: {content_preview}")

# %%
# Performance Metrics
# -------------------
#
# Let's measure how fast our agent responds.

import time

# Measure response time
queries = [
    "What's 2+2?",
    "Tell me a joke",
    "What's the capital of France?",
]

response_times = []

for query in queries:
    start_time = time.time()
    response = agent.run(query)
    end_time = time.time()
    response_time = end_time - start_time
    response_times.append(response_time)
    print(f"Query: {query}")
    print(f"Response time: {response_time:.2f}s")
    print()

# Visualize response times
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(range(len(queries)), response_times, color="#2196f3")
ax.set_xticks(range(len(queries)))
ax.set_xticklabels([q[:20] + "..." for q in queries], rotation=15, ha="right")
ax.set_ylabel("Response Time (seconds)")
ax.set_title("Agent Response Times")
ax.grid(True, alpha=0.3, axis="y")

# Add value labels
for bar, time in zip(bars, response_times):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0,
        height,
        f"{time:.2f}s",
        ha="center",
        va="bottom",
    )

plt.tight_layout()
plt.show()

# %%
# Next Steps
# ----------
#
# Congratulations! You've created your first Haive agent. Here's what you learned:
#
# 1. ✅ How to create a SimpleAgent
# 2. ✅ How agents maintain conversation context
# 3. ✅ How to measure agent performance
#
# **What's Next?**
#
# - Add tools to your agent: :doc:`/auto_examples/quickstart/first_tool`
# - Try structured outputs: :doc:`/auto_examples/agents/structured_output`
# - Build a ReAct agent: :doc:`/auto_examples/agents/react_agent_guide`
# - Create multi-agent systems: :doc:`/auto_examples/agents/multi_agent_intro`
#
# **Pro Tips:**
#
# - Lower `temperature` (0.1-0.3) for factual tasks
# - Higher `temperature` (0.7-0.9) for creative tasks
# - Use `system_message` to define agent behavior
# - SimpleAgent is perfect for conversational interfaces
#
# Happy building! 🚀
