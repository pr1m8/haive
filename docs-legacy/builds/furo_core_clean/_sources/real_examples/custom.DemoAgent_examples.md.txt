# Custom.Demoagent Agent Examples

Real examples and outputs from the custom.DemoAgent agent.

## capture_DemoAgent_DemoAgen

**Source**: `docs/captures/DemoAgent_39542cd9-d9dc-4072-8da4-a9495e621bee_20250626_113546.json`

```json
{
  "run_id": "39542cd9-d9dc-4072-8da4-a9495e621bee",
  "agent_name": "DemoAgent",
  "agent_type": "custom.DemoAgent",
  "start_time": "2025-06-26 11:35:46.689722",
  "end_time": "2025-06-26 11:35:46.690140",
  "input_data": {
    "query": "What is artificial intelligence?"
  },
  "final_output": {
    "step": "output",
    "content": {
      "result": "Processed: {'query': 'What is artificial intelligence?'}"
    }
  },
  "steps": [
    {
      "step_id": "266d6f9f-6dc7-496f-a646-a2bd63386272",
      "timestamp": "2025-06-26 11:35:46.690100",
      "step_type": "input",
      "node_name": null,
      "content": {
        "data": {
          "query": "What is artificial intelligence?"
        }
      },
      "metadata": {}
    },
    {
      "step_id": "00ef4df6-9b4a-4d3b-881a-82a27d659060",
      "timestamp": "2025-06-26 11:35:46.690122",
      "step_type": "node",
      "node_name": null,
      "content": {
        "step": "input",
        "content": {
          "query": "What is artificial intelligence?"
        }
      },
      "metadata": {}
    },
    {
      "step_id": "c7ca90c5-777f-4cdc-b4c7-712db7b5f680",
      "timestamp": "2025-06-26 11:35:46.690130",
      "step_type": "node",
      "node_name": null,
      "content": {
        "step": "processing",
        "content": {
          "status": "thinking"
        }
      },
      "metadata": {}
    },
    {
      "step_id": "4e26dadd-778b-4d73-ab5d-5db5c8ea5829",
      "timestamp": "2025-06-26 11:35:46.690137",
      "step_type": "node",
      "node_name": null,
      "content": {
        "step": "output",
        "content": {
          "result": "Processed: {'query': 'What is artificial intelligence?'}"
        }
      },
      "metadata": {}
    }
  ],
  "graph_visualization_path": "docs/captures/39542cd9-d9dc-4072-8da4-a9495e621bee_graph.png",
  "error": null,
  "metadata": {}
}
```

---
