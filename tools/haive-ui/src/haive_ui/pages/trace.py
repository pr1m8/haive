"""Trace viewer page - view execution traces and observability data."""

import streamlit as st

from haive_ui.utils.tracer import TraceCollector


def render():
    st.title("Trace Viewer")

    if "tracer" not in st.session_state:
        st.session_state.tracer = TraceCollector()

    tracer: TraceCollector = st.session_state.tracer
    traces = tracer.get_recent(100)

    # Top bar
    col_gen, col_clear, col_info = st.columns([1, 1, 2])
    with col_gen:
        if st.button("Generate Sample Traces"):
            _generate_sample_traces(tracer)
            st.rerun()
    with col_clear:
        if st.button("Clear All Traces"):
            st.session_state.tracer = TraceCollector()
            st.rerun()
    with col_info:
        st.caption(f"{len(traces)} traces recorded this session. Traces persist across page navigation.")

    if not traces:
        st.info("No traces yet. Run an agent or game to generate traces, or click 'Generate Sample Traces'.")
        return

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Traces", len(traces))
    with col2:
        completed = sum(1 for t in traces if t.status == "completed")
        st.metric("Completed", completed)
    with col3:
        errors = sum(1 for t in traces if t.status == "error")
        st.metric("Errors", errors)
    with col4:
        total_events = sum(len(t.events) for t in traces)
        st.metric("Total Events", total_events)

    st.divider()

    # Filter
    col_filter, col_search = st.columns([1, 2])
    with col_filter:
        status_filter = st.multiselect(
            "Filter by status",
            ["running", "completed", "error"],
            default=["running", "completed", "error"],
            key="trace_status_filter",
        )
    with col_search:
        trace_search = st.text_input("Search traces", "", key="trace_search")

    # Trace list
    for trace in traces:
        if trace.status not in status_filter:
            continue
        if trace_search and trace_search.lower() not in trace.name.lower():
            continue

        status_icon = {"completed": "OK", "error": "ERR", "running": "..."}.get(trace.status, "?")
        duration_str = f"{trace.total_duration_ms:.0f}ms" if trace.total_duration_ms else "..."

        with st.expander(
            f"[{status_icon}] **{trace.name}** | {trace.trace_id} | {duration_str} | {len(trace.events)} events"
        ):
            # Trace metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"Started: {trace.started_at}")
            with col2:
                st.caption(f"Status: {trace.status}")
            with col3:
                st.caption(f"Duration: {duration_str}")

            if trace.token_usage["total"] > 0:
                st.caption(
                    f"Tokens: {trace.token_usage['input']} in / "
                    f"{trace.token_usage['output']} out / "
                    f"{trace.token_usage['total']} total"
                )

            # Event timeline
            st.markdown("**Events:**")
            for event in trace.events:
                event_prefix = {
                    "input": ">>",
                    "output": "<<",
                    "llm_call": "AI",
                    "tool_call": "T>",
                    "game_move": "GM",
                    "error": "!!",
                }.get(event.event_type, "--")

                elapsed = event.metadata.get("elapsed_ms", 0)
                elapsed_str = f"+{elapsed:.0f}ms" if elapsed else ""

                st.markdown(
                    f"`{event_prefix}` **{event.event_type}** [{event.agent_name}] {elapsed_str}"
                )
                st.code(event.content[:500], language=None)

                if event.metadata:
                    filtered_meta = {k: v for k, v in event.metadata.items() if k != "elapsed_ms"}
                    if filtered_meta:
                        st.json(filtered_meta)


