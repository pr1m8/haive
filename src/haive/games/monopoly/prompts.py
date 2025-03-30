from langchain_core.prompts import ChatPromptTemplate

def generate_move_decision_prompt() -> ChatPromptTemplate:
    """Creates a prompt for the player to decide on movement-related actions."""
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a strategic Monopoly player assistant. You need to decide what move to make next.\n\n"
            "The actions available are:\n"
            "1. ROLL DICE - Roll the dice to move around the board (if you haven't rolled yet)\n"
            "2. PAY TO EXIT JAIL - Pay $50 to get out of jail (only if in jail)\n"
            "3. ROLL FOR DOUBLE - Try to roll a double to get out of jail (only if in jail)\n\n"
            "Consider your position, cash reserves, and overall game strategy before making a decision.\n"
            "You are playing to win by acquiring properties, developing them strategically, and eventually bankrupting your opponent."
        ),
        (
            "human",
            "# Current Game State\n"
            "Turn: {turn}\n"
            "Cash: ${current_player_cash}\n"
            "Position: {current_position} ({current_location})\n"
            "In Jail: {in_jail}\n"
            "Has Already Rolled: {has_rolled}\n\n"
            "# Board Information\n"
            "{board_representation}\n\n"
            "# Recent Events\n"
            "{recent_events}\n\n"
            "# Legal Moves\n"
            "{legal_moves}\n\n"
            "What move action do you want to make? Provide your reasoning."
        )
    ])

def generate_property_decision_prompt() -> ChatPromptTemplate:
    """Creates a prompt for the player to decide on property-related actions."""
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a strategic Monopoly player assistant. You need to decide what property actions to take.\n\n"
            "The property actions available include:\n"
            "1. BUY - Purchase an unowned property you've landed on\n"
            "2. BUILD HOUSE - Construct houses or hotels on properties you own\n"
            "3. SELL HOUSE - Sell houses or hotels to generate cash\n"
            "4. MORTGAGE - Mortgage a property to generate cash\n"
            "5. UNMORTGAGE - Pay off a mortgage to start earning rent again\n\n"
            "Consider your property portfolio, color group monopolies, cash reserves, and likely opponent moves.\n"
            "The most valuable monopolies are generally in this order: Orange > Red > Yellow/Green > Light Blue > Dark Blue > Purple > Dark Purple > Utilities/Railroads"
        ),
        (
            "human",
            "# Current Game State\n"
            "Turn: {turn}\n"
            "Cash: ${current_player_cash}\n"
            "Total Wealth: ${current_player_wealth}\n"
            "Current Position: {current_position} ({current_location})\n\n"
            "# Your Properties\n"
            "{player_properties}\n\n"
            "# Opponent's Properties\n"
            "{opponent_properties}\n\n"
            "# Available Property Actions\n"
            "{available_property_actions}\n\n"
            "# Recent Events\n"
            "{recent_events}\n\n"
            "What property actions do you want to take? You can list multiple actions if appropriate.\n"
            "For each action, specify the action type, property name, and your reasoning."
        )
    ])

def generate_strategy_analysis_prompt() -> ChatPromptTemplate:
    """Creates a prompt for the player to analyze their strategic position."""
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a Monopoly strategy expert. Analyze the current game state and provide strategic recommendations.\n\n"
            "Focus on:\n"
            "1. Property acquisition strategy - which color groups to pursue\n"
            "2. Development strategy - where to build houses\n"
            "3. Cash management - how much to keep in reserve\n"
            "4. Risk assessment - current dangers and how to mitigate them\n"
            "5. Opponent strategy - what your opponent might be planning\n\n"
            "Provide specific, actionable recommendations based on the current game state."
        ),
        (
            "human",
            "# Current Game State\n"
            "Turn: {turn}\n"
            "Round: {current_round}\n"
            "Cash: ${current_player_cash}\n"
            "Total Wealth: ${current_player_wealth}\n\n"
            "# Board Overview\n"
            "{board_representation}\n\n"
            "# Player Properties\n"
            "{player_properties}\n\n"
            "# Opponent's Properties\n"
            "{opponent_properties}\n\n"
            "# Recent Events\n"
            "{recent_events}\n\n"
            "Analyze my current position. What are my strategic strengths and weaknesses?\n"
            "What opportunities should I capitalize on, and what risks should I be aware of?\n"
            "Give specific recommendations for my next few turns."
        )
    ])

def generate_turn_decision_prompt() -> ChatPromptTemplate:
    """Creates a prompt for the player to make all decisions for their turn."""
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a strategic Monopoly player. Make decisions for your turn.\n\n"
            "Your decisions should include:\n"
            "1. MOVE ACTION (roll, pay to exit jail, roll for double)\n"
            "2. PROPERTY ACTIONS (buy, build, sell, mortgage, unmortgage)\n"
            "3. Whether to END TURN\n\n"
            "Think step-by-step to make the best strategic decisions. Consider your cash position, property ownership, opponent's position, and the likelihood of landing on different properties.\n\n"
            "The most valuable monopolies in Monopoly are generally: Orange > Red > Yellow/Green > Light Blue > Dark Blue > Purple > Dark Purple > Utilities/Railroads."
        ),
        (
            "human",
            "# Current Game State\n"
            "Turn: {turn}\n"
            "Cash: ${current_player_cash}\n"
            "Total Wealth: ${current_player_wealth}\n"
            "Position: {current_position} ({current_location})\n"
            "In Jail: {in_jail}\n"
            "Has Already Rolled: {has_rolled}\n\n"
            "# Board State\n"
            "{board_representation}\n\n"
            "# Property Ownership\n"
            "Your Properties: {player_properties}\n"
            "Opponent's Properties: {opponent_properties}\n\n"
            "# Available Actions\n"
            "Move Actions: {legal_moves}\n"
            "Property Actions: {available_property_actions}\n\n"
            "# Recent Events\n"
            "{recent_events}\n\n"
            "What decisions will you make for this turn? Think step-by-step about:\n"
            "1. What move action to take (if any)\n"
            "2. What property actions to take (if any)\n"
            "3. Whether to end your turn\n\n"
            "Provide clear reasoning for each decision."
        )
    ])