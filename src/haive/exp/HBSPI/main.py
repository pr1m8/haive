# src/haive/agents/hbspi/main.py

import logging
import json
from typing import Dict, Any
from uuid import uuid4
# Import the HBSPI components
from src.haive.agents.HBSPI.agent import HBSPIAgent, HBSPIAgentConfig
from src.haive.agents.HBSPI.rewoo_reasoner import ReWOOReasoner
from src.haive.agents.HBSPI.parallel_plan_tree import ParallelPlanTree
from src.haive.agents.HBSPI.belief_space import BeliefSpaceManager
from src.haive.agents.HBSPI.introspection import IntrospectionEngine

# Import necessary LLM components
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_hbspi_agent(name: str = "hbspi_agent", model: str = "gpt-4o") -> HBSPIAgent:
    """
    Create a configured HBSPI agent ready for use.
    
    Args:
        name: Name for the agent
        model: Model to use for the agent's engines
        
    Returns:
        HBSPIAgent instance
    """
    logger.info(f"Creating HBSPI agent: {name}")
    
    # Create a default LLM config
    llm_config = AzureLLMConfig(
        model=model,
        parameters={"temperature": 0.7}
    )
    
    # Create the config
    config = HBSPIAgentConfig.create_default(
        name=name,
        llm_config=llm_config
    )
    
    # Build the agent
    agent = config.build_agent()
    logger.info(f"HBSPI agent created successfully: {name}")
    
    return agent

def create_rewoo_reasoner(name: str = "rewoo_reasoner", model: str = "gpt-4o") -> ReWOOReasoner:
    """
    Create a configured ReWOO reasoner.
    
    Args:
        name: Name for the reasoner
        model: Model to use for the reasoner's engines
        
    Returns:
        ReWOOReasoner instance
    """
    logger.info(f"Creating ReWOO reasoner: {name}")
    
    # Create a default LLM config
    llm_config = AzureLLMConfig(
        model=model,
        parameters={"temperature": 0.7}
    )
    
    # Create specialized engines for different components
    
    # Planning engine
    planning_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert hierarchical planner. Break down complex problems into a hierarchy of subproblems."),
        MessagesPlaceholder(variable_name="context"),
        ("human", "{query}")
    ])
    
    planning_engine = AugLLMConfig(
        name='planning_engine',
        llm_config=llm_config,
        prompt_template=planning_prompt
    )
    
    # Evidence engine
    evidence_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in hypothetical reasoning. Generate and validate hypothetical evidence."),
        MessagesPlaceholder(variable_name="context"),
        ("human", "{query}")
    ])
    
    evidence_engine = AugLLMConfig(
        name='evidence_engine',
        llm_config=llm_config,
        prompt_template=evidence_prompt
    )
    
    # Belief engine
    belief_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in probabilistic belief updating and management."),
        MessagesPlaceholder(variable_name="context"),
        ("human", "{query}")
    ])
    
    belief_engine = AugLLMConfig(
        name='belief_engine',
        llm_config=llm_config,
        prompt_template=belief_prompt
    )
    
    # Introspection engine
    introspection_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in meta-cognitive evaluation. Analyze reasoning for flaws and improvements."),
        MessagesPlaceholder(variable_name="context"),
        ("human", "{query}")
    ])
    
    introspection_engine = AugLLMConfig(
        name='introspection_engine',
        llm_config=llm_config,
        prompt_template=introspection_prompt
    )
    
    # Create the reasoner
    reasoner = ReWOOReasoner.create(
        name=name,
        description=f"ReWOO reasoner using {model}",
        planning_engine=planning_engine,
        evidence_engine=evidence_engine,
        belief_engine=belief_engine,
        introspection_engine=introspection_engine
    )
    
    logger.info(f"ReWOO reasoner created successfully: {name}")
    return reasoner

def run_agent_demo(agent: HBSPIAgent, query: str) -> Dict[str, Any]:
    """
    Run a demonstration of the HBSPI agent.
    
    Args:
        agent: The agent to run
        query: The user query
        
    Returns:
        Results dictionary
    """
    logger.info(f"Running HBSPI agent demo with query: {query}")
    
    # Run the agent
    result = agent.run(query)
    
    logger.info("HBSPI agent demo completed successfully")
    return result

def run_reasoner_demo(reasoner: ReWOOReasoner, query: str) -> Dict[str, Any]:
    """
    Run a demonstration of the ReWOO reasoner.
    
    Args:
        reasoner: The reasoner to run
        query: The user query
        
    Returns:
        Results dictionary
    """
    logger.info(f"Running ReWOO reasoner demo with query: {query}")
    
    # Run the reasoner
    result = reasoner.reason_about_query(query)
    
    logger.info("ReWOO reasoner demo completed successfully")
    return result

def save_results(results: Dict[str, Any], filename: str) -> None:
    """
    Save results to a JSON file.
    
    Args:
        results: Results to save
        filename: Filename to save to
    """
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to: {filename}")

def main():
    """Main demonstration function."""
    print("======= HBSPI Demo =======")
    print("Hierarchical Belief-Space Planning with Introspection")
    print()
    
    # Create the agent and reasoner
    agent = create_hbspi_agent()
    reasoner = create_rewoo_reasoner()
    
    # Sample query
    query = "What are the key factors affecting global climate change and how do they interact with each other?"
    
    # Run the agent demo
    print(f"Running HBSPI agent with query: {query}")
    agent_results = run_agent_demo(agent, query)
    save_results(agent_results, "hbspi_agent_results.json")
    
    # Run the reasoner demo
    print(f"\nRunning ReWOO reasoner with query: {query}")
    reasoner_results = run_reasoner_demo(reasoner, query)
    save_results(reasoner_results, "rewoo_reasoner_results.json")
    
    # Print summary
    print("\n======= Results Summary =======")
    print(f"Agent message count: {len(agent_results.get('messages', []))}")
    print(f"Reasoner reasoning steps: {len(reasoner_results.get('reasoning_steps', []))}")
    print(f"Reasoning with {len(reasoner_results.get('plan_tree_statistics', {}).get('nodes_by_type', {}))}")
    print(f"Beliefs tracked: {reasoner_results.get('belief_space_statistics', {}).get('total_beliefs', 0)}")
    print(f"Insights generated: {reasoner_results.get('introspection_statistics', {}).get('total_insights', 0)}")
    print("\nSee output files for complete results.")

if __name__ == "__main__":
    main()