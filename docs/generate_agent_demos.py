#!/usr/bin/env python3
"""
Generate interactive demo pages for all Haive agents.

This script scans the agent modules and creates visualization-rich demo pages
for each agent type, including graph visualization, state tracking, and examples.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import importlib
import inspect
from jinja2 import Template

# Agent categories and their characteristics
AGENT_CATEGORIES = {
    "simple": {
        "icon": "🤖",
        "description": "Basic conversational agents for straightforward tasks",
        "color": "#4589ff"
    },
    "react": {
        "icon": "🧠",
        "description": "Reasoning and Acting agents that think before they act",
        "color": "#8a3ffc"
    },
    "rag": {
        "icon": "📚",
        "description": "Retrieval-Augmented Generation agents with knowledge",
        "color": "#24a148"
    },
    "planning": {
        "icon": "📋",
        "description": "Multi-step planning and execution agents",
        "color": "#ff832b"
    },
    "conversation": {
        "icon": "💬",
        "description": "Multi-agent conversation and collaboration",
        "color": "#f1c21b"
    },
    "research": {
        "icon": "🔬",
        "description": "Deep research and analysis agents",
        "color": "#0f62fe"
    },
    "document_modifiers": {
        "icon": "📄",
        "description": "Document processing and transformation agents",
        "color": "#da1e28"
    },
    "reasoning_and_critique": {
        "icon": "🎯",
        "description": "Advanced reasoning and self-critique agents",
        "color": "#6929c4"
    }
}

def generate_mock_graph_data(agent_type: str, agent_name: str) -> Dict[str, Any]:
    """Generate realistic graph data for an agent type."""
    
    base_nodes = [
        {"id": "start", "type": "start", "label": "START"},
        {"id": "end", "type": "end", "label": "END"}
    ]
    
    if agent_type == "simple":
        nodes = base_nodes + [
            {"id": "agent", "type": "agent", "label": f"{agent_name}", "description": "Main processing node"}
        ]
        edges = [
            {"source": "start", "target": "agent"},
            {"source": "agent", "target": "end"}
        ]
    
    elif agent_type == "react":
        nodes = base_nodes + [
            {"id": "reason", "type": "agent", "label": "Reasoning", "description": "Analyze the problem"},
            {"id": "act", "type": "tool", "label": "Action", "description": "Execute tools"},
            {"id": "observe", "type": "validation", "label": "Observe", "description": "Process results"}
        ]
        edges = [
            {"source": "start", "target": "reason"},
            {"source": "reason", "target": "act", "type": "conditional"},
            {"source": "act", "target": "observe"},
            {"source": "observe", "target": "reason"},
            {"source": "reason", "target": "end"}
        ]
    
    elif agent_type == "rag":
        nodes = base_nodes + [
            {"id": "query", "type": "agent", "label": "Query Analysis", "description": "Understand the question"},
            {"id": "retrieve", "type": "tool", "label": "Retrieve", "description": "Search knowledge base"},
            {"id": "generate", "type": "agent", "label": "Generate", "description": "Create response"}
        ]
        edges = [
            {"source": "start", "target": "query"},
            {"source": "query", "target": "retrieve"},
            {"source": "retrieve", "target": "generate"},
            {"source": "generate", "target": "end"}
        ]
    
    elif agent_type == "planning":
        nodes = base_nodes + [
            {"id": "plan", "type": "agent", "label": "Plan", "description": "Create execution plan"},
            {"id": "execute", "type": "tool", "label": "Execute", "description": "Run plan steps"},
            {"id": "monitor", "type": "validation", "label": "Monitor", "description": "Track progress"}
        ]
        edges = [
            {"source": "start", "target": "plan"},
            {"source": "plan", "target": "execute"},
            {"source": "execute", "target": "monitor"},
            {"source": "monitor", "target": "execute"},
            {"source": "monitor", "target": "end"}
        ]
    
    else:
        # Generic multi-step agent
        nodes = base_nodes + [
            {"id": "process", "type": "agent", "label": "Process", "description": "Main processing"},
            {"id": "tools", "type": "tool", "label": "Tools", "description": "External tools"},
            {"id": "validate", "type": "validation", "label": "Validate", "description": "Check results"}
        ]
        edges = [
            {"source": "start", "target": "process"},
            {"source": "process", "target": "tools"},
            {"source": "tools", "target": "validate"},
            {"source": "validate", "target": "end"}
        ]
    
    # Add execution trace
    execution_trace = [
        {"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"},
        {"step": 2, "node": nodes[2]["id"], "status": "completed", "duration": 1.2, "output": "Processing..."},
        {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}
    ]
    
    return {
        "nodes": nodes,
        "edges": edges,
        "executionTrace": execution_trace
    }

def generate_mock_state_history(agent_type: str) -> List[Dict[str, Any]]:
    """Generate realistic state history for visualization."""
    
    if agent_type == "react":
        return [
            {
                "timestamp": "2025-01-08T10:00:00Z",
                "step": 1,
                "state": {
                    "current_task": "Analyze problem",
                    "thoughts": ["Need to understand the user's request"],
                    "action_needed": True
                },
                "diff": {"added": ["current_task"], "changed": [], "removed": []}
            },
            {
                "timestamp": "2025-01-08T10:00:01Z", 
                "step": 2,
                "state": {
                    "current_task": "Execute tool",
                    "thoughts": ["Need to search for information", "Using web search tool"],
                    "action_needed": False,
                    "tool_results": "Found relevant information"
                },
                "diff": {"added": ["tool_results"], "changed": ["current_task", "action_needed"], "removed": []}
            }
        ]
    
    return [
        {
            "timestamp": "2025-01-08T10:00:00Z",
            "step": 1,
            "state": {"status": "initialized", "input": "User query"},
            "diff": {"added": ["status", "input"], "changed": [], "removed": []}
        },
        {
            "timestamp": "2025-01-08T10:00:01Z",
            "step": 2, 
            "state": {"status": "processing", "input": "User query", "output": "Generated response"},
            "diff": {"added": ["output"], "changed": ["status"], "removed": []}
        }
    ]

def get_agent_info(module_path: str, class_name: str) -> Dict[str, Any]:
    """Get information about an agent class."""
    
    # Determine agent type from module path
    agent_type = "simple"
    if "react" in module_path:
        agent_type = "react"
    elif "rag" in module_path:
        agent_type = "rag"
    elif "planning" in module_path:
        agent_type = "planning"
    elif "conversation" in module_path:
        agent_type = "conversation"
    elif "research" in module_path:
        agent_type = "research"
    elif "document_modifiers" in module_path:
        agent_type = "document_modifiers"
    elif "reasoning" in module_path:
        agent_type = "reasoning_and_critique"
    
    category = AGENT_CATEGORIES.get(agent_type, AGENT_CATEGORIES["simple"])
    
    return {
        "agent_id": class_name.lower().replace("agent", "").replace("_", "-"),
        "agent_name": class_name,
        "agent_class": class_name,
        "agent_type": agent_type,
        "agent_module_import": module_path,  # For Python import (with dots)
        "agent_module_path": module_path.replace(".", "/"),  # For file paths (with slashes)
        "agent_icon": category["icon"],
        "agent_description": f"{class_name} - {category['description']}",
        "agent_features": ["Interactive", "Visualized", "Stateful", "Async"],
        "agent_config": 'model="gpt-4",\n    temperature=0.7',
        "example_input": f"Example task for {class_name}",
        "agent_architecture_details": f"The {class_name} implements {category['description'].lower()}.",
        "agent_guide": f"{agent_type}-guide",
        "agent_example": f"{agent_type}-examples",
        "graph_data": generate_mock_graph_data(agent_type, class_name),
        "state_history": generate_mock_state_history(agent_type),
        "execution_trace": [
            {"step": 1, "operation": "Initialize", "duration": 0.1, "status": "success"},
            {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"},
            {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"}
        ]
    }

def create_agent_demo_page(agent_info: Dict[str, Any], output_dir: Path) -> None:
    """Create a demo page for an agent."""
    
    # Read template
    template_path = Path(__file__).parent / "source" / "_templates" / "agent_demo_template.rst"
    
    if not template_path.exists():
        print(f"Template not found: {template_path}")
        return
    
    with open(template_path, "r") as f:
        template_content = f.read()
    
    # Use simple string replacement instead of Jinja2 for now
    content = template_content
    for key, value in agent_info.items():
        if isinstance(value, (dict, list)):
            content = content.replace(f"{{{{ {key} | tojson }}}}", json.dumps(value))
        else:
            content = content.replace(f"{{{{ {key} }}}}", str(value))
    
    # Handle loops manually
    features_html = ""
    for feature in agent_info["agent_features"]:
        features_html += f'                <span class="feature-tag">{feature}</span>\n'
    content = content.replace("{% for feature in agent_features %}\n                <span class=\"feature-tag\">{{ feature }}</span>\n                {% endfor %}", features_html.rstrip())
    
    # Create output file
    filename = f"{agent_info['agent_id']}-demo.rst"
    output_file = output_dir / filename
    
    with open(output_file, "w") as f:
        f.write(content)
    
    print(f"Created demo page: {output_file}")

def scan_agent_modules() -> List[Dict[str, Any]]:
    """Scan for agent classes in the codebase."""
    
    # Mock agent data for demonstration
    agents = [
        ("haive.agents.simple", "SimpleAgent"),
        ("haive.agents.simple", "StructuredOutputAgent"),
        ("haive.agents.react", "ReactAgent"),
        ("haive.agents.react", "ReactWithMemoryAgent"),
        ("haive.agents.rag.base", "BaseRAGAgent"),
        ("haive.agents.rag.adaptive_rag", "AdaptiveRAGAgent"),
        ("haive.agents.planning.plan_and_execute", "PlanAndExecuteAgent"),
        ("haive.agents.conversation.debate", "DebateAgent"),
        ("haive.agents.research.person", "PersonResearchAgent"),
        ("haive.agents.document_modifiers.summarizer", "SummarizerAgent"),
        ("haive.agents.reasoning_and_critique.reflection", "ReflectionAgent"),
    ]
    
    return [get_agent_info(module_path, class_name) for module_path, class_name in agents]

def create_demo_index(agents: List[Dict[str, Any]], output_dir: Path) -> None:
    """Create the main demo index page."""
    
    content = """Agent Demos
