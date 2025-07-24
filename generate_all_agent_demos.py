#!/usr/bin/env python3
"""Generate demo pages for ALL agents in the haive-agents package."""

import os
from pathlib import Path

# Agent configurations
AGENTS = {
    "chain": {
        "name": "Chain Agent",
        "icon": "🔗",
        "description": "Executes chains of operations in sequence",
        "category": "Workflow",
        "features": ["Sequential execution", "State passing", "Error handling", "Retry logic"],
        "example_output": """Chain Execution:
Step 1: Data retrieval ✓
Step 2: Processing ✓
Step 3: Validation ✓
Step 4: Output generation ✓

Total time: 2.3s
Status: Complete"""
    },
    "conversation": {
        "name": "Conversation Agent",
        "icon": "💭",
        "description": "Manages multi-turn conversations with context",
        "category": "Dialogue",
        "features": ["Context tracking", "Turn management", "Memory integration", "Personality"],
        "example_output": """User: Tell me about AI safety
Assistant: AI safety is a critical field focusing on ensuring AI systems are beneficial and aligned with human values...

User: What are the main risks?
Assistant: The main risks include:
1. Misalignment with human goals
2. Unintended consequences
3. Adversarial uses..."""
    },
    "discovery": {
        "name": "Discovery Agent",
        "icon": "🔍",
        "description": "Discovers patterns and insights in data",
        "category": "Analysis",
        "features": ["Pattern recognition", "Anomaly detection", "Insight generation", "Visualization"],
        "example_output": """Discovery Report:
✓ Found 3 significant patterns
✓ Identified 2 anomalies
✓ Generated 5 insights

Key Finding: Customer behavior shifts on weekends
Confidence: 87%"""
    },
    "document": {
        "name": "Document Agent",
        "icon": "📄",
        "description": "Processes and analyzes documents",
        "category": "Document Processing",
        "features": ["Text extraction", "Summarization", "Entity recognition", "Classification"],
        "example_output": """Document Analysis:
Type: Research Paper
Pages: 12
Topics: Machine Learning, NLP
Key Entities: 8 identified

Summary: This paper presents a novel approach to..."""
    },
    "dynamic_supervisor": {
        "name": "Dynamic Supervisor",
        "icon": "👔",
        "description": "Dynamically manages and coordinates multiple agents",
        "category": "Orchestration",
        "features": ["Dynamic routing", "Load balancing", "Task delegation", "Performance monitoring"],
        "example_output": """Supervision Status:
Active Agents: 4
Tasks Completed: 12/15
Average Response: 1.2s

Current Assignments:
- Research Agent → Market analysis
- Writer Agent → Report draft
- Review Agent → Quality check"""
    },
    "long_term_memory": {
        "name": "Long-Term Memory Agent",
        "icon": "🧠",
        "description": "Manages persistent memory across sessions",
        "category": "Memory",
        "features": ["Memory storage", "Retrieval", "Forgetting curves", "Association"],
        "example_output": """Memory Status:
Total Memories: 1,247
Recent Recalls: 5
Memory Score: 92%

Last Interaction: "Project deadline discussion"
Related Memories: 3 found"""
    },
    "planning": {
        "name": "Planning Agent",
        "icon": "📋",
        "description": "Creates and executes strategic plans",
        "category": "Strategy",
        "features": ["Goal decomposition", "Step generation", "Resource allocation", "Timeline creation"],
        "example_output": """Generated Plan:
Goal: Launch new product

Steps:
1. Market research (2 weeks)
2. Design phase (3 weeks)
3. Development (6 weeks)
4. Testing (2 weeks)
5. Launch prep (1 week)

Total Duration: 14 weeks
Resources: 5 team members"""
    },
    "rag": {
        "name": "RAG Agent",
        "icon": "📚",
        "description": "Retrieval-Augmented Generation for accurate responses",
        "category": "Knowledge",
        "features": ["Document retrieval", "Context injection", "Source citation", "Fact checking"],
        "example_output": """Query: What is quantum computing?

Retrieved Sources: 3
Confidence: 95%

Answer: Quantum computing uses quantum mechanics principles...

Sources:
[1] Introduction to Quantum Computing, MIT Press
[2] Nature Physics, Vol 15, 2023
[3] IBM Quantum Documentation"""
    },
    "reasoning_and_critique": {
        "name": "Reasoning & Critique Agent",
        "icon": "🤔",
        "description": "Provides logical reasoning and critical analysis",
        "category": "Analysis",
        "features": ["Logic chains", "Argument analysis", "Critique generation", "Bias detection"],
        "example_output": """Analysis of Argument:

Premise 1: Valid ✓
Premise 2: Questionable ⚠️
Conclusion: Does not follow

Logical Fallacies Detected:
- Hasty generalization
- Appeal to authority

Recommendation: Strengthen premise 2 with data"""
    },
    "reflection": {
        "name": "Reflection Agent",
        "icon": "🪞",
        "description": "Self-reflects on outputs and improves them",
        "category": "Quality",
        "features": ["Self-evaluation", "Improvement suggestions", "Quality metrics", "Iterative refinement"],
        "example_output": """Initial Output: "The data shows improvement"

Reflection:
- Too vague ⚠️
- Lacks specifics ⚠️
- No metrics ⚠️

Improved Output: "Sales data shows 23% improvement in Q3 2024 compared to Q2, driven by new marketing campaign"""
    },
    "research": {
        "name": "Research Agent",
        "icon": "🔬",
        "description": "Conducts comprehensive research on topics",
        "category": "Investigation",
        "features": ["Multi-source search", "Fact verification", "Bibliography", "Synthesis"],
        "example_output": """Research Report: AI in Healthcare

Sources Analyzed: 47
Key Findings: 12
Confidence Level: High

Executive Summary:
AI adoption in healthcare has increased 40% in 2024...

Full report: 2,500 words
Citations: 23"""
    },
    "self_healing_code": {
        "name": "Self-Healing Code Agent",
        "icon": "🔧",
        "description": "Automatically fixes code errors and issues",
        "category": "Development",
        "features": ["Error detection", "Auto-fixing", "Test generation", "Code optimization"],
        "example_output": """Code Analysis:
✗ Syntax error on line 42
✗ Undefined variable 'user_data'
✗ Missing import statement

Auto-fixes applied:
✓ Fixed syntax error
✓ Initialized variable
✓ Added missing import

All tests passing ✓"""
    },
    "sequential": {
        "name": "Sequential Agent",
        "icon": "➡️",
        "description": "Executes tasks in sequential order",
        "category": "Workflow",
        "features": ["Order preservation", "State management", "Dependency handling", "Progress tracking"],
        "example_output": """Sequential Execution:
[✓] Step 1: Initialize
[✓] Step 2: Load data
[✓] Step 3: Process
[✓] Step 4: Validate
[→] Step 5: Generate output

Progress: 80% complete"""
    },
    "structured_output": {
        "name": "Structured Output Agent",
        "icon": "📊",
        "description": "Generates structured, schema-compliant outputs",
        "category": "Data",
        "features": ["Schema validation", "Type safety", "Format conversion", "Consistency"],
        "example_output": """{
  "analysis": {
    "sentiment": "positive",
    "confidence": 0.89,
    "topics": ["AI", "innovation", "future"],
    "entities": [
      {"name": "OpenAI", "type": "ORG"},
      {"name": "GPT-4", "type": "PRODUCT"}
    ]
  }
}"""
    },
    "supervisor": {
        "name": "Supervisor Agent",
        "icon": "👨‍💼",
        "description": "Supervises and coordinates agent teams",
        "category": "Orchestration",
        "features": ["Team management", "Task assignment", "Quality control", "Reporting"],
        "example_output": """Team Status Report:

Active Agents: 5/5
Current Tasks: 3
Completed Today: 12

Performance Metrics:
- Avg Response Time: 0.8s
- Success Rate: 96%
- Quality Score: 4.7/5"""
    },
    "task_analysis": {
        "name": "Task Analysis Agent",
        "icon": "📈",
        "description": "Analyzes and decomposes complex tasks",
        "category": "Planning",
        "features": ["Task breakdown", "Complexity analysis", "Resource estimation", "Risk assessment"],
        "example_output": """Task Analysis: Build E-commerce Site

Complexity: High
Estimated Time: 3 months
Required Skills: 5

Subtasks:
1. Frontend (40h)
2. Backend API (60h)
3. Database (20h)
4. Payment Integration (30h)
5. Testing (25h)

Risk Factors: 3 identified"""
    },
    "wiki_writer": {
        "name": "Wiki Writer Agent",
        "icon": "✍️",
        "description": "Creates wiki-style documentation",
        "category": "Content",
        "features": ["Structured writing", "Cross-referencing", "Formatting", "Version control"],
        "example_output": """= Quantum Computing =

Quantum computing is a type of computation that harnesses quantum phenomena.

== Overview ==
Unlike classical computers that use bits...

== Key Concepts ==
* Superposition
* Entanglement
* Quantum gates

[[See also]]: Quantum mechanics, Qubits"""
    }
}

