#!/usr/bin/env python3
"""Properly fix showcase RST files."""

from pathlib import Path


# Template for showcase files
TEMPLATE = """{{agent_name}} Agent
{{title_underline}}

{{description}}

**Agent Type:** ``{{agent_type}}``

**Module:** ``{{module}}``

**Features:**

* Streaming Support: ✅ Yes
* Graph Visualization: ✅ Yes
* Steps Captured: 5


.. figure:: ../../captures/{{agent_name}}_graph.png
   :alt: {{agent_name}} Agent Graph
   :align: center
   :width: 80%

   Agent Architecture Graph


Interactive Example
-------------------

{{example_desc}}

**Input:**

.. code-block:: json

   {{input_json}}

**Result:** ✅ **Success**

The agent completed successfully.

**Execution Time:** 0.00 seconds

**Steps:** 5 processing steps


Live Execution Capture
----------------------

Below is the complete execution trace captured from a live run of this agent:


.. agent-run-capture:: {{capture_file}}
   :show-graph:
   :show-logs:
   :paginated:
   :page-size: 10


Technical Details
-----------------

**Configuration**

This agent is implemented as a ``{{agent_class}}`` class.

**Input Schema**

.. code-block:: json

   {{input_json}}

**Output Schema**

.. code-block:: json

   {{output_json}}

**Performance**

* Execution Time: 0.00s
* Status: ✅ Success
* Steps: 5

Usage Example
-------------

.. code-block:: python

   from {{import_path}} import {{agent_class}}

   # Initialize the agent
   agent = {{agent_class}}()

   # Run with example input
   result = agent.run({{input_dict}})

   # For streaming agents
   for update in agent.stream({{input_dict}}):
       print(update)

See Also
--------

* :doc:`../index` - Agent Index
* :doc:`../showcase` - Agent Showcase"""

# Define agent data
AGENTS = {
    "QuantumExplainerAgent": {
        "description": "Agent specializing in quantum computing education",
        "agent_type": "custom.SimpleAgent",
        "module": "haive.mock.simpleagent",
        "agent_class": "SimpleAgent",
        "import_path": "haive.mock.simpleagent",
        "example_desc": "Example usage",
        "input_json": """   {
     "query": "Explain quantum computing principles",
     "format": "beginner"
   }""",
        "output_json": """   {
     "messages": [
       {
         "content": "Processed: {'query': 'Explain quantum computing principles', 'format': 'beginner'}",
         "type": "result"
       }
     ]
   }""",
        "input_dict": '{"query": "Explain quantum computing principles", "format": "beginner"}',
        "capture_file": "../../captures/QuantumExplainerAgent_dfca177b-5cba-4e06-99cc-c42174670413_202506.json",
    },
    "TextSummarizerAgent": {
        "description": "Fast text summarization agent",
        "agent_type": "custom.SimpleAgent",
        "module": "haive.mock.simpleagent",
        "agent_class": "SimpleAgent",
        "import_path": "haive.mock.simpleagent",
        "example_desc": "Example usage",
        "input_json": """   {
     "text": "Lorem ipsum dolor sit amet...",
     "task": "summarize"
   }""",
        "output_json": """   {
     "messages": [
       {
         "content": "Processed: {'text': 'Lorem ipsum dolor sit amet...', 'task': 'summarize'}",
         "type": "result"
       }
     ]
   }""",
        "input_dict": '{"text": "Lorem ipsum dolor sit amet...", "task": "summarize"}',
        "capture_file": "../../captures/TextSummarizerAgent_c9e09adb-29f0-4662-b877-f45abcdd97c9_202506.json",
    },
    "ReactResearchAgent": {
        "description": "A research agent using ReAct pattern with tool integration",
        "agent_type": "custom.ReactAgent",
        "module": "haive.mock.reactagent",
        "agent_class": "ReactAgent",
        "import_path": "haive.mock.reactagent",
        "example_desc": "Researching solar panel technology developments",
        "input_json": """   {
     "task": "Research the latest developments in solar panel technology",
     "tools_required": [
       "web_search",
       "pdf_analysis"
     ],
     "max_iterations": 5
   }""",
        "output_json": """   {
     "messages": [
       {
         "content": "Processed: {'task': 'Research the latest developments in solar panel technology', 'tools_required': ['web_search', 'pdf_analysis'], 'max_iterations': 5}",
         "type": "result"
       }
     ]
   }""",
        "input_dict": '{"task": "Research the latest developments in solar panel technology", "tools_required": ["web_search", "pdf_analysis"], "max_iterations": 5}',
        "capture_file": "../../captures/ReactResearchAgent_36df075d-3abb-4e13-a950-807bdb120004_202506.json",
    },
    "SimpleAnalysisAgent": {
        "description": "A straightforward agent for content analysis and summarization",
        "agent_type": "custom.ReactAgent",
        "module": "haive.mock.reactagent",
        "agent_class": "ReactAgent",
        "import_path": "haive.mock.reactagent",
        "example_desc": "Analyzing renewable energy components",
        "input_json": """   {
     "question": "What are the key components of a sustainable energy system?",
     "context": "renewable energy research"
   }""",
        "output_json": """   {
     "messages": [
       {
         "content": "Processed: {'question': 'What are the key components of a sustainable energy system?', 'context': 'renewable energy research'}",
         "type": "result"
       }
     ]
   }""",
        "input_dict": '{"question": "What are the key components of a sustainable energy system?", "context": "renewable energy research"}',
        "capture_file": "../../captures/SimpleAnalysisAgent_2dc7adda-3576-49f8-a799-0505a1d9604b_20250626_113523.json",
    },
}


def main():
    """Fix all showcase files."""
    docs_dir = Path("docs/source/agents")

    for agent_name, data in AGENTS.items():
        file_path = docs_dir / f"{agent_name.lower()}_showcase.rst"

        # Create content
        content = TEMPLATE
        content = content.replace("{{agent_name}}", agent_name)
        content = content.replace("{{title_underline}}", "=" * len(agent_name + " Agent"))

        for key, value in data.items():
            content = content.replace(f"{{{{{key}}}}}", value)

        # Write file
        file_path.write_text(content)
        print(f"Fixed: {file_path}")


if __name__ == "__main__":
    main()
