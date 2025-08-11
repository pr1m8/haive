"""Agent demo data configuration for Sphinx Jinja2 templates.

This file contains all the data needed to render agent demo templates.
"""

# Agent configuration data
AGENT_DATA = {
    "simple": {
        "agent_name": "SimpleAgent",
        "agent_description": "SimpleAgent - Basic conversational agents for straightforward tasks",
        "agent_icon": "🤖",
        "agent_type": "simple",
        "agent_id": "simple",
        "agent_features": ["Interactive", "Visualized", "Stateful", "Async"],
        "agent_module_import": "haive.agents.simple",
        "agent_class": "SimpleAgent",
        "agent_module_path": "haive/agents/simple",
        "agent_guide": "simple-guide",
        "agent_example": "simple-examples",
        "agent_config": """model="gpt-4",
    temperature=0.7""",
        "example_input": "Example task for SimpleAgent",
        "agent_architecture_details": "The SimpleAgent implements basic conversational agents for straightforward tasks.",
        "graph_data": {
            "nodes": [
                {"id": "start", "type": "start", "label": "START"},
                {"id": "end", "type": "end", "label": "END"},
                {
                    "id": "agent",
                    "type": "agent",
                    "label": "SimpleAgent",
                    "description": "Main processing node",
                },
            ],
            "edges": [
                {"source": "start", "target": "agent"},
                {"source": "agent", "target": "end"},
            ],
            "executionTrace": [
                {
                    "step": 1,
                    "node": "start",
                    "status": "completed",
                    "duration": 0.1,
                    "output": "Initialized",
                },
                {
                    "step": 2,
                    "node": "agent",
                    "status": "completed",
                    "duration": 1.2,
                    "output": "Processing...",
                },
                {
                    "step": 3,
                    "node": "end",
                    "status": "completed",
                    "duration": 0.1,
                    "output": "Finished",
                },
            ],
        },
        "state_history": [
            {
                "timestamp": "2025-01-08T10:00:00Z",
                "step": 1,
                "state": {"status": "initialized", "input": "User query"},
                "diff": {"added": ["status", "input"], "changed": [], "removed": []},
            },
            {
                "timestamp": "2025-01-08T10:00:01Z",
                "step": 2,
                "state": {
                    "status": "processing",
                    "input": "User query",
                    "output": "Generated response",
                },
                "diff": {"added": ["output"], "changed": ["status"], "removed": []},
            },
        ],
        "execution_trace": [
            {
                "step": 1,
                "operation": "Initialize",
                "duration": 0.1,
                "status": "success",
            },
            {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"},
            {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"},
        ],
    },
    "react": {
        "agent_name": "ReactAgent",
        "agent_description": "ReactAgent - Reasoning and Acting agents that think before they act",
        "agent_icon": "🧠",
        "agent_type": "react",
        "agent_id": "react",
        "agent_features": ["Interactive", "Visualized", "Stateful", "Async"],
        "agent_module_import": "haive.agents.react",
        "agent_class": "ReactAgent",
        "agent_module_path": "haive/agents/react",
        "agent_guide": "react-guide",
        "agent_example": "react-examples",
        "agent_config": """model="gpt-4",
    temperature=0.7,
    tools=[calculator_tool]""",
        "example_input": "Calculate 15 * 23 and explain the result",
        "agent_architecture_details": "The ReactAgent implements reasoning and acting agents that think before they act.",
        "graph_data": {
            "nodes": [
                {"id": "start", "type": "start", "label": "START"},
                {
                    "id": "think",
                    "type": "agent",
                    "label": "Think",
                    "description": "Reasoning step",
                },
                {
                    "id": "act",
                    "type": "agent",
                    "label": "Act",
                    "description": "Action step",
                },
                {
                    "id": "observe",
                    "type": "agent",
                    "label": "Observe",
                    "description": "Observation step",
                },
                {"id": "end", "type": "end", "label": "END"},
            ],
            "edges": [
                {"source": "start", "target": "think"},
                {"source": "think", "target": "act"},
                {"source": "act", "target": "observe"},
                {"source": "observe", "target": "think"},
                {"source": "think", "target": "end"},
            ],
            "executionTrace": [
                {
                    "step": 1,
                    "node": "start",
                    "status": "completed",
                    "duration": 0.1,
                    "output": "Initialized",
                },
                {
                    "step": 2,
                    "node": "think",
                    "status": "completed",
                    "duration": 1.5,
                    "output": "Reasoning...",
                },
                {
                    "step": 3,
                    "node": "act",
                    "status": "completed",
                    "duration": 0.8,
                    "output": "Acting...",
                },
                {
                    "step": 4,
                    "node": "observe",
                    "status": "completed",
                    "duration": 0.3,
                    "output": "Observing...",
                },
                {
                    "step": 5,
                    "node": "end",
                    "status": "completed",
                    "duration": 0.1,
                    "output": "Finished",
                },
            ],
        },
        "state_history": [
            {
                "timestamp": "2025-01-08T10:00:00Z",
                "step": 1,
                "state": {"status": "initialized", "input": "User query"},
                "diff": {"added": ["status", "input"], "changed": [], "removed": []},
            },
            {
                "timestamp": "2025-01-08T10:00:01Z",
                "step": 2,
                "state": {
                    "status": "thinking",
                    "input": "User query",
                    "thoughts": "Need to calculate...",
                },
                "diff": {"added": ["thoughts"], "changed": ["status"], "removed": []},
            },
        ],
        "execution_trace": [
            {
                "step": 1,
                "operation": "Initialize",
                "duration": 0.1,
                "status": "success",
            },
            {"step": 2, "operation": "Think", "duration": 1.2, "status": "success"},
            {"step": 3, "operation": "Act", "duration": 0.8, "status": "success"},
            {"step": 4, "operation": "Observe", "duration": 0.3, "status": "success"},
        ],
    },
    "baserag": {
        "agent_name": "BaseRAGAgent",
        "agent_description": "BaseRAGAgent - Retrieval-Augmented Generation agents with knowledge",
        "agent_icon": "📚",
        "agent_type": "rag",
        "agent_id": "baserag",
        "agent_features": ["Interactive", "Visualized", "Stateful", "Async"],
        "agent_module_import": "haive.agents.rag.base",
        "agent_class": "BaseRAGAgent",
        "agent_module_path": "haive/agents/rag/base",
        "agent_guide": "rag-guide",
        "agent_example": "rag-examples",
        "agent_config": """model="gpt-4",
    temperature=0.7,
    retriever=vector_store_retriever""",
        "example_input": "What is the purpose of Haive framework?",
        "agent_architecture_details": "The BaseRAGAgent implements retrieval-augmented generation with knowledge bases.",
        "graph_data": {
            "nodes": [
                {"id": "start", "type": "start", "label": "START"},
                {
                    "id": "retrieve",
                    "type": "agent",
                    "label": "Retrieve",
                    "description": "Knowledge retrieval",
                },
                {
                    "id": "generate",
                    "type": "agent",
                    "label": "Generate",
                    "description": "Response generation",
                },
                {"id": "end", "type": "end", "label": "END"},
            ],
            "edges": [
                {"source": "start", "target": "retrieve"},
                {"source": "retrieve", "target": "generate"},
                {"source": "generate", "target": "end"},
            ],
            "executionTrace": [
                {
                    "step": 1,
                    "node": "start",
                    "status": "completed",
                    "duration": 0.1,
                    "output": "Initialized",
                },
                {
                    "step": 2,
                    "node": "retrieve",
                    "status": "completed",
                    "duration": 0.8,
                    "output": "Retrieved docs",
                },
                {
                    "step": 3,
                    "node": "generate",
                    "status": "completed",
                    "duration": 1.5,
                    "output": "Generated response",
                },
                {
                    "step": 4,
                    "node": "end",
                    "status": "completed",
                    "duration": 0.1,
                    "output": "Finished",
                },
            ],
        },
        "state_history": [
            {
                "timestamp": "2025-01-08T10:00:00Z",
                "step": 1,
                "state": {"status": "initialized", "input": "User query"},
                "diff": {"added": ["status", "input"], "changed": [], "removed": []},
            },
            {
                "timestamp": "2025-01-08T10:00:01Z",
                "step": 2,
                "state": {
                    "status": "retrieving",
                    "input": "User query",
                    "documents": ["doc1", "doc2"],
                },
                "diff": {"added": ["documents"], "changed": ["status"], "removed": []},
            },
        ],
        "execution_trace": [
            {
                "step": 1,
                "operation": "Initialize",
                "duration": 0.1,
                "status": "success",
            },
            {"step": 2, "operation": "Retrieve", "duration": 0.8, "status": "success"},
            {"step": 3, "operation": "Generate", "duration": 1.5, "status": "success"},
        ],
    },
}


# Template context for Jinja2 rendering
def get_agent_context(agent_id):
    """Get template context for a specific agent."""
    if agent_id not in AGENT_DATA:
        raise ValueError(f"Agent {agent_id} not found in AGENT_DATA")

    context = AGENT_DATA[agent_id].copy()

    # Add JSON serialization for JavaScript data
    import json

    context["graph_data_json"] = json.dumps(context["graph_data"])
    context["state_history_json"] = json.dumps(context["state_history"])
    context["execution_trace_json"] = json.dumps(context["execution_trace"])

    return context


# All available agents
AVAILABLE_AGENTS = list(AGENT_DATA.keys())
