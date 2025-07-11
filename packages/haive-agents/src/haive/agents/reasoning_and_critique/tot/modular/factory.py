# src/haive/agents/tot/factory.py

from collections.abc import Callable

from agents.tot.modular.agent import ToTAgent
from agents.tot.modular.config import ToTAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate


def create_tot_agent(
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_depth: int = 5,
    threshold: float = 0.9,
    beam_size: int = 3,
    candidates_per_expansion: int = 3,
    name: str | None = None,
    system_prompt: str = "You are an expert problem solver using a step-by-step approach.",
    expand_prompt: str | ChatPromptTemplate | None = None,
    score_prompt: str | ChatPromptTemplate | None = None,
    score_function: Callable | None = None,
    visualize: bool = True,
    **kwargs,
) -> ToTAgent:
    """Create a Tree of Thoughts agent with customizable parameters.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        max_depth: Maximum depth for the search
        threshold: Score threshold for success
        beam_size: Number of candidates to keep after pruning
        candidates_per_expansion: Number of candidates to generate in each expansion
        name: Optional name for the agent
        system_prompt: System prompt for the agent
        expand_prompt: Custom prompt for expansion (string or ChatPromptTemplate)
        score_prompt: Custom prompt for scoring (string or ChatPromptTemplate)
        score_function: Optional function to score candidates instead of using LLM
        visualize: Whether to visualize the ToT graph
        **kwargs: Additional configuration parameters

    Returns:
        Configured ToTAgent instance
    """
    # Convert string prompts to ChatPromptTemplate if needed
    if isinstance(expand_prompt, str):
        expand_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("system", expand_prompt),
                ("user", "Problem: {problem}"),
                ("user", "Previous attempt: {seed}" if "{seed}" in kwargs else ""),
            ]
        )

    if isinstance(score_prompt, str) and not score_function:
        score_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("system", score_prompt),
                ("user", "Problem: {problem}"),
                ("user", "Solution attempt: {candidate}"),
            ]
        )

    # Create default prompts if none provided
    if not expand_prompt:
        expand_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "system",
                    f"Generate {candidates_per_expansion} different approaches to solve this problem. Be creative and diverse in your thinking.",
                ),
                ("user", "Problem: {problem}"),
                ("user", "Previous attempt: {seed}" if "{seed}" in kwargs else ""),
            ]
        )

    # Create the ToTAgentConfig
    config = ToTAgentConfig.from_scratch(
        model=model,
        temperature=temperature,
        system_prompt=system_prompt,
        expand_prompt=expand_prompt,
        score_prompt=score_prompt,
        max_depth=max_depth,
        threshold=threshold,
        beam_size=beam_size,
        candidates_per_expansion=candidates_per_expansion,
        score_function=score_function,
        name=name,
        visualize=visualize,
        **kwargs,
    )

    # Build and return the agent
    return config.build_agent()


def create_math_tot_agent(
    model: str = "gpt-4o", temperature: float = 0.7, name: str | None = None, **kwargs
) -> ToTAgent:
    """Create a Tree of Thoughts agent specifically for math problems.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        name: Optional agent name
        **kwargs: Additional configuration parameters

    Returns:
        ToTAgent configured for math problems
    """
    # Math-specific system prompt
    system_prompt = """
    You are a brilliant mathematician solving complex problems step by step.
    Break the problem into smaller parts and explore different approaches systematically.
    Show your reasoning, calculations, and intermediate steps clearly.
    """

    # Math-specific expand prompt
    expand_prompt = """
    Generate {k} different approaches to solve this mathematical problem.
    For each approach:
    1. Identify the key mathematical concepts needed
    2. Break down the problem into logical steps
    3. Show your calculations and reasoning
    4. Verify your solution if possible
    """

    # Function to score math solutions
    def score_math_solution(problem: str, solution: str) -> tuple:
        import re

        # Calculate length-normalized score based on:
        # 1. Presence of equations/numbers/calculations
        # 2. Presence of a clear final answer
        # 3. Logical structure
        # Check for equations and numerical content
        equations = len(re.findall(r"[-+*/=]", solution))
        numbers = len(re.findall(r"\b\d+(?:\.\d+)?\b", solution))

        # Check for a clear final answer
        has_answer = bool(
            re.search(r"answer|result|solution|=\s*\d+(?:\.\d+)?$", solution.lower())
        )

        # Calculate a base score
        base_score = min(1.0, (equations + numbers) / 20)  # Normalize math content
        if has_answer:
            base_score += 0.3  # Bonus for clear answer

        # Cap at 1.0
        score = min(1.0, base_score)

        # Generate feedback
        if score > 0.9:
            feedback = "Excellent solution with clear steps and final answer."
        elif score > 0.7:
            feedback = "Good approach with some mathematical work, could be clearer."
        elif score > 0.5:
            feedback = "Partial solution with some mathematical reasoning."
        else:
            feedback = "Limited mathematical content or unclear approach."

        return score, feedback

    return create_tot_agent(
        model=model,
        temperature=temperature,
        name=name or "math_tot_agent",
        system_prompt=system_prompt,
        expand_prompt=expand_prompt,
        score_function=score_math_solution,
        max_depth=3,  # Math problems often need fewer iterations
        threshold=0.85,
        beam_size=2,  # Keep fewer candidates for math problems
        candidates_per_expansion=3,
        **kwargs,
    )


