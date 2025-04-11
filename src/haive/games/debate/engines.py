# src/haive/games/debate/engines.py
from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.games.debate.models import Statement
from typing import Dict

# ------------------------------
# Moderator Prompts
# ------------------------------
def generate_moderator_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a moderator for a structured debate or discussion. Your role is to guide the conversation, "
            "enforce rules, ask clarifying questions, and ensure all participants have equal opportunity to speak. "
            "You should remain neutral and objective throughout the debate."
        ),
        ('human', 
            "Debate Topic: {topic}\n\n"
            "Current Phase: {debate_phase}\n\n"
            "Participants:\n{participants}\n\n"
            "Recent Statements:\n{recent_statements}\n\n"
            "Current Speaker: {current_speaker}\n\n"
            "As the moderator, please {action_prompt}."
        )
    ])

# ------------------------------
# Debater Prompts
# ------------------------------
def generate_debater_prompt(position: str = None) -> ChatPromptTemplate:
    position_guidance = ""
    if position == "pro":
        position_guidance = "You are arguing IN FAVOR of the topic. Present strong arguments supporting this position."
    elif position == "con":
        position_guidance = "You are arguing AGAINST the topic. Present strong arguments opposing this position."
    
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a skilled debater participating in a structured debate. {position_guidance} "
            "Use logical arguments, evidence, and persuasive rhetoric. Address counterarguments thoughtfully "
            "and maintain respectful tone even when disagreeing strongly."
        ),
        ('human', 
            "Debate Topic: {topic}\n\n"
            "Current Phase: {debate_phase}\n\n"
            "Your Position: {position}\n\n"
            "Recent Statements:\n{recent_statements}\n\n"
            "Your Previous Arguments:\n{your_statements}\n\n"
            "It's your turn to speak. Please provide a compelling {statement_type} for this phase of the debate."
        )
    ])

# ------------------------------
# Judge/Juror Prompts
# ------------------------------
def generate_judge_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are serving as a judge in this debate or proceeding. Your role is to evaluate arguments "
            "impartially, make rulings when necessary, and ultimately determine an outcome based on the "
            "strength of arguments and evidence presented. Maintain neutrality and focus on clarity and fairness."
        ),
        ('human', 
            "Topic/Case: {topic}\n\n"
            "Current Phase: {debate_phase}\n\n"
            "Participant Statements:\n{all_statements}\n\n"
            "Key Arguments:\n{key_arguments}\n\n"
            "Based on the proceedings so far, please {action_prompt}."
        )
    ])

# ------------------------------
# Trial-Specific Prompts
# ------------------------------
def generate_prosecutor_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are serving as a prosecutor in this legal proceeding. Your role is to present a compelling case "
            "against the defendant by organizing evidence, questioning witnesses effectively, and constructing "
            "a persuasive narrative. Focus on clarity, logical progression, and highlighting key facts."
        ),
        ('human', 
            "Case Details: {topic}\n\n"
            "Current Phase: {debate_phase}\n\n"
            "Evidence Available: {evidence}\n\n"
            "Witness Statements: {witness_statements}\n\n"
            "Recent Court Proceedings:\n{recent_statements}\n\n"
            "Please provide your {statement_type} for this phase of the trial."
        )
    ])

def generate_defense_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are serving as a defense attorney in this legal proceeding. Your role is to protect your client's "
            "interests by challenging the prosecution's case, presenting alternative explanations, highlighting "
            "weaknesses in evidence, and constructing reasonable doubt. Be thorough, logical, and persuasive."
        ),
        ('human', 
            "Case Details: {topic}\n\n"
            "Current Phase: {debate_phase}\n\n"
            "Client Information: {client_info}\n\n"
            "Evidence Available: {evidence}\n\n"
            "Prosecution Claims: {prosecution_claims}\n\n"
            "Recent Court Proceedings:\n{recent_statements}\n\n"
            "Please provide your {statement_type} for this phase of the trial."
        )
    ])

# ------------------------------
# Persona-Specific Prompts
# ------------------------------
def generate_persona_prompt(persona_traits: Dict[str, str]) -> ChatPromptTemplate:
    traits_description = ", ".join([f"{k}: {v}" for k, v in persona_traits.items()])
    
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"Embody a debate participant with the following characteristics: {traits_description}. "
            "Your responses should consistently reflect these traits through your communication style, "
            "priorities, and perspectives. However, remain focused on making cogent arguments relevant to the topic."
        ),
        ('human', 
            "Debate Topic: {topic}\n\n"
            "Current Phase: {debate_phase}\n\n"
            "Your Position: {position}\n\n"
            "Recent Statements:\n{recent_statements}\n\n"
            "It's your turn to speak. Please provide a {statement_type} that reflects your persona's perspective."
        )
    ])

# ------------------------------
# AugLLM Configurations
# ------------------------------
def build_debate_engines() -> Dict[str, Dict[str, AugLLMConfig]]:
    """Build engines for different debate roles."""
    return {
        "moderator": {
            "moderate": AugLLMConfig(
                name="moderator_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_moderator_prompt(),
                structured_output_model=Statement
            )
        },
        "debater": {
            "statement": AugLLMConfig(
                name="debater_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_debater_prompt(),
                structured_output_model=Statement
            ),
            "pro": AugLLMConfig(
                name="pro_debater_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_debater_prompt("pro"),
                structured_output_model=Statement
            ),
            "con": AugLLMConfig(
                name="con_debater_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_debater_prompt("con"),
                structured_output_model=Statement
            )
        },
        "judge": {
            "judgment": AugLLMConfig(
                name="judge_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_judge_prompt(),
                structured_output_model=Statement
            )
        },
        "prosecutor": {
            "statement": AugLLMConfig(
                name="prosecutor_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_prosecutor_prompt(),
                structured_output_model=Statement
            )
        },
        "defense": {
            "statement": AugLLMConfig(
                name="defense_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_defense_prompt(),
                structured_output_model=Statement
            )
        }
    }