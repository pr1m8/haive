"""Example demonstrating DynamicAgentDiscoverySupervisor capabilities.

This example shows how the supervisor can:
1. Discover agents dynamically from multiple sources
2. Add specialized agents based on task requirements
3. Route tasks to appropriate specialists
4. Build a team of agents on-demand
"""

import asyncio
import os
import tempfile

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.dynamic_agent_discovery_supervisor import (
    AgentDiscoveryMode,
    DynamicAgentDiscoverySupervisor,
)


async def basic_agent_discovery_example():
    """Basic example of DynamicAgentDiscoverySupervisor."""
    # Configure LLM
    config = AugLLMConfig(temperature=0.1)

    # Start with minimal agents
    initial_agents = {"generalist": SimpleAgent(name="generalist", engine=config)}

    # Create supervisor
    supervisor = DynamicAgentDiscoverySupervisor(
        name="team_builder",
        agents=initial_agents,
        engine=config,
        discovery_mode=AgentDiscoveryMode.HYBRID,
    )

    # Run task that needs specialists
    await supervisor.arun(
        "I need an expert to analyze financial data and another to write a professional report"
    )

    # Check discovered agents


async def factory_with_agent_specs_example():
    """Example using factory method with agent specifications."""
    config = AugLLMConfig(temperature=0.1)

    # Define team specifications
    team_specs = [
        {
            "name": "data_scientist",
            "agent_type": "ReactAgent",
            "description": "Expert in data science and machine learning",
            "specialties": ["data analysis", "machine learning", "statistics"],
            "tools": ["calculator", "data_processor", "ml_toolkit"],
            "config": {"tools": []},  # Will be created with empty tools initially
        },
        {
            "name": "business_analyst",
            "agent_type": "SimpleAgent",
            "description": "Expert in business analysis and strategy",
            "specialties": ["business strategy", "market analysis", "reporting"],
            "tools": [],
            "config": {},
        },
        {
            "name": "technical_writer",
            "agent_type": "SimpleAgent",
            "description": "Expert in technical documentation",
            "specialties": ["documentation", "technical writing", "API docs"],
            "tools": ["markdown_formatter", "code_documenter"],
            "config": {},
        },
    ]

    # Create supervisor with pre-defined team
    supervisor = DynamicAgentDiscoverySupervisor.create_with_agent_specs(
        name="project_team", initial_agent_specs=team_specs, engine=config
    )

    for agent_name, _agent in supervisor.agents.items():
        cap = supervisor.agent_capabilities.get(agent_name)
        if cap:
            pass

    # Run complex project task
    await supervisor.arun(
        "Analyze our sales data, identify trends, and create a comprehensive business report"
    )


async def discovery_sources_example():
    """Example with configured discovery sources."""
    config = AugLLMConfig(temperature=0.1)

    # Create temporary directory with agent documentation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create agent catalog documentation
        catalog_path = os.path.join(temp_dir, "agent_catalog.md")
        with open(catalog_path, "w") as f:
            f.write(
                """# Haive Agent Catalog

## Available Specialist Agents

### Financial Expert Agent
- **Type**: ReactAgent
- **Name**: financial_expert
- **Description**: Specialized in financial analysis, investment strategies, and market trends
- **Specialties**: finance, investments, market analysis, risk assessment
- **Tools**: financial_calculator, market_data_api, risk_analyzer
- **Use Cases**:
  - Portfolio analysis
  - Investment recommendations
  - Financial reporting
  - Risk assessment

### Healthcare Consultant Agent
- **Type**: SimpleAgent
- **Name**: healthcare_consultant
- **Description**: Medical and healthcare industry expert
- **Specialties**: healthcare, medical research, health policy, patient care
- **Tools**: medical_database, symptom_checker, drug_interaction_checker
- **Use Cases**:
  - Medical information queries
  - Healthcare policy analysis
  - Patient care recommendations
  - Medical research assistance

### Legal Advisor Agent
- **Type**: SimpleAgent
- **Name**: legal_advisor
- **Description**: Legal expert for contracts, compliance, and regulations
- **Specialties**: law, contracts, compliance, intellectual property
- **Tools**: legal_database, contract_analyzer, compliance_checker
- **Use Cases**:
  - Contract review
  - Compliance checking
  - Legal research
  - IP guidance

### Marketing Strategist Agent
- **Type**: ReactAgent
- **Name**: marketing_strategist
- **Description**: Digital marketing and brand strategy expert
- **Specialties**: marketing, branding, social media, SEO, content strategy
- **Tools**: seo_analyzer, social_media_tracker, competitor_analysis
- **Use Cases**:
  - Marketing campaign planning
  - Brand strategy development
  - Social media strategy
  - SEO optimization
"""
            )

        # Create supervisor with discovery sources
        supervisor = DynamicAgentDiscoverySupervisor.create_with_discovery(
            name="discovery_supervisor",
            agents={"assistant": SimpleAgent(name="assistant", engine=config)},
            engine=config,
            discovery_mode=AgentDiscoveryMode.HYBRID,
            rag_documents_path=temp_dir,
            component_discovery_config={
                "registry_path": "./agent_registry",
                "scan_packages": ["haive.agents"],
            },
            mcp_config={
                "endpoint": "http://localhost:8000/agents",
                "discover_agents": lambda x: [],  # Mock MCP discovery
            },
        )

        # Run task requiring specialists
        await supervisor.arun(
            "I need help with a legal contract review and then a marketing strategy for the product launch"
        )


