# Custom.Reactagent Agent Examples

Real examples and outputs from the custom.ReactAgent agent.

## capture_SimpleAnalysisAgent_SimpleAn

**Source**: `docs/captures/SimpleAnalysisAgent_2dc7adda-3576-49f8-a799-0505a1d9604b_20250626_113523.json`

```json
{
  "run_id": "2dc7adda-3576-49f8-a799-0505a1d9604b",
  "agent_name": "SimpleAnalysisAgent",
  "agent_type": "custom.ReactAgent",
  "start_time": "2025-06-26 11:35:23.149682",
  "end_time": "2025-06-26 11:35:23.150032",
  "input_data": {
    "question": "What are the key components of a sustainable energy system?",
    "context": "renewable energy research"
  },
  "final_output": {
    "messages": [
      {
        "content": "Processed: {'question': 'What are the key components of a sustainable energy system?', 'context': 'renewable energy research'}",
        "type": "result"
      }
    ]
  },
  "steps": [
    {
      "step_id": "8e3cc07f-d3fc-4fa4-a0b1-b4a05146a701",
      "timestamp": "2025-06-26 11:35:23.149984",
      "step_type": "input",
      "node_name": null,
      "content": {
        "data": {
          "question": "What are the key components of a sustainable energy system?",
          "context": "renewable energy research"
        }
      },
      "metadata": {}
    },
    {
      "step_id": "bac913c7-5dd0-48b7-90c8-fe5a49736dbd",
      "timestamp": "2025-06-26 11:35:23.150008",
      "step_type": "message",
      "node_name": null,
      "content": {
        "messages": [
          {
            "content": "Starting processing",
            "type": "system"
          }
        ]
      },
      "metadata": {}
    },
    {
      "step_id": "34c34174-bc35-48a8-b5d0-8326d49f2156",
      "timestamp": "2025-06-26 11:35:23.150016",
      "step_type": "node",
      "node_name": "input_processor",
      "content": {
        "node": "input_processor",
        "content": {
          "question": "What are the key components of a sustainable energy system?",
          "context": "renewable energy research"
        }
      },
      "metadata": {}
    },
    {
      "step_id": "43d6fb61-eaaa-46fe-b6d1-84a293422b59",
      "timestamp": "2025-06-26 11:35:23.150022",
      "step_type": "node",
      "node_name": "main_logic",
      "content": {
        "node": "main_

... (truncated)

```

---

## capture_SimpleAnalysisAgent_SimpleAn

**Source**: `docs/captures/SimpleAnalysisAgent_d3c33b9e-edd8-4749-92e3-bfaaa08e93b6_20250626_113331.json`

```json
{
  "run_id": "d3c33b9e-edd8-4749-92e3-bfaaa08e93b6",
  "agent_name": "SimpleAnalysisAgent",
  "agent_type": "custom.ReactAgent",
  "start_time": "2025-06-26 11:33:31.010886",
  "end_time": "2025-06-26 11:33:31.011913",
  "input_data": {
    "question": "What are the key components of a sustainable energy system?",
    "context": "renewable energy research"
  },
  "final_output": {
    "messages": [
      {
        "content": "Processed: {'question': 'What are the key components of a sustainable energy system?', 'context': 'renewable energy research'}",
        "type": "result"
      }
    ]
  },
  "steps": [
    {
      "step_id": "2e812ebe-147a-4ec0-ad5c-4f7f5bdd82a4",
      "timestamp": "2025-06-26 11:33:31.011868",
      "step_type": "input",
      "node_name": null,
      "content": {
        "data": {
          "question": "What are the key components of a sustainable energy system?",
          "context": "renewable energy research"
        }
      },
      "metadata": {}
    },
    {
      "step_id": "13f94ced-3a68-4c7a-9490-9dcb8cf3a49e",
      "timestamp": "2025-06-26 11:33:31.011888",
      "step_type": "message",
      "node_name": null,
      "content": {
        "messages": [
          {
            "content": "Starting processing",
            "type": "system"
          }
        ]
      },
      "metadata": {}
    },
    {
      "step_id": "82e315dd-600e-4f57-b802-3b46375b1e14",
      "timestamp": "2025-06-26 11:33:31.011895",
      "step_type": "node",
      "node_name": "input_processor",
      "content": {
        "node": "input_processor",
        "content": {
          "question": "What are the key components of a sustainable energy system?",
          "context": "renewable energy research"
        }
      },
      "metadata": {}
    },
    {
      "step_id": "72df0868-39cb-4722-b8df-1d73f22a13f9",
      "timestamp": "2025-06-26 11:33:31.011902",
      "step_type": "node",
      "node_name": "main_logic",
      "content": {
        "node": "main_

... (truncated)

```

---

## capture_ReactResearchAgent_ReactRes

**Source**: `docs/captures/ReactResearchAgent_36df075d-3abb-4e13-a950-807bdb120004_20250626_113523.json`

```json
{
  "run_id": "36df075d-3abb-4e13-a950-807bdb120004",
  "agent_name": "ReactResearchAgent",
  "agent_type": "custom.ReactAgent",
  "start_time": "2025-06-26 11:35:23.152461",
  "end_time": "2025-06-26 11:35:23.152747",
  "input_data": {
    "task": "Research the latest developments in solar panel technology",
    "tools_required": [
      "web_search",
      "pdf_analysis"
    ],
    "max_iterations": 5
  },
  "final_output": {
    "messages": [
      {
        "content": "Processed: {'task': 'Research the latest developments in solar panel technology', 'tools_required': ['web_search', 'pdf_analysis'], 'max_iterations': 5}",
        "type": "result"
      }
    ]
  },
  "steps": [
    {
      "step_id": "5763da8b-73e2-4b25-adc1-48df48e42f19",
      "timestamp": "2025-06-26 11:35:23.152679",
      "step_type": "input",
      "node_name": null,
      "content": {
        "data": {
          "task": "Research the latest developments in solar panel technology",
          "tools_required": [
            "web_search",
            "pdf_analysis"
          ],
          "max_iterations": 5
        }
      },
      "metadata": {}
    },
    {
      "step_id": "dfce467f-e21e-4a0d-810c-7f8a5b4bdb40",
      "timestamp": "2025-06-26 11:35:23.152713",
      "step_type": "message",
      "node_name": null,
      "content": {
        "messages": [
          {
            "content": "Starting processing",
            "type": "system"
          }
        ]
      },
      "metadata": {}
    },
    {
      "step_id": "b170e578-f71f-4f86-b94b-08c29a72008f",
      "timestamp": "2025-06-26 11:35:23.152728",
      "step_type": "node",
      "node_name": "input_processor",
      "content": {
        "node": "input_processor",
        "content": {
          "task": "Research the latest developments in solar panel technology",
          "tools_required": [
            "web_search",
            "pdf_analysis"
          ],
          "max_iterations": 5
        }
      },
      "metadata": {}


... (truncated)

```

---
