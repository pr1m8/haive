# analyze_bitfinex.py

import asyncio
import json
from src.haive.prebuilt.priv.agentconfig import KYCAgentRunnerConfig
from src.haive.prebuilt.priv.kyc_agent import KYCAgentRunner
# Bitfinex information
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
"""

async def analyze_bitfinex():
    """Analyze Bitfinex against risk appetite statement"""
    # Create runner with custom config
    runner = KYCAgentRunner(
        KYCAgentRunnerConfig(
            llm_model="gpt-4o",
            temperature=0.1,
            max_search_queries=8,
            max_reflection_steps=2,
            max_pages_total=30
        )
    )
    
    # Run analysis
    result = await runner.analyze_client(
        client_name="Bitfinex (iFinex Inc.)",
        initial_information=BITFINEX_INFO
    )
    
    # Print results
    runner.print_analysis_summary(result["analysis"])
    
    # Save results
    with open("bitfinex_analysis.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    
    return result

if __name__ == "__main__":
    asyncio.run(analyze_bitfinex())