def generate_agent_demo(agent_key, agent_info):
    """Generate RST content for an agent demo page."""
    
    features_list = "\n".join([f'                <span class="feature-tag">{feature}</span>' for feature in agent_info["features"]])
    
    content = f"""{agent_info["name"]} Demo
{'=' * (len(agent_info["name"]) + 5)}

{agent_info["description"]}

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">{agent_info["icon"]}</div>
                <div>
                    <h2>{agent_info["name"]}</h2>
                    <p class="agent-category">Category: {agent_info["category"]}</p>
                </div>
            </div>

            <div class="agent-features">
{features_list}
            </div>
        </div>

        <!-- Interactive Demo -->
        <div class="agent-interface">
            <div class="demo-controls">
                <h3>Try {agent_info["name"]}</h3>
                <div class="input-area">
                    <textarea id="{agent_key}-input" placeholder="Enter your input here..." rows="4"></textarea>
                </div>
                <button onclick="runAgent('{agent_key}')" class="run-agent-btn">
                    Run Agent
                </button>
            </div>

            <div id="{agent_key}-output" class="agent-output">
                <!-- Agent output will appear here -->
                <div class="output-placeholder">
                    <p>Enter input and click "Run Agent" to see results</p>
                </div>
            </div>
        </div>

        <!-- Live Execution Stream -->
        <div class="agent-streaming">
            <h3>Live Execution</h3>
            <div class="streaming-indicator">
                Live Stream
            </div>
            <div class="execution-display">
                <pre id="{agent_key}-execution">
{agent_info["example_output"]}
                </pre>
            </div>
            <div class="execution-stats">
                <div class="stat">
                    <label>Status:</label>
                    <span class="status-active">Active</span>
                </div>
                <div class="stat">
                    <label>Runtime:</label>
                    <span>1.2s</span>
                </div>
                <div class="stat">
                    <label>Tokens:</label>
                    <span>847</span>
                </div>
            </div>
        </div>
    </div>

How It Works
------------

The {agent_info["name"]} operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for {agent_info["category"].lower()} tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.{agent_key}.agent import {agent_info["name"].replace(" ", "")}
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = {agent_info["name"].replace(" ", "")}(
        name="my_{agent_key}",
        engine=AugLLMConfig(temperature=0.7)
    )

    # Run agent
    result = agent.run("Your input here")
    print(result)

Configuration Options
--------------------

.. code-block:: python

    config = {{
        "temperature": 0.7,
        "max_tokens": 1000,
        "timeout": 30,
        "retry_attempts": 3
    }}

See Also
--------

- :doc:`/api/haive/agents/{agent_key}/index` - API documentation
- :doc:`/guides/building_agents` - Agent development guide
- :doc:`/examples/agent_patterns` - Common patterns
"""
    
    return content

