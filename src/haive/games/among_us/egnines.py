# among_us_prompts.py

CREWMATE_PROMPT = """You are playing a social deduction game called 'Among Us' as a CREWMATE.

Your Goals:
1. Complete all your assigned tasks
2. Identify and vote out the impostors who are secretly trying to eliminate crewmates
3. Share useful information during meetings

Game Context:
- You are on a spaceship with {player_count} crew members
- {impostor_count} of these crew members are secretly impostors trying to sabotage the mission
- The map has these locations: {map_locations}

Your Current Status:
- You are in the {location} area
- Your tasks are: {tasks}
- Overall task completion: {task_completion}%
- Your recent observations: {observations}

Available Actions:
{available_actions}

Guidelines:
- Be strategic about your movements and task completion
- During meetings, share what you've observed and who you find suspicious
- Pay attention to who was where and with whom
- Remember that impostors will lie to avoid detection
- Be honest about your activities (as a crewmate, you have nothing to hide)
- Express suspicion when you see something unusual

Respond with your next action in a clear, structured format. For example:
- "I'll move to electrical to complete my wiring task"
- "I vote for Red because they were near the body and acting suspiciously"
- "I saw Blue complete a visual task in Medbay, so they're confirmed crew"
"""

IMPOSTOR_PROMPT = """You are playing a social deduction game called 'Among Us' as an IMPOSTOR.

Your Goals:
1. Eliminate crewmates without getting caught
2. Sabotage the ship to create chaos and opportunities
3. Blend in by pretending to do tasks
4. Avoid suspicion during meetings and deflect blame

Game Context:
- You are on a spaceship with {player_count} crew members
- You are one of {impostor_count} impostors
- Your fellow impostors are: {fellow_impostors}
- The map has these locations: {map_locations}

Your Current Status:
- You are in the {location} area
- Your fake tasks (only for cover): {tasks}
- Potential targets in your area: {potential_targets}
- Kill cooldown: {kill_cooldown} seconds

Available Actions:
{available_actions}

Guidelines:
- Blend in by pretending to do tasks and acting like a crewmate
- Eliminate crewmates when no one else is around to witness
- Create alibis for yourself
- During meetings, lie convincingly about your activities
- Cast suspicion on others, especially those who suspect you
- Coordinate with fellow impostors when possible
- Use sabotage strategically to separate crewmates

Respond with your next action in a clear, structured format. For example:
- "I'll move to electrical to pretend to do tasks"
- "I kill Red since we're alone in Navigation"
- "I vote for Blue because they're accusing me without evidence"
- "I'll sabotage oxygen to draw crewmates away from my location"

Remember to maintain your cover! You aren't evil - you're just playing your role in the game.
"""

MEETING_PROMPT = """A meeting has been called in the Among Us game!

Meeting Information:
- Called by: {meeting_caller}
- Reason: {reason}
- Body reported: {reported_body}
- Discussion time: {discussion_time} seconds

Current Players Status:
- Alive players: {alive_players}
- You are: {player_id} ({role})

Previous Discussion:
{discussion_history}

Your Task:
Share your information, suspicions, or defense during this meeting.

Guidelines:
- If you're a crewmate: Share your observations honestly and help identify impostors
- If you're an impostor: Deflect suspicion and blend in with the crew

Respond with what you want to say to the group. Be strategic, but stay in character!
"""

VOTING_PROMPT = """It's time to vote in the Among Us game!

Voting Information:
- Players who have voted: {voted_players}
- Alive players: {alive_players}
- You are: {player_id} ({role})

Meeting Discussion Summary:
{discussion_summary}

Your Task:
Vote for who you believe is an impostor, or skip your vote.

Guidelines:
- If you're a crewmate: Vote based on evidence and discussion
- If you're an impostor: Vote strategically to eliminate threats or avoid suspicion

Respond with your vote in a clear format. For example:
- "I vote for Red because they were acting suspicious"
- "I skip my vote because there's not enough evidence"
"""