"""Trace viewer page - view execution traces and observability data."""

import streamlit as st

from haive_ui.utils.tracer import TraceCollector


def render():
    st.title("Trace Viewer")

    if "tracer" not in st.session_state:
        st.session_state.tracer = TraceCollector()

    tracer: TraceCollector = st.session_state.tracer
    traces = tracer.get_recent(50)

    if not traces:
        st.info("No traces yet. Run an agent or game to generate traces.")
        if st.button("Generate Sample Traces"):
            _generate_sample_traces(tracer)
            st.rerun()
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
    status_filter = st.multiselect(
        "Filter by status",
        ["running", "completed", "error"],
        default=["running", "completed", "error"],
        key="trace_status_filter",
    )

    # Trace list
    for trace in traces:
        if trace.status not in status_filter:
            continue

        status_icon = {"completed": "✅", "error": "❌", "running": "⏳"}.get(trace.status, "❓")
        duration_str = f"{trace.total_duration_ms:.0f}ms" if trace.total_duration_ms else "..."

        with st.expander(
            f"{status_icon} **{trace.name}** | {trace.trace_id} | {duration_str} | {len(trace.events)} events"
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
                event_icon = {
                    "input": "📥",
                    "output": "📤",
                    "llm_call": "🤖",
                    "tool_call": "🔧",
                    "game_move": "🎮",
                    "error": "❌",
                }.get(event.event_type, "📝")

                elapsed = event.metadata.get("elapsed_ms", 0)
                elapsed_str = f"+{elapsed:.0f}ms" if elapsed else ""

                st.markdown(
                    f"{event_icon} **{event.event_type}** [{event.agent_name}] {elapsed_str}"
                )
                st.code(event.content[:500], language=None)

                if event.metadata:
                    filtered_meta = {k: v for k, v in event.metadata.items() if k != "elapsed_ms"}
                    if filtered_meta:
                        st.json(filtered_meta)

    st.divider()

    # Actions
    col_clear, col_gen = st.columns(2)
    with col_clear:
        if st.button("Clear All Traces", type="secondary"):
            st.session_state.tracer = TraceCollector()
            st.rerun()
    with col_gen:
        if st.button("Generate Sample Traces"):
            _generate_sample_traces(tracer)
            st.rerun()


def _generate_sample_traces(tracer: TraceCollector):
    """Generate sample traces for all 22 games and 37 agents."""

    # ── GAME TRACES (22 games) ──────────────────────────────────────

    tracer.start_trace("TicTacToe: Quick Game")
    tracer.log("input", "TicTacToeAgent", "Starting Tic Tac Toe. X plays first.", game="tictactoe")
    tracer.log("game_move", "X", "Center (1,1)", move="1,1", turn=1)
    tracer.log("game_move", "O", "Corner (0,0)", move="0,0", turn=2)
    tracer.log("game_move", "X", "Edge (0,1)", move="0,1", turn=3)
    tracer.log("game_move", "O", "Corner (2,2)", move="2,2", turn=4)
    tracer.log("game_move", "X", "Edge (2,1) - wins!", move="2,1", turn=5)
    tracer.log("output", "TicTacToeAgent", "X wins! Three in a column.", winner="X", turns=5)
    tracer.end_trace("completed")

    tracer.start_trace("Chess: Scholars Mate")
    tracer.log("input", "ChessAgent", "Starting chess. White plays first.", game="chess")
    tracer.log("game_move", "White", "e2-e4", move="e4", turn=1)
    tracer.log("game_move", "Black", "e7-e5", move="e5", turn=2)
    tracer.log("game_move", "White", "Bf1-c4", move="Bc4", turn=3)
    tracer.log("game_move", "Black", "Nb8-c6", move="Nc6", turn=4)
    tracer.log("game_move", "White", "Qd1-h5", move="Qh5", turn=5)
    tracer.log("game_move", "Black", "Ng8-f6??", move="Nf6", turn=6)
    tracer.log("game_move", "White", "Qh5xf7# Checkmate!", move="Qxf7#", turn=7)
    tracer.log("output", "ChessAgent", "White wins by Scholar's Mate in 4 moves.", winner="White", total_moves=7)
    tracer.end_trace("completed")

    tracer.start_trace("Go: 9x9 Board")
    tracer.log("input", "GoAgent", "Starting 9x9 Go game. Black plays first.", game="go", board_size=9)
    tracer.log("game_move", "Black", "Place stone at D5", move="D5", turn=1)
    tracer.log("game_move", "White", "Place stone at F5", move="F5", turn=2)
    tracer.log("game_move", "Black", "Place stone at C3", move="C3", turn=3)
    tracer.log("game_move", "White", "Pass", move="pass", turn=4)
    tracer.log("game_move", "Black", "Pass", move="pass", turn=5)
    tracer.log("output", "GoAgent", "Black wins by 4.5 points (komi 6.5). B+4.5", winner="Black")
    tracer.end_trace("completed")

    tracer.start_trace("Checkers: Red vs Black")
    tracer.log("input", "CheckersAgent", "Starting checkers. Red moves first.", game="checkers")
    tracer.log("game_move", "Red", "Move c3-d4", move="c3-d4", turn=1)
    tracer.log("game_move", "Black", "Move f6-e5", move="f6-e5", turn=2)
    tracer.log("game_move", "Red", "Jump d4-f6 (captures e5)", move="d4xf6", turn=3, capture=True)
    tracer.log("output", "CheckersAgent", "Red wins after 24 moves.", winner="Red", total_moves=24)
    tracer.end_trace("completed")

    tracer.start_trace("Connect4: Vertical Win")
    tracer.log("input", "Connect4Agent", "Starting Connect 4. Red drops first.", game="connect4")
    tracer.log("game_move", "Red", "Drop in column 3", column=3, turn=1)
    tracer.log("game_move", "Yellow", "Drop in column 4", column=4, turn=2)
    tracer.log("game_move", "Red", "Drop in column 3", column=3, turn=3)
    tracer.log("game_move", "Yellow", "Drop in column 5", column=5, turn=4)
    tracer.log("game_move", "Red", "Drop in column 3", column=3, turn=5)
    tracer.log("game_move", "Yellow", "Drop in column 6", column=6, turn=6)
    tracer.log("game_move", "Red", "Drop in column 3 - wins!", column=3, turn=7)
    tracer.log("output", "Connect4Agent", "Red wins with vertical 4 in column 3.", winner="Red")
    tracer.end_trace("completed")

    tracer.start_trace("Battleship: Naval Combat")
    tracer.log("input", "BattleshipAgent", "Starting Battleship. Players place ships.", game="battleship")
    tracer.log("game_move", "Player1", "Fire at B3 - Miss", target="B3", result="miss", turn=1)
    tracer.log("game_move", "Player2", "Fire at E5 - Hit!", target="E5", result="hit", turn=2)
    tracer.log("game_move", "Player1", "Fire at D7 - Hit! Destroyer sunk!", target="D7", result="sunk", ship="Destroyer")
    tracer.log("output", "BattleshipAgent", "Player 1 wins. All enemy ships sunk in 32 shots.", winner="Player1")
    tracer.end_trace("completed")

    tracer.start_trace("Reversi: Territory Control")
    tracer.log("input", "ReversiAgent", "Starting Reversi (Othello). Black places first.", game="reversi")
    tracer.log("game_move", "Black", "Place at D3, flips 1 piece", move="D3", flipped=1, turn=1)
    tracer.log("game_move", "White", "Place at C3, flips 1 piece", move="C3", flipped=1, turn=2)
    tracer.log("output", "ReversiAgent", "White wins 38-26.", winner="White", black=26, white=38)
    tracer.end_trace("completed")

    tracer.start_trace("Mancala: Seed Strategy")
    tracer.log("input", "MancalaAgent", "Starting Mancala. 4 stones per pit.", game="mancala")
    tracer.log("game_move", "Player1", "Sow from pit 3 (extra turn)", pit=3, turn=1)
    tracer.log("game_move", "Player1", "Sow from pit 5", pit=5, turn=2)
    tracer.log("game_move", "Player2", "Sow from pit 9", pit=9, turn=3)
    tracer.log("output", "MancalaAgent", "Player 1 wins 28-20.", winner="Player1", score_p1=28, score_p2=20)
    tracer.end_trace("completed")

    tracer.start_trace("Poker: Texas Hold'em")
    tracer.log("input", "PokerAgent", "Dealing to 4 players. Blinds: 1/2", game="poker", players=4)
    tracer.log("game_move", "Player1", "Dealt AhKh. Raise to 6", hand="AhKh", action="raise")
    tracer.log("game_move", "Player2", "Dealt 9s9d. Call", hand="9s9d", action="call")
    tracer.log("game_move", "Dealer", "Flop: Kd 9h 4c", community="Kd9h4c", street="flop")
    tracer.log("output", "PokerAgent", "Player1 wins with Kings full. Pot: 82", winner="Player1")
    tracer.end_trace("completed")

    tracer.start_trace("Hold'em: Heads Up")
    tracer.log("input", "HoldemAgent", "Heads-up Hold'em. Blinds: 5/10", game="holdem", players=2)
    tracer.log("game_move", "Player1", "Dealt AsKs. Raise to 30", action="raise")
    tracer.log("game_move", "Player2", "Dealt QhJh. Call", action="call")
    tracer.log("game_move", "Dealer", "Board: Ks Qd 7c 2s Ah", street="showdown")
    tracer.log("output", "HoldemAgent", "Player1 wins with two pair Aces and Kings.", winner="Player1")
    tracer.end_trace("completed")

    tracer.start_trace("Dominoes: Tile Matching")
    tracer.log("input", "DominoesAgent", "Starting Dominoes. 7 tiles each.", game="dominoes", players=4)
    tracer.log("game_move", "Player1", "Play [6|6] double six", tile="6-6", turn=1)
    tracer.log("game_move", "Player2", "Play [6|4]", tile="6-4", turn=2)
    tracer.log("game_move", "Player3", "Play [6|2]", tile="6-2", turn=3)
    tracer.log("output", "DominoesAgent", "Player1 wins by going out first. Score: 42 points.", winner="Player1")
    tracer.end_trace("completed")

    tracer.start_trace("Risk: World Domination")
    tracer.log("input", "RiskAgent", "Starting Risk. 4 players. Random territories.", game="risk", players=4)
    tracer.log("game_move", "Red", "Attack Ukraine from Southern Europe (3v2)", action="attack", turn=1)
    tracer.log("game_move", "Blue", "Fortify North Africa from Brazil", action="fortify", turn=2)
    tracer.log("output", "RiskAgent", "Red conquers all territories after 45 rounds.", winner="Red", rounds=45)
    tracer.end_trace("completed")

    tracer.start_trace("Monopoly: Property Trading")
    tracer.log("input", "MonopolyAgent", "Starting Monopoly. 4 players. $1500 each.", game="monopoly", players=4)
    tracer.log("game_move", "Player1", "Roll 7. Buy Boardwalk ($400)", action="buy", property="Boardwalk")
    tracer.log("game_move", "Player2", "Roll 5. Pay rent $50 on St. James Place", action="pay_rent")
    tracer.log("output", "MonopolyAgent", "Player1 wins. All others bankrupt.", winner="Player1")
    tracer.end_trace("completed")

    tracer.start_trace("Nim: Mathematical Strategy")
    tracer.log("input", "NimAgent", "Starting Nim. Heaps: [3, 5, 7]", game="nim")
    tracer.log("game_move", "Player1", "Take 2 from heap 2 -> [3, 3, 7]", heap=2, take=2, turn=1)
    tracer.log("game_move", "Player2", "Take 4 from heap 3 -> [3, 3, 3]", heap=3, take=4, turn=2)
    tracer.log("game_move", "Player1", "Take 3 from heap 1 -> [0, 3, 3]", heap=1, take=3, turn=3)
    tracer.log("output", "NimAgent", "Player1 wins by taking last object.", winner="Player1")
    tracer.end_trace("completed")

    tracer.start_trace("Fox & Geese: Asymmetric Pursuit")
    tracer.log("input", "FoxAndGeeseAgent", "Starting Fox & Geese. Fox vs 13 Geese.", game="fox_and_geese")
    tracer.log("game_move", "Fox", "Move to D5 (center)", move="D5", turn=1)
    tracer.log("game_move", "Geese", "Advance goose from E7 to E6", move="E7-E6", turn=2)
    tracer.log("game_move", "Fox", "Jump over goose at E6 to E5", move="D5xE6", capture=True)
    tracer.log("output", "FoxAndGeeseAgent", "Fox wins by escaping the geese.", winner="Fox")
    tracer.end_trace("completed")

    tracer.start_trace("Mafia: Social Deduction")
    tracer.log("input", "MafiaAgent", "Starting Mafia. 8 players: 2 Mafia, 1 Doctor, 1 Detective, 4 Townspeople.", game="mafia", players=8)
    tracer.log("game_move", "Night", "Mafia eliminates Player 5", phase="night", turn=1)
    tracer.log("game_move", "Day", "Town votes to eliminate Player 3 (Mafia!)", phase="day", turn=2, vote="Player3")
    tracer.log("game_move", "Night", "Doctor saves Player 2. Detective checks Player 7 (Town).", phase="night", turn=3)
    tracer.log("output", "MafiaAgent", "Town wins! All Mafia eliminated.", winner="Town", rounds=4)
    tracer.end_trace("completed")

    tracer.start_trace("Among Us: Impostor Hunt")
    tracer.log("input", "AmongUsAgent", "Starting Among Us. 8 crew, 2 impostors.", game="among_us", players=10)
    tracer.log("game_move", "Impostor1", "Sabotage reactor. Kill Crew3 in Electrical.", action="kill", location="Electrical")
    tracer.log("game_move", "Crew5", "Report body! Emergency meeting called.", action="report")
    tracer.log("game_move", "Vote", "Crew votes to eject Impostor1. 1 impostor remains.", action="eject")
    tracer.log("output", "AmongUsAgent", "Crew wins! Both impostors ejected.", winner="Crew")
    tracer.end_trace("completed")

    tracer.start_trace("Clue: Murder Mystery")
    tracer.log("input", "ClueAgent", "Starting Clue. 4 players investigating murder.", game="clue", players=4)
    tracer.log("game_move", "Col.Mustard", "Move to Kitchen. Suggest: Prof.Plum, Candlestick, Kitchen", room="Kitchen", turn=1)
    tracer.log("game_move", "Mrs.White", "Disprove: shows Candlestick card", action="disprove")
    tracer.log("game_move", "Col.Mustard", "Accuse: Prof.Plum, Wrench, Library - Correct!", action="accuse")
    tracer.log("output", "ClueAgent", "Col.Mustard solves it: Prof.Plum with the Wrench in the Library.", winner="Col.Mustard")
    tracer.end_trace("completed")

    tracer.start_trace("Mastermind: Code Breaking")
    tracer.log("input", "MastermindAgent", "Starting Mastermind. Secret: 4-color code.", game="mastermind")
    tracer.log("game_move", "Codebreaker", "Guess: RGBY -> 1 black, 1 white peg", guess="RGBY", black=1, white=1, turn=1)
    tracer.log("game_move", "Codebreaker", "Guess: GRYB -> 2 black, 1 white peg", guess="GRYB", black=2, white=1, turn=2)
    tracer.log("game_move", "Codebreaker", "Guess: GRBY -> 4 black pegs! Solved!", guess="GRBY", black=4, turn=3)
    tracer.log("output", "MastermindAgent", "Code cracked in 3 guesses!", winner="Codebreaker", guesses=3)
    tracer.end_trace("completed")

    tracer.start_trace("Debate: AI Ethics")
    tracer.log("input", "DebateAgent", "Topic: Should AI have rights?", game="debate")
    tracer.log("game_move", "Pro", "Opening: AI consciousness may emerge from complexity...", phase="opening")
    tracer.log("game_move", "Con", "Opening: Rights require sentience, which AI lacks...", phase="opening")
    tracer.log("game_move", "Pro", "Rebuttal: Functional consciousness suffices for moral status...", phase="rebuttal")
    tracer.log("output", "DebateAgent", "Judge rules: Con wins on stronger evidence basis.", winner="Con")
    tracer.end_trace("completed")

    tracer.start_trace("Debate V2: Climate Policy")
    tracer.log("input", "GameDebateAgent", "Topic: Carbon tax vs cap-and-trade.", game="debate_v2")
    tracer.log("llm_call", "Advocate1", "Carbon tax provides price certainty and simplicity...", phase="argument")
    tracer.log("llm_call", "Advocate2", "Cap-and-trade ensures emission targets are met...", phase="argument")
    tracer.log("output", "GameDebateAgent", "Panel scores: Carbon tax 7.2/10, Cap-and-trade 7.5/10.", winner="Cap-and-trade")
    tracer.end_trace("completed")

    tracer.start_trace("Debate V2 (Judges): Space Exploration")
    tracer.log("input", "JudgedDebateAgent", "Topic: Mars colonization priority. 3 judges.", game="debate_v2_judges")
    tracer.log("llm_call", "Pro", "Humanity needs multi-planetary backup for survival...", phase="opening")
    tracer.log("llm_call", "Con", "Resources better spent on Earth's climate crisis...", phase="opening")
    tracer.log("llm_call", "Judge1", "Score: Pro 8/10, Con 7/10", phase="scoring")
    tracer.log("llm_call", "Judge2", "Score: Pro 7/10, Con 8/10", phase="scoring")
    tracer.log("llm_call", "Judge3", "Score: Pro 8/10, Con 7/10", phase="scoring")
    tracer.log("output", "JudgedDebateAgent", "Pro wins 2-1 on judges' scorecards.", winner="Pro")
    tracer.end_trace("completed")

    # ── AGENT TRACES (37 agents) ────────────────────────────────────

    tracer.start_trace("SimpleAgent: Conversation")
    tracer.log("input", "SimpleAgent", "Tell me about quantum computing in 2 sentences.", agent_type="simple")
    tracer.log("llm_call", "SimpleAgent", "Generating response...", tokens_in=28, tokens_out=64)
    tracer.log("output", "SimpleAgent", "Quantum computing uses qubits that can exist in superposition. It promises exponential speedups for certain problems like cryptography and drug discovery.")
    tracer.end_trace("completed")

    tracer.start_trace("ReactAgent: Calculator Tool")
    tracer.log("input", "ReactAgent", "What is the square root of 1764?", agent_type="react")
    tracer.log("llm_call", "ReactAgent", "I need to calculate sqrt(1764). Using calculator tool.", tokens_in=35, tokens_out=48)
    tracer.log("tool_call", "calculator", "sqrt(1764) = 42.0", tool="calculator")
    tracer.log("llm_call", "ReactAgent", "The calculator returned 42. Formulating response.", tokens_in=85, tokens_out=32)
    tracer.log("output", "ReactAgent", "The square root of 1764 is 42.")
    tracer.end_trace("completed")

    tracer.start_trace("DynamicSupervisor: Task Delegation")
    tracer.log("input", "DynamicSupervisor", "Analyze sales data, create chart, write report.", agent_type="supervisor")
    tracer.log("llm_call", "DynamicSupervisor", "Breaking task into 3 subtasks. Spawning agents.", tokens_in=52, tokens_out=120)
    tracer.log("llm_call", "DataAnalyst", "Analyzing sales CSV. Found 15% growth YoY.", tokens_in=2400, tokens_out=340)
    tracer.log("llm_call", "Visualizer", "Creating bar chart of quarterly sales.", tokens_in=180, tokens_out=95)
    tracer.log("llm_call", "ReportWriter", "Writing executive summary with key findings.", tokens_in=480, tokens_out=620)
    tracer.log("output", "DynamicSupervisor", "Report complete. 3 agents used. Total tokens: 4287.")
    tracer.end_trace("completed")

    # RAG agents
    for name, desc in [
        ("AdaptiveRAG", "Routes to optimal retrieval strategy"),
        ("CorrectiveRAG", "Self-correcting with document grading"),
        ("FLARE_RAG", "Forward-looking active retrieval"),
        ("FusionRAG", "Multi-query fusion retrieval"),
        ("HyDE_RAG", "Hypothetical document embeddings"),
        ("MultiQueryRAG", "Generates multiple query variants"),
        ("SelfRouteRAG", "Self-routing between strategies"),
        ("SpeculativeRAG", "Hypothesis-driven retrieval"),
        ("StepBackRAG", "Abstraction-based prompting"),
        ("MemoryAwareRAG", "RAG with persistent memory"),
        ("DocGradingRAG", "Relevance-based document grading"),
        ("AgenticRAG", "Tool-augmented RAG"),
        ("FilteredRAG", "Metadata-filtered retrieval"),
        ("HallucinationGrader", "Detects hallucinations in output"),
        ("QueryDecomposer", "Decomposes complex queries"),
    ]:
        tracer.start_trace(f"{name}: {desc}")
        tracer.log("input", name, f"Query: What are the benefits of RAG?", agent_type="rag")
        tracer.log("tool_call", "retriever", f"{name} retrieving 5 relevant documents...", tool="vector_search", k=5)
        tracer.log("llm_call", name, f"Synthesizing answer from retrieved documents.", tokens_in=1800, tokens_out=250)
        tracer.log("output", name, f"RAG-augmented answer generated with 5 source documents. Confidence: 0.92")
        tracer.end_trace("completed")

    # Reasoning agents
    tracer.start_trace("SelfDiscover: Reasoning Structure")
    tracer.log("input", "SelfDiscover", "Design a sorting algorithm for nearly-sorted arrays.", agent_type="reasoning")
    tracer.log("llm_call", "SelfDiscover", "Discovering reasoning modules: [decomposition, optimization, comparison]", phase="select")
    tracer.log("llm_call", "SelfDiscover", "Adapting modules to sorting problem context", phase="adapt")
    tracer.log("llm_call", "SelfDiscover", "Implementing: Insertion sort is optimal for nearly-sorted data (O(n) best case)", phase="implement")
    tracer.log("output", "SelfDiscover", "Recommended: Insertion sort. Reasoning: nearly-sorted implies few inversions.")
    tracer.end_trace("completed")

    tracer.start_trace("Reflection: Essay Improvement")
    tracer.log("input", "ReflectionAgent", "Write and improve an essay about renewable energy.", agent_type="reasoning")
    tracer.log("llm_call", "ReflectionAgent", "Draft 1: Basic essay about solar and wind energy.", phase="generate")
    tracer.log("llm_call", "ReflectionAgent", "Critique: Lacks specific data, needs stronger conclusion.", phase="reflect")
    tracer.log("llm_call", "ReflectionAgent", "Draft 2: Added statistics, strengthened argument.", phase="revise")
    tracer.log("output", "ReflectionAgent", "Final essay: 450 words, 2 revision cycles. Quality: 8.5/10")
    tracer.end_trace("completed")

    tracer.start_trace("Reflexion: Code Debugging")
    tracer.log("input", "ReflexionAgent", "Fix the bug in this binary search implementation.", agent_type="reasoning")
    tracer.log("llm_call", "ReflexionAgent", "Attempt 1: Fixed off-by-one in mid calculation.", phase="act")
    tracer.log("llm_call", "ReflexionAgent", "Test failed: still returns -1 for existing elements.", phase="evaluate")
    tracer.log("llm_call", "ReflexionAgent", "Reflection: boundary condition wrong. Fix: use <= not <", phase="reflect")
    tracer.log("llm_call", "ReflexionAgent", "Attempt 2: Changed while condition. All tests pass.", phase="act")
    tracer.log("output", "ReflexionAgent", "Bug fixed in 2 attempts. Root cause: incorrect loop termination.")
    tracer.end_trace("completed")

    tracer.start_trace("TreeOfThought: Problem Solving")
    tracer.log("input", "ToTAgent", "Solve: 24 game with numbers 1, 5, 5, 5", agent_type="reasoning")
    tracer.log("llm_call", "ToTAgent", "Branch 1: 5*(5-1/5) = 24. Evaluating...", phase="expand", branch=1)
    tracer.log("llm_call", "ToTAgent", "Branch 2: (5-1)*5+5 = 25. Not 24. Prune.", phase="evaluate", branch=2)
    tracer.log("llm_call", "ToTAgent", "Branch 1 verified: 5*(5-1/5) = 5*4.8 = 24. Correct!", phase="verify")
    tracer.log("output", "ToTAgent", "Solution: 5*(5-1/5) = 24. Found in 3 branches explored.")
    tracer.end_trace("completed")

    tracer.start_trace("LATS: Language Agent Tree Search")
    tracer.log("input", "LATSAgent", "Find optimal route visiting 5 cities.", agent_type="reasoning")
    tracer.log("llm_call", "LATSAgent", "Generating initial solutions via sampling...", phase="sample")
    tracer.log("llm_call", "LATSAgent", "Scoring 4 candidates. Best: A-C-B-E-D (cost: 142)", phase="evaluate")
    tracer.log("llm_call", "LATSAgent", "Expanding best node. New candidate: A-C-E-B-D (cost: 138)", phase="expand")
    tracer.log("output", "LATSAgent", "Optimal route: A-C-E-B-D. Cost: 138. Nodes explored: 12.")
    tracer.end_trace("completed")

    tracer.start_trace("MCTS: Monte Carlo Reasoning")
    tracer.log("input", "MCTSAgent", "Evaluate chess position for best move.", agent_type="reasoning")
    tracer.log("llm_call", "MCTSAgent", "Selection: UCB1 selects Nf3 branch.", phase="select", simulations=100)
    tracer.log("llm_call", "MCTSAgent", "Expansion: Adding Bg5 node.", phase="expand")
    tracer.log("llm_call", "MCTSAgent", "Simulation: Nf3 wins 62/100 playouts.", phase="simulate")
    tracer.log("output", "MCTSAgent", "Best move: Nf3 (62% win rate, 500 simulations).")
    tracer.end_trace("completed")

    tracer.start_trace("LogicAgent: Formal Reasoning")
    tracer.log("input", "LogicAgent", "If all dogs are mammals and Rex is a dog, what is Rex?", agent_type="reasoning")
    tracer.log("llm_call", "LogicAgent", "Premise 1: All dogs are mammals. Premise 2: Rex is a dog.", phase="parse")
    tracer.log("llm_call", "LogicAgent", "Applying modus ponens: dog(Rex) -> mammal(Rex)", phase="infer")
    tracer.log("output", "LogicAgent", "Conclusion: Rex is a mammal. Proof: modus ponens on universal quantifier.")
    tracer.end_trace("completed")

    # Planning agents
    tracer.start_trace("PlanAndExecute: Project Plan")
    tracer.log("input", "PlanAndExecuteAgent", "Plan a website redesign project.", agent_type="planning")
    tracer.log("llm_call", "Planner", "Creating plan: 1) Audit current site 2) Design mockups 3) Develop 4) Test 5) Deploy", phase="plan")
    tracer.log("llm_call", "Executor", "Step 1: Auditing current site... Found 12 UX issues.", phase="execute", step=1)
    tracer.log("llm_call", "Executor", "Step 2: Creating 3 design mockups...", phase="execute", step=2)
    tracer.log("output", "PlanAndExecuteAgent", "Plan complete. 5 steps, 2 executed. Est. time: 6 weeks.")
    tracer.end_trace("completed")

    tracer.start_trace("ReWOO V3: Reasoning Without Observation")
    tracer.log("input", "ReWOOV3Agent", "Compare GDP of France and Germany.", agent_type="planning")
    tracer.log("llm_call", "ReWOOV3", "Plan: #E1=Search[France GDP] #E2=Search[Germany GDP] #E3=Compare[#E1,#E2]", phase="plan")
    tracer.log("tool_call", "search", "France GDP: $2.78T (2024)", tool="web_search")
    tracer.log("tool_call", "search", "Germany GDP: $4.07T (2024)", tool="web_search")
    tracer.log("output", "ReWOOV3Agent", "Germany GDP ($4.07T) exceeds France ($2.78T) by 46%.")
    tracer.end_trace("completed")

    tracer.start_trace("LLMCompiler V3: Task Compilation")
    tracer.log("input", "LLMCompilerV3Agent", "Analyze competitor pricing across 3 markets.", agent_type="planning")
    tracer.log("llm_call", "LLMCompilerV3", "Compiling parallel execution DAG for 3 market analyses.", phase="compile")
    tracer.log("llm_call", "Worker1", "US market analysis complete.", phase="execute")
    tracer.log("llm_call", "Worker2", "EU market analysis complete.", phase="execute")
    tracer.log("llm_call", "Worker3", "APAC market analysis complete.", phase="execute")
    tracer.log("output", "LLMCompilerV3Agent", "3 markets analyzed in parallel. Average price delta: -12%.")
    tracer.end_trace("completed")

    tracer.start_trace("PlanExecute V3: Enhanced Planning")
    tracer.log("input", "PlanExecuteV3Agent", "Organize a company hackathon.", agent_type="planning")
    tracer.log("llm_call", "PlanExecuteV3", "Plan: 8 tasks generated. Evaluating feasibility.", phase="plan")
    tracer.log("llm_call", "PlanExecuteV3", "Executing task 1: Book venue. Status: Complete.", phase="execute", step=1)
    tracer.log("llm_call", "PlanExecuteV3", "Re-evaluating plan after task 1. Adjusting timeline.", phase="replan")
    tracer.log("output", "PlanExecuteV3Agent", "Hackathon planned. 8 tasks, 3 completed, 5 scheduled.")
    tracer.end_trace("completed")

    # Research agents
    tracer.start_trace("OpenPerplexity: Web Research")
    tracer.log("input", "ResearchAgent", "What is the current state of quantum computing?", agent_type="research")
    tracer.log("tool_call", "web_search", "Searching: quantum computing 2025 breakthroughs", tool="web_search")
    tracer.log("tool_call", "web_search", "Searching: quantum error correction latest", tool="web_search")
    tracer.log("llm_call", "ResearchAgent", "Synthesizing 8 sources into comprehensive answer.", tokens_in=4200, tokens_out=850)
    tracer.log("output", "ResearchAgent", "Comprehensive answer with 8 citations. Key finding: 1000+ qubit systems now operational.")
    tracer.end_trace("completed")

    tracer.start_trace("PersonResearch: Profile Building")
    tracer.log("input", "PersonResearchAgent", "Research Yann LeCun's contributions to AI.", agent_type="research")
    tracer.log("tool_call", "web_search", "Searching: Yann LeCun research papers contributions", tool="web_search")
    tracer.log("llm_call", "PersonResearchAgent", "Building profile from 5 sources.", tokens_in=3200, tokens_out=640)
    tracer.log("output", "PersonResearchAgent", "Profile: VP & Chief AI Scientist at Meta. Turing Award 2018. Pioneer of CNNs.")
    tracer.end_trace("completed")

    # Conversation agents
    tracer.start_trace("BaseConversation: Multi-Turn")
    tracer.log("input", "BaseConversation", "Topic: Future of remote work. 3 participants.", agent_type="conversation")
    tracer.log("llm_call", "Manager", "Remote work has transformed how we collaborate...", turn=1)
    tracer.log("llm_call", "Engineer", "I agree, but I miss spontaneous hallway conversations...", turn=2)
    tracer.log("llm_call", "HR_Lead", "We need to balance flexibility with team cohesion...", turn=3)
    tracer.log("output", "BaseConversation", "Conversation concluded after 3 turns. Consensus: hybrid model preferred.")
    tracer.end_trace("completed")

    tracer.start_trace("Collaborative: Problem Solving")
    tracer.log("input", "CollaborativeConversation", "Topic: Design a sustainable city. 4 experts.", agent_type="conversation")
    tracer.log("llm_call", "Architect", "Green building standards and mixed-use zoning...", turn=1)
    tracer.log("llm_call", "Engineer", "Smart grid with renewable energy integration...", turn=2)
    tracer.log("llm_call", "Urbanist", "15-minute neighborhood concept reduces car dependency...", turn=3)
    tracer.log("llm_call", "Ecologist", "Urban forests and bioswales for water management...", turn=4)
    tracer.log("output", "CollaborativeConversation", "Collaborative plan created with 4 expert perspectives.")
    tracer.end_trace("completed")

    tracer.start_trace("DebateConversation: AI Regulation")
    tracer.log("input", "DebateConversation", "Topic: Should AI be regulated?", agent_type="conversation")
    tracer.log("llm_call", "ProRegulation", "AI poses risks requiring government oversight...", phase="opening")
    tracer.log("llm_call", "AntiRegulation", "Innovation requires freedom from heavy regulation...", phase="opening")
    tracer.log("llm_call", "ProRegulation", "Rebuttal: Industry self-regulation has failed...", phase="rebuttal")
    tracer.log("llm_call", "AntiRegulation", "Rebuttal: Regulators lack technical expertise...", phase="rebuttal")
    tracer.log("output", "DebateConversation", "Debate concluded. Judge: Draw with slight edge to pro-regulation.", rounds=3)
    tracer.end_trace("completed")

    tracer.start_trace("Directed: Classroom Discussion")
    tracer.log("input", "DirectedConversation", "Teacher asks students about photosynthesis.", agent_type="conversation")
    tracer.log("llm_call", "Teacher", "Alice, can you explain the light reactions?", turn=1)
    tracer.log("llm_call", "Alice", "Light reactions convert sunlight into ATP and NADPH...", turn=2)
    tracer.log("llm_call", "Teacher", "Good! Bob, what about the Calvin cycle?", turn=3)
    tracer.log("llm_call", "Bob", "The Calvin cycle fixes CO2 into glucose using ATP...", turn=4)
    tracer.log("output", "DirectedConversation", "All students participated. 6 turns, 3 students engaged.")
    tracer.end_trace("completed")

    tracer.start_trace("SocialMedia: Twitter Thread")
    tracer.log("input", "SocialMediaConversation", "Topic: AI startups. Platform: Twitter.", agent_type="conversation")
    tracer.log("llm_call", "@TechFounder", "Just raised $50M for our AI agent startup! #AIStartups", turn=1)
    tracer.log("llm_call", "@VCPartner", "@TechFounder Congrats! What's your moat? #investing", turn=2)
    tracer.log("llm_call", "@TechFounder", "@VCPartner Our proprietary training data. 10x better than GPT-4 on domain tasks", turn=3)
    tracer.log("output", "SocialMediaConversation", "Thread: 8 posts, 24 likes. @TechFounder went viral!", viral=True)
    tracer.end_trace("completed")

    tracer.start_trace("RoundRobin: Team Standup")
    tracer.log("input", "RoundRobinConversation", "Daily standup. 4 team members.", agent_type="conversation")
    tracer.log("llm_call", "Dev1", "Yesterday: Finished auth module. Today: Starting API tests.", turn=1)
    tracer.log("llm_call", "Dev2", "Yesterday: Fixed 3 bugs. Today: Code review. Blocker: CI pipeline down.", turn=2)
    tracer.log("llm_call", "Designer", "Yesterday: Finalized mockups. Today: Design system update.", turn=3)
    tracer.log("llm_call", "PM", "Thanks all. I'll look into the CI issue. Sprint on track.", turn=4)
    tracer.log("output", "RoundRobinConversation", "Standup complete. 4 updates, 1 blocker identified.")
    tracer.end_trace("completed")

    # Error trace
    tracer.start_trace("SimpleAgent: Auth Failure")
    tracer.log("input", "SimpleAgent", "Test query requiring API key", agent_type="simple")
    tracer.log("llm_call", "SimpleAgent", "Attempting LLM call to gpt-4o-mini...")
    tracer.log("error", "SimpleAgent", "AuthenticationError: Invalid API key. Check OPENAI_API_KEY.", error_type="AuthenticationError")
    tracer.end_trace("error")