async def dynamic_team_building_example():
    """Example showing dynamic team building based on project needs."""
    config = AugLLMConfig(temperature=0.1)

    # Start with just a project manager
    supervisor = DynamicAgentDiscoverySupervisor(
        name="project_supervisor",
        agents={"project_manager": SimpleAgent(name="project_manager", engine=config)},
        engine=config,
    )

    # Series of tasks that require different specialists
    tasks = [
        "We need to analyze customer data to identify purchasing patterns",
        "Based on the analysis, create a new product strategy",
        "Develop technical specifications for the product",
        "Create marketing materials and launch campaign",
        "Ensure all activities comply with regulations",
    ]

    for _i, task in enumerate(tasks):

        # Check team before task

        # Execute task
        await supervisor.arun(task)

        # Check if new agents were discovered
        if len(supervisor.discovered_agents) > 0:
            pass


async def agent_capability_routing_example():
    """Example showing routing based on agent capabilities."""
    config = AugLLMConfig(temperature=0.1)

    # Create diverse team with specific capabilities
    team_specs = [
        {
            "name": "frontend_dev",
            "agent_type": "ReactAgent",
            "description": "Frontend development expert",
            "specialties": ["React", "Vue", "CSS", "UI/UX"],
            "tools": ["code_editor", "browser_dev_tools"],
            "config": {"tools": []},
        },
        {
            "name": "backend_dev",
            "agent_type": "ReactAgent",
            "description": "Backend development expert",
            "specialties": ["Python", "Node.js", "databases", "APIs"],
            "tools": ["code_editor", "database_client"],
            "config": {"tools": []},
        },
        {
            "name": "devops_engineer",
            "agent_type": "SimpleAgent",
            "description": "DevOps and infrastructure expert",
            "specialties": ["Docker", "Kubernetes", "CI/CD", "AWS"],
            "tools": ["terminal", "cloud_console"],
            "config": {},
        },
        {
            "name": "qa_engineer",
            "agent_type": "SimpleAgent",
            "description": "Quality assurance expert",
            "specialties": ["testing", "automation", "bug tracking"],
            "tools": ["test_runner", "bug_tracker"],
            "config": {},
        },
    ]

    supervisor = DynamicAgentDiscoverySupervisor.create_with_agent_specs(
        name="dev_team_supervisor", initial_agent_specs=team_specs, engine=config
    )

    for _name, _cap in supervisor.agent_capabilities.items():
        pass

    # Test routing for different technical tasks
    technical_tasks = [
        "Fix the responsive design issues on the landing page",
        "Optimize the database queries for better performance",
        "Set up automated deployment pipeline",
        "Write comprehensive tests for the user authentication flow",
    ]

    for task in technical_tasks:

        # Simulate routing decision
        from haive.agents.supervisor.types import SupervisorState

        state = SupervisorState(
            messages=[HumanMessage(content=task)], next_agent="", agent_outputs={}
        )

        await supervisor._make_decision(state)


async def performance_tracking_example():
    """Example showing agent performance tracking."""
    config = AugLLMConfig(temperature=0.1)

    # Create team
    supervisor = DynamicAgentDiscoverySupervisor.create_with_agent_specs(
        name="performance_supervisor",
        initial_agent_specs=[
            {
                "name": "agent_a",
                "agent_type": "SimpleAgent",
                "description": "General agent A",
            },
            {
                "name": "agent_b",
                "agent_type": "SimpleAgent",
                "description": "General agent B",
            },
            {
                "name": "agent_c",
                "agent_type": "ReactAgent",
                "description": "General agent C",
                "config": {"tools": []},
            },
        ],
        engine=config,
    )

    # Run several tasks
    test_tasks = [
        "Write a short poem",
        "Explain quantum computing",
        "Solve this math problem: 15 * 23",
        "Translate 'Hello' to Spanish",
        "Create a todo list for a project",
    ]

    for task in test_tasks:
        await supervisor.arun(task)

    # Show agent utilization
    if hasattr(supervisor.state, "agent_execution_count"):
        for _agent, _count in supervisor.state.agent_execution_count.items():
            pass


async def main():
    """Run all examples."""
    await basic_agent_discovery_example()
    await factory_with_agent_specs_example()
    await discovery_sources_example()
    await dynamic_team_building_example()
    await agent_capability_routing_example()
    await performance_tracking_example()


if __name__ == "__main__":

    # Run examples
    asyncio.run(main())
