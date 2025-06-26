# Among Us Game Mechanics

This document outlines the enhanced game mechanics and rules for the improved Among Us game implementation.

## Core Gameplay Loop

The Among Us game follows this core gameplay loop:

1. **Task Phase**: Players move around the map, with crewmates completing tasks and impostors pretending to do tasks while looking for opportunities to eliminate crewmates.

2. **Meeting Phase**: Triggered by a player reporting a dead body or calling an emergency meeting, all players gather to discuss and share information.

3. **Voting Phase**: Players vote on who they suspect is an impostor, with the player receiving the most votes being ejected from the game.

4. **Win Conditions**: Crewmates win by completing all tasks or eliminating all impostors. Impostors win by eliminating enough crewmates to match or outnumber them, or by causing a critical sabotage to succeed.

## Enhanced Game Mechanics

### 1. Movement and Navigation

#### Room Connectivity

- Each room connects to specific other rooms with defined travel times
- Doors can be locked via sabotage, temporarily blocking passage
- Moving between rooms has a small delay based on:
  - Distance between rooms
  - Player speed setting
  - Whether the player is currently under suspicion (slows down impostor movements)

#### Line of Sight and Visibility

- Players can only see other players in the same room
- Vision range is limited and can be further reduced by sabotages
- Players maintain a "last seen" record for each other player
- Some tasks require focused attention, reducing peripheral vision while performing them

#### Room Occupancy Awareness

- Players are notified when someone enters or leaves a room they're in
- Players can see traces of recent activity (e.g., completed tasks, sabotage repairs)
- Security cameras allow remote viewing of certain rooms

### 2. Task System

#### Task Types and Mechanics

1. **Visual Tasks**
   - Show visible confirmation to other players when completed
   - Examples: Medical Scan, Asteroid Shooting, Shield Priming
   - Cannot be faked by impostors (other players will see no visual confirmation)

2. **Common Tasks**
   - Assigned to all crewmates
   - Examples: Card Swipe, Wiring
   - Easy to detect if someone claims different common tasks than others

3. **Short Tasks**
   - Quick to complete (2-5 seconds)
   - Single-step tasks
   - Examples: Align Engine Output, Chart Course

4. **Long Tasks**
   - Multi-step tasks that require more time
   - May span multiple rooms or have waiting periods
   - Examples: Upload/Download Data, Inspect Sample

5. **Critical Tasks**
   - Related to ship systems
   - Higher priority for game completion
   - Examples: Stabilize Reactor, Fix Oxygen

#### Task Mini-Games

Each task involves a simple mini-game mechanic:

1. **Pattern Matching**: Match a pattern or sequence
2. **Timing Challenges**: Click at the right moment
3. **Sorting**: Arrange items in the correct order
4. **Connection**: Connect matching items or wires
5. **Numerical Input**: Enter correct values
6. **Calibration**: Adjust sliders to target positions

#### Task Assignment and Completion

- Tasks are strategically distributed across the map
- Some tasks have prerequisites (e.g., "Download Data" must happen before "Upload Data")
- Task completion affects ship systems and game state
- Task completion updates can be set to "always," "meetings," or "never" to adjust difficulty

### 3. Impostor Abilities

#### Kill Mechanics

- Cooldown-based ability (configurable, default 45 seconds)
- Can only kill when no other crewmates are in the room (no witnesses)
- Killing leaves evidence that lasts for a period
- Body discovery has a proximity trigger
- Kill animations vary and may have different durations

#### Vent System

- Impostors can enter, hide in, and travel through vents
- Vent map is connected differently than the main room paths
- Limited oxygen in vents restricts how long impostors can stay
- Entering/exiting vents has a brief animation that can be spotted
- Some vents have one-way connections or special properties

#### Sabotage Abilities

1. **Critical Sabotages**
   - **Oxygen Depletion**: 30-45 second timer, requires two-location fix
   - **Reactor Meltdown**: 30-45 second timer, requires two-location fix
   - Only one critical sabotage can be active at a time
   - Causes game loss for crewmates if timer expires

