Overview



What is Haive?



Haive is a modern AI agent framework that simplifies the creation of intelligent, collaborative agents. Built with Python and designed for flexibility, Haive provides the building blocks for sophisticated AI workflows.

Architecture



The framework is organized into several key packages:

**Core Packages**

* *haive-core**: Foundation classes, schema system, and graph execution

** *haive-agents**: Pre-built agent types and base classes
** *haive-tools**: Tool integration and management system
** *haive-engines**: LLM engine abstractions and implementations

**Specialized Packages**

* *haive-games**: Gaming-specific agents and frameworks

** *haive-dataflow**: Data processing and pipeline agents
** *haive-prebuilt**: Ready-to-use agent configurations
** *haive-mcp**: Model Context Protocol integration

Design Principles



**Type Safety**: All agents use Pydantic models for state management
**Composability**: Mix and match components to build complex workflows
**Extensibility**: Easy to add new tools, engines, and agent types
**Observability**: Built-in logging, tracing, and debugging support

Use Cases



Haive is designed for:

* *Research Agents**: Information gathering and analysis

** *Conversation Agents**: Multi-turn dialogue and collaboration
** *Game Agents**: Strategic gameplay and competition
** *Workflow Automation**: Complex business process automation
** *Data Processing**: ETL and analysis pipelines
