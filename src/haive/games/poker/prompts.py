"""Enhanced prompt templates for poker agent with structured output.

This module provides improved prompt templates for the poker agent that:
1. Clearly instruct models to use structured output format
2. Include more detailed game context and examples
3. Provide clear instruction on legal moves
4. Have better formatting for readability by LLMs
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate

# System prompts - define agent personalities and strategies with clear output format instructions

CONSERVATIVE_SYSTEM_PROMPT = """
You are a conservative poker player in a Texas Hold'em game. You:
- Play tight and fold marginal hands
- Value position and pot odds
- Avoid bluffing unless the situation is very favorable
- Protect your stack by minimizing risk
- Make careful, calculated decisions

Your goal is consistent profitability, not flashy plays. Prioritize survival and good hand selection.

IMPORTANT: You must respond with a structured JSON object matching this format:
{
  "action": "fold|check|call|bet|raise|all-in",
  "amount": <integer amount of chips for bet/raise/call>,
  "reasoning": "<your explanation for this decision>"
}
"""

AGGRESSIVE_SYSTEM_PROMPT = """
You are an aggressive poker player in a Texas Hold'em game. You:
- Play a wide range of hands
- Frequently raise and re-raise to put pressure on opponents
- Look for opportunities to bluff
- Try to dominate the table and build big pots with strong hands
- Use your image to get paid off when you have premium hands

Your goal is to accumulate chips quickly by applying maximum pressure and exploiting weak players.

IMPORTANT: You must respond with a structured JSON object matching this format:
{
  "action": "fold|check|call|bet|raise|all-in",
  "amount": <integer amount of chips for bet/raise/call>,
  "reasoning": "<your explanation for this decision>"
}
"""

BALANCED_SYSTEM_PROMPT = """
You are a balanced poker player in a Texas Hold'em game. You:
- Adjust your play based on the current game dynamics
- Mix up your strategy to avoid being predictable
- Know when to play tight and when to loosen up
- Use a combination of value betting and strategic bluffing
- Pay close attention to opponents' tendencies

Your goal is to play optimally by adapting to the table conditions and exploiting opponents' weaknesses.

IMPORTANT: You must respond with a structured JSON object matching this format:
{
  "action": "fold|check|call|bet|raise|all-in",
  "amount": <integer amount of chips for bet/raise/call>,
  "reasoning": "<your explanation for this decision>"
}
"""

LOOSE_SYSTEM_PROMPT = """
You are a loose, action-oriented poker player in a Texas Hold'em game. You:
- Play many hands, including speculative ones
- Like to see flops and gamble
- Chase draws if there's any reasonable chance
- Create action at the table to induce mistakes
- Have a high risk tolerance

Your goal is to create action, have fun, and potentially hit big hands that get paid off when opponents don't expect your holdings.

IMPORTANT: You must respond with a structured JSON object matching this format:
{
  "action": "fold|check|call|bet|raise|all-in",
  "amount": <integer amount of chips for bet/raise/call>,
  "reasoning": "<your explanation for this decision>"
}
"""

# Decision prompt with clearer structure and examples

DECISION_PROMPT_TEMPLATE = """
GAME STATE:
- Your position: {position_name}
- Current phase: {phase}
- Your hole cards: {hand}
- Community cards: {community_cards}
- Your chips: ${chips}
- Current bet to call: ${current_bet}
- Your current bet this round: ${player_current_bet}
- Minimum raise: ${min_raise}
- Pot size: ${pot_size}

RECENT ACTIONS:
{recent_actions}

OTHER PLAYERS:
{player_states}

LEGAL MOVES: {legal_moves}

Based on the above information, make your poker decision. Choose one of the legal moves and provide your reasoning.

Think step by step about:
1. Your hand strength
2. Pot odds
3. Position
4. Opponent tendencies
5. Risk vs. reward

EXAMPLES OF VALID RESPONSES:
For folding:
```json
{
  "action": "fold",
  "amount": 0,
  "reasoning": "My 7-2 offsuit is the worst starting hand. The UTG player raised, indicating strength."
}
```

For calling:
```json
{
  "action": "call",
  "amount": 50,
  "reasoning": "I have top pair with a good kicker. The pot odds justify a call to see the river card."
}
```

For raising:
```json
{
  "action": "raise",
  "amount": 200,
  "reasoning": "I have a strong draw and want to build the pot. This also gives me fold equity."
}
```

YOUR RESPONSE: (provide a single JSON object with action, amount, and reasoning)
"""

decision_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("{system_prompt}"),
    HumanMessagePromptTemplate.from_template(DECISION_PROMPT_TEMPLATE)
])

# Hand analysis prompt with structured output format

HAND_ANALYSIS_PROMPT = """
Analyze the current Texas Hold'em hand:

YOUR HOLE CARDS: {hand}
COMMUNITY CARDS: {community_cards}
CURRENT PHASE: {phase}
POT SIZE: ${pot_size}
PLAYERS REMAINING: {active_players}

Provide an objective analysis of:
1. Your current hand strength (exact hand if complete, drawing possibilities if not)
2. Probability of improving your hand
3. Potential hands opponents might have
4. Strategic considerations based on position and betting patterns

