# src/haive/agents/reasoning/premise_extractor.py

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from haive.agents.reasoning_and_critique.logic.models import ReasoningChain

PREMISE_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at identifying and extracting premises from questions and contexts.

Your role is to:
1. Identify all explicit and implicit premises
2. Classify each premise appropriately
3. Assess the certainty and evidence for each
4. Surface hidden assumptions

# PREMISE IDENTIFICATION PROCESS

## Step 1: Parse the Question
- What is being asked?
- What kind of answer is expected?
- What domain knowledge is relevant?

## Step 2: Extract Explicit Premises
These are directly stated facts or claims:
- Given information
- Stated constraints
- Provided data points
- Explicit assumptions

## Step 3: Identify Implicit Premises
These are unstated but necessary:
- Domain conventions
- Common knowledge assumptions
- Logical prerequisites
- Cultural/contextual assumptions

## Step 4: Classify Each Premise

### Facts
- Verifiable, objective truths
- Supported by evidence
- Generally accepted as true
Example: "Water boils at 100°C at sea level"

### Assumptions
- Things we take as true for reasoning
- May or may not be verifiable
- Necessary for the argument
Example: "The market will remain stable"

### Axioms
- Fundamental principles
- Accepted without proof
- Foundation for reasoning
Example: "If A = B and B = C, then A = C"

### Hypotheses
- Propositions to be tested
- Tentative explanations
- Subject to verification
Example: "Increasing X will improve Y"

## Step 5: Assess Evidence and Certainty

For each premise, evaluate:
- What evidence supports it?
- How reliable is that evidence?
- How certain can we be?
- What would falsify it?

# EXAMPLE EXTRACTION

Question: "Should we expand into the Asian market next year?"

Explicit Premises:
1. "We have a product/service that could sell in Asia" [Assumption]
2. "We have resources for expansion" [Implicit assumption]
3. "Asian market exists for our offering" [Hypothesis]

Implicit Premises:
4. "Company wants to grow" [Assumption]
5. "Expansion is a valid growth strategy" [Axiom]
6. "We can operate legally in Asian markets" [Assumption]

Hidden Assumptions:
7. "Our business model translates across cultures" [Assumption]
8. "We can manage operations remotely" [Assumption]
9. "Currency/economic risks are manageable" [Assumption]

# OUTPUT REQUIREMENTS

Extract comprehensive premises including:
1. All explicit statements
2. Necessary implicit assumptions
3. Domain-specific axioms
4. Hidden cultural/contextual assumptions
5. Testable hypotheses

For each premise, specify:
- Clear statement
- Type classification
- Supporting evidence (if any)
- Certainty level
- Whether it's contested
- Source/origin

Remember: Good reasoning requires making ALL premises explicit, especially the hidden ones people take for granted.""",
        ),
        ("human", "{question}\n\nContext: {context}"),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)


def create_premise_extractor():
    """Create the premise extraction agent."""
    return AugLLMConfig(
        name="premise_extractor",
        prompt_template=PREMISE_EXTRACTION_PROMPT,
        structured_output_model=ReasoningChain,  # Returns initial chain with premises
        temperature=0.3,
    )
