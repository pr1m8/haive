# Example usage of the Multi-Agent Debate Framework

from src.haive.games.debate.agent import DebateAgent, DebateConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
    
def run_debate(topic: str, description: str = "", max_rounds: int = 2, num_debaters: int = 2, num_judges: int = 3):
    """
    Run a multi-agent debate on the specified topic.
    
    Args:
        topic: Topic of the debate
        description: Optional description of the debate context
        max_rounds: Number of argument rounds
        num_debaters: Number of debaters
        num_judges: Number of judges
    """
    print(f"Setting up debate on: {topic}")
    print(f"Rounds: {max_rounds}")
    print(f"Participants: {num_debaters} debaters, {num_judges} judges")
    print("-" * 60)
    
    # Create configuration
    config = DebateConfig(
        topic=topic,
        description=description,
        max_rounds=max_rounds,
        num_debaters=num_debaters,
        num_judges=num_judges,
        participant_generator_llm=AugLLMConfig(
            name="participant_generator_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.9})
        ),
        debater_llm=AugLLMConfig(
            name="debater_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7})
        ),
        judge_llm=AugLLMConfig(
            name="judge_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.4})
        ),
        #state_schema=DebateState
    )
    
    # Create agent
    agent = DebateAgent(config)
    
    # Run the debate
    print("Starting debate...")
    result = agent.run(input_data={"topic": topic, "description": description, "max_rounds": max_rounds, "num_debaters": num_debaters, "num_judges": num_judges})
    
    # Print the final transcript
    if "messages" in result:
        print("\nDebate completed!")
        for msg in result["messages"]:
            if hasattr(msg, 'content'):
                print(f"\n{msg.content}")
    
    # Return result for potential further processing
    return result


# Example extensions of the framework for specific debate types
def run_trial_debate(case_title: str, case_facts: str, charges: str):
    """
    Run a trial debate using the debate framework.
    
    Args:
        case_title: Title of the case
        case_facts: Facts of the case
        charges: Charges against the defendant
    """
    # Create a trial-specific description
    description = f"""
This is a courtroom trial simulation for the case of {case_title}.

CHARGES:
{charges}

CASE FACTS:
{case_facts}

The prosecution will argue that the defendant is guilty.
The defense will argue that the defendant is not guilty.
"""

    # Run with trial-specific settings
    return run_debate(
        topic=f"Trial: {case_title}",
        description=description,
        max_rounds=2,  # Shorter for demo purposes
        num_debaters=2,  # Prosecutor and defendant
        num_judges=5     # Jury members
    )


def run_policy_debate(policy: str, context: str = ""):
    """
    Run a policy debate using the debate framework.
    
    Args:
        policy: The policy to debate
        context: Context about the policy
    """
    description = f"""
This is a policy debate on the following proposal:

POLICY:
{policy}

CONTEXT:
{context}

One side will argue in favor of this policy.
The other side will argue against this policy.
"""

    return run_debate(
        topic=f"Policy Debate: {policy}",
        description=description,
        max_rounds=3,
        num_debaters=2,
        num_judges=3
    )


# Example usage
if __name__ == "__main__":
    # Run a basic debate
    #result = run_debate("Should artificial intelligence be regulated by governments?")
    
    # Run a trial debate
    result = run_trial_debate(
        case_title="State v. Johnson",
        case_facts="The defendant is accused of embezzling $75,000 from their employer, QuickBooks Accounting, where they worked as a financial controller. The prosecution alleges that over 18 months, the defendant created fake vendor accounts and issued payments to themselves.",
        charges="Grand Theft, Embezzlement, Falsifying Business Records"
    )
    
    # Run a policy debate
    #result = run_policy_debate(
    #    policy="Universal Basic Income of $1,000 per month should be implemented nationally",
    #    context="Rising automation threatens traditional employment while wealth inequality continues to grow."
    #)
    
    print(f"\nDebate winner: {result.get('winner', 'No winner determined')}")