def create_game24_tot_agent(
    model: str = "gpt-4o", temperature: float = 0.7, name: str | None = None, **kwargs
) -> ToTAgent:
    """Create a Tree of Thoughts agent specifically for "Game of 24" problems.

    Args:
        model: Model name to use
        temperature: Temperature for generation
        name: Optional agent name
        **kwargs: Additional configuration parameters

    Returns:
        ToTAgent configured for the Game of 24
    """
    # Game of 24 specific system prompt
    system_prompt = """
    You are solving the "Game of 24" puzzle. Given four numbers, you need to find a way to combine them using basic operations (addition, subtraction, multiplication, division) to reach exactly 24.

    Each number must be used exactly once, and you can use parentheses to control the order of operations.
    """

    # Define structured output models for Game of 24
    from pydantic import BaseModel, Field, field_validator

    class Equation(BaseModel):
        """An equation attempting to reach 24 using the provided numbers."""

        formula: str = Field(
            description="Mathematical formula using all four numbers and basic operations"
        )
        reasoning: str = Field(
            description="Step-by-step reasoning for how this formula works"
        )

        @field_validator("formula")
        def validate_formula(self, v):
            """Validate the formula has basic math operators."""
            if not any(op in v for op in ["+", "-", "*", "/"]):
                raise ValueError(
                    "Formula must contain at least one mathematical operator"
                )
            return v

    class EquationList(BaseModel):
        """Multiple possible equations for the Game of 24."""

        equations: list[Equation] = Field(description="List of candidate equations")

    # Create expand prompt with structured output
    expand_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "system",
                """Generate {k} different equations that might solve the Game of 24 for the given numbers.
                     For each attempt, show your formula and step-by-step reasoning.""",
            ),
            ("user", "Numbers: {problem}"),
            ("user", "Previous attempt: {seed}" if "{seed}" in kwargs else ""),
        ]
    )

    # Create score prompt with structured output
    score_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Evaluate how close this equation comes to the target value of 24.
                     Score from 0.0 to 1.0, where 1.0 means it equals exactly 24.""",
            ),
            ("user", "Numbers: {problem}"),
            ("user", "Equation: {candidate}"),
        ]
    )

    # Define a function to score Game of 24 solutions
    def score_equation(problem: str, solution: str) -> tuple:
        import re

        # Extract the numbers from the problem
        input_numbers = [int(n) for n in problem.split() if n.isdigit()]
        if not input_numbers:
            return 0.0, "Could not parse input numbers"

        # Extract a formula from the solution
        formula_match = re.search(r"([0-9()+\-*/.\s]+=[0-9.]+)", solution)
        if not formula_match:
            # Look for mathematical expression
            formula_match = re.search(r"([0-9()+\-*/.\s]+)", solution)
            if not formula_match:
                return 0.1, "Could not find a clear formula"

        formula = formula_match.group(1).strip()

        # Check if all input numbers are used
        for num in input_numbers:
            if str(num) not in re.sub(r"[^0-9]", " ", formula).split():
                return 0.2, f"Not all input numbers are used. Missing {num}"

        # Try to evaluate the formula
        try:
            # Extract the expression part if there's an equals sign
            if "=" in formula:
                formula = formula.split("=")[0].strip()

            # Import specific math functions instead of using wildcard import
            import math

            # Create a safe evaluation environment with math functions
            safe_dict = {
                "abs": abs,
                "pow": pow,
                "round": round,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan,
                "sqrt": math.sqrt,
                "exp": math.exp,
                "log": math.log,
                "log10": math.log10,
                "floor": math.floor,
                "ceil": math.ceil,
                "pi": math.pi,
                "e": math.e,
            }
            # Add all numeric operators
            safe_dict.update({str(i): i for i in range(10)})

            # Use the safer eval with explicit globals
            result = eval(formula, {"__builtins__": {}}, safe_dict)

            # Score based on how close it is to 24
            proximity = 1.0 / (1.0 + abs(24 - result))

            # Perfect score if exactly 24
            if abs(result - 24) < 0.0001:
                return 1.0, "Perfect! The expression equals exactly 24"
            return (
                proximity,
                f"Expression evaluates to {result}, which is {abs(24 - result)} away from 24",
            )
        except Exception as e:
            return 0.05, f"Error evaluating the formula: {e!s}"

    # Ensure expand LLM has structured output
    expand_llm_config = AugLLMConfig(
        name="game24_expand",
        llm_config=AzureLLMConfig(model=model, parameters={"temperature": temperature}),
        prompt_template=expand_prompt,
        structured_output_model=EquationList,
    )

    # Create score LLM with structured output
    from pydantic import BaseModel, Field

    class ScoreResult(BaseModel):
        """Score for a Game of 24 solution."""

        score: float = Field(
            description="Score between 0.0 and 1.0, with 1.0 being exactly 24"
        )
        feedback: str = Field(description="Explanation of the score and correctness")

    score_llm_config = AugLLMConfig(
        name="game24_score",
        llm_config=AzureLLMConfig(model=model, parameters={"temperature": 0.2}),
        prompt_template=score_prompt,
        structured_output_model=ScoreResult,
    )

    return create_tot_agent(
        model=model,
        temperature=temperature,
        name=name or "game24_tot_agent",
        system_prompt=system_prompt,
        expand_llm_config=expand_llm_config,
        score_llm_config=score_llm_config,
        score_function=score_equation,  # Use function-based scoring as backup
        max_depth=3,
        threshold=0.99,  # High threshold for Game of 24 (need exact answer)
        beam_size=3,
        candidates_per_expansion=4,
        **kwargs,
    )