2. **Utility Sabotages**
   - **Communications Disruption**: Disables task list and security systems
   - **Electrical Failure**: Reduces vision range significantly
   - **Door Locks**: Locks specific room doors for 10 seconds
   - Multiple utility sabotages can be active simultaneously

3. **Sabotage Cooldown System**
   - Global cooldown of 20-30 seconds between any sabotages
   - Longer cooldowns for critical sabotages (45-60 seconds)
   - Cooldown visible only to impostors
   - Strategically timing sabotages is crucial

### 4. Meeting and Voting System

#### Meeting Triggers

- **Body Reporting**: Player finds a dead body and reports it
- **Emergency Meeting**: Player calls a meeting at designated location (limited uses)
- Meeting transitions the game to a discussion phase

#### Discussion Phase

- Timed discussion period (configurable, default 45 seconds)
- Players take turns sharing information and suspicions
- Chat history is visible to all players
- Players can reference their observations and evidence

#### Voting Phase

- Timed voting period (configurable, default 30 seconds)
- Each player casts one vote or chooses to skip
- Vote visualization can be anonymous (configurable)
- Results are tallied and the player with most votes is ejected
- Tie votes result in no ejection
- Option to confirm the ejected player's role (configurable)

### 5. Evidence and Detection System

#### Physical Evidence

- Kill locations leave temporary traces
- Vent usage creates brief disturbances
- Task completion leaves visible indicators
- Sabotage resolution shows who helped fix

#### Alibis and Verification

- Visual tasks provide solid alibis for crewmates
- Security cameras provide verifiable location information
- Admin table shows room occupancy counts
- Medbay scan queuing creates mutual verification opportunities

#### Suspicion Mechanics

- Actions increase or decrease suspicion levels
- Suspicious behavior is tracked in player memory
- Evidence can be cross-referenced during meetings
- Behavior analysis helps identify impostor patterns

### 6. Environment and Map Features

#### Security Systems

- **Cameras**: View specific rooms remotely
- **Admin Table**: See room occupancy counts
- **Door Logs**: Track player movements between rooms
- **Vitals Monitor**: Check which players are alive or dead

#### Map Hazards and Features

- **Reactor**: Critical system that can be sabotaged
- **Oxygen**: Life support system that can be sabotaged
- **Electrical**: Controls lighting and can be sabotaged
- **Communications**: Controls information systems and can be sabotaged

#### Special Rooms

- **Cafeteria/Meeting Room**: Location for emergency meetings
- **Security**: Location of security cameras
- **Admin**: Location of admin table
- **Medbay**: Location of vitals and med scan

### 7. Player Memory and Information System

#### Observation Recording

- Players automatically record observations in their memory
- Observations include player movements, task completions, and suspicious activities
- Memory has limited capacity and older observations may fade
- Important events are remembered longer than routine activities

#### Information Sharing

- During meetings, players can share their observations
- Shared information becomes part of group knowledge
- False information can be planted by impostors
- Credibility system tracks reliability of player claims

#### Detective Work

- Players can combine observations to deduce impostor identity
- Contradiction detection helps identify lies
- Timeline construction aids in establishing alibis
- Process of elimination narrows suspect pool

## Game Rules and Balance

### 1. Game Setup and Configuration

- **Player Count**: 4-15 players
- **Impostor Count**: 1-4 impostors (based on player count)
- **Map Selection**: Different maps with unique layouts and features
- **Task Configuration**: Adjust number and distribution of tasks
- **Meeting Settings**: Configure discussion time, voting time, and emergency meeting count
- **Confirmation Settings**: Toggle eject confirmations and anonymous voting

### 2. Balance Mechanisms

- **Task Balance**: Task counts and difficulty balanced against player count
- **Cooldown Balance**: Kill and sabotage cooldowns adjusted based on map size and player count
- **Vision Balance**: Crewmate and impostor vision ranges balanced for fair play
- **Movement Speed**: Configurable to adjust game pace
- **Sabotage Impact**: Critical sabotages balanced by resolution difficulty and time limits

### 3. Anti-Griefing Measures

