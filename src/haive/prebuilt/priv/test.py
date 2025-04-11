"""
KYC Compliance Analysis Example for Bitfinex/Bitfinity

This example shows how to use the KYC agent framework to analyze a cryptocurrency
exchange against the risk appetite statement.
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional, List

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# Import the KYC agent components (in practice, these would be import statements to your modules)
from src.haive.prebuilt.priv.state import KYCAgentRunner, KYCAgentRunnerConfig


# Specific information about Bitfinex/Bitfinity (to be used as initial context)
BITFINEX_INFO = """
Bitfinex is a cryptocurrency exchange owned and operated by iFinex Inc., founded in 2012 and headquartered in Hong Kong with offices in other locations worldwide. Bitfinex offers trading of cryptocurrencies such as Bitcoin, Ethereum, and various other digital assets.

Key information:
- Full name: Bitfinex (operated by iFinex Inc.)
- Founded: 2012
- Headquarters: Hong Kong, with registered offices in the British Virgin Islands
- Services: Cryptocurrency trading, margin trading, cryptocurrency lending, staking
- Supported cryptocurrencies: Bitcoin, Ethereum, and numerous other cryptocurrencies
- Associated token: Unus Sed Leo (LEO)
- Related entities: Tether Limited (USDT stablecoin issuer)

Regulatory information:
- Bitfinex has faced regulatory scrutiny in various jurisdictions
- In 2021, Bitfinex agreed to pay $18.5 million to settle with the New York Attorney General over allegations related to covering up losses and misrepresenting the backing of Tether
- The company restricts service to certain jurisdictions including the United States
- Has implemented KYC/AML procedures, especially after regulatory challenges

The exchange offers various services including spot trading, margin trading, derivatives, staking, and other cryptocurrency financial services.

Regarding Bitfinity: There is a separate blockchain project called Bitfinity Network, which is a layer-2 EVM compatible blockchain on the Internet Computer, but it appears to be a different entity from Bitfinex.
"""


# Additional research queries specific to Bitfinex/Bitfinity
BITFINEX_QUERIES = [
    "Bitfinex cryptocurrency exchange regulatory compliance history",
    "Bitfinex ownership structure and relationship with Tether",
    "Bitfinex KYC AML procedures and implementation",
    "Bitfinex legal issues investigations penalties",
    "Bitfinex jurisdictions service restrictions",
    "Bitfinex licensing registration status by country",
    "Bitfinity vs Bitfinex difference between companies",
    "Bitfinex gambling services offered or restricted"
]


# Extended analysis function for Bitfinex
async def analyze_bitfinex():
    """
    Run a comprehensive KYC analysis on Bitfinex/Bitfinity
    with enhanced data collection and detailed reporting.
    """
    print("Starting comprehensive KYC analysis for Bitfinex/Bitfinity...")
    
    # Create runner with specialized configuration
    runner = KYCAgentRunner(
        KYCAgentRunnerConfig(
            llm_model="claude-3-5-sonnet-latest",  # Use the most capable model
            temperature=0.1,                      # Low temperature for factual analysis
            max_search_queries=8,                 # More queries for thorough research
            max_search_results=10,                # More results per query
            max_reflection_steps=3,               # More reflection for complex case
            minimum_confidence_threshold=0.8,     # Higher confidence requirement
            max_pages_total=30,                   # Analysis of more pages
            max_depth=3                           # Deeper link following
        )
    )
    
    # Enhance the initial information with specialized queries
    enhanced_initial_info = f"""
{BITFINEX_INFO}

Additional research should focus on:
1. Regulatory compliance status across all operating jurisdictions
2. Relationship with Tether Limited and USDT stablecoin
3. Implementation of KYC/AML procedures
4. History of regulatory actions, fines, or settlements
5. Verification of licensing status in key jurisdictions
6. Corporate structure and beneficial ownership
7. Types of services offered and any potential prohibited activities
8. Whether the exchange facilitates mixing/tumbling or privacy-enhancing transactions
9. Clear distinction between Bitfinex and Bitfinity Network if they are separate entities

