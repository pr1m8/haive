#!/usr/bin/env python3
"""
Agent Showcase Documentation Builder for Haive Framework

This script generates comprehensive, beautifully formatted documentation
for all discovered agents, creating an interactive showcase with examples,
usage patterns, and categorized organization.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentShowcaseBuilder:
    """Generates comprehensive documentation for the agent showcase."""
    
    def __init__(self, workspace_root: Path):
        """Initialize the documentation generator."""
        self.workspace_root = workspace_root
        self.docs_dir = workspace_root / "docs" / "source"
        self.agents_dir = self.docs_dir / "agents"
        
    def load_showcase_data(self) -> Dict[str, Any]:
        """Load the agent showcase data."""
        data_file = self.workspace_root / "docs" / "agent_showcase_data.json"
        if not data_file.exists():
            raise FileNotFoundError(f"Agent showcase data not found at {data_file}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_main_showcase(self, data: Dict[str, Any]) -> str:
        """Generate the main agent showcase page."""
        metadata = data['metadata']
        stats = data['stats']
        categories = data['categories']
        
        content = f'''# 🤖 Haive Agent Showcase

Welcome to the comprehensive showcase of Haive's intelligent agent ecosystem! This showcase presents **{metadata['total_agents']} agents** across **{metadata['total_categories']} categories**, demonstrating the full breadth and power of the Haive framework.

::{{admonition}} 🎯 Quick Navigation
:class: tip

- **[Foundation Agents](#foundation-agents)** - Start here if you're new to Haive
- **[Popular Categories](#popular-categories)** - Most commonly used agent types  
- **[Game Agents](#games)** - Interactive entertainment and strategy agents
- **[Business Solutions](#prebuilt-solutions)** - Production-ready specialized agents
- **[Advanced Reasoning](#reasoning-critique)** - Cutting-edge AI capabilities
::

## 📊 Agent Ecosystem Overview

### 📈 Quick Stats

| Metric | Value |
|--------|-------|
| **Total Agents** | {metadata['total_agents']} |
| **Categories** | {metadata['total_categories']} |
| **Packages** | {len(metadata['packages'])} |
| **Complex Agents** | {len([a for a in data['agents'] if a['complexity'] == 'complex'])} |

### 🏷️ Top Agent Categories

'''
        
        # Add category overview
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True)
        
        content += "| Category | Agents | Primary Package |\n"
        content += "|----------|--------|----------------|\n"
        
        for category, cat_data in sorted_categories[:10]:  # Top 10 categories
            primary_package = max(cat_data['packages'], key=lambda x: x.count(x)) if cat_data['packages'] else 'unknown'
            content += f"| **{category}** | {cat_data['count']} | `{primary_package}` |\n"
        
        if len(sorted_categories) > 10:
            content += f"| *...and {len(sorted_categories) - 10} more categories* | | |\n"
        
        # Add featured agents section
        content += "\n## ⭐ Featured Agents\n\n"
        content += self._generate_featured_agents_section(data)
        
        # Add getting started section
        content += self._generate_getting_started_section()
        
        return content
    
    def _generate_featured_agents_section(self, data: Dict[str, Any]) -> str:
        """Generate the featured agents section."""
        agents = data['agents']
        
        # Select featured agents based on criteria
        featured = []
        
        # Foundation agents
        foundation_agents = [a for a in agents if a['category'] == 'Foundation Agents']
        if foundation_agents:
            featured.extend(foundation_agents[:2])
        
        # Popular complex agents
        complex_agents = [a for a in agents if a['complexity'] == 'complex' and len(a['features']) >= 2]
        featured.extend(complex_agents[:3])
        
        # Game agents
        game_agents = [a for a in agents if 'Games' in a['category']]
        featured.extend(game_agents[:2])
        
        # Business agents
        business_agents = [a for a in agents if a['package'] == 'haive-prebuilt']
        featured.extend(business_agents[:2])
        
        # Remove duplicates and limit
        seen = set()
        unique_featured = []
        for agent in featured:
            if agent['name'] not in seen:
                unique_featured.append(agent)
                seen.add(agent['name'])
        
        featured = unique_featured[:6]  # Limit to 6 featured agents
        
        content = ""
        
        for agent in featured:
            complexity_badge = self._get_complexity_badge(agent['complexity'])
            features_str = ', '.join(agent['features'][:3]) if agent['features'] else 'Basic functionality'
            if len(agent['features']) > 3:
                features_str += f" +{len(agent['features']) - 3} more"
            
            content += f"""
### {agent['name']} ({complexity_badge})

**Category:** {agent['category']}  
**Package:** `{agent['package']}`  
**Features:** {features_str}

{agent['description']}

```python
from {agent['module_path']} import {agent['name']}

# Create the agent
agent = {agent['name']}(
    name="{agent['name'].lower()}"
)

# Use the agent  
result = agent.invoke({{"query": "Your task here"}})
```

---