- **Impostor Coordination**: Impostors can identify each other but must be careful about communication
- **Rage Quit Protection**: Game continues if players leave mid-game
- **Task Redistribution**: Tasks from disconnected players are redistributed or removed
- **Vote Skip Protection**: Skip votes count toward total to prevent trolling
- **Report Cooldown**: Brief cooldown after meetings to prevent spam

### 4. Edge Cases and Special Rules

- **Last Task Completion**: Final task triggers immediate win, even during meetings
- **Critical Mass Rule**: If impostors reach equal numbers with crewmates, game ends immediately
- **Ghost Mechanics**: Eliminated players can still complete tasks but cannot communicate
- **Sabotage During Meetings**: Not allowed
- **Vent Restrictions**: Cannot kill immediately after exiting a vent (brief cooldown)

## AI Agent Behavior Guidelines

### 1. Crewmate AI Strategy

- **Task Prioritization**: Optimize task completion routes
- **Evidence Collection**: Actively seek verifiable information
- **Buddy System**: Sometimes team up with trusted players
- **Security Usage**: Periodically check security systems
- **Suspicious Behavior Detection**: Monitor for unusual player movements
- **Meeting Effectiveness**: Share useful information during meetings

### 2. Impostor AI Strategy

- **Blend In**: Mimic crewmate task behavior
- **Strategic Kills**: Target isolated players and create alibis
- **Sabotage Timing**: Use sabotages to separate players or create distractions
- **Vent Usage**: Use vents for quick escapes or ambushes
- **Frame Others**: Create situations that cast suspicion on crewmates
- **Meeting Deception**: Provide false information without obvious lies

### 3. Adaptive Behavior

- Agents learn from game patterns
- Adjust strategies based on player actions
- Recognize and counter common tactics
- Balance risk and reward dynamically
- Develop unique personalities and play styles

## Game Flow Control

### 1. Round Progression

- Each round consists of one full task/meeting/voting cycle
- Round counter increments after each vote
- Game difficulty increases slightly each round
- Late-game tasks may be more complex
- Late-game sabotages may be more impactful

### 2. Time Management

- Task phase has no time limit but has task completion target
- Meeting discussion phase has configurable time limit
- Voting phase has configurable time limit
- Sabotage timers create urgency during critical events
- Overall game has a maximum round limit (configurable) to prevent stalemates

### 3. State Transitions

- Task → Meeting: Triggered by body report or emergency button
- Meeting → Voting: Automatic after discussion phase ends
- Voting → Task/Game Over: Automatic after voting results
- Any Phase → Game Over: Triggered when win conditions are met

## Enhanced Game Variants

### 1. Hide and Seek Mode

- Impostors are revealed at the start
- Impostors have reduced vision but no kill cooldown
- Crewmates must complete tasks before being caught
- No reporting or meetings allowed
- Fast-paced variant with different strategy

### 2. Sheriff Mode

- One crewmate is assigned the Sheriff role
- Sheriff can kill one player they suspect is an impostor
- If Sheriff kills a crewmate, Sheriff dies instead
- Adds "justified" killing to crewmate toolkit
- Increases strategic depth

### 3. Guardian Angel Mode

- Dead crewmates become Guardian Angels
- Guardian Angels can temporarily shield living players
- Each Guardian Angel has limited shields
- Adds protection mechanics and afterlife gameplay
- Changes impostor strategy significantly

### 4. Zombie Mode

- Killed crewmates become "infected"
- Infected players work with impostors
- Original impostors have special abilities
- Creates escalating difficulty for remaining crewmates
- Adds team-switching mechanics

### 5. Role Specialization Mode

- Crewmates have specialized roles with unique abilities
- Examples: Medic, Engineer, Detective, Scout
- Impostors have unique sabotage specializations
- Creates class-based gameplay
- Increases strategic depth and replayability

These enhanced mechanics create a much more strategic and engaging Among Us experience. The game rewards careful observation, logical deduction, and strategic planning, while still maintaining the core social deduction and betrayal elements that make Among Us fun.
