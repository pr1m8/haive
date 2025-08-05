"""
Basic Agent Visualization Demo
==============================

This example demonstrates basic agent visualization capabilities without
complex imports. We'll create simple visual demonstrations of agent concepts.
"""

# %%
# Create Agent Visualization Concept
# ----------------------------------
# Let's demonstrate the concept of agent workflows with a simple visualization.

import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt
import numpy as np

# Create a figure for agent workflow visualization
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Define workflow steps
steps = [
    "User Input",
    "Agent Processing",
    "LLM Execution",
    "Tool Integration",
    "Response Generation",
]

# Define positions for the workflow
positions = [(1, 4), (3, 4), (5, 4), (7, 4), (9, 4)]
colors = ["#e8f4f8", "#d4edda", "#fff3cd", "#f8d7da", "#e2e3e5"]

# Draw workflow boxes
for i, (step, pos, color) in enumerate(zip(steps, positions, colors, strict=False)):
    # Create fancy box
    box = FancyBboxPatch(
        (pos[0] - 0.8, pos[1] - 0.4),
        1.6,
        0.8,
        boxstyle="round,pad=0.1",
        facecolor=color,
        edgecolor="#6c757d",
        linewidth=2,
    )
    ax.add_patch(box)

    # Add text
    ax.text(
        pos[0],
        pos[1],
        step,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
    )

    # Add arrows between steps
    if i < len(positions) - 1:
        ax.arrow(
            pos[0] + 0.8,
            pos[1],
            1.4,
            0,
            head_width=0.1,
            head_length=0.2,
            fc="#007bff",
            ec="#007bff",
        )

# Set axis properties
ax.set_xlim(0, 10)
ax.set_ylim(3, 5)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Haive Agent Workflow Pattern", fontsize=16, fontweight="bold", pad=20)

plt.tight_layout()
plt.show()

# %%
# Agent Architecture Comparison
# -----------------------------
# Compare different agent architectures available in Haive.

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# SimpleAgent Architecture
simple_components = ["User Input", "SimpleAgent", "LLM Engine", "Response"]
simple_y = [3, 2, 1, 0]
simple_colors = ["#17a2b8", "#28a745", "#ffc107", "#dc3545"]

for i, (comp, y, color) in enumerate(
    zip(simple_components, simple_y, simple_colors, strict=False),
):
    rect = mpatches.Rectangle(
        (0, y),
        3,
        0.8,
        facecolor=color,
        alpha=0.7,
        edgecolor="black",
    )
    ax1.add_patch(rect)
    ax1.text(1.5, y + 0.4, comp, ha="center", va="center", fontweight="bold")

    if i < len(simple_y) - 1:
        ax1.arrow(
            1.5,
            y - 0.1,
            0,
            -0.6,
            head_width=0.2,
            head_length=0.1,
            fc="black",
            ec="black",
        )

ax1.set_xlim(-0.5, 3.5)
ax1.set_ylim(-0.5, 4)
ax1.set_title("SimpleAgent Architecture", fontsize=14, fontweight="bold")
ax1.axis("off")

# ReactAgent Architecture
react_components = [
    "User Input",
    "ReactAgent",
    "Reasoning Loop",
    "Tool Selection",
    "Tool Execution",
    "Response",
]
react_positions = [(1, 5), (1, 4), (0, 3), (2, 3), (1, 2), (1, 1)]
react_colors = ["#17a2b8", "#28a745", "#fd7e14", "#6f42c1", "#e83e8c", "#dc3545"]

for i, ((x, y), comp, color) in enumerate(
    zip(react_positions, react_components, react_colors, strict=False),
):
    circle = plt.Circle((x, y), 0.4, facecolor=color, alpha=0.7, edgecolor="black")
    ax2.add_patch(circle)
    ax2.text(
        x,
        y,
        comp,
        ha="center",
        va="center",
        fontsize=8,
        fontweight="bold",
        wrap=True,
    )

# Add connections
connections = [
    ((1, 4.6), (1, 4.4)),  # Input to ReactAgent
    ((1, 3.6), (0.6, 3.4)),  # ReactAgent to Reasoning
    ((1, 3.6), (1.4, 3.4)),  # ReactAgent to Tool Selection
    ((1.4, 2.6), (1, 2.4)),  # Tool Selection to Execution
    ((1, 1.6), (1, 1.4)),  # Execution to Response
]

for (x1, y1), (x2, y2) in connections:
    ax2.arrow(
        x1,
        y1,
        x2 - x1,
        y2 - y1,
        head_width=0.05,
        head_length=0.05,
        fc="gray",
        ec="gray",
    )

ax2.set_xlim(-0.8, 2.8)
ax2.set_ylim(0.5, 5.5)
ax2.set_title("ReactAgent Architecture", fontsize=14, fontweight="bold")
ax2.axis("off")

plt.tight_layout()
plt.show()

# %%
# Performance Comparison
# ----------------------
# Show performance characteristics of different agent types.

agent_types = ["SimpleAgent", "ReactAgent", "MultiAgent", "RAGAgent"]
setup_time = [0.5, 1.2, 2.1, 1.8]
execution_time = [0.3, 1.5, 3.2, 2.1]
memory_usage = [10, 25, 45, 35]

x = np.arange(len(agent_types))
width = 0.25

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Execution times
bars1 = ax1.bar(
    x - width / 2,
    setup_time,
    width,
    label="Setup Time (s)",
    color="#3498db",
    alpha=0.8,
)
bars2 = ax1.bar(
    x + width / 2,
    execution_time,
    width,
    label="Execution Time (s)",
    color="#e74c3c",
    alpha=0.8,
)

ax1.set_xlabel("Agent Types")
ax1.set_ylabel("Time (seconds)")
ax1.set_title("Agent Performance Comparison - Time")
ax1.set_xticks(x)
ax1.set_xticklabels(agent_types)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2.0,
        height + 0.02,
        f"{height}s",
        ha="center",
        va="bottom",
        fontsize=9,
    )

for bar in bars2:
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2.0,
        height + 0.02,
        f"{height}s",
        ha="center",
        va="bottom",
        fontsize=9,
    )

# Memory usage
bars3 = ax2.bar(
    agent_types,
    memory_usage,
    color=["#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"],
    alpha=0.8,
)
ax2.set_xlabel("Agent Types")
ax2.set_ylabel("Memory Usage (MB)")
ax2.set_title("Agent Performance Comparison - Memory")
ax2.grid(True, alpha=0.3)

# Add value labels
for bar in bars3:
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2.0,
        height + 0.5,
        f"{height}MB",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
    )

plt.tight_layout()
plt.show()

print("✅ Agent visualization examples completed!")
print("🎯 Key takeaways:")
print("   - SimpleAgent: Fast, lightweight, direct LLM interaction")
print("   - ReactAgent: Reasoning loops, tool integration, more complex")
print("   - MultiAgent: Coordination overhead, powerful for complex tasks")
print("   - RAGAgent: Knowledge retrieval, good balance of capability and performance")