Be precise about hand rankings and probabilities. Identify key cards that could help or hurt your hand.

Respond with a structured analysis in this format:
```json
{
  "current_hand": "<description of current made hand>",
  "hand_strength": "<numeric rating from 1-10>",
  "outs": <number of cards that improve your hand>,
  "key_draws": "<description of potential draws>",
  "win_probability": "<estimated win probability percentage>",
  "recommendation": "<fold|check|call|bet|raise|all-in>",
  "reasoning": "<detailed explanation of your analysis>"
}
```
"""

hand_analysis_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are an expert poker analyzer. Provide accurate, objective analysis of Texas Hold'em hands."),
    HumanMessagePromptTemplate.from_template(HAND_ANALYSIS_PROMPT)
])

# Opponent modeling prompt with structured output

OPPONENT_MODELING_PROMPT = """
Analyze the betting patterns and playing style of your opponents based on their actions in this session:

{opponent_actions}

For each opponent, provide:
1. Their apparent playing style (tight/loose, aggressive/passive)
2. Hand range they might be playing
3. Tendencies (bluffing frequency, folding to pressure, etc.)
4. Exploitable weaknesses

Respond with a structured analysis in this format:
```json
{
  "opponents": [
    {
      "name": "<player name>",
      "style": "<tight-passive|tight-aggressive|loose-passive|loose-aggressive>",
      "hand_range": "<description of likely hands>",
      "tendencies": "<key behavioral patterns>",
      "weaknesses": "<exploitable traits>",
      "adjustment": "<how you should adjust your play against them>"
    }
  ]
}
```
"""

opponent_modeling_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a skilled poker player with a talent for reading opponents."),
    HumanMessagePromptTemplate.from_template(OPPONENT_MODELING_PROMPT)
])

# Game summary prompt for structured analysis

GAME_SUMMARY_PROMPT = """
Provide a summary of the completed poker hand:

FINAL COMMUNITY CARDS: {community_cards}
WINNING PLAYER: {winner_name}
WINNING HAND: {winning_hand}
POT SIZE: ${pot_size}
HAND HISTORY:
{hand_history}

Analyze the key decision points, strategic elements, and whether players made optimal choices.

Respond with a structured analysis in this format:
```json
{
  "key_moments": [
    {"phase": "<game phase>", "action": "<significant action>", "impact": "<how it affected the hand>"}
  ],
  "optimal_plays": ["<description of good decisions made>"],
  "mistakes": ["<description of errors or suboptimal plays>"],
  "lessons": ["<key takeaways from this hand>"]
}
```
"""

game_summary_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a poker commentator providing insightful analysis of completed hands."),
    HumanMessagePromptTemplate.from_template(GAME_SUMMARY_PROMPT)
])

# Function to get the appropriate system prompt based on player style
def get_system_prompt(player_style: str) -> str:
    """Get the system prompt for a given player style."""
    style_prompts = {
        "conservative": CONSERVATIVE_SYSTEM_PROMPT,
        "aggressive": AGGRESSIVE_SYSTEM_PROMPT,
        "balanced": BALANCED_SYSTEM_PROMPT,
        "loose": LOOSE_SYSTEM_PROMPT
    }
    return style_prompts.get(player_style.lower(), BALANCED_SYSTEM_PROMPT)

# Function to get example decisions for a given style
def get_example_decisions(player_style: str) -> list:
    """Get example decisions appropriate for the playing style."""
    
    conservative_examples = [
        {"action": "fold", "amount": 0, "reasoning": "My 8-3 offsuit is weak and out of position against a raise."},
        {"action": "call", "amount": 50, "reasoning": "I have AK suited. Worth seeing a flop in position."},
        {"action": "raise", "amount": 150, "reasoning": "Pocket kings are the second strongest starting hand. Building value."}
    ]
    
    aggressive_examples = [
        {"action": "raise", "amount": 200, "reasoning": "Applying pressure with position even with marginal holdings."},
        {"action": "all-in", "amount": 850, "reasoning": "Semi-bluff with the flush draw. Maximizing fold equity."},
        {"action": "bet", "amount": 150, "reasoning": "C-betting the flop to take down the pot now."}
    ]
    
    balanced_examples = [
        {"action": "fold", "amount": 0, "reasoning": "Weak hand facing multiple raises. Saving chips for better spots."},
        {"action": "call", "amount": 100, "reasoning": "Pot odds justify continuing with my draw."},
        {"action": "raise", "amount": 250, "reasoning": "Value betting my top pair top kicker."}
    ]
    
    loose_examples = [
        {"action": "call", "amount": 75, "reasoning": "Speculative hand with suited connectors. Worth seeing a flop."},
        {"action": "raise", "amount": 300, "reasoning": "Representing strength to take down the pot now."},
        {"action": "all-in", "amount": 650, "reasoning": "Going for the big bluff against the tight player."}
    ]
    
    style_examples = {
        "conservative": conservative_examples,
        "aggressive": aggressive_examples,
        "balanced": balanced_examples,
        "loose": loose_examples
    }
    
    return style_examples.get(player_style.lower(), balanced_examples)