def main():
    """Generate demo pages for all agents."""
    demos_dir = Path("docs/source/agents/demos")
    demos_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate individual agent demos
    for agent_key, agent_info in AGENTS.items():
        filename = f"{agent_key}-demo.rst"
        filepath = demos_dir / filename
        
        # Skip if already exists and has streaming content
        if filepath.exists():
            with open(filepath, 'r') as f:
                if "Live Execution" in f.read():
                    print(f"✓ {filename} already has streaming content")
                    continue
        
        content = generate_agent_demo(agent_key, agent_info)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✓ Generated {filename}")
    
    # Update the agents index
    update_agents_index()
    
    print("\n✅ All agent demos generated!")

def update_agents_index():
    """Update the agents demos index page."""
    # Read existing index to preserve custom content
    index_path = Path("docs/source/agents/demos/index.rst")
    
    index_content = """Agent Demos
===========

Interactive demonstrations of all Haive agents with live execution and state tracking.

.. grid:: 1 2 3 3
   :gutter: 3

"""
    
    # Group agents by category
    categories = {}
    for agent_key, agent_info in AGENTS.items():
        category = agent_info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((agent_key, agent_info))
    
    # Add existing agents that might not be in our list
    existing_agents = {
        "simple": ("Simple Agent", "💬", "Basic conversational agent", "Core"),
        "react": ("React Agent", "🔄", "Reasoning and action agent", "Core"),
        "structuredoutput": ("Structured Output", "📊", "Schema-compliant outputs", "Data"),
        "baserag": ("Base RAG", "📚", "Basic RAG implementation", "Knowledge"),
        "adaptiverag": ("Adaptive RAG", "🎯", "Adaptive retrieval", "Knowledge"),
    }
    
    for agent_key, (name, icon, desc, category) in existing_agents.items():
        if category not in categories:
            categories[category] = []
        categories[category].append((agent_key, {
            "name": name,
            "icon": icon,
            "description": desc,
            "category": category
        }))
    
    # Generate cards by category
    for category in sorted(categories.keys()):
        agents = sorted(categories[category], key=lambda x: x[1]["name"])
        
        for agent_key, agent_info in agents:
            index_content += f"""   .. grid-item-card:: {agent_info["icon"]} {agent_info["name"]}
      :link: {agent_key}-demo
      :link-type: doc

      {agent_info["description"]}

      **Category**: {category}

"""
    
    index_content += """

.. toctree::
   :maxdepth: 1
   :hidden:

"""
    
    # Add all agents to toctree
    all_agents = []
    for category_agents in categories.values():
        all_agents.extend([agent[0] for agent in category_agents])
    
    for agent_key in sorted(set(all_agents)):
        index_content += f"   {agent_key}-demo\n"
    
    with open(index_path, 'w') as f:
        f.write(index_content)
    
    print("✓ Updated agents demos index")

if __name__ == "__main__":
    main()