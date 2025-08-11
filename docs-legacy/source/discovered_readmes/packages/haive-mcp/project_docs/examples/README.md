# MCP Examples

**Working code examples for dynamic MCP integration with Haive agents**

## 🎯 Overview

This directory contains comprehensive, working examples demonstrating various MCP integration patterns with Haive agents. All examples are production-ready and include proper error handling.

## 📚 Example Categories

### 🚀 Basic Examples

- **[Basic MCP Agent](#basic-mcp-agent)** - Simple static configuration
- **[Intelligent Discovery](#intelligent-discovery)** - Dynamic server discovery
- **[Tool Sharing](#tool-sharing)** - Agents sharing capabilities

### 🏗️ Advanced Examples

- **[Multi-Agent Workflows](#multi-agent-workflows)** - Coordinated agent systems
- **[Custom Discovery](#custom-discovery)** - Domain-specific discovery logic
- **[Production Deployment](#production-deployment)** - Enterprise-ready patterns

### 🎨 Domain-Specific Examples

- **[Research Assistant](#research-assistant)** - Academic/market research
- **[Data Analysis Pipeline](#data-analysis-pipeline)** - Data science workflows
- **[DevOps Automation](#devops-automation)** - Infrastructure management

## 🚀 Basic Examples

### Basic MCP Agent

Simple agent with pre-configured MCP servers.

```python
# examples/basic_mcp_agent.py
"""Basic MCP agent with static server configuration."""

import asyncio
import logging
from haive.mcp.agents import MCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig
from haive.core.engine.aug_llm import AugLLMConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Basic MCP agent example."""

    # Configure MCP servers
    config = MCPConfig(
        servers={
            "filesystem": MCPServerConfig(
                name="filesystem",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "./workspace"]
            ),
            "calculator": MCPServerConfig(
                name="calculator",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-calculator"]
            )
        }
    )

    # Create agent
    agent = MCPAgent(
        name="basic_agent",
        engine=AugLLMConfig(temperature=0.3),
        mcp_config=config
    )

    try:
        # Setup agent
        await agent.setup()
        logger.info(f"Agent setup complete. Available tools: {len(agent.mcp_tools)}")

        # Example interactions
        tasks = [
            "List the files in the current directory",
            "Calculate 15 * 23 + 47",
            "Create a file called 'results.txt' with the calculation result"
        ]

        for task in tasks:
            print(f"\n📝 Task: {task}")
            result = await agent.arun({
                "messages": [{"role": "user", "content": task}]
            })
            print(f"✅ Result: {result}")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Cleanup
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### Intelligent Discovery

Agent that automatically discovers and installs needed MCP servers.

```python
# examples/intelligent_discovery.py
"""Intelligent agent with automatic MCP server discovery."""

import asyncio
import logging
from haive.mcp.agents import IntelligentMCPAgent
from haive.core.engine.aug_llm import AugLLMConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def approval_callback(request):
    """Custom approval logic for server installations."""
    print(f"\n🔔 MCP Server Installation Request")
    print(f"Server: {request.recommendation.server_name}")
    print(f"Reason: {request.recommendation.reason}")
    print(f"Capabilities: {', '.join(request.recommendation.capabilities)}")
    print(f"Confidence: {request.recommendation.confidence:.2f}")

    # Auto-approve high-confidence, safe servers
    safe_servers = ["filesystem", "calculator", "weather", "datetime"]
    if (request.recommendation.server_name in safe_servers and
        request.recommendation.confidence > 0.8):
        print("✅ Auto-approved (safe server with high confidence)")
        return True

    # Ask for manual approval
    while True:
        response = input("Approve installation? (y/n/details): ").lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        elif response == 'details':
            print(f"Setup: {request.recommendation.setup_instructions}")
            print(f"Documentation: {request.recommendation.documentation_url}")
        else:
            print("Please enter 'y', 'n', or 'details'")

async def main():
    """Intelligent discovery example."""

    # Create intelligent agent
    agent = IntelligentMCPAgent(
        name="intelligent_agent",
        engine=AugLLMConfig(temperature=0.5),
        auto_discover=True,
        require_approval=True,
        approval_callback=approval_callback,
        approval_timeout=60.0  # 1 minute timeout
    )

    try:
        await agent.setup()

        # Example tasks that require different capabilities
        tasks = [
            "What's the weather like in San Francisco today?",
            "Search for recent papers about machine learning and save results to a spreadsheet",
            "Analyze the data in sales.csv and create visualizations",
            "Deploy the latest version of my web application to production"
        ]

        for i, task in enumerate(tasks, 1):
            print(f"\n{'='*60}")
            print(f"Task {i}: {task}")
            print('='*60)

            try:
                result = await agent.arun({
                    "messages": [{"role": "user", "content": task}]
                })
                print(f"✅ Completed: {result}")

                # Show current tool inventory
                tools = await agent.get_mcp_tools()
                print(f"📦 Available tools: {len(tools)} ({', '.join(tools.keys())})")

            except Exception as e:
                print(f"❌ Task failed: {e}")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### Tool Sharing

Agents sharing tools and capabilities with each other.

```python
# examples/tool_sharing.py
"""Example of agents sharing MCP tools."""

import asyncio
import logging
from haive.mcp.agents import TransferableMCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig
from haive.core.engine.aug_llm import AugLLMConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Tool sharing example."""

    # Create agent with web tools
    web_config = MCPConfig(
        servers={
            "brave_search": MCPServerConfig(
                name="brave_search",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-brave-search"],
                env={"BRAVE_API_KEY": "your-api-key"}  # Replace with real key
            ),
            "web_scraper": MCPServerConfig(
                name="web_scraper",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-puppeteer"]
            )
        }
    )

    # Create agent with data tools
    data_config = MCPConfig(
        servers={
            "filesystem": MCPServerConfig(
                name="filesystem",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "./data"]
            ),
            "sqlite": MCPServerConfig(
                name="sqlite",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-sqlite", "./data/analysis.db"]
            )
        }
    )

    # Create transferable agents
    web_agent = TransferableMCPAgent(
        name="web_specialist",
        engine=AugLLMConfig(temperature=0.3),
        mcp_config=web_config
    )

    data_agent = TransferableMCPAgent(
        name="data_specialist",
        engine=AugLLMConfig(temperature=0.2),
        mcp_config=data_config
    )

    try:
        # Setup both agents
        await web_agent.setup()
        await data_agent.setup()

        print("🔧 Initial tool inventories:")
        web_tools = await web_agent.get_mcp_tools()
        data_tools = await data_agent.get_mcp_tools()

        print(f"Web agent tools: {list(web_tools.keys())}")
        print(f"Data agent tools: {list(data_tools.keys())}")

        # Transfer web tools to data agent
        print("\n🔄 Transferring web tools to data agent...")
        await web_agent.transfer_tools_to_agent(
            data_agent,
            tool_names=["web_search", "scrape_page"]
        )

        # Transfer data tools to web agent
        print("🔄 Transferring data tools to web agent...")
        await data_agent.transfer_tools_to_agent(
            web_agent,
            tool_names=["read_file", "write_file", "sql_query"]
        )

        print("\n🔧 Updated tool inventories:")
        web_tools_updated = await web_agent.get_mcp_tools()
        data_tools_updated = await data_agent.get_mcp_tools()

        print(f"Web agent tools: {list(web_tools_updated.keys())}")
        print(f"Data agent tools: {list(data_tools_updated.keys())}")

        # Now both agents can do web + data tasks
        print("\n📊 Testing combined capabilities:")

        # Data agent can now search web
        result1 = await data_agent.arun({
            "messages": [{
                "role": "user",
                "content": "Search for 'Python data analysis best practices' and save top 5 results to a file"
            }]
        })
        print(f"Data agent web task: {result1}")

        # Web agent can now work with files
        result2 = await web_agent.arun({
            "messages": [{
                "role": "user",
                "content": "Read the search results file and create a summary report"
            }]
        })
        print(f"Web agent data task: {result2}")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await web_agent.cleanup()
        await data_agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🏗️ Advanced Examples

### Multi-Agent Workflows

Coordinated system of specialized agents working together.

```python
# examples/multi_agent_workflow.py
"""Multi-agent workflow with MCP capabilities."""

import asyncio
import logging
from typing import Dict, Any
from haive.mcp.agents import IntelligentMCPAgent, MCPAgent
from haive.agents.multi import MultiAgent
from haive.core.engine.aug_llm import AugLLMConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowCoordinator:
    """Coordinates multi-agent workflows with MCP capabilities."""

    def __init__(self):
        self.agents: Dict[str, MCPAgent] = {}

    async def create_research_workflow(self) -> MultiAgent:
        """Create a research workflow with specialized agents."""

        # Research agent - web search and data collection
        research_agent = IntelligentMCPAgent(
            name="researcher",
            engine=AugLLMConfig(temperature=0.3),
            auto_discover=True,
            require_approval=False  # Auto-approve for research tools
        )

        # Analysis agent - data processing and analysis
        analysis_agent = IntelligentMCPAgent(
            name="analyst",
            engine=AugLLMConfig(temperature=0.2),
            auto_discover=True,
            require_approval=False
        )

        # Writer agent - report generation and documentation
        writer_agent = IntelligentMCPAgent(
            name="writer",
            engine=AugLLMConfig(temperature=0.7),
            auto_discover=True,
            require_approval=False
        )

        # Setup all agents
        await asyncio.gather(
            research_agent.setup(),
            analysis_agent.setup(),
            writer_agent.setup()
        )

        self.agents = {
            "researcher": research_agent,
            "analyst": analysis_agent,
            "writer": writer_agent
        }

        # Create multi-agent coordinator
        return MultiAgent(
            agents=self.agents,
            execution_mode="sequential"  # Research → Analysis → Writing
        )

    async def execute_research_project(self, topic: str) -> Dict[str, Any]:
        """Execute complete research project."""

        workflow = await self.create_research_workflow()

        results = {}

        # Phase 1: Research
        print(f"🔍 Phase 1: Researching '{topic}'")
        research_result = await self.agents["researcher"].arun({
            "messages": [{
                "role": "user",
                "content": f"Research the topic '{topic}'. Find recent papers, articles, and data. Save all findings to structured files."
            }]
        })
        results["research"] = research_result

        # Phase 2: Analysis
        print(f"📊 Phase 2: Analyzing research data")
        analysis_result = await self.agents["analyst"].arun({
            "messages": [{
                "role": "user",
                "content": f"Analyze the research data collected about '{topic}'. Identify key trends, patterns, and insights. Create visualizations and statistical summaries."
            }]
        })
        results["analysis"] = analysis_result

        # Phase 3: Report Writing
        print(f"📝 Phase 3: Writing research report")
        report_result = await self.agents["writer"].arun({
            "messages": [{
                "role": "user",
                "content": f"Write a comprehensive research report on '{topic}' using the research data and analysis. Include executive summary, methodology, findings, and recommendations."
            }]
        })
        results["report"] = report_result

        return results

    async def cleanup(self):
        """Cleanup all agents."""
        for agent in self.agents.values():
            await agent.cleanup()

async def main():
    """Multi-agent workflow example."""

    coordinator = WorkflowCoordinator()

    try:
        # Execute research project
        results = await coordinator.execute_research_project(
            "Impact of AI on software development productivity"
        )

        print("\n" + "="*60)
        print("WORKFLOW RESULTS")
        print("="*60)

        for phase, result in results.items():
            print(f"\n{phase.upper()}:")
            print("-" * 40)
            print(result)

    except Exception as e:
        logger.error(f"Workflow error: {e}")
    finally:
        await coordinator.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Discovery

Domain-specific discovery logic for specialized use cases.

```python
# examples/custom_discovery.py
"""Custom discovery logic for domain-specific MCP integration."""

import asyncio
import re
from typing import List, Dict
from haive.mcp.agents import IntelligentMCPAgent
from haive.mcp.discovery import MCPServerDiscovery
from haive.core.engine.aug_llm import AugLLMConfig

class BioinformaticsDiscoveryAgent(IntelligentMCPAgent):
    """Specialized agent for bioinformatics with custom discovery logic."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Domain-specific capability mappings
        self.bio_capability_map = {
            "sequence": ["ncbi", "uniprot", "ensembl", "blast"],
            "structure": ["pdb", "alphafold", "pymol", "chembl"],
            "pathway": ["kegg", "reactome", "go", "string"],
            "literature": ["pubmed", "biorxiv", "semantic_scholar"],
            "analysis": ["r_bioconductor", "python_biopython", "galaxy"],
            "visualization": ["cytoscape", "igv", "matplotlib", "plotly"]
        }

    async def _analyze_capability_needs(self, user_message: str) -> List[str]:
        """Enhanced capability analysis for bioinformatics."""

        # Start with base analysis
        base_capabilities = await super()._analyze_capability_needs(user_message)

        # Add domain-specific analysis
        bio_capabilities = []
        message_lower = user_message.lower()

        # Sequence analysis keywords
        sequence_keywords = ["dna", "rna", "protein", "sequence", "blast", "alignment", "fasta"]
        if any(keyword in message_lower for keyword in sequence_keywords):
            bio_capabilities.extend(self.bio_capability_map["sequence"])

        # Structure analysis keywords
        structure_keywords = ["structure", "fold", "3d", "pdb", "crystal", "binding"]
        if any(keyword in message_lower for keyword in structure_keywords):
            bio_capabilities.extend(self.bio_capability_map["structure"])

        # Pathway analysis keywords
        pathway_keywords = ["pathway", "network", "interaction", "go", "kegg", "regulation"]
        if any(keyword in message_lower for keyword in pathway_keywords):
            bio_capabilities.extend(self.bio_capability_map["pathway"])

        # Literature keywords
        literature_keywords = ["paper", "literature", "pubmed", "research", "publication"]
        if any(keyword in message_lower for keyword in literature_keywords):
            bio_capabilities.extend(self.bio_capability_map["literature"])

        # Combine and deduplicate
        all_capabilities = list(set(base_capabilities + bio_capabilities))

        return all_capabilities

    async def analyze_gene_expression(self, dataset_path: str):
        """Specialized workflow for gene expression analysis."""

        workflow_steps = [
            "Load and validate gene expression dataset",
            "Perform quality control and normalization",
            "Identify differentially expressed genes",
            "Perform pathway enrichment analysis",
            "Create visualizations and heatmaps",
            "Generate biological interpretation report"
        ]

        results = []
        for step in workflow_steps:
            print(f"🧬 {step}...")
            result = await self.arun({
                "messages": [{
                    "role": "user",
                    "content": f"{step} for dataset at {dataset_path}"
                }]
            })
            results.append(result)

        return results

class FinanceDiscoveryAgent(IntelligentMCPAgent):
    """Specialized agent for financial analysis with custom discovery."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.finance_capability_map = {
            "market_data": ["yahoo_finance", "bloomberg", "alpha_vantage", "quandl"],
            "analysis": ["pandas", "numpy", "scipy", "statsmodels"],
            "visualization": ["matplotlib", "plotly", "seaborn", "bokeh"],
            "risk": ["value_at_risk", "monte_carlo", "portfolio_optimization"],
            "news": ["financial_news", "sentiment_analysis", "economic_calendar"],
            "reporting": ["excel", "pdf_generation", "powerpoint", "dashboard"]
        }

    async def _analyze_capability_needs(self, user_message: str) -> List[str]:
        """Financial domain capability analysis."""

        base_capabilities = await super()._analyze_capability_needs(user_message)

        finance_capabilities = []
        message_lower = user_message.lower()

        # Market data keywords
        if any(word in message_lower for word in ["stock", "price", "market", "ticker", "quote"]):
            finance_capabilities.extend(self.finance_capability_map["market_data"])

        # Risk analysis keywords
        if any(word in message_lower for word in ["risk", "volatility", "var", "portfolio"]):
            finance_capabilities.extend(self.finance_capability_map["risk"])

        # News and sentiment keywords
        if any(word in message_lower for word in ["news", "sentiment", "earnings", "announcement"]):
            finance_capabilities.extend(self.finance_capability_map["news"])

        return list(set(base_capabilities + finance_capabilities))

    async def portfolio_analysis(self, tickers: List[str], start_date: str, end_date: str):
        """Complete portfolio analysis workflow."""

        analysis_steps = [
            f"Fetch historical data for {', '.join(tickers)} from {start_date} to {end_date}",
            "Calculate returns, volatility, and correlations",
            "Perform risk analysis and Value at Risk calculation",
            "Optimize portfolio weights using Markowitz optimization",
            "Generate performance reports and visualizations",
            "Create executive summary with recommendations"
        ]

        results = {}
        for i, step in enumerate(analysis_steps, 1):
            print(f"💹 Step {i}: {step}")
            result = await self.arun({
                "messages": [{
                    "role": "user",
                    "content": step
                }]
            })
            results[f"step_{i}"] = result

        return results

async def main():
    """Custom discovery examples."""

    print("🧬 Bioinformatics Agent Example")
    print("="*50)

    # Create bioinformatics agent
    bio_agent = BioinformaticsDiscoveryAgent(
        name="bio_researcher",
        engine=AugLLMConfig(temperature=0.2),
        auto_discover=True,
        require_approval=True
    )

    try:
        await bio_agent.setup()

        # Example bioinformatics task
        bio_result = await bio_agent.arun({
            "messages": [{
                "role": "user",
                "content": "Analyze protein sequences for COVID-19 variants and compare their structures"
            }]
        })
        print(f"🧬 Bio result: {bio_result}")

    except Exception as e:
        print(f"Bio agent error: {e}")
    finally:
        await bio_agent.cleanup()

    print("\n💹 Finance Agent Example")
    print("="*50)

    # Create finance agent
    finance_agent = FinanceDiscoveryAgent(
        name="portfolio_manager",
        engine=AugLLMConfig(temperature=0.1),
        auto_discover=True,
        require_approval=True
    )

    try:
        await finance_agent.setup()

        # Example portfolio analysis
        portfolio_result = await finance_agent.portfolio_analysis(
            tickers=["AAPL", "GOOGL", "MSFT", "TSLA"],
            start_date="2023-01-01",
            end_date="2024-01-01"
        )
        print(f"💹 Portfolio analysis completed: {len(portfolio_result)} steps")

    except Exception as e:
        print(f"Finance agent error: {e}")
    finally:
        await finance_agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🎨 Running the Examples

### Setup Requirements

```bash
# Install Haive MCP package
pip install haive-mcp

# Install Node.js for MCP servers
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install common MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-postgres
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-calculator
```

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=your-openai-key
BRAVE_API_KEY=your-brave-search-key
DATABASE_URL=postgresql://user:pass@localhost/db
```

### Running Examples

```bash
# Basic examples
python examples/basic_mcp_agent.py
python examples/intelligent_discovery.py
python examples/tool_sharing.py

# Advanced examples
python examples/multi_agent_workflow.py
python examples/custom_discovery.py
python examples/production_deployment.py
```

## 📋 Example Templates

### Agent Template

```python
# template_agent.py
"""Template for creating MCP-enabled agents."""

import asyncio
import logging
from haive.mcp.agents import IntelligentMCPAgent
from haive.core.engine.aug_llm import AugLLMConfig

class MyCustomAgent(IntelligentMCPAgent):
    """Custom agent with specialized MCP capabilities."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add custom initialization

    async def _analyze_capability_needs(self, user_message: str) -> list[str]:
        """Custom capability analysis logic."""
        base_capabilities = await super()._analyze_capability_needs(user_message)

        # Add your domain-specific logic here
        custom_capabilities = []

        return base_capabilities + custom_capabilities

    async def custom_workflow(self, input_data: dict) -> dict:
        """Implement your custom workflow."""
        # Your workflow logic here
        pass

async def main():
    agent = MyCustomAgent(
        name="my_agent",
        engine=AugLLMConfig(),
        auto_discover=True,
        require_approval=True
    )

    try:
        await agent.setup()
        # Use your agent
        result = await agent.arun({"messages": [{"role": "user", "content": "Hello"}]})
        print(result)
    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

---

**Note**: All examples include proper error handling, logging, and cleanup. Modify the configurations and API keys according to your environment before running.