"""
        
        return content
    
    def _get_complexity_badge(self, complexity: str) -> str:
        """Get a badge for complexity level."""
        badges = {
            'simple': '🟢 Simple',
            'medium': '🟡 Medium', 
            'complex': '🔴 Complex'
        }
        return badges.get(complexity, '❓ Unknown')
    
    def _generate_getting_started_section(self) -> str:
        """Generate the getting started section."""
        return '''
## 🚀 Getting Started

### Quick Start Guide

1. **Choose Your Agent Type**
   - 🌟 **New to Haive?** Start with Foundation Agents (SimpleAgent, ReactAgent)
   - 🎯 **Building Apps?** Check out Prebuilt Solutions  
   - 🎮 **Want Fun?** Explore Game Agents
   - 🧠 **Advanced Use?** Try Reasoning & Critique agents

2. **Install & Import**
   ```bash
   pip install haive[agents]    # Core agents
   pip install haive[games]     # Game agents  
   pip install haive[prebuilt]  # Business solutions
   ```

3. **Basic Usage Pattern**
   ```python
   from haive.agents.simple import SimpleAgent
   
   # Create agent
   agent = SimpleAgent(
       name="my_agent",
       model="gpt-4"
   )
   
   # Use agent
   result = agent.invoke({"query": "Your task here"})
   ```

### 🎯 Quick Navigation by Use Case

| Use Case | Recommended Agents | Complexity |
|----------|-------------------|------------|
| **Text Processing** | SimpleAgent, DocumentLoaderAgent | 🟢 Easy |
| **Question Answering** | SimpleRAGAgent, MultiStrategyRAGAgent | 🟡 Medium |
| **Code Generation** | ReactAgent, PlanAndExecuteAgent | 🟡 Medium |
| **Multi-Step Reasoning** | ReflectionAgent, LATSAgent | 🔴 Advanced |
| **Team Collaboration** | MultiAgent, DebateConversation | 🔴 Advanced |
| **Gaming & Strategy** | ChessAgent, PokerAgent | 🟡 Medium |
| **Business Automation** | ProjectManagerAgent, ContractAnalysisAgent | 🟡 Medium |

### 💡 Pro Tips

- **Start Simple:** Begin with basic agents and add complexity as needed
- **Tool Integration:** Most agents support external tools and APIs
- **Memory & State:** Advanced agents include persistence for long conversations
- **Customization:** Every agent can be extended and customized

---

**Ready to explore?** Browse the complete catalog below or check the [complete agent index](complete_index.md)!

## 📚 Complete Agent Catalog

'''
    
    def generate_complete_catalog(self, data: Dict[str, Any]) -> str:
        """Generate the complete agent catalog organized by category."""
        categories = data['categories']
        agents = data['agents']
        
        content = ""
        
        # Sort categories by count
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True)
        
        for category, cat_data in sorted_categories:
            content += f"### {category}\n\n"
            content += f"**{cat_data['count']} agents** | "
            content += f"**Packages:** {', '.join(cat_data['packages'])}\n\n"
            
            # Get agents in this category
            category_agents = [a for a in agents if a['category'] == category]
            category_agents.sort(key=lambda x: (x['complexity'], x['name']))
            
            # Show agents in a table
            content += "| Agent | Complexity | Features | Description |\n"
            content += "|-------|------------|----------|-------------|\n"
            
            for agent in category_agents:
                complexity_badge = self._get_complexity_badge(agent['complexity'])
                features_str = ', '.join(agent['features'][:2]) if agent['features'] else 'Basic'
                if len(agent['features']) > 2:
                    features_str += f" +{len(agent['features']) - 2}"
                
                description = agent['description'][:80] + '...' if len(agent['description']) > 80 else agent['description']
                
                content += f"| **{agent['name']}** | {complexity_badge} | {features_str} | {description} |\n"
            
            content += "\n"
        
        return content
    
    def generate_complete_index(self, data: Dict[str, Any]) -> str:
        """Generate a complete alphabetical index of all agents."""
        agents = sorted(data['agents'], key=lambda x: x['name'])
        
        content = """# 📚 Complete Agent Index

Alphabetical listing of all agents in the Haive ecosystem.

"""
        
        # Group by first letter
        by_letter = {}
        for agent in agents:
            letter = agent['name'][0].upper()
            if letter not in by_letter:
                by_letter[letter] = []
            by_letter[letter].append(agent)
        
        # Generate index by letter
        for letter in sorted(by_letter.keys()):
            content += f"## {letter}\n\n"
            
            for agent in by_letter[letter]:
                complexity_badge = self._get_complexity_badge(agent['complexity'])
                features_str = ', '.join(agent['features'][:3]) if agent['features'] else 'Basic'
                if len(agent['features']) > 3:
                    features_str += f", +{len(agent['features']) - 3} more"
                
                content += f"""
**{agent['name']}** ({complexity_badge})  
*{agent['category']} | {agent['package']}*  
{agent['description'][:150]}{'...' if len(agent['description']) > 150 else ''}  
**Features:** {features_str}  
**Module:** `{agent['module_path']}`

"""
        
        return content
    
    def generate_all_documentation(self) -> None:
        """Generate all agent documentation."""
        logger.info("Loading showcase data...")
        data = self.load_showcase_data()
        
        # Create agents directory
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Generating main showcase page...")
        main_content = self.generate_main_showcase(data)
        
        # Add complete catalog to main page
        catalog_content = self.generate_complete_catalog(data)
        main_content += catalog_content
        
        with open(self.agents_dir / "showcase.md", 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        logger.info("Generating complete index...")
        index_content = self.generate_complete_index(data)
        with open(self.agents_dir / "complete_index.md", 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        logger.info(f"✅ Generated showcase documentation for {data['metadata']['total_agents']} agents!")
        logger.info(f"📄 Files created:")
        logger.info(f"  - {self.agents_dir / 'showcase.md'}")
        logger.info(f"  - {self.agents_dir / 'complete_index.md'}")

def main():
    """Main function to generate agent documentation."""
    # Find workspace root
    current_dir = Path(__file__).resolve().parent
    workspace_root = current_dir.parent
    
    logger.info(f"Workspace root: {workspace_root}")
    
    # Initialize generator
    builder = AgentShowcaseBuilder(workspace_root)
    
    # Generate all documentation
    builder.generate_all_documentation()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()