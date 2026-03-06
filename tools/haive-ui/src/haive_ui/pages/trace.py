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

    # Clear traces
    if st.button("Clear All Traces", type="secondary"):
        st.session_state.tracer = TraceCollector()
        st.rerun()
