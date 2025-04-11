from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from src.haive.agents.contract_analysis.models import ContractInfo, StepAnalysis
from src.haive.core.aug_llm.base import AugLLMConfig



CONTRACT_CLASSIFIER_SYSTEM_PROMPT = """Analyze the provided contract and determine:
    1. The type of contract (e.g., Employment, NDA, License Agreement)
    2. The industry it belongs to (if clear from the context)."""

messages = [
    SystemMessage(content=CONTRACT_CLASSIFIER_SYSTEM_PROMPT),
    HumanMessage(content="Contract text:\n{contract_text}")
]

contract_classifier_aug_llm = AugLLMConfig(
    #model="gpt-4o-mini",
    promptTemplate=ChatPromptTemplate.from_messages(messages),
    structured_output=ContractInfo
)

CONTRACT_REVIEW_SYSTEM_PROMPT = """You are a {role}.
    Review the contract from your professional perspective.

    Guidelines for your review:
    1. Identify specific sections that fall under your expertise
    2. Analyze those sections in detail
    3. Suggest concrete modifications where necessary

    Your response should include:
    1. analysis: A detailed explanation of your review findings
    2. modifications: A list of suggested changes, each containing:
       - original_text: The exact text to be modified
       - suggested_text: Your proposed replacement
       - reason: Clear reasoning for the change based on your role

    You may suggest multiple modifications or none if appropriate."""

contract_review_messages = [
    SystemMessage(content=CONTRACT_REVIEW_SYSTEM_PROMPT),
    HumanMessage(content="{contract_text}")
]

contract_review_aug_llm = AugLLMConfig(
    promptTemplate=ChatPromptTemplate.from_messages(contract_review_messages),
    structured_output=StepAnalysis
)


MODIFICATIONS_SYSTEM_PROMPT = """You are a {role}.
    Review the contract from your professional perspective.

    Guidelines for your review:
    1. Identify specific sections that fall under your expertise
    2. Analyze those sections in detail
    3. Suggest concrete modifications where necessary"""

modifications_messages = [
    SystemMessage(content=MODIFICATIONS_SYSTEM_PROMPT),
    HumanMessage(content="Please summarize the modifications to the contract.")
]

modifications_aug_llm = AugLLMConfig(
    promptTemplate=ChatPromptTemplate.from_messages(modifications_messages),
)