Suggested search queries:
{BITFINEX_QUERIES}
"""
    
    # Perform the analysis
    result = await runner.analyze_client(
        client_name="Bitfinex (iFinex Inc.)",
        initial_information=enhanced_initial_info
    )
    
    # Generate a more detailed report with extra analysis
    detailed_report = await generate_detailed_report(result, runner.risk_appetite_statement)
    
    # Save the analysis result to file
    timestamp = asyncio.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports", exist_ok=True)
    
    with open(f"reports/bitfinex_analysis_{timestamp}.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    
    with open(f"reports/bitfinex_detailed_report_{timestamp}.txt", "w") as f:
        f.write(detailed_report)
    
    print(f"Analysis complete. Reports saved to reports/ directory.")
    return result, detailed_report


async def generate_detailed_report(result: Dict[str, Any], risk_appetite_statement: str) -> str:
    """
    Generate a detailed human-readable report with enhanced analysis.
    
    Args:
        result: The analysis result from the KYC agent
        risk_appetite_statement: The risk appetite statement
        
    Returns:
        Detailed report as string
    """
    # Extract the analysis
    analysis = result.get("analysis", {})
    
    # Create an enhanced prompt for detailed report generation
    llm = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are a KYC compliance reporting specialist creating a comprehensive report
        on a cryptocurrency exchange. Your goal is to produce a detailed, well-structured
        report that thoroughly analyzes compliance risks and provides clear recommendations.
        
        The report should include:
        1. Executive Summary
        2. Company Overview
        3. Regulatory Landscape
        4. Detailed Risk Assessment
        5. Compliance Determination
        6. Specific Recommendations
        7. Appendix with Supporting Evidence
        
        Use a professional, objective tone and ensure all conclusions are evidence-based.
        """),
        HumanMessage(content=f"""
        Generate a detailed KYC compliance report for the following cryptocurrency exchange.
        
        RISK APPETITE STATEMENT:
        {risk_appetite_statement}
        
        ANALYSIS RESULTS:
        {json.dumps(analysis, indent=2, default=str)}
        
        Format the report professionally with clear sections and include recommendations
        that align with the risk appetite statement. Make sure to include:
        - Whether we should proceed with this client (ACCEPTABLE/RESTRICTED/PROHIBITED)
        - If RESTRICTED, what specific enhanced due diligence measures are required
        - If PROHIBITED, which specific prohibitions apply
        - Areas of uncertainty that would benefit from additional investigation
        
        Include specific citations from the analysis and risk appetite statement to support
        your recommendations.
        """)
    ])
    
    # Generate the report
    response = await llm.ainvoke(prompt)
    return response.content


# Extended research function for both Bitfinex and Bitfinity
async def analyze_bitfinity_vs_bitfinex():
    """
    Compare and analyze both Bitfinex and Bitfinity to determine if they
    are related entities and the compliance implications.
    """
    print("Starting comparative analysis between Bitfinity and Bitfinex...")
    
    # Create runner
    runner = KYCAgentRunner(KYCAgentRunnerConfig())
    
    # First analyze Bitfinex
    bitfinex_result = await runner.analyze_client(
        client_name="Bitfinex (iFinex Inc.)",
        initial_information=BITFINEX_INFO
    )
    
    # Then analyze Bitfinity
    bitfinity_info = """
    Bitfinity Network is a layer-2 EVM compatible blockchain built on the Internet Computer Protocol (ICP).
    It appears to be a blockchain infrastructure project rather than an exchange.
    Initial research indicates it may be unrelated to Bitfinex exchange despite the similar name.
    Need to confirm ownership structure, relationship (if any) to Bitfinex, and primary business activities.
    """
    
    bitfinity_result = await runner.analyze_client(
        client_name="Bitfinity Network",
        initial_information=bitfinity_info
    )
    
    # Generate comparison report
    llm = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0.2)
    
    # Extract analyses
    bitfinex_analysis = bitfinex_result.get("analysis", {})
    bitfinity_analysis = bitfinity_result.get("analysis", {})
    
    comparison_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are a KYC compliance analyst comparing two potentially related entities
        to determine their relationship and the combined compliance implications.
        """),
        HumanMessage(content=f"""
        Compare the following two entities and determine:
        1. Whether they are related entities or separate companies
        2. If related, the nature of the relationship
        3. The combined compliance implications
        4. Whether treating them as a single entity or separate entities is appropriate
        5. The overall compliance determination considering both entities together
        
        ENTITY 1 (BITFINEX):
        {json.dumps(bitfinex_analysis, indent=2, default=str)}
        
        ENTITY 2 (BITFINITY):
        {json.dumps(bitfinity_analysis, indent=2, default=str)}
        
        RISK APPETITE STATEMENT:
        {runner.risk_appetite_statement}
        
        Provide a detailed comparison report with evidence-based conclusions.
        """)
    ])
    
    # Generate the comparison report
    response = await llm.ainvoke(comparison_prompt)
    comparison_report = response.content
    
    # Save the comparison report
    timestamp = asyncio.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports", exist_ok=True)
    
    with open(f"reports/bitfinex_bitfinity_comparison_{timestamp}.txt", "w") as f:
        f.write(comparison_report)
    
    print(f"Comparison analysis complete. Report saved to reports/ directory.")
    return comparison_report


async def main():
    """Run the Bitfinex/Bitfinity analysis examples"""
    # Choose which analysis to run
    analysis_type = input("Choose analysis type (1: Bitfinex only, 2: Compare Bitfinex vs Bitfinity): ")
    
    if analysis_type == "2":
        # Run comparison analysis
        comparison_report = await analyze_bitfinity_vs_bitfinex()
        print("\nCOMPARISON REPORT SUMMARY:")
        print("-" * 80)
        print(comparison_report[:500] + "...")  # Print first 500 chars of report
    else:
        # Default to Bitfinex analysis
        result, detailed_report = await analyze_bitfinex()
        print("\nDETAILED REPORT SUMMARY:")
        print("-" * 80)
        print(detailed_report[:500] + "...")  # Print first 500 chars of report


if __name__ == "__main__":
    asyncio.run(main())