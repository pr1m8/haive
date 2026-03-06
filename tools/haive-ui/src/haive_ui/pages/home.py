"""Home page - dashboard overview."""

import streamlit as st

from haive_ui.utils.registry import AGENT_REGISTRY, GAME_REGISTRY, get_agents_by_category, get_games_by_category


def render():
    st.title("Haive AI Agent Framework")
    st.markdown("**Dynamic agents, games, and multi-agent systems powered by LLMs.**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Agents", len(AGENT_REGISTRY))
    with col2:
        st.metric("Games", len(GAME_REGISTRY))
    with col3:
        st.metric("Agent Categories", len(get_agents_by_category()))
    with col4:
        st.metric("Game Categories", len(get_games_by_category()))

    st.divider()

    # Agent categories overview
    st.subheader("Agent Categories")
    for cat, agents in get_agents_by_category().items():
        with st.expander(f"**{cat.title()}** ({len(agents)} agents)"):
            for a in agents:
                st.markdown(f"- **{a.name}** — {a.description}")

    st.divider()

    # Game categories overview
    st.subheader("Game Categories")
    for cat, games in get_games_by_category().items():
        with st.expander(f"**{cat.replace('_', ' ').title()}** ({len(games)} games)"):
            for g in games:
                st.markdown(f"- **{g.name}** — {g.description} ({g.min_players}-{g.max_players} players)")

    st.divider()

    # Quick status check
    st.subheader("System Status")
    if st.button("Run Import Health Check"):
        _run_health_check()


def _run_health_check():
    """Quick import check for all registered components."""
    from haive_ui.utils.registry import try_import

    st.write("**Agents:**")
    ok = fail = 0
    for a in AGENT_REGISTRY:
        cls, err = try_import(a.module_path, a.class_name)
        if cls:
            ok += 1
        else:
            fail += 1
            st.error(f"  {a.name}: {err}")

    if fail == 0:
        st.success(f"All {ok} agents import OK")
    else:
        st.warning(f"{ok}/{ok + fail} agents import OK, {fail} failed")

    st.write("**Games:**")
    ok = fail = 0
    for g in GAME_REGISTRY:
        cls, err = try_import(g.module_path, g.class_name)
        if cls:
            ok += 1
        else:
            fail += 1
            st.error(f"  {g.name}: {err}")

    if fail == 0:
        st.success(f"All {ok} games import OK")
    else:
        st.warning(f"{ok}/{ok + fail} games import OK, {fail} failed")