===========

Interactive demonstrations of all Haive agents with graph visualization, state tracking, and live examples.

.. toctree::
   :maxdepth: 1
   :caption: Agent Demonstrations

"""
    
    # Group agents by type
    by_type = {}
    for agent in agents:
        agent_type = agent["agent_type"]
        if agent_type not in by_type:
            by_type[agent_type] = []
        by_type[agent_type].append(agent)
    
    # Add sections for each type
    for agent_type, agent_list in by_type.items():
        category = AGENT_CATEGORIES.get(agent_type, AGENT_CATEGORIES["simple"])
        content += f"\n{category['icon']} {agent_type.title()} Agents\n"
        content += "~" * (len(agent_type) + 15) + "\n\n"
        
        for agent in agent_list:
            content += f"   {agent['agent_id']}-demo\n"
    
    content += """

.. raw:: html

    <style>
    .agent-demo-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .demo-card {
        background: var(--color-background-secondary);
        border: 1px solid var(--color-background-border);
        border-radius: 12px;
        padding: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .demo-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .demo-card h3 {
        margin-top: 0;
        color: var(--color-brand-primary);
    }
    
    .demo-features {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .feature-tag {
        background: var(--color-brand-primary);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
    }
    </style>

    <div class="agent-demo-grid">
"""
    
    # Add cards for each agent
    for agent in agents:
        category = AGENT_CATEGORIES.get(agent["agent_type"], AGENT_CATEGORIES["simple"])
        content += f"""
        <div class="demo-card">
            <h3>{category['icon']} {agent['agent_name']}</h3>
            <p>{agent['agent_description']}</p>
            <div class="demo-features">
"""
        for feature in agent["agent_features"]:
            content += f'                <span class="feature-tag">{feature}</span>\n'
        
        content += f"""            </div>
            <a href="{agent['agent_id']}-demo.html" class="demo-link">View Demo →</a>
        </div>
"""
    
    content += """    </div>"""
    
    # Write index file
    index_file = output_dir / "index.rst"
    with open(index_file, "w") as f:
        f.write(content)
    
    print(f"Created demo index: {index_file}")

def main():
    """Generate all agent demo pages."""
    
    # Create output directory
    output_dir = Path(__file__).parent / "source" / "agents" / "demos"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Scan for agents
    print("Scanning for agent classes...")
    agents = scan_agent_modules()
    print(f"Found {len(agents)} agents")
    
    # Create demo pages
    print("Creating demo pages...")
    for agent in agents:
        create_agent_demo_page(agent, output_dir)
    
    # Create index
    create_demo_index(agents, output_dir)
    
    print(f"\nGenerated {len(agents)} demo pages in {output_dir}")
    print("Add to your main documentation with:")
    print("   :doc:`/agents/demos/index` - Interactive agent demonstrations")

if __name__ == "__main__":
    main()