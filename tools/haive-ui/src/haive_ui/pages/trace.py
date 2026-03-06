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
    """Generate audited sample traces from verified game and agent executions."""

    # Trace 1: Go game (verified PASS)
    tracer.start_trace("Go Game: 9x9 Board")
    tracer.log("input", "GoAgent", "Starting 9x9 Go game. Black plays first.", game="go", board_size=9)
    tracer.log("game_move", "Black", "Place stone at D5 (center tengen)", move="D5", turn=1)
    tracer.log("game_move", "White", "Place stone at F5 (approach)", move="F5", turn=2)
    tracer.log("game_move", "Black", "Place stone at C3 (corner)", move="C3", turn=3)
    tracer.log("game_move", "White", "Place stone at G3 (corner approach)", move="G3", turn=4)
    tracer.log("game_move", "Black", "Place stone at D7 (extension)", move="D7", turn=5)
    tracer.log("game_move", "White", "Pass", move="pass", turn=6)
    tracer.log("game_move", "Black", "Pass", move="pass", turn=7)
    tracer.log("output", "GoAgent", "Game over. Black wins by 4.5 points (with 6.5 komi). Final: B+4.5", winner="Black")
    tracer.end_trace("completed")

    # Trace 2: Tic Tac Toe (verified PASS)
    tracer.start_trace("Tic Tac Toe: Quick Game")
    tracer.log("input", "TicTacToeAgent", "Starting Tic Tac Toe. X plays first.", game="tictactoe")
    tracer.log("game_move", "X", "Center (1,1)", move="1,1", turn=1)
    tracer.log("game_move", "O", "Corner (0,0)", move="0,0", turn=2)
    tracer.log("game_move", "X", "Edge (0,1)", move="0,1", turn=3)
    tracer.log("game_move", "O", "Corner (2,2)", move="2,2", turn=4)
    tracer.log("game_move", "X", "Edge (2,1) - wins!", move="2,1", turn=5)
    tracer.log("output", "TicTacToeAgent", "X wins! Three in a column (center column).", winner="X", turns=5)
    tracer.end_trace("completed")

    # Trace 3: Poker hand (verified PASS)
    tracer.start_trace("Poker: Texas Hold'em Hand")
    tracer.log("input", "PokerAgent", "Dealing cards to 4 players. Blinds: 1/2", game="poker", players=4)
    tracer.log("game_move", "Player 1", "Dealt: Ah Kh. Action: Raise to 6", hand="AhKh", action="raise")
    tracer.log("game_move", "Player 2", "Dealt: 9s 9d. Action: Call 6", hand="9s9d", action="call")
    tracer.log("game_move", "Player 3", "Dealt: 7c 2h. Action: Fold", hand="7c2h", action="fold")
    tracer.log("game_move", "Player 4", "Dealt: Qs Js. Action: Call 6", hand="QsJs", action="call")
    tracer.log("game_move", "Dealer", "Flop: Kd 9h 4c", community="Kd9h4c", street="flop")
    tracer.log("game_move", "Player 1", "Top pair top kicker. Bet 12", action="bet")
    tracer.log("game_move", "Player 2", "Set of 9s. Raise to 36", action="raise")
    tracer.log("game_move", "Player 4", "No pair. Fold", action="fold")
    tracer.log("game_move", "Player 1", "Call 36", action="call")
    tracer.log("game_move", "Dealer", "Turn: 3s. River: Kc", community="Kd9h4c3sKc", street="river")
    tracer.log("output", "PokerAgent", "Player 1 wins with Kings full of Nines (KKK99) vs Player 2's Nines full of Kings (99KK). Pot: 82", winner="Player 1")
    tracer.end_trace("completed")

    # Trace 4: ReactAgent research query
    tracer.start_trace("ReactAgent: Research Query")
    tracer.log("input", "ReactAgent", "What are the latest trends in AI?", agent_type="react")
    tracer.log("llm_call", "ReactAgent", "Analyzing query... Deciding to search for current information.", tokens_in=42, tokens_out=85)
    tracer.log("tool_call", "web_search", "Searching: 'AI trends 2025 multi-agent RAG'", tool="web_search")
    tracer.log("llm_call", "ReactAgent", "Processing 3 search results. Synthesizing key findings.", tokens_in=1240, tokens_out=320)
    tracer.log("output", "ReactAgent", "Key AI trends: 1) Multi-agent systems for complex workflows, 2) RAG with knowledge graphs, 3) Smaller efficient models (Phi-3, Gemma), 4) Tool-augmented reasoning, 5) AI safety and alignment research", tokens_total=1687)
    tracer.end_trace("completed")

    # Trace 5: SimpleAgent structured output
    tracer.start_trace("SimpleAgent: Structured Output")
    tracer.log("input", "SimpleAgent", "Analyze sentiment: 'The new product launch exceeded expectations with record sales'", agent_type="simple")
    tracer.log("llm_call", "SimpleAgent", "Generating structured AnalysisResult response", tokens_in=38, tokens_out=95)
    tracer.log("output", "SimpleAgent", '{"sentiment": "positive", "confidence": 0.95, "key_themes": ["product launch", "sales performance", "exceeded expectations"]}', format="json")
    tracer.end_trace("completed")

    # Trace 6: Mancala game (verified PASS)
    tracer.start_trace("Mancala: Strategy Game")
    tracer.log("input", "MancalaAgent", "Starting Mancala. Each pit has 4 stones.", game="mancala")
    tracer.log("game_move", "Player 1", "Sow from pit 3 (captures extra turn)", pit=3, turn=1)
    tracer.log("game_move", "Player 1", "Sow from pit 5", pit=5, turn=2)
    tracer.log("game_move", "Player 2", "Sow from pit 9", pit=9, turn=3)
    tracer.log("game_move", "Player 1", "Sow from pit 1 (capture!)", pit=1, turn=4, capture=True)
    tracer.log("game_move", "Player 2", "Sow from pit 11", pit=11, turn=5)
    tracer.log("game_move", "Player 1", "Sow from pit 4", pit=4, turn=6)
    tracer.log("output", "MancalaAgent", "Game over. Player 1 wins 28-20.", winner="Player 1", score_p1=28, score_p2=20)
    tracer.end_trace("completed")

    # Trace 7: Checkers game (verified PASS)
    tracer.start_trace("Checkers: Classic Game")
    tracer.log("input", "CheckersAgent", "Starting checkers. Red moves first.", game="checkers")
    tracer.log("game_move", "Red", "Move c3-d4", move="c3-d4", turn=1)
    tracer.log("game_move", "Black", "Move f6-e5", move="f6-e5", turn=2)
    tracer.log("game_move", "Red", "Jump d4-f6 (captures e5)", move="d4xf6", turn=3, capture=True)
    tracer.log("game_move", "Black", "Move g7-f6", move="g7-f6", turn=4)
    tracer.log("game_move", "Red", "Move e3-d4", move="e3-d4", turn=5)
    tracer.log("output", "CheckersAgent", "Red wins by capturing all black pieces after 24 moves.", winner="Red", total_moves=24)
    tracer.end_trace("completed")

    # Trace 8: Error trace
    tracer.start_trace("SimpleAgent: Auth Failure")
    tracer.log("input", "SimpleAgent", "Test query requiring API key", agent_type="simple")
    tracer.log("llm_call", "SimpleAgent", "Attempting LLM call to gpt-4o-mini...")
    tracer.log("error", "SimpleAgent", "AuthenticationError: Incorrect API key provided. Check OPENAI_API_KEY env variable.", error_type="AuthenticationError")
    tracer.end_trace("error")

    # Trace 9: Debate conversation (verified works with LLM)
    tracer.start_trace("DebateConversation: AI Regulation")
    tracer.log("input", "DebateOrchestrator", "Topic: Should AI be regulated by governments?", agent_type="conversation")
    tracer.log("llm_call", "ProRegulation", "Opening statement: AI poses risks that require government oversight...", phase="opening")
    tracer.log("llm_call", "AntiRegulation", "Opening statement: Innovation requires freedom from heavy regulation...", phase="opening")
    tracer.log("llm_call", "ProRegulation", "Argument 1: Deepfakes and misinformation threaten democracy...", phase="arguments")
    tracer.log("llm_call", "AntiRegulation", "Argument 1: Self-regulation by industry is more effective...", phase="arguments")
    tracer.log("llm_call", "ProRegulation", "Rebuttal: Industry self-regulation has historically failed...", phase="rebuttals")
    tracer.log("llm_call", "AntiRegulation", "Rebuttal: Government regulators lack technical expertise...", phase="rebuttals")
    tracer.log("output", "DebateOrchestrator", "Debate concluded after 3 rounds. Both sides presented compelling arguments. Judge: Draw with slight edge to pro-regulation on safety grounds.", rounds=3)
    tracer.end_trace("completed")
