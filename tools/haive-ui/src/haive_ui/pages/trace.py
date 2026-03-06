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
    """Generate sample traces for demonstration."""
    import time as _time

    # Sample: Chess game trace
    t1 = tracer.start_trace("Chess Game: gpt-4o vs gpt-4o-mini")
    tracer.log("input", "ChessAgent", "Starting chess game with default config")
    tracer.log("llm_call", "Player White", "Analyzing board position... Playing e2-e4")
    tracer.log("game_move", "Player White", "e2-e4 (King's Pawn Opening)")
    tracer.log("llm_call", "Player Black", "Responding to King's Pawn... Playing e7-e5")
    tracer.log("game_move", "Player Black", "e7-e5 (Open Game)")
    tracer.log("llm_call", "Player White", "Developing knight... Playing Ng1-f3")
    tracer.log("game_move", "Player White", "Ng1-f3 (King's Knight)")
    tracer.log("output", "ChessAgent", "Game completed after 32 moves. White wins by checkmate.")
    tracer.end_trace("completed")

    # Sample: Agent run trace
    t2 = tracer.start_trace("ReactAgent: research query")
    tracer.log("input", "ReactAgent", "What are the latest trends in AI?")
    tracer.log("llm_call", "ReactAgent", "Analyzing query, deciding to use web_search tool")
    tracer.log("tool_call", "web_search", "Searching: 'AI trends 2025'")
    tracer.log("llm_call", "ReactAgent", "Processing search results, formulating response")
    tracer.log("output", "ReactAgent", "Based on my research, the key AI trends are: 1) Multi-agent systems, 2) RAG improvements, 3) Smaller, faster models")
    tracer.end_trace("completed")

    # Sample: Error trace
    t3 = tracer.start_trace("SimpleAgent: failed query")
    tracer.log("input", "SimpleAgent", "Test query with missing API key")
    tracer.log("llm_call", "SimpleAgent", "Attempting LLM call...")
    tracer.log("error", "SimpleAgent", "AuthenticationError: Invalid API key provided")
    tracer.end_trace("error")