def _generate_sample_traces(tracer: TraceCollector):
    """Generate sample traces for games and agents."""

    # -- Game traces --
    _game_trace(tracer, "TicTacToe", "TicTacToeAgent", [
        ("X", "Center (1,1)"), ("O", "Corner (0,0)"), ("X", "Edge (0,1)"),
        ("O", "Corner (2,2)"), ("X", "Edge (2,1) - wins!")
    ], "X wins! Three in a column.")

    _game_trace(tracer, "Chess", "ChessAgent", [
        ("White", "e2-e4"), ("Black", "e7-e5"), ("White", "Bf1-c4"),
        ("Black", "Nb8-c6"), ("White", "Qd1-h5"), ("Black", "Ng8-f6??"),
        ("White", "Qh5xf7# Checkmate!")
    ], "White wins by Scholar's Mate.")

    _game_trace(tracer, "Go", "GoAgent", [
        ("Black", "D5"), ("White", "F5"), ("Black", "C3"),
        ("White", "Pass"), ("Black", "Pass")
    ], "Black wins by 4.5 points.")

    _game_trace(tracer, "Checkers", "CheckersAgent", [
        ("Red", "Move 3-7"), ("Black", "Move 22-17"), ("Red", "Jump 7-14")
    ], "Red wins by capturing all pieces.")

    _game_trace(tracer, "Connect4", "Connect4Agent", [
        ("Player1", "Column 4"), ("Player2", "Column 3"),
        ("Player1", "Column 4"), ("Player2", "Column 5"),
        ("Player1", "Column 4"), ("Player2", "Column 2"),
        ("Player1", "Column 4 - wins!")
    ], "Player 1 wins with vertical connect four!")

    _game_trace(tracer, "Battleship", "BattleshipAgent", [
        ("Player1", "Fire at B5 - Miss"), ("Player2", "Fire at D3 - Hit!"),
        ("Player1", "Fire at B6 - Hit!"), ("Player2", "Fire at D4 - Hit! Sunk Destroyer!")
    ], "Player 2 wins. All ships sunk.")

    _game_trace(tracer, "Reversi", "ReversiAgent", [
        ("Black", "Place at D3"), ("White", "Place at C5"),
        ("Black", "Place at F6"), ("White", "Place at E3")
    ], "Black wins 38-26.")

    _game_trace(tracer, "Mancala", "MancalaAgent", [
        ("Player1", "Pit 3"), ("Player2", "Pit 5"), ("Player1", "Pit 1 - extra turn"),
    ], "Player 1 wins 26-22.")

    _game_trace(tracer, "Poker", "PokerAgent", [
        ("Dealer", "Deal: Player1=[Ah,Kh], Player2=[Qs,Jd]"),
        ("Player1", "Raise $50"), ("Player2", "Call"),
        ("Dealer", "Flop: [10h, 2h, 7s]"),
        ("Player1", "All-in"), ("Player2", "Fold")
    ], "Player 1 wins $150 pot.")

    _game_trace(tracer, "Hold'em", "HoldemGameAgent", [
        ("Dealer", "Deal hole cards"), ("Player1", "Raise"),
        ("Player2", "Call"), ("Dealer", "Flop revealed")
    ], "Player 1 wins the hand.")

    _game_trace(tracer, "Dominoes", "DominoesAgent", [
        ("Player1", "[6|6]"), ("Player2", "[6|4]"), ("Player1", "[4|3]"),
    ], "Player 1 wins. Player 2 has 12 points left.")

    _game_trace(tracer, "Risk", "RiskAgent", [
        ("Player1", "Deploy 5 to North America"), ("Player2", "Deploy 3 to Europe"),
        ("Player1", "Attack Europe from NA (3v2)"), ("Player1", "Won battle, captured territory")
    ], "Player 1 achieves world domination.")

    _game_trace(tracer, "Monopoly", "MonopolyAgent", [
        ("Player1", "Roll 7, land on Boardwalk, buy for $400"),
        ("Player2", "Roll 5, land on Community Chest"),
        ("Player1", "Roll 11, land on Park Place, buy for $350")
    ], "Player 1 wins with monopoly on dark blue.")

    _game_trace(tracer, "Nim", "NimAgent", [
        ("Player1", "Take 2 from pile 1 (5->3)"),
        ("Player2", "Take 1 from pile 2 (4->3)"),
        ("Player1", "Take 3 from pile 1 (3->0)"),
        ("Player2", "Take 3 from pile 2 (3->0) - last object")
    ], "Player 1 wins (misere rules).")

    _game_trace(tracer, "Fox & Geese", "FoxAndGeeseAgent", [
        ("Fox", "Move to center"), ("Geese", "Advance formation"),
        ("Fox", "Jump goose!"), ("Geese", "Close ranks")
    ], "Fox escapes! Fox wins.")

    _game_trace(tracer, "Mafia", "MafiaAgent", [
        ("Narrator", "Night phase. Mafia chooses victim."),
        ("Mafia", "Eliminate Player3"), ("Doctor", "Protect Player2"),
        ("Narrator", "Day phase. Player3 eliminated."),
        ("Town", "Vote: Player5 is suspicious"), ("Town", "Player5 eliminated - was Mafia!")
    ], "Town wins! All mafia eliminated.")

    _game_trace(tracer, "Among Us", "AmongUsAgent", [
        ("System", "Tasks: 3/10 completed"), ("Impostor", "Sabotage reactor"),
        ("Crewmate1", "Report body in Electrical!"),
        ("Discussion", "Vote: Crewmate3 is sus"), ("System", "Crewmate3 was not the impostor")
    ], "Impostor wins. Not enough crew remaining.")

    _game_trace(tracer, "Clue", "ClueAgent", [
        ("Player1", "Move to Library, suggest: Col. Mustard, Wrench, Library"),
        ("Player2", "Shows card: Library"), ("Player3", "Move to Kitchen"),
        ("Player1", "Accuse: Prof. Plum, Candlestick, Conservatory")
    ], "Player 1 correct! Mystery solved.")

    _game_trace(tracer, "Mastermind", "MastermindAgent", [
        ("Codemaker", "Secret code set (4 pegs)"),
        ("Breaker", "Guess: RGBY -> 1 black, 2 white"),
        ("Breaker", "Guess: GBRY -> 2 black, 1 white"),
        ("Breaker", "Guess: GRYB -> 4 black! Code broken!")
    ], "Code broken in 3 guesses!")

    _game_trace(tracer, "Debate", "DebateAgent", [
        ("Moderator", "Topic: Is AI beneficial for education?"),
        ("Pro", "AI personalizes learning and increases access"),
        ("Con", "AI risks replacing human mentorship"),
        ("Pro", "Rebuttal: AI augments, not replaces teachers")
    ], "Debate concluded. Pro arguments rated higher.")

    _game_trace(tracer, "Debate V2", "GameDebateAgent", [
        ("Moderator", "Topic: Space exploration funding"),
        ("For", "Investment drives innovation"), ("Against", "Resources needed on Earth"),
    ], "For wins 7-5.")

    _game_trace(tracer, "Debate V2 Judges", "JudgedGameDebateAgent", [
        ("Moderator", "Topic: Universal Basic Income"),
        ("Pro", "Reduces poverty"), ("Con", "Creates inflation risk"),
        ("Judge1", "Score: Pro 8/10, Con 7/10"),
        ("Judge2", "Score: Pro 7/10, Con 8/10"),
        ("Judge3", "Score: Pro 9/10, Con 6/10")
    ], "Pro wins 24-21 across 3 judges.")

    # -- Agent traces --
    _agent_trace(tracer, "Simple Agent", "SimpleAgent", "What is Python?",
                 "Python is a high-level programming language known for readability.", 150)

    _agent_trace(tracer, "React Agent", "ReactAgent", "Calculate 15*23",
                 "Using calculator tool. 15 * 23 = 345", 820,
                 tool_calls=[("calculator", "15*23", "345")])

    _agent_trace(tracer, "Dynamic Supervisor", "DynamicSupervisor", "Research and summarize AI trends",
                 "Delegated to researcher and summarizer agents. Key trends: LLMs, multimodal AI.", 2500)

    # RAG agents
    for name in ["Adaptive RAG", "Corrective RAG", "FLARE RAG", "Fusion RAG", "HyDE RAG",
                  "Multi-Query RAG", "Self-Route RAG", "Speculative RAG", "Step-Back RAG",
                  "Memory-Aware RAG", "Document Grading RAG", "Agentic RAG", "Filtered RAG",
                  "Hallucination Grader", "Query Decomposer"]:
        _agent_trace(tracer, name, name.replace(" ", ""), f"RAG query for {name}",
                     f"Retrieved 3 documents. Generated answer using {name} strategy.", 950)

    # Reasoning agents
    _agent_trace(tracer, "Self-Discover", "SelfDiscover", "Solve: optimize delivery routes",
                 "Selected reasoning modules: decomposition, constraint analysis. Solution found.", 3200)
    _agent_trace(tracer, "Reflection", "ReflectionAgent", "Write essay on climate change",
                 "Draft -> Reflection -> Revised draft. Quality improved from 6/10 to 9/10.", 4500)
    _agent_trace(tracer, "Reflexion", "ReflexionAgent", "Debug this code: def factorial(n): return n * factorial(n)",
                 "Attempt 1 failed (infinite recursion). Reflected. Attempt 2: added base case. Correct.", 2800)
    _agent_trace(tracer, "Tree of Thought", "ToTAgent", "Creative problem: design a new board game",
                 "Generated 3 branches, evaluated each. Best: cooperative puzzle game.", 5000)
    _agent_trace(tracer, "LATS", "LATSAgent", "Solve logic puzzle",
                 "Tree search with 4 expansions. Found optimal solution path.", 6000)
    _agent_trace(tracer, "MCTS", "MCTSAgent", "Best move in game position",
                 "1000 simulations. Best move: C4 (win rate 72%).", 3500)
    _agent_trace(tracer, "Logic Agent", "LogicAgent", "Analyze argument validity",
                 "Premises valid. Conclusion follows logically. Argument is sound.", 1200)

    # Planning agents
    _agent_trace(tracer, "Plan & Execute", "PlanAndExecuteAgent", "Build a web scraper",
                 "Plan: 1) Design architecture 2) Implement scraper 3) Test. All steps completed.", 4000)
    _agent_trace(tracer, "ReWOO V3", "ReWOOV3Agent", "Research quantum computing",
                 "Plan without observation. 3 search tasks planned, results synthesized.", 3000)
    _agent_trace(tracer, "LLM Compiler V3", "LLMCompilerV3Agent", "Data pipeline task",
                 "Compiled 4 parallel tasks. Executed in 2 waves. Pipeline complete.", 2500)
    _agent_trace(tracer, "Plan Execute V3", "PlanExecuteV3Agent", "Project planning",
                 "Generated 5-step plan. Executed with evaluation. 4/5 steps successful.", 3500)

    # Research agents
    _agent_trace(tracer, "Open Perplexity", "ResearchAgent", "Latest AI developments",
                 "Searched 5 sources. Synthesized findings on LLMs, multimodal AI, reasoning.", 2000)
    _agent_trace(tracer, "Person Research", "PersonResearchAgent", "Research Alan Turing",
                 "Found biography, publications, awards. Generated comprehensive profile.", 1800)

    # Conversation agents
    _agent_trace(tracer, "Base Conversation", "BaseConversationAgent", "Hello, how are you?",
                 "Multi-turn conversation initialized. Responded with greeting.", 400)
    _agent_trace(tracer, "Collaborative Conversation", "CollaborativeConversation", "Let's brainstorm product ideas",
                 "3 agents collaborated. Generated 5 unique product ideas.", 3000)
    _agent_trace(tracer, "Debate Conversation", "DebateConversation", "Should AI be regulated?",
                 "Pro and con agents debated. 3 rounds of arguments.", 4000)
    _agent_trace(tracer, "Directed Conversation", "DirectedConversation", "Interview about career goals",
                 "Directed 5-question interview completed. Summary generated.", 2500)
    _agent_trace(tracer, "Social Media Conversation", "SocialMediaConversation", "Viral tweet about space",
                 "Generated tweet thread with engagement simulation.", 1500)
    _agent_trace(tracer, "Round Robin Conversation", "RoundRobinConversation", "Team standup meeting",
                 "4 agents reported status in round-robin order.", 2000)

    # Error trace example
    tracer.start_trace("Error Example: API Timeout")
    tracer.log("input", "TestAgent", "This is a simulated error trace")
    tracer.log("llm_call", "TestAgent", "Calling LLM API...")
    tracer.log("error", "TestAgent", "TimeoutError: API call timed out after 30s")
    tracer.end_trace("error")


def _game_trace(tracer: TraceCollector, game_name: str, agent_name: str,
                moves: list[tuple[str, str]], result: str):
    """Generate a sample game trace."""
    tracer.start_trace(f"{game_name}: Sample Game")
    tracer.log("input", agent_name, f"Starting {game_name} game.")
    for player, move in moves:
        tracer.log("game_move", player, move)
    tracer.log("output", agent_name, result)
    tracer.end_trace("completed")


def _agent_trace(tracer: TraceCollector, agent_name: str, class_name: str,
                 query: str, result: str, duration_ms: float,
                 tool_calls: list[tuple[str, str, str]] | None = None):
    """Generate a sample agent trace."""
    tracer.start_trace(f"{agent_name}: {query[:40]}")
    tracer.log("input", class_name, query)
    tracer.log("llm_call", class_name, f"Processing with {class_name}")
    if tool_calls:
        for tool_name, tool_input, tool_output in tool_calls:
            tracer.log("tool_call", tool_name, f"Input: {tool_input} -> Output: {tool_output}")
    tracer.log("output", class_name, result)
    tracer.end_trace("completed")
